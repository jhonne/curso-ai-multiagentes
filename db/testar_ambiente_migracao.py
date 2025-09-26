#!/usr/bin/env python3
"""
Script para testar a conexão com PostgreSQL e verificar dependências
Deve ser executado antes da migração para garantir que tudo está funcionando

Autor: Gerado pelo GitHub Copilot
Data: 26 de setembro de 2025
"""

import sys
import os
from datetime import datetime

def verificar_dependencias():
    """Verifica se as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    dependencias_ok = True
    
    # Verificar psycopg2
    try:
        import psycopg2
        print("✅ psycopg2 instalado")
    except ImportError:
        print("❌ psycopg2 não encontrado")
        print("   Instale com: pip install psycopg2-binary")
        dependencias_ok = False
    
    # Verificar sqlite3 (nativo do Python)
    try:
        import sqlite3
        print("✅ sqlite3 disponível (nativo)")
    except ImportError:
        print("❌ sqlite3 não disponível")
        dependencias_ok = False
    
    return dependencias_ok

def testar_conexao_postgresql():
    """Testa a conexão com o PostgreSQL"""
    print("\n🔌 Testando conexão PostgreSQL...")
    
    # Configurações padrão (mesmo do script principal)
    config = {
        'host': 'localhost',
        'port': '5432', 
        'database': 'curso',
        'user': 'postgres',
        'password': 'postgres'
    }
    
    print("📋 Configuração:")
    for key, value in config.items():
        if key == 'password':
            print(f"   {key}: {'*' * len(value)}")
        else:
            print(f"   {key}: {value}")
    
    try:
        import psycopg2
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        
        # Testar consulta básica
        cursor.execute("SELECT version();")
        versao = cursor.fetchone()[0]
        print(f"✅ Conexão PostgreSQL bem-sucedida")
        print(f"📊 Versão: {versao}")
        
        # Verificar se as tabelas existem
        tabelas_esperadas = [
            'ia_estabelecimento',
            'ia_queixa_principal',
            'ia_sintoma', 
            'ia_historico_atendimento_sintoma'
        ]
        
        print(f"\n📋 Verificando tabelas no banco 'curso':")
        for tabela in tabelas_esperadas:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
                count = cursor.fetchone()[0]
                print(f"✅ {tabela}: {count} registros")
            except Exception as e:
                print(f"❌ {tabela}: {e}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão PostgreSQL: {e}")
        print("\n💡 Dicas para resolver:")
        print("   1. Verifique se o PostgreSQL está rodando")
        print("   2. Confirme host, porta, usuário e senha")
        print("   3. Certifique-se que o banco 'curso' existe")
        print("   4. Verifique as permissões do usuário")
        return False

def testar_sqlite():
    """Testa a criação de arquivo SQLite"""
    print("\n💾 Testando SQLite...")
    
    try:
        import sqlite3
        
        # Criar arquivo de teste
        test_db = 'teste_sqlite.db'
        conn = sqlite3.connect(test_db)
        cursor = conn.cursor()
        
        # Criar tabela de teste
        cursor.execute('''
            CREATE TABLE teste (
                id INTEGER PRIMARY KEY,
                nome TEXT
            )
        ''')
        
        # Inserir dados de teste
        cursor.execute("INSERT INTO teste (nome) VALUES (?)", ("teste",))
        conn.commit()
        
        # Verificar dados
        cursor.execute("SELECT COUNT(*) FROM teste")
        count = cursor.fetchone()[0]
        
        conn.close()
        os.remove(test_db)  # Limpar arquivo de teste
        
        print(f"✅ SQLite funcionando corretamente")
        return True
        
    except Exception as e:
        print(f"❌ Erro no SQLite: {e}")
        return False

def mostrar_configuracoes():
    """Mostra as configurações que serão usadas na migração"""
    print("\n⚙️  Configurações da Migração:")
    print("   PostgreSQL:")
    print("     - Host: localhost")
    print("     - Porta: 5432")
    print("     - Banco: curso")
    print("     - Usuário: postgres")
    print("   SQLite:")
    print("     - Arquivo: curso.db")
    print("   Tabelas:")
    print("     - ia_estabelecimento")
    print("     - ia_queixa_principal")
    print("     - ia_sintoma")
    print("     - ia_historico_atendimento_sintoma")

def main():
    """Função principal"""
    print("="*60)
    print("🧪 TESTE DE AMBIENTE - MIGRAÇÃO PostgreSQL -> SQLite")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    tudo_ok = True
    
    # 1. Verificar dependências
    if not verificar_dependencias():
        tudo_ok = False
    
    # 2. Testar PostgreSQL
    if not testar_conexao_postgresql():
        tudo_ok = False
    
    # 3. Testar SQLite
    if not testar_sqlite():
        tudo_ok = False
    
    # 4. Mostrar configurações
    mostrar_configuracoes()
    
    # Resultado final
    print("\n" + "="*60)
    if tudo_ok:
        print("✅ AMBIENTE PRONTO PARA MIGRAÇÃO!")
        print("🚀 Execute: python migrar_postgres_para_sqlite.py")
    else:
        print("❌ PROBLEMAS ENCONTRADOS!")
        print("🔧 Resolva os erros acima antes de continuar")
    print("="*60)

if __name__ == "__main__":
    main()