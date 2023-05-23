# distutils: language = c++

from Tabua cimport Tabua
from Tabua cimport Periodicidade
from libcpp.vector cimport vector

cdef class PyPeriodicidade:
    cdef Periodicidade c_periodicidade
    def __cinit__(self, int val):
        self.c_periodicidade = <Periodicidade> val

cdef class PyTabua:
    cdef Tabua c_tabua

    def __init__(self, qx, percentual, PyPeriodicidade periodicidade):
        self.c_tabua = Tabua(qx, percentual, periodicidade.c_periodicidade)

    def qx(self, int x, vector[int] t):
        return self.c_tabua.qx(x, t)

    def tpx(self,  int x, vector[int] t):
        return self.c_tabua.tpx(x, t)

    def t_qx(self, int x, vector[int] t):
        return self.c_tabua.t_qx(x, t)

    def tempo_futuro_maximo(self, x):
        return self.c_tabua.tempo_futuro_maximo(x)

    def possui_fechamento_plato(self):
        return self.c_tabua.possui_fechamento_plato()

    # def pegar_periodicidade(self):
    #     return self.c_tabua.pegar_periodicidade()

    def pegar_percentual(self):
        return self.c_tabua.pegar_percentual()

    def pegar_fracionamento(self):
        return self.c_tabua.pegar_fracionamento()
