#pragma once
#include <vector>
#include <limits>
#include "Periodicidade.h"


class Tabua final
{
private:
    std::vector<double> m_qx_anual;
    std::vector<double> m_qx;
    std::vector<double> m_lx;
    int m_w = std::numeric_limits<int>::max() - 1;
    int m_qx_anual_size;
    int m_qx_size;
    Periodicidade m_periodicidade;
    int m_fracionamento;
    double m_percentual;

public:
    Tabua();
    Tabua(std::vector<double> qx, double percentual, Periodicidade periodicidade);
    double qx(int x, int t) const;
    double tpx(int x, int t) const;
    double t_qx(int x, int t) const;
    std::vector<double> qx(int x, std::vector<int> t) const;
    std::vector<double> tpx(int x, std::vector<int> t) const;
    std::vector<double> t_qx(int x, std::vector<int> t) const;
    int tempo_futuro_maximo(int x) const;
    bool possui_fechamento_plato() const;
    Periodicidade pegar_periodicidade() const;
    double pegar_percentual() const;
    int pegar_fracionamento() const;

private:
    double lx(int x) const;
    void calcular_lx(double raiz);
    void agravar_qx(double& qx);
    void fracionar_qx(double& qx);
    void preparar_qx();
    void explodir_qx();
};