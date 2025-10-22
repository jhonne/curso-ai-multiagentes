"""
Exercício Rápido - RAG em 10 Minutos
Crie um chatbot médico com Memory + Knowledge
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ✅ Configurar storage ANTES de importar CrewAI
load_dotenv()

# ✅ AGORA importar CrewAI (usa a config acima)
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# ✅ Configurar storage ANTES de importar CrewAI
load_dotenv()
from setup_storage import configurar_storage
config = configurar_storage(__file__)

# ✅ AGORA importar CrewAI
from crewai import Agent, Task, Crew, LLM
from crewai.knowledge.source.string_knowledge_source import (
    StringKnowledgeSource
)


def criar_protocolo():
    """Cria protocolo médico básico"""
    return """
    PROTOCOLO DE SINTOMAS COMUNS:
    
    FEBRE:
    - Febre >39°C: Urgente (atendimento em 1h)
    - Febre 38-39°C: Moderado (atendimento em 2h)
    - Febre <38°C: Leve (orientação)
    
    DOR DE CABEÇA:
    - Com rigidez de nuca: Emergência
    - Enxaqueca forte: Urgente
    - Leve: Orientação domiciliar
    
    TOSSE:
    - Com falta de ar: Urgente
    - Persistente >7 dias: Consulta
    - Leve/recente: Orientação
    """


def exercicio():
    """
    TODO: Complete o código abaixo para criar um chatbot que:
    1. LEMBRA do nome e idade do paciente (memory)
    2. CONSULTA protocolos médicos (knowledge)
    3. FORNECE orientação personalizada (RAG)
    """
    
    print("\n" + "="*60)
    print("EXERCÍCIO: CHATBOT MÉDICO COM RAG")
    print("="*60)
    
    # TODO 1: Criar knowledge source com o protocolo
    protocolo = criar_protocolo()
    knowledge = None  # TODO: Criar StringKnowledgeSource
    
    # TODO 2: Criar LLM
    llm = None  # TODO: LLM(model="gpt-4o-mini", temperature=0.1)
    
    # TODO 3: Criar agente com role apropriado
    agente = None
    # TODO: Agent(
    #     role="Médico Virtual",
    #     goal="Atender pacientes com empatia e protocolo",
    #     backstory="Médico que consulta protocolos e lembra dos pacientes.",
    #     llm=llm
    # )
    
    # TODO 4: Criar tarefa
    tarefa = None
    # TODO: Task(
    #     description="Atenda o paciente: {mensagem}",
    #     expected_output="Orientação médica personalizada",
    #     agent=agente
    # )
    
    # TODO 5: Criar crew com memory=True e knowledge_sources
    crew = None
    # TODO: Crew(
    #     agents=[agente],
    #     tasks=[tarefa],
    #     memory=???,  # True ou False?
    #     knowledge_sources=???,  # Lista com knowledge
    #     verbose=False
    # )
    
    # Teste do chatbot
    print("\n🧪 TESTANDO CHATBOT...\n")
    
    if crew is None:
        print("❌ Complete os TODOs primeiro!")
        return
    
    # Conversa 1
    print("👤 Paciente: 'Olá, sou Maria, 35 anos'")
    r1 = crew.kickoff(inputs={"mensagem": "Olá, sou Maria, 35 anos"})
    print(f"🤖 Chatbot: {r1.raw}\n")
    
    # Conversa 2
    print("👤 Paciente: 'Estou com febre de 39.5°C'")
    r2 = crew.kickoff(inputs={"mensagem": "Estou com febre de 39.5°C"})
    print(f"🤖 Chatbot: {r2.raw}\n")
    
    # Verificação
    print("\n" + "="*60)
    print("VERIFICAÇÃO:")
    print("="*60)
    print("✅ Chatbot lembrou do nome 'Maria'?")
    print("✅ Chatbot consultou protocolo de febre >39°C?")
    print("✅ Chatbot recomendou 'Urgente (1h)'?")
    print("\nSe SIM para todas, você completou com sucesso! 🎉")


def solucao():
    """Solução completa do exercício"""
    
    print("\n" + "="*60)
    print("GABARITO - SOLUÇÃO COMPLETA")
    print("="*60 + "\n")
    
    # Solução 1: Knowledge source
    protocolo = criar_protocolo()
    knowledge = StringKnowledgeSource(content=protocolo)
    
    # Solução 2: LLM
    llm = LLM(model="gpt-4o-mini", temperature=0.1)
    
    # Solução 3: Agente
    agente = Agent(
        role="Médico Virtual",
        goal="Atender pacientes com empatia consultando protocolos",
        backstory="""Médico experiente que sempre consulta protocolos
        oficiais e lembra de cada paciente.""",
        llm=llm
    )
    
    # Solução 4: Tarefa
    tarefa = Task(
        description="Atenda o paciente: {mensagem}",
        expected_output="Orientação médica personalizada e fundamentada",
        agent=agente
    )
    
    # Solução 5: Crew com RAG
    crew = Crew(
        agents=[agente],
        tasks=[tarefa],
        memory=True,  # 🧠 Memory ativado
        knowledge_sources=[knowledge],  # 📚 Knowledge ativado
        verbose=False
    )
    
    # Teste
    print("🧪 TESTANDO SOLUÇÃO...\n")
    
    print("👤 Paciente: 'Sou Pedro, 28 anos, com tosse e falta de ar'")
    r1 = crew.kickoff(
        inputs={"mensagem": "Sou Pedro, 28 anos, com tosse e falta de ar"}
    )
    print(f"🤖 Chatbot: {r1.raw}\n")
    
    print("👤 Paciente: 'Quanto tempo devo esperar?'")
    r2 = crew.kickoff(inputs={"mensagem": "Quanto tempo devo esperar?"})
    print(f"🤖 Chatbot: {r2.raw}\n")
    
    print("✅ SOLUÇÃO FUNCIONANDO!")
    print("\nObserve como o chatbot:")
    print("1. 🧠 LEMBROU do nome 'Pedro' na segunda mensagem")
    print("2. 📚 CONSULTOU protocolo (tosse + falta de ar = Urgente)")
    print("3. 🚀 COMBINOU tudo em resposta personalizada!")


def main():
    """Menu principal"""
    
    print("\n" + "="*60)
    print("EXERCÍCIO RÁPIDO - RAG EM 10 MINUTOS")
    print("="*60)
    
    print("""
Escolha uma opção:

1. 💪 Fazer exercício (10 min)
2. 👀 Ver gabarito direto
3. 🚪 Sair
    """)
    
    escolha = input("Opção: ").strip()
    
    if escolha == "1":
        print("\n📝 EXERCÍCIO:")
        print("Complete os TODOs no código acima e execute novamente.\n")
        exercicio()
    elif escolha == "2":
        solucao()
    else:
        print("👋 Até logo!")


if __name__ == "__main__":
    main()
