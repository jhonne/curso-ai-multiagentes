#!/usr/bin/env python3
"""Teste rápido para verificar onde o ChromaDB está criando arquivos"""

import os
from pathlib import Path

# Configurar ANTES de imports
AULA11_ROOT = Path(__file__).parent.absolute()
STORAGE_DIR = AULA11_ROOT / ".crewai_storage"
CHROMADB_DIR = STORAGE_DIR / "chromadb"

STORAGE_DIR.mkdir(exist_ok=True)
CHROMADB_DIR.mkdir(exist_ok=True)

os.environ["CREWAI_STORAGE_DIR"] = str(STORAGE_DIR)
os.environ["CHROMA_PERSIST_DIRECTORY"] = str(CHROMADB_DIR)
os.environ["IS_PERSISTENT"] = "TRUE"

print(f"✅ STORAGE_DIR: {STORAGE_DIR}")
print(f"✅ CHROMADB_DIR: {CHROMADB_DIR}")
print(f"✅ ENV CREWAI_STORAGE_DIR: {os.getenv('CREWAI_STORAGE_DIR')}")
print(f"✅ ENV CHROMA_PERSIST_DIRECTORY: {os.getenv('CHROMA_PERSIST_DIRECTORY')}")

# Listar arquivos na raiz
raiz_files = list(AULA11_ROOT.glob("chromadb*.lock"))
if raiz_files:
    print(f"\n❌ Arquivos na raiz: {len(raiz_files)}")
    for f in raiz_files[:3]:
        print(f"   - {f.name}")
else:
    print("\n✅ Nenhum arquivo lock na raiz")

# Listar arquivos no storage
storage_files = list(CHROMADB_DIR.glob("*"))
print(f"\n📁 Arquivos em {CHROMADB_DIR.relative_to(AULA11_ROOT)}: {len(storage_files)}")
