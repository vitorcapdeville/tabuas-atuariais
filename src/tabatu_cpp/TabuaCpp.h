#pragma once
#include <vector>
#include "TabuaBaseCpp.h"

class TabuaCpp final
{
private:
    std::vector<TabuaBaseCpp> m_tabuas;
    int m_numero_vidas = 1;
    int m_numero_decrementos = 1;

public:
    TabuaCpp();
    TabuaCpp(std::vector<double> qx);
    TabuaCpp(TabuaBaseCpp tabua);
    double qx(int x, double t) const;
    double tpx(int x, double t) const;
    double t_qx(int x, double t) const;
    std::vector<double> qx(int x, std::vector<double> t) const;
    std::vector<double> tpx(int x, std::vector<double> t) const;
    std::vector<double> t_qx(int x, std::vector<double> t) const;
    double tempo_futuro_maximo(int x) const;
    bool possui_fechamento_plato() const;
    int pega_numero_vidas() const;
    int pega_numero_decrementos() const;
    std::vector<TabuaBaseCpp> pega_tabuas() const;
};