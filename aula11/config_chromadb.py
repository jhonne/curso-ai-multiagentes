"""
Configuração centralizada para RAG com ChromaDB
Define o diretório padrão para armazenamento do ChromaDB
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configurar diretório base da aula11
AULA11_DIR = Path(__file__).parent.absolute()

# Configurar diretório ÚNICO de storage (.crewai_storage)
STORAGE_DIR = AULA11_DIR / ".crewai_storage"
STORAGE_DIR.mkdir(exist_ok=True)

# ChromaDB dentro de .crewai_storage
CHROMADB_DIR = STORAGE_DIR / "chromadb"
CHROMADB_DIR.mkdir(exist_ok=True)

# Configurar variáveis de ambiente para o ChromaDB
os.environ["CREWAI_STORAGE_DIR"] = str(STORAGE_DIR)
os.environ["CHROMA_PERSIST_DIRECTORY"] = str(CHROMADB_DIR)
os.environ["IS_PERSISTENT"] = os.getenv("IS_PERSISTENT", "TRUE")


# Para scripts executados em subdiretórios (modulos/*)
# detectar e usar o .chromadb da raiz
def get_chromadb_path():
    """Retorna o caminho para o diretório ChromaDB"""
    current = Path.cwd()
    
    # Se estamos em um módulo, volta para a raiz da aula11
    if "modulos" in str(current):
        # Procura pela raiz da aula11
        while current.name != "aula11" and current.parent != current:
            current = current.parent
        return current / ".crewai_storage" / "chromadb"
    
    return CHROMADB_DIR


def setup_chromadb():
    """Configura o ChromaDB para usar diretório centralizado"""
    chromadb_path = get_chromadb_path()
    chromadb_path.mkdir(parents=True, exist_ok=True)
    
    # Configurar também o storage dir pai
    storage_dir = chromadb_path.parent
    os.environ["CREWAI_STORAGE_DIR"] = str(storage_dir)
    os.environ["CHROMA_PERSIST_DIRECTORY"] = str(chromadb_path)
    
    return chromadb_path


# Executar configuração automaticamente ao importar
CHROMADB_PATH = setup_chromadb()

# Informações úteis para debug
if __name__ == "__main__":
    print("=" * 60)
    print("CONFIGURAÇÃO CHROMADB")
    print("=" * 60)
    print(f"📁 Diretório da Aula11: {AULA11_DIR}")
    print(f"💾 Diretório ChromaDB: {CHROMADB_PATH}")
    print(f"✅ Diretório existe: {CHROMADB_PATH.exists()}")
    print("📋 Arquivos no ChromaDB:")
    
    if CHROMADB_PATH.exists():
        files = list(CHROMADB_PATH.glob("*"))
        if files:
            for f in files[:10]:  # Mostrar até 10 arquivos
                print(f"   - {f.name}")
            if len(files) > 10:
                print(f"   ... e mais {len(files) - 10} arquivos")
        else:
            print("   (vazio)")
    print("=" * 60)
