# Exercício 1: Equipe de Conteúdo - Padaria do João
# Solução: Criando agentes para gerar post de Instagram

from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

print("🍞 Exercício 1: Criando Post para Padaria do João")
print("=" * 50)

# --- AGENTE 1: Gerador de Ideias ---
gerador_ideias = Agent(
    role='Criativo Gerador de Ideias',
    goal='Criar uma ideia interessante para o post da padaria',
    backstory="""Você é uma pessoa criativa que adora pensar em ideias 
    divertidas para redes sociais. Você sempre pensa em como tornar 
    as coisas simples mais atrativas e interessantes para as pessoas.""",
    verbose=True,
    allow_delegation=False
)

# --- AGENTE 2: Escritor de Posts ---
escritor_posts = Agent(
    role='Escritor de Posts para Redes Sociais',
    goal='Transformar a ideia em um texto atrativo para Instagram',
    backstory="""Você sabe escrever textos que chamam atenção e fazem 
    as pessoas quererem comprar. Você conhece bem o Instagram e sabe 
    como fazer posts que as pessoas gostam de curtir e compartilhar.""",
    verbose=True,
    allow_delegation=False
)

# --- TAREFA 1: Gerar Ideia ---
tarefa_ideia = Task(
    description="""Crie uma ideia criativa para um post de Instagram 
    da Padaria do João. 
    
    Informações da padaria:
    - Nome: Padaria do João
    - Especialidade: Pão francês quentinho
    - Localização: Bairro Vila Nova
    - Diferencial: Sempre tem pão quente de manhã
    
    A ideia deve ser simples, atrativa e relacionada ao diferencial da padaria.""",
    expected_output="""Uma ideia criativa e simples para o post, explicando 
    qual será o foco principal e por que vai chamar atenção dos clientes.""",
    agent=gerador_ideias
)

# --- TAREFA 2: Escrever Post ---
tarefa_post = Task(
    description="""Com base na ideia criada, escreva o texto completo 
    do post para Instagram da Padaria do João.
    
    O texto deve:
    - Ser atrativo e fazer as pessoas quererem ir à padaria
    - Mencionar o diferencial (pão quente de manhã)
    - Incluir pelo menos um emoji relacionado à padaria
    - Ser adequado para o Instagram
    - Não passar de 150 caracteres""",
    expected_output="""Texto completo pronto para postar no Instagram, 
    com emoji e linguagem atrativa.""",
    agent=escritor_posts
)

# --- MONTAGEM DA EQUIPE ---
print("\n🚀 Montando equipe de marketing...")
equipe_marketing = Crew(
    agents=[gerador_ideias, escritor_posts],
    tasks=[tarefa_ideia, tarefa_post],
    process=Process.sequential,
    verbose=True
)

# --- EXECUTANDO O TRABALHO ---
print("\n🎬 Iniciando criação do post...")
print("Aguarde enquanto nossa equipe cria o post perfeito...\n")

try:
    resultado = equipe_marketing.kickoff()
    
    print("\n" + "="*60)
    print("🎉 POST CRIADO COM SUCESSO!")
    print("="*60)
    print("\n📱 SEU POST PARA INSTAGRAM:")
    print("-" * 40)
    print(resultado)
    
    print("\n" + "="*60)
    print("💡 O QUE VOCÊ APRENDEU:")
    print("="*60)
    print("✅ Criou 2 agentes com papéis específicos")
    print("✅ Definiu tarefas claras para cada agente")
    print("✅ Os agentes trabalharam em sequência")
    print("✅ Gerou conteúdo real para uma situação prática")
    
except Exception as e:
    print(f"\n❌ Erro durante a execução: {e}")
    print("\n🔧 Dicas para resolver:")
    print("- Verifique se sua chave OpenAI está configurada")
    print("- Confirme se tem créditos na conta OpenAI")
    print("- Tente executar novamente")
