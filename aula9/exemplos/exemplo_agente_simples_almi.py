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

        print(f"🔍 FerramentaSimples: buscando info tipo '{tipo_info}'")
        
        try:
            if tipo_info == "nenhum":
                return """❌ INFORMAÇÃO NÃO DISPONÍVEL:
                
• Não há dados disponíveis para esta consulta
• Por favor, faça uma pergunta sobre:
  - Hospitais e estabelecimentos
  - Estatísticas do sistema
  - Informações gerais"""
                
            conn = self._conectar_banco()
            cursor = conn.cursor()
            
            if tipo_info == "hospitais":
                # Buscar informações sobre estabelecimentos
                cursor.execute("SELECT COUNT(*) FROM ia_estabelecimento")
                total = cursor.fetchone()[0]
                
                cursor.execute("""
                    SELECT nome 
                    FROM ia_estabelecimento 
                    ORDER BY nome
                """)
                exemplos = cursor.fetchall()
                
                resultado = f"""🏥 INFORMAÇÃO SOBRE HOSPITAIS (DADOS REAIS):
                
• Total de estabelecimentos: {total} unidades
• Exemplos:
"""
                for nome in exemplos:
                    resultado += f"  - {nome}\n"
                
                conn.close()
                print(f"\n📤 Resultado da consulta:\n{resultado}\n")
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
                print(f"\n📤 Resultado da consulta:\n{resultado}\n")
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
                print(f"\n📤 Resultado da consulta:\n{resultado}\n")
                return resultado
                
        except Exception as e:
            return f"❌ Erro ao acessar banco de dados: {str(e)}"


# =============================================================================
# AGENTES SIMPLES
# =============================================================================

def criar_agente_interprete():
    """Agente intérprete que analisa e direciona as perguntas"""
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
    
    agente = Agent(
        role="Intérprete de Consultas",
        goal="Analisar perguntas e identificar o melhor tipo de consulta",
        backstory="""Sou um especialista em análise de linguagem natural.
        Minha função é entender a intenção do usuário e direcionar para o tipo
        de consulta mais adequado.""",
        llm=llm,
        verbose=False
    )
    
    return agente

def criar_agente_especialista():
    """Agente especialista que responde usando a ferramenta"""
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    ferramenta = FerramentaSimples()
    
    agente = Agent(
        role="Especialista em Informações",
        goal="Fornecer informações precisas usando a base de dados",
        backstory="""Sou um especialista que acessa e interpreta dados do sistema
        de saúde, fornecendo respostas precisas e relevantes.""",
        llm=llm,
        tools=[ferramenta],
        verbose=False
    )
    
    return agente

# =============================================================================
# SISTEMA MULTI-AGENTE APRIMORADO
# =============================================================================

def executar_exemplo_multiagente(pergunta: str):
    """Executa exemplo com sistema de interpretação inteligente"""
    
    print(f"🤔 Pergunta: '{pergunta}'")
    
    # Criar agentes
    agente_interprete = criar_agente_interprete()
    agente_especialista = criar_agente_especialista()
    
    # Tarefa de interpretação
    tarefa_interpretacao = Task(
        description=f"""
        Analise a pergunta: "{pergunta}"
        
        Determine qual tipo de informação é mais adequado:
        - "hospitais" para perguntas sobre estabelecimentos de saúde
        - "estatisticas" para perguntas sobre números e dados sobre estabelecimentos de saude, queixas e sintomas
        - "geral" para perguntas gerais sobre estabelecimentos de saude, queixas e sintomas
        - "nenhum" para perguntas que não se encaixem nessas categorias
        
        Retorne apenas o tipo escolhido em minúsculas, sem explicações adicionais.
        """,
        agent=agente_interprete,
        expected_output="hospitais | estatisticas | geral | nenhum"
    )
    
    # Executar interpretação
    crew_interprete = Crew(
        agents=[agente_interprete],
        tasks=[tarefa_interpretacao],
        process=Process.sequential,
        verbose=False
    )
    
    try:
        tipo_info = crew_interprete.kickoff()
        print(f"🎯 Tipo de consulta identificada: {tipo_info}")
        
        # Tarefa de resposta
        tarefa_resposta = Task(
            description=f"""
            Responda à pergunta: "{pergunta}"
            
            Use a ferramenta_simples com tipo_info: {tipo_info}
            
            Seja claro e objetivo na resposta. Caso não seja possível responder,
            informe que não há dados disponíveis.
            """,
            agent=agente_especialista,
            expected_output="Resposta clara e informativa"
        )
        
        # Executar resposta
        crew_resposta = Crew(
            agents=[agente_especialista],
            tasks=[tarefa_resposta],
            process=Process.sequential,
            verbose=False
        )
        
        return crew_resposta.kickoff()
    
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