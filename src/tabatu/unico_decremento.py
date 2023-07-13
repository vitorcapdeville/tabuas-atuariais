from __future__ import annotations


from tabatu.periodicidade import Periodicidade
from numpy import ndarray

import tabatu_cpp


class Tabua(tabatu_cpp.Tabua):
    __slots__ = "_tabuas", "_numero_vidas", "_numero_decrementos", "_periodicidade"

    def __init__(
        self, qx: ndarray[float], periodicidade: Periodicidade = Periodicidade.ANUAL
    ):
        super().__init__(qx)
        self._periodicidade = periodicidade

    @property
    def periodicidade(self) -> Periodicidade:
        """Periodicidade da tábua."""
        return self._periodicidade
