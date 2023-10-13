from typing import Iterable
from numpy import array

import tabatu.core as core
from tabatu.periodicidade import Periodicidade
from tabatu.alterar_tabua import alterar_periodicidade_qx


class TabuaBase(core.TabuaBase):
    __slots__ = "_tabua", "_periodicidade"

    def __init__(
        self, qx: Iterable[float], periodicidade: Periodicidade = Periodicidade.ANUAL
    ):
        self._periodicidade: Periodicidade = Periodicidade(periodicidade)
        super().__init__(qx)

    @property
    def periodicidade(self) -> Periodicidade:
        return self._periodicidade

    def alterar_periodicidade(self, nova_periodicidade: Periodicidade) -> "TabuaBase":
        qx = alterar_periodicidade_qx(
            self.pega_qx(), self._periodicidade, nova_periodicidade
        )
        return TabuaBase(qx, nova_periodicidade)


def valida_periodicidade(*args: TabuaBase) -> Periodicidade:
    periodicidade = array([tabua.periodicidade for tabua in args])
    if not (periodicidade == periodicidade[0]).all():
        raise ValueError("Todas as tabuas precisam possuir a mesma periodicidade.")
    return periodicidade[0]
