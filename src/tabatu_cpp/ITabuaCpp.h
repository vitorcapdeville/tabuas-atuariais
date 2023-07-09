#pragma once
#include <vector>
#include "TabuaBaseCpp.h"

class ITabuaCpp
{
private:
    std::vector<TabuaBaseCpp> m_tabuas;
    int m_numero_vidas = 1;
    int m_numero_decrementos = 1;

public:
    virtual double qx(int x, double t) const = 0;
    virtual double tpx(int x, double t) const = 0;
    double t_qx(int x, double t) const;
    virtual std::vector<double> qx(int x, std::vector<double> t) const = 0;
    virtual std::vector<double> tpx(int x, std::vector<double> t) const = 0;
    std::vector<double> t_qx(int x, std::vector<double> t) const;
    virtual double tempo_futuro_maximo(int x) const = 0;
    bool possui_fechamento_plato() const;
    int pega_numero_vidas() const;
    int pega_numero_decrementos() const;
    std::vector<TabuaBaseCpp> pega_tabuas() const;
};