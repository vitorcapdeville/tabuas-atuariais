from libcpp.vector cimport vector
from libcpp cimport bool
from TabuaBaseCpp cimport TabuaBaseCpp
from TabuaCpp cimport TabuaCpp

cdef extern from "TabuaMultiplasVidasCpp.cpp":
    pass

cdef extern from "TabuaMultiplasVidasCpp.h":
    cdef cppclass TabuaMultiplasVidasCpp:
        TabuaMultiplasVidasCpp() except +
        TabuaMultiplasVidasCpp(vector[TabuaCpp] tabuas, StatusVidasConjuntasCpp status_vidas_conjuntas)
        vector[double] qx(vector[int] x, vector[double] t) except +
        vector[double] tpx(vector[int] x, vector[double] t) except +
        vector[double] t_qx(vector[int] x, vector[double] t) except +
        double tempo_futuro_maximo(vector[int] x) except +
        bool possui_fechamento_plato() const
        int pega_numero_vidas() const
        int pega_numero_decrementos() const
        vector[TabuaBaseCpp] pega_tabuas() const

    cdef cppclass StatusVidasConjuntasCpp:
        pass



