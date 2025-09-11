#!/usr/bin/env python3
"""
Configurador de Penalties para CrewAI
Ferramenta para otimizar frequency_penalty e presence_penalty em projetos existentes
"""

import json
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from crewai import Agent
from langchain_openai import ChatOpenAI


@dataclass
class ConfiguracaoPenalties:
    """Configuração de penalties para diferentes contextos"""

    contexto: str
    frequency_penalty: float
    presence_penalty: float
    temperature: float
    model: str
    descricao: str
    casos_uso: list

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ConfiguracaoPenalties":
        """Cria instância a partir de dicionário"""
        return cls(**data)


class BibliotecaConfiguracoes:
    """Biblioteca de configurações pré-definidas"""

    def __init__(self):
        self.configuracoes = {
            "documentacao_tecnica": ConfiguracaoPenalties(
                contexto="documentacao_tecnica",
                frequency_penalty=0.1,
                presence_penalty=0.0,
                temperature=0.2,
                model="gpt-4o-mini",
                descricao="Para documentação técnica precisa que precisa repetir termos específicos",
                casos_uso=["APIs", "manuais", "especificações", "código"],
            ),
            "relatorio_analitico": ConfiguracaoPenalties(
                contexto="relatorio_analitico",
                frequency_penalty=0.3,
                presence_penalty=0.2,
                temperature=0.3,
                model="gpt-4o-mini",
                descricao="Para relatórios que precisam de precisão mas com alguma variação",
                casos_uso=["análises de dados", "relatórios financeiros", "pesquisas"],
            ),
            "conteudo_educacional": ConfiguracaoPenalties(
                contexto="conteudo_educacional",
                frequency_penalty=0.4,
                presence_penalty=0.4,
                temperature=0.6,
                model="gpt-4o-mini",
                descricao="Para conteúdo que deve ser variado e explorar diferentes aspectos",
                casos_uso=["artigos", "tutoriais", "explicações", "cursos"],
            ),
            "brainstorming": ConfiguracaoPenalties(
                contexto="brainstorming",
                frequency_penalty=0.7,
                presence_penalty=0.8,
                temperature=0.8,
                model="gpt-4o",
                descricao="Para máxima criatividade e exploração de ideias",
                casos_uso=["ideação", "inovação", "soluções criativas", "estratégias"],
            ),
            "chatbot_atendimento": ConfiguracaoPenalties(
                contexto="chatbot_atendimento",
                frequency_penalty=0.3,
                presence_penalty=0.2,
                temperature=0.7,
                model="gpt-4o-mini",
                descricao="Para conversas naturais mas focadas no problema",
                casos_uso=["suporte", "FAQ", "atendimento", "assistente virtual"],
            ),
            "storytelling": ConfiguracaoPenalties(
                contexto="storytelling",
                frequency_penalty=0.5,
                presence_penalty=0.6,
                temperature=0.8,
                model="gpt-4o",
                descricao="Para narrativas ricas e envolventes",
                casos_uso=["histórias", "cases", "narrativas", "marketing"],
            ),
            "codigo_comentarios": ConfiguracaoPenalties(
                contexto="codigo_comentarios",
                frequency_penalty=0.2,
                presence_penalty=0.1,
                temperature=0.3,
                model="gpt-4o-mini",
                descricao="Para comentários de código claros e concisos",
                casos_uso=["documentação código", "comments", "docstrings"],
            ),
            "marketing_criativo": ConfiguracaoPenalties(
                contexto="marketing_criativo",
                frequency_penalty=0.6,
                presence_penalty=0.7,
                temperature=0.9,
                model="gpt-4o",
                descricao="Para copy criativo e campanhas inovadoras",
                casos_uso=["copy", "slogans", "campanhas", "social media"],
            ),
        }

    def obter_configuracao(self, contexto: str) -> Optional[ConfiguracaoPenalties]:
        """Obtém configuração por contexto"""
        return self.configuracoes.get(contexto)

    def listar_contextos(self) -> list:
        """Lista todos os contextos disponíveis"""
        return list(self.configuracoes.keys())

    def buscar_por_caso_uso(self, caso_uso: str) -> list:
        """Busca configurações por caso de uso"""
        resultados = []
        for config in self.configuracoes.values():
            if any(caso_uso.lower() in uso.lower() for uso in config.casos_uso):
                resultados.append(config)
        return resultados

    def salvar_biblioteca(self, arquivo: str = "configuracoes_penalties.json"):
        """Salva biblioteca em arquivo JSON"""
        data = {ctx: config.to_dict() for ctx, config in self.configuracoes.items()}
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ Biblioteca salva em {arquivo}")

    def carregar_biblioteca(self, arquivo: str = "configuracoes_penalties.json"):
        """Carrega biblioteca de arquivo JSON"""
        try:
            with open(arquivo, "r", encoding="utf-8") as f:
                data = json.load(f)

            self.configuracoes = {
                ctx: ConfiguracaoPenalties.from_dict(config_data)
                for ctx, config_data in data.items()
            }
            print(f"✅ Biblioteca carregada de {arquivo}")
        except FileNotFoundError:
            print(f"⚠️ Arquivo {arquivo} não encontrado, usando configurações padrão")


class OtimizadorPenalties:
    """Otimizador que sugere configurações baseado em feedback"""

    def __init__(self):
        self.historico_otimizacao = []

    def analisar_texto(self, texto: str) -> Dict[str, float]:
        """Analisa características do texto gerado"""
        palavras = texto.lower().split()

        # Diversidade vocabular
        palavras_unicas = len(set(palavras))
        total_palavras = len(palavras)
        diversidade = palavras_unicas / total_palavras if total_palavras > 0 else 0

        # Análise de repetição
        contagem_palavras = {}
        for palavra in palavras:
            contagem_palavras[palavra] = contagem_palavras.get(palavra, 0) + 1

        # Palavras que aparecem mais de uma vez
        palavras_repetidas = sum(1 for count in contagem_palavras.values() if count > 1)
        taxa_repeticao = (
            palavras_repetidas / len(contagem_palavras) if contagem_palavras else 0
        )

        # Análise de frases
        frases = [f.strip() for f in texto.split(".") if f.strip()]
        frases_unicas = len(set(frases))
        diversidade_frases = frases_unicas / len(frases) if frases else 0

        return {
            "diversidade_vocabular": diversidade,
            "taxa_repeticao": taxa_repeticao,
            "diversidade_frases": diversidade_frases,
            "total_palavras": total_palavras,
            "total_frases": len(frases),
        }

    def sugerir_ajustes(
        self, analise: Dict[str, float], config_atual: ConfiguracaoPenalties
    ) -> Dict[str, Any]:
        """Sugere ajustes baseado na análise"""
        sugestoes = {
            "frequency_penalty": config_atual.frequency_penalty,
            "presence_penalty": config_atual.presence_penalty,
            "justificativas": [],
        }

        # Se diversidade vocabular está baixa, aumentar frequency penalty
        if analise["diversidade_vocabular"] < 0.6:
            nova_freq = min(config_atual.frequency_penalty + 0.2, 2.0)
            sugestoes["frequency_penalty"] = nova_freq
            sugestoes["justificativas"].append(
                f"Diversidade vocabular baixa ({analise['diversidade_vocabular']:.2f}): "
                f"aumentar frequency_penalty para {nova_freq}"
            )

        # Se taxa de repetição alta, aumentar frequency penalty
        if analise["taxa_repeticao"] > 0.4:
            nova_freq = min(config_atual.frequency_penalty + 0.3, 2.0)
            sugestoes["frequency_penalty"] = max(
                sugestoes["frequency_penalty"], nova_freq
            )
            sugestoes["justificativas"].append(
                f"Taxa de repetição alta ({analise['taxa_repeticao']:.2f}): "
                f"aumentar frequency_penalty para {nova_freq}"
            )

        # Se diversidade de frases baixa, aumentar presence penalty
        if analise["diversidade_frases"] < 0.7:
            nova_pres = min(config_atual.presence_penalty + 0.3, 2.0)
            sugestoes["presence_penalty"] = nova_pres
            sugestoes["justificativas"].append(
                f"Diversidade de frases baixa ({analise['diversidade_frases']:.2f}): "
                f"aumentar presence_penalty para {nova_pres}"
            )

        # Se diversidade muito alta (pode estar incoerente)
        if analise["diversidade_vocabular"] > 0.9:
            nova_freq = max(config_atual.frequency_penalty - 0.1, 0.0)
            sugestoes["frequency_penalty"] = nova_freq
            sugestoes["justificativas"].append(
                f"Diversidade muito alta ({analise['diversidade_vocabular']:.2f}): "
                f"reduzir frequency_penalty para {nova_freq}"
            )

        return sugestoes


class ConfiguradorCrewAI:
    """Configurador principal para integração com CrewAI"""

    def __init__(self):
        self.biblioteca = BibliotecaConfiguracoes()
        self.otimizador = OtimizadorPenalties()

    def criar_llm_configurado(self, contexto: str, **kwargs) -> ChatOpenAI:
        """Cria LLM configurado para contexto específico"""
        config = self.biblioteca.obter_configuracao(contexto)

        if not config:
            print(f"⚠️ Contexto '{contexto}' não encontrado, usando padrão educacional")
            config = self.biblioteca.obter_configuracao("conteudo_educacional")

        # Permite override de parâmetros
        frequency_penalty = kwargs.get("frequency_penalty", config.frequency_penalty)
        presence_penalty = kwargs.get("presence_penalty", config.presence_penalty)
        temperature = kwargs.get("temperature", config.temperature)
        model = kwargs.get("model", config.model)

        print(f"🔧 Configurando LLM para contexto '{contexto}':")
        print(f"   📊 Frequency Penalty: {frequency_penalty}")
        print(f"   🌟 Presence Penalty: {presence_penalty}")
        print(f"   🌡️ Temperature: {temperature}")
        print(f"   🤖 Model: {model}")

        return ChatOpenAI(
            model=model,
            temperature=temperature,
            model_kwargs={
                "frequency_penalty": frequency_penalty,
                "presence_penalty": presence_penalty,
            },
        )

    def criar_agente_otimizado(
        self, contexto: str, role: str, goal: str, backstory: str, **kwargs
    ) -> Agent:
        """Cria agente com configuração otimizada"""
        llm = self.criar_llm_configurado(contexto, **kwargs)

        return Agent(
            role=role,
            goal=goal,
            backstory=backstory,
            llm=llm,
            verbose=kwargs.get("verbose", True),
        )

    def avaliar_e_otimizar(
        self, texto_gerado: str, contexto_usado: str
    ) -> Dict[str, Any]:
        """Avalia resultado e sugere otimizações"""
        config_atual = self.biblioteca.obter_configuracao(contexto_usado)
        analise = self.otimizador.analisar_texto(texto_gerado)
        sugestoes = self.otimizador.sugerir_ajustes(analise, config_atual)

        return {
            "analise": analise,
            "configuracao_atual": config_atual.to_dict(),
            "sugestoes": sugestoes,
        }

    def gerar_relatorio_configuracao(self) -> str:
        """Gera relatório completo das configurações"""
        relatorio = ["📋 RELATÓRIO DE CONFIGURAÇÕES PENALTIES", "=" * 50, ""]

        for contexto, config in self.biblioteca.configuracoes.items():
            relatorio.extend(
                [
                    f"🎯 {contexto.upper().replace('_', ' ')}:",
                    f"   📊 Frequency: {config.frequency_penalty} | Presence: {config.presence_penalty}",
                    f"   🌡️ Temperature: {config.temperature} | Model: {config.model}",
                    f"   💭 {config.descricao}",
                    f"   🎨 Casos de uso: {', '.join(config.casos_uso)}",
                    "",
                ]
            )

        return "\n".join(relatorio)


def demonstrar_uso_pratico():
    """Demonstra uso prático do configurador"""

    print("🚀 DEMONSTRAÇÃO: CONFIGURADOR DE PENALTIES")
    print("=" * 60)

    configurador = ConfiguradorCrewAI()

    # Lista contextos disponíveis
    print("📋 Contextos disponíveis:")
    for contexto in configurador.biblioteca.listar_contextos():
        config = configurador.biblioteca.obter_configuracao(contexto)
        print(f"   • {contexto}: {config.descricao}")

    print("\n" + configurador.gerar_relatorio_configuracao())

    # Exemplo de busca por caso de uso
    print("🔍 BUSCA POR CASO DE USO:")
    resultados = configurador.biblioteca.buscar_por_caso_uso("documentação")
    for config in resultados:
        print(f"   • {config.contexto}: {config.descricao}")

    # Exemplo de criação de agente
    print("\n🤖 EXEMPLO: CRIANDO AGENTE OTIMIZADO")
    try:
        agente_docs = configurador.criar_agente_otimizado(
            contexto="documentacao_tecnica",
            role="Documentador Técnico",
            goal="Criar documentação clara e precisa",
            backstory="Especialista em documentação técnica",
            verbose=False,
        )
        print("✅ Agente criado com sucesso!")

    except Exception as e:
        print(f"⚠️ Não foi possível criar agente (sem API key): {e}")

    # Simula análise de texto
    print("\n📊 EXEMPLO: ANÁLISE E OTIMIZAÇÃO")
    texto_exemplo = """
    A documentação deve ser clara. A documentação deve ser precisa. 
    A documentação deve ser completa. A documentação é importante.
    """

    analise = configurador.otimizador.analisar_texto(texto_exemplo)
    print(f"📝 Texto analisado: {texto_exemplo[:50]}...")
    print(f"📊 Diversidade vocabular: {analise['diversidade_vocabular']:.3f}")
    print(f"🔄 Taxa de repetição: {analise['taxa_repeticao']:.3f}")

    # Sugere melhorias
    config_exemplo = configurador.biblioteca.obter_configuracao("documentacao_tecnica")
    sugestoes = configurador.otimizador.sugerir_ajustes(analise, config_exemplo)

    if sugestoes["justificativas"]:
        print("\n💡 SUGESTÕES DE MELHORIA:")
        for justificativa in sugestoes["justificativas"]:
            print(f"   • {justificativa}")
    else:
        print("\n✅ Configuração atual parece adequada!")


def main():
    """Função principal"""
    print("⚙️ CONFIGURADOR DE PENALTIES PARA CREWAI")
    print("Ferramenta para otimizar frequency_penalty e presence_penalty")
    print("=" * 70)

    # Demonstra uso prático
    demonstrar_uso_pratico()

    # Salva configurações para uso futuro
    configurador = ConfiguradorCrewAI()
    configurador.biblioteca.salvar_biblioteca()

    print("\n💾 Configurações salvas em 'configuracoes_penalties.json'")
    print("🔧 Use essas configurações em seus projetos CrewAI!")

    print("\n📚 PRÓXIMOS PASSOS:")
    print("1. Importe este módulo em seus projetos")
    print("2. Use criar_agente_otimizado() com o contexto apropriado")
    print("3. Monitore resultados com avaliar_e_otimizar()")
    print("4. Ajuste configurações conforme necessário")


if __name__ == "__main__":
    main()
