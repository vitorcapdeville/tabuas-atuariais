from unittest.mock import Mock, MagicMock
import pytest
from numpy import array
from numpy.testing import assert_array_equal

from tabatu import TabuaMDT
from tabatu.multiplos_decrementos import qx2qxj
from tabatu.multiplos_decrementos import converter_mdt
from tabatu.multiplos_decrementos import valida_quantidade_tabuas
from tabatu.multiplos_decrementos import captura_argumentos
import tabatu.multiplos_decrementos as tabuas_mdt


class TestCapturaArgumentos:
    def test_a_chave_eh_a_posicao_do_argumento_como_string_e_o_valor_eh_a_posicao_quando_argumento_nao_nomeado(self):
        assert captura_argumentos(10, 20) == {'0': 0, '1': 1}

    def test_a_chave_eh_o_nome_e_o_valor_eh_a_posicao_quando_argumento_eh_nomeado(self):
        assert captura_argumentos(a=10, b=20) == {'a': 0, 'b': 1}
        assert captura_argumentos(b=10, a=20) == {'b': 0, 'a': 1}

    def test_captura_argumentos_funciona_com_argumentos_nomeados_e_nao_nomeados(self):
        assert captura_argumentos(10, b=20) == {'0': 0, 'b': 1}


class TestQx2qxj:
    @pytest.mark.parametrize(
        'qx1, qx2',
        [
            (array([0.1, 0.2, 0.3]), array([0.9, 0.8, 0.7])),
            (array([0.1, 0.2, 0.3]), 0),
            (array([0.1]), 0),
        ]
    )
    def test_qx2qxj_retorna_um_array_com_o_mesmo_numero_de_elementos_de_qx1(self, qx1, qx2):
        assert len(qx2qxj(qx1, qx2)) == len(qx1)

    def test_quando_todos_os_outros_decrementos_sao_zero_retorna_qx1(self):
        qx1 = array([0.1, 0.2, 0.3])
        assert_array_equal(qx1, qx2qxj(qx1, 0, 0))
        assert_array_equal(qx1, qx2qxj(qx1, 0))

    def test_quando_sao_fornecidos_arrays_de_tamanho_diferente_e_maior_que_1_deve_falhar(self):
        with pytest.raises(ValueError):
            qx2qxj(array([0.1, 0.2]), array([0.9, 0.8, 0.7]))


class TestConverterMDT:
    def test_retorna_array_com_numero_de_dimensoes_igual_a_quantidade_de_inputs(self):
        assert converter_mdt(array([0.1, 0.2, 0.3])).shape == (1, 3)
        assert converter_mdt(array([0.1, 0.2, 0.3]), array([0.9, 0.8, 0.7])).shape == (2, 3)
        assert converter_mdt(array([0.1, 0.2]), array([0.9, 0.8]), array([0.4, 0.3])).shape == (3, 2)

    def test_quando_arrays_de_tamanho_diferentes_deve_falhar(self):
        with pytest.raises(ValueError):
            converter_mdt(array([0.1, 0.2]), array([0.9, 0.8, 0.7]))


class TestValidaQuantidadeDeTabuas:
    def test_quando_existem_mais_que_3_tabuas_deve_falhar(self):
        with pytest.raises(ValueError):
            valida_quantidade_tabuas(Mock(), Mock(), Mock(), Mock())

    def test_quando_nao_existem_tabuas_deve_falhar(self):
        with pytest.raises(ValueError):
            valida_quantidade_tabuas()

    @pytest.mark.parametrize("args", [(1,), (1, 2), (1, 2, 3)])
    def test_quando_existem_de_uma_a_tres_tabuas_deve_retornar_tupla_com_elas(self, args: tuple):
        resultado = valida_quantidade_tabuas(*args)
        assert isinstance(resultado, tuple)
        for i in range(len(args)):
            assert args[i] == resultado[i]


class TestTabuaMDT:
    def test_init_falha_se_causa_principal_eh_invalida(self, mock_tabua1, mock_tabua2):
        with pytest.raises(ValueError):
            TabuaMDT(mock_tabua1, mock_tabua2, causa_principal=3)

        with pytest.raises(ValueError):
            TabuaMDT(mock_tabua1, morte=mock_tabua2, causa_principal="invalidez")

    def test_tpx_eh_o_produto_dos_tpxs_de_cada_tabua(self, mock_tabua1, mock_tabua2):
        tabua = TabuaMDT(mock_tabua1, mock_tabua2)
        resultado = tabua.tpx([1, 2], 0)
        mock_tabua1.tabuas[0].tpx.assert_called_once_with(array([1]), 0)
        mock_tabua2.tabuas[0].tpx.assert_called_once_with(array([2]), 0)
        esperado = mock_tabua1.tabuas[0].tpx() * mock_tabua2.tabuas[0].tpx()
        assert_array_equal(resultado, esperado)

    def test_tpx_funciona_com_apenas_uma_idade(self, mock_tabua1, mock_tabua2):
        tabua = TabuaMDT(mock_tabua1, mock_tabua2)
        resultado = tabua.tpx(1, 0)
        mock_tabua1.tabuas[0].tpx.assert_called_once_with(array([1]), 0)
        mock_tabua2.tabuas[0].tpx.assert_called_once_with(array([1]), 0)
        esperado = mock_tabua1.tabuas[0].tpx() * mock_tabua2.tabuas[0].tpx()
        assert_array_equal(resultado, esperado)

    def test_tpx_falha_quando_o_numero_de_tabuas_nao_eh_1_e_nao_eh_compativel_com_o_numero_de_decrementos(
        self, mock_tabua1, mock_tabua2
    ):
        tabua = TabuaMDT(mock_tabua1, mock_tabua2)
        with pytest.raises(ValueError):
            tabua.tpx([1, 1, 1], 0)

    def test_qx_j_retorna_uma_array_com_2_dimensoes(self, mock_tabua1, mock_tabua2):
        tabua = TabuaMDT(mock_tabua1, mock_tabua2)
        assert tabua.qx_j(0, 0, 1).shape == (1, len(mock_tabua1.tabuas[0].qx()))
        assert tabua.qx_j(0, 0, [0, 1]).shape == (2, len(mock_tabua1.tabuas[0].qx()))

    def test_qx_j_chama_converter_mdt_com_qx_das_tabuas(self, mock_tabua1, mock_tabua2, monkeypatch):
        tabua = TabuaMDT(mock_tabua1, mock_tabua2)
        mock_converter_mdt = MagicMock()
        monkeypatch.setattr(tabuas_mdt, "converter_mdt", mock_converter_mdt)
        tabua.qx_j(0, 0, 1)
        mock_converter_mdt.assert_called_once_with(mock_tabua1.tabuas[0].qx(), mock_tabua2.tabuas[0].qx())

    def test_qx_j_aceita_string_quando_as_tabuas_sao_passadas_por_nome(self, mock_tabua1, mock_tabua2):
        tabua = TabuaMDT(mock_tabua1, causa1=mock_tabua2)
        assert tabua.qx_j(0, 0, 1).shape == (1, len(mock_tabua1.tabuas[0].qx()))
        assert tabua.qx_j(0, 0, [0, 1]).shape == (2, len(mock_tabua1.tabuas[0].qx()))
        assert tabua.qx_j(0, 0, [0, "causa1"]).shape == (2, len(mock_tabua1.tabuas[0].qx()))
        assert tabua.qx_j(0, 0, ["0", "causa1"]).shape == (2, len(mock_tabua1.tabuas[0].qx()))
        assert tabua.qx_j(0, 0, "causa1").shape == (1, len(mock_tabua1.tabuas[0].qx()))

    def test_qx_j_falha_quando_o_numero_de_tabuas_nao_eh_1_e_nao_eh_compativel_com_o_numero_de_decrementos(
        self, mock_tabua1, mock_tabua2
    ):
        tabua = TabuaMDT(mock_tabua1, mock_tabua2)
        with pytest.raises(ValueError):
            tabua.qx_j([1, 1, 1], 0, 1)

    def test_qx_chama_qx_j_com_todas_as_causas_e_retorna_array_com_uma_dimensao(self, mock_tabua1, mock_tabua2):
        tabua = TabuaMDT(mock_tabua1, mock_tabua2)
        tabua.qx_j = Mock(return_value=array([[0.1, 0.2, 0.3], [0.3, 0.5, 0.8]]))
        resultado = tabua.qx([0, 0], 1)
        tabua.qx_j.assert_called_once()
        assert tabua.qx_j.call_args[0][0] == [0, 0]
        assert tabua.qx_j.call_args[0][1] == 1
        assert_array_equal(tabua.qx_j.call_args[0][2], array([0, 1]))
        assert resultado.ndim == 1

    def test_qx_j_retorna_array_com_2_dimensoes(self, mock_tabua1, mock_tabua2):
        tabua = TabuaMDT(mock_tabua1, mock_tabua2)
        assert tabua.qx_j(0, 0, 1).shape == (1, len(mock_tabua1.tabuas[0].qx()))
        assert tabua.qx_j(0, 0, [0, 1]).shape == (2, len(mock_tabua1.tabuas[0].qx()))

    def test_tempo_futuro_max_retorna_o_menor_dos_tempos_de_cada_tabua(self, mock_tabua1, mock_tabua2):
        tabua = TabuaMDT(mock_tabua1, mock_tabua2)
        assert tabua.tempo_futuro_max(4) == min(
            mock_tabua1.tabuas[0].tempo_futuro_max(), mock_tabua2.tabuas[0].tempo_futuro_max()
        )

    def test_tempo_futuro_maximo_falha_quando_a_quantidadde_de_idades_eh_incompativel(self, mock_tabua1, mock_tabua2):
        tabua = TabuaMDT(mock_tabua1, mock_tabua2)
        with pytest.raises(ValueError):
            tabua.tempo_futuro_max([5, 5, 5])

    def test_t_qx_considera_apenas_a_causa_principal_quando_ela_eh_fornecida(self, mock_tabua1, mock_tabua2):
        tabua = TabuaMDT(mock_tabua1, mock_tabua2, causa_principal=1)
        tabua.t_qx_j = Mock(return_value=array([[0.3, 0.5, 0.8]]))
        resultado = tabua.t_qx([0, 0], 1)
        tabua.t_qx_j.assert_called_once_with([0, 0], 1, '1')
        assert resultado.ndim == 1
