from libcpp.vector cimport vector

cdef extern from "alterar_tabua.cpp":
    pass

cdef extern from "alterar_tabua.h":
    vector[double] alterar_periodicidade_qx_cpp(vector[double] qx, int periodicidade, int nova_periodicidade) except +
    vector[double] agravar_qx_cpp(vector[double] qx, double percentual) except +
