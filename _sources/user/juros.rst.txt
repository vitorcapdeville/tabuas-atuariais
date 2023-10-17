=====
Juros
=====

A classe :class:`~tabatu.JurosConstante` define a taxa de juros, que usualmente acompanha as tábuas biométricas em seguroos de vida.

Para o :class:`~tabatu.JurosConstante`, basta fornecer a taxa de juros e a periodicidade dessa taxa. Por exemplo,
para criar uma taxa de juros constante de 3% ao ano, utilizamos:

>>> from tabatu import JurosConstante
>>> from tabatu.periodicidade import Periodicidade
>>> juros = JurosConstante(0.03, Periodicidade.ANUAL)

A partir dessa instância, podemos calcular a taxa de juros e a taxa de desconto para um determinado período. Como o
juros é anual, podemos calcular a taxa de juros para os 4 primeiros anos.

>>> juros.taxa_juros([0, 1, 2, 3])
array([0.03, 0.03, 0.03, 0.03])

Como o juros é constante, obtemos os mesmos 3% para todos os períodos. A taxa de desconto é calculada da mesma forma:

>>> juros.taxa_desconto([0, 1, 2, 3])
array([1.        , 0.97087379, 0.94259591, 0.91514166])
