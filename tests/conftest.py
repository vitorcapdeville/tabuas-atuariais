from unittest.mock import Mock

import pytest
from numpy import array

qx_plato = array([0.1, 0.3, 0.5, 0.7, 0.9])
qx_completo = array([0.1, 0.2, 0.4, 0.8, 1.0])


@pytest.fixture
def mock_tabua1(monkeypatch):
    mock_tabua = Mock()
    mock_tabua.tabuas = (Mock(),)
    mock_tabua.tabuas[0].qx = Mock(return_value=array([0.1, 0.2, 0.3]))
    mock_tabua.tabuas[0].tpx = Mock(return_value=array([0.9, 0.8, 0.7]))
    mock_tabua.tabuas[0].tempo_futuro_max = Mock(return_value=3)
    mock_tabua.periodicidade = 1
    return mock_tabua


@pytest.fixture
def mock_tabua2(monkeypatch):
    mock_tabua = Mock()
    mock_tabua.tabuas = (Mock(),)
    mock_tabua.tabuas[0].qx = Mock(return_value=array([0.3, 0.5, 0.8]))
    mock_tabua.tabuas[0].tpx = Mock(return_value=array([0.7, 0.4, 0.2]))
    mock_tabua.tabuas[0].tempo_futuro_max = Mock(return_value=2)
    mock_tabua.periodicidade = 1
    return mock_tabua
