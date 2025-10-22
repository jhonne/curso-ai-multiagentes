#!/usr/bin/env python3
"""
Exercício 3: Sistema RAG Completo

OBJETIVO: Criar sistema de triagem end-to-end integrando TUDO.

REQUISITOS:
1. Integrar embeddings da Aula 10 (busca semântica)
2. Habilitar memory system
3. Criar knowledge base customizada
4. Sistema completo com múltiplos agentes

DIFICULDADE: 🔴 Avançado

Execute: uv run aula11/exercicios/exercicio3_rag_completo.py
"""

import os
import sys
from pathlib import Path
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

# TODO: Importar busca semântica da Aula 10
# sys.path.append(str(Path(__file__).parent.parent.parent))
# from aula10.main import BuscaSemantica, EmbeddingManager

load_dotenv()


def criar_base_conhecimento_completa():
    """
    TODO: Criar knowledge base completa com:
    - Protocolos de triagem
    - Sinais de alerta
    - Fatores agravantes
    - Orientações de encaminhamento
    """
    
    conhecimento = """
    TODO: Complete com conhecimento médico completo
    
    === PROTOCOLOS DE TRIAGEM ===
    (adicione aqui)
    
    === SINAIS DE ALERTA ===
    (adicione aqui)
    
    === FATORES AGRAVANTES ===
    (adicione aqui)
    
    === ORIENTAÇÕES DE ENCAMINHAMENTO ===
    (adicione aqui)
    """
    
    return StringKnowledgeSource(content=conhecimento)


def criar_sistema_rag_completo():
    """
    TODO: Criar sistema RAG completo com 3 agentes:
    
    1. Recepcionista (coleta informações)
    2. Triagista (classifica urgência)
    3. Coordenador (recomenda encaminhamento)
    
    O sistema deve:
    - Ter memória habilitada (lembrar de tudo)
    - Consultar knowledge base
    - Usar busca semântica (opcional avançado)
    """
    
    llm = LLM(model="gpt-4o-mini", temperature=0.5)
    conhecimento = criar_base_conhecimento_completa()
    
    # TODO: AGENTE 1 - Recepcionista
    recepcionista = Agent(
        role="COMPLETE AQUI",
        goal="COMPLETE AQUI",
        backstory="COMPLETE AQUI",
        llm=llm,
        verbose=False
    )
    
    # TODO: AGENTE 2 - Triagista
    triagista = Agent(
        role="COMPLETE AQUI",
        goal="COMPLETE AQUI",
        backstory="COMPLETE AQUI",
        llm=llm,
        verbose=False
    )
    
    # TODO: AGENTE 3 - Coordenador
    coordenador = Agent(
        role="COMPLETE AQUI",
        goal="COMPLETE AQUI",
        backstory="COMPLETE AQUI",
        llm=llm,
        verbose=False
    )
    
    # TODO: TAREFA 1 - Coleta de informações
    coleta = Task(
        description="COMPLETE AQUI: {paciente_info}",
        expected_output="COMPLETE AQUI",
        agent=recepcionista
    )
    
    # TODO: TAREFA 2 - Classificação de urgência
    classificacao = Task(
        description="COMPLETE AQUI",
        expected_output="COMPLETE AQUI",
        agent=triagista,
        context=[]  # TODO: Adicionar contexto (coleta)
    )
    
    # TODO: TAREFA 3 - Encaminhamento
    encaminhamento = Task(
        description="COMPLETE AQUI",
        expected_output="COMPLETE AQUI",
        agent=coordenador,
        context=[]  # TODO: Adicionar contexto (coleta, classificacao)
    )
    
    # TODO: CREW COMPLETA
    crew = Crew(
        agents=[],  # TODO: Adicionar agentes
        tasks=[],  # TODO: Adicionar tarefas
        memory=False,  # TODO: Habilitar memória
        knowledge_sources=[],  # TODO: Adicionar conhecimento
        process=Process.sequential,
        verbose=True
    )
    
    return crew


def testar_caso_emergencia():
    """Testa com caso de emergência"""
    print("\n" + "=" * 70)
    print("🚨 CASO DE EMERGÊNCIA")
    print("=" * 70)
    
    # TODO: Criar sistema
    # crew = criar_sistema_rag_completo()
    
    caso = {
        "nome": "José Santos, 65 anos",
        "sintomas": "dor forte no peito há 30 minutos",
        "detalhes": "dor irradia para braço, sudorese, falta de ar",
        "historico": "hipertenso, diabético"
    }
    
    print(f"\n👤 {caso['nome']}")
    print(f"🩺 {caso['sintomas']}")
    print(f"📝 {caso['detalhes']}")
    print(f"📋 {caso['historico']}\n")
    
    # TODO: Executar sistema
    print("[IMPLEMENTE O SISTEMA PARA VER RESULTADO]")
    
    print("\n🎯 OBJETIVO: Sistema deve classificar como:")
    print("   🔴 VERMELHO (Emergência)")
    print("   🏥 Encaminhar para HOSPITAL com UTI")
    print("   ⏱️  Atendimento IMEDIATO")


def testar_integracao_embeddings():
    """
    DESAFIO AVANÇADO: Integrar com embeddings da Aula 10
    
    Use busca semântica para:
    1. Encontrar sintomas similares no banco
    2. Buscar estabelecimentos apropriados
    3. Recomendar baseado em casos similares
    """
    print("\n" + "=" * 70)
    print("🚀 DESAFIO: INTEGRAÇÃO COM EMBEDDINGS (Aula 10)")
    print("=" * 70)
    
    print("""
    TODO: Integrar com a Aula 10
    
    Passos:
    1. Importar BuscaSemantica e EmbeddingManager
    2. Criar tool customizada que usa busca semântica
    3. Adicionar tool ao agente recomendador
    4. Usar embeddings para encontrar casos similares
    
    Exemplo de uso:
    - Paciente relata "dor no peito"
    - Sistema busca semanticamente sintomas relacionados
    - Encontra: "precordialgia", "angina", "IAM"
    - Classifica com mais precisão
    """)
    
    print("\n[IMPLEMENTE PARA COMPLETAR O DESAFIO]")


def solucao_completa():
    """GABARITO: Solução completa end-to-end"""
    print("\n" + "=" * 70)
    print("✅ GABARITO - SISTEMA RAG COMPLETO")
    print("=" * 70)
    
    conhecimento = StringKnowledgeSource(content="""
    SISTEMA DE TRIAGEM MÉDICA COMPLETO
    
    === CLASSIFICAÇÃO ===
    🔴 VERMELHO: Parada, IAM, AVC, Choque
    🟠 LARANJA: Dor torácica intensa, dispneia severa
    🟡 AMARELO: Febre alta, dor moderada
    🟢 VERDE: Sintomas leves
    🔵 AZUL: Administrativo
    
    === ENCAMINHAMENTO ===
    VERMELHO → Hospital com UTI
    LARANJA → Hospital ou UPA 24h
    AMARELO → UPA ou Pronto Atendimento
    VERDE → UBS ou Pronto Atendimento
    AZUL → UBS
    """)
    
    llm = LLM(model="gpt-4o-mini", temperature=0.5)
    
    recepcionista = Agent(
        role="Recepcionista Virtual",
        goal="Coletar informações completas do paciente",
        backstory="Experiente, empática, detalhista.",
        llm=llm,
        verbose=False
    )
    
    triagista = Agent(
        role="Enfermeiro de Triagem",
        goal="Classificar urgência com precisão",
        backstory="Especialista em protocolos de Manchester.",
        llm=llm,
        verbose=False
    )
    
    coordenador = Agent(
        role="Coordenador de Encaminhamento",
        goal="Recomendar melhor unidade de saúde",
        backstory="Conhece toda a rede de saúde.",
        llm=llm,
        verbose=False
    )
    
    coleta = Task(
        description="Colete informações de: {paciente_info}",
        expected_output="Resumo estruturado",
        agent=recepcionista
    )
    
    classificacao = Task(
        description="Classifique urgência consultando protocolos",
        expected_output="Cor, tempo, justificativa",
        agent=triagista,
        context=[coleta]
    )
    
    encaminhamento = Task(
        description="Recomende unidade apropriada",
        expected_output="Encaminhamento com orientações",
        agent=coordenador,
        context=[coleta, classificacao]
    )
    
    crew = Crew(
        agents=[recepcionista, triagista, coordenador],
        tasks=[coleta, classificacao, encaminhamento],
        memory=True,
        knowledge_sources=[conhecimento],
        process=Process.sequential,
        verbose=True
    )
    
    # Teste
    caso = "José Santos, 65 anos, dor forte no peito, sudorese, hipertenso"
    print(f"\n📋 Caso: {caso}\n")
    resultado = crew.kickoff(inputs={"paciente_info": caso})
    print(f"\n📊 Resultado:\n{resultado.raw}")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY não configurada")
        sys.exit(1)
    
    print("\n🎓 EXERCÍCIO 3: SISTEMA RAG COMPLETO")
    print("\n📝 Este é o exercício mais completo do curso!")
    print("Integra: Memory + Knowledge + Múltiplos Agentes")
    print("\n💡 Desafio avançado: Integrar com embeddings (Aula 10)")
    
    escolha = input("\n1. Testar caso emergência\n2. Ver desafio embeddings\n3. Ver gabarito\n\nEscolha: ")
    
    if escolha == "1":
        testar_caso_emergencia()
    elif escolha == "2":
        testar_integracao_embeddings()
    elif escolha == "3":
        solucao_completa()
    else:
        print("❌ Opção inválida")
    
    print("\n" + "=" * 70)
    print("🎯 Parabéns por chegar até aqui!")
    print("=" * 70)
    print("\nVocê aprendeu:")
    print("   🧠 Memory System do CrewAI")
    print("   📚 Knowledge Sources")
    print("   🤝 Colaboração entre agentes")
    print("   🚀 RAG (Retrieval-Augmented Generation)")
    print("\n💪 Agora você pode criar sistemas RAG de verdade!")
