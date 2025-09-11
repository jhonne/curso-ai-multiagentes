"""
Template Base para Exercícios - Aula 4
Sistema de Cadeia de Agentes Especializados

Use este template como ponto de partida para implementar seus exercícios.
Já inclui todas as práticas de segurança e economia de custos.
"""

import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# =============================================================================
# 1. VERIFICAÇÃO BÁSICA
# =============================================================================

if not os.getenv("OPENAI_API_KEY"):
    print("⚠️  Configure a API key: $env:OPENAI_API_KEY='sua_chave'")
    exit(1)

# =============================================================================
# 2. CONFIGURAÇÃO OTIMIZADA PARA ECONOMIA
# =============================================================================

llm_economico = ChatOpenAI(
    model="gpt-4o-mini",  # 85% mais barato que GPT-4o
    temperature=0.1,  # Consistência
    max_tokens=500,  # Limite de custo
)

# =============================================================================
# 3. MONITOR DE CUSTOS (OBRIGATÓRIO)
# =============================================================================


class MonitorCustos:
    def __init__(self, orcamento=1.0):
        self.orcamento = orcamento
        self.gasto = 0.0
        # Preços GPT-4o Mini (por 1M tokens)
        self.precos = {"input": 0.15 / 1000000, "output": 0.60 / 1000000}

    def estimar_custo(self, entrada):
        tokens = len(entrada) * 0.25 + 500  # entrada + saída estimada
        return tokens * 0.60 / 1000000  # usar preço output (mais alto)

    def verificar_orcamento(self, custo):
        if self.gasto + custo > self.orcamento:
            raise Exception(f"❌ Orçamento excedido! ${self.gasto:.4f}")

    def registrar_gasto(self, custo):
        self.gasto += custo
        print(f"💰 Custo: ${custo:.6f} | Total: ${self.gasto:.4f}")


# =============================================================================
# 4. VALIDAÇÃO DE ENTRADA (OBRIGATÓRIO)
# =============================================================================


def validar_entrada(texto, min_chars=10, max_chars=2000):
    """Valida entrada do usuário"""
    if not texto or len(texto) < min_chars:
        raise ValueError(f"Entrada muito curta. Mínimo {min_chars} caracteres.")
    if len(texto) > max_chars:
        raise ValueError(f"Entrada muito longa. Máximo {max_chars} caracteres.")
    return True


# =============================================================================
# 5. TEMPLATE DE AGENTES
# =============================================================================


def criar_agentes():
    """
    MODIFIQUE ESTA FUNÇÃO PARA SEU EXERCÍCIO

    Exemplo para sistema de 3 agentes:
    - Agente 1: Análise inicial
    - Agente 2: Processamento
    - Agente 3: Resposta final
    """

    agente1 = Agent(
        role="Seu Papel Aqui",
        goal="Seu objetivo específico",
        backstory="História breve (máx 200 chars para economia)",
        llm=llm_economico,
        verbose=False,  # Economia: reduz output
    )

    agente2 = Agent(
        role="Segundo Agente",
        goal="Segundo objetivo",
        backstory="Segunda história breve",
        llm=llm_economico,
        verbose=False,
    )

    agente3 = Agent(
        role="Terceiro Agente",
        goal="Terceiro objetivo",
        backstory="Terceira história breve",
        llm=llm_economico,
        verbose=False,
    )

    return [agente1, agente2, agente3]


# =============================================================================
# 6. TEMPLATE DE TAREFAS
# =============================================================================


def criar_tarefas(agentes, entrada_usuario):
    """
    MODIFIQUE ESTA FUNÇÃO PARA SEU EXERCÍCIO

    Crie tarefas que se conectam em sequência usando context=[]
    """

    agente1, agente2, agente3 = agentes

    tarefa1 = Task(
        description=f"""
        Sua primeira tarefa com: {entrada_usuario}
        
        LIMITE: Responda em máximo 150 palavras.
        """,
        agent=agente1,
        expected_output="Resultado específico da tarefa 1",
    )

    tarefa2 = Task(
        description="""
        Segunda tarefa baseada no resultado anterior.
        
        LIMITE: Responda em máximo 150 palavras.
        """,
        agent=agente2,
        expected_output="Resultado específico da tarefa 2",
        context=[tarefa1],  # IMPORTANTE: Recebe resultado da tarefa1
    )

    tarefa3 = Task(
        description="""
        Tarefa final: gere resposta amigável para o usuário.
        
        LIMITE: Responda em máximo 200 palavras.
        """,
        agent=agente3,
        expected_output="Resposta final para o usuário",
        context=[tarefa2],  # IMPORTANTE: Recebe resultado da tarefa2
    )

    return [tarefa1, tarefa2, tarefa3]


# =============================================================================
# 7. FUNÇÃO PRINCIPAL
# =============================================================================


def processar_entrada(entrada_usuario):
    """Processa entrada através da cadeia de agentes"""

    # Monitor de custos
    monitor = MonitorCustos(orcamento=0.10)  # Baixo para testes

    try:
        # 1. Validar entrada
        validar_entrada(entrada_usuario)

        # 2. Verificar custo
        custo = monitor.estimar_custo(entrada_usuario)
        monitor.verificar_orcamento(custo)

        print("🚀 Iniciando processamento...")

        # 3. Criar agentes e tarefas
        agentes = criar_agentes()
        tarefas = criar_tarefas(agentes, entrada_usuario)

        # 4. Criar crew
        crew = Crew(
            agents=agentes,
            tasks=tarefas,
            process=Process.sequential,
            verbose=False,  # Economia
        )

        # 5. Executar
        resultado = crew.kickoff()

        # 6. Registrar custo
        monitor.registrar_gasto(custo)

        return resultado

    except Exception as e:
        print(f"❌ Erro: {e}")
        return None


# =============================================================================
# 8. EXECUÇÃO E TESTES
# =============================================================================


def main():
    """Função principal com menu interativo"""

    print(
        """
    🎯 TEMPLATE BASE - EXERCÍCIOS AULA 4
    
    Modifique as funções:
    - criar_agentes(): Defina seus agentes especializados
    - criar_tarefas(): Defina as tarefas da cadeia
    
    Inclui automaticamente:
    ✅ Economia máxima (GPT-4o Mini)
    ✅ Monitor de custos
    ✅ Validação de entrada
    ✅ Estrutura de cadeia sequencial
    """
    )

    # Exemplos para teste
    exemplos = [
        "Analise este produto: Smartphone XYZ",
        "Crie um roteiro de viagem para Paris",
        "Avalie este currículo: João, programador Python",
    ]

    print("\nOpções:")
    print("1. Testar com exemplos")
    print("2. Entrada personalizada")

    escolha = input("\nEscolha (1 ou 2): ").strip()

    if escolha == "1":
        for i, exemplo in enumerate(exemplos, 1):
            print(f"\n{'='*50}")
            print(f"🧪 TESTE {i}: {exemplo}")
            print(f"{'='*50}")

            resultado = processar_entrada(exemplo)
            if resultado:
                print(f"✅ Resultado:\n{resultado}")

            if i < len(exemplos):
                input("\n⏸️ Enter para próximo teste...")

    elif escolha == "2":
        entrada = input("\n💬 Digite sua entrada: ").strip()
        if entrada:
            resultado = processar_entrada(entrada)
            if resultado:
                print(f"\n✅ Resultado:\n{resultado}")
        else:
            print("❌ Entrada vazia!")

    else:
        print("❌ Opção inválida!")


# =============================================================================
# 9. CHECKLIST PARA IMPLEMENTAÇÃO
# =============================================================================

"""
📋 CHECKLIST PARA SEU EXERCÍCIO:

OBRIGATÓRIO ✅:
[ ] Modificar criar_agentes() com seus agentes especializados
[ ] Modificar criar_tarefas() com sua cadeia específica
[ ] Definir role, goal, backstory específicos para seu domínio
[ ] Usar context=[] para conectar tarefas em sequência
[ ] Testar com entradas válidas e inválidas

ECONOMIA 💰:
[ ] Manter llm_economico (GPT-4o Mini)
[ ] Manter max_tokens baixo (500)
[ ] Manter verbose=False
[ ] Backstories breves (máx 200 chars)
[ ] Expected outputs específicos

SEGURANÇA 🛡️:
[ ] Validação de entrada ativa
[ ] Limites de caracteres configurados
[ ] Monitor de custos funcionando
[ ] Tratamento de erros implementado

QUALIDADE 🎯:
[ ] Agentes realmente especializados
[ ] Comunicação clara entre tarefas
[ ] Output final útil para o usuário
[ ] Código bem documentado
"""

# =============================================================================
# 10. EXECUÇÃO
# =============================================================================

if __name__ == "__main__":
    main()
