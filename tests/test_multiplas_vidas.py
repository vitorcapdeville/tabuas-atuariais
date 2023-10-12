from unittest.mock import Mock, call

import pytest
from numpy import cumprod
from numpy.testing import assert_array_equal

import tabatu.multiplas_vidas as tabuas_mvd_modulo
import tabatu.tabua_base as tabua_base_modulo
from tabatu.multiplas_vidas import StatusVidasConjuntas, TabuaMultiplasVidas
from tabatu.periodicidade import Periodicidade


def test_tpx_retorna_produto_acumulado_de_um_menos_qx(tabua_1dt_1, tabua_1dt_2):
    tabua = TabuaMultiplasVidas(
        tabua_1dt_1, tabua_1dt_2, status=StatusVidasConjuntas.LAST
    )
    assert tabua.tpx([0, 0], [0]) == 1
    assert_array_equal(
        tabua.tpx([0, 0], [1, 2, 3]), cumprod(1 - tabua.qx([0, 0], [0, 1, 2]))
    )


def test_qx_retorna_o_produto_de_qx_de_cada_tabua_quando_status_eh_last(
    tabua_1dt_1, tabua_1dt_2
):
    tabua = TabuaMultiplasVidas(
        tabua_1dt_1, tabua_1dt_2, status=StatusVidasConjuntas.LAST
    )
    resultado = tabua.qx([0, 0], [1, 2, 3])
    esperado = tabua_1dt_1.tabuas[0].qx(0, [1, 2, 3]) * tabua_1dt_2.tabuas[0].qx(
        0, [1, 2, 3]
    )
    assert_array_equal(resultado, esperado)


def test_qx_retorna_um_menos_o_produto_de_1_menos_qx_quando_status_eh_joint(
    tabua_1dt_1, tabua_1dt_2
):
    tabua = TabuaMultiplasVidas(
        tabua_1dt_1, tabua_1dt_2, status=StatusVidasConjuntas.JOINT
    )
    resultado = tabua.qx([0, 0], [1, 2, 3])
    esperado = 1 - (1 - tabua_1dt_1.tabuas[0].qx(0, [1, 2, 3])) * (
        1 - tabua_1dt_2.tabuas[0].qx(0, [1, 2, 3])
    )
    assert_array_equal(resultado, esperado)


def test_qx_falha_quando_tamanho_de_x_eh_incompativel_com_a_qntd_de_tabuas(
    tabua_1dt_1, tabua_1dt_2
):
    tabua = TabuaMultiplasVidas(
        tabua_1dt_1, tabua_1dt_2, status=StatusVidasConjuntas.JOINT
    )
    with pytest.raises(ValueError):
        tabua.qx([0], [1, 2, 3])
    with pytest.raises(ValueError):
        tabua.qx([0, 0, 0], [1, 2, 3])


def test_tempo_futuro_max_retorna_o_menor_dos_tempos_quando_status_eh_joint(
    tabua_1dt_1, tabua_1dt_2
):
    tabua = TabuaMultiplasVidas(
        tabua_1dt_1, tabua_1dt_2, status=StatusVidasConjuntas.JOINT
    )
    assert tabua.tempo_futuro_maximo([0, 0]) == min(
        tabua_1dt_1.tabuas[0].tempo_futuro_maximo(0),
        tabua_1dt_2.tabuas[0].tempo_futuro_maximo(0),
    )


def test_tempo_futuro_max_retorna_o_maior_dos_tempos_quando_status_eh_last(
    tabua_1dt_1, tabua_1dt_2
):
    tabua = TabuaMultiplasVidas(
        tabua_1dt_1, tabua_1dt_2, status=StatusVidasConjuntas.LAST
    )
    assert tabua.tempo_futuro_maximo([0, 0]) == max(
        tabua_1dt_1.tabuas[0].tempo_futuro_maximo(0),
        tabua_1dt_2.tabuas[0].tempo_futuro_maximo(0),
    )


def test_tempo_futuro_max_falha_quando_o_tamanho_de_x_eh_incompativel_com_a_qntd_de_tabuas(
    tabua_1dt_1, tabua_1dt_2
):
    tabua = TabuaMultiplasVidas(
        tabua_1dt_1, tabua_1dt_2, status=StatusVidasConjuntas.LAST
    )
    with pytest.raises(ValueError):
        tabua.tempo_futuro_maximo([0])
    with pytest.raises(ValueError):
        tabua.tempo_futuro_maximo([0, 0, 0])


def test_alterar_periodicidade_chama_alterar_periodicidade_da_tabua_base_e_gera_nova_tabua_mvd(
    monkeypatch, tabua_1dt_1, tabua_1dt_2
):
    tabua = TabuaMultiplasVidas(
        tabua_1dt_1, tabua_1dt_2, status=StatusVidasConjuntas.LAST
    )

    monkeypatch.setattr(
        tabuas_mvd_modulo.Tabua, "from_tabua_base", Mock(return_value=tabua_1dt_1)
    )
    mock_alterar_periodicidade = Mock()
    monkeypatch.setattr(
        tabua_base_modulo.TabuaBase, "alterar_periodicidade", mock_alterar_periodicidade
    )
    nova_tabua = tabua.alterar_periodicidade(Periodicidade.MENSAL)

    mock_alterar_periodicidade.assert_has_calls(
        [call(Periodicidade.MENSAL), call(Periodicidade.MENSAL)]
    )

    assert isinstance(nova_tabua, TabuaMultiplasVidas)
    assert nova_tabua.status == tabua.status
