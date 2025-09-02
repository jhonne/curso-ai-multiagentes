# Implementação Prática: Otimização de Latência com CrewAI

## Visão Geral

Este guia mostra como implementar os 7 princípios de otimização de latência da OpenAI especificamente em projetos CrewAI.

## Configuração Inicial

### 1. Configuração de Modelos por Tarefa

```python
# config/models.py
MODEL_CONFIG = {
    # Tarefas simples - usar modelos menores
    "classification": "gpt-3.5-turbo",
    "keyword_extraction": "gpt-3.5-turbo", 
    "sentiment_analysis": "gpt-3.5-turbo",
    
    # Tarefas complexas - usar modelos maiores
    "content_generation": "gpt-4o",
    "complex_reasoning": "gpt-4o",
    "creative_writing": "gpt-4o"
}
```

### 2. Templates de Prompts Otimizados

```python
# prompts/optimized_templates.py
OPTIMIZED_PROMPTS = {
    "quick_analysis": """
    Analise e retorne JSON:
    {
        "sent": "[pos/neg/neu]",
        "type": "[A/B/C]", 
        "conf": "[1-5]"
    }
    """,
    
    "brief_summary": "Resuma em máximo 10 palavras:",
    
    "classification": "Classifique como A, B ou C:",
}
```

## Implementação dos 7 Princípios

### Princípio 1: Processar Tokens Mais Rapidamente

```python
from crewai import Agent

# ✅ Agente otimizado com modelo menor
fast_analyzer = Agent(
    role="Analisador Rápido",
    goal="Análise eficiente de dados",
    backstory="Especialista em processamento rápido",
    llm="gpt-3.5-turbo",  # Modelo menor para velocidade
    max_iter=2,  # Limitar iterações
    memory=False  # Desabilitar memória se não necessária
)

# ✅ Agente para tarefas complexas
quality_responder = Agent(
    role="Especialista Sênior", 
    goal="Respostas de alta qualidade",
    backstory="Expert com anos de experiência",
    llm="gpt-4o",  # Modelo maior apenas quando necessário
    memory=True
)
```

### Princípio 2: Gerar Menos Tokens

```python
# ✅ Prompt otimizado para saída estruturada
def create_optimized_task(description: str):
    return Task(
        description=f"""
        {description}
        
        IMPORTANTE: Retorne apenas JSON válido:
        {{
            "res": "[resultado]",     # resultado principal
            "conf": "[1-5]",          # confiança
            "act": "[next_action]"    # próxima ação
        }}
        """,
        expected_output="JSON válido com campos: res, conf, act"
    )

# ❌ Evitar prompts verbosos
# "Por favor, analise cuidadosamente o texto fornecido..."

# ✅ Prompts concisos
# "Analise e retorne JSON:"
```

### Princípio 3: Usar Menos Tokens de Entrada

```python
class ContextOptimizer:
    def __init__(self, max_history: int = 3):
        self.max_history = max_history
    
    def optimize_context(self, conversation: List[Dict]) -> str:
        """Otimiza contexto para KV cache"""
        
        # Instruções fixas primeiro (melhor para cache)
        context = """
REGRAS FIXAS:
- Seja conciso
- Use formato JSON
- Mantenha tom profissional

EXEMPLOS:
Input: "Como está o tempo?"
Output: {"res": "Não tenho dados meteorológicos", "conf": "5"}

"""
        
        # Contexto dinâmico no final
        recent_msgs = conversation[-self.max_history:]
        context += "\nHISTÓRICO RECENTE:\n"
        
        for msg in recent_msgs:
            # Limitar tamanho de cada mensagem
            content = msg['content'][:100]
            context += f"- {msg['role']}: {content}\n"
        
        return context
```

### Princípio 4: Fazer Menos Requisições

```python
# ✅ Combinar múltiplas tarefas
class CombinedAnalysisAgent(Agent):
    def analyze_complete(self, text: str) -> Dict:
        """Combina análise, classificação e resposta em uma única call"""
        
        combined_prompt = f"""
        Para o texto: "{text}"
        
        Execute TODAS as etapas e retorne JSON:
        1. Analise sentimento
        2. Extraia palavras-chave (máx 3)
        3. Classifique categoria
        4. Sugira resposta (máx 15 palavras)
        
        {{
            "sentiment": "",
            "keywords": [],
            "category": "",
            "response": ""
        }}
        """
        
        return self.llm.invoke(combined_prompt)

# ❌ Evitar múltiplas requisições sequenciais
# sentiment = agent1.analyze_sentiment(text)
# keywords = agent2.extract_keywords(text)  
# category = agent3.classify(text)
```

### Princípio 5: Paralelizar

```python
import asyncio
from typing import List

class ParallelCrewProcessor:
    def __init__(self):
        self.agents = {
            'analyzer': fast_analyzer,
            'classifier': fast_analyzer, 
            'responder': quality_responder
        }
    
    async def process_parallel_tasks(self, inputs: List[str]) -> List[Dict]:
        """Processa múltiplas entradas em paralelo"""
        
        async def process_single(text: str) -> Dict:
            # Tarefas independentes podem ser paralelas
            analysis_task = asyncio.create_task(
                self.agents['analyzer'].execute(f"Analise: {text}")
            )
            
            classification_task = asyncio.create_task(
                self.agents['classifier'].execute(f"Classifique: {text}")
            )
            
            # Aguardar ambas
            analysis, classification = await asyncio.gather(
                analysis_task, classification_task
            )
            
            return {
                'analysis': analysis,
                'classification': classification
            }
        
        # Processar todos os inputs em paralelo
        tasks = [process_single(text) for text in inputs]
        return await asyncio.gather(*tasks)
    
    async def speculative_execution(self, user_input: str) -> Dict:
        """Execução especulativa para fluxos prováveis"""
        
        # Iniciar moderação E processamento simultaneamente
        moderation_task = asyncio.create_task(
            self.moderate_content(user_input)
        )
        
        processing_task = asyncio.create_task(
            self.process_content(user_input)
        )
        
        # Verificar moderação primeiro
        is_safe = await moderation_task
        
        if is_safe:
            # Usar resultado do processamento
            result = await processing_task
            return {'status': 'success', 'result': result}
        else:
            # Cancelar processamento
            processing_task.cancel()
            return {'status': 'blocked', 'reason': 'content_policy'}
```

### Princípio 6: Fazer Usuários Esperarem Menos

```python
class StreamingCrewInterface:
    def __init__(self, crew):
        self.crew = crew
    
    def stream_crew_execution(self, initial_input: str):
        """Implementa streaming para execução do crew"""
        
        # Mostrar progresso imediato
        yield "🤖 Iniciando análise..."
        
        # Executar crew com callbacks
        def step_callback(agent_name: str, task_desc: str):
            yield f"👨‍💼 {agent_name}: {task_desc[:50]}..."
        
        # Configurar crew com callback
        self.crew.step_callback = step_callback
        
        # Executar e streamar resultados
        yield "⚡ Processando dados..."
        result = self.crew.kickoff(inputs={'input': initial_input})
        
        yield "✅ Processamento concluído!"
        yield f"📋 Resultado: {result}"
    
    def chunked_response(self, long_response: str, chunk_size: int = 50):
        """Processa resposta longa em chunks"""
        
        words = long_response.split()
        
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            yield chunk
            time.sleep(0.1)  # Simula processamento
```

### Princípio 7: Não Usar LLM por Padrão

```python
class HybridCrewSystem:
    def __init__(self):
        # Respostas pré-computadas
        self.quick_responses = {
            'greeting': ['Olá!', 'Oi! Como posso ajudar?'],
            'thanks': ['De nada!', 'Sempre às ordens!'],
            'goodbye': ['Até logo!', 'Tenha um ótimo dia!']
        }
        
        # Cache de respostas
        self.response_cache = {}
        
        # Crew para casos complexos
        self.crew = None
    
    def should_use_llm(self, user_input: str) -> bool:
        """Decide se deve usar LLM ou método tradicional"""
        
        # Verificar padrões simples
        simple_patterns = [
            'oi', 'olá', 'tchau', 'obrigado', 'obrigada',
            'sim', 'não', 'ok', 'certo'
        ]
        
        if any(pattern in user_input.lower() for pattern in simple_patterns):
            return False
        
        # Verificar se é pergunta complexa
        complex_indicators = ['como', 'por que', 'quando', 'onde', 'qual']
        if any(indicator in user_input.lower() for indicator in complex_indicators):
            return True
        
        return len(user_input.split()) > 5  # Mais de 5 palavras = complexo
    
    def get_response(self, user_input: str) -> str:
        """Sistema híbrido de resposta"""
        
        # 1. Verificar respostas rápidas
        for category, responses in self.quick_responses.items():
            if self._matches_category(user_input, category):
                return random.choice(responses)
        
        # 2. Verificar cache
        if user_input in self.response_cache:
            return self.response_cache[user_input]
        
        # 3. Decidir se usar LLM
        if not self.should_use_llm(user_input):
            # Usar lógica tradicional
            return self._traditional_response(user_input)
        
        # 4. Usar LLM apenas se necessário
        llm_response = self.crew.kickoff(inputs={'input': user_input})
        self.response_cache[user_input] = llm_response
        
        return llm_response
    
    def _traditional_response(self, user_input: str) -> str:
        """Resposta usando lógica tradicional"""
        
        # Análise baseada em regras
        if '?' in user_input:
            return "Posso ajudar com informações específicas. O que você gostaria de saber?"
        
        if any(word in user_input.lower() for word in ['problema', 'erro', 'bug']):
            return "Vou conectar você com nosso suporte técnico."
        
        return "Como posso ajudar você hoje?"
```

## Exemplo de Implementação Completa

```python
class OptimizedCrewAIService:
    def __init__(self):
        # Configurar agentes otimizados
        self.setup_optimized_agents()
        
        # Configurar sistema híbrido
        self.hybrid_system = HybridCrewSystem()
        
        # Configurar monitoramento
        self.metrics = LatencyMetrics()
    
    def setup_optimized_agents(self):
        """Configura agentes com otimizações aplicadas"""
        
        # Agente rápido para análises simples
        self.fast_agent = Agent(
            role="Analisador Rápido",
            goal="Análise eficiente de entrada do usuário",
            backstory="Especialista em processamento otimizado",
            llm="gpt-3.5-turbo",
            tools=[extract_keywords_tool, classify_intent_tool]
        )
        
        # Agente de qualidade para respostas complexas
        self.quality_agent = Agent(
            role="Especialista Senior",
            goal="Gerar respostas de alta qualidade",
            backstory="Expert em atendimento personalizado",
            llm="gpt-4o"
        )
        
        # Configurar crew otimizado
        self.crew = Crew(
            agents=[self.fast_agent, self.quality_agent],
            tasks=[],  # Tarefas criadas dinamicamente
            process=Process.sequential,  # ou hierarchical
            verbose=True
        )
    
    @monitor_latency
    def process_user_request(self, user_input: str) -> Dict[str, Any]:
        """Processa requisição aplicando todas as otimizações"""
        
        # Aplicar sistema híbrido (Princípio 7)
        quick_response = self.hybrid_system.get_response(user_input)
        if quick_response and quick_response != user_input:
            return {
                'response': quick_response,
                'method': 'quick_response',
                'latency_optimizations': ['hard_coded_response']
            }
        
        # Otimizar contexto (Princípio 3)
        optimized_context = self.optimize_context_for_request(user_input)
        
        # Criar tarefa combinada (Princípio 4)
        combined_task = self.create_combined_task(user_input, optimized_context)
        
        # Executar com monitoramento
        with self.metrics.track_execution():
            result = self.crew.kickoff(inputs={'context': optimized_context})
        
        return {
            'response': result,
            'method': 'optimized_crew',
            'latency_optimizations': [
                'model_selection',
                'combined_tasks', 
                'optimized_context',
                'response_caching'
            ]
        }

# Uso do sistema otimizado
if __name__ == "__main__":
    service = OptimizedCrewAIService()
    
    # Teste com diferentes tipos de entrada
    test_cases = [
        "oi",  # Deve usar resposta rápida
        "Como posso cancelar meu plano?",  # Deve usar crew otimizado
        "Preciso de ajuda urgente com um bug"  # Deve usar crew completo
    ]
    
    for user_input in test_cases:
        result = service.process_user_request(user_input)
        print(f"Input: {user_input}")
        print(f"Response: {result['response']}")
        print(f"Method: {result['method']}")
        print(f"Optimizations: {result.get('latency_optimizations', [])}")
        print("-" * 50)
```

## Métricas e Monitoramento

```python
class LatencyMetrics:
    def __init__(self):
        self.metrics = []
    
    def track_execution(self):
        """Context manager para rastrear tempo de execução"""
        
        class ExecutionTracker:
            def __init__(self, metrics_collector):
                self.metrics = metrics_collector
                self.start_time = None
            
            def __enter__(self):
                self.start_time = time.time()
                return self
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                execution_time = time.time() - self.start_time
                self.metrics.metrics.append({
                    'timestamp': time.time(),
                    'execution_time': execution_time,
                    'success': exc_type is None
                })
        
        return ExecutionTracker(self)
    
    def get_average_latency(self) -> float:
        """Calcula latência média"""
        if not self.metrics:
            return 0.0
        
        total_time = sum(m['execution_time'] for m in self.metrics)
        return total_time / len(self.metrics)
    
    def get_performance_report(self) -> Dict:
        """Gera relatório de performance"""
        if not self.metrics:
            return {'status': 'no_data'}
        
        execution_times = [m['execution_time'] for m in self.metrics]
        
        return {
            'total_requests': len(self.metrics),
            'average_latency': statistics.mean(execution_times),
            'median_latency': statistics.median(execution_times),
            'p95_latency': statistics.quantiles(execution_times, n=20)[18],  # 95th percentile
            'success_rate': sum(1 for m in self.metrics if m['success']) / len(self.metrics)
        }
```

## Configurações Recomendadas

### Para Diferentes Cenários

```python
# Configuração para alta velocidade (sacrifica qualidade)
SPEED_CONFIG = {
    'default_model': 'gpt-3.5-turbo',
    'max_tokens': 100,
    'temperature': 0.1,
    'enable_streaming': True,
    'cache_responses': True
}

# Configuração balanceada
BALANCED_CONFIG = {
    'fast_model': 'gpt-3.5-turbo',
    'quality_model': 'gpt-4o',
    'max_tokens': 300,
    'temperature': 0.3,
    'enable_streaming': True,
    'cache_responses': True
}

# Configuração para máxima qualidade
QUALITY_CONFIG = {
    'default_model': 'gpt-4o',
    'max_tokens': 1000,
    'temperature': 0.7,
    'enable_streaming': False,
    'cache_responses': False
}
```

## Checklist de Implementação

### ✅ Tarefas Concluídas

- [ ] Configurar modelos por tipo de tarefa
- [ ] Implementar templates de prompts otimizados
- [ ] Configurar sistema de cache de respostas
- [ ] Implementar respostas hard-coded para casos simples
- [ ] Configurar execução paralela para tarefas independentes
- [ ] Implementar streaming para melhorar UX
- [ ] Configurar monitoramento de latência
- [ ] Otimizar contexto para KV cache
- [ ] Implementar sistema híbrido (LLM + tradicional)
- [ ] Configurar métricas de performance

### 📊 Métricas para Acompanhar

1. **Latência Média**: < 2 segundos
2. **P95 de Latência**: < 5 segundos  
3. **Cache Hit Rate**: > 40%
4. **Quick Response Rate**: > 30%
5. **Satisfação do Usuário**: > 4.5/5

## Recursos Adicionais

- [Documentação CrewAI](https://docs.crewai.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [Guia de Otimização OpenAI](./GUIA_OTIMIZACAO_LATENCIA_OPENAI.md)
