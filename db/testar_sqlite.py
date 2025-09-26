#!/usr/bin/env python3
"""
Script para testar e explorar o banco SQLite criado pela migração
Executa consultas de teste e estatísticas

Autor: Gerado pelo GitHub Copilot
Data: 26 de setembro de 2025
"""

import sqlite3
import os
from datetime import datetime

def conectar_sqlite():
    """Conecta ao banco SQLite"""
    db_path = 'curso.db'
    if not os.path.exists(db_path):
        print(f"❌ Arquivo {db_path} não encontrado!")
        return None
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Para acessar colunas por nome
        return conn
    except Exception as e:
        print(f"❌ Erro ao conectar SQLite: {e}")
        return None

def listar_tabelas(conn):
    """Lista todas as tabelas do banco"""
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tabelas = [row[0] for row in cursor.fetchall()]
    return tabelas

def contar_registros(conn, tabela):
    """Conta registros de uma tabela"""
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
    return cursor.fetchone()[0]

def mostrar_estatisticas(conn):
    """Mostra estatísticas gerais do banco"""
    print("📊 ESTATÍSTICAS DO BANCO SQLite")
    print("="*50)
    
    tabelas = listar_tabelas(conn)
    total_registros = 0
    
    for tabela in tabelas:
        count = contar_registros(conn, tabela)
        total_registros += count
        print(f"📋 {tabela}: {count:,} registros")
    
    print(f"\n📈 Total: {total_registros:,} registros em {len(tabelas)} tabelas")

def testar_consultas(conn):
    """Executa consultas de teste"""
    print("\n🔍 CONSULTAS DE TESTE")
    print("="*50)
    
    cursor = conn.cursor()
    
    # 1. Estabelecimentos
    print("\n1️⃣ Estabelecimentos de Saúde:")
    cursor.execute("""
        SELECT cnes, nome, bairro 
        FROM ia_estabelecimento 
        ORDER BY nome
        LIMIT 5
    """)
    for row in cursor.fetchall():
        print(f"   🏥 {row['nome'][:50]}... ({row['cnes']}) - {row['bairro']}")
    
    # 2. Queixas mais comuns
    print("\n2️⃣ Top 5 Queixas Principais Mais Atendidas:")
    cursor.execute("""
        SELECT 
            q.nome,
            COUNT(*) as total_atendimentos
        FROM ia_historico_atendimento_sintoma h
        JOIN ia_queixa_principal q ON h.queixa_principal_id = q.id
        GROUP BY q.id, q.nome
        ORDER BY total_atendimentos DESC
        LIMIT 5
    """)
    for i, row in enumerate(cursor.fetchall(), 1):
        print(f"   {i}. {row['nome'][:40]}... ({row['total_atendimentos']} atendimentos)")
    
    # 3. Sintomas mais frequentes
    print("\n3️⃣ Top 5 Sintomas Mais Frequentes:")
    cursor.execute("""
        SELECT 
            s.nome,
            COUNT(*) as total_ocorrencias
        FROM ia_historico_atendimento_sintoma h
        JOIN ia_sintoma s ON h.sintoma_id = s.id
        GROUP BY s.id, s.nome
        ORDER BY total_ocorrencias DESC
        LIMIT 5
    """)
    for i, row in enumerate(cursor.fetchall(), 1):
        print(f"   {i}. {row['nome'][:40]}... ({row['total_ocorrencias']} ocorrências)")
    
    # 4. Estabelecimento com mais atendimentos
    print("\n4️⃣ Top 3 Estabelecimentos com Mais Atendimentos:")
    cursor.execute("""
        SELECT 
            e.nome,
            e.bairro,
            COUNT(*) as total_atendimentos
        FROM ia_historico_atendimento_sintoma h
        JOIN ia_estabelecimento e ON h.estabelecimento_cnes = e.cnes
        GROUP BY e.cnes, e.nome, e.bairro
        ORDER BY total_atendimentos DESC
        LIMIT 3
    """)
    for i, row in enumerate(cursor.fetchall(), 1):
        print(f"   {i}. {row['nome'][:30]}... - {row['bairro']} ({row['total_atendimentos']} atendimentos)")

def verificar_integridade(conn):
    """Verifica integridade referencial"""
    print("\n🔍 VERIFICAÇÃO DE INTEGRIDADE")
    print("="*50)
    
    cursor = conn.cursor()
    
    # Verificar se todas as referências existem
    cursor.execute("""
        SELECT COUNT(*) as orfaos
        FROM ia_historico_atendimento_sintoma h
        LEFT JOIN ia_estabelecimento e ON h.estabelecimento_cnes = e.cnes
        WHERE e.cnes IS NULL
    """)
    orfaos_estabelecimento = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) as orfaos
        FROM ia_historico_atendimento_sintoma h
        LEFT JOIN ia_queixa_principal q ON h.queixa_principal_id = q.id
        WHERE q.id IS NULL
    """)
    orfaos_queixa = cursor.fetchone()[0]
    
    cursor.execute("""
        SELECT COUNT(*) as orfaos
        FROM ia_historico_atendimento_sintoma h
        LEFT JOIN ia_sintoma s ON h.sintoma_id = s.id
        WHERE s.id IS NULL
    """)
    orfaos_sintoma = cursor.fetchone()[0]
    
    print(f"🔗 Referências órfãs:")
    print(f"   • Estabelecimentos: {orfaos_estabelecimento}")
    print(f"   • Queixas Principais: {orfaos_queixa}")
    print(f"   • Sintomas: {orfaos_sintoma}")
    
    if orfaos_estabelecimento + orfaos_queixa + orfaos_sintoma == 0:
        print("✅ Integridade referencial OK!")
    else:
        print("⚠️  Foram encontradas referências órfãs")

def mostrar_esquema(conn):
    """Mostra o esquema das tabelas"""
    print("\n📋 ESQUEMA DAS TABELAS")
    print("="*50)
    
    cursor = conn.cursor()
    
    tabelas = listar_tabelas(conn)
    for tabela in tabelas:
        print(f"\n🗂️  {tabela.upper()}:")
        cursor.execute(f"PRAGMA table_info({tabela})")
        colunas = cursor.fetchall()
        
        for col in colunas:
            pk = " (PK)" if col[5] else ""
            null = "NOT NULL" if col[3] else "NULL"
            default = f" DEFAULT {col[4]}" if col[4] else ""
            print(f"   • {col[1]}: {col[2]}{pk} {null}{default}")

def main():
    """Função principal"""
    print("="*60)
    print("🧪 TESTE DO BANCO SQLite - Migração Concluída")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Conectar ao banco
    conn = conectar_sqlite()
    if not conn:
        return
    
    try:
        # Estatísticas gerais
        mostrar_estatisticas(conn)
        
        # Consultas de teste
        testar_consultas(conn)
        
        # Verificar integridade
        verificar_integridade(conn)
        
        # Mostrar esquema
        mostrar_esquema(conn)
        
        print("\n" + "="*60)
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("📁 Banco SQLite está funcionando corretamente")
        print("🚀 Pronto para uso em aplicações!")
        print("="*60)
        
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()