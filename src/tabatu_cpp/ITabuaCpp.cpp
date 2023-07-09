#include "ITabuaCpp.h"

bool ITabuaCpp::possui_fechamento_plato() const {
    return isinf(tempo_futuro_maximo(0));
}

double ITabuaCpp::t_qx(int x, double t) const {
    return qx(x, t) * tpx(x, (int)t);
}
std::vector<double> ITabuaCpp::t_qx(int x, std::vector<double> t) const {
    std::vector<double> ret(t.size());
    int n = (int)t.size();
    for (int i = 0; i < n; i++)
    {
        ret[i] = t_qx(x, t[i]);
    }
    return ret;
}

int ITabuaCpp::pega_numero_vidas() const {
    return m_numero_vidas;
}

int ITabuaCpp::pega_numero_decrementos() const {
    return m_numero_decrementos;
}

std::vector<TabuaBaseCpp> ITabuaCpp::pega_tabuas() const {
    return m_tabuas;
}