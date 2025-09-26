#!/usr/bin/env python3
"""
Script de configuração para a migração PostgreSQL -> SQLite
Permite personalizar as credenciais de conexão

Autor: Gerado pelo GitHub Copilot
Data: 26 de setembro de 2025
"""

import os
import json
import getpass
from pathlib import Path

CONFIG_FILE = "config_migracao.json"

def obter_credenciais_postgres():
    """Obtém as credenciais do PostgreSQL do usuário"""
    print("📋 Configuração do PostgreSQL")
    print("Por favor, insira as credenciais do seu banco PostgreSQL:")
    print()
    
    config = {}
    
    # Host
    host = input("🏠 Host [localhost]: ").strip()
    config['host'] = host if host else 'localhost'
    
    # Porta
    porta = input("🔌 Porta [5432]: ").strip()
    config['port'] = porta if porta else '5432'
    
    # Database
    database = input("💾 Nome do banco [curso]: ").strip()
    config['database'] = database if database else 'curso'
    
    # Usuário
    usuario = input("👤 Usuário [postgres]: ").strip()
    config['user'] = usuario if usuario else 'postgres'
    
    # Senha
    senha = getpass.getpass("🔐 Senha: ")
    config['password'] = senha
    
    return config

def testar_conexao(config):
    """Testa a conexão com as credenciais fornecidas"""
    try:
        import psycopg2
        print("\n🔍 Testando conexão...")
        
        conn = psycopg2.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        versao = cursor.fetchone()[0]
        
        print("✅ Conexão bem-sucedida!")
        print(f"📊 PostgreSQL: {versao.split(',')[0]}")
        
        # Verificar se o banco tem as tabelas necessárias
        tabelas = [
            'ia_estabelecimento',
            'ia_queixa_principal', 
            'ia_sintoma',
            'ia_historico_atendimento_sintoma'
        ]
        
        print(f"\n📋 Verificando tabelas no banco '{config['database']}':")
        tabelas_encontradas = 0
        
        for tabela in tabelas:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
                count = cursor.fetchone()[0]
                print(f"✅ {tabela}: {count:,} registros")
                tabelas_encontradas += 1
            except Exception as e:
                print(f"❌ {tabela}: {str(e)[:60]}...")
        
        conn.close()
        
        if tabelas_encontradas == len(tabelas):
            print(f"\n🎉 Todas as {len(tabelas)} tabelas encontradas!")
            return True
        else:
            print(f"\n⚠️  Apenas {tabelas_encontradas}/{len(tabelas)} tabelas encontradas")
            print("💡 Execute os scripts SQL da pasta /sql primeiro")
            return False
            
    except Exception as e:
        print(f"\n❌ Erro na conexão: {e}")
        return False

def salvar_configuracao(config):
    """Salva a configuração em arquivo JSON"""
    try:
        # Criar cópia sem a senha para logging
        config_log = config.copy()
        config_log['password'] = '*' * len(config['password'])
        
        # Salvar configuração completa
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"\n💾 Configuração salva em: {CONFIG_FILE}")
        print("📋 Configuração:")
        for key, value in config_log.items():
            print(f"   {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao salvar configuração: {e}")
        return False

def carregar_configuracao():
    """Carrega configuração existente"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
            print(f"📖 Configuração carregada de: {CONFIG_FILE}")
            return config
        return None
    except Exception as e:
        print(f"❌ Erro ao carregar configuração: {e}")
        return None

def atualizar_script_migracao(config):
    """Atualiza o script de migração com as novas credenciais"""
    try:
        script_path = "migrar_postgres_para_sqlite.py"
        
        if not os.path.exists(script_path):
            print(f"❌ Script {script_path} não encontrado")
            return False
        
        # Ler o script atual
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Construir nova configuração
        nova_config = f"""POSTGRES_CONFIG = {{
    'host': '{config['host']}',
    'port': '{config['port']}',
    'database': '{config['database']}',
    'user': '{config['user']}',
    'password': '{config['password']}'
}}"""
        
        # Substituir configuração existente
        import re
        pattern = r"POSTGRES_CONFIG\s*=\s*\{[^}]*\}"
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, nova_config, content, flags=re.DOTALL)
        else:
            print("⚠️  Não foi possível localizar POSTGRES_CONFIG no script")
            return False
        
        # Salvar script atualizado
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Script {script_path} atualizado com novas credenciais")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao atualizar script: {e}")
        return False

def main():
    """Função principal"""
    print("="*60)
    print("⚙️  CONFIGURADOR DE MIGRAÇÃO PostgreSQL -> SQLite")
    print("="*60)
    
    # Verificar se já existe configuração
    config_existente = carregar_configuracao()
    
    if config_existente:
        resposta = input("\n📄 Configuração encontrada. Usar existente? (s/N): ")
        if resposta.lower() in ['s', 'sim', 'y', 'yes']:
            config = config_existente
        else:
            config = obter_credenciais_postgres()
    else:
        config = obter_credenciais_postgres()
    
    # Testar conexão
    if testar_conexao(config):
        print("\n🎯 Próximos passos:")
        
        # Salvar configuração
        if salvar_configuracao(config):
            # Atualizar script de migração
            if atualizar_script_migracao(config):
                print("\n✅ Configuração concluída!")
                print("🚀 Execute agora: uv run python migrar_postgres_para_sqlite.py")
            else:
                print("\n⚠️  Configuração salva, mas falha ao atualizar script")
                print("🔧 Edite manualmente o arquivo migrar_postgres_para_sqlite.py")
        else:
            print("\n❌ Falha ao salvar configuração")
    else:
        print("\n🔧 Resolva os problemas de conexão antes de continuar")
        
        # Perguntar se quer salvar mesmo assim
        resposta = input("\n💾 Salvar configuração mesmo assim? (s/N): ")
        if resposta.lower() in ['s', 'sim', 'y', 'yes']:
            salvar_configuracao(config)
            atualizar_script_migracao(config)
    
    print("\n" + "="*60)

if __name__ == "__main__":
    main()