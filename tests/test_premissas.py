from unittest.mock import Mock
from unittest.mock import MagicMock
from unittest.mock import Mock

import pytest
from numpy import array
from numpy import atleast_1d
from numpy import repeat
import pytest
from tabatu.juros_constante import JurosConstante

from tabatu.premissas import Premissas
from tabatu.premissas import PremissasRenda
from tabatu.premissas import PremissasRendaInvalidez
from tabatu.periodicidade import Periodicidade
from tabatu import Tabua, TabuaMDT


@pytest.fixture(scope="module")
def mock_tabua_acumulacao_anual():
    """Fixture da tabua mockada. Evita testar a classe tabua ao testar as coberturas.
    Entretanto, é preciso rodar o init para garantir que os testes vão quebrar em
    caso de mudança na interface das tábuas.
    """
    mock = MagicMock(spec_set=Tabua)
    mock.periodicidade = Periodicidade.ANUAL
    mock.numero_decrementos = 1
    mock.numero_vidas = 1
    mock.possui_fechamento_plato = Mock(return_value=False)
    mock.tempo_futuro_maximo = Mock(return_value=1200)
    mock.t_qx = Mock(return_value=array([0.3]))
    mock.tpx = Mock(return_value=array([0.7]))
    mock.tabuas = Mock()
    mock.tabuas.__len__ = Mock(return_value=1)
    return mock


@pytest.fixture(scope="module")
def mock_tabua_mdt_anual():
    mock = MagicMock(spec_set=TabuaMDT)
    mock.numero_decrementos = 1
    mock.numero_vidas = 1
    mock.possui_fechamento_plato = Mock(return_value=False)
    mock.tempo_futuro_maximo = Mock(return_value=1200)
    mock.periodicidade = Periodicidade.ANUAL
    mock.t_qx_j = Mock(return_value=array([0.4]))
    return mock


@pytest.fixture(scope="module")
def mock_premissas(mock_tabua_acumulacao_anual):
    mock = Mock()
    mock.periodicidade = Periodicidade.ANUAL
    mock.tabua = mock_tabua_acumulacao_anual
    mock.alterar_periodicidade = Mock(return_value=mock)
    return mock


@pytest.fixture(scope="module")
def mock_tabua_concessao_anual():
    """Fixture da tabua mockada. Evita testar a classe tabua ao testar as coberturas.
    Entretanto, é preciso rodar o init para garantir que os testes vão quebrar em
    caso de mudança na interface das tábuas.
    """
    mock = MagicMock(spec_set=Tabua)
    mock.periodicidade = Periodicidade.ANUAL
    mock.numero_decrementos = 1
    mock.numero_vidas = 1
    mock.possui_fechamento_plato = Mock(return_value=False)
    mock.tempo_futuro_maximo = Mock(return_value=1200)
    mock.t_qx = Mock(return_value=array([0.2]))
    mock.tpx = lambda x, t: repeat(0.8, len(atleast_1d(t)))
    mock.tabuas = Mock()
    mock.tabuas.__len__ = Mock(return_value=1)
    return mock


@pytest.fixture(scope="module")
def mock_juros_anual():
    """Fixtura da tabua mockada. Evita testar a classe juros ao testar as coberturas.
    Entretanto, é preciso rodar o init para garantir que os testes vão quebrar em
    caso de mudança na interface do juros.
    """
    mock = MagicMock(spec_set=JurosConstante)
    mock.periodicidade = Periodicidade.ANUAL
    mock.taxa_desconto = Mock(return_value=array([0.9]))
    return mock


def test_tabua_e_juros_precisam_ter_a_mesma_periodicidade(
    mock_tabua_acumulacao_anual, mock_juros_anual, monkeypatch
):
    """Tabua e juros devem possuir o mesmo fracionamento."""
    monkeypatch.setattr(
        mock_tabua_acumulacao_anual, "periodicidade", Periodicidade.MENSAL
    )
    with pytest.raises(ValueError):
        Premissas(mock_tabua_acumulacao_anual, mock_juros_anual)


def test_tabua_acumulacao_nao_pode_ter_fechamento_plato(
    mock_tabua_acumulacao_anual, mock_juros_anual, monkeypatch
):
    """4 - nao sao permitidas tabuas com fechamento plato"""
    monkeypatch.setattr(
        mock_tabua_acumulacao_anual,
        "possui_fechamento_plato",
        lambda *args, **kwargs: True,
    )
    with pytest.raises(ValueError):
        Premissas(mock_tabua_acumulacao_anual, mock_juros_anual)


def test_alterar_periodicidade_gera_nova_premissa_com_nova_tabua_e_novos_juros(
    mock_tabua_acumulacao_anual, mock_juros_anual, monkeypatch
):
    mock_alterar_periodicidade_tabua = Mock(return_value=mock_tabua_acumulacao_anual)
    mock_alterar_periodicidade_juros = Mock(return_value=mock_juros_anual)
    monkeypatch.setattr(
        mock_tabua_acumulacao_anual,
        "alterar_periodicidade",
        mock_alterar_periodicidade_tabua,
    )
    monkeypatch.setattr(
        mock_juros_anual, "alterar_periodicidade", mock_alterar_periodicidade_juros
    )

    premissas = Premissas(mock_tabua_acumulacao_anual, mock_juros_anual)
    nova_premissas = premissas.alterar_periodicidade(Periodicidade.MENSAL)

    mock_alterar_periodicidade_tabua.assert_called_once_with(Periodicidade.MENSAL)
    mock_alterar_periodicidade_juros.assert_called_once_with(Periodicidade.MENSAL)
    assert nova_premissas is not premissas


def test_tabua_concessao_e_outras_premissas_devem_ter_a_mesma_periodicidade(
    mock_tabua_acumulacao_anual,
    mock_tabua_concessao_anual,
    mock_juros_anual,
    monkeypatch,
):
    """4 - nao sao permitidas tabuas com fechamento plato"""
    monkeypatch.setattr(
        mock_tabua_concessao_anual, "periodicidade", Periodicidade.MENSAL
    )
    with pytest.raises(ValueError):
        PremissasRenda(
            tabua=mock_tabua_acumulacao_anual,
            tabua_concessao=mock_tabua_concessao_anual,
            juros=mock_juros_anual,
        )


def test_tabua_concessao_nao_pode_ter_fechamento_plato(
    mock_tabua_acumulacao_anual,
    mock_tabua_concessao_anual,
    mock_juros_anual,
    monkeypatch,
):
    """4 - nao sao permitidas tabuas com fechamento plato"""
    monkeypatch.setattr(
        mock_tabua_concessao_anual,
        "possui_fechamento_plato",
        lambda *args, **kwargs: True,
    )
    with pytest.raises(ValueError):
        PremissasRenda(
            tabua=mock_tabua_acumulacao_anual,
            tabua_concessao=mock_tabua_concessao_anual,
            juros=mock_juros_anual,
        )


def test_alterar_periodicidade_gera_nova_premissa_com_nova_tabua_e_novos_juros_e_nova_tabua_concessao(
    mock_tabua_acumulacao_anual,
    mock_tabua_concessao_anual,
    mock_juros_anual,
    monkeypatch,
):
    mock_alterar_periodicidade_tabua = Mock(return_value=mock_tabua_acumulacao_anual)
    mock_alterar_periodicidade_tabua_concessao = Mock(
        return_value=mock_tabua_concessao_anual
    )
    mock_alterar_periodicidade_juros = Mock(return_value=mock_juros_anual)
    monkeypatch.setattr(
        mock_tabua_acumulacao_anual,
        "alterar_periodicidade",
        mock_alterar_periodicidade_tabua,
    )
    monkeypatch.setattr(
        mock_juros_anual, "alterar_periodicidade", mock_alterar_periodicidade_juros
    )
    monkeypatch.setattr(
        mock_tabua_concessao_anual,
        "alterar_periodicidade",
        mock_alterar_periodicidade_tabua_concessao,
    )

    premissas = PremissasRenda(
        tabua=mock_tabua_acumulacao_anual,
        tabua_concessao=mock_tabua_concessao_anual,
        juros=mock_juros_anual,
    )
    nova_premissas = premissas.alterar_periodicidade(Periodicidade.MENSAL)

    mock_alterar_periodicidade_tabua.assert_called_once_with(Periodicidade.MENSAL)
    mock_alterar_periodicidade_juros.assert_called_once_with(Periodicidade.MENSAL)
    mock_alterar_periodicidade_tabua_concessao.assert_called_once_with(
        Periodicidade.MENSAL
    )
    assert nova_premissas is not premissas


def test_tabua_acumulacao_deve_ter_causa_principal_na_renda_invalidez(
    mock_tabua_mdt_anual, mock_tabua_concessao_anual, mock_juros_anual, monkeypatch
):
    monkeypatch.setattr(
        mock_tabua_mdt_anual, "possui_causa_principal", lambda *args, **kwargs: False
    )
    with pytest.raises(ValueError):
        PremissasRendaInvalidez(
            tabua=mock_tabua_mdt_anual,
            tabua_concessao=mock_tabua_concessao_anual,
            juros=mock_juros_anual,
        )
