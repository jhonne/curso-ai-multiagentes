# Aula 2: Construindo seu Primeiro Crew: Agentes e Tarefas
# Objetivo: Criar um Crew com dois agentes colaborando

from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

print("🎯 Aula 2: Criando um Crew com Pesquisador e Redator")
print("=" * 50)

# --- Definição do Agente Pesquisador ---
pesquisador = Agent(
    role='Pesquisador Especialista',
    goal='Coletar informações detalhadas e precisas sobre tópicos solicitados',
    backstory="""Você é um pesquisador experiente com anos de experiência
    em análise e coleta de informações. Sua especialidade é encontrar
    dados relevantes, verificar fontes e apresentar informações de forma
    organizada e estruturada. Você sempre busca múltiplas perspectivas
    sobre um tópico antes de formar suas conclusões. Responde sempre em
    português brasileiro.""",
    verbose=True,
    allow_delegation=False
)

# --- Definição do Agente Redator ---
redator = Agent(
    role='Redator e Editor Criativo',
    goal='Transformar informações brutas em conteúdo claro e envolvente',
    backstory="""Você é um redator profissional com talento para
    transformar informações complexas em textos claros e envolventes.
    Sua habilidade especial é pegar dados brutos de pesquisa e criar
    narrativas coerentes e interessantes. Você sempre adapta o tom e
    estilo do texto para o público-alvo e garante que o conteúdo seja
    acessível e bem organizado. Escreve sempre em português brasileiro.""",
    verbose=True,
    allow_delegation=False
)

# --- Definição da Tarefa de Pesquisa ---
tarefa_pesquisa = Task(
    description="""Pesquise e colete informações abrangentes sobre
    'Inteligência Artificial aplicada à educação'. Foque nos seguintes
    aspectos:
    
    1. Principais benefícios da IA na educação
    2. Ferramentas de IA mais utilizadas por educadores
    3. Desafios e limitações atuais
    4. Tendências futuras na área
    
    Organize as informações de forma estruturada e inclua dados
    específicos quando possível.""",
    expected_output="""Um relatório estruturado com:
    - Lista dos principais benefícios da IA na educação (mínimo 5 pontos)
    - Pelo menos 3 ferramentas de IA populares na educação
    - Principais desafios identificados (mínimo 3)
    - Pelo menos 2 tendências futuras
    - Informações organizadas em seções claras""",
    agent=pesquisador
)

# --- Definição da Tarefa de Redação ---
tarefa_redacao = Task(
    description="""Com base na pesquisa realizada pelo pesquisador,
    crie um artigo informativo e envolvente sobre 'IA na Educação:
    Transformando o Futuro do Aprendizado'.
    
    O artigo deve:
    - Ter uma introdução cativante
    - Organizar as informações em seções lógicas
    - Usar uma linguagem acessível para educadores
    - Incluir uma conclusão inspiradora
    - Ter entre 800-1000 palavras""",
    expected_output="""Um artigo completo e bem estruturado com:
    - Título atrativo
    - Introdução envolvente (1-2 parágrafos)
    - Desenvolvimento em seções organizadas
    - Conclusão inspiradora
    - Linguagem clara e acessível
    - Aproximadamente 800-1000 palavras""",
    agent=redator
)

# --- Definição de uma Tarefa Adicional: Resumo Executivo ---
tarefa_resumo = Task(
    description="""Crie um resumo executivo do artigo produzido,
    destacando os pontos-chave de forma concisa para gestores
    educacionais que têm pouco tempo para leitura completa.""",
    expected_output="""Um resumo executivo de no máximo 200 palavras contendo:
    - Os 3 principais benefícios da IA na educação
    - O principal desafio a ser superado
    - Uma recomendação prática para implementação
    - Formatado em bullet points para fácil leitura""",
    agent=redator
)

# --- Montagem da Equipe (Crew) ---
print("\n🚀 Montando a equipe de trabalho...")
equipe_conteudo = Crew(
    agents=[pesquisador, redator],
    tasks=[tarefa_pesquisa, tarefa_redacao, tarefa_resumo],
    process=Process.sequential,  # Execução sequencial
    verbose=True
)

# --- Início do Trabalho ---
print("\n🎬 Iniciando o trabalho da equipe...")
print("Aguarde enquanto nossos agentes trabalham em colaboração...\n")

try:
    resultado = equipe_conteudo.kickoff()
    
    print("\n" + "="*60)
    print("🎉 TRABALHO CONCLUÍDO COM SUCESSO!")
    print("="*60)
    print("\n📋 RESULTADO FINAL DA COLABORAÇÃO:")
    print("-" * 40)
    print(resultado)
    
    print("\n" + "="*60)
    print("💡 LIÇÕES DA AULA 2:")
    print("="*60)
    print("✅ Criamos dois agentes com papéis específicos")
    print("✅ Definimos tarefas com descrições e resultados esperados claros")
    print("✅ Organizamos um fluxo sequencial de trabalho")
    print("✅ Vimos como agentes podem colaborar em um projeto complexo")
    print("\n🎯 Próxima aula: Ferramentas e Processos Avançados!")
    
except Exception as e:
    print(f"\n❌ Erro durante a execução: {e}")
    print("\n🔧 Verificações necessárias:")
    print("- Sua chave da OpenAI está configurada corretamente?")
    print("- Você tem créditos suficientes na sua conta OpenAI?")
    print("- Sua conexão com a internet está funcionando?")
