# include "TabuaInterfaceCpp.h"
# include <stdexcept>
# include <cmath>

TabuaInterfaceCpp::TabuaInterfaceCpp()
{

}

TabuaInterfaceCpp::TabuaInterfaceCpp(int numero_decrementos, int numero_vidas, std::vector<TabuaBaseCpp> tabuas) :
    m_numero_decrementos(numero_decrementos), m_numero_vidas(numero_vidas), m_tabuas(tabuas)
{

}

bool TabuaInterfaceCpp::possui_fechamento_plato() const {
    std::vector<int> x(m_numero_vidas * m_numero_decrementos, 0);
    return std::isinf(tempo_futuro_maximo(x));
}


double TabuaInterfaceCpp::t_qx(std::vector<int> x, double t) const {
    return qx(x, t) * tpx(x, (int)t);
}


int TabuaInterfaceCpp::pega_numero_vidas() const {
    return m_numero_vidas;
}

int TabuaInterfaceCpp::pega_numero_decrementos() const {
    return m_numero_decrementos;
}

std::vector<TabuaBaseCpp> TabuaInterfaceCpp::pega_tabuas() const {
    return m_tabuas;
}