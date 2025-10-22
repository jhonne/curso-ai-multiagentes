#!/usr/bin/env python3
"""
Exercício 1: Chatbot com Memória

OBJETIVO: Criar um chatbot médico que mantém contexto entre conversas.

REQUISITOS:
1. Agente que lembra de sintomas mencionados anteriormente
2. Fazer perguntas de acompanhamento baseadas no histórico
3. Testar short-term memory
4. Verificar storage path

DIFICULDADE: 🟢 Básico

Execute: uv run aula11/exercicios/exercicio1_chatbot_memoria.py
"""

import os
import sys
from dotenv import load_dotenv
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# ✅ Configurar storage ANTES de importar CrewAI
load_dotenv()
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from setup_storage import configurar_storage
config = configurar_storage(__file__)

# ✅ AGORA importar CrewAI
from crewai import Agent, Task, Crew, Process, LLM
from crewai.utilities.paths import db_storage_path

load_dotenv()


def criar_chatbot_medico():
    """
    TODO: Criar um chatbot médico com memória.
    
    O chatbot deve:
    - Lembrar de todos os sintomas mencionados
    - Fazer perguntas de acompanhamento relevantes
    - Manter contexto entre múltiplas conversas
    """
    
    llm = LLM(model="gpt-4o-mini", temperature=0.7)
    
    # TODO: Criar agente com role, goal e backstory apropriados
    # Dica: O backstory deve mencionar que ele tem "memória fotográfica"
    agente = Agent(
        role="COMPLETE AQUI",  # Ex: "Médico Virtual"
        goal="COMPLETE AQUI",  # Ex: "Atender pacientes lembrando..."
        backstory="""COMPLETE AQUI
        Dica: Mencione que o médico lembra de todas as conversas
        e sempre faz referência ao histórico do paciente.
        """,
        llm=llm,
        verbose=False
    )
    
    # TODO: Criar tarefa para conversar com paciente
    tarefa = Task(
        description="COMPLETE AQUI: {mensagem}",
        expected_output="COMPLETE AQUI",
        agent=agente
    )
    
    # TODO: Criar crew COM MEMÓRIA HABILITADA
    crew = Crew(
        agents=[agente],
        tasks=[tarefa],
        memory=False,  # TODO: Mudar para True!
        process=Process.sequential,
        verbose=False
    )
    
    return crew


def testar_chatbot():
    """Testa o chatbot com uma conversa simulada"""
    print("\n" + "=" * 70)
    print("🧪 TESTANDO CHATBOT COM MEMÓRIA")
    print("=" * 70)
    
    crew = criar_chatbot_medico()
    
    # Conversa simulada
    conversas = [
        "Olá, estou com dor de cabeça desde ontem",
        "A dor é moderada, na região frontal",
        "Sim, também estou com um pouco de febre",
        "Pode me resumir todos os sintomas que mencionei?"
    ]
    
    print("\n💬 CONVERSA:\n")
    
    for i, mensagem in enumerate(conversas, 1):
        print(f"👤 Paciente: {mensagem}")
        
        # TODO: Executar crew com a mensagem
        # resultado = crew.kickoff(inputs={"mensagem": mensagem})
        # print(f"🤖 Médico: {resultado.raw}\n")
        
        print("🤖 Médico: [IMPLEMENTE O CHATBOT PARA VER A RESPOSTA]\n")
        
        if i < len(conversas):
            input("   ⏸️  ENTER para continuar...")
    
    # TODO: Verificar se o agente lembrou de TODOS os sintomas na última pergunta
    print("\n✅ OBJETIVO: Na última resposta, o médico deve listar:")
    print("   - Dor de cabeça (frontal, moderada)")
    print("   - Febre")


def verificar_storage():
    """Verifica onde a memória está sendo salva"""
    print("\n" + "=" * 70)
    print("📁 VERIFICANDO STORAGE")
    print("=" * 70)
    
    storage = db_storage_path()
    print(f"\n💾 Storage path: {storage}\n")
    
    if os.path.exists(storage):
        print("✅ Storage criado! Conteúdo:")
        for item in os.listdir(storage):
            print(f"   └── {item}")
    else:
        print("❌ Storage ainda não criado")
        print("   Execute o chatbot com memory=True primeiro")


def solucao_completa():
    """
    GABARITO: Solução completa do exercício.
    Só olhe depois de tentar implementar!
    """
    print("\n" + "=" * 70)
    print("✅ GABARITO - SOLUÇÃO COMPLETA")
    print("=" * 70)
    
    llm = LLM(model="gpt-4o-mini", temperature=0.7)
    
    agente = Agent(
        role="Médico Virtual",
        goal="Atender pacientes lembrando de todo o histórico de conversas",
        backstory="""Você é um médico virtual experiente com memória fotográfica.
        Sempre se lembra de todos os sintomas mencionados pelo paciente
        e faz referência a conversas anteriores.
        Faz perguntas de acompanhamento relevantes.""",
        llm=llm,
        verbose=False
    )
    
    tarefa = Task(
        description="Converse com o paciente sobre: {mensagem}",
        expected_output="Resposta empática e contextualizada",
        agent=agente
    )
    
    crew = Crew(
        agents=[agente],
        tasks=[tarefa],
        memory=True,  # ✅ Memória habilitada!
        process=Process.sequential,
        verbose=False
    )
    
    # Teste
    conversas = [
        "Olá, estou com dor de cabeça desde ontem",
        "A dor é moderada, na região frontal",
        "Sim, também estou com um pouco de febre",
        "Pode me resumir todos os sintomas que mencionei?"
    ]
    
    print("\n💬 CONVERSA COM SOLUÇÃO:\n")
    
    for mensagem in conversas:
        print(f"👤 Paciente: {mensagem}")
        resultado = crew.kickoff(inputs={"mensagem": mensagem})
        print(f"🤖 Médico: {resultado.raw}\n")
        input("   ⏸️  ENTER...")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY não configurada")
        sys.exit(1)
    
    print("\n🎓 EXERCÍCIO 1: CHATBOT COM MEMÓRIA")
    print("\n📝 Complete o código nos locais marcados com TODO")
    
    escolha = input("\n1. Testar minha implementação\n2. Ver gabarito\n\nEscolha: ")
    
    if escolha == "1":
        testar_chatbot()
        input("\n⏸️  ENTER para verificar storage...")
        verificar_storage()
    elif escolha == "2":
        solucao_completa()
    else:
        print("❌ Opção inválida")
