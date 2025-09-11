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
        Analise esta mensagem do usuário: "{mensagem_usuario}"
        
        RESPONDA EXATAMENTE no seguinte formato:
        
        TIPO DE SOLICITAÇÃO: [Pergunta informativa/Pedido de ajuda/Reclamação/Solicitação de serviço/Conversa casual]
        
        TÓPICO PRINCIPAL: [Descreva o assunto central em uma frase]
        
        PALAVRAS-CHAVE: [Liste 3-5 palavras importantes]
        
        URGÊNCIA: [Baixa/Média/Alta] - [Breve justificativa]
        
        SENTIMENTO: [Positivo/Neutro/Negativo] - [Observações sobre o tom]
        
        RECOMENDAÇÃO: [Próximo passo sugerido em uma frase]
        """,
        expected_output="""
        Relatório estruturado de triagem seguindo exatamente o formato solicitado com:
        - Tipo de solicitação claramente identificado
        - Tópico principal resumido
        - Lista de palavras-chave relevantes
        - Nível de urgência com justificativa
        - Análise de sentimento com observações
        - Recomendação clara para próximos passos
        """,
        agent=agente_triagem,
    )


def criar_tarefa_intencao(agente_intencao, tarefa_triagem):
    """
    Cria tarefa de análise de intenção - entende o que usuário quer
    """
    return Task(
        description="""
        Com base na triagem inicial, analise a intenção do usuário.
        
        RESPONDA EXATAMENTE no seguinte formato:
        
        OBJETIVO REAL: [O que o usuário realmente quer alcançar]
        
        CONTEXTO IMPLÍCITO: [Informações subentendidas ou background provável]
        
        TIPO DE RESPOSTA IDEAL: [Explicação técnica/Resposta simples/Tutorial/Lista de opções]
        
        INFORMAÇÕES NECESSÁRIAS: [Dados específicos que precisamos abordar]
        
        ABORDAGEM COMUNICATIVA: [Como devemos comunicar - tom e estilo]
        """,
        expected_output="""
        Análise estruturada de intenção seguindo exatamente o formato com:
        - Objetivo real identificado claramente
        - Contexto e background provável do usuário
        - Tipo de resposta mais adequado especificado
        - Lista específica de informações necessárias
        - Sugestões claras de abordagem comunicativa
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
        Com base nas análises anteriores, organize as informações necessárias.
        
        RESPONDA EXATAMENTE no seguinte formato:
        
        INFORMAÇÕES PRINCIPAIS: [Dados centrais e conceitos fundamentais sobre o tópico]
        
        INFORMAÇÕES COMPLEMENTARES: [Detalhes relevantes, exemplos práticos e casos de uso]
        
        ESTRUTURA DA RESPOSTA: [Como organizar - sequência lógica de apresentação]
        
        PONTOS DE DESTAQUE: [Aspectos que merecem ênfase especial]
        
        VERIFICAÇÃO: [Confirmação de completude e relevância das informações]
        """,
        expected_output="""
        Conjunto estruturado de informações seguindo o formato com:
        - Dados principais organizados sobre o tópico
        - Informações complementares com exemplos práticos
        - Estrutura clara sugerida para a resposta final
        - Lista de pontos que merecem destaque especial
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
        Crie a resposta final usando TODAS as análises anteriores.
        
        A resposta deve seguir estas diretrizes:
        
        1. CLARA E ESTRUTURADA: Use linguagem apropriada e organize logicamente
        
        2. COMPLETA MAS CONCISA: Responda completamente mas vá direto ao ponto
        
        3. ÚTIL E PRÁTICA: Inclua informações aplicáveis e exemplos relevantes
        
        4. AMIGÁVEL E PROFISSIONAL: Use tom adequado e seja empático
        
        IMPORTANTE: Baseie-se nas análises de triagem, intenção e busca para criar 
        uma resposta específica e relevante para a pergunta original do usuário.
        
        NÃO use respostas genéricas. Use as informações específicas coletadas.
        """,
        expected_output="""
        Resposta final completa que:
        - Atende diretamente à pergunta original do usuário
        - Está organizada de forma clara e lógica
        - Usa linguagem apropriada e tom amigável
        - Inclui informações práticas e relevantes
        - Demonstra ter usado todas as análises anteriores
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
