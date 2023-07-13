from __future__ import annotations

from typing import Any
from typing import Optional
from typing import Union

from numpy import array
from numpy import atleast_1d
from numpy import atleast_2d
from numpy import ndarray
from numpy.typing import ArrayLike

from tabatu.unico_decremento import Tabua
from tabatu.tabua_interface import valida_periodicidade
import tabatu_cpp


def captura_argumentos(*args: Any, **kwargs: Any) -> dict[str, int]:
    result = {}
    for i in range(len(args)):
        result[str(i)] = i
    contador = len(args)
    for key in kwargs.keys():
        result[key] = contador
        contador += 1
    return result


def valida_quantidade_tabuas(*args: Any) -> Any:
    if len(args) == 0:
        raise ValueError("Pelo menos 1 tábua deve ser fornecida.")
    if len(args) > 3:
        raise ValueError("São suportadas no máximo 3 tábuas.")
    return args


def valida_causa_principal(
    causa_principal: Union[int, str], causas: dict[str, int]
) -> Optional[str]:
    if causa_principal is None:
        return None
    if isinstance(causa_principal, int):
        causa_principal = str(causa_principal)
    if causa_principal not in causas.keys():
        raise ValueError(
            f"Causa principal invalida. Deve ser um entre {list(causas.keys())}."
        )
    return causa_principal


class TabuaMDT(tabatu_cpp.TabuaMDT):
    _causa_principal: Union[int, str]
    _causas: dict[str, int]

    def __init__(
        self,
        *args: Tabua,
        causa_principal: Union[int, str, None] = None,
        **kwargs: Tabua,
    ) -> None:
        tabuas: tuple[Tabua, ...] = args + tuple(kwargs.values())
        tabuas = valida_quantidade_tabuas(*tabuas)
        self._causas = captura_argumentos(*args, **kwargs)
        self._causa_principal: Optional[str] = valida_causa_principal(
            causa_principal, self._causas
        )
        self._periodicidade = valida_periodicidade(*tabuas)
        super().__init__(*tabuas)

    @property
    def causas(self) -> dict[str, int]:
        return self._causas

    @property
    def causa_principal(self) -> Optional[str]:
        return self._causa_principal

    def t_qx(self, x: ArrayLike, t: ArrayLike) -> ndarray[float]:
        if self._causa_principal is None:
            return super().t_qx(x, t)
        return self.t_qx_j(x, t, self._causa_principal).sum(axis=0)

    def qx_j(self, x: ArrayLike, t: ArrayLike, j: ArrayLike) -> ndarray[float]:
        j = atleast_1d(j)
        if isinstance(j[0], str):
            j = array([self._causas[x] for x in j])
        return super().qx_j(x, t, j)

    def t_qx_j(self, x: ArrayLike, t: ArrayLike, j: ArrayLike) -> ndarray[float]:
        j = atleast_1d(j)
        return atleast_2d(self.tpx(x, t) * self.qx_j(x, t, j))

    def possui_causa_principal(self) -> bool:
        """Verifica se existe uma causa principal."""
        return self._causa_principal is not None
