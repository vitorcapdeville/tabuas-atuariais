from unittest.mock import Mock

import pytest
from numpy import array
from tabatu.multiplas_vidas import StatusVidasConjuntas, TabuaMultiplasVidas
from tabatu.multiplos_decrementos import TabuaMDT

from tabatu.unico_decremento import Tabua

qx_plato = array([0.1, 0.3, 0.5, 0.7, 0.9])
qx_completo = array([0.1, 0.2, 0.4, 0.8, 1.0])


@pytest.fixture
def mock_tabua1(monkeypatch):
    mock_tabua = Mock()
    mock_tabua.tabuas = (Mock(),)
    mock_tabua.tabuas[0].qx = Mock(return_value=array([0.1, 0.2, 0.3]))
    mock_tabua.tabuas[0].tpx = Mock(return_value=array([0.9, 0.8, 0.7]))
    mock_tabua.tabuas[0].tempo_futuro_maximo = Mock(return_value=3)
    mock_tabua.periodicidade = 1
    return mock_tabua


@pytest.fixture
def mock_tabua2(monkeypatch):
    mock_tabua = Mock()
    mock_tabua.tabuas = (Mock(),)
    mock_tabua.tabuas[0].qx = Mock(return_value=array([0.3, 0.5, 0.8]))
    mock_tabua.tabuas[0].tpx = Mock(return_value=array([0.7, 0.4, 0.2]))
    mock_tabua.tabuas[0].tempo_futuro_maximo = Mock(return_value=2)
    mock_tabua.periodicidade = 1
    return mock_tabua

@pytest.fixture
def tabua_1dt_1():
    tabua = Tabua(array([0.1, 0.2, 0.3, 0.4, 1.0]))
    return tabua

@pytest.fixture
def tabua_1dt_2():
    tabua = Tabua(array([0.9, 0.8, 0.7, 0.6]))
    return tabua

@pytest.fixture
def tabua_mdt(tabua_1dt_1, tabua_1dt_2):
    tabua = TabuaMDT(tabua_1dt_1, causa1=tabua_1dt_2, causa_principal="causa1")
    return tabua

@pytest.fixture
def tabua_mvd(tabua_1dt_1, tabua_1dt_2):
    tabua = TabuaMultiplasVidas(tabua_1dt_1, causa1=tabua_1dt_2, status=StatusVidasConjuntas.LAST)
    return tabua