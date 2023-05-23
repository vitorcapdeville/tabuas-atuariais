#include "Tabua.h"
#include <math.h>
#include <limits>

Tabua::Tabua() {
}

Tabua::Tabua(std::vector<double> qx, double percentual, Periodicidade periodicidade) :
    m_qx_anual(qx),
    m_percentual(percentual),
    m_periodicidade(periodicidade)
{
    m_fracionamento = static_cast<int>(m_periodicidade);
    m_qx_anual_size = (int)m_qx_anual.size();
    m_qx_size = m_qx_anual_size * m_fracionamento;
    m_qx = m_qx_anual;
    m_lx = std::vector<double>(m_qx_size + 1);

    preparar_qx();
    explodir_qx();

    calcular_lx(10000.0);
}

void Tabua::calcular_lx(double raiz) {
    m_lx[0] = raiz;
    for (int i = 1; i < m_qx_size + 1; i++)
    {
        m_lx[i] = m_lx[i - 1] * (1 - m_qx[i - 1]);
        if (m_lx[i] == 0) {
            m_w = i - 1;
        }
    }
}

void Tabua::agravar_qx(double& qx) {
    qx = std::min(qx * m_percentual / 100.0, 1.0);
}

void Tabua::fracionar_qx(double& qx) {
    qx = 1 - pow(1 - qx, 1.0 / m_fracionamento);
}

void Tabua::preparar_qx() {
    for (int i = 0; i < m_qx_anual_size; i++)
    {
        agravar_qx(m_qx[i]);
        fracionar_qx(m_qx[i]);
    }
}

void Tabua::explodir_qx() {
    std::vector<double> qx_explodido(m_qx_size);
    for (int i = 0; i < m_qx_anual_size; i++)
    {
        for (int j = 0; j < m_fracionamento; j++)
        {
            qx_explodido[i * m_fracionamento + j] = m_qx_anual[i];
        }
    }
    m_qx = qx_explodido;
}

int Tabua::tempo_futuro_maximo(int x) const {
    return std::max(m_w - x + 1, 0);
}

bool Tabua::possui_fechamento_plato() const {
    return m_w == std::numeric_limits<int>::max() - 1;
}

double Tabua::lx(int x) const {
    int limite_superior_x = std::min(tempo_futuro_maximo(0), (int)(m_qx_size));
    int x_trunc = std::min(x, limite_superior_x);
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

std::vector<double> Tabua::qx(int x, std::vector<int> t) const {
    std::vector<double> ret(t.size());
    int n = (int)t.size();
    for (int i = 0; i < n; i++)
    {
        ret[i] = qx(x, t[i]);
    }
    return ret;
}

double Tabua::qx(int x, int t) const {
    int limite_superior_x = std::min(tempo_futuro_maximo(0), (int)(m_qx_size - 1));
    x = std::min(x, limite_superior_x);
    int limite_superior_t = std::min(tempo_futuro_maximo(x), (int)(m_qx_size - x - 1));
    t = std::min(t, limite_superior_t);
    return m_qx[x + t];
}

double Tabua::tpx(int x, int t) const {
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

std::vector<double> Tabua::tpx(int x, std::vector<int> t) const {
    std::vector<double> ret(t.size());
    int n = (int)t.size();
    for (int i = 0; i < n; i++)
    {
        ret[i] = tpx(x, t[i]);
    }
    return ret;
}

double Tabua::t_qx(int x, int t) const {
    return qx(x, t) * tpx(x, t);
}

std::vector<double> Tabua::t_qx(int x, std::vector<int> t) const {
    std::vector<double> ret(t.size());
    int n = (int)t.size();
    for (int i = 0; i < n; i++)
    {
        ret[i] = t_qx(x, t[i]);
    }
    return ret;
}

double Tabua::pegar_percentual() const {
    return m_percentual;
}

Periodicidade Tabua::pegar_periodicidade() const {
    return m_periodicidade;
}

int Tabua::pegar_fracionamento() const {
    return m_fracionamento;
}
