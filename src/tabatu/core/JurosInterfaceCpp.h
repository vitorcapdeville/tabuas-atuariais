#pragma once
#include <vector>

class JurosInterfaceCpp
{
private:
    virtual double mapear_t(double t) const = 0;

public:
    JurosInterfaceCpp();
    virtual double taxa_juros(double t) const = 0;
    std::vector<double> taxa_juros(std::vector<double> t) const;
    double taxa_desconto(double t) const;
    std::vector<double> taxa_desconto(std::vector<double> t) const;

};