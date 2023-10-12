from numpy import atleast_1d
from numpy import ndarray
from numpy.typing import ArrayLike

import tabatu.core as core
from tabatu.periodicidade import Periodicidade
from tabatu.alterar_tabua import alterar_periodicidade_qx


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


class TabuaBase(core.TabuaBase):
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

    def alterar_periodicidade(self, nova_periodicidade: Periodicidade):
        qx = alterar_periodicidade_qx(self.pega_qx(), self._periodicidade, nova_periodicidade)
        return TabuaBase(qx, nova_periodicidade)
