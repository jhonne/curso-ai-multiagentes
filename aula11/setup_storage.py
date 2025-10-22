"""
Configuração Centralizada de Storage para Aula 11

Este módulo DEVE ser importado ANTES de qualquer import do CrewAI
em TODOS os arquivos da aula11.

USO:
    from setup_storage import configurar_storage
    configurar_storage()
    
    # AGORA pode importar CrewAI
    from crewai import Agent, Task, Crew

PROPÓSITO:
    Garante que TODOS os arquivos do ChromaDB sejam criados em:
    .crewai_storage/chromadb/
    
    E NÃO na raiz da aula11!
"""

import os
from pathlib import Path


def configurar_storage(script_path=None):
    """
    Configura TODOS os paths de storage ANTES de importar CrewAI
    
    Args:
        script_path: Path do script atual (opcional, detecta automaticamente)
    
    Returns:
        tuple: (AULA11_ROOT, STORAGE_DIR, CHROMADB_DIR)
    """
    
    # Detectar raiz da aula11
    if script_path:
        current = Path(script_path).parent.absolute()
    else:
        current = Path(__file__).parent.absolute()
    
    # Se estamos em um subdiretório, subir até aula11
    while current.name != "aula11" and current.parent != current:
        current = current.parent
    
    AULA11_ROOT = current
    
    # Diretórios de storage
    STORAGE_DIR = AULA11_ROOT / ".crewai_storage"
    CHROMADB_DIR = STORAGE_DIR / "chromadb"
    
    # Criar diretórios
    STORAGE_DIR.mkdir(exist_ok=True)
    CHROMADB_DIR.mkdir(exist_ok=True)
    
    # ✅ CONFIGURAR TODAS AS VARIÁVEIS DE AMBIENTE
    # Estas DEVEM ser configuradas ANTES de importar CrewAI
    os.environ["CREWAI_STORAGE_DIR"] = str(STORAGE_DIR)
    os.environ["CHROMA_PERSIST_DIRECTORY"] = str(CHROMADB_DIR)
    os.environ["IS_PERSISTENT"] = "TRUE"
    
    # Configurações adicionais do ChromaDB
    os.environ["ANONYMIZED_TELEMETRY"] = "False"
    os.environ["ALLOW_RESET"] = "True"
    
    # ✅ MUDAR DIRETÓRIO DE TRABALHO
    # Isso previne que arquivos .lock sejam criados na raiz
    # Salvamos o diretório original para poder voltar se necessário
    original_cwd = os.getcwd()
    os.chdir(str(STORAGE_DIR))
    
    # Retornar informações úteis
    return {
        'AULA11_ROOT': AULA11_ROOT,
        'STORAGE_DIR': STORAGE_DIR,
        'CHROMADB_DIR': CHROMADB_DIR,
        'ORIGINAL_CWD': original_cwd
    }


def verificar_configuracao():
    """Verifica se a configuração está correta"""
    print("\n" + "=" * 70)
    print("🔍 VERIFICAÇÃO DE CONFIGURAÇÃO DE STORAGE")
    print("=" * 70)
    
    crewai_storage = os.environ.get("CREWAI_STORAGE_DIR")
    chroma_dir = os.environ.get("CHROMA_PERSIST_DIRECTORY")
    
    print(f"\n📁 CREWAI_STORAGE_DIR: {crewai_storage}")
    print(f"📁 CHROMA_PERSIST_DIRECTORY: {chroma_dir}")
    print(f"📂 Diretório atual: {os.getcwd()}")
    
    if crewai_storage and Path(crewai_storage).exists():
        print(f"\n✅ Storage configurado corretamente em: {crewai_storage}")
        print(f"✅ ChromaDB será criado em: {chroma_dir}")
    else:
        print("\n❌ Storage NÃO configurado!")
        print("💡 Execute: configurar_storage() antes de importar CrewAI")
    
    print("=" * 70)


def limpar_locks_raiz():
    """Remove arquivos .lock do ChromaDB da raiz da aula11"""
    aula11_root = Path(__file__).parent.absolute()
    locks_removidos = []
    
    for lock_file in aula11_root.glob("chromadb-*.lock"):
        try:
            lock_file.unlink()
            locks_removidos.append(lock_file.name)
        except Exception as e:
            print(f"⚠️ Não foi possível remover {lock_file.name}: {e}")
    
    if locks_removidos:
        print(f"\n🧹 Removidos {len(locks_removidos)} arquivos .lock da raiz:")
        for lock in locks_removidos:
            print(f"   ✓ {lock}")
    else:
        print("\n✅ Nenhum arquivo .lock encontrado na raiz")
    
    return locks_removidos


if __name__ == "__main__":
    print("🔧 SETUP STORAGE - Aula 11")
    print("\nEste módulo deve ser importado em TODOS os scripts da aula11")
    print("ANTES de importar CrewAI.\n")
    
    config = configurar_storage()
    verificar_configuracao()
    
    print("\n" + "=" * 70)
    print("🧹 LIMPANDO ARQUIVOS .lock DA RAIZ")
    print("=" * 70)
    limpar_locks_raiz()
    
    print("\n✅ Configuração completa!")
    print("\nPara usar em seus scripts:")
    print("""
from setup_storage import configurar_storage
configurar_storage()

# AGORA importar CrewAI
from crewai import Agent, Task, Crew
    """)
