#!/usr/bin/env -S uv run
"""
Script de Verificação de Storage - Aula 11
Verifica se os arquivos do ChromaDB estão organizados corretamente

USO:
    uv run aula11/verificar_storage.py
"""

import os
from pathlib import Path


def verificar_storage():
    """Verifica organização dos arquivos de storage"""
    
    print("=" * 70)
    print("🔍 VERIFICAÇÃO DE STORAGE - AULA 11")
    print("=" * 70)
    
    # Diretórios
    aula11_root = Path(__file__).parent.absolute()
    storage_dir = aula11_root / ".crewai_storage"
    chromadb_dir = aula11_root / ".chromadb"
    
    # Status geral
    status_ok = True
    
    # 1. Verificar arquivos lock na raiz (NÃO devem existir)
    print("\n1️⃣  Verificando arquivos lock na raiz da aula11...")
    lock_files_raiz = list(aula11_root.glob("chromadb-*.lock"))
    
    if lock_files_raiz:
        print("   ❌ PROBLEMA: Encontrados arquivos lock na raiz!")
        for f in lock_files_raiz:
            print(f"      - {f.name}")
        print("   💡 Execute: rm -f chromadb-*.lock")
        status_ok = False
    else:
        print("   ✅ OK: Nenhum arquivo lock na raiz")
    
    # 2. Verificar diretório .crewai_storage
    print("\n2️⃣  Verificando diretório .crewai_storage...")
    
    if not storage_dir.exists():
        print("   ⚠️  Diretório não existe (será criado na primeira execução)")
    else:
        print(f"   ✅ Diretório existe: {storage_dir}")
        
        # Contar arquivos
        arquivos = list(storage_dir.rglob("*"))
        arquivos_apenas = [f for f in arquivos if f.is_file()]
        diretorios = [f for f in arquivos if f.is_dir()]
        
        print(f"   📁 {len(diretorios)} diretórios")
        print(f"   📄 {len(arquivos_apenas)} arquivos")
        
        # Verificar arquivos importantes
        db_files = list(storage_dir.glob("*.db"))
        lock_files = list(storage_dir.glob("chromadb-*.lock"))
        
        if db_files:
            print(f"   ✅ {len(db_files)} arquivos de banco de dados (.db)")
        if lock_files:
            print(f"   ✅ {len(lock_files)} arquivos lock (dentro do storage)")
    
    # 3. Verificar diretório .chromadb
    print("\n3️⃣  Verificando diretório .chromadb...")
    
    if not chromadb_dir.exists():
        print("   ⚠️  Diretório não existe (será criado automaticamente)")
    else:
        print(f"   ✅ Diretório existe: {chromadb_dir}")
        
        arquivos = list(chromadb_dir.rglob("*"))
        if not arquivos:
            print("   📂 Vazio (normal, CrewAI usa .crewai_storage)")
        else:
            print(f"   📂 {len(arquivos)} itens")
    
    # 4. Verificar variáveis de ambiente no main.py
    print("\n4️⃣  Verificando configuração no main.py...")
    
    main_py = aula11_root / "main.py"
    if main_py.exists():
        content = main_py.read_text()
        
        checks = {
            'load_dotenv()': 'Carrega .env',
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# ✅ Configurar storage ANTES de importar CrewAI
load_dotenv()
from setup_storage import configurar_storage
config = configurar_storage(__file__)

# ✅ AGORA importar CrewAI
            'from crewai import': 'Importa CrewAI'
        }
        
        all_found = True
        for check, descricao in checks.items():
            if check in content:
                print(f"   ✅ {descricao}")
            else:
                print(f"   ❌ FALTA: {descricao}")
                all_found = False
                status_ok = False
        
        # Verificar ordem correta (load_dotenv antes de imports)
        dotenv_pos = content.find('load_dotenv()')
        import_pos = content.find('from crewai import')
        
        if dotenv_pos > 0 and import_pos > 0:
            if dotenv_pos < import_pos:
                print("   ✅ Ordem correta: load_dotenv() antes de imports")
            else:
                print("   ❌ PROBLEMA: load_dotenv() deve vir antes dos imports!")
                status_ok = False
    else:
        print("   ❌ main.py não encontrado!")
        status_ok = False
    
    # 5. Resumo final
    print("\n" + "=" * 70)
    if status_ok:
        print("✅ TUDO OK! Storage configurado corretamente")
    else:
        print("❌ PROBLEMAS ENCONTRADOS - Verifique os itens acima")
    print("=" * 70)
    
    # 6. Informações adicionais
    print("\n📚 Documentação:")
    print("   - VERIFICACAO_STORAGE.md - Status atual")
    print("   - SOLUCAO_ARQUIVOS_LOCK.md - Solução implementada")
    print("   - PROBLEMA_STORAGE_CHROMADB.md - Histórico")
    
    return status_ok


if __name__ == "__main__":
    import sys
    
    try:
        sucesso = verificar_storage()
        sys.exit(0 if sucesso else 1)
    except Exception as e:
        print(f"\n❌ Erro durante verificação: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(2)
