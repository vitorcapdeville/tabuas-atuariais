from __future__ import annotations

from enum import Enum

import tabatu.core as core
from tabatu.tabua_interface import valida_periodicidade
from tabatu.unico_decremento import Tabua


class StatusVidasConjuntas(Enum):
    JOINT = b"JOINT"
    LAST = b"LAST"


class TabuaMultiplasVidas(core.TabuaMultiplasVidas):
    _status: StatusVidasConjuntas

    def __init__(
        self, *args: Tabua, status: StatusVidasConjuntas = StatusVidasConjuntas.LAST
    ) -> None:
        self._periodicidade = valida_periodicidade(*args)
        self._status = status
        super().__init__(*args, status=core.StatusVidasConjuntas(status.value))

    @property
    def status(self) -> StatusVidasConjuntas:
        """Status de vida conjunta."""
        return self._status
