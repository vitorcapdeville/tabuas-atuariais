#include "alterar_tabua.h"
#include <vector>
#include <iostream>

int main() {

    std::vector<double> qx = { 0.0, 0.2, 0.3, 0.4, 0.5, 1.0 };
    std::vector<double> qx_alterado = alterar_periodicidade_cpp(qx, 1, 1);
    for (auto i : qx_alterado)
        std::cout << i << std::endl;
    // std::cout << alterar_periodicidade_cpp(qx, 1, 1) << std::endl;
    
    return 0;
}
