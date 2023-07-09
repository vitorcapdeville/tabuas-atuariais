#include "TabuaCpp.h"
#include "TabuaBaseCpp.h"

TabuaCpp::TabuaCpp() {
}

TabuaCpp::TabuaCpp(std::vector<double> qx)
{
    m_tabuas = { TabuaBaseCpp(qx) };
}

TabuaCpp::TabuaCpp(TabuaBaseCpp tabua)
{
    m_tabuas = { tabua };
}

double TabuaCpp::qx(int x, double t) const {
    return m_tabuas[0].qx(x, t);
}

double TabuaCpp::tpx(int x, double t) const {
    return m_tabuas[0].tpx(x, t);
}

std::vector<double> TabuaCpp::qx(int x, std::vector<double> t) const {
    return m_tabuas[0].qx(x, t);
}

std::vector<double> TabuaCpp::tpx(int x, std::vector<double> t) const {
    return m_tabuas[0].tpx(x, t);
}

double TabuaCpp::tempo_futuro_maximo(int x) const {
    return m_tabuas[0].tempo_futuro_maximo(x);
}

bool TabuaCpp::possui_fechamento_plato() const {
    return isinf(tempo_futuro_maximo(0));
}

double TabuaCpp::t_qx(int x, double t) const {
    return qx(x, t) * tpx(x, (int)t);
}
std::vector<double> TabuaCpp::t_qx(int x, std::vector<double> t) const {
    std::vector<double> ret(t.size());
    int n = (int)t.size();
    for (int i = 0; i < n; i++)
    {
        ret[i] = t_qx(x, t[i]);
    }
    return ret;
}

int TabuaCpp::pega_numero_vidas() const {
    return m_numero_vidas;
}

int TabuaCpp::pega_numero_decrementos() const {
    return m_numero_decrementos;
}

std::vector<TabuaBaseCpp> TabuaCpp::pega_tabuas() const {
    return m_tabuas;
}