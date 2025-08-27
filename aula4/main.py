"""
Aula 4 - Cadeia de Agentes Especializados
Sistema de Atendimento ao Cliente com 4 Agentes

Este exemplo demonstra como criar agentes especializados que trabalham
em sequência, cada um com uma responsabilidade específica.
"""

import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Configuração do modelo de linguagem
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

# Base de dados simulada de produtos
PRODUTOS_DB = {
    "notebook gamer": {
        "nome": "Notebook Gamer Ultra X1",
        "preco": 2999.90,
        "estoque": 15,
        "categoria": "informatica",
    },
    "smartphone": {
        "nome": "Smartphone Pro Max 256GB",
        "preco": 1599.90,
        "estoque": 8,
        "categoria": "celulares",
    },
    "fone bluetooth": {
        "nome": "Fone Bluetooth Premium",
        "preco": 299.90,
        "estoque": 25,
        "categoria": "acessorios",
    },
}


def buscar_produto_db(query):
    """Simula busca no banco de dados"""
    query_lower = query.lower()

    for key, produto in PRODUTOS_DB.items():
        if key in query_lower or any(
            word in produto["nome"].lower() for word in query_lower.split()
        ):
            return produto

    return None


# ===============================================
# 1. AGENTE DE SAUDAÇÃO E TRIAGEM (O Recepcionista)
# ===============================================

agente_recepcao = Agent(
    role="Recepcionista Virtual",
    goal="Receber e preparar as perguntas dos clientes para processamento",
    backstory="""
    Você é um recepcionista virtual experiente e cordial.
    Sua função é receber as perguntas dos clientes, fazer uma limpeza
    básica do texto (remover gírias excessivas, corrigir erros óbvios)
    e preparar a pergunta para os próximos agentes.
    
    Mantenha o tom original da pergunta, mas torne-a mais clara e objetiva.
    """,
    verbose=True,
    llm=llm,
)

# ===============================================
# 2. AGENTE DE EXTRAÇÃO DE INTENÇÃO (O Analista)
# ===============================================

agente_analise = Agent(
    role="Analista de Intenções",
    goal="Extrair a intenção e entidades importantes da pergunta do cliente",
    backstory="""
    Você é um analista especialista em compreender intenções de clientes.
    Sua missão é analisar a pergunta limpa e extrair:
    
    1. A INTENÇÃO principal (consultar_preco, verificar_estoque, obter_informacoes, etc.)
    2. O PRODUTO mencionado (seja específico ou categoria)
    3. Qualquer CONTEXTO adicional relevante
    
    Sempre retorne sua análise no formato JSON estruturado:
    {
        "intencao": "tipo_da_intencao",
        "produto": "produto_identificado",
        "contexto": "informações_adicionais"
    }
    """,
    verbose=True,
    llm=llm,
)

# ===============================================
# 3. AGENTE DE BUSCA DE INFORMAÇÃO (O Pesquisador)
# ===============================================

agente_pesquisa = Agent(
    role="Pesquisador de Informações",
    goal="Buscar informações específicas baseadas na intenção identificada",
    backstory="""
    Você é um pesquisador especializado em localizar informações precisas
    sobre produtos em nossa base de dados.
    
    Receba a intenção estruturada e busque as informações necessárias.
    
    Para consultas de preço: retorne preço atual e disponibilidade
    Para verificação de estoque: retorne quantidade disponível
    Para informações gerais: retorne todos os dados relevantes do produto
    
    Sempre retorne dados factuais e precisos, sem elaboração.
    """,
    verbose=True,
    llm=llm,
)

# ===============================================
# 4. AGENTE DE GERAÇÃO DE RESPOSTA (O Comunicador)
# ===============================================

agente_resposta = Agent(
    role="Comunicador de Atendimento",
    goal="Transformar informações técnicas em respostas amigáveis e úteis",
    backstory="""
    Você é um comunicador experiente em atendimento ao cliente.
    Sua missão é pegar as informações factuais encontradas e
    transformá-las em uma resposta calorosa, útil e profissional.
    
    Características da sua comunicação:
    - Tom amigável e acolhedor
    - Informações claras e diretas
    - Sempre ofereça ajuda adicional
    - Use uma linguagem natural e humana
    
    Evite soar robótico ou muito formal.
    """,
    verbose=True,
    llm=llm,
)

# ===============================================
# DEFINIÇÃO DAS TAREFAS
# ===============================================


def criar_tarefas(pergunta_usuario):
    """Cria as tarefas para processar a pergunta do usuário"""

    # Tarefa 1: Recepção e limpeza
    tarefa_recepcao = Task(
        description=f"""
        Receba esta pergunta do cliente: "{pergunta_usuario}"
        
        Faça uma limpeza básica:
        - Corrija erros de digitação óbvios
        - Torne a pergunta mais clara
        - Mantenha o sentido original
        
        Entregue a pergunta limpa e preparada.
        """,
        agent=agente_recepcao,
        expected_output="Pergunta do cliente limpa e clara",
    )

    # Tarefa 2: Análise de intenção
    tarefa_analise = Task(
        description="""
        Analise a pergunta limpa recebida da tarefa anterior.
        
        Identifique:
        1. A intenção principal do cliente
        2. O produto mencionado
        3. Contexto adicional relevante
        
        Retorne OBRIGATORIAMENTE no formato JSON:
        {
            "intencao": "tipo_da_intencao",
            "produto": "produto_identificado", 
            "contexto": "informações_adicionais"
        }
        """,
        agent=agente_analise,
        expected_output="JSON estruturado com intenção, produto e contexto",
        context=[tarefa_recepcao],
    )

    # Tarefa 3: Busca de informações
    tarefa_pesquisa = Task(
        description=f"""
        Com base na intenção estruturada da tarefa anterior, busque as informações necessárias.
        
        Base de dados disponível:
        {PRODUTOS_DB}
        
        Instruções de busca:
        - Para "consultar_preco": retorne preço e disponibilidade
        - Para "verificar_estoque": retorne quantidade em estoque
        - Para "obter_informacoes": retorne todos os dados do produto
        
        Retorne apenas dados factuais encontrados.
        """,
        agent=agente_pesquisa,
        expected_output="Informações factuais específicas sobre o produto consultado",
        context=[tarefa_analise],
    )

    # Tarefa 4: Geração da resposta final
    tarefa_resposta = Task(
        description="""
        Transforme as informações factuais da tarefa anterior em uma resposta
        amigável e útil para o cliente.
        
        A resposta deve:
        - Ser calorosa e acolhedora
        - Responder diretamente à pergunta original
        - Incluir as informações encontradas de forma clara
        - Oferecer ajuda adicional
        - Soar natural e humana
        
        Esta é a resposta final que o cliente receberá.
        """,
        agent=agente_resposta,
        expected_output="Resposta final amigável e completa para o cliente",
        context=[tarefa_pesquisa],
    )

    return [tarefa_recepcao, tarefa_analise, tarefa_pesquisa, tarefa_resposta]


# ===============================================
# FUNÇÃO PRINCIPAL DE ATENDIMENTO
# ===============================================


def processar_atendimento(pergunta_usuario):
    """Processa uma pergunta do cliente através da cadeia de agentes"""

    print("=" * 60)
    print("🤖 SISTEMA DE ATENDIMENTO - CADEIA DE AGENTES")
    print("=" * 60)
    print(f"📝 Pergunta recebida: {pergunta_usuario}")
    print("=" * 60)

    # Criar as tarefas
    tarefas = criar_tarefas(pergunta_usuario)

    # Criar a equipe (crew)
    equipe_atendimento = Crew(
        agents=[agente_recepcao, agente_analise, agente_pesquisa, agente_resposta],
        tasks=tarefas,
        process=Process.sequential,  # Processo sequencial - um agente por vez
        verbose=True,
    )

    # Executar o processamento
    resultado = equipe_atendimento.kickoff()

    print("\n" + "=" * 60)
    print("✅ RESPOSTA FINAL PARA O CLIENTE:")
    print("=" * 60)
    print(resultado)
    print("=" * 60)

    return resultado


# ===============================================
# EXEMPLOS DE TESTE
# ===============================================


def executar_exemplos():
    """Executa alguns exemplos para demonstrar o sistema"""

    exemplos = [
        "e aí, queria saber o preço daquele notebook gamer",
        "tem smartphone em estoque?",
        "preciso de info sobre o fone bluetooth",
        "quanto custa aquele celular novo?",
    ]

    for i, exemplo in enumerate(exemplos, 1):
        print(f"\n🔄 EXEMPLO {i}")
        processar_atendimento(exemplo)

        if i < len(exemplos):
            input("\n⏸️  Pressione Enter para continuar para o próximo exemplo...")


# ===============================================
# EXECUÇÃO PRINCIPAL
# ===============================================

if __name__ == "__main__":
    print(
        """
    🎯 AULA 4 - CADEIA DE AGENTES ESPECIALIZADOS
    
    Este exemplo demonstra 4 agentes trabalhando em sequência:
    
    1. 🏢 Recepcionista: Limpa e prepara a pergunta
    2. 🔍 Analista: Extrai intenção e entidades  
    3. 📊 Pesquisador: Busca informações específicas
    4. 💬 Comunicador: Gera resposta amigável
    
    Cada agente tem uma responsabilidade específica e passa
    o resultado para o próximo na cadeia.
    """
    )

    # Escolha do modo de execução
    print("\nEscolha uma opção:")
    print("1. Executar exemplos pré-definidos")
    print("2. Fazer uma pergunta personalizada")

    escolha = input("\nDigite sua escolha (1 ou 2): ").strip()

    if escolha == "1":
        executar_exemplos()
    elif escolha == "2":
        pergunta = input("\n💬 Digite sua pergunta: ").strip()
        if pergunta:
            processar_atendimento(pergunta)
        else:
            print("❌ Pergunta não pode estar vazia!")
    else:
        print("❌ Opção inválida!")
