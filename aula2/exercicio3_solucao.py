# Exercício 3: Desenvolvimento de Produto - App para Estudantes
# Solução: Criando agentes para gerar ideias de aplicativo

from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

print("📱 Exercício 3: Criando Ideia de App para Estudantes")
print("=" * 50)

# --- AGENTE 1: Descobridor de Problemas ---
descobridor = Agent(
    role='Especialista em Identificação de Problemas',
    goal='Encontrar um problema que muita gente tem',
    backstory="""Você é observador e sempre repara quando as pessoas
    reclamam de alguma coisa. Você tem facilidade para identificar
    problemas comuns do dia a dia, especialmente de estudantes
    universitários.""",
    verbose=True,
    allow_delegation=False
)

# --- AGENTE 2: Criador de Ideias ---
criador = Agent(
    role='Criador de Soluções Tecnológicas',
    goal='Criar uma ideia de aplicativo para resolver o problema',
    backstory="""Você adora tecnologia e sempre pensa: "Podia ter um
    app para isso!" Você é criativo e sabe pensar em soluções simples
    e práticas usando tecnologia.""",
    verbose=True,
    allow_delegation=False
)

# --- TAREFA 1: Encontrar um Problema ---
tarefa_problema = Task(
    description="""Identifique um problema comum e chato que estudantes
    universitários enfrentam no seu dia a dia na faculdade.

    Foque em:
    - Público: Estudantes universitários
    - Contexto: Vida na faculdade
    - Tipo: Problemas do dia a dia

    O problema deve ser algo que realmente incomoda e que muitos
    estudantes passam por isso.""",
    expected_output="""Um problema específico e comum que estudantes
    universitários enfrentam, explicado de forma clara e simples.""",
    agent=descobridor
)

# --- TAREFA 2: Criar Ideia de App ---
tarefa_app = Task(
    description="""Com base no problema identificado, crie uma ideia
    de aplicativo simples para resolver esse problema.

    A ideia deve incluir:
    - Nome criativo para o app
    - Explicação simples de como funciona
    - Por que seria útil para estudantes
    - Funcionalidade principal

    Mantenha a ideia simples e prática.""",
    expected_output="""Uma ideia completa de aplicativo com nome
    criativo e explicação clara de como resolveria o problema dos
    estudantes.""",
    agent=criador
)

# --- MONTAGEM DA EQUIPE ---
print("\n🚀 Montando equipe de desenvolvimento...")
equipe_produto = Crew(
    agents=[descobridor, criador],
    tasks=[tarefa_problema, tarefa_app],
    process=Process.sequential,
    verbose=True
)

# --- EXECUTANDO O TRABALHO ---
print("\n🎬 Descobrindo problemas e criando soluções...")
print("Aguarde enquanto nossa equipe desenvolve a ideia...\n")

try:
    resultado = equipe_produto.kickoff()

    print("\n" + "="*60)
    print("🎉 IDEIA DE APP CRIADA!")
    print("="*60)
    print("\n💡 SUA NOVA IDEIA DE APLICATIVO:")
    print("-" * 40)
    print(resultado)

    print("\n" + "="*60)
    print("📚 O QUE VOCÊ APRENDEU:")
    print("="*60)
    print("✅ Identificou problemas reais de usuários")
    print("✅ Criou soluções tecnológicas práticas")
    print("✅ Desenvolveu ideias de produto com foco no usuário")
    print("✅ Aplicou processo criativo estruturado")

except Exception as e:
    print(f"\n❌ Erro durante a execução: {e}")
    print("\n🔧 Dicas para resolver:")
    print("- Verifique se sua chave OpenAI está configurada")
    print("- Confirme se tem créditos na conta OpenAI")
    print("- Tente executar novamente")
