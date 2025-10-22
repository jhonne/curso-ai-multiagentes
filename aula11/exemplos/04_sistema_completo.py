#!/usr/bin/env python3
"""
Exemplo 4: Sistema RAG Completo

Sistema completo de triagem médica integrando:
- Memory (histórico de pacientes)
- Knowledge (protocolos médicos)
- Múltiplos agentes colaborando

Execute: uv run aula11/exemplos/04_sistema_completo.py
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
sys.path.insert(0, str(Path(__file__).parent.parent))
from setup_storage import configurar_storage
config = configurar_storage(__file__)

# ✅ AGORA importar CrewAI
from crewai import Agent, Task, Crew, Process, LLM
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

load_dotenv()


def criar_conhecimento_completo():
    """Base de conhecimento médica completa"""
    return StringKnowledgeSource(content="""
SISTEMA DE TRIAGEM MÉDICA - PROTOCOLOS COMPLETOS

=== CLASSIFICAÇÃO DE URGÊNCIA ===

🔴 VERMELHO - Emergência (0 min)
Condições que ameaçam a vida:
- Parada cardiorrespiratória
- IAM (Infarto Agudo do Miocárdio)
- AVC (Acidente Vascular Cerebral)
- Choque de qualquer etiologia
- Trauma grave com instabilidade
Encaminhamento: HOSPITAL com UTI

🟠 LARANJA - Muito Urgente (10 min)
Risco potencial de vida:
- Dor torácica intensa
- Dispneia severa
- Alteração neurológica aguda
- Sangramento moderado/grave
- Dor abdominal intensa
Encaminhamento: HOSPITAL ou UPA 24h

🟡 AMARELO - Urgente (60 min)
Necessita avaliação médica breve:
- Febre alta persistente
- Dor moderada
- Vômitos/diarreia com desidratação
- Traumas leves/moderados
Encaminhamento: UPA ou Pronto Atendimento

🟢 VERDE - Pouco Urgente (120 min)
Condições não urgentes:
- Sintomas leves e crônicos
- Problemas administrativos de saúde
Encaminhamento: UBS ou Pronto Atendimento

=== FATORES AGRAVANTES ===
- Idade > 60 anos ou < 2 anos
- Comorbidades (diabetes, hipertensão, cardiopatias)
- Imunossupressão
- Gestação

=== SINAIS DE ALERTA ===
- Alteração do nível de consciência
- Cianose (lábios/extremidades azulados)
- Sudorese fria
- Taquicardia ou bradicardia severa
- Hipotensão
""")


def sistema_triagem_completo():
    """Sistema completo com múltiplos agentes"""
    print("\n" + "=" * 70)
    print("🏥 SISTEMA DE TRIAGEM COMPLETO")
    print("=" * 70)
    
    llm = LLM(model="gpt-4o-mini", temperature=0.5)
    conhecimento = criar_conhecimento_completo()
    
    # AGENTE 1: Recepcionista
    recepcionista = Agent(
        role="Recepcionista Virtual",
        goal="Coletar informações iniciais do paciente com empatia",
        backstory="""Recepcionista experiente e empática.
        Coleta sintomas principais, histórico e dados relevantes.
        Sempre registra informações importantes.""",
        llm=llm,
        verbose=False
    )
    
    # AGENTE 2: Enfermeiro de Triagem
    triagem = Agent(
        role="Enfermeiro de Triagem",
        goal="Classificar urgência usando protocolos oficiais",
        backstory="""Enfermeiro especializado em triagem.
        Segue rigorosamente os protocolos de Manchester.
        Considera fatores agravantes e sinais de alerta.""",
        llm=llm,
        verbose=False
    )
    
    # AGENTE 3: Coordenador de Encaminhamento
    coordenador = Agent(
        role="Coordenador de Encaminhamento",
        goal="Recomendar melhor unidade de saúde",
        backstory="""Coordenador que conhece a rede de saúde.
        Encaminha para UTI, UPA, Hospital ou UBS conforme necessidade.""",
        llm=llm,
        verbose=False
    )
    
    # TASKS
    coleta = Task(
        description="""Converse com o paciente {nome} e colete:
        
        1. Sintomas principais e quando começaram
        2. Intensidade dos sintomas (leve/moderado/grave)
        3. Histórico médico (doenças, medicamentos)
        4. Idade e condições especiais
        
        Seja empático e completo.""",
        expected_output="Resumo estruturado do caso",
        agent=recepcionista
    )
    
    classificacao = Task(
        description="""Baseado nos dados coletados, classifique a urgência.
        
        Consulte os PROTOCOLOS e determine:
        1. Cor de classificação (VERMELHO/LARANJA/AMARELO/VERDE)
        2. Tempo de espera recomendado
        3. Identificação de fatores agravantes
        4. Sinais de alerta presentes
        
        Justifique cada ponto usando os protocolos.""",
        expected_output="Classificação completa e fundamentada",
        agent=triagem,
        context=[coleta]
    )
    
    encaminhamento = Task(
        description="""Recomende a unidade de saúde apropriada.
        
        Considere:
        - Classificação de urgência
        - Complexidade do caso
        - Necessidade de recursos especializados
        
        Opções: HOSPITAL com UTI, UPA 24h, Pronto Atendimento, UBS
        
        Forneça orientações ao paciente sobre o que fazer.""",
        expected_output="Recomendação de encaminhamento",
        agent=coordenador,
        context=[coleta, classificacao]
    )
    
    # CREW COMPLETA
    crew = Crew(
        agents=[recepcionista, triagem, coordenador],
        tasks=[coleta, classificacao, encaminhamento],
        memory=True,  # 🧠 Memória entre agentes e sessões
        knowledge_sources=[conhecimento],  # 📚 Protocolos completos
        process=Process.sequential,
        verbose=True  # Ver fluxo completo
    )
    
    return crew


def executar_caso_1():
    """Caso 1: Emergência cardíaca"""
    print("\n" + "=" * 70)
    print("📋 CASO 1: EMERGÊNCIA CARDÍACA")
    print("=" * 70)
    
    crew = sistema_triagem_completo()
    
    caso = {
        "nome": "José Santos, 65 anos",
        "sintomas_principais": "dor forte no peito há 30 minutos",
        "detalhes": "dor irradia para braço esquerdo, sudorese, falta de ar",
        "historico": "hipertenso, diabético"
    }
    
    print(f"\n👤 Paciente: {caso['nome']}")
    print(f"🩺 Sintomas: {caso['sintomas_principais']}")
    print(f"📝 Detalhes: {caso['detalhes']}")
    print(f"📋 Histórico: {caso['historico']}\n")
    
    print("🚀 Iniciando triagem...")
    print("-" * 70)
    
    resultado = crew.kickoff(inputs=caso)
    
    print("\n" + "=" * 70)
    print("📊 RESULTADO FINAL")
    print("=" * 70)
    print(f"\n{resultado.raw}\n")


def executar_caso_2():
    """Caso 2: Urgência moderada"""
    print("\n" + "=" * 70)
    print("📋 CASO 2: URGÊNCIA MODERADA")
    print("=" * 70)
    
    crew = sistema_triagem_completo()
    
    caso = {
        "nome": "Maria Silva, 42 anos",
        "sintomas_principais": "febre alta 39°C há 2 dias",
        "detalhes": "tosse com catarro, dificuldade respiratória moderada",
        "historico": "saudável, sem comorbidades"
    }
    
    print(f"\n👤 Paciente: {caso['nome']}")
    print(f"🩺 Sintomas: {caso['sintomas_principais']}")
    print(f"📝 Detalhes: {caso['detalhes']}")
    print(f"📋 Histórico: {caso['historico']}\n")
    
    print("🚀 Iniciando triagem...")
    print("-" * 70)
    
    resultado = crew.kickoff(inputs=caso)
    
    print("\n" + "=" * 70)
    print("📊 RESULTADO FINAL")
    print("=" * 70)
    print(f"\n{resultado.raw}\n")


if __name__ == "__main__":
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY não configurada")
        sys.exit(1)
    
    print("\n🎓 EXEMPLO 4: SISTEMA RAG COMPLETO")
    print("\nSistema de triagem médica com múltiplos agentes")
    print("Integra: Memory + Knowledge + Colaboração\n")
    
    input("⏸️  Pressione ENTER para CASO 1 (Emergência)...")
    executar_caso_1()
    
    input("\n⏸️  Pressione ENTER para CASO 2 (Urgência Moderada)...")
    executar_caso_2()
    
    print("\n" + "=" * 70)
    print("✅ EXEMPLO CONCLUÍDO!")
    print("=" * 70)
    print("\n🎯 Você viu um sistema RAG completo em ação!")
    print("   🧠 Memória mantendo contexto")
    print("   📚 Protocolos sendo consultados")
    print("   👥 Agentes colaborando")
    print("\n💡 Agora tente os exercícios em aula11/exercicios/")
