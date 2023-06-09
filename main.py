from timeit import timeit

import matatu.tabuas as matatu
import matatu.tabuas.multiplas_vidas as mvd
import matatu.periodicidade as per_matatu
from matatu.banco_tabuas import pega_qx
from tabatu.periodicidade import Periodicidade
from numpy import arange, array

import tabatu
import tabatu_cpp

#qx
brems_mt_f_2015 = array(pega_qx("BR-EMSmt-v.2015-f").Taxa)

#1 decremento
tabua_cpp = tabatu.Tabua(brems_mt_f_2015, Periodicidade.ANUAL)
# tabua_cpp = tabatu_cpp.Tabua(brems_mt_f_2015)
tabua_py = matatu.Tabua(brems_mt_f_2015, per_matatu.Periodicidade.ANUAL)

# 3 decrementos
tabua_cpp_mdt = tabatu.TabuaMDT(tabua_cpp, tabua_cpp, tabua_cpp)
# tabua_cpp_mdt = tabatu_cpp.TabuaMDT(tabua_cpp, tabua_cpp, tabua_cpp)
tabua_py_mdt = matatu.TabuaMDT(tabua_py, tabua_py, tabua_py)

# 3 vidas
tabua_cpp_mvd = tabatu.TabuaMultiplasVidas(tabua_cpp, tabua_cpp, tabua_cpp, status = tabatu.StatusVidasConjuntas.JOINT)
# tabua_cpp_mvd = tabatu_cpp.TabuaMultiplasVidas(tabua_cpp, tabua_cpp, tabua_cpp, status = tabatu_cpp.StatusVidasConjuntas(1))
tabua_py_mvd = matatu.TabuaMultiplasVidas(tabua_py, tabua_py, tabua_py, status=mvd.StatusVidasConjuntas.JOINT)

# print(tabatu_cpp.StatusVidasConjuntas("LAST").get_status())
print(tabua_cpp.tabuas)
print(tabua_cpp_mdt.tabuas)
print(tabua_cpp_mvd.tabuas)

print("\n")
print("Tabuas com um único decremento")
print("\n")
tempo_cpp = timeit(lambda: tabua_cpp.tpx([30], arange(50)), number=1000)
tempo_python = timeit(lambda: tabua_py.tpx([30], arange(50)), number=1000)

print(f"tabua tpx c++: {tempo_cpp} - {sum(tabua_cpp.tpx([30], arange(50)))}")
print(f"tabua tpx python: {tempo_python} - {sum(tabua_py.tpx([30], arange(50)))}")
print(f"Razao c++/python: {(tempo_python - tempo_cpp)/tempo_python}")

tempo_cpp = timeit(lambda: tabua_cpp.t_qx([30], arange(50)), number=1000)
tempo_python = timeit(lambda: tabua_py.t_qx([30], arange(50)), number=1000)
print(f"tabua t_qx c++: {tempo_cpp} - {sum(tabua_cpp.t_qx([30], arange(50)))}")
print(f"tabua t_qx python: {tempo_python} - {sum(tabua_py.t_qx([30], arange(50)))}")
print(f"Razao c++/python: {(tempo_python - tempo_cpp)/tempo_python}")

print("\n")
print("Tabuas com 3 decrementos")
print("\n")

tempo_cpp = timeit(lambda: tabua_cpp_mdt.tpx([30, 30, 30], arange(50)), number=1000)
tempo_python = timeit(lambda: tabua_py_mdt.tpx(30, arange(50)), number=1000)

print(f"tabua tpx c++: {tempo_cpp} - {sum(tabua_cpp_mdt.tpx([30, 30, 30], arange(50)))}")
print(f"tabua tpx python: {tempo_python} - {sum(tabua_py_mdt.tpx(30, arange(50)))}")
print(f"Razao c++/python: {(tempo_python - tempo_cpp)/tempo_python}")

tempo_cpp = timeit(lambda: tabua_cpp_mdt.t_qx([30, 30, 30], arange(50)), number=1000)
tempo_python = timeit(lambda: tabua_py_mdt.t_qx(30, arange(50)), number=1000)
print(f"tabua t_qx c++: {tempo_cpp} - {sum(tabua_cpp_mdt.t_qx([30, 30, 30], arange(50)))}")
print(f"tabua t_qx python: {tempo_python} - {sum(tabua_py_mdt.t_qx(30, arange(50)))}")
print(f"Razao c++/python: {(tempo_python - tempo_cpp)/tempo_python}")


print("\n")
print("Tabuas com multiplas vidas")
print("\n")
tempo_cpp = timeit(lambda: tabua_cpp_mvd.tpx([30, 30, 30], arange(50)), number=1000)
tempo_python = timeit(lambda: tabua_py_mvd.tpx([30, 30, 30], arange(50)), number=1000)

print(f"tabua tpx c++: {tempo_cpp} - {sum(tabua_cpp_mvd.tpx([30, 30, 30], arange(50)))}")
print(f"tabua tpx python: {tempo_python} - {sum(tabua_py_mvd.tpx([30, 30, 30], arange(50)))}")
print(f"Razao c++/python: {(tempo_python - tempo_cpp)/tempo_python}")

tempo_cpp = timeit(lambda: tabua_cpp_mvd.qx([30, 30, 30], arange(50)), number=1000)
tempo_python = timeit(lambda: tabua_py_mvd.qx([30, 30, 30], arange(50)), number=1000)

print(f"tabua qx c++: {tempo_cpp} - {sum(tabua_cpp_mvd.qx([30, 30, 30], arange(50)))}")
print(f"tabua qx python: {tempo_python} - {sum(tabua_py_mvd.qx([30, 30, 30], arange(50)))}")
print(f"Razao c++/python: {(tempo_python - tempo_cpp)/tempo_python}")
