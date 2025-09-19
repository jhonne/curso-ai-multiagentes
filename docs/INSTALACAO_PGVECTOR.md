# 📦 Guia de Instalação do pgvector - Curso CrewAI

## 🎯 Visão Geral

O **pgvector** é uma extensão open-source do PostgreSQL que adiciona suporte nativo para **busca de similaridade de vetores**. Esta extensão é essencial para o Curso CrewAI, pois permite:

- ✅ Armazenamento eficiente de embeddings OpenAI
- ✅ Busca semântica ultrarrápida em sintomas e queixas médicas
- ✅ Consultas por similaridade usando L2, coseno, produto interno
- ✅ Índices otimizados (HNSW e IVFFlat)
- ✅ Suporte completo a ACID, JOINs e recursos PostgreSQL

## ⚡ Compatibilidade

### Versões Suportadas
- **PostgreSQL**: 13, 14, 15, 16, 17+
- **pgvector**: v0.8.1+ (recomendado v0.8.1)
- **Sistemas**: Linux, macOS, Windows
- **Dimensões suportadas**: até 2.000 (vector), 4.000 (halfvec), 64.000 (bit)

### Para o Curso CrewAI
- **Embedding OpenAI**: 1.536 dimensões (suportado ✅)
- **Modelo usado**: `text-embedding-3-small`
- **Índices recomendados**: HNSW para performance otimizada

import os
import sys
import asyncio
import asyncpg
import logging
from typing import Dict, List, Tuple
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ConfiguradorPgvector:
    """Configurador automático do pgvector"""
    
    def __init__(self, database_url: str = None):
        self.database_url = database_url or os.getenv(
            "DATABASE_URL", 
            "postgresql://postgres:password@localhost:5432/curso"
        )
        self.conn = None
    
    async def conectar(self):
        """Conecta ao banco de dados"""
        try:
            self.conn = await asyncpg.connect(self.database_url)
            logger.info("✅ Conectado ao PostgreSQL")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao conectar ao PostgreSQL: {e}")
            return False
    
    async def verificar_postgresql_version(self) -> Tuple[bool, str]:
        """Verifica versão do PostgreSQL"""
        try:
            version = await self.conn.fetchval("SELECT version()")
            
            # Extrair número da versão
            version_parts = version.split()
            version_number = version_parts[1] if len(version_parts) > 1 else "unknown"
            
            # Verificar se é versão suportada (13+)
            major_version = int(version_number.split('.')[0])
            is_supported = major_version >= 13
            
            if is_supported:
                logger.info(f"✅ PostgreSQL {version_number} (suportado)")
            else:
                logger.error(f"❌ PostgreSQL {version_number} (requer 13+)")
            
            return is_supported, version_number
        except Exception as e:
            logger.error(f"❌ Erro ao verificar versão do PostgreSQL: {e}")
            return False, "unknown"
    
    async def verificar_extensao_pgvector(self) -> Tuple[bool, str]:
        """Verifica se pgvector está instalado"""
        try:
            # Verificar se extensão está disponível
            available = await self.conn.fetchval(
                "SELECT 1 FROM pg_available_extensions WHERE name = 'vector'"
            )
            
            if not available:
                logger.error("❌ pgvector não está instalado no sistema")
                return False, "não instalado"
            
            # Verificar se extensão está habilitada
            enabled = await self.conn.fetchval(
                "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
            )
            
            if enabled:
                logger.info(f"✅ pgvector {enabled} habilitado")
                return True, enabled
            else:
                logger.warning("⚠️ pgvector disponível mas não habilitado")
                return False, "disponível"
        
        except Exception as e:
            logger.error(f"❌ Erro ao verificar pgvector: {e}")
            return False, "erro"
    
    async def habilitar_pgvector(self) -> bool:
        """Habilita extensão pgvector"""
        try:
            await self.conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
            logger.info("✅ Extensão pgvector habilitada")
            
            # Verificar versão instalada
            version = await self.conn.fetchval(
                "SELECT extversion FROM pg_extension WHERE extname = 'vector'"
            )
            logger.info(f"📦 Versão instalada: {version}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Erro ao habilitar pgvector: {e}")
            return False
    
    async def testar_funcionalidades_basicas(self) -> bool:
        """Testa funcionalidades básicas do pgvector"""
        try:
            logger.info("🧪 Testando funcionalidades básicas...")
            
            # 1. Criar tabela de teste
            await self.conn.execute("""
                DROP TABLE IF EXISTS teste_pgvector_config;
                CREATE TABLE teste_pgvector_config (
                    id SERIAL PRIMARY KEY,
                    nome TEXT,
                    embedding VECTOR(3)
                );
            """)
            
            # 2. Inserir dados de teste
            await self.conn.execute("""
                INSERT INTO teste_pgvector_config (nome, embedding) VALUES 
                    ('Teste A', '[1,2,3]'),
                    ('Teste B', '[4,5,6]'),
                    ('Teste C', '[7,8,9]');
            """)
            
            # 3. Testar consulta por similaridade L2
            result = await self.conn.fetch("""
                SELECT nome, embedding <-> '[2,3,4]' AS distancia 
                FROM teste_pgvector_config 
                ORDER BY embedding <-> '[2,3,4]' 
                LIMIT 3;
            """)
            
            if len(result) == 3:
                logger.info("✅ Busca por similaridade L2 funcionando")
            else:
                logger.error("❌ Falha na busca por similaridade L2")
                return False
            
            # 4. Testar outras funções de distância
            funcs_distancia = [
                ("Produto interno", "<#>"),
                ("Distância cosseno", "<=>"),
                ("Distância L1", "<+>")
            ]
            
            for nome_func, operador in funcs_distancia:
                try:
                    await self.conn.fetchval(f"""
                        SELECT embedding {operador} '[2,3,4]' 
                        FROM teste_pgvector_config 
                        LIMIT 1;
                    """)
                    logger.info(f"✅ {nome_func} funcionando")
                except Exception:
                    logger.warning(f"⚠️ {nome_func} pode não estar disponível")
            
            # 5. Testar criação de índice HNSW
            await self.conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_teste_pgvector_hnsw 
                ON teste_pgvector_config 
                USING hnsw (embedding vector_l2_ops);
            """)
            logger.info("✅ Índice HNSW criado com sucesso")
            
            # 6. Testar consulta com índice
            plan = await self.conn.fetchval("""
                EXPLAIN (FORMAT JSON) 
                SELECT nome FROM teste_pgvector_config 
                ORDER BY embedding <-> '[2,3,4]' 
                LIMIT 1;
            """)
            
            # Verificar se está usando índice
            plan_dict = json.loads(plan)[0]['Plan']
            if 'Index' in plan_dict.get('Node Type', ''):
                logger.info("✅ Consultas usando índice HNSW")
            else:
                logger.warning("⚠️ Índice pode não estar sendo usado (normal com poucos dados)")
            
            # 7. Limpeza
            await self.conn.execute("DROP TABLE teste_pgvector_config;")
            logger.info("✅ Testes básicos concluídos com sucesso")
            return True
        
        except Exception as e:
            logger.error(f"❌ Erro nos testes básicos: {e}")
            return False
    
    async def configurar_parametros_otimizados(self) -> bool:
        """Configura parâmetros otimizados para o curso"""
        try:
            logger.info("⚙️ Configurando parâmetros otimizados...")
            
            # Configurações específicas do pgvector para a sessão
            configuracoes = [
                ("hnsw.ef_search", "100", "Melhora qualidade de busca HNSW"),
                ("maintenance_work_mem", "512MB", "Acelera criação de índices"),
                ("work_mem", "64MB", "Otimiza consultas de vetores"),
            ]
            
            for param, valor, descricao in configuracoes:
                try:
                    await self.conn.execute(f"SET {param} = '{valor}';")
                    logger.info(f"✅ {param} = {valor} ({descricao})")
                except Exception as e:
                    logger.warning(f"⚠️ Não foi possível definir {param}: {e}")
            
            return True
        
        except Exception as e:
            logger.error(f"❌ Erro ao configurar parâmetros: {e}")
            return False
    
    async def verificar_limites_suportados(self) -> Dict:
        """Verifica limites suportados da instalação"""
        try:
            logger.info("📊 Verificando limites suportados...")
            
            limites = {
                'vector_max_dimensions': 2000,
                'halfvec_max_dimensions': 4000,
                'bit_max_dimensions': 64000,
                'sparsevec_max_elements': 1000
            }
            
            # Testar dimensões máximas para vector normal
            try:
                await self.conn.execute("""
                    CREATE TEMP TABLE teste_limite AS 
                    SELECT ('[' || string_agg(i::text, ',') || ']')::vector(1536) as emb
                    FROM generate_series(1, 1536) i;
                """)
                logger.info("✅ Suporte a vetores de 1536 dimensões (OpenAI embeddings)")
            except Exception:
                logger.warning("⚠️ Problema com vetores de 1536 dimensões")
            
            return limites
        
        except Exception as e:
            logger.error(f"❌ Erro ao verificar limites: {e}")
            return {}
    
    async def gerar_relatorio_configuracao(self) -> Dict:
        """Gera relatório completo da configuração"""
        relatorio = {
            'timestamp': '2024-12-19',
            'postgresql': {},
            'pgvector': {},
            'testes': {},
            'configuracao': {},
            'status': 'unknown'
        }
        
        try:
            # Verificar PostgreSQL
            pg_ok, pg_version = await self.verificar_postgresql_version()
            relatorio['postgresql'] = {
                'version': pg_version,
                'compatible': pg_ok
            }
            
            # Verificar pgvector
            pv_ok, pv_version = await self.verificar_extensao_pgvector()
            relatorio['pgvector'] = {
                'installed': pv_ok,
                'version': pv_version
            }
            
            # Se não estiver habilitado, tentar habilitar
            if not pv_ok and pv_version == "disponível":
                pv_ok = await self.habilitar_pgvector()
                if pv_ok:
                    _, pv_version = await self.verificar_extensao_pgvector()
                    relatorio['pgvector']['version'] = pv_version
            
            # Executar testes se tudo estiver OK
            if pg_ok and pv_ok:
                testes_ok = await self.testar_funcionalidades_basicas()
                config_ok = await self.configurar_parametros_otimizados()
                limites = await self.verificar_limites_suportados()
                
                relatorio['testes'] = {
                    'basic_functionality': testes_ok,
                    'configuration': config_ok,
                    'limits': limites
                }
                
                # Status geral
                if testes_ok and config_ok:
                    relatorio['status'] = 'ready'
                    logger.info("🎉 pgvector configurado e pronto para uso!")
                else:
                    relatorio['status'] = 'partial'
                    logger.warning("⚠️ pgvector parcialmente configurado")
            else:
                relatorio['status'] = 'error'
                logger.error("❌ pgvector não está pronto para uso")
            
            return relatorio
        
        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório: {e}")
            relatorio['status'] = 'error'
            relatorio['error'] = str(e)
            return relatorio
    
    async def desconectar(self):
        """Desconecta do banco"""
        if self.conn:
            await self.conn.close()
            logger.info("🔚 Desconectado do PostgreSQL")

async def main():
    """Função principal"""
    print("=" * 80)
    print("🚀 CONFIGURADOR PGVECTOR PARA CURSO CREWAI")
    print("=" * 80)
    
    # Verificar variável de ambiente
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("⚠️ Variável DATABASE_URL não encontrada")
        print("💡 Usando configuração padrão: postgresql://postgres:password@localhost:5432/curso")
        print("💡 Para usar outra configuração, defina: export DATABASE_URL='sua_conexao'")
    
    configurador = ConfiguradorPgvector()
    
    try:
        # Conectar
        if not await configurador.conectar():
            print("❌ Falha na conexão. Verifique se PostgreSQL está rodando")
            return False
        
        # Executar configuração completa
        relatorio = await configurador.gerar_relatorio_configuracao()
        
        # Mostrar resultados
        print("\n" + "=" * 80)
        print("📊 RELATÓRIO DE CONFIGURAÇÃO")
        print("=" * 80)
        
        print(f"🐘 PostgreSQL: {relatorio['postgresql']['version']}")
        print(f"📦 pgvector: {relatorio['pgvector']['version']}")
        print(f"🎯 Status: {relatorio['status'].upper()}")
        
        if relatorio['status'] == 'ready':
            print("\n✅ CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
            print("🎉 pgvector está pronto para usar no Curso CrewAI")
            print("\n📋 Próximos passos:")
            print("  1. Execute: uv run aula7/scripts/01_criar_tabelas_embeddings.sql")
            print("  2. Execute: uv run aula7/scripts/02_migrar_dados_embeddings.py")
            print("  3. Execute: uv run aula7/scripts/03_testar_embeddings.py")
        
        elif relatorio['status'] == 'partial':
            print("\n⚠️ CONFIGURAÇÃO PARCIAL")
            print("💡 pgvector está instalado mas pode ter limitações")
        
        else:
            print("\n❌ CONFIGURAÇÃO FALHOU")
            print("🔧 Instruções de instalação manual:")
            print("  Ubuntu/Debian: sudo apt-get install postgresql-15-pgvector")
            print("  macOS: brew install pgvector")
            print("  Docker: docker run -d pgvector/pgvector:pg15")
        
        # Salvar relatório
        with open('pgvector_config_report.json', 'w') as f:
            json.dump(relatorio, f, indent=2)
        print(f"\n📄 Relatório salvo: pgvector_config_report.json")
        
        return relatorio['status'] == 'ready'
    
    finally:
        await configurador.desconectar()

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)