#!/bin/bash
# Script para organizar arquivos do ChromaDB automaticamente

cd "$(dirname "$0")"

# Criar pasta .chromadb se não existir
mkdir -p .chromadb

# Mover arquivos lock do ChromaDB para a pasta
if ls chromadb-*.lock 1> /dev/null 2>&1; then
    mv chromadb-*.lock .chromadb/ 2>/dev/null
    echo "✅ Arquivos ChromaDB organizados em .chromadb/"
else
    echo "✅ Nenhum arquivo ChromaDB para organizar"
fi
