#!/usr/bin/env python3
"""
Script para migrar dados do banco PostgreSQL para SQLite
Migra as tabelas: ia_estabelecimento, ia_queixa_principal, ia_sintoma, ia_historico_atendimento_sintoma

Autor: Gerado pelo GitHub Copilot
Data: 26 de setembro de 2025
"""

import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import sys
from datetime import datetime
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('migracao.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Configurações do banco PostgreSQL
POSTGRES_CONFIG = {
    'host': 'localhost',
    'port': '5432',
    'database': 'curso',
    'user': 'postgres',
    'password': 'arpus'
}

# Arquivo do banco SQLite
SQLITE_DB = 'curso.db'

class MigradorDados:
    def __init__(self):
        self.conn_pg = None
        self.conn_sqlite = None
        
    def conectar_postgresql(self):
        """Conecta ao banco PostgreSQL"""
        try:
            logger.info("Conectando ao PostgreSQL...")
            self.conn_pg = psycopg2.connect(**POSTGRES_CONFIG)
            logger.info("✅ Conexão PostgreSQL estabelecida com sucesso")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao conectar PostgreSQL: {e}")
            return False
    
    def conectar_sqlite(self):
        """Conecta/cria o banco SQLite"""
        try:
            logger.info(f"Conectando ao SQLite: {SQLITE_DB}")
            self.conn_sqlite = sqlite3.connect(SQLITE_DB)
            logger.info("✅ Conexão SQLite estabelecida com sucesso")
            return True
        except Exception as e:
            logger.error(f"❌ Erro ao conectar SQLite: {e}")
            return False
    
    def criar_tabelas_sqlite(self):
        """Cria as tabelas no banco SQLite"""
        try:
            cursor = self.conn_sqlite.cursor()
            
            # Tabela ia_estabelecimento
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ia_estabelecimento (
                    cnes TEXT PRIMARY KEY,
                    nome TEXT,
                    endereco TEXT,
                    fone TEXT,
                    bairro TEXT,
                    longitude REAL,
                    latitude REAL
                )
            ''')
            
            # Tabela ia_queixa_principal
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ia_queixa_principal (
                    id INTEGER PRIMARY KEY,
                    nome TEXT
                )
            ''')
            
            # Tabela ia_sintoma
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ia_sintoma (
                    id INTEGER PRIMARY KEY,
                    nome TEXT
                )
            ''')
            
            # Tabela ia_historico_atendimento_sintoma
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS ia_historico_atendimento_sintoma (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    estabelecimento_cnes TEXT,
                    queixa_principal_id INTEGER,
                    sintoma_id INTEGER,
                    FOREIGN KEY (estabelecimento_cnes) REFERENCES ia_estabelecimento(cnes),
                    FOREIGN KEY (queixa_principal_id) REFERENCES ia_queixa_principal(id),
                    FOREIGN KEY (sintoma_id) REFERENCES ia_sintoma(id)
                )
            ''')
            
            self.conn_sqlite.commit()
            logger.info("✅ Tabelas criadas no SQLite com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar tabelas SQLite: {e}")
            return False
    
    def migrar_tabela(self, nome_tabela, colunas_select=None):
        """Migra uma tabela específica do PostgreSQL para SQLite"""
        try:
            logger.info(f"📊 Iniciando migração da tabela: {nome_tabela}")
            
            # Cursor PostgreSQL
            cursor_pg = self.conn_pg.cursor(cursor_factory=RealDictCursor)
            cursor_sqlite = self.conn_sqlite.cursor()
            
            # Definir colunas específicas ou todas
            if colunas_select:
                select_cols = ', '.join(colunas_select)
                placeholders = ', '.join(['?' for _ in colunas_select])
            else:
                select_cols = '*'
            
            # Buscar dados do PostgreSQL
            cursor_pg.execute(f"SELECT {select_cols} FROM {nome_tabela}")
            registros = cursor_pg.fetchall()
            
            if not registros:
                logger.warning(f"⚠️  Tabela {nome_tabela} está vazia no PostgreSQL")
                return True
            
            logger.info(f"📈 Encontrados {len(registros)} registros na tabela {nome_tabela}")
            
            # Preparar inserção no SQLite
            if not colunas_select:
                colunas_select = [desc[0] for desc in cursor_pg.description]
                placeholders = ', '.join(['?' for _ in colunas_select])
            
            colunas_str = ', '.join(colunas_select)
            
            # Limpar tabela SQLite se existir dados
            cursor_sqlite.execute(f"DELETE FROM {nome_tabela}")
            
            # Inserir dados
            insert_sql = f"INSERT INTO {nome_tabela} ({colunas_str}) VALUES ({placeholders})"
            
            registros_inseridos = 0
            for registro in registros:
                try:
                    # Converter dict para tupla na ordem das colunas
                    if isinstance(registro, dict):
                        valores = tuple(registro[col] for col in colunas_select)
                    else:
                        valores = tuple(registro)
                    
                    cursor_sqlite.execute(insert_sql, valores)
                    registros_inseridos += 1
                    
                except Exception as e:
                    logger.error(f"❌ Erro ao inserir registro na tabela {nome_tabela}: {e}")
                    logger.error(f"Registro problemático: {registro}")
            
            self.conn_sqlite.commit()
            logger.info(f"✅ Tabela {nome_tabela}: {registros_inseridos} registros migrados com sucesso")
            
            # Validar migração
            cursor_sqlite.execute(f"SELECT COUNT(*) FROM {nome_tabela}")
            count_sqlite = cursor_sqlite.fetchone()[0]
            logger.info(f"🔍 Validação - Registros em SQLite: {count_sqlite}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro ao migrar tabela {nome_tabela}: {e}")
            return False
    
    def validar_migracao(self):
        """Valida se a migração foi bem-sucedida"""
        try:
            logger.info("🔍 Iniciando validação da migração...")
            
            tabelas = [
                'ia_estabelecimento',
                'ia_queixa_principal', 
                'ia_sintoma',
                'ia_historico_atendimento_sintoma'
            ]
            
            cursor_pg = self.conn_pg.cursor()
            cursor_sqlite = self.conn_sqlite.cursor()
            
            for tabela in tabelas:
                # Contar registros no PostgreSQL
                cursor_pg.execute(f"SELECT COUNT(*) FROM {tabela}")
                count_pg = cursor_pg.fetchone()[0]
                
                # Contar registros no SQLite
                cursor_sqlite.execute(f"SELECT COUNT(*) FROM {tabela}")
                count_sqlite = cursor_sqlite.fetchone()[0]
                
                status = "✅" if count_pg == count_sqlite else "❌"
                logger.info(f"{status} {tabela}: PostgreSQL={count_pg}, SQLite={count_sqlite}")
                
                if count_pg != count_sqlite:
                    logger.warning(f"⚠️  Inconsistência na tabela {tabela}")
            
            logger.info("🎉 Validação concluída")
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro na validação: {e}")
            return False
    
    def executar_migracao(self):
        """Executa todo o processo de migração"""
        try:
            logger.info("🚀 Iniciando processo de migração PostgreSQL -> SQLite")
            logger.info(f"📅 Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Conectar aos bancos
            if not self.conectar_postgresql():
                return False
                
            if not self.conectar_sqlite():
                return False
            
            # Criar estrutura SQLite
            if not self.criar_tabelas_sqlite():
                return False
            
            # Migrar cada tabela
            tabelas_config = {
                'ia_estabelecimento': ['cnes', 'nome', 'endereco', 'fone', 'bairro', 'longitude', 'latitude'],
                'ia_queixa_principal': ['id', 'nome'],
                'ia_sintoma': ['id', 'nome'],
                'ia_historico_atendimento_sintoma': ['estabelecimento_cnes', 'queixa_principal_id', 'sintoma_id']
            }
            
            for tabela, colunas in tabelas_config.items():
                if not self.migrar_tabela(tabela, colunas):
                    logger.error(f"❌ Falha na migração da tabela {tabela}")
                    return False
            
            # Validar migração
            self.validar_migracao()
            
            logger.info("🎉 Migração concluída com sucesso!")
            logger.info(f"📁 Banco SQLite criado: {os.path.abspath(SQLITE_DB)}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Erro no processo de migração: {e}")
            return False
            
        finally:
            # Fechar conexões
            if self.conn_pg:
                self.conn_pg.close()
                logger.info("📴 Conexão PostgreSQL fechada")
            
            if self.conn_sqlite:
                self.conn_sqlite.close()
                logger.info("📴 Conexão SQLite fechada")

def main():
    """Função principal"""
    print("="*60)
    print("🔄 MIGRADOR DE DADOS: PostgreSQL -> SQLite")
    print("="*60)
    print(f"📋 Tabelas a migrar:")
    print("   • ia_estabelecimento")
    print("   • ia_queixa_principal") 
    print("   • ia_sintoma")
    print("   • ia_historico_atendimento_sintoma")
    print("="*60)
    
    # Verificar se arquivo SQLite já existe
    if os.path.exists(SQLITE_DB):
        resposta = input(f"⚠️  Arquivo {SQLITE_DB} já existe. Sobrescrever? (s/N): ")
        if resposta.lower() not in ['s', 'sim', 'y', 'yes']:
            print("❌ Migração cancelada pelo usuário")
            return
        
        os.remove(SQLITE_DB)
        print(f"🗑️  Arquivo {SQLITE_DB} removido")
    
    # Executar migração
    migrador = MigradorDados()
    sucesso = migrador.executar_migracao()
    
    if sucesso:
        print("\n" + "="*60)
        print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print(f"📁 Banco SQLite: {os.path.abspath(SQLITE_DB)}")
        print("📋 Log detalhado: migracao.log")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("❌ MIGRAÇÃO FALHOU!")
        print("📋 Verifique o log para mais detalhes: migracao.log")
        print("="*60)

if __name__ == "__main__":
    main()