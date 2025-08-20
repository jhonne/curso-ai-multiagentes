# Exercício 2: Atendimento ao Cliente - Loja Online
# Solução: Criando agentes para responder reclamações

from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

print("🛍️ Exercício 2: Sistema de Atendimento ao Cliente")
print("=" * 50)

# --- AGENTE 1: Analisador de Problemas ---
analisador = Agent(
    role='Analisador de Problemas de Clientes',
    goal='Descobrir qual é o problema do cliente',
    backstory="""Você é bom em ler mensagens e entender rapidamente
    o que está acontecendo. Você consegue identificar o problema
    principal e explicar de forma clara e simples.""",
    verbose=True,
    allow_delegation=False
)

# --- AGENTE 2: Respondedor Amigável ---
respondedor = Agent(
    role='Especialista em Atendimento ao Cliente',
    goal='Escrever uma resposta gentil e que ajude o cliente',
    backstory="""Você sabe falar com clientes de forma educada e
    sempre tenta ajudar. Você é paciente, compreensivo e sempre
    busca a melhor solução para o cliente.""",
    verbose=True,
    allow_delegation=False
)

# --- TAREFA 1: Entender o Problema ---
tarefa_analise = Task(
    description="""Analise a seguinte reclamação de cliente e
    identifique qual é o problema principal:

    Cliente: Ana
    Mensagem: "Comprei uma camiseta na semana passada e ela chegou
    com um buraco. Quero trocar!"

    Explique de forma simples e clara qual é o problema da Ana.""",
    expected_output="""Um resumo claro do problema da cliente,
    identificando o que aconteceu e o que ela quer.""",
    agent=analisador
)

# --- TAREFA 2: Responder ao Cliente ---
tarefa_resposta = Task(
    description="""Com base na análise do problema, escreva uma
    resposta educada e útil para a cliente Ana.

    A resposta deve:
    - Ser educada e amigável
    - Mostrar que entendemos o problema
    - Incluir o nome da cliente
    - Oferecer uma solução prática
    - Não passar de 100 palavras""",
    expected_output="""Uma resposta completa e profissional pronta
    para enviar à cliente Ana.""",
    agent=respondedor
)

# --- MONTAGEM DA EQUIPE ---
print("\n🚀 Montando equipe de atendimento...")
equipe_atendimento = Crew(
    agents=[analisador, respondedor],
    tasks=[tarefa_analise, tarefa_resposta],
    process=Process.sequential,
    verbose=True
)

# --- EXECUTANDO O TRABALHO ---
print("\n🎬 Analisando e respondendo à reclamação...")
print("Aguarde enquanto nossa equipe resolve o problema...\n")

try:
    resultado = equipe_atendimento.kickoff()

    print("\n" + "="*60)
    print("🎉 ATENDIMENTO CONCLUÍDO!")
    print("="*60)
    print("\n📧 RESPOSTA PARA O CLIENTE:")
    print("-" * 40)
    print(resultado)

    print("\n" + "="*60)
    print("💡 O QUE VOCÊ APRENDEU:")
    print("="*60)
    print("✅ Criou agentes especializados em atendimento")
    print("✅ Analisou problemas de clientes de forma estruturada")
    print("✅ Gerou respostas profissionais e educadas")
    print("✅ Aplicou processo sequencial para resolver problemas")

except Exception as e:
    print(f"\n❌ Erro durante a execução: {e}")
    print("\n🔧 Dicas para resolver:")
    print("- Verifique se sua chave OpenAI está configurada")
    print("- Confirme se tem créditos na conta OpenAI")
    print("- Tente executar novamente")
