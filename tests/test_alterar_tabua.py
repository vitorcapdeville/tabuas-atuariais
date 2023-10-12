import pytest
from numpy import array
from numpy import repeat
from numpy.testing import assert_array_almost_equal
from numpy.testing import assert_array_equal

from tabatu.periodicidade import Periodicidade
from tabatu.alterar_tabua import agravar_qx
from tabatu.alterar_tabua import alterar_periodicidade_qx


class TestAlterarPeriodicidade:
    def test_alterar_periodicidade_funciona_quando_periodicidade_aumenta(self):
        qx_original = array([0.1, 0.5, 0.7, 1.0])
        qx_alterado = alterar_periodicidade_qx(qx_original, Periodicidade.BIMESTRAL, Periodicidade.MENSAL)
        qx_esperado = 1 - (1 - repeat(qx_original, 2)) ** (1 / 2)
        assert_array_equal(qx_esperado, qx_alterado)

    def test_alterar_periodicidade_funciona_quando_periodicidade_diminui(self):
        qx_original = array([0.1, 0.1, 0.5, 0.5, 0.7, 0.7, 1.0])
        qx_alterado = alterar_periodicidade_qx(qx_original, Periodicidade.MENSAL, Periodicidade.BIMESTRAL)
        qx_esperado = 1 - (1 - qx_original[0:len(qx_original):2]) ** 2
        assert_array_equal(qx_esperado, qx_alterado)

    @pytest.mark.parametrize("periodicidade", [Periodicidade.MENSAL, Periodicidade.SEMESTRAL, Periodicidade.ANUAL, ])
    def test_alterar_para_mesma_periodicidade_retorna_o_qx_original(self, periodicidade):
        qx_original = array([0.1, 0.5, 0.7, 1.0])
        qx_alterado = alterar_periodicidade_qx(qx_original, periodicidade, periodicidade)
        assert_array_equal(qx_original, qx_alterado)

    def test_aumentar_periodicidade_de_qx_que_nao_possui_taxas_constantes_nos_subintervalos_retorna_erro(self):
        """Se o qx mensal, por exemplo, não possui taxas constantes em todos os meses do mesmo ano, torná-lo anual
        resultaria em perda de informação."""
        qx_mensal = array([0.1, 0.5, 0.7, 1.0])
        with pytest.raises(ValueError):
            alterar_periodicidade_qx(qx_mensal, Periodicidade.MENSAL, Periodicidade.ANUAL)

    def test_reduzir_e_aumentar_a_periodicidade_do_mesmo_qx_resulta_no_qx_original(self):
        qx_original = array([0.1, 0.5, 0.7, 1.0])
        qx_reduzido = alterar_periodicidade_qx(qx_original, Periodicidade.ANUAL, Periodicidade.MENSAL)
        qx_aumentado = alterar_periodicidade_qx(qx_reduzido, Periodicidade.MENSAL, Periodicidade.ANUAL)
        assert_array_almost_equal(qx_original, qx_aumentado)

    def test_aumentar_e_reduzir_a_periodicidade_do_mesmo_qx_resulta_no_qx_original(self):
        qx_original = repeat(array([0.1, 0.5, 0.7, 1.0]), 12)
        qx_aumentado = alterar_periodicidade_qx(qx_original, Periodicidade.MENSAL, Periodicidade.ANUAL)
        qx_reduzido = alterar_periodicidade_qx(qx_aumentado, Periodicidade.ANUAL, Periodicidade.MENSAL)
        assert_array_almost_equal(qx_original, qx_reduzido)

    def test_alterar_periodicidade_falha_quando_reduzindo_e_periodicidades_sao_incompativeis(self):
        """Não é possível aumentar a periodicidade quando a nova periodicidade não é múltipla da antiga."""
        qx_original = array([0.1, 0.5, 0.7, 1.0])
        with pytest.raises(ValueError):
            alterar_periodicidade_qx(qx_original, Periodicidade.TRIMESTRAL, Periodicidade.BIMESTRAL)

    def test_alterar_periodicidade_falha_quando_aumentando_e_periodicidades_sao_incompativeis(self):
        """Não é possível reduzir a periodicidade quando a periodicidade antiga não é multipla da nova"""
        qx_original = array([0.1, 0.5, 0.7, 1.0])
        with pytest.raises(ValueError):
            alterar_periodicidade_qx(qx_original, Periodicidade.BIMESTRAL, Periodicidade.TRIMESTRAL)


class TestAgravarQx:
    def test_agravar_qx_nao_gera_qx_com_valores_acima_de_1(self):
        qx_original = array([0.1, 0.5, 0.7, 1.0])
        qx_agravado = agravar_qx(qx_original, 150)
        assert_array_almost_equal(qx_agravado, array([0.1 * 1.5, 0.5 * 1.5, 1.0, 1.0]))

    def test_agravar_qx_falha_com_percentual_negativo(self):
        qx_original = array([0.1, 0.5, 0.7, 1.0])
        with pytest.raises(ValueError):
            agravar_qx(qx_original, -15)