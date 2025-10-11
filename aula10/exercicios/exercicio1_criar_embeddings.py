#!/usr/bin/env python3
"""
Exercício 1: Criar Embeddings para Sintomas

Objetivo: Criar embeddings para todos os sintomas do banco de dados
e salvá-los para uso posterior.

Nível: 🟢 Iniciante

Tarefas:
1. Conectar ao banco SQLite
2. Ler todos os sintomas
3. Criar embeddings usando OpenAI API
4. Salvar embeddings no banco
5. Validar que foram salvos corretamente
"""

import os
import sys
import sqlite3
import json
from pathlib import Path
from typing import List, Dict
from dotenv import load_dotenv
from openai import OpenAI

# Configurar paths
load_dotenv()
PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "db" / "curso.db"


def inicializar_tabela_embeddings():
    """
    Tarefa 1: Criar tabela para armazenar embeddings
    
    TODO: Implemente a criação da tabela 'sintoma_embeddings' com:
    - sintoma_id (INTEGER PRIMARY KEY)
    - nome (TEXT NOT NULL)
    - embedding_json (TEXT NOT NULL)
    - created_at (TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # TODO: Escreva o SQL CREATE TABLE aqui
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sintoma_embeddings (
            -- Sua estrutura aqui
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Tabela criada")


def obter_sintomas() -> List[Dict]:
    """
    Tarefa 2: Ler todos os sintomas do banco
    
    TODO: Consulte a tabela ia_sintoma e retorne lista de dicionários
    com 'id' e 'nome'
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # TODO: Escreva a query SELECT aqui
    cursor.execute("""
        SELECT -- Suas colunas aqui
        FROM ia_sintoma
        ORDER BY nome
    """)
    
    sintomas = []
    for row in cursor.fetchall():
        # TODO: Crie o dicionário com id e nome
        sintoma = {
            'id': None,  # Preencha
            'nome': None  # Preencha
        }
        sintomas.append(sintoma)
    
    conn.close()
    print(f"✅ {len(sintomas)} sintomas carregados")
    return sintomas


def criar_embedding(texto: str) -> List[float]:
    """
    Tarefa 3: Criar embedding usando OpenAI API
    
    TODO: Use a API da OpenAI para criar embedding
    Modelo: text-embedding-3-small
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    try:
        # TODO: Chame client.embeddings.create()
        response = None  # Sua chamada aqui
        
        # TODO: Extraia o embedding da resposta
        embedding = None  # Extrair de response
        
        return embedding
    
    except Exception as e:
        print(f"❌ Erro ao criar embedding: {e}")
        return None


def salvar_embedding(sintoma_id: int, nome: str, embedding: List[float]):
    """
    Tarefa 4: Salvar embedding no banco
    
    TODO: Salve o embedding na tabela sintoma_embeddings
    Dica: Use json.dumps() para converter lista em JSON
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # TODO: Converter embedding para JSON
    embedding_json = None  # Use json.dumps()
    
    # TODO: INSERT no banco
    cursor.execute("""
        INSERT OR REPLACE INTO sintoma_embeddings 
        (sintoma_id, nome, embedding_json)
        VALUES (?, ?, ?)
    """, (None, None, None))  # Preencha os valores
    
    conn.commit()
    conn.close()


def processar_todos_sintomas():
    """
    Tarefa 5: Processar todos os sintomas
    
    TODO: Junte todas as funções anteriores para:
    1. Obter sintomas
    2. Para cada sintoma, criar embedding
    3. Salvar no banco
    4. Mostrar progresso
    """
    print("\n🚀 Processando sintomas...")
    
    # TODO: Obter lista de sintomas
    sintomas = []  # Chame obter_sintomas()
    
    total = len(sintomas)
    
    for idx, sintoma in enumerate(sintomas, 1):
        # TODO: Criar embedding
        embedding = None  # Chame criar_embedding()
        
        if embedding:
            # TODO: Salvar
            # Chame salvar_embedding()
            
            print(f"✅ [{idx}/{total}] {sintoma['nome']}")
        else:
            print(f"❌ [{idx}/{total}] Falha: {sintoma['nome']}")
    
    print(f"\n✅ Processamento concluído!")


def validar_embeddings():
    """
    Tarefa 6: Validar que embeddings foram salvos
    
    TODO: Consulte a tabela e mostre estatísticas:
    - Total de embeddings salvos
    - Dimensões do embedding
    - Exemplos
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # TODO: Contar total
    cursor.execute("""
        SELECT COUNT(*) FROM sintoma_embeddings
    """)
    total = cursor.fetchone()[0]
    
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   Total de embeddings: {total}")
    
    # TODO: Pegar um exemplo e mostrar dimensões
    cursor.execute("""
        SELECT nome, embedding_json
        FROM sintoma_embeddings
        LIMIT 1
    """)
    
    row = cursor.fetchone()
    if row:
        nome, embedding_json = row
        embedding = json.loads(embedding_json)
        
        print(f"   Dimensões: {len(embedding)}")
        print(f"   Exemplo: {nome}")
        print(f"   Primeiros 5 valores: {embedding[:5]}")
    
    conn.close()


def main():
    """Menu principal do exercício"""
    print("=" * 80)
    print("🎓 EXERCÍCIO 1: CRIAR EMBEDDINGS PARA SINTOMAS")
    print("=" * 80)
    
    # Verificações
    if not DB_PATH.exists():
        print(f"❌ Banco não encontrado: {DB_PATH}")
        return
    
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY não configurada!")
        return
    
    while True:
        print("\n📋 TAREFAS:")
        print("1. ✅ Inicializar tabela de embeddings")
        print("2. 🔍 Ver sintomas do banco")
        print("3. 🧪 Testar criação de 1 embedding")
        print("4. 🚀 Processar todos os sintomas")
        print("5. 📊 Validar embeddings salvos")
        print("6. 💡 Ver solução completa")
        print("7. 🚪 Sair")
        
        escolha = input("\n👉 Escolha: ").strip()
        
        if escolha == "1":
            inicializar_tabela_embeddings()
        
        elif escolha == "2":
            sintomas = obter_sintomas()
            print(f"\n📋 Primeiros 5 sintomas:")
            for s in sintomas[:5]:
                print(f"   • {s['nome']}")
        
        elif escolha == "3":
            texto = input("\n📝 Digite um texto para teste: ").strip()
            if texto:
                emb = criar_embedding(texto)
                if emb:
                    print(f"✅ Embedding criado: {len(emb)} dimensões")
        
        elif escolha == "4":
            confirma = input("\n⚠️  Isso irá processar TODOS os sintomas. Continuar? (s/n): ")
            if confirma.lower() == 's':
                processar_todos_sintomas()
        
        elif escolha == "5":
            validar_embeddings()
        
        elif escolha == "6":
            mostrar_solucao()
        
        elif escolha == "7":
            print("\n👋 Até logo!")
            break


def mostrar_solucao():
    """Mostra a solução completa do exercício"""
    print("\n" + "=" * 80)
    print("💡 SOLUÇÃO COMPLETA")
    print("=" * 80)
    
    print("""
📝 TAREFA 1 - Inicializar Tabela:

CREATE TABLE IF NOT EXISTS sintoma_embeddings (
    sintoma_id INTEGER PRIMARY KEY,
    nome TEXT NOT NULL,
    embedding_json TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

📝 TAREFA 2 - Obter Sintomas:

SELECT id, nome FROM ia_sintoma ORDER BY nome

sintoma = {
    'id': row[0],
    'nome': row[1]
}

📝 TAREFA 3 - Criar Embedding:

response = client.embeddings.create(
    input=texto,
    model="text-embedding-3-small"
)
embedding = response.data[0].embedding

📝 TAREFA 4 - Salvar Embedding:

embedding_json = json.dumps(embedding)

cursor.execute('''
    INSERT OR REPLACE INTO sintoma_embeddings 
    (sintoma_id, nome, embedding_json)
    VALUES (?, ?, ?)
''', (sintoma_id, nome, embedding_json))

📝 TAREFA 5 - Processar Todos:

sintomas = obter_sintomas()

for idx, sintoma in enumerate(sintomas, 1):
    embedding = criar_embedding(sintoma['nome'])
    if embedding:
        salvar_embedding(sintoma['id'], sintoma['nome'], embedding)

💡 DICA: Consulte o arquivo main.py da aula10 para ver implementação completa!
""")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Exercício interrompido")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
