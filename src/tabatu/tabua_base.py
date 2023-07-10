import stat
from typing import Union

from numpy import atleast_1d
from numpy import ndarray
from numpy.typing import ArrayLike

import tabatu_cpp
from matatu.periodicidade import Periodicidade


def validar_qx(qx: ArrayLike) -> ndarray:
    """Valida que qx é um array 1D com valores entre 0 e 1."""
    qx = atleast_1d(qx)
    errors = []
    if not qx.ndim == 1:
        errors.append("qx deve possuir apenas 1 dimensão.")
    if not (qx >= 0).all():
        errors.append("Todos os elementos de qx devem ser >= 0.")
    if not (qx <= 1).all():
        errors.append("Todos os elementos de qx devem ser <= 1.")
    if len(errors) > 0:
        raise ValueError("\n" + "\n".join(errors))
    return qx


class TabuaBase(tabatu_cpp.TabuaBase):
    __slots__ = "_tabua", "_periodicidade"

    def __init__(
        self, qx: ArrayLike, periodicidade: Periodicidade = Periodicidade["ANUAL"]
    ):
        qx: ndarray[float] = validar_qx(qx)
        self._periodicidade: Periodicidade = Periodicidade(periodicidade)
        super().__init__(qx)

    @property
    def periodicidade(self) -> Periodicidade:
        return self._periodicidade

    def tpx(self, x: int, t: ArrayLike) -> ndarray[float]:
        t = atleast_1d(t)
        return super().tpx(x, t)

    def t_qx(self, x: int, t: ArrayLike) -> ndarray[float]:
        t = atleast_1d(t)
        return super().t_qx(x, t)

    def qx(self, x: int, t: ArrayLike) -> ndarray[float]:
        t = atleast_1d(t)
        return super().qx(x, t)

    def tempo_futuro_maximo(self, x: int) -> Union[int, float]:
        return super().tempo_futuro_maximo(x)

    def possui_fechamento_plato(self) -> bool:
        return super().possui_fechamento_plato()
