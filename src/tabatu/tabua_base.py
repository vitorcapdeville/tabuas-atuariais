from typing import Union

from numpy import atleast_1d
from numpy import ndarray
from numpy.typing import ArrayLike

from tabatu_cpp import PyTabua
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


class TabuaBase:
    def __init__(self, qx: ArrayLike, periodicidade: Periodicidade = Periodicidade["ANUAL"]):
        qx: ndarray[float] = validar_qx(qx)
        self._tabua = PyTabua(qx)
        self._periodicidade: Periodicidade = Periodicidade(periodicidade)

    @property
    def periodicidade(self) -> Periodicidade:
        return self._periodicidade


    def tpx(self, x: int, t: ArrayLike) -> ndarray[float]:
        if x < 0:
            raise ValueError("x deve ser >= 0.")
        t = atleast_1d(t)
        if (t < 0).any():
            raise ValueError("t deve ser >= 0.")
        return self._tabua.tpx(x, t)

    def t_qx(self, x: int, t: ArrayLike) -> ndarray[float]:
        return self.tpx(x, t) * self.qx(x, t)

    def qx(self, x: int, t: ArrayLike) -> ndarray[float]:
        if x < 0:
            raise ValueError("x deve ser >= 0.")
        t = atleast_1d(t)
        if (t < 0).any():
            raise ValueError("t deve ser >= 0.")
        return self._tabua.qx(x, t)

    def tempo_futuro_max(self, x: int) -> Union[int, float]:
        return self._tabua.tempo_futuro_maximo(x)

    def possui_fechamento_plato(self) -> bool:
        return self._tabua.possui_fechamento_plato()
