#include "TabuaMDTCpp.h"
#include "TabuaCpp.h"
#include <stdexcept>

double qx2qxj(double qx1, double qx2, double qx3)
{
	return qx1 * (1 - 0.5 * (qx2 + qx3) + 1.0 / 3.0 * (qx2 * qx3));
}

std::vector<double> qx2qxj(std::vector<double> qx1, std::vector<double> qx2, std::vector<double> qx3)
{
	std::vector<double> qxj;
	qxj.reserve(qx1.size());
	for (int i = 0; i < qx1.size(); i++)
	{
		qxj.push_back(qx2qxj(qx1[i], qx2[i], qx3[i]));
	}
	return qxj;
}

std::vector<double> converter_mdt(std::vector<double> qx) {
	std::vector<double> qxj(3);
	int tamanho = 3 - qx.size();
	double zeros = 0.0;
	if (tamanho < 0) {
		throw std::invalid_argument("O número de tábuas não pode ser maior que 3");
	}
	for (int i = 0; i < tamanho; i++) {
		qx.push_back(zeros);
	}
	qxj[0] = qx2qxj(qx[0], qx[1], qx[2]);
	qxj[1] = qx2qxj(qx[1], qx[2], qx[0]);
	qxj[2] = qx2qxj(qx[2], qx[0], qx[1]);
	return qxj;
}

std::vector<std::vector<double>> converter_mdt(std::vector<std::vector<double>> qx) {
	std::vector<std::vector<double>> qxj(3);
	int tamanho = 3 - qx.size();
	std::vector<double> zeros(qx[0].size(), 0.0);
	if (tamanho < 0) {
		throw std::invalid_argument("O número de tábuas não pode ser maior que 3");
	}
	for (int i = 0; i < tamanho; i++) {
		qx.push_back(zeros);
	}
	qxj[0] = qx2qxj(qx[0], qx[1], qx[2]);
	qxj[1] = qx2qxj(qx[1], qx[2], qx[0]);
	qxj[2] = qx2qxj(qx[2], qx[0], qx[1]);
	return qxj;
}

TabuaMDTCpp::TabuaMDTCpp() {
}

TabuaMDTCpp::TabuaMDTCpp(std::vector<TabuaCpp> tabuas)
{
	m_numero_decrementos = tabuas.size();
	m_tabuas.reserve(m_numero_decrementos);
	for (TabuaCpp tabua : tabuas) {
		m_tabuas.push_back(tabua.pega_tabuas()[0]);
	}
	
}

// comeco
double TabuaMDTCpp::qx_j(int x, double t, int j) const {
	if (j > m_numero_decrementos) {
		throw std::out_of_range("");
	}
	std::vector<double> qx;
	qx.reserve(m_tabuas.size());
	for (TabuaBaseCpp tabua : m_tabuas) {
		qx.push_back(tabua.qx(x, t));
	}
	return converter_mdt(qx)[j];
}

std::vector<double> TabuaMDTCpp::qx_j(int x, std::vector<double> t, int j) const {
    std::vector<double> ret(t.size());
    int n = (int)t.size();
    for (int i = 0; i < n; i++)
    {
        ret[i] = qx_j(x, t[i], j);
    }
    return ret;
}

std::vector<std::vector<double>> TabuaMDTCpp::qx_j(int x, std::vector<double> t, std::vector<int> j) const {
    std::vector<std::vector<double>> ret(j.size());
    int n = (int)t.size();
    for (int i = 0; i < n; i++)
    {
        ret[i] = qx_j(x, t, j[i]);
    }
    return ret;
}

double TabuaMDTCpp::qx(int x, double t) const {
	double ret = 0.0;
	for (size_t i = 0; i < m_numero_decrementos; i++)
	{
		ret += qx_j(x, t, i);
	}
	return ret;
}

double TabuaMDTCpp::tpx(int x, double t) const {
	double ret = 1.0;
	for (TabuaBaseCpp tabua : m_tabuas)
	{
		ret = ret * tabua.tpx(x, t);
	}
	return ret;
}

std::vector<double> TabuaMDTCpp::qx(int x, std::vector<double> t) const {
	std::vector<double> ret(t.size());
    int n = (int)t.size();
    for (int i = 0; i < n; i++)
    {
        ret[i] = qx(x, t[i]);
    }
    return ret;
}

std::vector<double> TabuaMDTCpp::tpx(int x, std::vector<double> t) const {
	std::vector<double> ret(t.size());
    int n = (int)t.size();
    for (int i = 0; i < n; i++)
    {
        ret[i] = tpx(x, t[i]);
    }
    return ret;
}

double TabuaMDTCpp::tempo_futuro_maximo(int x) const {
	std::vector<double> ret(m_numero_decrementos);
	for (TabuaBaseCpp tabua : m_tabuas)
	{
		ret.push_back(tabua.tempo_futuro_maximo(x));
	}
	return *std::min_element(ret.begin(), ret.end());
}

// fim

bool TabuaMDTCpp::possui_fechamento_plato() const {
    return isinf(tempo_futuro_maximo(0));
}

double TabuaMDTCpp::t_qx(int x, double t) const {
    return qx(x, t) * tpx(x, (int)t);
}
std::vector<double> TabuaMDTCpp::t_qx(int x, std::vector<double> t) const {
    std::vector<double> ret(t.size());
    int n = (int)t.size();
    for (int i = 0; i < n; i++)
    {
        ret[i] = t_qx(x, t[i]);
    }
    return ret;
}

int TabuaMDTCpp::pega_numero_vidas() const {
    return m_numero_vidas;
}

int TabuaMDTCpp::pega_numero_decrementos() const {
    return m_numero_decrementos;
}

std::vector<TabuaBaseCpp> TabuaMDTCpp::pega_tabuas() const {
    return m_tabuas;
}