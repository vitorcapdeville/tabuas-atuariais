{% if objtype == 'property' %}
:orphan:
{% endif %}

{{ objname | escape | underline}}

.. currentmodule:: {{ module }}

{% if objtype == 'property' %}
property
{% endif %}

.. auto{{ objtype }}:: {{ objname | replace("tabatu.", "tabatu::") }}

{# In the fullname (e.g. `numpy.ma.MaskedArray.methodname`), the module name
is ambiguous. Using a `::` separator (e.g. `numpy::ma.MaskedArray.methodname`)
specifies `numpy` as the module name. #}