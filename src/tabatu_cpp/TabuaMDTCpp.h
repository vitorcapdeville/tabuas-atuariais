#pragma once
#include <vector>
#include "TabuaBaseCpp.h"
#include "TabuaCpp.h"

class TabuaMDTCpp final
{
private:
    std::vector<TabuaBaseCpp> m_tabuas;
    int m_numero_vidas = 1;
    int m_numero_decrementos = 1;

public:
    TabuaMDTCpp();
    TabuaMDTCpp(std::vector<TabuaCpp> tabuas);
    double qx_j(int x, double t, int j) const;
    double qx(int x, double t) const;
    double tpx(int x, double t) const;
    double t_qx(int x, double t) const;
    std::vector<double> qx_j(int x, std::vector<double> t, int j) const;
    std::vector<std::vector<double>> qx_j(int x, std::vector<double> t, std::vector<int> j) const;
    std::vector<double> qx(int x, std::vector<double> t) const;
    std::vector<double> tpx(int x, std::vector<double> t) const;
    std::vector<double> t_qx(int x, std::vector<double> t) const;
    double tempo_futuro_maximo(int x) const;
    bool possui_fechamento_plato() const;
    int pega_numero_vidas() const;
    int pega_numero_decrementos() const;
    std::vector<TabuaBaseCpp> pega_tabuas() const;
};