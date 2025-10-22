#!/usr/bin/env python3
"""
Exercício 2: Knowledge Base Médica

OBJETIVO: Criar agente que consulta protocolos médicos para classificação.

REQUISITOS:
1. Criar knowledge source com protocolos de triagem
2. Agente que consulta protocolos antes de classificar
3. Comparar respostas COM e SEM knowledge
4. Testar com múltiplos casos

DIFICULDADE: 🟡 Intermediário

Execute: uv run aula11/exercicios/exercicio2_knowledge_base.py
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
from crewai.knowledge.source.string_knowledge_source import (
    StringKnowledgeSource
)

load_dotenv()


def criar_protocolo_triagem():
    """
    TODO: Criar knowledge source com protocolos de triagem.
    
    Inclua pelo menos:
    - Classificação de cores (Vermelho, Laranja, Amarelo, Verde, Azul)
    - Tempos de espera
    - Critérios para cada classificação
    """
    
    # TODO: Complete o protocolo abaixo
    protocolo = """
    PROTOCOLOS DE TRIAGEM
    
    TODO: Adicione aqui as classificações completas
    
    VERMELHO (Emergência):
    - TODO: Liste condições de emergência
    
    LARANJA (Muito Urgente):
    - TODO: Liste condições muito urgentes
    
    AMARELO (Urgente):
    - TODO: Liste condições urgentes
    
    VERDE (Pouco Urgente):
    - TODO: Liste condições pouco urgentes
    """
    
    return StringKnowledgeSource(content=protocolo)


def criar_agente_sem_knowledge():
    """Agente SEM acesso a protocolos"""
    
    llm = LLM(model="gpt-4o-mini", temperature=0.3)
    
    # TODO: Criar agente básico
    agente = Agent(
        role="COMPLETE AQUI",
        goal="Classificar urgência sem protocolos formais",
        backstory="COMPLETE AQUI",
        llm=llm,
        verbose=False
    )
    
    tarefa = Task(
        description="Classifique a urgência: {sintomas}",
        expected_output="Classificação básica",
        agent=agente
    )
    
    crew = Crew(
        agents=[agente],
        tasks=[tarefa],
        # TODO: NÃO adicionar knowledge_sources aqui!
        process=Process.sequential,
        verbose=False
    )
    
    return crew


def criar_agente_com_knowledge():
    """Agente COM acesso a protocolos"""
    
    llm = LLM(model="gpt-4o-mini", temperature=0.3)
    
    # TODO: Obter knowledge source
    protocolo = criar_protocolo_triagem()
    
    # TODO: Criar agente especializado
    agente = Agent(
        role="COMPLETE AQUI",  # Ex: "Enfermeiro de Triagem"
        goal="COMPLETE AQUI",
        backstory="""COMPLETE AQUI
        Dica: Mencione que o enfermeiro segue protocolos oficiais
        """,
        llm=llm,
        verbose=False
    )
    
    # TODO: Criar tarefa que pede para consultar protocolos
    tarefa = Task(
        description="""COMPLETE AQUI: {sintomas}
        
        Consulte os protocolos e forneça:
        1. Cor de classificação
        2. Tempo de espera
        3. Justificativa baseada no protocolo
        """,
        expected_output="COMPLETE AQUI",
        agent=agente
    )
    
    # TODO: Criar crew COM knowledge_sources
    crew = Crew(
        agents=[agente],
        tasks=[tarefa],
        knowledge_sources=[],  # TODO: Adicionar protocolo aqui!
        process=Process.sequential,
        verbose=False
    )
    
    return crew


def comparar_resultados():
    """Compara agente SEM vs COM knowledge"""
    print("\n" + "=" * 70)
    print("🔬 COMPARAÇÃO: SEM vs COM KNOWLEDGE")
    print("=" * 70)
    
    sintomas = "dor no peito intensa, falta de ar, sudorese"
    
    print(f"\n🩺 Sintomas: {sintomas}\n")
    
    # SEM knowledge
    print("❌ AGENTE SEM KNOWLEDGE:")
    print("-" * 70)
    # TODO: Implementar
    print("[IMPLEMENTE PARA VER RESULTADO]\n")
    
    # COM knowledge
    print("✅ AGENTE COM KNOWLEDGE:")
    print("-" * 70)
    # TODO: Implementar
    print("[IMPLEMENTE PARA VER RESULTADO]\n")
    
    print("🎯 OBJETIVO: O agente COM knowledge deve:")
    print("   - Classificar como VERMELHO (emergência)")
    print("   - Justificar baseado em protocolos")
    print("   - Mencionar tempo de atendimento imediato")


def testar_multiplos_casos():
    """Testa agente com knowledge em vários casos"""
    print("\n" + "=" * 70)
    print("🧪 TESTANDO MÚLTIPLOS CASOS")
    print("=" * 70)
    
    casos = [
        "dor leve no joelho há 3 dias",
        "febre 39°C com tosse e falta de ar",
        "renovação de receita médica"
    ]
    
    # TODO: Criar agente com knowledge
    # crew = criar_agente_com_knowledge()
    
    for i, caso in enumerate(casos, 1):
        print(f"\n📋 Caso {i}: {caso}")
        print("-" * 70)
        
        # TODO: Executar classificação
        print("[IMPLEMENTE PARA VER RESULTADO]")


def solucao_completa():
    """GABARITO: Solução completa"""
    print("\n" + "=" * 70)
    print("✅ GABARITO")
    print("=" * 70)
    
    # Knowledge completo
    protocolo = StringKnowledgeSource(content="""
    PROTOCOLO DE TRIAGEM - SISTEMA MANCHESTER
    
    🔴 VERMELHO - Emergência (IMEDIATO)
    - Parada cardiorrespiratória
    - Dor torácica com sinais de IAM
    - Inconsciência
    - Choque
    
    🟠 LARANJA - Muito Urgente (10 min)
    - Dor torácica intensa
    - Dispneia severa
    - Sangramento moderado
    
    🟡 AMARELO - Urgente (60 min)
    - Febre alta persistente
    - Dor moderada
    - Vômitos/diarreia
    
    🟢 VERDE - Pouco Urgente (120 min)
    - Sintomas leves
    - Condições crônicas estáveis
    
    🔵 AZUL - Não Urgente (240 min)
    - Problemas administrativos
    - Renovação de receitas
    """)
    
    llm = LLM(model="gpt-4o-mini", temperature=0.3)
    
    agente = Agent(
        role="Enfermeiro de Triagem",
        goal="Classificar urgência baseado em protocolos oficiais",
        backstory="Especialista em triagem de Manchester.",
        llm=llm,
        verbose=False
    )
    
    tarefa = Task(
        description="""Classifique: {sintomas}
        Consulte protocolos e forneça: cor, tempo, justificativa""",
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
    
    # Teste
    sintomas = "dor no peito intensa, falta de ar, sudorese"
    print(f"\n🩺 Sintomas: {sintomas}\n")
    resultado = crew.kickoff(inputs={"sintomas": sintomas})
    print(f"💬 Classificação:\n{resultado.raw}")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY não configurada")
        sys.exit(1)
    
    print("\n🎓 EXERCÍCIO 2: KNOWLEDGE BASE MÉDICA")
    print("\n📝 Complete o código nos locais marcados com TODO")
    
    escolha = input("\n1. Comparar SEM vs COM knowledge\n2. Testar múltiplos casos\n3. Ver gabarito\n\nEscolha: ")
    
    if escolha == "1":
        comparar_resultados()
    elif escolha == "2":
        testar_multiplos_casos()
    elif escolha == "3":
        solucao_completa()
    else:
        print("❌ Opção inválida")
