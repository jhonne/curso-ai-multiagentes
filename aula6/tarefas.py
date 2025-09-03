"""
Aula 6 - Definição das Tarefas

Este arquivo contém templates e funções para criar tarefas
para os diferentes agentes do sistema.

Cada tarefa define:
- Description (o que fazer)
- Expected_output (resultado esperado)
- Agent (quem vai executar)
- Context (dados de tarefas anteriores)
"""

from crewai import Task


def criar_tarefa_triagem(mensagem_usuario, agente_triagem):
    """
    Cria tarefa de triagem - primeira análise da mensagem
    """
    return Task(
        description=f"""
        Faça a triagem inicial desta mensagem do usuário: "{mensagem_usuario}"
        
        Sua análise deve incluir:
        
        1. TIPO DE SOLICITAÇÃO:
           - Pergunta informativa
           - Pedido de ajuda técnica
           - Reclamação ou problema
           - Solicitação de serviço
           - Conversa casual
        
        2. TÓPICO PRINCIPAL:
           - Identifique o assunto central
           - Palavras-chave importantes
        
        3. NÍVEL DE URGÊNCIA:
           - Baixa (informação geral)
           - Média (dúvida específica)
           - Alta (problema urgente)
        
        4. SENTIMENTO:
           - Positivo, neutro ou negativo
           - Nível de frustração se houver
        
        Seja claro e objetivo na classificação.
        """,
        expected_output="""
        Relatório de triagem com:
        - Tipo de solicitação identificado
        - Tópico principal e palavras-chave
        - Nível de urgência (baixa/média/alta)
        - Análise de sentimento
        - Recomendações para próximos passos
        """,
        agent=agente_triagem,
    )


def criar_tarefa_intencao(agente_intencao, tarefa_triagem):
    """
    Cria tarefa de análise de intenção - entende o que usuário quer
    """
    return Task(
        description="""
        Com base na triagem inicial, analise profundamente a intenção do usuário.
        
        Determine:
        
        1. OBJETIVO REAL:
           - O que o usuário realmente quer alcançar?
           - Existe uma necessidade por trás da pergunta?
        
        2. CONTEXTO IMPLÍCITO:
           - Que informações estão subentendidas?
           - Qual pode ser o background do usuário?
        
        3. TIPO DE RESPOSTA IDEAL:
           - Explicação técnica detalhada
           - Resposta simples e direta
           - Tutorial passo-a-passo
           - Lista de opções/alternativas
        
        4. INFORMAÇÕES NECESSÁRIAS:
           - Que dados precisamos buscar?
           - Que aspectos devem ser abordados?
        
        Use a análise de triagem para refinar sua compreensão.
        """,
        expected_output="""
        Análise de intenção contendo:
        - Objetivo real do usuário
        - Contexto e background provável
        - Tipo de resposta mais adequado
        - Lista de informações necessárias para resposta completa
        - Sugestões de abordagem comunicativa
        """,
        agent=agente_intencao,
        context=[tarefa_triagem],
    )


def criar_tarefa_busca(agente_busca, tarefa_triagem, tarefa_intencao):
    """
    Cria tarefa de busca/processamento de informações
    """
    return Task(
        description="""
        Com base nas análises anteriores, processe as informações necessárias.
        
        Organize:
        
        1. INFORMAÇÕES PRINCIPAIS:
           - Dados centrais sobre o tópico
           - Fatos importantes e atuais
           - Conceitos fundamentais
        
        2. INFORMAÇÕES COMPLEMENTARES:
           - Detalhes relevantes
           - Exemplos práticos
           - Casos de uso
        
        3. ESTRUTURA DA RESPOSTA:
           - Como organizar as informações
           - Sequência lógica de apresentação
           - Pontos que merecem destaque
        
        4. VERIFICAÇÕES:
           - Informações estão corretas?
           - São relevantes para o usuário?
           - Falta algum aspecto importante?
        
        Use tanto a triagem quanto a análise de intenção para guiar sua pesquisa.
        """,
        expected_output="""
        Conjunto organizado de informações incluindo:
        - Dados principais sobre o tópico
        - Informações complementares relevantes
        - Estrutura sugerida para a resposta
        - Exemplos práticos quando aplicável
        - Verificação de completude e relevância
        """,
        agent=agente_busca,
        context=[tarefa_triagem, tarefa_intencao],
    )


def criar_tarefa_resposta(
    agente_resposta, tarefa_triagem, tarefa_intencao, tarefa_busca
):
    """
    Cria tarefa de formulação da resposta final
    """
    return Task(
        description="""
        Crie a resposta final para o usuário usando todas as análises anteriores.
        
        A resposta deve ser:
        
        1. CLARA E ESTRUTURADA:
           - Linguagem apropriada ao usuário
           - Organização lógica das informações
           - Parágrafos bem definidos
        
        2. COMPLETA MAS CONCISA:
           - Responde completamente à pergunta
           - Não é muito longa nem muito curta
           - Vai direto ao ponto
        
        3. ÚTIL E PRÁTICA:
           - Informações aplicáveis
           - Exemplos quando necessário
           - Próximos passos se relevante
        
        4. AMIGÁVEL E PROFISSIONAL:
           - Tom adequado ao contexto
           - Empático quando necessário
           - Convida para mais perguntas
        
        Use TODAS as informações das análises anteriores para criar a melhor resposta.
        """,
        expected_output="""
        Resposta final completa e bem estruturada que:
        - Atende completamente à necessidade do usuário
        - Está organizada de forma clara e lógica
        - Usa linguagem apropriada e tom amigável
        - Inclui informações práticas e relevantes
        - Convida para interação futura se apropriado
        """,
        agent=agente_resposta,
        context=[tarefa_triagem, tarefa_intencao, tarefa_busca],
    )


def criar_tarefas_completas(mensagem_usuario, agentes):
    """
    Cria o conjunto completo de tarefas interconectadas

    Args:
        mensagem_usuario: A mensagem que o usuário enviou
        agentes: Dicionário com os agentes {triagem, intencao, busca, resposta}

    Returns:
        Lista de tarefas na ordem correta de execução
    """

    # Criar tarefas na sequência correta
    tarefa_triagem = criar_tarefa_triagem(mensagem_usuario, agentes["triagem"])

    tarefa_intencao = criar_tarefa_intencao(agentes["intencao"], tarefa_triagem)

    tarefa_busca = criar_tarefa_busca(agentes["busca"], tarefa_triagem, tarefa_intencao)

    tarefa_resposta = criar_tarefa_resposta(
        agentes["resposta"], tarefa_triagem, tarefa_intencao, tarefa_busca
    )

    return [tarefa_triagem, tarefa_intencao, tarefa_busca, tarefa_resposta]


# Versões simplificadas para exemplos básicos
def criar_tarefas_simples(mensagem, agente1, agente2, agente3):
    """
    Versão simplificada para exemplos introdutórios
    """

    tarefa1 = Task(
        description=f'Analise esta pergunta: "{mensagem}"',
        expected_output="Análise da pergunta do usuário",
        agent=agente1,
    )

    tarefa2 = Task(
        description="Processe informações sobre o tópico identificado",
        expected_output="Informações organizadas sobre o tópico",
        agent=agente2,
        context=[tarefa1],
    )

    tarefa3 = Task(
        description="Crie uma resposta final clara e útil",
        expected_output="Resposta final para o usuário",
        agent=agente3,
        context=[tarefa1, tarefa2],
    )

    return [tarefa1, tarefa2, tarefa3]


if __name__ == "__main__":
    """
    Teste para verificar se as funções estão funcionando
    """
    print("📝 Testando criação de tarefas...")

    # Este é só um teste de sintaxe - não executa as tarefas
    from agentes import criar_todos_agentes

    agentes = criar_todos_agentes()
    mensagem_teste = "Como funciona inteligência artificial?"

    try:
        tarefas = criar_tarefas_completas(mensagem_teste, agentes)
        print(f"✅ {len(tarefas)} tarefas criadas com sucesso!")

        for i, tarefa in enumerate(tarefas, 1):
            print(f"   {i}. {tarefa.agent.role}")

    except Exception as e:
        print(f"❌ Erro ao criar tarefas: {e}")

    print("\n🎯 Teste de criação concluído!")
