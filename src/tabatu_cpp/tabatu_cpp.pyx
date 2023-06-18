# distutils: language = c++

from Tabua cimport Tabua
from libcpp.vector cimport vector
import numpy as np

cdef class PyTabua:
    cdef Tabua c_tabua

    def __init__(self, qx):
        self.c_tabua = Tabua(qx)

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
