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
import sqlite3
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
# FERRAMENTA COM BANCO DE DADOS
# =============================================================================

class FerramentaSimples(BaseTool):
    """Ferramenta que busca informações reais do banco de dados"""
    
    name: str = "ferramenta_simples"
    description: str = "Ferramenta que retorna informações do banco de dados"
    
    def _conectar_banco(self):
        """Conecta ao banco de dados SQLite"""
        return sqlite3.connect(DB_PATH)
    
    def _run(self, tipo_info: str = "geral") -> str:
        """Retorna informação do banco baseada no tipo"""
        
        try:
            conn = self._conectar_banco()
            cursor = conn.cursor()
            
            if tipo_info == "hospitais":
                # Buscar informações sobre estabelecimentos
                cursor.execute("SELECT COUNT(*) FROM ia_estabelecimento")
                total = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT nome, tipo_estabelecimento 
                    FROM ia_estabelecimento 
                    LIMIT 3
                """)
                exemplos = cursor.fetchall()
                
                resultado = f"""🏥 INFORMAÇÃO SOBRE HOSPITAIS (DADOS REAIS):
                
• Total de estabelecimentos: {total} unidades
• Exemplos:
"""
                for nome, tipo in exemplos:
                    resultado += f"  - {nome} ({tipo})\n"
                
                conn.close()
                return resultado

            elif tipo_info == "estatisticas":
                # Buscar estatísticas reais
                cursor.execute("SELECT COUNT(*) FROM ia_estabelecimento")
                total_estab = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM ia_queixa_principal")
                total_queixas = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM ia_historico_atendimento_sintoma")
                total_atendimentos = cursor.fetchone()[0]
                
                resultado = f"""📊 ESTATÍSTICAS BÁSICAS (DADOS REAIS):
                
• Estabelecimentos: {total_estab} unidades
• Queixas catalogadas: {total_queixas} tipos
• Atendimentos registrados: {total_atendimentos} casos
• Fonte: Banco de dados SQLite"""
                
                conn.close()
                return resultado

            else:
                # Informação geral com dados do banco
                cursor.execute("SELECT COUNT(*) FROM ia_estabelecimento")
                total_estab = cursor.fetchone()[0]
                
                cursor.execute("SELECT COUNT(*) FROM ia_queixa_principal")
                total_queixas = cursor.fetchone()[0]
                
                resultado = f"""ℹ️ INFORMAÇÃO GERAL (DADOS REAIS):
                
• Sistema de saúde com {total_estab} estabelecimentos
• {total_queixas} tipos de queixas catalogadas
• Banco de dados: SQLite
• Objetivo: Demonstrar multi-agentes CrewAI com dados reais"""
                
                conn.close()
                return resultado
                
        except Exception as e:
            return f"❌ Erro ao acessar banco de dados: {str(e)}"


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
        
        # Comentado para execução automática
        # if i < len(exemplos):
        #     input("\n⏸️ Pressione ENTER para continuar...")


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