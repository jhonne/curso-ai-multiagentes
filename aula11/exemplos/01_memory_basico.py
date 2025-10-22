#!/usr/bin/env python3
"""
Exemplo 1: Memory System Básico

Demonstra como usar o sistema de memória do CrewAI para criar
um chatbot que lembra do histórico de conversas.

Execute: uv run aula11/exemplos/01_memory_basico.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# ✅ Configurar storage ANTES de importar CrewAI
load_dotenv()

# Adicionar aula11 ao path para importar setup_storage
sys.path.insert(0, str(Path(__file__).parent.parent))
from setup_storage import configurar_storage
config = configurar_storage(__file__)

# ✅ AGORA importar CrewAI (usa a config acima)
from crewai import Agent, Task, Crew, Process, LLM


def exemplo_sem_memoria():
    """Chatbot SEM memória - não lembra de interações anteriores"""
    print("\n" + "=" * 70)
    print("❌ CHATBOT SEM MEMÓRIA")
    print("=" * 70)
    
    llm = LLM(model="gpt-4o-mini", temperature=0.7)
    
    agente = Agent(
        role="Atendente Simples",
        goal="Responder perguntas do paciente",
        backstory="Atendente básico sem acesso a histórico.",
        llm=llm,
        verbose=False
    )
    
    tarefa = Task(
        description="Responda: {pergunta}",
        expected_output="Resposta clara e direta",
        agent=agente
    )
    
    crew = Crew(
        agents=[agente],
        tasks=[tarefa],
        memory=False,  # ❌ SEM memória
        process=Process.sequential,
        verbose=False
    )
    
    # Primeira pergunta
    print("\n📝 Pergunta 1: Estou com dor de cabeça")
    r1 = crew.kickoff(inputs={"pergunta": "Estou com dor de cabeça"})
    print(f"💬 Resposta: {r1.raw}\n")
    
    # Segunda pergunta - NÃO vai lembrar da primeira
    print("📝 Pergunta 2: E agora tenho febre também")
    r2 = crew.kickoff(inputs={"pergunta": "E agora tenho febre também"})
    print(f"💬 Resposta: {r2.raw}\n")
    
    print("⚠️  Observe: O agente NÃO lembrou da dor de cabeça!")


def exemplo_com_memoria():
    """Chatbot COM memória - lembra de tudo!"""
    print("\n" + "=" * 70)
    print("✅ CHATBOT COM MEMÓRIA")
    print("=" * 70)
    
    llm = LLM(model="gpt-4o-mini", temperature=0.7)
    
    agente = Agent(
        role="Atendente Inteligente",
        goal="Atender pacientes lembrando de todo o histórico",
        backstory="""Atendente experiente com memória fotográfica.
        Sempre faz referência a conversas anteriores.""",
        llm=llm,
        verbose=False
    )
    
    tarefa = Task(
        description="Responda: {pergunta}",
        expected_output="Resposta contextualizada e empática",
        agent=agente
    )
    
    crew = Crew(
        agents=[agente],
        tasks=[tarefa],
        memory=True,  # ✅ COM memória!
        process=Process.sequential,
        verbose=False
    )
    
    # Primeira pergunta
    print("\n📝 Pergunta 1: Estou com dor de cabeça")
    r1 = crew.kickoff(inputs={"pergunta": "Estou com dor de cabeça"})
    print(f"💬 Resposta: {r1.raw}\n")
    
    # Segunda pergunta - VAI lembrar da primeira!
    print("📝 Pergunta 2: E agora tenho febre também")
    r2 = crew.kickoff(inputs={"pergunta": "E agora tenho febre também"})
    print(f"💬 Resposta: {r2.raw}\n")
    
    print("✨ Observe: O agente LEMBROU da dor de cabeça!")
    
    # Terceira pergunta para confirmar memória
    print("📝 Pergunta 3: Recapitule meus sintomas")
    r3 = crew.kickoff(inputs={
        "pergunta": "Pode me dizer todos os sintomas que mencionei?"
    })
    print(f"💬 Resposta: {r3.raw}\n")
    
    print("🎯 O agente lembrou de TUDO: dor de cabeça + febre!")


def verificar_storage():
    """Mostra onde a memória é armazenada"""
    from crewai.utilities.paths import db_storage_path
    
    print("\n" + "=" * 70)
    print("📁 LOCALIZAÇÃO DO STORAGE")
    print("=" * 70)
    
    storage = db_storage_path()
    print(f"\n💾 Memórias salvas em: {storage}\n")
    
    if os.path.exists(storage):
        print("📂 Estrutura:")
        for item in os.listdir(storage):
            print(f"   └── {item}")
    else:
        print("⚠️  Storage ainda não criado (execute o exemplo primeiro)")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY não configurada")
        print("💡 Execute: uv run configurar.py")
        sys.exit(1)
    
    print("\n🎓 EXEMPLO 1: MEMORY SYSTEM BÁSICO")
    print("\nVamos comparar chatbot SEM memória vs COM memória\n")
    
    input("⏸️  Pressione ENTER para ver chatbot SEM memória...")
    exemplo_sem_memoria()
    
    input("\n⏸️  Pressione ENTER para ver chatbot COM memória...")
    exemplo_com_memoria()
    
    input("\n⏸️  Pressione ENTER para ver localização do storage...")
    verificar_storage()
    
    print("\n" + "=" * 70)
    print("✅ EXEMPLO CONCLUÍDO!")
    print("=" * 70)
    print("\n💡 Próximo passo: uv run aula11/exemplos/02_knowledge_pdf.py")
