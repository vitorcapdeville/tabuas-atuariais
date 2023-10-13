#include "alterar_tabua.h"
#include <cmath>
#include <stdexcept>

double reduzir_periodicidade(double qx, int razao_nova_atual) {
    return 1.0 - std::pow(1.0 - qx, 1.0 / razao_nova_atual);
}

std::vector<double> reduzir_periodicidade(std::vector<double> qx, int razao_nova_atual) {
    std::vector<double> qx_reduzido(qx.size() * razao_nova_atual);
    for (int i = 0; i < qx.size() * razao_nova_atual; i++) {
        if (i % razao_nova_atual == 0) {
            qx_reduzido[i] = reduzir_periodicidade(qx[(int) i / razao_nova_atual], razao_nova_atual);
        }
        else {
            qx_reduzido[i] = qx_reduzido[i - 1];
        }
    }
    return qx_reduzido;
}

double aumentar_periodicidade(double qx, int razao_atual_nova) {
    return 1 - std::pow(1 - qx, razao_atual_nova);
}

std::vector<double> aumentar_periodicidade(std::vector<double> qx, int razao_atual_nova) {
    int tamanho = std::ceil((double) qx.size() / razao_atual_nova);
    int indice_atual;
    std::vector<double> qx_aumentado(tamanho);
    for (int i = 0; i < tamanho; i++) {
        indice_atual = std::min(i * razao_atual_nova, (int)qx.size() - 1);
        for (int j = 1; j < razao_atual_nova; j++) {
            if (indice_atual == (int)qx.size() - 1) break;
            if (qx[indice_atual + j] != qx[indice_atual]) {
                throw std::invalid_argument("Alterar a periodicidade de uma tábua que não possui taxas constantes em cada subintervalo resultaria em perda de informação");
            }
        }
        qx_aumentado[i] = aumentar_periodicidade(qx[indice_atual], razao_atual_nova);
    }
    return qx_aumentado;
}

std::vector<double> alterar_periodicidade_qx_cpp(std::vector<double> qx, int periodicidade, int nova_periodicidade) {
    if (periodicidade < nova_periodicidade) {
        return reduzir_periodicidade(qx, (int) nova_periodicidade / periodicidade);
    }
    else if (periodicidade > nova_periodicidade)
    {
        return aumentar_periodicidade(qx, (int) periodicidade / nova_periodicidade);
    }
    return qx;

}

std::vector<double> agravar_qx_cpp(std::vector<double> qx, double percentual) {
    if (percentual < 0.0) {
        throw std::invalid_argument("O percentual de agravo deve ser positivo.");
    }
    if (percentual == 0.0) {
        return qx;
    }
    std::vector<double> qx_agravado(qx.size(), 1.0);
    for (int i = 0; i < qx.size(); i++) {
        if (qx[i] < 1) {
            qx_agravado[i] = std::min(qx[i] * (percentual / 100), 1.0);
        }
    }
    return qx_agravado;
};
