#!/usr/bin/env python3
"""
Exemplo 3: RAG Simples

Demonstra RAG básico combinando Memory + Knowledge.
Um sistema que lembra do histórico E consulta protocolos.

Execute: uv run aula11/exemplos/03_rag_simples.py
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
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

load_dotenv()


def criar_base_conhecimento():
    """Cria knowledge base com informações médicas"""
    conhecimento = """
    PROTOCOLOS MÉDICOS - SISTEMA DE TRIAGEM
    
    SINTOMAS DE EMERGÊNCIA (VERMELHO):
    - Dor no peito com irradiação para braço/mandíbula
    - Falta de ar severa com cianose
    - Perda de consciência
    - Convulsões
    - Hemorragia intensa
    
    SINTOMAS MUITO URGENTES (LARANJA):
    - Dor no peito moderada a intensa
    - Febre alta com rigidez de nuca
    - Dificuldade respiratória moderada
    - Alteração de comportamento súbita
    
    ORIENTAÇÕES GERAIS:
    - Sempre pergunte sobre histórico médico
    - Considere idade e condições pré-existentes
    - Em dúvida, classifique para urgência maior
    - Documente todos os sintomas relatados
    """
    
    return StringKnowledgeSource(content=conhecimento)


def exemplo_rag_consulta_unica():
    """RAG com consulta única - Memory + Knowledge"""
    print("\n" + "=" * 70)
    print("🎯 RAG SIMPLES - Consulta Única")
    print("=" * 70)
    
    llm = LLM(model="gpt-4o-mini", temperature=0.5)
    conhecimento = criar_base_conhecimento()
    
    agente = Agent(
        role="Assistente Médico Virtual",
        goal="Avaliar pacientes usando protocolos e lembrando do histórico",
        backstory="""Assistente treinado em triagem médica.
        Tem acesso a protocolos e lembra de todos os pacientes.""",
        llm=llm,
        verbose=False
    )
    
    tarefa = Task(
        description="""Avalie o paciente {nome} com sintomas: {sintomas}
        
        Consulte os protocolos e forneça:
        1. Classificação de urgência
        2. Perguntas adicionais relevantes
        3. Orientações iniciais""",
        expected_output="Avaliação completa do caso",
        agent=agente
    )
    
    crew = Crew(
        agents=[agente],
        tasks=[tarefa],
        memory=True,  # 🧠 Memória
        knowledge_sources=[conhecimento],  # 📚 Protocolos
        process=Process.sequential,
        verbose=False
    )
    
    print("\n👤 Paciente: Carlos Silva")
    print("🩺 Sintomas: Dor no peito há 30 minutos\n")
    
    resultado = crew.kickoff(inputs={
        "nome": "Carlos Silva",
        "sintomas": "dor no peito há 30 minutos"
    })
    
    print(f"💬 Avaliação:\n{resultado.raw}\n")
    print("✨ Sistema usou protocolos para classificar!")


def exemplo_rag_conversacional():
    """RAG conversacional - Múltiplas interações com memória"""
    print("\n" + "=" * 70)
    print("💬 RAG CONVERSACIONAL - Múltiplas Interações")
    print("=" * 70)
    
    llm = LLM(model="gpt-4o-mini", temperature=0.5)
    conhecimento = criar_base_conhecimento()
    
    agente = Agent(
        role="Triagista Virtual",
        goal="Coletar informações e classificar urgência",
        backstory="""Triagista experiente que conversa com pacientes.
        Faz perguntas relevantes e lembra de todas as respostas.""",
        llm=llm,
        verbose=False
    )
    
    tarefa = Task(
        description="Responda ao paciente: {mensagem}",
        expected_output="Resposta contextualizada",
        agent=agente
    )
    
    crew = Crew(
        agents=[agente],
        tasks=[tarefa],
        memory=True,  # 🧠 Lembra de tudo!
        knowledge_sources=[conhecimento],  # 📚 Consulta protocolos!
        process=Process.sequential,
        verbose=False
    )
    
    # Conversa simulada
    conversas = [
        ("Olá, estou com dor no peito", "👤 Paciente"),
        ("A dor começou há 1 hora e irradia para o braço esquerdo", "👤 Paciente"),
        ("Sim, estou suando muito e com falta de ar", "👤 Paciente"),
        ("Tenho histórico de pressão alta", "👤 Paciente")
    ]
    
    print("\n🗣️  CONVERSA INTERATIVA:\n")
    
    for mensagem, autor in conversas:
        print(f"{autor}: {mensagem}")
        resultado = crew.kickoff(inputs={"mensagem": mensagem})
        print(f"🤖 Triagista: {resultado.raw}\n")
        input("   ⏸️  ENTER para continuar...")
    
    print("\n✨ Observe como o triagista:")
    print("   🧠 LEMBROU de todos os sintomas anteriores")
    print("   📚 CONSULTOU protocolos para classificar")
    print("   🎯 RECONHECEU sinais de emergência (VERMELHO)")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY não configurada")
        sys.exit(1)
    
    print("\n🎓 EXEMPLO 3: RAG SIMPLES")
    print("\nDemonstração de Memory + Knowledge trabalhando juntos\n")
    
    input("⏸️  Pressione ENTER para consulta única...")
    exemplo_rag_consulta_unica()
    
    input("\n⏸️  Pressione ENTER para modo conversacional...")
    exemplo_rag_conversacional()
    
    print("\n" + "=" * 70)
    print("✅ EXEMPLO CONCLUÍDO!")
    print("=" * 70)
    print("\n💡 Próximo: uv run aula11/exemplos/04_sistema_completo.py")
