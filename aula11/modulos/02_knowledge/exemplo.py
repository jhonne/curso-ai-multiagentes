#!/usr/bin/env python3
"""
Exemplo 2: Knowledge Sources

Demonstra como carregar e usar documentos externos como
base de conhecimento para agentes.

Execute: uv run aula11/exemplos/02_knowledge_pdf.py
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


def criar_protocolo_triagem():
    """Cria knowledge source com protocolo de triagem"""
    protocolo = """
    PROTOCOLO DE TRIAGEM - SISTEMA MANCHESTER
    
    CLASSIFICAÇÃO POR COR E TEMPO:
    
    🔴 VERMELHO - Emergência (IMEDIATO)
    - Parada cardiorrespiratória
    - Dor torácica com sinais de IAM
    - Hemorragia grave não controlada
    - Inconsciência ou coma
    - Choque
    
    🟠 LARANJA - Muito Urgente (10 minutos)
    - Dor torácica intensa
    - Dificuldade respiratória severa
    - Alteração do nível de consciência
    - Dor intensa (escore 8-10)
    - Sangramento moderado
    
    🟡 AMARELO - Urgente (60 minutos)
    - Dor moderada (escore 5-7)
    - Febre alta sem sinais de gravidade
    - Vômitos persistentes
    - Diarreia com desidratação leve
    
    🟢 VERDE - Pouco Urgente (120 minutos)
    - Sintomas leves
    - Dor leve (escore 1-4)
    - Problemas crônicos estáveis
    
    🔵 AZUL - Não Urgente (240 minutos)
    - Problemas administrativos
    - Consultas de rotina
    - Renovação de receitas
    """
    
    return StringKnowledgeSource(content=protocolo)


def exemplo_sem_knowledge():
    """Agente SEM acesso a protocolos"""
    print("\n" + "=" * 70)
    print("❌ AGENTE SEM KNOWLEDGE")
    print("=" * 70)
    
    llm = LLM(model="gpt-4o-mini", temperature=0.3)
    
    agente = Agent(
        role="Atendente Básico",
        goal="Avaliar urgência do paciente",
        backstory="Atendente sem acesso a protocolos formais.",
        llm=llm,
        verbose=False
    )
    
    tarefa = Task(
        description="""Classifique a urgência do paciente: {sintomas}
        Dê uma classificação básica.""",
        expected_output="Classificação de urgência",
        agent=agente
    )
    
    crew = Crew(
        agents=[agente],
        tasks=[tarefa],
        process=Process.sequential,
        verbose=False
    )
    
    print("\n🩺 Sintomas: Dor forte no peito, falta de ar, sudorese")
    resultado = crew.kickoff(inputs={
        "sintomas": "dor forte no peito, falta de ar, sudorese"
    })
    print(f"\n💬 Resposta: {resultado.raw}\n")
    print("⚠️  Resposta genérica, sem base em protocolos!")


def exemplo_com_knowledge():
    """Agente COM acesso a protocolos"""
    print("\n" + "=" * 70)
    print("✅ AGENTE COM KNOWLEDGE (PROTOCOLOS)")
    print("=" * 70)
    
    llm = LLM(model="gpt-4o-mini", temperature=0.3)
    
    # Criar knowledge source
    protocolo = criar_protocolo_triagem()
    
    agente = Agent(
        role="Enfermeiro de Triagem",
        goal="Classificar urgência baseado em protocolos oficiais",
        backstory="""Enfermeiro especializado em triagem.
        Segue rigorosamente os protocolos de Manchester.""",
        llm=llm,
        verbose=False
    )
    
    tarefa = Task(
        description="""Classifique a urgência: {sintomas}
        
        Consulte os protocolos e forneça:
        1. Cor de classificação
        2. Tempo de espera
        3. Justificativa baseada no protocolo""",
        expected_output="Classificação completa com justificativa",
        agent=agente
    )
    
    crew = Crew(
        agents=[agente],
        tasks=[tarefa],
        knowledge_sources=[protocolo],  # 📚 Protocolos disponíveis!
        process=Process.sequential,
        verbose=False
    )
    
    print("\n🩺 Sintomas: Dor forte no peito, falta de ar, sudorese")
    resultado = crew.kickoff(inputs={
        "sintomas": "dor forte no peito, falta de ar, sudorese"
    })
    print(f"\n💬 Resposta: {resultado.raw}\n")
    print("✨ Resposta FUNDAMENTADA no protocolo!")


def testar_multiplos_casos():
    """Testa múltiplos casos com knowledge"""
    print("\n" + "=" * 70)
    print("🧪 TESTANDO MÚLTIPLOS CASOS")
    print("=" * 70)
    
    llm = LLM(model="gpt-4o-mini", temperature=0.3)
    protocolo = criar_protocolo_triagem()
    
    agente = Agent(
        role="Enfermeiro de Triagem",
        goal="Classificar urgência com precisão",
        backstory="Especialista em triagem de Manchester.",
        llm=llm,
        verbose=False
    )
    
    tarefa = Task(
        description="""Classifique: {sintomas}
        Forneça: cor, tempo de espera, justificativa""",
        expected_output="Classificação fundamentada",
        agent=agente
    )
    
    crew = Crew(
        agents=[agente],
        tasks=[tarefa],
        knowledge_sources=[protocolo],
        process=Process.sequential,
        verbose=False
    )
    
    casos = [
        "dor leve no joelho há 3 dias",
        "febre 39°C, tosse, falta de ar moderada",
        "renovação de receita de remédio de pressão"
    ]
    
    for i, caso in enumerate(casos, 1):
        print(f"\n📋 Caso {i}: {caso}")
        print("-" * 70)
        resultado = crew.kickoff(inputs={"sintomas": caso})
        print(f"💬 {resultado.raw}")
        
        if i < len(casos):
            input("\n   ⏸️  ENTER para próximo caso...")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY não configurada")
        sys.exit(1)
    
    print("\n🎓 EXEMPLO 2: KNOWLEDGE SOURCES")
    print("\nVamos comparar agente SEM vs COM acesso a protocolos\n")
    
    input("⏸️  Pressione ENTER para ver agente SEM knowledge...")
    exemplo_sem_knowledge()
    
    input("\n⏸️  Pressione ENTER para ver agente COM knowledge...")
    exemplo_com_knowledge()
    
    input("\n⏸️  Pressione ENTER para testar múltiplos casos...")
    testar_multiplos_casos()
    
    print("\n" + "=" * 70)
    print("✅ EXEMPLO CONCLUÍDO!")
    print("=" * 70)
    print("\n💡 Próximo: uv run aula11/exemplos/03_rag_simples.py")
