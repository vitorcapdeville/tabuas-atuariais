from __future__ import annotations

from tabatu.periodicidade import Periodicidade


def alterar_periodicidade_juros(
    juros: float, periodicidade: Periodicidade, nova_periodicidade: Periodicidade
) -> float:
    """Fracionamento da taxa de juros.

    Args:
        juros (float): Taxa de juros.
        periodicidade (Periodicidade): Periodicdade atual do juros.
        nova_periodicidade (Periodicidade): Periodicidade que o juros terá após a alteração.

    Returns:
        float: Taxa de juros fracionada.
    """
    return (1 + juros) ** periodicidade.quantidade_periodos_1_periodicidade(
        nova_periodicidade
    ) - 1
