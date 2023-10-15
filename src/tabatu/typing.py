from typing import Iterable, Protocol

from numpy import float64
from numpy.typing import NDArray

from tabatu.periodicidade import Periodicidade


class TabuaInterface(Protocol):
    @property
    def periodicidade(self) -> Periodicidade:
        ...

    def qx(self, x: Iterable[int], t: Iterable[int]) -> NDArray[float64]:
        ...

    def tpx(self, x: Iterable[int], t: Iterable[int]) -> NDArray[float64]:
        ...

    def t_qx(self, x: Iterable[int], t: Iterable[int]) -> NDArray[float64]:
        ...

    def tempo_futuro_maximo(self, x: Iterable[int]) -> float:
        ...

    def possui_fechamento_plato(self) -> bool:
        ...

    def alterar_periodicidade(
        self, nova_periodicidade: Periodicidade
    ) -> "TabuaInterface":
        ...


class JurosInterface(Protocol):
    @property
    def periodicidade(self) -> Periodicidade:
        ...

    def alterar_periodicidade(
        self, nova_periodicidade: Periodicidade
    ) -> "JurosInterface":
        ...

    def taxa_juros(self, t: Iterable[int]) -> NDArray[float64]:
        ...

    def taxa_desconto(self, t: Iterable[int]) -> NDArray[float64]:
        ...
