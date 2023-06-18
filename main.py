import tabatu
import tabatu_cpp
from numpy import arange, array
import matatu.tabuas as matatu 
from matatu.banco_tabuas import pega_qx
from matatu.periodicidade import Periodicidade
from timeit import timeit


brems_mt_f_2015 = array(pega_qx("BR-EMSmt-v.2015-f").Taxa)
# tabua_cpp = tabatu.Tabua(brems_mt_f_2015, Periodicidade.ANUAL)
tabua_cpp = tabatu_cpp.PyTabua(brems_mt_f_2015)
tabua_py = matatu.Tabua(brems_mt_f_2015, Periodicidade.ANUAL)

tempo_cpp = timeit(lambda: tabua_cpp.tpx(30, arange(50)), number=1000)
tempo_python = timeit(lambda: tabua_py.tpx(30, arange(50)), number=1000)

print(f"tabua tpx c++: {tempo_cpp} - {sum(tabua_cpp.tpx(30, arange(50)))}")
print(f"tabua tpx python: {tempo_python} - {sum(tabua_py.tpx(30, arange(50)))}")
print(f"Razao c++/python: {tempo_cpp/tempo_python}")

tempo_cpp = timeit(lambda: tabua_cpp.t_qx(30, arange(50)), number=1000)
tempo_python = timeit(lambda: tabua_py.t_qx(30, arange(50)), number=1000)
print(f"tabua t_qx c++: {tempo_cpp} - {sum(tabua_cpp.t_qx(30, arange(50)))}")
print(f"tabua t_qx python: {tempo_python} - {sum(tabua_py.t_qx(30, arange(50)))}")
print(f"Razao c++/python: {tempo_cpp/tempo_python}")

