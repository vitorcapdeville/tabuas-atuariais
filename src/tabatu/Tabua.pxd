from libcpp.vector cimport vector
from libcpp cimport bool

cdef extern from "Periodicidade.h":
  cdef cppclass Periodicidade:
    pass

cdef extern from "Periodicidade.h" namespace "Periodicidade":
  cdef Periodicidade Anual
  cdef Periodicidade Semestral
  cdef Periodicidade Quadrimestral
  cdef Periodicidade Trimestral
  cdef Periodicidade Bimestral
  cdef Periodicidade Mensal

cdef extern from "Tabua.cpp":
    pass

cdef extern from "Tabua.h":
    cdef cppclass Tabua:
        Tabua() except +
        Tabua(vector[double] qx, double percentual, Periodicidade periodicidade)
        double qx(int x, int t) const
        double tpx(int x, int t) const
        double t_qx(int x, int t) const
        vector[double] qx(int x, vector[int] t) const
        vector[double] tpx(int x, vector[int] t) const
        vector[double] t_qx(int x, vector[int] t) const
        int tempo_futuro_maximo(int x) const
        bool possui_fechamento_plato() const
        Periodicidade pegar_periodicidade() const
        double pegar_percentual() const
        int pegar_fracionamento() const