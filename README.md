# tabuas-atuariais
Definição de tábuas atuariais em python com códigos em C++ para melhor performance.

## TODO


- verificar se eu continuo fazendo a parte de capturar argumentos no pyton msm ou se faço no c++.

- Verificar efeito de adicionar atleast 1d nos argumentos, no cython.
- Verificar se eu consigo deixar o cython decidir qual método chamar ao inves de fazer atleast 1d
- Verificar impacto das duas alterações.
- Incluir testes p garantir que os argumentos são flexiveis, isto é, eu posso chamar com int, vetor, array etc.

- Verificar se faz sentido matar o módulo de python e deixar tudo em c++ cython
- Incluir documentacao.

- Verificar se da p usar herança de alguma forma no cython.


Compilar Cython

python setup.py build_ext --inplace

Intalar pacote (Também compila o cython)

pip install -e . 