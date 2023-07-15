======
Tábuas
======


A classe :class:`~tabatu.Tabua` define a distribuição do tempo de vida futuro, a partir de uma array de taxas.

Essa classe também requer que seja definida uma periodicidade para essas taxas. A periodicidade não faz nada por si só,
mas garante que ao misturar mais de uma tábua, ou ao usar uma tábua com um juros, tudo continua coerente.

>>> from tabatu import Tabua
>>> from tabatu.periodicidade import Periodicidade
>>> import numpy as np
>>> qx1 = np.array([(i + 1) / 100 for i in range(100)])
>>> tabua = Tabua(qx=qx1, periodicidade=Periodicidade.ANUAL)

A partir de uma instância da :class:`~tabatu.Tabua`, é possível cálcular as probabilidades de falha e sobrevivência usuais.
Por exemplo, como a tábua criada é anual, podemos calcular a probabilidade de um indivíduo de 50 anos sobreviver por mais 10 anos.

>>> tabua.tpx([50], [10])
array([0.00029821])

Podemos calcular também a probabilidade de um indivíduo com 50 anos morrer com exatamente 60 anos.

>>> tabua.t_qx([50], [10])
array([0.00018191])

Repare que o output desses métodos sempre é um array do numpy. Além disso, os métodos permitem cálculos vetorizadoos,
isto é, cálculo para diversos argumentos de uma única vez.

>>> tabua.tpx([50], [0, 1, 2, 3, 4, 5])
array([1.        , 0.49      , 0.2352    , 0.110544  , 0.05085024,
       0.02288261])

>>> tabua.t_qx([50], [0, 1, 2, 3, 4, 5])
array([0.51      , 0.2548    , 0.124656  , 0.05969376, 0.02796763,
       0.01281426])

============================================
Comportamento das tábuas após a idade limite
============================================

As tábuas possuem uma característica peculiar com relação ao limite de idade que uma pessoa pode chegar viva.
Em alguns casos, podemos usar uma tábua que termina, digamos, na idade 100 para definir uma população.
E essa população pode conter pessoas com mais de 100 anos. Como são definidas as probabilidades nesse caso?

As Tábuas estão modeladas de forma que dado que a pessoa ta viva e ultrapassou o limite de idade,
essa pessoa irá morrer com probabilidade 1 antes do próximo aniversário.

Para a tábua que criamos anteriormente, podemos obter a idade limite.

>>> tabua.tempo_futuro_maximo([0])
100.0

Se tentamos calcular as probabilidades de sobrevivência para pessoas com mais de 100 anos, obtemos sempre 1 para
o tempo futuro 0, já que a pessoa sempre está viva no tempo 0, e 0 para todos os outros tempos.

>>> tabua.tpx([103], [0, 1, 2, 3])
array([1., 0., 0., 0.])

O mesmo acontece para a probabilidade de falha. A probabilidade de alguém que superou a idade máxima da tábua
falhar antes do próximo aniversário é 1, e a probabilidade sobrevivver por pelo menos mais 1 período e falhar em seguida
é sempre zero.

>>> tabua.t_qx([103], [0, 1, 2, 3])
array([1., 0., 0., 0.])


=====================================
Tábuas fracionadas e tábuas agravadas
=====================================

Em alguns casos recebemos as probabilidades de falha em uma determinada periodicidade (usualmente anual) e precisamos
convertê-las para outra periodicidade (usualmente mensal). Além disso, também é comum utilizar versões agravadas ou
desagravadas de uma tábua que não reflete bem a experiência de uma carteira. Para auxiliar com essas operações,
o pacote tabatu fornece as funções :func:`~tabatu.alterar_periodicidade_qx` e :func:`~tabatu.agravar_qx`.

É importante ressaltar que a ordem que essas operações são realizadas importa, e que o agravo deve **SEMPRE** acontecer
antes da alteração de periodicidade.

Vamos definir algumas várias para explorar as duas operações.

>>> from tabatu import alterar_periodicidade_qx, agravar_qx, Tabua
>>> from tabatu.periodicidade import Periodicidade
>>> import numpy as np
>>> qx_anual = np.array([0.1, 0.2, 0.4, 0.8, 1.0])

Com relação ao agravo e desagravo, os taxas resultantes nunca irão ultrapassar 1 ou serem menores que 0.
Note que quando agravamos o
antes da alteração de periodicidade.

Vamos definir algumas várias para explorar as duas operações.

>>> from tabatu import alterar_periodicidade_qx, agravar_qx, Tabua
>>> from tabatu.periodicidade import Periodicidade
>>> import numpy as np
>>> qx_anual = np.array([0.1, 0.2, 0.4, 0.8, 1.0])

Com relação ao agravo e desagravo, os taxas resultantes nunca irão ultrapassar 1 ou serem menores que 0.
Note que quando agravamos o
antes da alteração de periodicidade.

Vamos definir algumas várias para explorar as duas operações.

>>> from tabatu import alterar_periodicidade_qx, agravar_qx, Tabua
>>> from tabatu.periodicidade import Periodicidade
>>> import numpy as np
>>> qx_anual = np.array([0.1, 0.2, 0.4, 0.8, 1.0])

Com relação ao agravo e desagravo, os taxas resultantes nunca irão ultrapassar 1 ou serem menores que 0.
Note que quando agravamos o ``qx_anual`` em 150%, a taxa que antes era ``0.8`` fica limitada em ``1.0`` ao invés
de ``1.2``.

>>> agravar_qx(qx_anual, 150)
array([0.15, 0.3 , 0.6 , 1.  , 1.  ])

Para a alteração de periodicidade, quando a periodicidade é reduzida (de anual para mensal, por exemplo), as taxas são
explodidas de forma que o novo array de taxas possua uma taxa para cada unidade na nova periodicidade.

>>> qx_mensal = alterar_periodicidade_qx(qx_anual, Periodicidade.ANUAL, Periodicidade.MENSAL)
>>> qx_mensal
array([0.00874161, 0.00874161, 0.00874161, 0.00874161, 0.00874161,
       0.00874161, 0.00874161, 0.00874161, 0.00874161, 0.00874161,
       0.00874161, 0.00874161, 0.01842347, 0.01842347, 0.01842347,
       0.01842347, 0.01842347, 0.01842347, 0.01842347, 0.01842347,
       0.01842347, 0.01842347, 0.01842347, 0.01842347, 0.04167547,
       0.04167547, 0.04167547, 0.04167547, 0.04167547, 0.04167547,
       0.04167547, 0.04167547, 0.04167547, 0.04167547, 0.04167547,
       0.04167547, 0.12551473, 0.12551473, 0.12551473, 0.12551473,
       0.12551473, 0.12551473, 0.12551473, 0.12551473, 0.12551473,
       0.12551473, 0.12551473, 0.12551473, 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ,
       1.        , 1.        , 1.        , 1.        , 1.        ])
>>> len(qx_mensal)
60

Note que o array original possuia 5 elementos, e o array resultante possui 60 elementos. Isso acontece porque existem 60
meses em um ano.

Já quando a periodicidade é aumentada, as taxas são filtradas com o mesmo propósito: obter uma taxa para cada unidade
na nova periodicidade.

>>> alterar_periodicidade_qx(qx_mensal, Periodicidade.MENSAL, Periodicidade.ANUAL)
array([0.1, 0.2, 0.4, 0.8, 1. ])

Após ajustar o array de taxas para o agravamento e a periodicidade desejada, as tábuas podem ser criadas como usual.

>>> tabua_anual = Tabua(qx_anual, Periodicidade.ANUAL)
>>> tabua_mensal = Tabua(qx_mensal, Periodicidade.MENSAL)

Note que a lógica de alteração de periodicidade utilizada preserva as probabilidades nos pontos de quebra.
Por exemplo, a probabilidade de um indivíduo de 2 anos sobreviver por mais 1 anos na tabua anual é equivalente
a probabilidade de um indivíduo de 24 meses (2 anos) sobreviver por mais 12 meses (1 ano) na tábua mensal.

>>> tabua_anual.tpx([2], [1])
array([0.6])

>>> tabua_mensal.tpx([24], [12])
array([0.6])

Da mesma forma, a probabilidade de um indivíduo de 2 anos sobreviver por mais 1 ano e morrer antes de completar 4 anos
de acordo com a tábua anual é equivalente a probabilidade de um indivíduo de 24 meses sobreviver por mais 12 meses e
morrer antes de completar 48 meses de acordo com a tábua mensal.

>>> tabua_anual.t_qx([2], [1])
array([0.48])

>>> tabua_mensal.t_qx([24], np.arange(12,24)).sum()
0.48000000000000026

===============================
Tábuas de múltiplos decrementos
===============================

Em alguns casos existem mais do que uma causa de falha, como por exemplo em seguros de invalidez. Nesses casos, é
preciso construir tábuas de múltiplos decremenots. As tábuas de múltiplos decrementos podem ser construídas modelando
os eventos de forma conjunta, ou a partir de tábuas que são assumidas independentes, que é o mais usual.
O pacote tabatu fornece uma interface para o segundo caso através da :class:`~tabatu.TabuaMDT`.

Esse novo tipo de tábua recebe até 3 :class:`~tabatu.Tabua` como argumentos nomeados ou não nomeados, além de
opcionalmente receber também um argumento indicando qual é a causa principal.

Com a tábua de múltiplos decrementos é possível calcular as mesmas quantidades que a :class:`~tabatu.Tabua`, porém
agora com significado levemente diferente. O método :meth:`~tabatu.TabuaMDT.tpx` retorna a probabilidade de um
indivíduo de idade ``x`` sobreviver por mais ``t`` períodos, sem sofrer nenhum dos decrementos. O método
:meth:`~tabatu.TabuaMDT.t_qx` retorna a probabilidade de um indivíduo de idade ``x`` sobreviver por mais ``t``
períodos, sem sofrer nenhum dos decrementos, e morrer no período ``t`` por qualquer decremento.
O parâmetro ``causa_principal`` afeta o comportamento do método :meth:`~tabatu.TabuaMDT.t_qx`, que passa a retornar
a probabilidade de um indivíduo de idade ``x`` sobreviver por mais ``t`` períodos, sem sofrer nenhum dos decrementos, e
morrer no período ``t`` pela causa principal. Isso é útil quando se tem uma tábua de múltiplos decrementos onde apenas um
deles gera o sinistro.
Além disso, as tábuas de múltiplos decrementos também possuem os métodos :meth:`~tabatu.TabuaMDT.t_qx_j` e
:meth:`~tabatu.TabuaMDT.qx_j`, para obter as probabilidades de falha por decremento.

Podemos construir uma tábua de múltiplos decrementos usando duas tábuas como argumentos posicionais.

>>> from tabatu import Tabua, TabuaMDT
>>> import numpy as np
>>> qx1 = np.array([(i + 1) / 100 for i in range(100)])
>>> qx2 = np.array([0.01 for i in range(100)])
>>> tabua_mdt = TabuaMDT(Tabua(qx1), Tabua(qx2))

Dessa forma, essas tábuas serão mapeadas na posição que foram fornecidas.

>>> tabua_mdt.causas
{'0': 0, '1': 1}

E dessa forma será possível calcular as probabilidades de falha para causas específicas utilizando essa posição.

>>> tabua_mdt.t_qx_j([30, 30], [5], [0])
array([[0.04594007]])

Se as tábuas tivessem sido passadas como argumentos nomeados, poderíamos acessá-las pelo nome ou pela posição.

>>> tabua_mdt_nomeadas = TabuaMDT(morte=Tabua(qx1), invalidez=Tabua(qx2))
>>> tabua_mdt_nomeadas.causas
{'morte': 0, 'invalidez': 1}

>>> tabua_mdt_nomeadas.t_qx_j([30, 30], [5], ['morte'])
array([[0.04594007]])
>>> tabua_mdt_nomeadas.t_qx_j([30, 30], [5], [0])
array([[0.04594007]])

Note que o output de :meth:`~tabatu.TabuaMDT.t_qx_j` é um array de duas dimensões, onde cada linha representa
representa um decremento. Poderíamos então calcular as taxas de falha para cada decremento na mesma expressão.

>>> tabua_mdt_nomeadas.t_qx_j([30, 30], [5], ['morte', 'invalidez'])
array([[0.04594007],
       [0.00105167]])

Também é possível criar tábuas de múltiplos decrementos onde apenas alguns argumentos são nomeados.

>>> tabua_mdt_nomeados_e_posicionais = TabuaMDT(Tabua(qx1), invalidez = Tabua(qx2))
>>> tabua_mdt_nomeados_e_posicionais.causas
{'0': 0, 'invalidez': 1}

A feature da ``causa_principal`` pode ser utilizada se referindo a posição da causa principal ou ao nome.

>>> tabua_mdt_causa_principal_posicao = TabuaMDT(Tabua(qx1), Tabua(qx2), causa_principal=1)
>>> tabua_mdt_causa_principal_nome = TabuaMDT(Tabua(qx1), invalidez=Tabua(qx2), causa_principal='invalidez')

Agora, quando calcularmos :meth:`~tabatu.TabuaMDT.t_qx` obteremos o mesmo valor que
:meth:`~tabatu.TabuaMDT.t_qx_j` para a causa principal.

>>> tabua_mdt_causa_principal_posicao.t_qx([30, 30], [5])
array([0.00105167])

>>> tabua_mdt_causa_principal_posicao.t_qx_j([30, 30], [5], [1])
array([[0.00105167]])

Ainda podemos recuperar a probabilidade de falha por qualquer causa ao calcular o t_qx_j para todas as causas e somar.
>>> tabua_mdt_causa_principal_posicao.t_qx_j([30, 30], [5], [0, 1]).sum()
0.04699174108523214

Um caso comum de uso de tábuas de múltiplos decrementos é para incluir as probabilidades de cancelamento junto com probabilidades
de sinistro. Neste caso, surge uma complicação extra, pois as probabilidades de sinistro geralmente possuem como origem
o nascimento do segurado, enquanto as probabilidades de cancelamento possuem como origem a data de início da vigência.
As tábuas de múltiplos decrementos permitem que sejam passadas duas idades diferentes para os cálculos das probabilidades,
uma para cada causa.

>>> tabua_mdt_com_cancelamento = TabuaMDT(Tabua(qx1), Tabua(qx2))
>>> tabua_mdt_com_cancelamento.t_qx([50, 12], [10])
array([0.00016557])

=========================
Tábuas de múltiplas vidas
=========================

Em alguns casos, existe o interesse de calcular probabilidades de falha de mais de um indivíduo de forma conjunta.
Isso ocorre em rendas com múltiplos beneficiários, por exemplo, onde as rendas são pagas enquanto pelo menos um
beneficiário estiver vivo ou enquanto todos os beneficiários estiverem vivos.
O pacote tabatu fornece uma interface para este tipo de tábua também, através da classe
:class:`~tabatu.TabuaMultiplasVidas`.

Essa tábua funciona de forma parecida com a tábua de múltiplos decrementos, porém não há limitação para a quantidade
de vidas que serão consideradas, e as tábuas são passadas sempre como argumentos posicionais (não-nomeados). Além disso,
é possível escolher o status de vida conjunta que será utilizado - JOINT ou LAST. O status joint indica que a falha ocorre
na primeira falah, enquanto que o status last indica que a falha ocorre na última falha.

>>> from tabatu import Tabua, TabuaMultiplasVidas, StatusVidasConjuntas
>>> import numpy as np
>>> qx1 = np.array([(i + 1) / 100 for i in range(100)])
>>> tabua_last = TabuaMultiplasVidas(Tabua(qx1), Tabua(qx1), status=StatusVidasConjuntas.LAST)
>>> tabua_joint = TabuaMultiplasVidas(Tabua(qx1), Tabua(qx1), status=StatusVidasConjuntas.JOINT)

Com a tábua de multiplas vidas geralmente existe interesse em calcular as probabilidades de sobrevivência.

>>> tabua_last.tpx([30, 20], [0, 1, 2, 3, 4])
array([1.        , 0.9349    , 0.86908304, 0.80311964, 0.73758507])

>>> tabua_joint.tpx([30, 20], [0, 1, 2, 3, 4])
array([1.        , 0.5451    , 0.28912104, 0.14915754, 0.07481742])

Dependendo o status de vida conjunta, o tempo futuro máximo da tábua também é adaptado. Para uma tábua com status joint,
o tempo futuro máximo é o menor dos tempos futuros máximos de cada beneficiário, enquanto que para uma tábua com status
last, o tempo futuro máximo é o maior dos tempos futuros máximos de cada beneficiário.

>>> tabua_last.tempo_futuro_maximo([30, 20])
80.0

>>> tabua_joint.tempo_futuro_maximo([30, 20])
70.0