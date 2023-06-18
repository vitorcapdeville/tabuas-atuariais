from abc import ABC
from abc import abstractmethod
from typing import Union

from numpy import array
from numpy import isinf
from numpy import ndarray
from numpy import repeat
from numpy.typing import ArrayLike

from matatu.periodicidade import Periodicidade
from tabatu.tabua_base import TabuaBase


def valida_periodicidade(*args: TabuaBase) -> Periodicidade:
    periodicidade = array([tabua.periodicidade for tabua in args])
    if not (periodicidade == periodicidade[0]).all():
        raise ValueError("Todas as tabuas precisam possuir a mesma periodicidade.")
    return periodicidade[0]


class TabuaInterface(ABC):
    _tabuas: tuple[TabuaBase, ...]
    _numero_vidas: int
    _numero_decrementos: int
    _periodicidade: Periodicidade

    @abstractmethod
    def tpx(self, x: ArrayLike, t: ArrayLike) -> ndarray[float]:
        pass

    def t_qx(self, x: ArrayLike, t: ArrayLike) -> ndarray[float]:
        return self.tpx(x, t) * self.qx(x, t)

    @abstractmethod
    def qx(self, x: ArrayLike, t: ArrayLike) -> ndarray[float]:
        pass

    @abstractmethod
    def tempo_futuro_max(self, x: ArrayLike) -> Union[int, float]:
        pass

    def possui_fechamento_plato(self) -> bool:
        """Verifica se a tábua possui fechamento de tipo platô."""
        x = repeat(0, self._numero_vidas * self._numero_decrementos)
        return isinf(self.tempo_futuro_max(x))

    @property
    def numero_vidas(self) -> int:
        """Número de vidas da tábua."""
        return self._numero_vidas

    @property
    def numero_decrementos(self) -> int:
        """Número de decrementos da tábua"""
        return self._numero_decrementos

    @property
    def tabuas(self) -> tuple[TabuaBase, ...]:
        """Tupla com as tábuas (base) que compõem a tábua."""
        return self._tabuas

    @property
    def periodicidade(self) -> Periodicidade:
        """Periodicidade da tábua."""
        return self._periodicidade