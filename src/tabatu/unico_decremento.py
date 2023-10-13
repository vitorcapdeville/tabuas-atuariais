from __future__ import annotations

from typing import Iterable

from numpy import float64
from numpy.typing import NDArray

import tabatu.core as core
from tabatu.periodicidade import Periodicidade
from tabatu.tabua_base import TabuaBase


class Tabua(core.Tabua):
    __slots__ = "_periodicidade"

    def __init__(
        self, qx: Iterable[float], periodicidade: Periodicidade = Periodicidade.ANUAL
    ):
        super().__init__(qx)
        self._periodicidade = periodicidade

    @classmethod
    def from_tabua_base(cls, tabua: TabuaBase) -> Tabua:
        """Cria uma Tabua a partir de uma TabuaBase.

        Args:
            tabua (TabuaBase): TabuaBase a ser usada como base.

        Returns:
            Tabua: Tabua criada.
        """
        return cls(tabua.pega_qx(), tabua.periodicidade)

    @property
    def periodicidade(self) -> Periodicidade:
        """Periodicidade da tábua."""
        return self._periodicidade

    def qx(self, x: Iterable[int], t: Iterable[int]) -> NDArray[float64]:
        """Probabilidade de um indivíduo com idade x + t falhar
        antes de completar a idade x + t + 1.

        Args:
            x (Iterable[int]): Idade de inicial, deve ser um inteiro ou um array com um único inteiro.
            t (Iterable[int]): Tempo extra. Pode ser um array com diversos tempos.

        Returns:
            NDArray[float64]: Array com o mesmo tamanho que t, fornecendo as probabilidades
            de falha entre x + t e x + t + 1.

        Examples:

            >>> import numpy as np
            >>> qx = (np.arange(100) + 1)/100
            >>> Tabua(qx).qx([30], [0,1,2,3,4,5])
            array([0.31, 0.32, 0.33, 0.34, 0.35, 0.36])
        """
        return super().qx(x, t)

    def tpx(self, x: Iterable[int], t: Iterable[int]) -> NDArray[float64]:
        """Probabilidade de um indivíduo com idade x sobreviver a idade
        x + t.

        Args:
            x (Iterable[int]): Idade de inicial, deve ser um inteiro ou um array com um único inteiro.
            t (Iterable[int]): Tempo extra. Pode ser um array com diversos tempos.

        Returns:
            NDArray[float64]: Probabilidade de um indivíduo com idade x sobreviver a
            idade x + t.

        Examples:

            >>> import numpy as np
            >>> qx = (np.arange(100) + 1)/100
            >>> Tabua(qx).tpx([30], [0,1,2,3,4,5])
            array([1.        , 0.69      , 0.4692    , 0.314364  , 0.20748024,
                   0.13486216])
        """
        return super().tpx(x, t)

    def t_qx(self, x: Iterable[int], t: Iterable[int]) -> NDArray[float64]:
        """Probabilidade de um indivíduo com idade x falhar com
        idade exatamente igual a x + t.

        Args:
            x (Iterable[int]): Idade de inicial, deve ser um inteiro ou um array com um único inteiro.
            t (Iterable[int]): Tempo extra. Pode ser um array com diversos tempos.

        Returns:
            NDArray[float64]: Probabilidade de um indivíduo com idade x falhar com
            idade exatamente igual a x + t.

        Examples:

            >>> import numpy as np
            >>> qx = (np.arange(100) + 1)/100
            >>> Tabua(qx).t_qx([30], [0, 1, 2, 3, 4, 5])
            array([0.31      , 0.2208    , 0.154836  , 0.10688376, 0.07261808,
                   0.04855038])
        """
        return super().t_qx(x, t)

    def tempo_futuro_maximo(self, x: Iterable[int]) -> float:
        """Tempo de vida futuro máximo.

        Args:
            x (Iterable[int]): Idade de inicial, deve ser um inteiro ou um array com um único inteiro.

        Returns:
            float: Tempo de vida futuro máximo, pode ser infinito.

        Examples:

            >>> import numpy as np
            >>> qx = (np.arange(100) + 1)/100
            >>> Tabua(qx).tempo_futuro_maximo([30])
            70.0
            >>> Tabua(qx).tempo_futuro_maximo([0])
            100.0
        """
        return super().tempo_futuro_maximo(x)

    def possui_fechamento_plato(self) -> bool:
        """Verifica se a tábua possui fechamento de tipo platô."""
        return super().possui_fechamento_plato()

    @property
    def tabuas(self) -> list[TabuaBase]:
        return [
            TabuaBase(tabua.pega_qx(), self._periodicidade) for tabua in super().tabuas
        ]

    def alterar_periodicidade(self, nova_periodicidade: Periodicidade) -> Tabua:
        """Altera a periodicidade da tábua.

        Args:
            nova_periodicidade (Periodicidade): Nova periodicidade.
        """
        nova_tabua_base = self.tabuas[0].alterar_periodicidade(nova_periodicidade)
        return Tabua.from_tabua_base(nova_tabua_base)
