#!/usr/bin/env python3
"""
Exemplo 2: Introdução a Embeddings

Demonstra criação e uso básico de embeddings.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI
import numpy as np

# Configurar paths
load_dotenv()
PROJECT_ROOT = Path(__file__).parent.parent.parent


def criar_embedding_simples(texto: str):
    """Cria um embedding para um texto"""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    print(f"\n📝 Texto: '{texto}'")
    print("🔄 Criando embedding...")
    
    try:
        response = client.embeddings.create(
            input=texto,
            model="text-embedding-3-small"
        )
        
        embedding = response.data[0].embedding
        
        print(f"✅ Embedding criado!")
        print(f"📊 Dimensões: {len(embedding)}")
        print(f"📈 Primeiros 10 valores: {embedding[:10]}")
        print(f"🔢 Tipo de dados: float")
        print(f"💾 Tamanho aproximado: {len(embedding) * 4 / 1024:.2f} KB")
        
        return embedding
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None


def comparar_embeddings(texto1: str, texto2: str):
    """Compara similaridade entre dois textos"""
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    print(f"\n🔬 COMPARANDO EMBEDDINGS")
    print("=" * 60)
    print(f"📝 Texto 1: '{texto1}'")
    print(f"📝 Texto 2: '{texto2}'")
    
    # Criar embeddings
    print("\n🔄 Criando embeddings...")
    response = client.embeddings.create(
        input=[texto1, texto2],
        model="text-embedding-3-small"
    )
    
    emb1 = np.array(response.data[0].embedding)
    emb2 = np.array(response.data[1].embedding)
    
    # Calcular similaridade coseno
    dot_product = np.dot(emb1, emb2)
    norm1 = np.linalg.norm(emb1)
    norm2 = np.linalg.norm(emb2)
    similaridade = dot_product / (norm1 * norm2)
    
    print(f"\n📊 RESULTADO:")
    print(f"   Similaridade coseno: {similaridade:.4f}")
    print(f"   Percentual: {similaridade * 100:.2f}%")
    
    # Interpretar
    print(f"\n💡 INTERPRETAÇÃO:")
    if similaridade > 0.9:
        print("   ✅ MUITO SIMILAR - Praticamente sinônimos")
    elif similaridade > 0.7:
        print("   🟢 RELACIONADO - Conceitos próximos")
    elif similaridade > 0.5:
        print("   🟡 ALGO RELACIONADO - Mesmo domínio")
    else:
        print("   🔴 DIFERENTES - Conceitos distintos")
    
    return similaridade


def visualizar_espaco_vetorial():
    """Visualiza conceito de espaço vetorial (simplificado)"""
    print("\n" + "=" * 80)
    print("🌌 ESPAÇO VETORIAL (Conceito Simplificado)")
    print("=" * 80)
    
    print("""
🎯 CONCEITO:
   • Cada texto vira um ponto no espaço de 1536 dimensões
   • Textos similares ficam PRÓXIMOS
   • Textos diferentes ficam DISTANTES
   
📐 VISUALIZAÇÃO 2D (real é 1536D!):

      cefaleia •
            ↗︎
  dor de cabeça •
            ↘︎
       enxaqueca •
       
       
                    • dor no estômago
                    (LONGE - conceito diferente)

💡 MATEMÁTICA:
   Distância = sqrt(sum((v1[i] - v2[i])²))
   Similaridade coseno = dot(v1, v2) / (||v1|| * ||v2||)
""")


def demonstracao_interativa():
    """Demonstração interativa de embeddings"""
    print("\n" + "=" * 80)
    print("🧪 DEMONSTRAÇÃO INTERATIVA DE EMBEDDINGS")
    print("=" * 80)
    
    exemplos = [
        ("dor de cabeça", "cefaleia", "Sinônimos médicos"),
        ("febre", "hipertermia", "Termos relacionados"),
        ("tosse", "náusea", "Sintomas diferentes"),
        ("hospital", "dor de cabeça", "Conceitos não relacionados")
    ]
    
    for texto1, texto2, descricao in exemplos:
        print(f"\n📌 Caso: {descricao}")
        input("   Pressione ENTER para testar...")
        
        similaridade = comparar_embeddings(texto1, texto2)
        
        continuar = input("\n➡️  Próximo exemplo? (s/n): ")
        if continuar.lower() != 's':
            break


def testar_proprios_textos():
    """Permite usuário testar seus próprios textos"""
    print("\n" + "=" * 80)
    print("✏️  TESTE SEUS PRÓPRIOS TEXTOS")
    print("=" * 80)
    
    while True:
        print("\n📝 Digite dois textos para comparar:")
        texto1 = input("   Texto 1: ").strip()
        texto2 = input("   Texto 2: ").strip()
        
        if not texto1 or not texto2:
            print("❌ Ambos textos são necessários!")
            continue
        
        comparar_embeddings(texto1, texto2)
        
        continuar = input("\n➡️  Testar outros textos? (s/n): ")
        if continuar.lower() != 's':
            break


if __name__ == "__main__":
    # Verificar API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY não configurada!")
        print("💡 Execute: uv run configurar.py")
        sys.exit(1)
    
    print("🎓 EXEMPLO 2: INTRODUÇÃO A EMBEDDINGS")
    print("=" * 80)
    
    # Menu
    while True:
        print("\n📋 OPÇÕES:")
        print("1. Criar embedding de um texto")
        print("2. Comparar dois textos")
        print("3. Demonstração interativa")
        print("4. Testar seus próprios textos")
        print("5. Visualizar conceito de espaço vetorial")
        print("6. Sair")
        
        escolha = input("\n👉 Escolha: ").strip()
        
        if escolha == "1":
            texto = input("\n📝 Digite o texto: ").strip()
            if texto:
                criar_embedding_simples(texto)
        
        elif escolha == "2":
            texto1 = input("\n📝 Texto 1: ").strip()
            texto2 = input("📝 Texto 2: ").strip()
            if texto1 and texto2:
                comparar_embeddings(texto1, texto2)
        
        elif escolha == "3":
            demonstracao_interativa()
        
        elif escolha == "4":
            testar_proprios_textos()
        
        elif escolha == "5":
            visualizar_espaco_vetorial()
        
        elif escolha == "6":
            print("\n👋 Até logo!")
            break
        
        else:
            print("\n❌ Opção inválida!")
