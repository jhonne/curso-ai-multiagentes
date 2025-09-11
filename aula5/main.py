#!/usr/bin/env python3
"""
Aula 5: Otimização e Configuração Avançada dos Agentes

Este arquivo demonstra os conceitos principais da aula através de exemplos práticos.
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
import time
import json
from datetime import datetime

# Carrega variáveis de ambiente
load_dotenv()


class AgenteOtimizado:
    """
    Classe base para criar agentes com configurações otimizadas
    """

    def __init__(
        self,
        role,
        goal,
        backstory,
        model="gpt-3.5-turbo",
        temperature=0.7,
        max_tokens=1000,
    ):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.metrics = {"tokens_used": 0, "execution_time": 0, "success_rate": 0}

    def create_agent(self, tools=None):
        """Cria um agente CrewAI com configurações otimizadas"""
        return Agent(
            role=self.role,
            goal=self.goal,
            backstory=self.backstory,
            tools=tools or [],
            verbose=True,
            allow_delegation=False,
            llm_config={
                "model": self.model,
                "temperature": self.temperature,
                "max_tokens": self.max_tokens,
            },
        )

    def log_performance(self, start_time, tokens_used):
        """Registra métricas de performance"""
        execution_time = time.time() - start_time
        self.metrics["execution_time"] = execution_time
        self.metrics["tokens_used"] += tokens_used

        print(f"\n📊 Métricas do Agente {self.role}:")
        print(f"⏱️  Tempo de execução: {execution_time:.2f}s")
        print(f"🔤 Tokens utilizados: {tokens_used}")
        print(f"💰 Custo estimado: ${(tokens_used * 0.002):.4f}")


def exemplo_prompt_engineering():
    """
    Demonstra técnicas avançadas de prompt engineering
    """
    print("\n🎯 === EXEMPLO: PROMPT ENGINEERING AVANÇADO ===")

    # Prompt básico vs otimizado
    prompt_basico = "Analise este texto"

    prompt_otimizado = """
    Você é um analista de conteúdo especializado em extrair insights acionáveis.
    
    CONTEXTO: Análise de feedback de clientes
    OBJETIVO: Identificar padrões e sugestões de melhoria
    
    FORMATO DE RESPOSTA:
    1. Resumo executivo (max 50 palavras)
    2. Principais insights (máximo 3 pontos)
    3. Ações recomendadas (máximo 3 ações)
    
    EXEMPLO:
    Texto: "O produto é bom, mas a entrega demorou muito"
    Resposta:
    1. Cliente satisfeito com produto, insatisfeito com logística
    2. Insights: Qualidade mantida, logística precisa melhorar
    3. Ações: Revisar processo de entrega, comunicar prazos melhor
    
    Analise o seguinte texto:
    """

    print(f"❌ Prompt básico: {prompt_basico}")
    print(f"✅ Prompt otimizado: {prompt_otimizado[:200]}...")
    print("\n💡 Diferenças:")
    print("- Contexto específico")
    print("- Formato estruturado de resposta")
    print("- Exemplo prático (few-shot learning)")
    print("- Limitações claras de tamanho")


def exemplo_configuracao_modelos():
    """
    Demonstra configuração de diferentes modelos para diferentes tipos de agentes
    """
    print("\n⚙️ === EXEMPLO: CONFIGURAÇÃO DE MODELOS ===")

    # Configurações por tipo de agente
    configs = {
        "agente_criativo": {
            "model": "gpt-4",
            "temperature": 0.9,  # Alta criatividade
            "max_tokens": 2000,
            "top_p": 0.9,
        },
        "agente_analitico": {
            "model": "gpt-3.5-turbo",
            "temperature": 0.1,  # Baixa variabilidade
            "max_tokens": 1000,
            "top_p": 0.1,
        },
        "agente_conversacional": {
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,  # Equilibrado
            "max_tokens": 500,
            "top_p": 0.8,
        },
    }

    for tipo, config in configs.items():
        print(f"\n🤖 {tipo.upper()}:")
        for param, valor in config.items():
            print(f"  {param}: {valor}")

        # Explicação da configuração
        if "criativo" in tipo:
            print("  📝 Foco: Geração de conteúdo original e criativo")
        elif "analitico" in tipo:
            print("  📊 Foco: Análise precisa e consistente")
        elif "conversacional" in tipo:
            print("  💬 Foco: Interação natural e fluida")


def exemplo_sistema_cache():
    """
    Demonstra implementação de cache para otimizar custos
    """
    print("\n💾 === EXEMPLO: SISTEMA DE CACHE ===")

    class CacheSimples:
        def __init__(self):
            self.cache = {}
            self.hits = 0
            self.misses = 0

        def get_hash(self, prompt):
            """Gera hash simples do prompt"""
            return hash(prompt.strip().lower())

        def get(self, prompt):
            """Busca resposta no cache"""
            key = self.get_hash(prompt)
            if key in self.cache:
                self.hits += 1
                print(f"✅ Cache HIT para prompt: {prompt[:50]}...")
                return self.cache[key]
            else:
                self.misses += 1
                print(f"❌ Cache MISS para prompt: {prompt[:50]}...")
                return None

        def set(self, prompt, response):
            """Armazena resposta no cache"""
            key = self.get_hash(prompt)
            self.cache[key] = response
            print(f"💾 Resposta armazenada no cache")

        def stats(self):
            """Estatísticas do cache"""
            total = self.hits + self.misses
            hit_rate = (self.hits / total * 100) if total > 0 else 0
            return {
                "hits": self.hits,
                "misses": self.misses,
                "hit_rate": f"{hit_rate:.1f}%",
            }

    # Demonstração
    cache = CacheSimples()

    prompts_teste = [
        "Qual é a capital do Brasil?",
        "Como fazer um bolo de chocolate?",
        "Qual é a capital do Brasil?",  # Repetido - deve usar cache
        "Explique machine learning",
        "Como fazer um bolo de chocolate?",  # Repetido - deve usar cache
    ]

    for prompt in prompts_teste:
        resposta = cache.get(prompt)
        if not resposta:
            # Simula resposta da API
            resposta = f"Resposta simulada para: {prompt}"
            cache.set(prompt, resposta)

    print(f"\n📈 Estatísticas do Cache: {cache.stats()}")
    print("💡 Taxa de cache de 40% = 40% de economia em tokens!")


def main():
    """
    Função principal que executa todos os exemplos
    """
    print("🚀 AULA 5: OTIMIZAÇÃO E CONFIGURAÇÃO AVANÇADA DOS AGENTES")
    print("=" * 70)

    # Executa exemplos
    exemplo_prompt_engineering()
    exemplo_configuracao_modelos()
    exemplo_sistema_cache()

    print("\n✅ Exemplos concluídos!")
    print("\n📚 Próximos passos:")
    print("1. Execute os exemplos na pasta 'exemplos/'")
    print("2. Complete os exercícios na pasta 'exercicios/'")
    print("3. Use os templates para seus próprios agentes")
    print("\n💡 Dica: Use sempre verbose=True durante desenvolvimento!")


if __name__ == "__main__":
    main()
