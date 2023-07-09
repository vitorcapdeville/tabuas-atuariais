from libcpp.vector cimport vector
from libcpp cimport bool
from TabuaBaseCpp cimport TabuaBaseCpp

cdef extern from "TabuaCpp.cpp":
    pass

cdef extern from "TabuaCpp.h":
    cdef cppclass TabuaCpp:
        TabuaCpp() except +
        TabuaCpp(vector[double] qx)
        double qx(int x, double t) const
        double tpx(int x, double t) const
        double t_qx(int x, double t) const
        vector[double] qx(int x, vector[double] t) except +
        vector[double] tpx(int x, vector[double] t) except +
        vector[double] t_qx(int x, vector[double] t) except +
        double tempo_futuro_maximo(int x) except +
        bool possui_fechamento_plato() const
        int pega_numero_vidas() const
        int pega_numero_decrementos() const
        vector[TabuaBaseCpp] pega_tabuas() const
