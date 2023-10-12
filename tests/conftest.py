import pytest
from numpy import array

from tabatu.multiplas_vidas import StatusVidasConjuntas, TabuaMultiplasVidas
from tabatu.multiplos_decrementos import TabuaMDT
from tabatu.unico_decremento import Tabua

qx_plato = array([0.1, 0.3, 0.5, 0.7, 0.9])
qx_completo = array([0.1, 0.2, 0.4, 0.8, 1.0])


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
    tabua = TabuaMultiplasVidas(
        tabua_1dt_1, causa1=tabua_1dt_2, status=StatusVidasConjuntas.LAST
    )
    return tabua
