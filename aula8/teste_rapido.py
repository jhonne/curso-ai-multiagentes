#!/usr/bin/env python3
"""
🧪 TESTE RÁPIDO: Aula 8 - Sistema Interativo SQLite
==================================================

Script de teste para verificar se o sistema da Aula 8 está funcionando corretamente.
Executa algumas consultas básicas para validar a integração CrewAI + SQLite.

EXECUÇÃO:
uv run aula8/teste_rapido.py
"""

import sqlite3
from pathlib import Path
from dotenv import load_dotenv
import os

# Configuração
load_dotenv()
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "db" / "curso.db"

print("🧪 TESTE RÁPIDO - Aula 8")
print("=" * 40)

def testar_banco_sqlite():
    """Testa conexão e consultas básicas no SQLite"""
    
    print("🔍 1. Testando conexão com SQLite...")
    
    try:
        if not DB_PATH.exists():
            print(f"❌ Banco não encontrado: {DB_PATH}")
            return False
        
        conn = sqlite3.connect(str(DB_PATH))
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Testar tabelas
        print("📊 2. Verificando tabelas disponíveis...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas = [row[0] for row in cursor.fetchall()]
        print(f"   Tabelas encontradas: {len(tabelas)}")
        for tabela in tabelas[:5]:  # Mostrar primeiras 5
            print(f"   • {tabela}")
        
        # Testar dados de estabelecimentos
        print("🏥 3. Testando dados de estabelecimentos...")
        cursor.execute("SELECT COUNT(*) FROM ia_estabelecimento")
        total_est = cursor.fetchone()[0]
        print(f"   Total de estabelecimentos: {total_est:,}")
        
        # Mostrar alguns exemplos
        cursor.execute("""
            SELECT nome, bairro FROM ia_estabelecimento 
            ORDER BY nome LIMIT 5
        """)
        exemplos = cursor.fetchall()
        print("   Exemplos:")
        for est in exemplos:
            print(f"   • {est['nome']} ({est['bairro']})")
        
        # Testar queixas
        print("🏥 4. Testando dados de queixas...")
        cursor.execute("SELECT COUNT(*) FROM ia_queixa_principal")
        total_queixas = cursor.fetchone()[0]
        print(f"   Total de queixas: {total_queixas:,}")
        
        cursor.execute("""
            SELECT q.nome, COUNT(*) as total
            FROM ia_queixa_principal q
            JOIN ia_historico_atendimento_sintoma h ON q.id = h.queixa_principal_id
            GROUP BY q.id, q.nome
            ORDER BY total DESC
            LIMIT 3
        """)
        top_queixas = cursor.fetchall()
        print("   Top 3 queixas:")
        for queixa in top_queixas:
            print(f"   • {queixa['nome']}: {queixa['total']:,} casos")
        
        conn.close()
        print("✅ Banco SQLite funcionando perfeitamente!")
        return True
        
    except Exception as e:
        print(f"❌ Erro no SQLite: {e}")
        return False

def testar_openai_config():
    """Testa configuração da OpenAI API"""
    
    print("🤖 5. Testando configuração OpenAI...")
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OpenAI API Key não configurada")
        print("💡 Configure no arquivo .env: OPENAI_API_KEY=sua_chave")
        return False
    
    if len(api_key) < 20:
        print("⚠️ API Key parece incompleta")
        return False
    
    print("✅ OpenAI API Key configurada")
    return True

def testar_dependencias():
    """Testa se todas as dependências estão instaladas"""
    
    print("📦 6. Testando dependências...")
    
    try:
        import crewai
        print(f"   ✅ CrewAI: {crewai.__version__ if hasattr(crewai, '__version__') else 'OK'}")
        
        from langchain_openai import ChatOpenAI
        print("   ✅ LangChain OpenAI: OK")
        
        import sqlite3
        print("   ✅ SQLite3: OK")
        
        from dotenv import load_dotenv
        print("   ✅ python-dotenv: OK")
        
        return True
        
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        print("💡 Execute: uv sync")
        return False

def main():
    """Função principal de teste"""
    
    print("🎯 Executando bateria de testes para Aula 8...\n")
    
    testes = [
        testar_dependencias(),
        testar_banco_sqlite(),
        testar_openai_config()
    ]
    
    print("\n" + "="*40)
    print("📋 RESULTADO DOS TESTES:")
    print("="*40)
    
    sucessos = sum(testes)
    total = len(testes)
    
    if sucessos == total:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ Sistema da Aula 8 está pronto para uso!")
        print("\n🚀 Para executar o sistema completo:")
        print("   uv run aula8/main.py")
        print("\n📚 Para exercícios práticos:")
        print("   uv run aula8/exercicios/exercicio1_consultas_basicas.py")
        print("   uv run aula8/exercicios/exercicio2_interface_melhorada.py")
        
    else:
        print(f"⚠️ {sucessos}/{total} testes passaram")
        print("❌ Corrija os problemas antes de continuar")
        
        if not testes[0]:  # dependências
            print("\n💡 SOLUÇÃO: uv sync")
        if not testes[2]:  # openai
            print("\n💡 SOLUÇÃO: Configure OpenAI no .env ou execute:")
            print("   uv run configurar.py")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Teste interrompido")
    except Exception as e:
        print(f"\n❌ Erro no teste: {e}")