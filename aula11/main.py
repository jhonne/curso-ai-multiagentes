#!/usr/bin/env -S uv run
"""
Aula 11: RAG - Sistema Interativo de Demonstração

Sistema didático progressivo que ensina RAG através de exemplos práticos.

USO:
    uv run aula11/main.py

Autor: Curso CrewAI
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# ✅ 1. Carregar .env PRIMEIRO
load_dotenv()

# ✅ 2. Configurar storage ANTES de importar CrewAI
AULA11_ROOT = Path(__file__).parent
STORAGE_DIR = AULA11_ROOT / ".chromadb"
os.environ["CREWAI_STORAGE_DIR"] = str(STORAGE_DIR)

# ✅ 3. AGORA importar CrewAI
from crewai import Agent, Task, Crew, Process, LLM
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource
from crewai.knowledge.source.text_file_knowledge_source import TextFileKnowledgeSource


def verificar_api_key():
    """Verifica se API Key está configurada"""
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ ERRO: OPENAI_API_KEY não configurada!")
        print("💡 Solução: Execute 'uv run configurar-crewai' na raiz do projeto\n")
        sys.exit(1)
    print("✅ API Key configurada\n")


def limpar_tela():
    """Limpa a tela do terminal"""
    os.system('clear' if os.name != 'nt' else 'cls')


def criar_protocolo_triagem():
    """Cria knowledge source com protocolo médico"""
    conteudo = """
PROTOCOLO DE TRIAGEM - SISTEMA MANCHESTER

🔴 VERMELHO (Emergência) - IMEDIATO
- Dor no peito intensa
- Dificuldade respiratória grave
- Hemorragia severa
- Inconsciência

🟠 LARANJA (Muito Urgente) - 10 minutos
- Dor no peito moderada
- Febre alta com sinais graves
- Sangramento moderado

🟡 AMARELO (Urgente) - 60 minutos
- Dor moderada
- Febre sem gravidade
- Vômitos persistentes

🟢 VERDE (Pouco Urgente) - 2 horas
- Sintomas leves
- Dor leve

🔵 AZUL (Não Urgente) - 4 horas
- Problemas administrativos
- Condições estáveis
"""
    return StringKnowledgeSource(content=conteudo)


def exemplo_1_sem_memory():
    """Demonstra agente SEM memory"""
    print("\n" + "="*70)
    print("🤖 EXEMPLO 1: Agente SEM Memory")
    print("="*70)
    print("\nObserve: O agente NÃO lembra da conversa anterior\n")
    
    llm = LLM(model="gpt-4o-mini", temperature=0.7)
    
    agente = Agent(
        role="Atendente Virtual",
        goal="Responder perguntas do paciente",
        backstory="Atendente de hospital prestativo.",
        llm=llm,
        memory=False,  # ❌ SEM memory
        verbose=False
    )
    
    # Primeira pergunta
    print("👤 Paciente: 'Meu nome é João Silva'")
    tarefa1 = Task(
        description="Paciente disse: 'Meu nome é João Silva'. Responda educadamente.",
        expected_output="Resposta curta e educada",
        agent=agente
    )
    
    crew = Crew(agents=[agente], tasks=[tarefa1], process=Process.sequential, verbose=False)
    resultado1 = crew.kickoff()
    print(f"🤖 Agente: {resultado1.raw}\n")
    
    # Segunda pergunta - deve esquecer o nome!
    print("👤 Paciente: 'Qual é o meu nome?'")
    tarefa2 = Task(
        description="Paciente perguntou: 'Qual é o meu nome?'. Responda.",
        expected_output="Resposta sobre o nome",
        agent=agente
    )
    
    crew = Crew(agents=[agente], tasks=[tarefa2], process=Process.sequential, verbose=False)
    resultado2 = crew.kickoff()
    print(f"🤖 Agente: {resultado2.raw}")
    print(f"\n❌ PROBLEMA: Agente NÃO lembrou que o nome é 'João Silva'!\n")
    
    input("Pressione ENTER para continuar...")


def exemplo_2_com_memory():
    """Demonstra agente COM memory"""
    print("\n" + "="*70)
    print("🧠 EXEMPLO 2: Agente COM Memory")
    print("="*70)
    print("\nObserve: O agente LEMBRA da conversa anterior\n")
    
    llm = LLM(model="gpt-4o-mini", temperature=0.7)
    
    agente = Agent(
        role="Atendente Virtual",
        goal="Responder perguntas lembrando de tudo",
        backstory="Atendente experiente que nunca esquece detalhes.",
        llm=llm,
        verbose=False
    )
    
    # Primeira pergunta
    print("👤 Paciente: 'Meu nome é Maria Santos'")
    tarefa1 = Task(
        description="Paciente disse: 'Meu nome é Maria Santos'. Responda educadamente.",
        expected_output="Resposta curta e educada",
        agent=agente
    )
    
    crew = Crew(
        agents=[agente],
        tasks=[tarefa1],
        memory=True,  # ✅ COM memory
        process=Process.sequential,
        verbose=False
    )
    resultado1 = crew.kickoff()
    print(f"🤖 Agente: {resultado1.raw}\n")
    
    # Segunda pergunta - deve lembrar o nome!
    print("👤 Paciente: 'Qual é o meu nome?'")
    tarefa2 = Task(
        description="Paciente perguntou: 'Qual é o meu nome?'. Responda.",
        expected_output="Resposta sobre o nome",
        agent=agente
    )
    
    crew = Crew(
        agents=[agente],
        tasks=[tarefa2],
        memory=True,  # ✅ COM memory
        process=Process.sequential,
        verbose=False
    )
    resultado2 = crew.kickoff()
    print(f"🤖 Agente: {resultado2.raw}")
    print(f"\n✅ SUCESSO: Agente LEMBROU que o nome é 'Maria Santos'!\n")
    
    input("Pressione ENTER para continuar...")


def exemplo_3_sem_knowledge():
    """Demonstra agente SEM knowledge"""
    print("\n" + "="*70)
    print("🤖 EXEMPLO 3: Agente SEM Knowledge")
    print("="*70)
    print("\nObserve: Resposta genérica, sem protocolo específico\n")
    
    llm = LLM(model="gpt-4o-mini", temperature=0.7)
    
    agente = Agent(
        role="Enfermeiro de Triagem",
        goal="Classificar urgência de pacientes",
        backstory="Enfermeiro experiente em triagem.",
        llm=llm,
        verbose=False
        # ❌ SEM knowledge_sources
    )
    
    print("👤 Paciente: 'Estou com dor no peito intensa'")
    tarefa = Task(
        description="Paciente relata: 'Dor no peito intensa'. Classifique urgência.",
        expected_output="Classificação de urgência",
        agent=agente
    )
    
    crew = Crew(agents=[agente], tasks=[tarefa], process=Process.sequential, verbose=False)
    resultado = crew.kickoff()
    print(f"🤖 Agente: {resultado.raw}")
    print(f"\n❌ PROBLEMA: Resposta genérica, não seguiu protocolo específico!\n")
    
    input("Pressione ENTER para continuar...")


def exemplo_4_com_knowledge():
    """Demonstra agente COM knowledge"""
    print("\n" + "="*70)
    print("📚 EXEMPLO 4: Agente COM Knowledge")
    print("="*70)
    print("\nObserve: Resposta baseada no Protocolo Manchester\n")
    
    llm = LLM(model="gpt-4o-mini", temperature=0.7)
    protocolo = criar_protocolo_triagem()
    
    agente = Agent(
        role="Enfermeiro de Triagem",
        goal="Classificar pacientes segundo Protocolo Manchester",
        backstory="Enfermeiro especializado em triagem que sempre consulta protocolos oficiais.",
        llm=llm,
        knowledge_sources=[protocolo],  # ✅ COM knowledge
        verbose=False
    )
    
    print("👤 Paciente: 'Estou com dor no peito intensa'")
    tarefa = Task(
        description="Paciente relata: 'Dor no peito intensa'. Classifique segundo Protocolo Manchester.",
        expected_output="Classificação com cor e tempo",
        agent=agente
    )
    
    crew = Crew(agents=[agente], tasks=[tarefa], process=Process.sequential, verbose=False)
    resultado = crew.kickoff()
    print(f"🤖 Agente: {resultado.raw}")
    print(f"\n✅ SUCESSO: Resposta baseada no protocolo oficial!\n")
    
    input("Pressione ENTER para continuar...")


def exemplo_5_rag_completo():
    """Demonstra RAG completo: Memory + Knowledge"""
    print("\n" + "="*70)
    print("🚀 EXEMPLO 5: RAG COMPLETO (Memory + Knowledge)")
    print("="*70)
    print("\nObserve: Agente LEMBRA do paciente E consulta protocolo\n")
    
    llm = LLM(model="gpt-4o-mini", temperature=0.7)
    protocolo = criar_protocolo_triagem()
    
    agente = Agent(
        role="Enfermeiro de Triagem",
        goal="Atender pacientes lembrando do histórico e seguindo protocolos",
        backstory="Enfermeiro experiente que nunca esquece pacientes e sempre consulta protocolos.",
        llm=llm,
        knowledge_sources=[protocolo],  # ✅ Knowledge
        verbose=False
    )
    
    # Primeira interação: paciente se apresenta
    print("👤 Paciente: 'Meu nome é Carlos, 55 anos'")
    tarefa1 = Task(
        description="Paciente disse: 'Meu nome é Carlos, 55 anos'. Registre as informações.",
        expected_output="Confirmação dos dados",
        agent=agente
    )
    
    crew = Crew(
        agents=[agente],
        tasks=[tarefa1],
        memory=True,  # ✅ Memory
        process=Process.sequential,
        verbose=False
    )
    resultado1 = crew.kickoff()
    print(f"🤖 Agente: {resultado1.raw}\n")
    
    # Segunda interação: sintoma
    print("👤 Paciente: 'Estou com dor no peito há 30 minutos'")
    tarefa2 = Task(
        description="Paciente relata: 'Dor no peito há 30 minutos'. Classifique segundo protocolo considerando idade.",
        expected_output="Classificação personalizada",
        agent=agente
    )
    
    crew = Crew(
        agents=[agente],
        tasks=[tarefa2],
        memory=True,  # ✅ Memory
        process=Process.sequential,
        verbose=False
    )
    resultado2 = crew.kickoff()
    print(f"🤖 Agente: {resultado2.raw}")
    print(f"\n✅ PERFEITO: Resposta personalizada (lembrou idade) + protocolo!\n")
    
    input("Pressione ENTER para voltar ao menu...")


def mostrar_menu():
    """Mostra menu principal"""
    limpar_tela()
    print("\n" + "="*70)
    print("🎓 AULA 11: RAG (Retrieval-Augmented Generation) com CrewAI")
    print("="*70)
    print("\n📚 MENU DE EXEMPLOS PROGRESSIVOS:\n")
    print("   1️⃣  Agente SEM Memory (veja a limitação)")
    print("   2️⃣  Agente COM Memory (veja a diferença!)")
    print("   3️⃣  Agente SEM Knowledge (resposta genérica)")
    print("   4️⃣  Agente COM Knowledge (resposta baseada em docs)")
    print("   5️⃣  RAG Completo (Memory + Knowledge = Poder!)")
    print("\n   6️⃣  Executar TODOS os exemplos em sequência")
    print("   0️⃣  Sair")
    print("\n" + "="*70)


def main():
    """Função principal"""
    verificar_api_key()
    
    while True:
        mostrar_menu()
        opcao = input("\n👉 Escolha uma opção (0-6): ").strip()
        
        if opcao == "1":
            exemplo_1_sem_memory()
        elif opcao == "2":
            exemplo_2_com_memory()
        elif opcao == "3":
            exemplo_3_sem_knowledge()
        elif opcao == "4":
            exemplo_4_com_knowledge()
        elif opcao == "5":
            exemplo_5_rag_completo()
        elif opcao == "6":
            print("\n🎬 Executando todos os exemplos...\n")
            exemplo_1_sem_memory()
            exemplo_2_com_memory()
            exemplo_3_sem_knowledge()
            exemplo_4_com_knowledge()
            exemplo_5_rag_completo()
            print("\n✅ Todos os exemplos concluídos!")
            input("\nPressione ENTER para voltar ao menu...")
        elif opcao == "0":
            print("\n👋 Até logo! Bons estudos!\n")
            break
        else:
            print("\n❌ Opção inválida! Escolha entre 0-6.")
            input("Pressione ENTER para continuar...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido. Até logo!\n")
    except Exception as e:
        print(f"\n❌ ERRO: {e}")
        print("\n💡 Dica: Verifique TROUBLESHOOTING.md para soluções comuns\n")
        sys.exit(1)
