from unittest.mock import Mock

import pytest
from numpy import array

import tabatu.unico_decremento as unico_decremento
from tabatu import Tabua

qx_mock = Mock()


@pytest.fixture
def mock_tabua_base(monkeypatch):
    mock_tabua_base = Mock()
    mock_tabua_base.tpx = Mock(return_value=2)
    mock_tabua_base.qx = Mock(return_value=3)
    mock_tabua_base.tempo_futuro_max = Mock()
    monkeypatch.setattr(unico_decremento, "TabuaBase", Mock(return_value=mock_tabua_base))
    return mock_tabua_base


@pytest.mark.parametrize("x", [array([0]), [0], (0,), 0])
class TestArgumentosSaoPassadosComoInteirosNosMetodosDeTabua:
    def test_tpx_passa_argumentos_para_tabua_base_quando_x_eh_inteiro_ou_array_like(self, mock_tabua_base, x):
        tabua = Tabua(qx_mock)
        tabua.tpx(x, 0)
        mock_tabua_base.tpx.assert_called_once_with(0, 0)

    def test_t_qx_passa_argumentos_para_tabua_base_quando_x_eh_inteiro_ou_array_like(self, mock_tabua_base, x):
        tabua = Tabua(qx_mock)
        assert tabua.t_qx(x, 0) == 2 * 3
        mock_tabua_base.tpx.assert_called_once_with(0, 0)
        mock_tabua_base.qx.assert_called_once_with(0, 0)

    def test_qx_passa_argumentos_para_tabua_base_quando_x_eh_array_de_um_elemento(self, mock_tabua_base, x):
        tabua = Tabua(qx_mock)
        tabua.qx(x, 0)
        mock_tabua_base.qx.assert_called_once_with(0, 0)

    def test_tempo_futuro_max_passa_argumentos_para_tabua_base_quando_x_eh_array_de_um_elemento(
        self, mock_tabua_base, x
    ):
        tabua = Tabua(qx_mock)
        tabua.tempo_futuro_max(x)
        mock_tabua_base.tempo_futuro_max.assert_called_once_with(0)


@pytest.mark.parametrize("x", [array([0, 0]), [0, 0], (0, 0)])
class TestMetodosFalhamQuandoXPossuiMaisQueUmElemento:
    def test_tpx_falha_quando_x_possui_mais_que_um_elemento(self, mock_tabua_base, x):
        tabua = Tabua(qx_mock)
        with pytest.raises(ValueError):
            tabua.tpx(x, 0)

    def test_t_qx_falha_quando_x_possui_mais_que_um_elemento(self, mock_tabua_base, x):
        tabua = Tabua(qx_mock)
        with pytest.raises(ValueError):
            tabua.t_qx(x, 0)

    def test_qx_falha_quando_x_possui_mais_que_um_elemento(self, mock_tabua_base, x):
        tabua = Tabua(qx_mock)
        with pytest.raises(ValueError):
            tabua.qx(x, 0)

    def test_tempo_futuro_max_falha_quando_x_possui_mais_que_um_elemento(self, mock_tabua_base, x):
        tabua = Tabua(qx_mock)
        with pytest.raises(ValueError):
            tabua.tempo_futuro_max(x)
