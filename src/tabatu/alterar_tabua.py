from typing import Iterable
from numpy import fromiter, minimum
from numpy import multiply
from numpy import ones_like
from numpy import float64
from numpy.typing import NDArray

from tabatu.periodicidade import Periodicidade
import tabatu.core as core


def alterar_periodicidade_qx(
    qx: Iterable[float],
    periodicidade: Periodicidade,
    nova_periodicidade: Periodicidade,
) -> NDArray[float64]:
    """Altera a periodicidade de um array de taxas. Retorna um novo array de taxas.

    IMPORTANTE: As taxas devem ser agravadas antes de terem a sua periodicidade alterada.
    """
    if periodicidade < nova_periodicidade and not periodicidade.quantidade_periodos_1_periodicidade(nova_periodicidade).is_integer():
        raise ValueError(
            f"A quantidade de periodos da periodicidade em 1 período da nova periodicidade original deve ser inteiro."
            f" Por exemplo, em um trimestre existem 1.5 bimestres, logo, não é possível converter."
        )
    if periodicidade > nova_periodicidade and not nova_periodicidade.quantidade_periodos_1_periodicidade(periodicidade).is_integer():
        raise ValueError(
            f"A quantidade de periodos da nova periodicidade em 1 período da periodicidade original deve ser inteiro."
            f" Por exemplo, em um trimestre existem 1.5 bimestres, logo, não é possível converter."
        )
    
    return core.alterar_periodicidade_qx(
        qx,
        periodicidade.quantidade_periodos_1_ano(),
        nova_periodicidade.quantidade_periodos_1_ano(),
    )


def agravar_qx(qx: Iterable[float], percentual: float) -> NDArray[float64]:
    qx = fromiter(qx, float64)
    if percentual < 0:
        raise ValueError("O percentual deve ser positivo.")
    qx = minimum(multiply(qx, percentual / 100, out=ones_like(qx), where=qx < 1), 1)
    return qx
