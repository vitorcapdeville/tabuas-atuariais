from libcpp.vector cimport vector


cdef extern from "JurosInterfaceCpp.cpp":
    pass

cdef extern from "JurosInterfaceCpp.h":
    cdef cppclass JurosInterfaceCpp:
        JurosInterfaceCpp() except +
        vector[double] taxa_juros(vector[double] t) const
        vector[double] taxa_desconto(vector[double] t) const
