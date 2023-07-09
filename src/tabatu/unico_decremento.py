from __future__ import annotations

from typing import Union

from numpy import atleast_1d
from numpy import ndarray
from numpy.typing import ArrayLike
import tabatu_cpp

from matatu.periodicidade import Periodicidade


class Tabua(tabatu_cpp.Tabua):
    """Representação de tábuas de únicos decrementos.

    Fornece métodos para cálculo das probabilidades de falha e sobrevivência,
    além de serem blocos para a construção de tábuas de múltiplos decrementos
    e tábuas de múltiplas vidas.

    Args:
        qx (ndarray[float]): Array contendo as probabilidades de falha entre x e x + 1,
            no cenário que essas taxas representam o único decremento existente.
            Deve estar na periodicidade original da tábua. Para tábuas fracionadas,
            crie a tábua e use o setter de periodicidade.
        periodicidade (Periodicidade, optional): Periodicidade das probabilidades
            de falha fornecidas. Por default, é considerado que as taxas são anuais.

    Note:
        A periodicidade controla como os métodos devem ser usados.

        Se periodocidade for mensal, então tpx(600, 100) é a probabilidade de
        um indivíduo com 600 meses não falhar nos próximos 100 meses.

    Examples:

        >>> import numpy as np
        >>> qx1 = (np.arange(100) + 1)/100
        >>> tabua = Tabua(qx1, periodicidade=Periodicidade["ANUAL"])
    """

    __slots__ = "_tabuas", "_numero_vidas", "_numero_decrementos", "_periodicidade"

    def __init__(
        self, qx: ndarray[float], periodicidade: Periodicidade = Periodicidade.ANUAL
    ):
        super().__init__(qx)
        self._periodicidade = periodicidade

    def tpx(self, x: ArrayLike, t: ArrayLike) -> ndarray[float]:
        """Probabilidade de um indivíduo com idade x sobreviver a idade
        x + t.

        Args:
            x (ArrayLike): Idade de inicial, deve ser um inteiro ou um array com um único inteiro.
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
        """
        x = atleast_1d(x).item()
        return super().tpx(x, t)

    def t_qx(self, x: ArrayLike, t: ArrayLike) -> ndarray[float]:
        """Probabilidade de um indivíduo com idade x falhar com
        idade exatamente igual a x + t.

        Args:
            x (ArrayLike): Idade de inicial, deve ser um inteiro ou um array com um único inteiro.
            t (ArrayLike): Tempo extra. Pode ser um array com diversos tempos.

        Returns:
            ndarray[float]: Probabilidade de um indivíduo com idade x falhar com
            idade exatamente igual a x + t.

        Examples:

            >>> import numpy as np
            >>> from tabatu import Tabua, TabuaMDT
            >>> qx1 = (np.arange(100) + 1)/100
            >>> Tabua(qx1).t_qx(30, [0, 1, 2, 3, 4, 5])
            array([0.31      , 0.2208    , 0.154836  , 0.10688376, 0.07261808,
                   0.04855038])
        """
        x = atleast_1d(x).item()
        return super().t_qx(x, t)

    def qx(self, x: ArrayLike, t: ArrayLike) -> ndarray[float]:
        """Probabilidade de um indivíduo com idade x + t falhar
        antes de completar a idade x + t + 1.

        Args:
            x (ArrayLike): Idade de inicial, deve ser um inteiro ou um array com um único inteiro.
            t (ArrayLike): Tempo extra. Pode ser um array com diversos tempos.

        Returns:
            ndarray[float]: Array com o mesmo tamanho que t, fornecendo as probabilidades
            de falha entre x + t e x + t + 1.

        Examples:

            >>> import numpy as np
            >>> qx = (np.arange(100) + 1)/100
            >>> Tabua(qx).qx(30, [0,1,2,3,4,5])
            array([0.31, 0.32, 0.33, 0.34, 0.35, 0.36])
        """
        x = atleast_1d(x).item()
        return super().qx(x, t)

    def tempo_futuro_max(self, x: ArrayLike) -> Union[int, float]:
        """Tempo de vida futuro máximo.

        Args:
            x (ArrayLike): Idade de inicial, deve ser um inteiro ou um array com um único inteiro.

        Returns:
            int: Tempo de vida futuro máximo.

        Examples:

            >>> import numpy as np
            >>> qx = (np.arange(100) + 1)/100
            >>> Tabua(qx).tempo_futuro_max(30)
            70
            >>> Tabua(qx).tempo_futuro_max(0)
            100
        """
        x = atleast_1d(x).item()
        return super().tempo_futuro_max(x)

    @property
    def periodicidade(self) -> Periodicidade:
        """Periodicidade da tábua."""
        return self._periodicidade
