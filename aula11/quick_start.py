"""
Quick Start - RAG em 30 Minutos
Demonstração prática e interativa dos conceitos básicos de RAG
"""

import os
import sys
from pathlib import Path

# ✅ PRIMEIRO: Carregar dotenv
from dotenv import load_dotenv
load_dotenv()

# ✅ SEGUNDO: Configurar storage ANTES de importar CrewAI
from setup_storage import configurar_storage
config = configurar_storage(__file__)

AULA11_ROOT = config['AULA11_ROOT']
STORAGE_DIR = config['STORAGE_DIR']
CHROMADB_DIR = config['CHROMADB_DIR']

# ✅ TERCEIRO: AGORA importar CrewAI
from crewai import Agent, Task, Crew, LLM
from crewai.knowledge.source.string_knowledge_source import (
    StringKnowledgeSource
)


def linha_separadora(titulo="", char="="):
    """Imprime linha separadora formatada"""
    largura = 80
    if titulo:
        titulo_format = f" {titulo} "
        padding = (largura - len(titulo_format)) // 2
        print(f"\n{char * padding}{titulo_format}{char * padding}")
    else:
        print(f"\n{char * largura}")


def pausar(mensagem="\n⏸️  Pressione ENTER para continuar..."):
    """Pausa a execução"""
    input(mensagem)


def demo_1_memory():
    """Demonstração: Diferença entre com e sem memória"""
    
    linha_separadora("DEMO 1: MEMORY SYSTEM")
    
    print("""
🧠 MEMORY SYSTEM - Por que é importante?

Imagine conversar com alguém que esquece tudo a cada frase.
Frustrante, né? Agentes sem memória são assim!
    """)
    
    pausar()
    
    # SEM MEMÓRIA
    print("\n❌ AGENTE SEM MEMÓRIA:")
    print("-" * 40)
    
    llm = LLM(model="gpt-4o-mini", temperature=0.1)
    
    agente_sem_memoria = Agent(
        role="Atendente",
        goal="Conversar com o paciente",
        backstory="Atendente educado mas sem memória.",
        llm=llm
    )
    
    # Simulação de conversa
    print("\n👤 Usuário: 'Meu nome é João Silva'")
    print("🤖 Agente: 'Olá! Como posso ajudar?'")
    print("\n👤 Usuário: 'Qual meu nome?'")
    print("🤖 Agente: 'Desculpe, não sei seu nome.'")
    print("\n💡 Problema: Agente NÃO lembrou!")
    
    pausar()
    
    # COM MEMÓRIA
    print("\n✅ AGENTE COM MEMÓRIA:")
    print("-" * 40)
    
    agente_com_memoria = Agent(
        role="Atendente",
        goal="Conversar e lembrar do paciente",
        backstory="Atendente com memória perfeita.",
        llm=llm
    )
    
    tarefa = Task(
        description="Converse: {mensagem}",
        expected_output="Resposta contextualizada",
        agent=agente_com_memoria
    )
    
    crew = Crew(
        agents=[agente_com_memoria],
        tasks=[tarefa],
        memory=True,  # 🔑 MEMÓRIA ATIVADA!
        verbose=False
    )
    
    print("\n👤 Usuário: 'Meu nome é João Silva'")
    resultado1 = crew.kickoff(inputs={"mensagem": "Meu nome é João Silva"})
    print(f"🤖 Agente: {resultado1.raw[:100]}...")
    
    print("\n👤 Usuário: 'Qual meu nome?'")
    resultado2 = crew.kickoff(inputs={"mensagem": "Qual meu nome?"})
    print(f"🤖 Agente: {resultado2.raw[:100]}...")
    
    print("\n💡 Sucesso: Agente LEMBROU do nome!")
    
    pausar()


def demo_2_knowledge():
    """Demonstração: Diferença entre com e sem knowledge"""
    
    linha_separadora("DEMO 2: KNOWLEDGE SOURCES")
    
    print("""
📚 KNOWLEDGE SOURCES - Por que é importante?

LLMs sozinhos não têm acesso a documentos específicos.
Knowledge Sources permitem consultar protocolos, manuais, etc.
    """)
    
    pausar()
    
    # Criar protocolo
    protocolo = """
    PROTOCOLO DE TRIAGEM - MANCHESTER
    
    🔴 VERMELHO (Emergência - 0 min):
    - Parada cardíaca
    - Dor torácica com sinais de IAM
    - Trauma craniano grave
    
    🟠 LARANJA (Muito Urgente - 10 min):
    - Dor torácica sem IAM
    - Dificuldade respiratória
    - Hemorragia importante
    
    🟡 AMARELO (Urgente - 60 min):
    - Dor moderada
    - Febre alta
    - Fraturas simples
    """
    
    # SEM KNOWLEDGE
    print("\n❌ AGENTE SEM KNOWLEDGE:")
    print("-" * 40)
    
    llm = LLM(model="gpt-4o-mini", temperature=0.1)
    
    agente_generico = Agent(
        role="Triagista",
        goal="Classificar urgência",
        backstory="Usa conhecimento geral.",
        llm=llm
    )
    
    print("\n👤 Caso: 'Paciente com dor no peito há 30 minutos'")
    print("🤖 Agente: 'Pode ser sério, procure atendimento'")
    print("💡 Problema: Resposta GENÉRICA, sem protocolo!")
    
    pausar()
    
    # COM KNOWLEDGE
    print("\n✅ AGENTE COM KNOWLEDGE:")
    print("-" * 40)
    
    knowledge = StringKnowledgeSource(content=protocolo)
    
    agente_protocolo = Agent(
        role="Triagista",
        goal="Classificar usando protocolos oficiais",
        backstory="Consulta protocolo Manchester.",
        llm=llm
    )
    
    tarefa = Task(
        description="Classifique: {sintomas}. Cite o protocolo.",
        expected_output="Classificação com protocolo",
        agent=agente_protocolo
    )
    
    crew = Crew(
        agents=[agente_protocolo],
        tasks=[tarefa],
        knowledge_sources=[knowledge],  # 🔑 KNOWLEDGE ATIVADO!
        verbose=False
    )
    
    print("\n👤 Caso: 'Paciente com dor no peito há 30 minutos'")
    resultado = crew.kickoff(inputs={"sintomas": "dor no peito há 30 minutos"})
    print(f"🤖 Agente: {resultado.raw[:200]}...")
    print("\n💡 Sucesso: Consultou PROTOCOLO específico!")
    
    pausar()


def demo_3_rag_completo():
    """Demonstração: RAG = Memory + Knowledge"""
    
    linha_separadora("DEMO 3: RAG COMPLETO")
    
    print("""
🚀 RAG = MEMORY + KNOWLEDGE

Combina o melhor dos dois mundos:
- LEMBRA do paciente (histórico)
- CONSULTA protocolos (conhecimento atualizado)
    """)
    
    pausar()
    
    # Protocolo
    protocolo = """
    PROTOCOLO TRIAGEM:
    
    🔴 VERMELHO: Dor torácica + idade >40 anos
    🟠 LARANJA: Dor torácica + idade <40 anos
    🟡 AMARELO: Sintomas moderados
    """
    
    knowledge = StringKnowledgeSource(content=protocolo)
    llm = LLM(model="gpt-4o-mini", temperature=0.1)
    
    agente_rag = Agent(
        role="Triagista Inteligente",
        goal="Classificar com memória e protocolo",
        backstory="Combina histórico do paciente com protocolos.",
        llm=llm
    )
    
    tarefa = Task(
        description="Atenda: {mensagem}",
        expected_output="Resposta contextualizada",
        agent=agente_rag
    )
    
    crew = Crew(
        agents=[agente_rag],
        tasks=[tarefa],
        memory=True,  # 🧠 Memory
        knowledge_sources=[knowledge],  # 📚 Knowledge
        verbose=False
    )
    
    print("\n✨ SISTEMA RAG EM AÇÃO:")
    print("-" * 40)
    
    print("\n👤 Interação 1: 'Meu nome é Carlos, 45 anos'")
    r1 = crew.kickoff(inputs={"mensagem": "Meu nome é Carlos, 45 anos"})
    print(f"🤖 Sistema: Registrado! {r1.raw[:80]}...")
    
    pausar("\n⏸️  Veja como o sistema vai LEMBRAR + CONSULTAR...")
    
    print("\n👤 Interação 2: 'Estou com dor no peito'")
    r2 = crew.kickoff(inputs={"mensagem": "Estou com dor no peito"})
    print(f"🤖 Sistema: {r2.raw[:250]}...")
    
    print("""
    
💡 O QUE ACONTECEU:
1. 🧠 MEMÓRIA: Lembrou que é Carlos, 45 anos
2. 📚 CONHECIMENTO: Consultou protocolo (idade >40 = agravante)
3. 🚀 RAG: Combinou tudo = Classificação VERMELHO precisa!
    """)
    
    pausar()


def resumo_final():
    """Resumo e próximos passos"""
    
    linha_separadora("PARABÉNS!")
    
    print("""
🎉 VOCÊ COMPLETOU O QUICK START!

Em 30 minutos você aprendeu:

✅ Memory System - Agentes que lembram
✅ Knowledge Sources - Agentes que consultam docs
✅ RAG Completo - Memory + Knowledge = Poder!

📊 CONCEITOS DOMINADOS:
┌─────────────────────────────────────────┐
│ Memory:    Histórico de conversas      │
│ Knowledge: Acesso a documentos         │
│ RAG:       Combina ambos!              │
└─────────────────────────────────────────┘

🎯 PRÓXIMOS PASSOS:

1. 🟢 INICIANTE:
   cd modulos/01_memory && uv run exemplo.py
   cd modulos/02_knowledge && uv run exemplo.py

2. 🟡 INTERMEDIÁRIO:
   cd modulos/03_rag_avancado && uv run exemplo_multiagent.py

3. 🔴 AVANÇADO:
   cat docs/GUIA_COMPLETO.md
   Criar seu próprio sistema RAG!

📚 DOCUMENTAÇÃO:
   - README.md - Visão completa da aula
   - docs/GUIA_COMPLETO.md - Referência detalhada
   - docs/CASOS_DE_USO.md - Inspiração para projetos

💪 EXERCÍCIO RÁPIDO:
   uv run exercicio_rapido.py (10 minutos)

🚀 Bom estudo!
    """)


def main():
    """Execução principal do Quick Start"""
    
    # Verificar API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ ERRO: OPENAI_API_KEY não configurada!")
        print("Execute: uv run configurar-crewai")
        return
    
    linha_separadora("QUICK START - RAG EM 30 MINUTOS", "=")
    
    print("""
Bem-vindo ao Quick Start de RAG!

Você vai ver 3 demonstrações práticas:
1. Memory System (agentes que lembram)
2. Knowledge Sources (agentes que consultam docs)
3. RAG Completo (memory + knowledge)

⏱️  Tempo: ~30 minutos
💰 Custo: ~$0.01 (OpenAI)

Vamos começar!
    """)
    
    pausar()
    
    # Demos
    try:
        demo_1_memory()
        demo_2_knowledge()
        demo_3_rag_completo()
        resumo_final()
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Quick Start interrompido. Você pode retomar a qualquer momento!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("Tente novamente ou veja docs/TROUBLESHOOTING.md")


if __name__ == "__main__":
    main()
