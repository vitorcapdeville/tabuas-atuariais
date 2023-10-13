#include "JurosConstanteCpp.h"

JurosConstanteCpp::JurosConstanteCpp() {
}

JurosConstanteCpp::JurosConstanteCpp(double juros) : m_taxa_juros(juros) {
}

double JurosConstanteCpp::taxa_juros(double t) const {
    return m_taxa_juros;
}

double JurosConstanteCpp::mapear_t(double t) const {
    return t;
}

std::vector<double> JurosConstanteCpp::taxa_juros(std::vector<double> t) const {
    return JurosInterfaceCpp::taxa_juros(t);
}

double JurosConstanteCpp::taxa_desconto(double t) const {
    return JurosInterfaceCpp::taxa_desconto(t);
}

std::vector<double> JurosConstanteCpp::taxa_desconto(std::vector<double> t) const {
    return JurosInterfaceCpp::taxa_desconto(t);
}