from libcpp.vector cimport vector
from libcpp cimport bool
from TabuaBaseCpp cimport TabuaBaseCpp
from TabuaCpp cimport TabuaCpp

cdef extern from "TabuaMDTCpp.cpp":
    pass

cdef extern from "TabuaMDTCpp.h":
    cdef cppclass TabuaMDTCpp:
        TabuaMDTCpp() except +
        TabuaMDTCpp(vector[TabuaCpp] tabuas)
        vector[vector[double]] qx_j(int x, vector[double] t, vector[int] j) except +
        vector[double] qx(int x, vector[double] t) except +
        vector[double] tpx(int x, vector[double] t) except +
        vector[double] t_qx(int x, vector[double] t) except +
        double tempo_futuro_maximo(int x) except +
        bool possui_fechamento_plato() const
        int pega_numero_vidas() const
        int pega_numero_decrementos() const
        vector[TabuaBaseCpp] pega_tabuas() const
