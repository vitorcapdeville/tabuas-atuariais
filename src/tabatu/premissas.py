from __future__ import annotations

from dataclasses import dataclass
from dataclasses import replace

from tabatu.multiplos_decrementos import TabuaMDT
from tabatu.periodicidade import Periodicidade
from tabatu.typing import TabuaInterface
from tabatu.typing import JurosInterface


@dataclass(frozen=True)
class Premissas:
    """Define a estrutura de premissas utilizadas em diversos cálculos atuariais.
    São realizadas validações para garantir que os componentes são compatíveis entre si.

    Args:
        tabua (TabuaInterface): Tabua biométrica.
        juros (JurosInterface): Juros.
    """
    tabua: TabuaInterface
    juros: JurosInterface

    def __post_init__(self):
        if self.tabua.periodicidade != self.juros.periodicidade:
            raise ValueError("Tabua e juros devem ter a mesma periodicidade.")

        if self.tabua.possui_fechamento_plato():
            raise ValueError("Tabua nao pode ser plato")

    @property
    def periodicidade(self) -> Periodicidade:
        """Periodicidade das premissas."""
        return self.tabua.periodicidade

    def alterar_periodicidade(self, periodicidade: Periodicidade):
        """Gera uma nova premissa com a periodicidade alterada."""
        nova_tabua = self.tabua.alterar_periodicidade(periodicidade)
        novos_juros = self.juros.alterar_periodicidade(periodicidade)
        return replace(self, tabua=nova_tabua, juros=novos_juros)


@dataclass(frozen=True)
class PremissasRenda(Premissas):
    """Define a estrutura de premissas utilizadas em diversos cálculos atuariais relacionados 
    a concessão de rendas.
    São realizadas validações para garantir que os componentes são compatíveis entre si.

    Args:
        tabua (TabuaInterface): Tabua biométrica.
        juros (JurosInterface): Juros.
        tabua_concessao (TabuaInterface): Tábua biométrica associada a concessão da renda.
    """
    tabua: TabuaInterface
    juros: JurosInterface
    tabua_concessao: TabuaInterface

    def __post_init__(self):
        super().__post_init__()
        if self.tabua_concessao.possui_fechamento_plato():
            raise ValueError("tabua de concessao nao pode ser plato")

        if self.tabua.periodicidade != self.tabua_concessao.periodicidade:
            raise ValueError(
                "Tabua, juros e tabua de concessão devem ter a mesma periodicidade."
            )

    def alterar_periodicidade(self, periodicidade: Periodicidade):
        nova_tabua = self.tabua.alterar_periodicidade(periodicidade)
        novos_juros = self.juros.alterar_periodicidade(periodicidade)
        nova_tabua_concessao = self.tabua_concessao.alterar_periodicidade(periodicidade)
        return replace(
            self,
            tabua=nova_tabua,
            juros=novos_juros,
            tabua_concessao=nova_tabua_concessao,
        )


class PremissasRendaInvalidez(PremissasRenda):
    """Define a estrutura de premissas utilizadas em cálculos associados a rendas por invalidez.
    São realizadas validações para garantir que os componentes são compatíveis entre si.

    Args:
        tabua (TabuaMDT): Tabua biométrica, deve possuir como causa principal a invalidez.
        juros (JurosInterface): Juros.
        tabua_concessao (TabuaInterface): Tábua biométrica associada a concessão da renda.
    """
    tabua: TabuaMDT
    juros: JurosInterface
    tabua_concessao: TabuaInterface

    def __post_init__(self):
        super().__post_init__()
        if not self.tabua.possui_causa_principal():
            raise ValueError("A tabua de acumulação deve possuir uma causa principal.")
