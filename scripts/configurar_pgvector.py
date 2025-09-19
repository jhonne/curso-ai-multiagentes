#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCRIPT DE CONFIGURAÇÃO E VERIFICAÇÃO AUTOMÁTICA DO PGVECTOR
===========================================================

Script para verificar e configurar automaticamente o pgvector
no PostgreSQL para o Curso CrewAI.

Execução:
    uv run scripts/configurar_pgvector.py

Autor: Curso CrewAI - Sistema de Triagem Médica
"""

import os
import sys
import asyncio
import asyncpg
import logging
from typing import Dict, Tuple
import json
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class ConfiguradorPgvector:
    """Configurador automático do pgvector"""

    def __init__(self, database_url: str = None):
        self.database_url = database_url or os.getenv(
            "DATABASE_URL", "postgresql://postgres:password@localhost:5432/curso"
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
            try:
                major_version = int(version_number.split(".")[0])
                is_supported = major_version >= 13
            except ValueError:
                is_supported = False

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
            await self.conn.execute(
                """
                DROP TABLE IF EXISTS teste_pgvector_config;
                CREATE TABLE teste_pgvector_config (
                    id SERIAL PRIMARY KEY,
                    nome TEXT,
                    embedding VECTOR(3)
                );
            """
            )

            # 2. Inserir dados de teste
            await self.conn.execute(
                """
                INSERT INTO teste_pgvector_config (nome, embedding) VALUES 
                    ('Teste A', '[1,2,3]'),
                    ('Teste B', '[4,5,6]'),
                    ('Teste C', '[7,8,9]');
            """
            )

            # 3. Testar consulta por similaridade L2
            result = await self.conn.fetch(
                """
                SELECT nome, embedding <-> '[2,3,4]' AS distancia 
                FROM teste_pgvector_config 
                ORDER BY embedding <-> '[2,3,4]' 
                LIMIT 3;
            """
            )

            if len(result) == 3:
                logger.info("✅ Busca por similaridade L2 funcionando")
                logger.info(
                    f"📊 Resultado mais próximo: {result[0]['nome']} (distância: {result[0]['distancia']:.4f})"
                )
            else:
                logger.error("❌ Falha na busca por similaridade L2")
                return False

            # 4. Testar outras funções de distância
            funcs_distancia = [
                ("Produto interno", "<#>"),
                ("Distância cosseno", "<=>"),
                ("Distância L1", "<+>"),
            ]

            for nome_func, operador in funcs_distancia:
                try:
                    await self.conn.fetchval(
                        f"""
                        SELECT embedding {operador} '[2,3,4]' 
                        FROM teste_pgvector_config 
                        LIMIT 1;
                    """
                    )
                    logger.info(f"✅ {nome_func} funcionando")
                except Exception:
                    logger.warning(f"⚠️ {nome_func} pode não estar disponível")

            # 5. Testar criação de índice HNSW
            await self.conn.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_teste_pgvector_hnsw 
                ON teste_pgvector_config 
                USING hnsw (embedding vector_l2_ops);
            """
            )
            logger.info("✅ Índice HNSW criado com sucesso")

            # 6. Testar dimensões do OpenAI (1536)
            try:
                await self.conn.execute(
                    """
                    CREATE TEMP TABLE teste_openai_dims (
                        embedding VECTOR(1536)
                    );
                    INSERT INTO teste_openai_dims (embedding)
                    SELECT ('[' || string_agg(random()::text, ',') || ']')::vector(1536)
                    FROM generate_series(1, 1536);
                """
                )
                logger.info(
                    "✅ Suporte a 1536 dimensões (OpenAI embeddings) confirmado"
                )
            except Exception as e:
                logger.warning(f"⚠️ Problema com 1536 dimensões: {e}")

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
                (
                    "max_parallel_maintenance_workers",
                    "4",
                    "Paralelismo na criação de índices",
                ),
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
                "vector_max_dimensions": 2000,
                "halfvec_max_dimensions": 4000,
                "bit_max_dimensions": 64000,
                "sparsevec_max_elements": 1000,
                "openai_embedding_support": False,
                "indices_suportados": [],
            }

            # Testar dimensões do OpenAI (1536)
            try:
                await self.conn.execute(
                    """
                    CREATE TEMP TABLE teste_limite_1536 AS 
                    SELECT ('[' || string_agg(i::text, ',') || ']')::vector(1536) as emb
                    FROM generate_series(1, 1536) i;
                """
                )
                limites["openai_embedding_support"] = True
                logger.info(
                    "✅ Suporte a vetores de 1536 dimensões (OpenAI embeddings)"
                )
            except Exception:
                logger.warning("⚠️ Problema com vetores de 1536 dimensões")

            # Testar tipos de índices
            tipos_indices = ["hnsw", "ivfflat"]
            for tipo_indice in tipos_indices:
                try:
                    await self.conn.execute(
                        f"""
                        CREATE TEMP TABLE teste_idx_{tipo_indice} (emb VECTOR(3));
                        INSERT INTO teste_idx_{tipo_indice} VALUES ('[1,2,3]');
                        CREATE INDEX ON teste_idx_{tipo_indice} USING {tipo_indice} (emb vector_l2_ops);
                    """
                    )
                    limites["indices_suportados"].append(tipo_indice)
                    logger.info(f"✅ Índice {tipo_indice.upper()} suportado")
                except Exception:
                    logger.warning(f"⚠️ Índice {tipo_indice.upper()} não disponível")

            return limites

        except Exception as e:
            logger.error(f"❌ Erro ao verificar limites: {e}")
            return {}

    async def gerar_relatorio_configuracao(self) -> Dict:
        """Gera relatório completo da configuração"""
        relatorio = {
            "timestamp": datetime.now().isoformat(),
            "postgresql": {},
            "pgvector": {},
            "testes": {},
            "configuracao": {},
            "status": "unknown",
        }

        try:
            # Verificar PostgreSQL
            pg_ok, pg_version = await self.verificar_postgresql_version()
            relatorio["postgresql"] = {"version": pg_version, "compatible": pg_ok}

            # Verificar pgvector
            pv_ok, pv_version = await self.verificar_extensao_pgvector()
            relatorio["pgvector"] = {"installed": pv_ok, "version": pv_version}

            # Se não estiver habilitado, tentar habilitar
            if not pv_ok and pv_version == "disponível":
                pv_ok = await self.habilitar_pgvector()
                if pv_ok:
                    _, pv_version = await self.verificar_extensao_pgvector()
                    relatorio["pgvector"]["version"] = pv_version
                    relatorio["pgvector"]["installed"] = True

            # Executar testes se tudo estiver OK
            if pg_ok and pv_ok:
                testes_ok = await self.testar_funcionalidades_basicas()
                config_ok = await self.configurar_parametros_otimizados()
                limites = await self.verificar_limites_suportados()

                relatorio["testes"] = {
                    "basic_functionality": testes_ok,
                    "configuration": config_ok,
                    "limits": limites,
                }

                # Status geral
                if (
                    testes_ok
                    and config_ok
                    and limites.get("openai_embedding_support", False)
                ):
                    relatorio["status"] = "ready"
                    logger.info("🎉 pgvector configurado e pronto para uso!")
                elif testes_ok:
                    relatorio["status"] = "partial"
                    logger.warning("⚠️ pgvector funcionando mas com limitações")
                else:
                    relatorio["status"] = "error"
                    logger.error("❌ pgvector com problemas")
            else:
                relatorio["status"] = "error"
                logger.error("❌ pgvector não está pronto para uso")

            return relatorio

        except Exception as e:
            logger.error(f"❌ Erro ao gerar relatório: {e}")
            relatorio["status"] = "error"
            relatorio["error"] = str(e)
            return relatorio

    async def desconectar(self):
        """Desconecta do banco"""
        if self.conn:
            await self.conn.close()
            logger.info("🔚 Desconectado do PostgreSQL")


def imprimir_banner():
    """Imprime banner do configurador"""
    print("=" * 80)
    print("🚀 CONFIGURADOR AUTOMÁTICO PGVECTOR - CURSO CREWAI")
    print("=" * 80)
    print("📋 Este script verifica e configura automaticamente o pgvector")
    print("🎯 Objetivo: Preparar PostgreSQL para embeddings OpenAI")
    print("🏥 Contexto: Sistema de triagem médica inteligente")
    print("=" * 80)


def imprimir_instrucoes_instalacao():
    """Imprime instruções de instalação manual"""
    print("\n" + "=" * 80)
    print("🔧 INSTRUÇÕES DE INSTALAÇÃO MANUAL DO PGVECTOR")
    print("=" * 80)

    print("\n🐧 Ubuntu/Debian:")
    print("  sudo apt update")
    print("  sudo apt install postgresql-15-pgvector")

    print("\n🍎 macOS:")
    print("  brew install pgvector")

    print("\n🪟 Windows:")
    print("  # Usar Docker ou compilar manualmente")
    print("  # Ver: https://github.com/pgvector/pgvector")

    print("\n🐳 Docker (Recomendado):")
    print("  docker run -d --name postgres-pgvector \\")
    print("    -e POSTGRES_DB=curso \\")
    print("    -e POSTGRES_USER=postgres \\")
    print("    -e POSTGRES_PASSWORD=password \\")
    print("    -p 5432:5432 \\")
    print("    pgvector/pgvector:pg17")

    print("\n☁️ Serviços Hospedados (com pgvector pré-instalado):")
    print("  • Supabase: https://supabase.com/")
    print("  • Neon: https://neon.tech/")
    print("  • Railway: https://railway.app/")

    print("=" * 80)


async def main():
    """Função principal"""
    imprimir_banner()

    # Verificar variável de ambiente
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("\n⚠️ Variável DATABASE_URL não encontrada")
        print(
            "💡 Usando configuração padrão: postgresql://postgres:password@localhost:5432/curso"
        )
        print(
            "💡 Para usar outra configuração, defina: export DATABASE_URL='sua_conexao'"
        )
    else:
        print(f"\n✅ Usando DATABASE_URL: {database_url[:50]}...")

    configurador = ConfiguradorPgvector(database_url)

    try:
        # Conectar
        if not await configurador.conectar():
            print("\n❌ Falha na conexão com PostgreSQL")
            print("🔍 Verifique se o PostgreSQL está rodando:")
            print("  • Linux: sudo systemctl status postgresql")
            print("  • macOS: brew services list | grep postgresql")
            print("  • Docker: docker ps | grep postgres")
            imprimir_instrucoes_instalacao()
            return False

        # Executar configuração completa
        relatorio = await configurador.gerar_relatorio_configuracao()

        # Mostrar resultados
        print("\n" + "=" * 80)
        print("📊 RELATÓRIO DE CONFIGURAÇÃO")
        print("=" * 80)

        print(f"🐘 PostgreSQL: {relatorio['postgresql']['version']} ", end="")
        print("✅" if relatorio["postgresql"]["compatible"] else "❌")

        print(f"📦 pgvector: {relatorio['pgvector']['version']} ", end="")
        print("✅" if relatorio["pgvector"]["installed"] else "❌")

        status_emoji = {"ready": "🎉", "partial": "⚠️", "error": "❌", "unknown": "❓"}
        print(
            f"{status_emoji.get(relatorio['status'], '❓')} Status: {relatorio['status'].upper()}"
        )

        # Detalhes dos testes se executados
        if "testes" in relatorio and relatorio["testes"]:
            testes = relatorio["testes"]
            print(
                f"\n🧪 Funcionalidades básicas: {'✅' if testes.get('basic_functionality') else '❌'}"
            )
            print(
                f"⚙️ Configuração otimizada: {'✅' if testes.get('configuration') else '❌'}"
            )

            limites = testes.get("limits", {})
            print(
                f"🎯 Embeddings OpenAI (1536D): {'✅' if limites.get('openai_embedding_support') else '❌'}"
            )

            if limites.get("indices_suportados"):
                indices = ", ".join(limites["indices_suportados"]).upper()
                print(f"🗂️ Índices suportados: {indices}")

        # Resultado final e próximos passos
        print("\n" + "=" * 80)
        if relatorio["status"] == "ready":
            print("🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
            print("✅ pgvector está pronto para usar no Curso CrewAI")
            print("\n📋 Próximos passos:")
            print("  1. uv run aula7/scripts/01_criar_tabelas_embeddings.sql")
            print("  2. uv run aula7/scripts/02_migrar_dados_embeddings.py")
            print("  3. uv run aula7/scripts/03_testar_embeddings.py")

        elif relatorio["status"] == "partial":
            print("⚠️ CONFIGURAÇÃO PARCIAL")
            print("💡 pgvector está instalado mas pode ter limitações")
            print("🔄 Tente executar novamente ou verifique as permissões")

        else:
            print("❌ CONFIGURAÇÃO FALHOU")
            if not relatorio["pgvector"]["installed"]:
                print("🚫 pgvector não está instalado no sistema")
                imprimir_instrucoes_instalacao()
            else:
                print("🔧 pgvector instalado mas com problemas de configuração")
                print("💡 Tente conectar como superuser:")
                print("  sudo -u postgres psql -d curso")
                print("  CREATE EXTENSION IF NOT EXISTS vector;")

        # Salvar relatório
        relatorio_file = "pgvector_config_report.json"
        with open(relatorio_file, "w", encoding="utf-8") as f:
            json.dump(relatorio, f, indent=2, ensure_ascii=False)
        print(f"\n📄 Relatório detalhado salvo: {relatorio_file}")
        print("=" * 80)

        return relatorio["status"] == "ready"

    except KeyboardInterrupt:
        print("\n\n⏹️ Configuração interrompida pelo usuário")
        return False
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        return False

    finally:
        await configurador.desconectar()


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n👋 Até logo!")
        sys.exit(1)
