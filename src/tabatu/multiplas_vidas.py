from __future__ import annotations

from enum import Enum

from numpy import ndarray
from numpy.typing import ArrayLike

from tabatu.tabua_interface import valida_periodicidade
from tabatu.unico_decremento import Tabua
import tabatu_cpp


class StatusVidasConjuntas(Enum):
    """
    Status de vidas conjuntas. "last" significa que a falha total é
    equivalente à falha de todas as vidas, ou seja, pelo menos
    uma vida precisa estar viva. "joint" signficia que a falha total
    é dada pela falha de pelo menos uma das vidas, ou seja, todas as vidas
    precisam estar vivas.
    """

    JOINT = 0
    LAST = 1


class TabuaMultiplasVidas(tabatu_cpp.TabuaMultiplasVidas):
    """Representação de tábuas de múltiplas vidas.

    Args:
        *args (Tabua): Uma quantidade arbitrária de tábuas, representando
            as falhas de cada vida.
        status (StatusVidasConjuntas): status de vida conjunta.

    Examples:

        >>> import numpy as np
        >>> qx1 = (np.arange(100) + 1)/100
        >>> tabua = TabuaMultiplasVidas(Tabua(qx1), Tabua(qx1), status = StatusVidasConjuntas.LAST)
    """

    _status: StatusVidasConjuntas

    def __init__(
        self, *args: Tabua, status: StatusVidasConjuntas = StatusVidasConjuntas.LAST
    ) -> None:
        self._periodicidade = valida_periodicidade(*args)
        self._status = status
        super().__init__(*args, status=tabatu_cpp.StatusVidasConjuntas(status.value))

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
        """
        return super().t_qx(x, t)

    def tpx(self, x: ArrayLike, t: ArrayLike) -> ndarray[float]:
        """Probabilidade de um indivíduo com idade x sobreviver a idade
        x + t.

        Args:
            x (ArrayLike): Idade de inicial. Deve ser um array com 1 elemento
                para cada vida.
            t (ArrayLike): Tempo extra. Pode ser um array com diversos tempos.

        Returns:
            ndarray[float]: Probabilidade de um indivíduo com idade x sobreviver a
            idade x + t.

        Examples:

            >>> import numpy as np
            >>> from tabatu import Tabua, TabuaMultiplasVidas
            >>> from tabatu.multiplas_vidas import StatusVidasConjuntas
            >>> qx = (np.arange(100) + 1)/100
            >>> Tabua(qx).tpx(30, [0,1,2,3,4,5])
            array([1.        , 0.69      , 0.4692    , 0.314364  , 0.20748024,
                   0.13486216])

            >>> tabua = TabuaMultiplasVidas(Tabua(qx), Tabua(qx), status = StatusVidasConjuntas.LAST)
            >>> tpx = tabua.tpx([30, 50], [0,1,2,3,4,5])
            >>> np.round(tpx, 5)
            array([1.     , 0.8419 , 0.70181, 0.57906, 0.47275, 0.38174])
        """

        return super().tpx(x, t)

    def qx(self, x: ArrayLike, t: ArrayLike) -> ndarray[float]:
        """Probabilidade de falha entre as idades x + t e x + t + 1.

        A falha é definida pelo status da tabua. Se o status é "last", então
        a falha é definida por todas as vidas falharem.
        Se o status é "joint", então a falha é definida por pelo menos uma vida
        falhar.

        Args:
            x (ArrayLike): Idade de inicial. Deve ser um array com 1 elemento
                para cada vida.
            t (ArrayLike): Tempo extra. Pode ser um array com diversos tempos.

        Returns:
            ndarray[float]: Array com o mesmo tamanho que t, fornecendo as probabilidades
            de falha entre x + t e x + t + 1.

        Examples:

            Como seria esperado, as probabildiades de falha no status "last"
            são mais baixas que as probabilidades de falha no status "joint".

            >>> import numpy as np
            >>> qx1 = (np.arange(100) + 1)/100
            >>> tabua = TabuaMultiplasVidas(Tabua(qx1), Tabua(qx1), status=StatusVidasConjuntas.LAST)
            >>> tabua.qx([50, 30], [0, 1, 2, 3])
            array([0.1581, 0.1664, 0.1749, 0.1836])
            >>> tabua = TabuaMultiplasVidas(Tabua(qx1), Tabua(qx1), status=StatusVidasConjuntas.JOINT)
            >>> tabua.qx([50, 30], [0, 1, 2, 3])
            array([0.6619, 0.6736, 0.6851, 0.6964])
        """
        return super().qx(x, t)

    def tempo_futuro_maximo(self, x: ArrayLike) -> int:
        """Tempo de vida futuro máximo.

        A idade deve ser composta por um array com tamanho igual ao número de vidas.

        Args:
            x (ArrayLike): Idade de inicial. Deve ser um array com
                uma idade para cada vida.

        Returns:
            int: Tempo de vida futuro máximo.

        Examples:

            >>> import numpy as np
            >>> qx1 = (np.arange(100) + 1)/100

            Com o status "last" o tempo futuro é maior dos tempos, afinal a tabua
            continua se pelo menos uma vida está viva.

            >>> tabua = TabuaMultiplasVidas(Tabua(qx1), Tabua(qx1), status = StatusVidasConjuntas.LAST)
            >>> tabua.tempo_futuro_maximo([50, 30])
            70

            Já para o status "joint", quando a primeira vida morre, a tabua se encerra.

            >>> tabua = TabuaMultiplasVidas(Tabua(qx1), Tabua(qx1), status = StatusVidasConjuntas.JOINT)
            >>> tabua.tempo_futuro_maximo([50, 30])
            50
        """
        return super().tempo_futuro_maximo(x)

    @property
    def status(self) -> StatusVidasConjuntas:
        """Status de vida conjunta."""
        return self._status
