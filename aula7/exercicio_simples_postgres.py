#!/usr/bin/env python3
"""
Exercício PostgreSQL - Versão Simplificada
==========================================

Teste básico de agente CrewAI com PostgreSQL

EXECUÇÃO: uv run aula7/exercicio_simples_postgres.py
"""

import os
from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Carregar variáveis de ambiente
load_dotenv()

def testar_conexao_postgres():
    """Testa conexão PostgreSQL (simulado para exercício)"""
    print("🔍 Testando conexão PostgreSQL...")
    
    # Simulação de dados (caso não tenha PostgreSQL)
    estabelecimentos_mock = [
        {"id": 1, "nome": "Hospital São Paulo", "tipo": "hospital", "municipio": "São Paulo", "telefone": "(11) 1111-1111"},
        {"id": 2, "nome": "UPA Central", "tipo": "upa", "municipio": "São Paulo", "telefone": "(11) 2222-2222"},
        {"id": 3, "nome": "Clínica Santa Maria", "tipo": "clinica", "municipio": "Santo André", "telefone": "(11) 3333-3333"},
    ]
    
    print("✅ Dados carregados (simulação)")
    return estabelecimentos_mock

def criar_agente_consultor():
    """Cria agente consultor de estabelecimentos médicos"""
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1
    )
    
    agente = Agent(
        role="Consultor de Estabelecimentos Médicos",
        goal="Analisar e organizar informações sobre estabelecimentos de saúde",
        backstory="""
        Sou especialista em análise de dados de estabelecimentos médicos.
        Organizo informações sobre hospitais, UPAs e clínicas de forma clara
        para ajudar pacientes a encontrar atendimento adequado.
        """,
        verbose=True,
        llm=llm
    )
    
    return agente

def executar_exercicio_simples():
    """Executa exercício simples"""
    
    print("🏥 EXERCÍCIO CREWAI + POSTGRESQL (SIMPLES)")
    print("=" * 45)
    
    # Dados simulados
    dados = testar_conexao_postgres()
    
    # Criar agente
    print("\n🤖 Criando agente...")
    agente = criar_agente_consultor()
    
    # Dados para análise
    dados_texto = "\n".join([
        f"- {item['nome']} ({item['tipo']}) - {item['municipio']} - {item['telefone']}"
        for item in dados
    ])
    
    # Tarefa de análise
    tarefa = Task(
        description=f"""
        Analise os seguintes estabelecimentos médicos encontrados no banco PostgreSQL:
        
        ESTABELECIMENTOS ENCONTRADOS:
        {dados_texto}
        
        Tarefas:
        1. Organize por tipo (hospitais, UPAs, clínicas)
        2. Destaque informações importantes
        3. Faça recomendações sobre quando procurar cada tipo
        4. Apresente um resumo executivo
        """,
        agent=agente,
        expected_output="""
        Relatório organizado com:
        1. Lista por tipo de estabelecimento
        2. Informações de contato organizadas
        3. Recomendações de uso
        4. Resumo executivo
        """
    )
    
    # Executar
    crew = Crew(
        agents=[agente],
        tasks=[tarefa],
        process=Process.sequential,
        verbose=False
    )
    
    print("\n🚀 Executando análise...")
    resultado = crew.kickoff()
    
    print("\n📋 RESULTADO DA ANÁLISE:")
    print("-" * 35)
    print(resultado.raw)
    
    print("\n✅ EXERCÍCIO CONCLUÍDO!")
    print("🎓 Agente analisou dados simulados do PostgreSQL")

if __name__ == "__main__":
    try:
        executar_exercicio_simples()
    except KeyboardInterrupt:
        print("\n⏹️ Exercício interrompido")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("💡 Este é um exercício de demonstração")