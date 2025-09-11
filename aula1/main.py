# main.py
import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
# Garante que a chave da API da OpenAI seja carregada de forma segura
load_dotenv()

# --- Definição do Agente ---
# Criação de um agente especialista em pesquisa de tecnologias de IA
pesquisador = Agent(
  role='Pesquisador de Tecnologias de IA Brasileiro',
  goal='Encontrar e analisar informações sobre as vantagens de frameworks de IA em português brasileiro',
  backstory="""Você é um analista de tecnologia brasileiro experiente, com um profundo conhecimento 
  sobre as últimas tendências em inteligência artificial. Sua habilidade é destrinchar 
  conceitos complexos e apresentá-los de forma clara e concisa em português brasileiro.
  Você SEMPRE responde em português brasileiro de forma natural e acessível.""",
  verbose=True,  # Habilita o log detalhado do processo de pensamento do agente
  allow_delegation=False, # Impede que o agente delegue tarefas para outros
)

cardiologista = Agent(
  role='Tratar problemas do coração das pessoas',
  goal='Dar maior bem estar para as pessoas',
  backstory="""Você é um cardiologista experiente, dedicado a entender e tratar problemas do coração. Sua missão é promover a saúde cardiovascular e melhorar a qualidade de vida dos seus pacientes. Você não responde sobre outras especialidades ou áreas da medicina.""",
  verbose=True,  # Habilita o log detalhado do processo de pensamento do agente
  allow_delegation=False, # Impede que o agente delegue tarefas para outros
)

# --- Definição da Tarefa ---
# Criação de uma tarefa específica para o agente pesquisador
tarefa_pesquisa = Task(
  description='Qual é a principal vantagem de se utilizar o framework CrewAI para construir equipes de agentes de IA?',
  expected_output='Um parágrafo curto (2 a 3 frases) explicando o principal benefício do CrewAI.',
  agent=pesquisador # Atribui a tarefa ao agente que acabamos de criar
)

tarefa_cardiologia = Task(
  description='Estou sentindo o coração, ele as vezes acelera do nada e as vezes está lento. o que significa?',
  expected_output='Um parágrafo curto (2 a 3 frases).',
  agent=cardiologista # Atribui a tarefa ao agente que acabamos de criar
)

# --- Montagem da Equipe (Crew) ---
# Criação da "crew" com o agente e a tarefa, definindo o processo
equipe = Crew(
  agents=[pesquisador, cardiologista], # Lista de agentes que compõem a equipe
  tasks=[tarefa_pesquisa, tarefa_cardiologia],
  process=Process.sequential, # As tarefas serão executadas uma após a outra
  verbose=True # Log detalhado da execução da crew
)

# --- Início do Trabalho ---
# O método "kickoff" inicia a execução das tarefas pela equipe
print("🚀 Iniciando a execução da equipe...")
resultado = equipe.kickoff()

print("\n\n########################")
print("## Resultado Final:")
print("########################")
print(resultado)