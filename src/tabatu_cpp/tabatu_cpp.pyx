# distutils: language = c++

from TabuaBaseCpp cimport TabuaBaseCpp
from TabuaCpp cimport TabuaCpp
from libcpp.vector cimport vector
import numpy as np

cdef class TabuaBase:
    cdef TabuaBaseCpp c_tabua

    def __init__(self, qx):
        self.c_tabua = TabuaBaseCpp(qx)

    def qx(self, int x, vector[double] t):
        return np.array(self.c_tabua.qx(x, t))

    def tpx(self,  int x, vector[double] t):
        return np.array(self.c_tabua.tpx(x, t))

    def t_qx(self, int x, vector[double] t):
        return np.array(self.c_tabua.t_qx(x, t))

    def tempo_futuro_maximo(self, x):
        return self.c_tabua.tempo_futuro_maximo(x)

    def possui_fechamento_plato(self):
        return self.c_tabua.possui_fechamento_plato()


cdef class Tabua:
    cdef TabuaCpp c_tabua

    def __init__(self, qx):
        self.c_tabua = TabuaCpp(qx)

    def qx(self, int x, vector[double] t):
        return np.array(self.c_tabua.qx(x, t))

    def tpx(self,  int x, vector[double] t):
        return np.array(self.c_tabua.tpx(x, t))

    def t_qx(self, int x, vector[double] t):
        return np.array(self.c_tabua.t_qx(x, t))

    def tempo_futuro_maximo(self, x):
        return self.c_tabua.tempo_futuro_maximo(x)

    def possui_fechamento_plato(self):
        return self.c_tabua.possui_fechamento_plato()

    @property
    def numero_vidas(self):
        return self.c_tabua.pega_numero_vidas()

    @property
    def numero_vidas(self):
        return self.c_tabua.pega_numero_vidas()
