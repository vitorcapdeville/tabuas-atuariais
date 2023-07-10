from unittest.mock import Mock

import pytest
from numpy import array
from numpy.testing import assert_array_equal

from tabatu.multiplas_vidas import TabuaMultiplasVidas, StatusVidasConjuntas


def test_tpx_retorna_produto_acumulado_de_um_menos_qx(mock_tabua1, mock_tabua2):
    tabua = TabuaMultiplasVidas(mock_tabua1, mock_tabua2, status=StatusVidasConjuntas.LAST)
    qx_mock = array([0.1, 0.2, 0.3])
    tabua.qx = Mock(return_value=qx_mock)
    assert tabua.tpx([0, 0], 0) == 1
    assert_array_equal(tabua.tpx([0, 0], [1, 2, 3]), [0.9, 0.9 * 0.8, 0.9 * 0.8 * 0.7])


def test_qx_retorna_o_produto_de_qx_de_cada_tabua_quando_status_eh_last(mock_tabua1, mock_tabua2):
    tabua = TabuaMultiplasVidas(mock_tabua1, mock_tabua2, status=StatusVidasConjuntas.LAST)
    resultado = tabua.qx([0, 0], [1, 2, 3])
    esperado = mock_tabua1.tabuas[0].qx() * mock_tabua2.tabuas[0].qx()
    assert_array_equal(resultado, esperado)


def test_qx_retorna_um_menos_o_produto_de_1_menos_qx_quando_status_eh_joint(mock_tabua1, mock_tabua2):
    tabua = TabuaMultiplasVidas(mock_tabua1, mock_tabua2, status=StatusVidasConjuntas.JOINT)
    resultado = tabua.qx([0, 0], [1, 2, 3])
    esperado = 1 - (1 - mock_tabua1.tabuas[0].qx()) * (1 - mock_tabua2.tabuas[0].qx())
    assert_array_equal(resultado, esperado)


def test_qx_falha_quando_tamanho_de_x_eh_incompativel_com_a_qntd_de_tabuas(mock_tabua1, mock_tabua2):
    tabua = TabuaMultiplasVidas(mock_tabua1, mock_tabua2, status=StatusVidasConjuntas.JOINT)
    with pytest.raises(ValueError):
        tabua.qx([0], [1, 2, 3])
    with pytest.raises(ValueError):
        tabua.qx([0, 0, 0], [1, 2, 3])


def test_tempo_futuro_max_retorna_o_menor_dos_tempos_quando_status_eh_joint(mock_tabua1, mock_tabua2):
    tabua = TabuaMultiplasVidas(mock_tabua1, mock_tabua2, status=StatusVidasConjuntas.JOINT)
    assert tabua.tempo_futuro_maximo([0, 0]) == min(
        mock_tabua1.tabuas[0].tempo_futuro_maximo(0),
        mock_tabua2.tabuas[0].tempo_futuro_maximo(0)
    )


def test_tempo_futuro_max_retorna_o_maior_dos_tempos_quando_status_eh_last(mock_tabua1, mock_tabua2):
    tabua = TabuaMultiplasVidas(mock_tabua1, mock_tabua2, status=StatusVidasConjuntas.LAST)
    assert tabua.tempo_futuro_maximo([0, 0]) == max(
        mock_tabua1.tabuas[0].tempo_futuro_maximo(0),
        mock_tabua2.tabuas[0].tempo_futuro_maximo(0)
    )


def test_tempo_futuro_max_falha_quando_o_tamanho_de_x_eh_incompativel_com_a_qntd_de_tabuas(mock_tabua1, mock_tabua2):
    tabua = TabuaMultiplasVidas(mock_tabua1, mock_tabua2, status=StatusVidasConjuntas.LAST)
    with pytest.raises(ValueError):
        tabua.tempo_futuro_maximo([0])
    with pytest.raises(ValueError):
        tabua.tempo_futuro_maximo([0, 0, 0])
