# tabuas-atuariais
Definição de tábuas atuariais em python com códigos em C++ para melhor performance.

## TODO

- Trazer os testes.
- Achar uma forma de usar o nome Tabua e Periodicidade sem o Py na frente.
- Incluir tabuas de múltiplos decrementos e múltiplas vidas.
- Quando eu uso a função diretamente em c++ (PyTabua) fica muito mais rápido do que quando eu uso o wrapper (Tabua). Verificar o motivo.
parece que os ifs estão atrasando, e a conversão de lista para array parece pesar tb. Seria legal se tivesse como eu retornar o vector[double]
como array[float] ao inves de retornar pro python como list[float] e então converter em array do numpy.
- Talvez eu precise de fato colocar absolutamente tudo em c++.
- Coloquei os inputs e outputs que podem ser infinitos como double, mas ficou um pouco mais lento. Pensar numa melhor forma.
- parece que transformar em array no output não pesou tanto no tempoo.


Compilar Cython

python setup.py build_ext --inplace

Intalar pacote (Também compila o cython)

pip install -e . 