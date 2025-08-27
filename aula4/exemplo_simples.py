"""
Exemplo Simplificado para Demonstração da Aula 4
Sistema de Atendimento com Cadeia de Agentes

Execute este arquivo para ver os agentes trabalhando em sequência
"""

import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Verificar se a API key está configurada
if not os.getenv("OPENAI_API_KEY"):
    print("⚠️  ATENÇÃO: Configure a variável OPENAI_API_KEY")
    print("No Windows PowerShell: $env:OPENAI_API_KEY='sua_chave_aqui'")
    exit(1)

# Configuração do modelo
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)


def exemplo_simples():
    """Exemplo simplificado com uma pergunta pré-definida"""

    # Base de dados simples
    produtos = {
        "notebook": "Notebook Gamer X1 - R$ 2.999,90 - Disponível",
        "smartphone": "Smartphone Pro - R$ 1.599,90 - Em estoque",
        "fone": "Fone Bluetooth - R$ 299,90 - Disponível",
    }

    # ===== AGENTE 1: RECEPCIONISTA =====
    recepcionista = Agent(
        role="Recepcionista Virtual",
        goal="Limpar e preparar a pergunta do cliente",
        backstory="Você é responsável por receber e organizar as perguntas dos clientes.",
        llm=llm,
        verbose=True,
    )

    # ===== AGENTE 2: ANALISTA =====
    analista = Agent(
        role="Analista de Intenções",
        goal="Extrair a intenção principal da pergunta",
        backstory="Você identifica o que o cliente realmente quer saber.",
        llm=llm,
        verbose=True,
    )

    # ===== AGENTE 3: PESQUISADOR =====
    pesquisador = Agent(
        role="Pesquisador de Produtos",
        goal="Buscar informações sobre produtos",
        backstory=f"Você consulta nossa base de produtos: {produtos}",
        llm=llm,
        verbose=True,
    )

    # ===== AGENTE 4: COMUNICADOR =====
    comunicador = Agent(
        role="Comunicador de Atendimento",
        goal="Criar resposta amigável para o cliente",
        backstory="Você transforma informações técnicas em respostas humanas e úteis.",
        llm=llm,
        verbose=True,
    )

    # ===== PERGUNTA DO CLIENTE =====
    pergunta = "e ai, quanto custa aquele notebook gamer?"

    # ===== TAREFAS =====
    tarefa1 = Task(
        description=f"Limpe esta pergunta: '{pergunta}'",
        agent=recepcionista,
        expected_output="Pergunta limpa e clara",
    )

    tarefa2 = Task(
        description="Analise a pergunta e extraia: intenção e produto mencionado",
        agent=analista,
        expected_output="Intenção identificada e produto extraído",
        context=[tarefa1],
    )

    tarefa3 = Task(
        description="Busque informações sobre o produto identificado",
        agent=pesquisador,
        expected_output="Informações específicas do produto",
        context=[tarefa2],
    )

    tarefa4 = Task(
        description="Crie uma resposta amigável com as informações encontradas",
        agent=comunicador,
        expected_output="Resposta final para o cliente",
        context=[tarefa3],
    )

    # ===== EXECUÇÃO =====
    print("🤖 INICIANDO CADEIA DE AGENTES")
    print("=" * 50)
    print(f"📝 Pergunta: {pergunta}")
    print("=" * 50)

    equipe = Crew(
        agents=[recepcionista, analista, pesquisador, comunicador],
        tasks=[tarefa1, tarefa2, tarefa3, tarefa4],
        process=Process.sequential,
        verbose=True,
    )

    resultado = equipe.kickoff()

    print("\n" + "=" * 50)
    print("✅ RESPOSTA FINAL:")
    print("=" * 50)
    print(resultado)
    print("=" * 50)


if __name__ == "__main__":
    exemplo_simples()
