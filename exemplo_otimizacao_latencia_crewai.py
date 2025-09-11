"""
Exemplo de Otimização de Latência com CrewAI
Demonstra aplicação dos 7 princípios de otimização da OpenAI
"""

import asyncio
import time
from functools import wraps
from typing import List, Dict, Any
from crewai import Agent, Task, Crew
from crewai.tools import tool


# Decorator para monitorar latência
def monitor_latency(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print(f"⏱️ {func.__name__}: {(end - start) * 1000:.2f}ms")
        return result

    return wrapper


# Princípio 1: Processar tokens mais rapidamente - Usar modelos menores para tarefas específicas
@tool
def extract_keywords_fast(text: str) -> List[str]:
    """Extrai palavras-chave usando GPT-3.5 em vez de GPT-4"""
    # Implementação otimizada com modelo menor
    pass


# Princípio 2: Gerar menos tokens - Prompts concisos e estrutura otimizada
OPTIMIZED_PROMPTS = {
    "analysis": """
    Analise o texto e retorne JSON:
    {
        "sent": "[pos/neg/neu]",     # sentiment
        "type": "[query/complaint/info]",  # type
        "priority": "[1-5]",         # priority level
        "response": "[brief response]"  # max 20 words
    }
    """,
    "summary": "Resuma em máximo 15 palavras:",
    "classification": "Classifique como: A|B|C|D (apenas letra):",
}


# Princípio 3: Usar menos tokens de entrada - Contexto otimizado
def optimize_context(conversation_history: List[Dict], max_messages: int = 3) -> str:
    """Otimiza contexto mantendo apenas mensagens relevantes"""
    # Manter apenas últimas N mensagens
    recent_messages = conversation_history[-max_messages:]

    # Template otimizado para KV cache
    context = """
INSTRUÇÕES FIXAS:
- Seja conciso
- Use formato JSON quando solicitado
- Mantenha tom profissional

HISTÓRICO RECENTE:
"""
    for msg in recent_messages:
        context += f"- {msg['role']}: {msg['content'][:100]}...\n"

    return context


# Princípio 4: Fazer menos requisições - Combinar etapas
class OptimizedAgent(Agent):
    """Agente otimizado que combina múltiplas tarefas"""

    @monitor_latency
    def process_combined_task(self, user_input: str) -> Dict[str, Any]:
        """Combina análise, classificação e resposta em uma única requisição"""

        combined_prompt = f"""
        Execute todas as etapas para: {user_input}
        
        1. Analise sentimento (pos/neg/neu)
        2. Classifique tipo (pergunta/reclamação/info)
        3. Determine prioridade (1-5)
        4. Gere resposta (máx 20 palavras)
        
        Retorne JSON:
        {{
            "sentiment": "",
            "type": "",
            "priority": "",
            "response": ""
        }}
        """

        # Uma única chamada em vez de 4 separadas
        return self.llm.invoke(combined_prompt)


# Princípio 5: Paralelizar - Executar tarefas independentes em paralelo
async def parallel_analysis(texts: List[str]) -> List[Dict]:
    """Analisa múltiplos textos em paralelo"""

    async def analyze_single(text: str) -> Dict:
        # Simula análise individual
        await asyncio.sleep(0.1)  # Simula latência
        return {"text": text, "analysis": "completed"}

    # Executar em paralelo
    tasks = [analyze_single(text) for text in texts]
    results = await asyncio.gather(*tasks)

    return results


# Princípio 6: Fazer usuários esperarem menos - Streaming e chunking
class StreamingCrewAI:
    """Implementa streaming para melhorar experiência do usuário"""

    def __init__(self):
        self.crew = None

    def stream_response(self, query: str):
        """Simula streaming de resposta"""
        response_parts = [
            "Analisando sua solicitação...",
            "Processando dados...",
            "Gerando resposta...",
            "Finalizando...",
        ]

        for part in response_parts:
            yield part
            time.sleep(0.5)  # Simula processamento

    def show_progress(self, steps: List[str]):
        """Mostra progresso das etapas"""
        for i, step in enumerate(steps, 1):
            print(f"[{i}/{len(steps)}] {step}")
            time.sleep(0.3)


# Princípio 7: Não usar LLM por padrão - Hard-coding para respostas simples
class HybridResponseSystem:
    """Sistema híbrido que usa LLM apenas quando necessário"""

    # Respostas pré-definidas (hard-coded)
    QUICK_RESPONSES = {
        "obrigado": ["De nada!", "Fico feliz em ajudar!", "Sempre às ordens!"],
        "oi": ["Olá!", "Oi! Como posso ajudar?", "Olá! Em que posso auxiliar?"],
        "tchau": ["Até logo!", "Tenha um ótimo dia!", "Volte sempre!"],
    }

    # Cache de respostas computadas
    response_cache = {}

    def get_response(self, user_input: str) -> str:
        """Decide se usa resposta hard-coded, cache ou LLM"""

        # 1. Verificar respostas rápidas
        for keyword, responses in self.QUICK_RESPONSES.items():
            if keyword in user_input.lower():
                return random.choice(responses)

        # 2. Verificar cache
        if user_input in self.response_cache:
            return self.response_cache[user_input]

        # 3. Usar LLM apenas se necessário
        llm_response = self._generate_llm_response(user_input)
        self.response_cache[user_input] = llm_response

        return llm_response

    def _generate_llm_response(self, user_input: str) -> str:
        """Gera resposta usando LLM"""
        # Implementação com LLM
        pass


# Exemplo de uso integrado
class OptimizedCustomerServiceCrew:
    """Crew de atendimento otimizado aplicando todos os princípios"""

    def __init__(self):
        # Agente otimizado para análise rápida (GPT-3.5)
        self.analyzer = Agent(
            role="Analisador Rápido",
            goal="Analisar rapidamente consultas de clientes",
            backstory="Especialista em análise eficiente de sentimentos e classificação",
            llm="gpt-3.5-turbo",  # Modelo menor para velocidade
            tools=[extract_keywords_fast],
        )

        # Agente para respostas complexas (GPT-4)
        self.responder = Agent(
            role="Especialista em Respostas",
            goal="Gerar respostas de alta qualidade",
            backstory="Expert em atendimento ao cliente com foco na qualidade",
            llm="gpt-4o",  # Modelo maior apenas quando necessário
        )

        self.hybrid_system = HybridResponseSystem()
        self.streaming_system = StreamingCrewAI()

    @monitor_latency
    async def process_request(self, user_input: str) -> Dict[str, Any]:
        """Processa requisição aplicando todos os princípios de otimização"""

        # Princípio 7: Verificar se precisa de LLM
        quick_response = self.hybrid_system.get_response(user_input)
        if quick_response:
            return {"response": quick_response, "method": "hardcoded"}

        # Princípio 6: Mostrar progresso
        steps = ["Analisando entrada", "Classificando tipo", "Gerando resposta"]
        self.streaming_system.show_progress(steps)

        # Princípio 3: Otimizar contexto
        optimized_context = optimize_context([])

        # Princípio 4 + 5: Combinar e paralelizar quando possível
        analysis_task = Task(
            description=f"Analise rapidamente: {user_input}",
            agent=self.analyzer,
            expected_output="JSON com análise",
        )

        # Executar crew otimizado
        crew = Crew(
            agents=[self.analyzer, self.responder], tasks=[analysis_task], verbose=True
        )

        result = crew.kickoff()

        return {
            "response": result,
            "method": "optimized_crew",
            "optimizations_applied": [
                "Modelo menor para análise",
                "Contexto otimizado",
                "Tarefas combinadas",
                "Progresso visualizado",
            ],
        }


# Demonstração
async def demonstrate_optimizations():
    """Demonstra as otimizações em ação"""

    print("🚀 Demonstração de Otimizações de Latência CrewAI\n")

    # Instanciar sistema otimizado
    service = OptimizedCustomerServiceCrew()

    # Teste com diferentes tipos de entrada
    test_inputs = [
        "obrigado",  # Deve usar resposta hard-coded
        "Como posso cancelar minha assinatura?",  # Deve usar LLM otimizado
        "Qual o horário de funcionamento?",  # Deve usar análise completa
    ]

    for i, user_input in enumerate(test_inputs, 1):
        print(f"\n--- Teste {i}: '{user_input}' ---")

        # Medir tempo total
        start_time = time.time()
        result = await service.process_request(user_input)
        total_time = time.time() - start_time

        print(f"✅ Resultado: {result['response']}")
        print(f"⚡ Método: {result['method']}")
        print(f"⏱️ Tempo total: {total_time * 1000:.2f}ms")

        if "optimizations_applied" in result:
            print("🔧 Otimizações aplicadas:")
            for opt in result["optimizations_applied"]:
                print(f"   - {opt}")


if __name__ == "__main__":
    # Executar demonstração
    asyncio.run(demonstrate_optimizations())
