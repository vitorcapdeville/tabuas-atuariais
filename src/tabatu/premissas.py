from __future__ import annotations

from dataclasses import dataclass
from dataclasses import replace

from tabatu.multiplos_decrementos import TabuaMDT
from tabatu.periodicidade import Periodicidade
from tabatu.typing import TabuaInterface
from tabatu.typing import JurosInterface


@dataclass(frozen=True)
class PremissasAtuariais:
    tabua: TabuaInterface
    juros: JurosInterface

    def __post_init__(self):
        if self.tabua.periodicidade != self.juros.periodicidade:
            raise ValueError("Tabua e juros devem ter a mesma periodicidade.")

        if self.tabua.possui_fechamento_plato():
            raise ValueError("Tabua nao pode ser plato")

    @property
    def periodicidade(self) -> Periodicidade:
        return self.tabua.periodicidade

    def alterar_periodicidade(self, periodicidade: Periodicidade):
        nova_tabua = self.tabua.alterar_periodicidade(periodicidade)
        novos_juros = self.juros.alterar_periodicidade(periodicidade)
        return replace(self, tabua=nova_tabua, juros=novos_juros)


@dataclass(frozen=True)
class PremissasAtuariaisRenda(PremissasAtuariais):
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


class PremissasAtuariaisRendaInvalidez(PremissasAtuariaisRenda):
    tabua: TabuaMDT

    def __post_init__(self):
        super().__post_init__()
        if not self.tabua.possui_causa_principal():
            raise ValueError("A tabua de acumulação deve possuir uma causa principal.")
