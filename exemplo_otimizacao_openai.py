#!/usr/bin/env python3
"""
Script de exemplo implementando as boas práticas de otimização OpenAI
extraídas do guia da Holori para uso com CrewAI.
"""

import os
import time
import hashlib
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI


@dataclass
class TokenUsage:
    """Classe para rastrear uso de tokens."""
    input_tokens: int
    output_tokens: int
    cached_tokens: int = 0
    model: str = "gpt-4o-mini"
    
    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens
    
    @property
    def estimated_cost(self) -> float:
        """Calcula custo estimado baseado nos preços atuais."""
        pricing = {
            "gpt-4o-mini": {"input": 0.15/1000000, "output": 0.60/1000000, "cache": 0.075/1000000},
            "gpt-4o": {"input": 2.50/1000000, "output": 10.00/1000000, "cache": 1.25/1000000},
            "gpt-4": {"input": 30.00/1000000, "output": 60.00/1000000, "cache": 15.00/1000000}
        }
        
        if self.model not in pricing:
            return 0.0
            
        prices = pricing[self.model]
        cost = (
            self.input_tokens * prices["input"] +
            self.output_tokens * prices["output"] +
            self.cached_tokens * prices["cache"]
        )
        return cost


class IntelligentCache:
    """Sistema de cache inteligente para respostas da OpenAI."""
    
    def __init__(self, ttl: int = 3600):
        self.cache: Dict[str, tuple] = {}
        self.ttl = ttl
        self.hit_count = 0
        self.miss_count = 0
    
    def _generate_key(self, prompt: str, model: str, temperature: float, **kwargs) -> str:
        """Gera chave única para cache."""
        key_data = f"{prompt}|{model}|{temperature}|{kwargs}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def get(self, prompt: str, model: str, temperature: float, **kwargs) -> Optional[str]:
        """Recupera resposta do cache se válida."""
        key = self._generate_key(prompt, model, temperature, **kwargs)
        
        if key in self.cache:
            timestamp, response = self.cache[key]
            if time.time() - timestamp < self.ttl:
                self.hit_count += 1
                print(f"✅ Cache HIT - Economizou uma chamada API")
                return response
            else:
                del self.cache[key]
        
        self.miss_count += 1
        return None
    
    def set(self, prompt: str, model: str, temperature: float, response: str, **kwargs):
        """Armazena resposta no cache."""
        key = self._generate_key(prompt, model, temperature, **kwargs)
        self.cache[key] = (time.time(), response)
    
    def get_stats(self) -> Dict[str, Any]:
        """Retorna estatísticas do cache."""
        total_requests = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "cache_hits": self.hit_count,
            "cache_misses": self.miss_count,
            "hit_rate": f"{hit_rate:.1f}%",
            "cached_items": len(self.cache)
        }


class CrewAIOptimizer:
    """Classe principal para otimização de custos em CrewAI."""
    
    def __init__(self, budget_limit: float = 10.0):
        self.budget_limit = budget_limit
        self.total_cost = 0.0
        self.cache = IntelligentCache()
        self.usage_history: List[TokenUsage] = []
        
        # Configuração otimizada do LLM
        self.llm_economico = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            max_tokens=1000,
            model_kwargs={"frequency_penalty": 0.1}  # Reduz repetições
        )
        
        self.llm_premium = ChatOpenAI(
            model="gpt-4o",
            temperature=0.1,
            max_tokens=2000
        )
    
    def get_optimized_llm(self, complexity: str = "low") -> ChatOpenAI:
        """Retorna LLM otimizado baseado na complexidade da tarefa."""
        if complexity in ["high", "complex", "advanced"]:
            print("🔥 Usando GPT-4o para tarefa complexa")
            return self.llm_premium
        else:
            print("⚡ Usando GPT-4o Mini para tarefa simples")
            return self.llm_economico
    
    def create_optimized_agent(self, 
                             role: str, 
                             goal: str, 
                             backstory: str,
                             complexity: str = "low",
                             **kwargs) -> Agent:
        """Cria agente otimizado para custo."""
        
        # Backstory conciso mas efetivo
        optimized_backstory = self._optimize_backstory(backstory)
        
        return Agent(
            role=role,
            goal=goal,
            backstory=optimized_backstory,
            llm=self.get_optimized_llm(complexity),
            verbose=False,  # Reduz output desnecessário
            allow_delegation=False,  # Evita delegações custosas
            **kwargs
        )
    
    def create_optimized_task(self,
                            description: str,
                            agent: Agent,
                            expected_output: str,
                            max_words: int = 200,
                            **kwargs) -> Task:
        """Cria tarefa otimizada com limite de output."""
        
        # Adiciona limite de palavras na descrição
        optimized_description = f"""
        {description}
        
        IMPORTANTE: Limite sua resposta a no máximo {max_words} palavras.
        Seja conciso e direto ao ponto.
        """
        
        return Task(
            description=optimized_description.strip(),
            agent=agent,
            expected_output=f"{expected_output} (máximo {max_words} palavras)",
            **kwargs
        )
    
    def create_optimized_crew(self,
                            agents: List[Agent],
                            tasks: List[Task],
                            process: Process = Process.sequential,
                            **kwargs) -> Crew:
        """Cria crew otimizada para custo."""
        
        return Crew(
            agents=agents,
            tasks=tasks,
            process=process,
            verbose=False,          # Reduz logs
            memory=False,           # Desativa se não necessário
            planning=False,         # Desativa se não necessário
            full_output=True,       # Para rastreamento de custo
            **kwargs
        )
    
    def execute_with_monitoring(self, crew: Crew) -> Dict[str, Any]:
        """Executa crew com monitoramento de custo."""
        
        print(f"💰 Orçamento atual: ${self.budget_limit:.2f}")
        print(f"💸 Gasto acumulado: ${self.total_cost:.4f}")
        
        if self.total_cost >= self.budget_limit:
            raise ValueError(f"❌ Orçamento excedido! Limite: ${self.budget_limit:.2f}")
        
        start_time = time.time()
        
        try:
            # Executa crew
            result = crew.kickoff()
            
            # Calcula custo estimado
            estimated_cost = self._estimate_execution_cost(result)
            self.total_cost += estimated_cost
            
            execution_time = time.time() - start_time
            
            # Registra estatísticas
            self._log_execution_stats(estimated_cost, execution_time, result)
            
            return {
                "result": result,
                "cost": estimated_cost,
                "execution_time": execution_time,
                "total_cost": self.total_cost,
                "budget_remaining": self.budget_limit - self.total_cost
            }
            
        except Exception as e:
            print(f"❌ Erro na execução: {e}")
            raise
    
    def _optimize_backstory(self, backstory: str) -> str:
        """Otimiza backstory para ser conciso mas efetivo."""
        if len(backstory.split()) > 50:
            print("⚠️  Backstory muito longo, considere resumir para economia")
        return backstory[:300] + "..." if len(backstory) > 300 else backstory
    
    def _estimate_execution_cost(self, result) -> float:
        """Estima custo de execução baseado no resultado."""
        if hasattr(result, 'raw'):
            text_length = len(str(result.raw))
        else:
            text_length = len(str(result))
        
        # Estimativa conservadora: 1 caractere ≈ 0.25 tokens
        estimated_tokens = text_length * 0.25
        
        # Assume uso do modelo econômico
        token_usage = TokenUsage(
            input_tokens=int(estimated_tokens * 0.3),  # 30% input
            output_tokens=int(estimated_tokens * 0.7), # 70% output
            model="gpt-4o-mini"
        )
        
        self.usage_history.append(token_usage)
        return token_usage.estimated_cost
    
    def _log_execution_stats(self, cost: float, execution_time: float, result):
        """Registra estatísticas da execução."""
        print(f"\n📊 ESTATÍSTICAS DA EXECUÇÃO:")
        print(f"   💰 Custo estimado: ${cost:.6f}")
        print(f"   ⏱️  Tempo execução: {execution_time:.2f}s")
        print(f"   📝 Tamanho resultado: {len(str(result))} caracteres")
        print(f"   💸 Total gasto: ${self.total_cost:.4f}")
        print(f"   💳 Orçamento restante: ${self.budget_limit - self.total_cost:.4f}")
        
        # Estatísticas do cache
        cache_stats = self.cache.get_stats()
        print(f"   🚀 Cache hit rate: {cache_stats['hit_rate']}")
        print(f"   📦 Itens em cache: {cache_stats['cached_items']}")
    
    def get_usage_report(self) -> Dict[str, Any]:
        """Gera relatório de uso detalhado."""
        if not self.usage_history:
            return {"message": "Nenhuma execução registrada"}
        
        total_tokens = sum(usage.total_tokens for usage in self.usage_history)
        total_cost = sum(usage.estimated_cost for usage in self.usage_history)
        
        return {
            "execucoes": len(self.usage_history),
            "total_tokens": int(total_tokens),
            "total_cost": f"${total_cost:.6f}",
            "cost_per_execution": f"${total_cost/len(self.usage_history):.6f}",
            "cache_stats": self.cache.get_stats(),
            "budget_utilization": f"{(total_cost/self.budget_limit)*100:.1f}%"
        }


# Exemplo de uso prático
def exemplo_agencia_marketing_otimizada():
    """Exemplo de agência de marketing otimizada para custo."""
    
    print("🚀 Iniciando exemplo de agência de marketing otimizada")
    
    # Configura otimizador com orçamento de $1
    optimizer = CrewAIOptimizer(budget_limit=1.0)
    
    # Cria agentes otimizados
    pesquisador = optimizer.create_optimized_agent(
        role="Pesquisador de Mercado",
        goal="Analisar tendências e público-alvo",
        backstory="Especialista em pesquisa de mercado com foco em dados acionáveis.",
        complexity="low"  # Tarefa simples, usa modelo econômico
    )
    
    estrategista = optimizer.create_optimized_agent(
        role="Estrategista de Marketing",
        goal="Desenvolver estratégias baseadas em dados",
        backstory="Estrategista experiente que cria campanhas eficazes e mensuráveis.",
        complexity="medium"  # Pode precisar de mais poder de processamento
    )
    
    # Cria tarefas otimizadas
    tarefa_pesquisa = optimizer.create_optimized_task(
        description="Analise o mercado de produtos eco-friendly para millennials brasileiros",
        agent=pesquisador,
        expected_output="Resumo com 3 insights principais sobre o mercado",
        max_words=150
    )
    
    tarefa_estrategia = optimizer.create_optimized_task(
        description="Baseado na pesquisa, crie uma estratégia de marketing digital",
        agent=estrategista,
        expected_output="Estratégia com 3 táticas específicas e mensuráveis",
        max_words=200,
        context=[tarefa_pesquisa]
    )
    
    # Cria crew otimizada
    agencia = optimizer.create_optimized_crew(
        agents=[pesquisador, estrategista],
        tasks=[tarefa_pesquisa, tarefa_estrategia]
    )
    
    # Executa com monitoramento
    try:
        resultado = optimizer.execute_with_monitoring(agencia)
        
        print(f"\n✅ EXECUÇÃO CONCLUÍDA!")
        print(f"📊 Resultado:\n{resultado['result']}")
        
        # Relatório final
        relatorio = optimizer.get_usage_report()
        print(f"\n📋 RELATÓRIO DE USO:")
        for key, value in relatorio.items():
            print(f"   {key}: {value}")
            
    except Exception as e:
        print(f"❌ Erro: {e}")


def dicas_economia_adicional():
    """Dicas adicionais para economia de custos."""
    
    print("\n💡 DICAS ADICIONAIS DE ECONOMIA:")
    print("""
    1. 🎯 Escolha do Modelo:
       • GPT-4o Mini: Tarefas simples, análises básicas
       • GPT-4o: Apenas para raciocínio complexo
       • Fine-tuning: Para tarefas muito específicas
    
    2. ⚡ Otimização de Prompts:
       • Seja específico e conciso
       • Use exemplos quando necessário
       • Limite o tamanho da resposta
    
    3. 🚀 Cache Inteligente:
       • Cache respostas similares
       • TTL apropriado por tipo de conteúdo
       • Monitore hit rate do cache
    
    4. 📊 Monitoramento:
       • Defina orçamentos claros
       • Monitore em tempo real
       • Relatórios regulares de uso
    
    5. 🔄 Batch Processing:
       • Use Batch API quando possível (50% desconto)
       • Agrupe tarefas similares
       • Processe em horários de menor demanda
    
    6. 🏢 Configurações Empresariais:
       • Negocie contratos de volume
       • Considere descontos anuais
       • Avalie alternativas (Claude, Mistral)
    """)


if __name__ == "__main__":
    # Verifica se API key está configurada
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ Configure a OPENAI_API_KEY no arquivo .env")
        print("💡 Execute: uv run configurar-crewai")
        exit(1)
    
    print("🎯 Exemplo de Otimização OpenAI para CrewAI")
    print("=" * 50)
    
    # Executa exemplo
    exemplo_agencia_marketing_otimizada()
    
    # Mostra dicas adicionais
    dicas_economia_adicional()
    
    print("\n🎉 Exemplo concluído! Use essas práticas em seus projetos.")