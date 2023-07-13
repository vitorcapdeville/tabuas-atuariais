from __future__ import annotations

from enum import Enum

import tabatu_cpp
from tabatu.tabua_interface import valida_periodicidade
from tabatu.unico_decremento import Tabua


class StatusVidasConjuntas(Enum):
    JOINT = 0
    LAST = 1


class TabuaMultiplasVidas(tabatu_cpp.TabuaMultiplasVidas):
    _status: StatusVidasConjuntas

    def __init__(
        self, *args: Tabua, status: StatusVidasConjuntas = StatusVidasConjuntas.LAST
    ) -> None:
        self._periodicidade = valida_periodicidade(*args)
        self._status = status
        super().__init__(*args, status=tabatu_cpp.StatusVidasConjuntas(status.value))

    @property
    def status(self) -> StatusVidasConjuntas:
        """Status de vida conjunta."""
        return self._status
