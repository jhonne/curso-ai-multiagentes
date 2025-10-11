#!/usr/bin/env python3
"""
Aula 10: Embeddings e Busca Semântica vs. SQLite Tradicional

Sistema interativo que demonstra a diferença entre busca SQL tradicional
e busca semântica com embeddings.

Autor: Curso CrewAI
"""

import os
import sys
import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Tuple
import numpy as np
from dotenv import load_dotenv
from openai import OpenAI

# Carregar variáveis de ambiente
load_dotenv()

# Configurar paths
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "db" / "curso.db"


class EmbeddingManager:
    """Gerenciador de embeddings com cache em SQLite"""
    
    def __init__(self, db_path: str = str(DB_PATH)):
        self.db_path = db_path
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = "text-embedding-3-small"
        self._inicializar_tabela_embeddings()
    
    def _inicializar_tabela_embeddings(self):
        """Cria tabela para armazenar embeddings se não existir"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sintoma_embeddings (
                sintoma_id INTEGER PRIMARY KEY,
                nome TEXT NOT NULL,
                embedding_json TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
        print("✅ Tabela de embeddings inicializada")
    
    def criar_embedding(self, texto: str) -> List[float]:
        """Cria embedding usando OpenAI API"""
        try:
            response = self.client.embeddings.create(
                input=texto,
                model=self.model
            )
            embedding = response.data[0].embedding
            print(f"✅ Embedding criado: {len(embedding)} dimensões")
            return embedding
        except Exception as e:
            print(f"❌ Erro ao criar embedding: {e}")
            return None
    
    def salvar_embedding(self, sintoma_id: int, nome: str, embedding: List[float]):
        """Salva embedding no banco"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        embedding_json = json.dumps(embedding)
        
        cursor.execute("""
            INSERT OR REPLACE INTO sintoma_embeddings (sintoma_id, nome, embedding_json)
            VALUES (?, ?, ?)
        """, (sintoma_id, nome, embedding_json))
        
        conn.commit()
        conn.close()
        print(f"✅ Embedding salvo para: {nome}")
    
    def obter_embedding(self, sintoma_id: int) -> List[float]:
        """Obtém embedding do banco"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT embedding_json FROM sintoma_embeddings
            WHERE sintoma_id = ?
        """, (sintoma_id,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return json.loads(result[0])
        return None
    
    def listar_todos_embeddings(self) -> List[Tuple[int, str, List[float]]]:
        """Lista todos os embeddings salvos"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT sintoma_id, nome, embedding_json
            FROM sintoma_embeddings
        """)
        
        resultados = []
        for row in cursor.fetchall():
            sintoma_id, nome, embedding_json = row
            embedding = json.loads(embedding_json)
            resultados.append((sintoma_id, nome, embedding))
        
        conn.close()
        return resultados
    
    def criar_embeddings_todos_sintomas(self):
        """Cria embeddings para todos os sintomas do banco"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, nome FROM ia_sintoma ORDER BY nome")
        sintomas = cursor.fetchall()
        conn.close()
        
        print(f"\n🚀 Criando embeddings para {len(sintomas)} sintomas...")
        
        for idx, (sintoma_id, nome) in enumerate(sintomas, 1):
            # Verificar se já existe
            if self.obter_embedding(sintoma_id):
                print(f"⏭️  [{idx}/{len(sintomas)}] Embedding já existe: {nome}")
                continue
            
            # Criar embedding
            embedding = self.criar_embedding(nome)
            if embedding:
                self.salvar_embedding(sintoma_id, nome, embedding)
                print(f"✅ [{idx}/{len(sintomas)}] Processado: {nome}")
        
        print(f"\n✅ Embeddings criados com sucesso!")


class BuscaSemantica:
    """Busca semântica usando similaridade de vetores"""
    
    def __init__(self, embedding_manager: EmbeddingManager):
        self.em = embedding_manager
    
    def similaridade_coseno(self, vec1: List[float], vec2: List[float]) -> float:
        """Calcula similaridade coseno entre dois vetores"""
        vec1_np = np.array(vec1)
        vec2_np = np.array(vec2)
        
        dot_product = np.dot(vec1_np, vec2_np)
        norm1 = np.linalg.norm(vec1_np)
        norm2 = np.linalg.norm(vec2_np)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        return dot_product / (norm1 * norm2)
    
    def buscar_similares(self, query: str, top_k: int = 5) -> List[Dict]:
        """Busca sintomas similares usando embeddings"""
        print(f"\n🔍 Buscando semanticamente: '{query}'")
        
        # Criar embedding da query
        query_embedding = self.em.criar_embedding(query)
        if not query_embedding:
            return []
        
        # Obter todos os embeddings
        todos_embeddings = self.em.listar_todos_embeddings()
        
        # Calcular similaridades
        resultados = []
        for sintoma_id, nome, embedding in todos_embeddings:
            similaridade = self.similaridade_coseno(query_embedding, embedding)
            resultados.append({
                'id': sintoma_id,
                'nome': nome,
                'similaridade': similaridade
            })
        
        # Ordenar por similaridade (descendente)
        resultados.sort(key=lambda x: x['similaridade'], reverse=True)
        
        return resultados[:top_k]


class BuscaTradicionalSQL:
    """Busca tradicional usando SQL LIKE"""
    
    def __init__(self, db_path: str = str(DB_PATH)):
        self.db_path = db_path
    
    def buscar_like(self, query: str) -> List[Dict]:
        """Busca usando SQL LIKE (case-insensitive)"""
        print(f"\n🗄️  Buscando com SQL LIKE: '{query}'")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Busca case-insensitive
        pattern = f"%{query}%"
        cursor.execute("""
            SELECT id, nome
            FROM ia_sintoma
            WHERE LOWER(nome) LIKE LOWER(?)
            ORDER BY nome
        """, (pattern,))
        
        resultados = []
        for row in cursor.fetchall():
            resultados.append({
                'id': row[0],
                'nome': row[1]
            })
        
        conn.close()
        return resultados


class ComparadorBuscas:
    """Compara busca SQL tradicional vs busca semântica"""
    
    def __init__(self):
        self.em = EmbeddingManager()
        self.busca_semantica = BuscaSemantica(self.em)
        self.busca_sql = BuscaTradicionalSQL()
    
    def comparar(self, query: str, top_k: int = 5):
        """Executa ambas buscas e compara resultados"""
        print("\n" + "=" * 80)
        print(f"🔬 COMPARAÇÃO: SQL LIKE vs BUSCA SEMÂNTICA")
        print("=" * 80)
        print(f"📝 Query: \"{query}\"")
        
        # Busca SQL
        print("\n" + "-" * 80)
        print("🗄️  BUSCA SQL TRADICIONAL (LIKE)")
        print("-" * 80)
        resultados_sql = self.busca_sql.buscar_like(query)
        
        if resultados_sql:
            print(f"\n✅ Encontrados {len(resultados_sql)} resultados:")
            for idx, r in enumerate(resultados_sql[:top_k], 1):
                print(f"  {idx}. {r['nome']}")
        else:
            print("\n❌ Nenhum resultado encontrado com SQL LIKE")
        
        # Busca Semântica
        print("\n" + "-" * 80)
        print("🧠 BUSCA SEMÂNTICA (EMBEDDINGS)")
        print("-" * 80)
        resultados_semantica = self.busca_semantica.buscar_similares(query, top_k)
        
        if resultados_semantica:
            print(f"\n✅ Top {top_k} resultados por similaridade:")
            for idx, r in enumerate(resultados_semantica, 1):
                similaridade_percent = r['similaridade'] * 100
                print(f"  {idx}. {r['nome']:<40} ({similaridade_percent:.1f}% similar)")
        else:
            print("\n❌ Nenhum embedding encontrado")
        
        # Análise comparativa
        print("\n" + "=" * 80)
        print("📊 ANÁLISE COMPARATIVA")
        print("=" * 80)
        
        sql_count = len(resultados_sql)
        semantic_count = len(resultados_semantica)
        
        print(f"\n📌 Resultados SQL: {sql_count}")
        print(f"🧠 Resultados Semânticos: {semantic_count}")
        
        if semantic_count > sql_count:
            diferenca = semantic_count - sql_count
            print(f"\n✅ Busca semântica encontrou {diferenca} resultado(s) adicional(is)!")
        elif sql_count > semantic_count:
            print(f"\n⚠️  SQL encontrou mais resultados (busca mais ampla)")
        else:
            print(f"\n🤝 Ambas encontraram a mesma quantidade")
        
        # Mostrar vantagens de cada abordagem
        print("\n💡 VANTAGENS:")
        print("\n🗄️  SQL LIKE:")
        print("   ✅ Muito rápido (índices)")
        print("   ✅ Sem custo de API")
        print("   ❌ Precisa match exato de substring")
        print("   ❌ Não entende sinônimos")
        
        print("\n🧠 BUSCA SEMÂNTICA:")
        print("   ✅ Entende significado e contexto")
        print("   ✅ Encontra sinônimos automaticamente")
        print("   ✅ Tolerante a variações")
        print("   ❌ Custo de API para criar embeddings (uma vez)")
        print("   ⚡ Busca é rápida depois de embeddings criados")


def menu_principal():
    """Menu interativo principal"""
    comparador = ComparadorBuscas()
    
    while True:
        print("\n" + "=" * 80)
        print("🎓 AULA 10: EMBEDDINGS E BUSCA SEMÂNTICA")
        print("=" * 80)
        print("\n📋 MENU PRINCIPAL:")
        print("1. 🔬 Comparar SQL vs Embeddings (busca interativa)")
        print("2. 🧪 Demonstração com exemplos pré-definidos")
        print("3. 🚀 Criar embeddings de todos os sintomas")
        print("4. 📊 Estatísticas dos embeddings")
        print("5. ❓ Ajuda - Quando usar cada abordagem")
        print("6. 🚪 Sair")
        
        escolha = input("\n👉 Escolha uma opção: ").strip()
        
        if escolha == "1":
            query = input("\n📝 Digite sua busca: ").strip()
            if query:
                comparador.comparar(query)
        
        elif escolha == "2":
            demonstracao_exemplos(comparador)
        
        elif escolha == "3":
            print("\n🚀 Iniciando criação de embeddings...")
            resposta = input("⚠️  Isso irá consumir API da OpenAI. Continuar? (s/n): ")
            if resposta.lower() == 's':
                comparador.em.criar_embeddings_todos_sintomas()
        
        elif escolha == "4":
            mostrar_estatisticas(comparador.em)
        
        elif escolha == "5":
            mostrar_ajuda()
        
        elif escolha == "6":
            print("\n👋 Até logo!")
            break
        
        else:
            print("\n❌ Opção inválida!")


def demonstracao_exemplos(comparador: ComparadorBuscas):
    """Demonstração com exemplos pré-definidos"""
    exemplos = [
        ("dor de cabeça", "Mostra sinônimos como 'cefaleia'"),
        ("problemas respiratórios", "Encontra 'dispneia', 'falta de ar', etc."),
        ("febre alta", "Busca semântica vs literal"),
        ("dor no peito", "Termos médicos relacionados")
    ]
    
    print("\n" + "=" * 80)
    print("🧪 DEMONSTRAÇÃO COM EXEMPLOS PRÉ-DEFINIDOS")
    print("=" * 80)
    
    for idx, (query, descricao) in enumerate(exemplos, 1):
        print(f"\n📌 Exemplo {idx}: {descricao}")
        input("   Pressione ENTER para continuar...")
        comparador.comparar(query, top_k=5)
        
        if idx < len(exemplos):
            continuar = input("\n➡️  Próximo exemplo? (s/n): ")
            if continuar.lower() != 's':
                break


def mostrar_estatisticas(em: EmbeddingManager):
    """Mostra estatísticas dos embeddings"""
    todos = em.listar_todos_embeddings()
    
    print("\n" + "=" * 80)
    print("📊 ESTATÍSTICAS DOS EMBEDDINGS")
    print("=" * 80)
    
    print(f"\n💾 Total de embeddings salvos: {len(todos)}")
    
    if todos:
        # Tamanho do primeiro embedding
        dimensoes = len(todos[0][2])
        print(f"📏 Dimensões por embedding: {dimensoes}")
        
        # Tamanho em memória (aproximado)
        tamanho_mb = (len(todos) * dimensoes * 4) / (1024 * 1024)  # 4 bytes por float
        print(f"💾 Tamanho aproximado em memória: {tamanho_mb:.2f} MB")
        
        # Listar alguns exemplos
        print(f"\n📋 Primeiros 5 sintomas com embeddings:")
        for idx, (sid, nome, _) in enumerate(todos[:5], 1):
            print(f"  {idx}. {nome} (ID: {sid})")


def mostrar_ajuda():
    """Mostra guia de quando usar cada abordagem"""
    print("\n" + "=" * 80)
    print("❓ GUIA: QUANDO USAR CADA ABORDAGEM")
    print("=" * 80)
    
    print("\n✅ USE SQL LIKE QUANDO:")
    print("   • Busca exata de substring")
    print("   • Dados bem estruturados")
    print("   • Performance crítica")
    print("   • Sem custo de API permitido")
    print("   • Exemplos: IDs, códigos, datas")
    
    print("\n✅ USE BUSCA SEMÂNTICA QUANDO:")
    print("   • Usuário usa linguagem natural")
    print("   • Precisa encontrar sinônimos")
    print("   • Busca por significado/contexto")
    print("   • Recomendações por similaridade")
    print("   • Exemplos: descrições, sintomas, textos livres")
    
    print("\n🎯 ABORDAGEM HÍBRIDA (MELHOR):")
    print("   • Filtre com SQL primeiro (rápido)")
    print("   • Depois use busca semântica (preciso)")
    print("   • Exemplo: Filtrar por região + buscar sintomas similares")


if __name__ == "__main__":
    # Verificar banco de dados
    if not DB_PATH.exists():
        print(f"❌ Banco de dados não encontrado: {DB_PATH}")
        print(f"💡 Execute primeiro: uv run db/migrar_postgres_para_sqlite.py")
        sys.exit(1)
    
    # Verificar API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("❌ OPENAI_API_KEY não configurada no .env")
        print("💡 Execute: uv run configurar.py")
        sys.exit(1)
    
    # Iniciar menu
    try:
        menu_principal()
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
