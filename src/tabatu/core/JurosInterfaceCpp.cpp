#include "JurosInterfaceCpp.h"
#include <cmath>

JurosInterfaceCpp::JurosInterfaceCpp() {
}

double JurosInterfaceCpp::taxa_desconto(double t) const {
    return std::pow(1.0 + taxa_juros(t), -mapear_t(t));
}

std::vector<double> JurosInterfaceCpp::taxa_desconto(std::vector<double> t) const {
    std::vector<double> taxa(t.size());
    for (int i = 0; i < t.size(); i++) {
        taxa[i] = taxa_desconto(t[i]);
    }
    return taxa;
}

std::vector<double> JurosInterfaceCpp::taxa_juros(std::vector<double> t) const {
    std::vector<double> taxa(t.size());
    for (int i = 0; i < t.size(); i++) {
        taxa[i] = taxa_juros(t[i]);
    }
    return taxa;
}