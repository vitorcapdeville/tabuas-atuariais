#include "TabuaCpp.h"
#include "TabuaBaseCpp.h"
#include <stdexcept>

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

double TabuaCpp::qx(std::vector<int> x, double t) const {
    return m_tabuas[0].qx(x[0], t);
}

double TabuaCpp::tpx(std::vector<int> x, double t) const {
    return m_tabuas[0].tpx(x[0], t);
}

std::vector<double> TabuaCpp::qx(std::vector<int> x, std::vector<double> t) const {
    if (x.size() > 1) {
        throw std::invalid_argument("x deve ter tamanho 1");
    }
    return m_tabuas[0].qx(x[0], t);
}

std::vector<double> TabuaCpp::tpx(std::vector<int> x, std::vector<double> t) const {
    if (x.size() > 1) {
        throw std::invalid_argument("x deve ter tamanho 1");
    }
    return m_tabuas[0].tpx(x[0], t);
}

double TabuaCpp::tempo_futuro_maximo(std::vector<int> x) const {
    if (x.size() > 1) {
        throw std::invalid_argument("x deve ter tamanho 1");
    }
    return m_tabuas[0].tempo_futuro_maximo(x[0]);
}

bool TabuaCpp::possui_fechamento_plato() const {
    return isinf(tempo_futuro_maximo({ 0 }));
}

double TabuaCpp::t_qx(std::vector<int> x, double t) const {
    return qx(x, t) * tpx(x, (int)t);
}
std::vector<double> TabuaCpp::t_qx(std::vector<int> x, std::vector<double> t) const {
    if (x.size() > 1) {
        throw std::invalid_argument("x deve ter tamanho 1");
    }
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