from unittest.mock import Mock

import pytest
from numpy import array
from numpy.testing import assert_array_equal

import tabatu.unico_decremento as unico_decremento
from tabatu import Tabua
from tabatu.periodicidade import Periodicidade


@pytest.fixture
def mock_tabua_base(monkeypatch):
    mock_tabua_base = Mock()
    mock_tabua_base.tpx = Mock(return_value=2)
    mock_tabua_base.qx = Mock(return_value=3)
    mock_tabua_base.tempo_futuro_maximo = Mock()
    mock_tabua_base.alterar_periodicidade = Mock()
    monkeypatch.setattr(
        unico_decremento, "TabuaBase", Mock(return_value=mock_tabua_base)
    ) 
    return mock_tabua_base


@pytest.mark.parametrize("x", [array([0]), [0], (0,)])
class TestArgumentosSaoPassadosComoInteirosNosMetodosDeTabua:
    def test_tpx_passa_argumentos_para_tabua_base_quando_x_eh_inteiro_ou_array_like(
        self, tabua_1dt_1, x
    ):
        assert_array_equal(
            tabua_1dt_1.tpx([0], [0, 1, 2]), tabua_1dt_1.tpx(x, [0, 1, 2])
        )

    def test_t_qx_passa_argumentos_para_tabua_base_quando_x_eh_inteiro_ou_array_like(
        self, tabua_1dt_1, x
    ):
        assert_array_equal(
            tabua_1dt_1.t_qx([0], [0, 1, 2]), tabua_1dt_1.t_qx(x, [0, 1, 2])
        )

    def test_qx_passa_argumentos_para_tabua_base_quando_x_eh_array_de_um_elemento(
        self, tabua_1dt_1, x
    ):
        assert_array_equal(tabua_1dt_1.qx([0], [0, 1, 2]), tabua_1dt_1.qx(x, [0, 1, 2]))

    def test_tempo_futuro_max_passa_argumentos_para_tabua_base_quando_x_eh_array_de_um_elemento(
        self, tabua_1dt_1, x
    ):
        assert_array_equal(
            tabua_1dt_1.tempo_futuro_maximo([0]), tabua_1dt_1.tempo_futuro_maximo(x)
        )


@pytest.mark.parametrize("x", [array([0, 0]), [0, 0], (0, 0)])
class TestMetodosFalhamQuandoXPossuiMaisQueUmElemento:
    def test_tpx_falha_quando_x_possui_mais_que_um_elemento(self, tabua_1dt_1, x):
        with pytest.raises(ValueError):
            tabua_1dt_1.tpx(x, [0])

    def test_t_qx_falha_quando_x_possui_mais_que_um_elemento(self, tabua_1dt_1, x):
        with pytest.raises(ValueError):
            tabua_1dt_1.t_qx(x, [0])

    def test_qx_falha_quando_x_possui_mais_que_um_elemento(self, tabua_1dt_1, x):
        with pytest.raises(ValueError):
            tabua_1dt_1.qx(x, [0])

    def test_tempo_futuro_max_falha_quando_x_possui_mais_que_um_elemento(
        self, tabua_1dt_1, x
    ):
        with pytest.raises(ValueError):
            tabua_1dt_1.tempo_futuro_maximo(x)


def test_alterar_periodicidade_chama_alterar_periodicidade_da_tabua_base_e_gera_nova_tabua(
    monkeypatch, mock_tabua_base, tabua_1dt_1
):
    mock_init = Mock(return_value=None)
    monkeypatch.setattr(Tabua, "__init__", mock_init)

    nova_tabua = tabua_1dt_1.alterar_periodicidade(Periodicidade.MENSAL)

    mock_tabua_base.alterar_periodicidade.assert_called_once_with(Periodicidade.MENSAL)
    mock_init.assert_called_once_with(
        mock_tabua_base.alterar_periodicidade.return_value.pega_qx(),
        mock_tabua_base.alterar_periodicidade.return_value.periodicidade,
    )

    assert isinstance(nova_tabua, Tabua)
