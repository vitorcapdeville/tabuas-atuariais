from __future__ import annotations
from typing import Iterable

from numpy import float64
from numpy.typing import NDArray

import tabatu.core as core
from tabatu.periodicidade import Periodicidade
from tabatu.alterar_juros import alterar_periodicidade_juros


class JurosConstante(core.JurosConstante):
    """Definição de juros constante no tempo.

    Args:
        taxa_juros (float): Taxa de juros.
        periodicidade (Periodicidade, optional): Periodicidade da taxa de juros.

    Examples:

        >>> juros = JurosConstante(0.01)
    """

    def __init__(
        self, taxa_juros: float, periodicidade: Periodicidade = Periodicidade.ANUAL
    ):
        self._periodicidade = periodicidade
        super().__init__(taxa_juros)

    @property
    def periodicidade(self) -> Periodicidade:
        """Periodicidade do juros."""
        return self._periodicidade

    def alterar_periodicidade(
        self, nova_periodicidade: Periodicidade
    ) -> JurosConstante:
        """Alteração da periodicidade dos juros.

        Args:
            nova_periodicidade (Periodicidade): Nova periodicidade dos juros.

        Returns:
            JurosInterface: Juros com a nova periodicidade.
        """
        taxa_juros_convertida = alterar_periodicidade_juros(
            self.taxa_juros([0]).item(), self._periodicidade, nova_periodicidade
        )
        return JurosConstante(taxa_juros_convertida, nova_periodicidade)

    def taxa_juros(self, t: Iterable[int]) -> NDArray[float64]:
        """Taxa de juros no tempo ``t``.

        Args:
            t (Iterable[int]): Tempo (ou tempos) para os quais se deseja obter a taxa de juros.

        Returns:
            NDArray[float64]: Taxa de juros nos tempos desejados.

        Examples:
            Juros anual de 1%, calculado para os 5 primeiros anos.

            >>> juros = JurosConstante(0.01)
            >>> juros.taxa_juros([0, 1, 2, 3, 4])
            array([0.01, 0.01, 0.01, 0.01, 0.01])

            Juros anual de 1%, calculado para os 5 primeiros meses

            >>> taxa_juros=alterar_periodicidade_juros(0.01, Periodicidade.ANUAL, Periodicidade.MENSAL)
            >>> juros = JurosConstante(taxa_juros, periodicidade=Periodicidade["MENSAL"])
            >>> juros.taxa_juros([0, 1, 2, 3, 4])
            array([0.00082954, 0.00082954, 0.00082954, 0.00082954, 0.00082954])
        """
        return super().taxa_juros(t)

    def taxa_desconto(self, t: Iterable[int]) -> NDArray[float64]:
        """Taxa de desconto no tempo ``t``.

        Args:
            t (Iterable[int]): Tempos para os quais se deseja obter a taxa de desconto.
                Deve estar na mesma periodicidade que o juros.

        Returns:
            NDArray[float64]: Taxa de desconto nos tempos desejados.

        Examples:

            Juros anual de 1%, calculado para os 5 primeiros anos.

            >>> juros = JurosConstante(0.01)
            >>> juros.taxa_desconto([0, 1, 2, 3, 4])
            array([1.        , 0.99009901, 0.98029605, 0.97059015, 0.96098034])

            Juros anual de 1%, calculado para os 5 primeiros meses
            >>> taxa_juros=alterar_periodicidade_juros(0.01, Periodicidade.ANUAL, Periodicidade.MENSAL)
            >>> juros = JurosConstante(taxa_juros, periodicidade=Periodicidade["MENSAL"])
            >>> juros.taxa_desconto([0, 1, 2, 3, 4])
            array([1.        , 0.99917115, 0.99834299, 0.99751551, 0.99668872])
        """
        return super().taxa_desconto(t)
