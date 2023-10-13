from libcpp.vector cimport vector
from JurosInterfaceCpp cimport JurosInterfaceCpp

cdef extern from "JurosConstanteCpp.cpp":
    pass

cdef extern from "JurosConstanteCpp.h":
    cdef cppclass JurosConstanteCpp(JurosInterfaceCpp):
        JurosConstanteCpp() except +
        JurosConstanteCpp(double juros)
