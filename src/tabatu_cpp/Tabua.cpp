#include "Tabua.h"
#include <math.h>
#include <limits>

Tabua::Tabua() {
}

Tabua::Tabua(std::vector<double> qx) :
    m_qx(qx)
{
    m_qx_size = (int)m_qx.size();
    m_lx = std::vector<double>(m_qx_size + 1);

    calcular_lx(10000.0);
}

void Tabua::calcular_lx(double raiz) {
    m_lx[0] = raiz;
    for (int i = 1; i < m_qx_size + 1; i++)
    {
        m_lx[i] = m_lx[i - 1] * (1 - m_qx[i - 1]);
        if (m_lx[i] == 0) {
            m_w = (double)(i - 1);
            break;
        }
    }
}

double Tabua::tempo_futuro_maximo(int x) const {
    return std::max(m_w - x + 1.0, 0.0);
}

bool Tabua::possui_fechamento_plato() const {
    return isinf(m_w);
}

double Tabua::lx(double x) const {
    double limite_superior_x = std::min(tempo_futuro_maximo(0), (double)(m_qx_size));
    int x_trunc = (int)std::min(x, limite_superior_x);
    double lx_ret = m_lx[x_trunc];
    if (possui_fechamento_plato() && (x > x_trunc)) {
        int extras = x - x_trunc;
        double qx_last = m_qx.back();
        for (int i = 0; i < extras; i++)
        {
            lx_ret = lx_ret * (1 - qx_last);
        }
    }
    return lx_ret;
}

std::vector<double> Tabua::qx(int x, std::vector<double> t) const {
    std::vector<double> ret(t.size());
    int n = (int)t.size();
    for (int i = 0; i < n; i++)
    {
        ret[i] = qx(x, t[i]);
    }
    return ret;
}

double Tabua::qx(int x, double t) const {
    int limite_superior_x = std::min(tempo_futuro_maximo(0), (double)(m_qx_size - 1));
    x = std::min(x, limite_superior_x);
    double limite_superior_t = std::min(tempo_futuro_maximo(x), (double)(m_qx_size - x - 1));
    t = std::min(t, limite_superior_t);
    return m_qx[x + (int)t];
}

double Tabua::tpx(int x, double t) const {
    if (t == 0) {
        return 1;
    }
    double _lx = lx(x);
    double _lxt = lx(x + t);
    if (_lx == 0) {
        return 0;
    }
    return _lxt / _lx;
}

std::vector<double> Tabua::tpx(int x, std::vector<double> t) const {
    std::vector<double> ret(t.size());
    int n = (int)t.size();
    for (int i = 0; i < n; i++)
    {
        ret[i] = tpx(x, t[i]);
    }
    return ret;
}

double Tabua::t_qx(int x, double t) const {
    return qx(x, t) * tpx(x, (int)t);
}

std::vector<double> Tabua::t_qx(int x, std::vector<double> t) const {
    std::vector<double> ret(t.size());
    int n = (int)t.size();
    for (int i = 0; i < n; i++)
    {
        ret[i] = t_qx(x, t[i]);
    }
    return ret;
}

