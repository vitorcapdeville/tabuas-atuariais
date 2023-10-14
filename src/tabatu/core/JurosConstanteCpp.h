#pragma once
#include "JurosInterfaceCpp.h"


class JurosConstanteCpp final : public JurosInterfaceCpp
{
private:
    double mapear_t(double t) const override;
    double m_taxa_juros;

public:
    JurosConstanteCpp();
    JurosConstanteCpp(double taxa_juros);
    double taxa_juros(double t) const override;
    std::vector<double> taxa_juros(std::vector<double> t) const;
    double taxa_desconto(double t) const;
    std::vector<double> taxa_desconto(std::vector<double> t) const;
};
