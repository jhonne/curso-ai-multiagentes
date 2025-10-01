#!/usr/bin/env python3
"""
🎓 EXEMPLO SIMPLES: Agente Básico da Aula 9
===========================================

Este é um exemplo simplificado da Aula 9, demonstrando como criar
um agente básico que trabalha com múltiplas especialidades.

OBJETIVO:
Mostrar os conceitos fundamentais de múltiplos agentes de forma simples,
sem a complexidade completa do sistema da Aula 9.

EXECUÇÃO:
uv run aula9/exemplos/exemplo_agente_simples.py
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI

# Configurações básicas
load_dotenv()
PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "db" / "curso.db"

print("🎓 EXEMPLO SIMPLES: Conceitos Básicos Multi-Agente")
print("=" * 55)

# =============================================================================
# FERRAMENTA SIMPLES
# =============================================================================

class FerramentaSimples(BaseTool):
    """Ferramenta simplificada para demonstração"""
    
    name: str = "ferramenta_simples"
    description: str = "Ferramenta de exemplo que retorna informações básicas"
    
    def _run(self, tipo_info: str = "geral") -> str:
        """Retorna informação básica baseada no tipo"""
        
        if tipo_info == "hospitais":
            return """🏥 INFORMAÇÃO SOBRE HOSPITAIS:
            
• Total estimado: 8 estabelecimentos hospitalares
• Tipos: Hospitais gerais, especializados e de urgência
• Distribuição: Concentrados em áreas urbanas
• Funcionamento: 24 horas para emergências"""

        elif tipo_info == "estatisticas":
            return """📊 ESTATÍSTICAS BÁSICAS:
            
• Estabelecimentos: ~8 unidades principais
• Queixas catalogadas: ~141 tipos diferentes  
• Atendimentos registrados: ~1,579 casos
• Bairros atendidos: Múltiplas regiões"""

        else:
            return """ℹ️ INFORMAÇÃO GERAL:
            
• Sistema de saúde com dados reais
• Estabelecimentos: hospitais, UPAs, postos
• Análises: estatísticas, geográficas, clínicas
• Objetivo: Demonstrar multi-agentes CrewAI"""


# =============================================================================
# AGENTES SIMPLES
# =============================================================================

def criar_agente_simples_hospitais():
    """Agente simples focado em hospitais"""
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    ferramenta = FerramentaSimples()
    
    agente = Agent(
        role="Especialista Simples em Hospitais",
        goal="Fornecer informações básicas sobre hospitais e estabelecimentos",
        backstory="Sou um especialista que conhece os estabelecimentos de saúde.",
        llm=llm,
        tools=[ferramenta],
        verbose=False
    )
    
    return agente


def criar_agente_simples_estatisticas():
    """Agente simples focado em estatísticas"""
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    ferramenta = FerramentaSimples()
    
    agente = Agent(
        role="Especialista Simples em Estatísticas",
        goal="Fornecer números e estatísticas básicas",
        backstory="Sou um analista que trabalha com dados numéricos.",
        llm=llm,
        tools=[ferramenta],
        verbose=False
    )
    
    return agente


# =============================================================================
# SISTEMA MULTI-AGENTE SIMPLES
# =============================================================================

def executar_exemplo_multiagente(pergunta: str):
    """Executa exemplo com múltiplos agentes simples"""
    
    print(f"🤔 Pergunta: '{pergunta}'")
    
    # Escolher agente baseado na pergunta (lógica simples)
    if any(palavra in pergunta.lower() for palavra in ['hospital', 'estabelecimento']):
        agente = criar_agente_simples_hospitais()
        tipo_info = "hospitais"
        nome_agente = "Especialista em Hospitais"
    elif any(palavra in pergunta.lower() for palavra in ['estatística', 'número', 'quantos']):
        agente = criar_agente_simples_estatisticas()
        tipo_info = "estatisticas"
        nome_agente = "Especialista em Estatísticas"
    else:
        agente = criar_agente_simples_hospitais()
        tipo_info = "geral"
        nome_agente = "Especialista Geral"
    
    print(f"🎯 Direcionando para: {nome_agente}")
    
    # Criar tarefa
    tarefa = Task(
        description=f"""
        Responda à pergunta: "{pergunta}"
        
        Use a ferramenta_simples com tipo_info: {tipo_info}
        
        Seja claro e objetivo na resposta.
        """,
        agent=agente,
        expected_output="Resposta clara e informativa"
    )
    
    # Executar
    crew = Crew(
        agents=[agente],
        tasks=[tarefa],
        process=Process.sequential,
        verbose=False
    )
    
    try:
        resultado = crew.kickoff()
        return resultado.raw
    except Exception as e:
        return f"❌ Erro: {str(e)}"


# =============================================================================
# DEMONSTRAÇÃO
# =============================================================================

def demonstracao_simples():
    """Demonstração dos conceitos básicos"""
    
    print("\n🎬 DEMONSTRAÇÃO DOS CONCEITOS BÁSICOS")
    print("=" * 50)
    
    exemplos = [
        "Quais são os hospitais disponíveis?",
        "Mostre estatísticas gerais",
        "Informações sobre o sistema"
    ]
    
    for i, pergunta in enumerate(exemplos, 1):
        print(f"\n📝 Exemplo {i}: {pergunta}")
        print("-" * 30)
        
        resposta = executar_exemplo_multiagente(pergunta)
        print(resposta)
        
        if i < len(exemplos):
            input("\n⏸️ Pressione ENTER para continuar...")


def main():
    """Função principal do exemplo simples"""
    
    print("\n🎯 ESCOLHA O MODO:")
    print("1. 🎬 Demonstração Automática")
    print("2. 💬 Modo Interativo Simples")
    print("3. ❌ Sair")
    
    while True:
        escolha = input("\nEscolha (1-3): ").strip()
        
        if escolha == '1':
            demonstracao_simples()
            break
        elif escolha == '2':
            print("\n💬 Modo Interativo Simples")
            print("Digite perguntas sobre hospitais ou estatísticas:")
            print("('sair' para encerrar)")
            
            while True:
                pergunta = input("\n💬 Sua pergunta: ").strip()
                if pergunta.lower() in ['sair', 'quit']:
                    break
                if pergunta:
                    resposta = executar_exemplo_multiagente(pergunta)
                    print(f"\n📋 Resposta: {resposta}")
            break
        elif escolha == '3':
            print("👋 Até mais!")
            break
        else:
            print("⚠️ Opção inválida")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Exemplo interrompido!")
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")