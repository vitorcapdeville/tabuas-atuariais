from libcpp.vector cimport vector
from libcpp cimport bool

cdef extern from "Tabua.cpp":
    pass

cdef extern from "Tabua.h":
    cdef cppclass Tabua:
        Tabua() except +
        Tabua(vector[double] qx)
        double qx(int x, double t) const
        double tpx(int x, double t) const
        double t_qx(int x, double t) const
        vector[double] qx(int x, vector[double] t) const
        vector[double] tpx(int x, vector[double] t) const
        vector[double] t_qx(int x, vector[double] t) const
        double tempo_futuro_maximo(int x) const
        bool possui_fechamento_plato() const