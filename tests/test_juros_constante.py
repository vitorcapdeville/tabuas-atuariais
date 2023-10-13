import numpy as np
from numpy.testing import assert_array_equal

from tabatu import JurosConstante
from tabatu import alterar_periodicidade_juros
from tabatu.periodicidade import Periodicidade


class TestJurosConstante:
    juros = JurosConstante(0.05, Periodicidade["ANUAL"])
    _juros_mensal = alterar_periodicidade_juros(0.05, Periodicidade.ANUAL, Periodicidade.MENSAL)
    juros2 = JurosConstante(_juros_mensal, Periodicidade["MENSAL"])

    def test_fracionamento(self):
        assert (self.juros2.taxa_juros([2]).round(7) == np.array([0.0040741])).all()

    def test_taxa_juros(self):
        assert (
            self.juros.taxa_juros(np.arange(10)).round(2) == np.repeat(0.05, 10)
        ).all()

    def test_taxa_desconto(self):
        assert_array_equal(
            self.juros.taxa_desconto(np.arange(10)).round(7),
            np.array(
                [
                    1.0,
                    0.952381,
                    0.9070295,
                    0.8638376,
                    0.8227025,
                    0.7835262,
                    0.7462154,
                    0.7106813,
                    0.6768394,
                    0.6446089,
                ]
            ).round(7)
        )

    def test_alteracao_periodicidade(self):
        juros_mensal = self.juros.alterar_periodicidade(Periodicidade["MENSAL"])
        assert juros_mensal.periodicidade == Periodicidade.MENSAL
        assert juros_mensal.taxa_juros([0]) == self.juros2.taxa_juros([0])