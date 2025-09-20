"""
Configuração PostgreSQL Real - Aula 7
=====================================

Sistema de banco PostgreSQL com suporte a:
- pgvector para embeddings
- PostGIS para geolocalização  
- Busca semântica avançada
- Cache inteligente de embeddings
- Integração com OpenAI Embeddings API

Execute primeiro:
uv add psycopg2-binary pgvector-python openai python-dotenv

Para configurar PostgreSQL localmente:
docker run --name postgres-crewai \
  -e POSTGRES_PASSWORD=senha123 \
  -e POSTGRES_DB=crewai_medico \
  -p 5432:5432 \
  -d pgvector/pgvector:pg16
"""

import os
import json
import hashlib
import time
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from dotenv import load_dotenv

import psycopg2
from psycopg2.extras import RealDictCursor
from pgvector.psycopg2 import register_vector

from openai import OpenAI
import numpy as np

# Carregar variáveis de ambiente
load_dotenv()


class PostgreSQLMedico:
    """Classe para gerenciar PostgreSQL com embeddings e busca semântica"""
    
    def __init__(self):
        """Inicializa conexão PostgreSQL e OpenAI"""
        self.conn = None
        self.openai_client = OpenAI()
        self.cache_embeddings = {}
        self.cache_ttl = 3600  # 1 hora
        
        # Configurações do banco
        self.db_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': os.getenv('POSTGRES_PORT', '5432'),
            'database': os.getenv('POSTGRES_DB', 'curso'),
            'user': os.getenv('POSTGRES_USER', 'postgres'),
            'password': os.getenv('POSTGRES_PASSWORD', 'arpus')
        }
        
        self._conectar()
        self._configurar_extensoes()
        self._criar_schema()
        
        # Mensagem final consolidada removida - interface mais limpa
    
    def _conectar(self):
        """Estabelece conexão com PostgreSQL"""
        try:
            self.conn = psycopg2.connect(**self.db_config)
            self.conn.autocommit = True
            register_vector(self.conn)  # Registra suporte a pgvector
            
            # Testar conexão
            cursor = self.conn.cursor()
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0]
            # Mensagem simplificada para interface limpa
            print("🗄️ PostgreSQL conectado")
            
        except Exception as e:
            print(f"❌ Erro ao conectar PostgreSQL: {e}")
            print("\n� CONFIGURAÇÃO ATUAL:")
            print(f"   Host: {self.db_config['host']}")
            print(f"   Port: {self.db_config['port']}")
            print(f"   Database: {self.db_config['database']}")
            print(f"   User: {self.db_config['user']}")
            print("\n💡 VERIFICAÇÕES:")
            print("   • PostgreSQL está rodando?")
            print("   • Database 'curso' existe?")
            print("   • Extensões pgvector/postgis instaladas?")
            raise e
    
    def _configurar_extensoes(self):
        """Configura extensões necessárias (pgvector, PostGIS)"""
        cursor = self.conn.cursor()
        
        try:
            # Instalar pgvector
            cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
            print("✅ Extensão pgvector configurada")
            
            # Instalar PostGIS (opcional para geolocalização avançada)
            cursor.execute("CREATE EXTENSION IF NOT EXISTS postgis")
            print("✅ Extensão PostGIS configurada")
            
        except Exception as e:
            print(f"⚠️ Aviso: Algumas extensões podem não estar disponíveis: {e}")
            # pgvector é essencial, PostGIS é opcional
            try:
                cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
                print("✅ pgvector instalado (PostGIS opcional)")
            except Exception as e2:
                print(f"❌ Erro crítico: pgvector não disponível: {e2}")
                raise e2
    
    def _criar_schema(self):
        """Cria schema completo do sistema médico"""
        cursor = self.conn.cursor()
        
        # Tabela de estabelecimentos com suporte geográfico
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS estabelecimentos (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL,
            latitude DECIMAL(10, 7) NOT NULL,
            longitude DECIMAL(10, 7) NOT NULL,
            municipio TEXT NOT NULL,
            telefone TEXT,
            endereco TEXT,
            horario_funcionamento TEXT DEFAULT '24h',
            especialidades TEXT[], -- Array de especialidades
            capacidade INTEGER DEFAULT 50,
            avaliacao DECIMAL(2,1) DEFAULT 4.0,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            -- Índice espacial para busca geográfica
            localizacao GEOGRAPHY(POINT, 4326) GENERATED ALWAYS AS (
                ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
            ) STORED
        )
        """)
        
        # Tabela de queixas principais com embeddings
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS queixas_principais (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL UNIQUE,
            descricao TEXT,
            nivel_urgencia INTEGER DEFAULT 2,
            keywords TEXT[], -- Palavras-chave para busca
            protocolo_atendimento TEXT,
            tempo_limite_atendimento INTERVAL,
            -- Embedding para busca semântica
            embedding VECTOR(1536), -- OpenAI ada-002 dimensões
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Tabela de sintomas com embeddings
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS sintomas (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            descricao TEXT,
            criticidade INTEGER DEFAULT 2,
            categoria TEXT, -- cardiovascular, respiratorio, neurologico, etc
            sinonimos TEXT[], -- Variações do nome
            -- Embedding para busca semântica
            embedding VECTOR(1536),
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Tabela de relacionamento queixa-sintoma (many-to-many)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS queixa_sintoma (
            queixa_id INTEGER REFERENCES queixas_principais(id),
            sintoma_id INTEGER REFERENCES sintomas(id),
            relevancia DECIMAL(3,2) DEFAULT 1.0, -- Peso da relação
            PRIMARY KEY (queixa_id, sintoma_id)
        )
        """)
        
        # Tabela de consultas médicas (log/histórico)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultas_medicas (
            id SERIAL PRIMARY KEY,
            texto_sintomas TEXT NOT NULL,
            embedding_sintomas VECTOR(1536),
            sintomas_identificados INTEGER[],
            queixa_principal_id INTEGER REFERENCES queixas_principais(id),
            nivel_urgencia INTEGER,
            estabelecimento_recomendado_id INTEGER REFERENCES estabelecimentos(id),
            latitude_paciente DECIMAL(10, 7),
            longitude_paciente DECIMAL(10, 7),
            feedback_usuario TEXT,
            avaliacao INTEGER, -- 1-5 estrelas
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Tabela de cache de embeddings
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cache_embeddings (
            id SERIAL PRIMARY KEY,
            texto_hash TEXT UNIQUE NOT NULL,
            texto_original TEXT NOT NULL,
            embedding VECTOR(1536) NOT NULL,
            modelo TEXT DEFAULT 'text-embedding-3-small',
            tokens_utilizados INTEGER,
            custo_estimado DECIMAL(10,6),
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            acessado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            count_acessos INTEGER DEFAULT 1
        )
        """)
        
        # Criar índices para performance
        self._criar_indices()
        
        # Schema criado silenciosamente
    
    def _criar_indices(self):
        """Cria índices otimizados para busca"""
        cursor = self.conn.cursor()
        
        try:
            # Índices para embeddings (HNSW para busca por similaridade)
            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_queixas_embedding 
            ON queixas_principais USING hnsw (embedding vector_cosine_ops)
            """)
            
            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_sintomas_embedding 
            ON sintomas USING hnsw (embedding vector_cosine_ops)
            """)
            
            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_cache_embedding 
            ON cache_embeddings USING hnsw (embedding vector_cosine_ops)
            """)
            
            # Índices geográficos
            cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_estabelecimentos_geo 
            ON estabelecimentos USING GIST (localizacao)
            """)
            
            # Índices tradicionais
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_estabelecimentos_tipo ON estabelecimentos(tipo)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_sintomas_criticidade ON sintomas(criticidade)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_cache_hash ON cache_embeddings(texto_hash)")
            
            # Índices criados silenciosamente
            
        except Exception as e:
            print(f"⚠️ Alguns índices podem não ter sido criados: {e}")
    
    def gerar_embedding(self, texto: str, usar_cache: bool = True) -> List[float]:
        """
        Gera embedding usando OpenAI API com cache inteligente
        
        Args:
            texto: Texto para gerar embedding
            usar_cache: Se deve usar cache (default: True)
            
        Returns:
            Lista com embedding (1536 dimensões)
        """
        
        # Normalizar texto
        texto = texto.strip().lower()
        if not texto:
            raise ValueError("Texto vazio não pode gerar embedding")
        
        # Hash do texto para cache
        texto_hash = hashlib.md5(texto.encode()).hexdigest()
        
        # Verificar cache em memória primeiro
        if usar_cache and texto_hash in self.cache_embeddings:
            cache_entry = self.cache_embeddings[texto_hash]
            if time.time() - cache_entry['timestamp'] < self.cache_ttl:
                print(f"📄 Cache em memória: {texto[:50]}...")
                return cache_entry['embedding']
        
        # Verificar cache no banco
        if usar_cache:
            cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            cursor.execute("""
            SELECT embedding, acessado_em FROM cache_embeddings 
            WHERE texto_hash = %s
            """, (texto_hash,))
            
            resultado = cursor.fetchone()
            if resultado:
                # Atualizar estatísticas de acesso
                cursor.execute("""
                UPDATE cache_embeddings 
                SET acessado_em = CURRENT_TIMESTAMP,
                    count_acessos = count_acessos + 1
                WHERE texto_hash = %s
                """, (texto_hash,))
                
                embedding = resultado['embedding']
                
                # Atualizar cache em memória
                self.cache_embeddings[texto_hash] = {
                    'embedding': embedding,
                    'timestamp': time.time()
                }
                
                print(f"💾 Cache PostgreSQL: {texto[:50]}...")
                return embedding
        
        # Gerar novo embedding via OpenAI
        try:
            print(f"🤖 Gerando embedding: {texto[:50]}...")
            
            response = self.openai_client.embeddings.create(
                model="text-embedding-3-small",  # Modelo mais econômico
                input=texto
            )
            
            embedding = response.data[0].embedding
            tokens_utilizados = response.usage.total_tokens
            
            # Estimar custo (text-embedding-3-small: $0.02 / 1M tokens)
            custo_estimado = (tokens_utilizados / 1000000) * 0.02
            
            print(f"💰 Tokens: {tokens_utilizados}, Custo: ${custo_estimado:.6f}")
            
            # Salvar no cache do banco
            if usar_cache:
                cursor = self.conn.cursor()
                cursor.execute("""
                INSERT INTO cache_embeddings 
                (texto_hash, texto_original, embedding, tokens_utilizados, custo_estimado)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (texto_hash) DO UPDATE SET
                    acessado_em = CURRENT_TIMESTAMP,
                    count_acessos = cache_embeddings.count_acessos + 1
                """, (texto_hash, texto, embedding, tokens_utilizados, custo_estimado))
            
            # Atualizar cache em memória
            self.cache_embeddings[texto_hash] = {
                'embedding': embedding,
                'timestamp': time.time()
            }
            
            return embedding
            
        except Exception as e:
            print(f"❌ Erro ao gerar embedding: {e}")
            raise e
    
    def buscar_sintomas_similaridade(self, texto_sintomas: str, limite: int = 5, 
                                   threshold: float = 0.7) -> List[Dict]:
        """
        Busca sintomas por similaridade usando embeddings
        
        Args:
            texto_sintomas: Descrição dos sintomas
            limite: Número máximo de resultados
            threshold: Limite de similaridade (0-1)
            
        Returns:
            Lista de sintomas similares com scores
        """
        
        # Gerar embedding do texto
        embedding_busca = self.gerar_embedding(texto_sintomas)
        
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        # Buscar por similaridade de cosseno
        cursor.execute("""
        SELECT 
            id, nome, descricao, criticidade, categoria,
            1 - (embedding <=> %s::vector) AS similaridade
        FROM sintomas
        WHERE embedding IS NOT NULL
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        """, (embedding_busca, embedding_busca, limite))
        
        resultados = cursor.fetchall()
        
        # Filtrar por threshold
        sintomas_relevantes = [
            dict(resultado) for resultado in resultados 
            if resultado['similaridade'] >= threshold
        ]
        
        print(f"🔍 Encontrados {len(sintomas_relevantes)} sintomas similares")
        
        return sintomas_relevantes
    
    def buscar_queixas_similaridade(self, texto_sintomas: str, limite: int = 3) -> List[Dict]:
        """Busca queixas principais por similaridade"""
        
        embedding_busca = self.gerar_embedding(texto_sintomas)
        
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
        SELECT 
            id, nome, descricao, nivel_urgencia, protocolo_atendimento,
            1 - (embedding <=> %s::vector) AS similaridade
        FROM queixas_principais
        WHERE embedding IS NOT NULL
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        """, (embedding_busca, embedding_busca, limite))
        
        return [dict(resultado) for resultado in cursor.fetchall()]
    
    def buscar_estabelecimentos_geografico(self, latitude: float, longitude: float, 
                                         raio_km: float = 10, tipo: str = None,
                                         limite: int = 10) -> List[Dict]:
        """
        Busca estabelecimentos por proximidade geográfica usando PostGIS
        
        Args:
            latitude, longitude: Coordenadas do paciente
            raio_km: Raio de busca em quilômetros
            tipo: Tipo de estabelecimento (opcional)
            limite: Número máximo de resultados
            
        Returns:
            Lista de estabelecimentos ordenados por distância
        """
        
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        # Query com ou sem filtro de tipo
        if tipo:
            query = """
            SELECT 
                id, nome, tipo, latitude, longitude, municipio, 
                telefone, endereco, horario_funcionamento, especialidades,
                ST_Distance(
                    localizacao,
                    ST_SetSRID(ST_MakePoint(%s, %s), 4326)
                ) / 1000 AS distancia_km
            FROM estabelecimentos
            WHERE tipo = %s
              AND ST_DWithin(
                localizacao,
                ST_SetSRID(ST_MakePoint(%s, %s), 4326),
                %s * 1000
              )
            ORDER BY distancia_km
            LIMIT %s
            """
            parametros = (longitude, latitude, tipo, longitude, latitude, raio_km, limite)
        else:
            query = """
            SELECT 
                id, nome, tipo, latitude, longitude, municipio,
                telefone, endereco, horario_funcionamento, especialidades,
                ST_Distance(
                    localizacao,
                    ST_SetSRID(ST_MakePoint(%s, %s), 4326)
                ) / 1000 AS distancia_km
            FROM estabelecimentos
            WHERE ST_DWithin(
                localizacao,
                ST_SetSRID(ST_MakePoint(%s, %s), 4326),
                %s * 1000
              )
            ORDER BY distancia_km
            LIMIT %s
            """
            parametros = (longitude, latitude, longitude, latitude, raio_km, limite)
        
        cursor.execute(query, parametros)
        
        return [dict(resultado) for resultado in cursor.fetchall()]
    
    def registrar_consulta(self, texto_sintomas: str, sintomas_identificados: List[int],
                          queixa_principal_id: Optional[int], nivel_urgencia: int,
                          estabelecimento_id: Optional[int], latitude: float, longitude: float) -> int:
        """Registra consulta médica para análise e melhoria do sistema"""
        
        embedding_sintomas = self.gerar_embedding(texto_sintomas)
        
        cursor = self.conn.cursor()
        cursor.execute("""
        INSERT INTO consultas_medicas 
        (texto_sintomas, embedding_sintomas, sintomas_identificados, 
         queixa_principal_id, nivel_urgencia, estabelecimento_recomendado_id,
         latitude_paciente, longitude_paciente)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id
        """, (texto_sintomas, embedding_sintomas, sintomas_identificados,
              queixa_principal_id, nivel_urgencia, estabelecimento_id,
              latitude, longitude))
        
        consulta_id = cursor.fetchone()[0]
        print(f"📝 Consulta registrada: ID {consulta_id}")
        
        return consulta_id
    
    def get_estatisticas_sistema(self) -> Dict:
        """Retorna estatísticas completas do sistema"""
        
        cursor = self.conn.cursor(cursor_factory=RealDictCursor)
        
        # Estatísticas básicas
        cursor.execute("SELECT COUNT(*) as total FROM estabelecimentos")
        total_estabelecimentos = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM sintomas")
        total_sintomas = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM queixas_principais")
        total_queixas = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM consultas_medicas")
        total_consultas = cursor.fetchone()['total']
        
        # Estatísticas de cache
        cursor.execute("""
        SELECT 
            COUNT(*) as entradas_cache,
            SUM(tokens_utilizados) as total_tokens,
            SUM(custo_estimado) as custo_total,
            SUM(count_acessos) as total_acessos
        FROM cache_embeddings
        """)
        stats_cache = cursor.fetchone()
        
        # Estabelecimentos por tipo
        cursor.execute("SELECT tipo, COUNT(*) as quantidade FROM estabelecimentos GROUP BY tipo")
        tipos_estabelecimentos = {row['tipo']: row['quantidade'] for row in cursor.fetchall()}
        
        return {
            'total_estabelecimentos': total_estabelecimentos,
            'total_sintomas': total_sintomas,
            'total_queixas': total_queixas,
            'total_consultas': total_consultas,
            'tipos_estabelecimentos': tipos_estabelecimentos,
            'cache_embeddings': {
                'entradas': stats_cache['entradas_cache'] or 0,
                'tokens_total': stats_cache['total_tokens'] or 0,
                'custo_total_usd': float(stats_cache['custo_total'] or 0),
                'acessos_total': stats_cache['total_acessos'] or 0
            }
        }
    
    def limpar_cache_antigo(self, dias: int = 7):
        """Remove entradas de cache mais antigas que X dias"""
        
        cursor = self.conn.cursor()
        cursor.execute("""
        DELETE FROM cache_embeddings 
        WHERE acessado_em < CURRENT_TIMESTAMP - INTERVAL '%s days'
        """, (dias,))
        
        removidas = cursor.rowcount
        print(f"🗑️ Removidas {removidas} entradas de cache antigas")
        
        return removidas
    
    def __del__(self):
        """Fecha conexão ao destruir objeto"""
        if self.conn:
            self.conn.close()


def configurar_banco_exemplo():
    """Configura banco com dados de exemplo para desenvolvimento"""
    
    print("🚀 CONFIGURANDO BANCO POSTGRESQL + EMBEDDINGS")
    print("="*50)
    
    try:
        db = PostgreSQLMedico()
        
        print("\n📊 Inserindo dados de exemplo...")
        
        # Dados de exemplo aqui serão inseridos no próximo todo
        # Por enquanto, só testamos a conexão
        
        stats = db.get_estatisticas_sistema()
        print("✅ Sistema de banco preparado")
        print(f"📈 Estatísticas: {stats}")
        
        return db
        
    except Exception as e:
        print(f"❌ Erro na configuração: {e}")
        return None


if __name__ == "__main__":
    configurar_banco_exemplo()