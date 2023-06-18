from __future__ import annotations

from typing import Any
from typing import Optional
from typing import Union

from numpy import arange
from numpy import array
from numpy import atleast_1d
from numpy import atleast_2d
from numpy import ndarray
from numpy import prod
from numpy import repeat
from numpy.typing import ArrayLike

from tabatu.tabua_interface import TabuaInterface
from tabatu.tabua_interface import valida_periodicidade
from tabatu.unico_decremento import Tabua


def captura_argumentos(*args: Any, **kwargs: Any) -> dict[str, int]:
    """Captura os argumentos nomeados e não nomeados e cria um dicionário contendo
    o nome do argumento e a posição em que ele se encontra na tupla de argumentos.
    Argumentos não nomeados recebem a sua posição como nome."""
    result = {}
    for i in range(len(args)):
        result[str(i)] = i
    contador = len(args)
    for key in kwargs.keys():
        result[key] = contador
        contador += 1
    return result


def qx2qxj(qx1: ndarray[float], qx2: Union[int, ndarray] = 0, qx3: Union[int, ndarray] = 0) -> ndarray[float]:
    """Converter o qx do cenário de causas independentes em qx no cenário de múltiplos decrementos."""
    return qx1 * (1 - 0.5 * (qx2 + qx3) + 1 / 3 * (qx2 * qx3))


def converter_mdt(*qx: ndarray[float]) -> ndarray[float]:
    """O array de saída terá shape equivalente a p x n onde n é o número de elemento de cada
    qx fornecido e p é a quantidade de qx fornecidos."""
    params = [
        [qx[i], *[qx[j] for j in range(len(qx)) if j != i]] for i in range(len(qx))
    ]
    return array([qx2qxj(*x) for x in params])


def valida_quantidade_tabuas(*args: Any) -> Any:
    if len(args) == 0:
        raise ValueError("Pelo menos 1 tábua deve ser fornecida.")
    if len(args) > 3:
        raise ValueError("São suportadas no máximo 3 tábuas.")
    return args


def valida_causa_principal(causa_principal: Union[int, str], causas: dict[str, int]) -> Optional[str]:
    if causa_principal is None:
        return None
    if isinstance(causa_principal, int):
        causa_principal = str(causa_principal)
    if causa_principal not in causas.keys():
        raise ValueError(f"Causa principal invalida. Deve ser um entre {list(causas.keys())}.")
    return causa_principal


class TabuaMDT(TabuaInterface):
    """Representação de tábuas de múltiplos decrementos.

    Args:
        *args (Tabua): Até 3 tábuas de únicos decrementos.
        causa_principal (int, str, Optional): Causa principal de decremento. Pode ser um inteiro ou uma string.
        **kwargs (Tabua): Até 3 tábuas de únicos decrementos.

    Notes:
        As tábuas podem ser fornecidas por posição ou por nome.
        args e kwargs devem somar no máximo três tábuas. As tábuas fornecidas por posição irão utilizar a sua
        posição como identificador nos métodos qx_j e t_qx_j. As tábuas fornecidas por nome irão utilizar ou a posição,
        ou o nome.
        O argumento causa_principal é um artífico para permitir que seja criada uma tábua de múltiplos decrementos
        onde o sinistro é definido por apenas um dos decrementos, enquanto os outros decrementos não configuram
        sinistro, mas encerram a 'vida' do indivíduo. Por exemplo, quando temos uma tábua de morte e uma tábua de
        cancelamento, usualmente, o t_qx é usado para calcular a probabilidade de sinistro, e não a probabilidade
        de sinistro ou cancelamento. Dessa forma, a causa principal faz com o t_qx seja calculado apenas
        com a causa principal. As outras causas podem ter o t_qx calculado especificamente usando o t_qx_j, e o
        t_qx de todas as causas pode ser calculado passando todas as causas para o t_qx_j e somando.

    Examples:

        >>> import numpy as np
        >>> qx1 = (np.arange(100) + 1)/100
        >>> qx2 = np.repeat(0.01, 100)
        >>> tabua_posicao = TabuaMDT(Tabua(qx1), Tabua(qx2))
        >>> tabua_posicao_e_nome = TabuaMDT(Tabua(qx1), morte = Tabua(qx2))
        >>> tabua_nome = TabuaMDT(cancelamento = Tabua(qx1), morte = Tabua(qx2))
    """
    _causa_principal: Union[int, str]
    _causas: dict[str, int]

    def __init__(self, *args: Tabua, causa_principal: Union[int, str, None] = None, **kwargs: Tabua) -> None:
        tabuas: tuple[Tabua, ...] = args + tuple(kwargs.values())
        tabuas = valida_quantidade_tabuas(*tabuas)
        self._causas = captura_argumentos(*args, **kwargs)
        self._causa_principal: Optional[str] = valida_causa_principal(causa_principal, self._causas)
        self._numero_decrementos = len(tabuas)
        self._numero_vidas = 1
        self._periodicidade = valida_periodicidade(*tabuas)
        self._tabuas = tuple(tabua.tabuas[0] for tabua in tabuas)

    @property
    def causas(self) -> dict[str, int]:
        """Causas de decremento da tábua."""
        return self._causas

    @property
    def causa_principal(self) -> Optional[str]:
        """Causa principal de decremento da tábua. Se não existir, retorna None."""
        return self._causa_principal

    def tpx(self, x: ArrayLike, t: ArrayLike) -> ndarray[float]:
        """Probabilidade de um indivíduo com idade x sobreviver a idade
        x + t.

        Args:
            x (ArrayLike): Idade de inicial. Deve ser um array com 1 elemento
                para cada decremento.
            t (ArrayLike): Tempo extra. Pode ser um array com diversos tempos.

        Returns:
            ndarray: Probabilidade de um indivíduo com idade x sobreviver a
            idade x + t.

        Examples:

            >>> import numpy as np
            >>> from tabatu import Tabua, TabuaMultiplasVidas
            >>> from tabatu.multiplas_vidas import StatusVidasConjuntas
            >>> qx = (np.arange(100) + 1)/100
            >>> Tabua(qx).tpx(30, [0,1,2,3,4,5])
            array([1.        , 0.69      , 0.4692    , 0.314364  , 0.20748024,
                   0.13486216])
        """
        t = atleast_1d(t)
        x = atleast_1d(x)
        if len(x) == 1:
            x = repeat(x, self._numero_decrementos)
        if len(x) != self._numero_decrementos:
            raise ValueError("x deve ter tamanho igual a n_decrementos.")
        return prod([tabua.tpx(idade, t) for idade, tabua in zip(x, self._tabuas)], axis=0)

    def t_qx(self, x: ArrayLike, t: ArrayLike) -> ndarray[float]:
        """Probabilidade de um indivíduo com idade x falhar com
        idade exatamente igual a x + t.

        Args:
            x (ArrayLike): Idade de inicial. Deve ser um array com 1 elemento
                ou um array com uma idade para cada decremento.
            t (ArrayLike): Tempo extra. Pode ser um array com diversos tempos.

        Returns:
            ndarray[float]: Probabilidade de um indivíduo com idade x falhar com
            idade exatamente igual a x + t.

        Examples:

            >>> import numpy as np
            >>> from tabatu import Tabua, TabuaMDT
            >>> qx1 = (np.arange(100) + 1)/100
            >>> qx2 = np.repeat(0.01, 100)
            >>> tabua = TabuaMDT(Tabua(qx1), Tabua(qx2))
            >>> tabua.t_qx([50, 0], [0, 1, 2, 3])
            array([0.5149    , 0.25458048, 0.12325879, 0.0584142 ])
        """
        if self._causa_principal is None:
            return super().t_qx(x, t)
        return self.t_qx_j(x, t, self._causa_principal).sum(axis=0)

    def qx_j(self, x: ArrayLike, t: ArrayLike, j: ArrayLike) -> ndarray[float]:
        """Probabilidade de um indivíduo com idade x + t falhar pela causa j
        antes de completar a idade x + t + 1.

        Args:
            x (ArrayLike): Idade de inicial. Deve ser um array com 1 elemento
                ou um array com uma idade para cada decremento.
            t (ArrayLike): Tempo extra. Pode ser um array com diversos tempos.
            j (ArrayLike of str or int): Causa da falha. Deve ser um número de 0 até self.n_decremento.
                Pode receber mais de um número. As causas de falha são ordenadas pela
                forma como foram utilizadas na inicialização da classe.

        Returns:
            ndarray[float]: Array com o mesmo tamanho que t, fornecendo as probabilidades
            de falha pela causa j entre x + t e x + t + 1.

        Notes:
            As probabilidades são convertidas para o cenário de múltiplos decrementos
            antes do cálculo.

        Examples:

            >>> import numpy as np
            >>> qx1 = (np.arange(100) + 1)/100
            >>> qx2 = np.repeat(0.01, 100)
            >>> tabua = TabuaMDT(Tabua(qx1), Tabua(qx2))
            >>> tabua.qx_j([50, 0], [0, 1, 2, 3], 0)
            array([[0.50745, 0.5174 , 0.52735, 0.5373 ]])
            >>> tabua.qx_j([50, 0], [0, 1, 2, 3], 1)
            array([[0.00745, 0.0074 , 0.00735, 0.0073 ]])
            >>> tabua.qx_j([50, 0], [0, 1, 2, 3], [0, 1])
            array([[0.50745, 0.5174 , 0.52735, 0.5373 ],
                   [0.00745, 0.0074 , 0.00735, 0.0073 ]])
        """
        x = atleast_1d(x)
        if len(x) == 1:
            x = repeat(x, self._numero_decrementos)
        if len(x) != self._numero_decrementos:
            raise ValueError("x deve ter tamanho igual a n_decrementos.")
        j = atleast_1d(j)
        if isinstance(j[0], str):
            j = array([self._causas[x] for x in j])
        qx_original = tuple(
            [tabua.qx(idade, t) for idade, tabua in zip(x, self._tabuas)]
        )
        return converter_mdt(*qx_original)[j]

    def qx(self, x: ArrayLike, t: ArrayLike) -> ndarray[float]:
        """Probabilidade de um indivíduo com idade x + t falhar por qualquer causa
        antes de completar a idade x + t + 1.

        Args:
            x (ArrayLike): Idade de inicial. Deve ser um array com 1 elemento
                ou um array com uma idade para cada decremento.
            t (ArrayLike): Tempo extra. Pode ser um array com diversos tempos.

        Returns:
            ndarray[float]: Array com o mesmo tamanho que t, fornecendo as probabilidades
            de falha entre x + t e x + t + 1.

        Notes:
            As probabilidades são convertidas para o cenário de múltiplos decrementos
            antes do cálculo.

        Examples:

            >>> import numpy as np
            >>> qx1 = (np.arange(100) + 1)/100
            >>> qx2 = np.repeat(0.01, 100)
            >>> tabua = TabuaMDT(Tabua(qx1), Tabua(qx2))
            >>> tabua.qx([50, 0], [0, 1, 2, 3])
            array([0.5149, 0.5248, 0.5347, 0.5446])
        """
        j = arange(self._numero_decrementos)
        return self.qx_j(x, t, j).sum(axis=0)

    def t_qx_j(self, x: ArrayLike, t: ArrayLike, j: ArrayLike) -> ndarray[float]:
        """Probabilidade de um indivíduo com idade x falhar com
        idade exatamente igual a x + t, pela causa j.

        Args:
            x (ArrayLike): Idade de inicial. Deve ser um array com 1 elemento
                ou um array com uma idade para cada decremento.
            t (ArrayLike): Tempo extra. Pode ser um array com diversos tempos.
            j (ArrayLike): Causa da falha. Deve ser um número de 0 até self.n_decremento.
                Pode receber mais de um número. As causas de falha são ordenadas pela
                forma como foram utilizadas na inicialização da classe.

        Returns:
            ndarray[float]: Probabilidade de um indivíduo com idade x falhar com
            idade exatamente igual a x + t, pela causa j.

        Examples:

            >>> import numpy as np
            >>> qx1 = (np.arange(100) + 1)/100
            >>> qx2 = np.repeat(0.01, 100)
            >>> tabua = TabuaMDT(Tabua(qx1), Tabua(qx2))
            >>> tabua.t_qx_j([50, 0], [0, 1, 2, 3], 0)
            array([[0.50745   , 0.25099074, 0.12156447, 0.05763119]])
            >>> tabua.t_qx_j([50, 0], [0, 1, 2, 3], 1)
            array([[0.00745   , 0.00358974, 0.00169432, 0.000783  ]])
            >>> tabua.t_qx_j([50, 0], [0, 1, 2, 3], [0, 1])
            array([[0.50745   , 0.25099074, 0.12156447, 0.05763119],
                   [0.00745   , 0.00358974, 0.00169432, 0.000783  ]])
        """
        j = atleast_1d(j)
        return atleast_2d(self.tpx(x, t) * self.qx_j(x, t, j))

    def tempo_futuro_max(self, x: ArrayLike) -> int:
        """Tempo de vida futuro máximo.

        A idade pode ser composta de duas idades diferentes, como, por exemplo,
        no caso em que existe uma tábua de morte e uma tábua de cancelamento.

        Args:
            x (ndarray): Idade de inicial. Deve ser um array com 1 elemento
                ou um array com uma idade para cada decremento.

        Returns:
            int: Tempo de vida futuro máximo.

        Examples:

            >>> import numpy as np
            >>> qx1 = (np.arange(100) + 1)/100
            >>> qx2 = np.repeat(0.01, 100)
            >>> tabua = TabuaMDT(Tabua(qx1), Tabua(qx2))
            >>> tabua.tempo_futuro_max(30)
            70
            >>> tabua.tempo_futuro_max([50, 0])
            50
        """
        x = atleast_1d(x)
        if len(x) == 1:
            x = repeat(x, self._numero_decrementos)
        if len(x) != self._numero_decrementos:
            raise ValueError("x deve ter tamanho igual a n_decrementos.")
        return min([tabua.tempo_futuro_max(idade) for idade, tabua in zip(x, self._tabuas)])

    def possui_causa_principal(self) -> bool:
        """Verifica se existe uma causa principal."""
        return self._causa_principal is not None
