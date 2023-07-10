# distutils: language = c++

from TabuaBaseCpp cimport TabuaBaseCpp
from TabuaCpp cimport TabuaCpp
from TabuaMDTCpp cimport TabuaMDTCpp
from libcpp.vector cimport vector
import numpy as np

cdef class TabuaBase:
    cdef TabuaBaseCpp c_tabua

    def __init__(self, qx = None):
        if qx is None:
            self.c_tabua = TabuaBaseCpp()
        else:
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
    def numero_decrementos(self):
        return self.c_tabua.pega_numero_decrementos()

    @property
    def tabuas(self):
        cdef vector[TabuaBaseCpp] tabuas_cpp = self.c_tabua.pega_tabuas()
        tabuas = []
        for i in range(tabuas_cpp.size()):
            tabua = TabuaBase()
            tabua.c_tabua = tabuas_cpp[i]
            tabuas.append(tabua)
        return tuple(tabuas)

cdef class TabuaMDT:
    cdef TabuaMDTCpp c_tabua

    def __init__(self, *tabuas):
        cdef vector[TabuaCpp] tabuas_vec
        for i in range(len(tabuas)):
            tabua: Tabua = tabuas[i]
            tabuas_vec.push_back(tabua.c_tabua)
        self.c_tabua = TabuaMDTCpp(tabuas_vec)

    def qx_j(self, vector[int] x, vector[double] t, vector[int] j):
        return np.atleast_2d(self.c_tabua.qx_j(x, t, j))

    def qx(self, vector[int] x, vector[double] t):
        return np.atleast_1d(self.c_tabua.qx(x, t))

    def tpx(self,  vector[int] x, vector[double] t):
        return np.atleast_1d(self.c_tabua.tpx(x, t))

    def t_qx(self, vector[int] x, vector[double] t):
        return np.atleast_1d(self.c_tabua.t_qx(x, t))

    def tempo_futuro_maximo(self, x):
        return self.c_tabua.tempo_futuro_maximo(x)

    def possui_fechamento_plato(self):
        return self.c_tabua.possui_fechamento_plato()

    @property
    def numero_vidas(self):
        return self.c_tabua.pega_numero_vidas()

    @property
    def numero_decrementos(self):
        return self.c_tabua.pega_numero_decrementos()

    @property
    def tabuas(self):
        cdef vector[TabuaBaseCpp] tabuas_cpp = self.c_tabua.pega_tabuas()
        tabuas = []
        for i in range(tabuas_cpp.size()):
            tabua = TabuaBase()
            tabua.c_tabua = tabuas_cpp[i]
            tabuas.append(tabua)
        return tuple(tabuas)
