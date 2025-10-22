#!/bin/bash
# Script para organizar arquivos ChromaDB em pasta dedicada

echo "🧹 Organizando arquivos ChromaDB da Aula 11..."

# Diretório da aula11
AULA11_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$AULA11_DIR"

# Criar diretório de storage se não existir
mkdir -p .crewai_storage

# Contar arquivos lock na raiz
LOCK_COUNT=$(ls -1 chromadb-*.lock 2>/dev/null | wc -l)

if [ "$LOCK_COUNT" -gt 0 ]; then
    echo "📦 Movendo $LOCK_COUNT arquivo(s) .lock para .crewai_storage/..."
    mv chromadb-*.lock .crewai_storage/ 2>/dev/null
    echo "✅ Arquivos movidos com sucesso!"
else
    echo "✅ Nenhum arquivo .lock encontrado na raiz (já está organizado!)"
fi

# Verificar se existe pasta .chromadb antiga
if [ -d ".chromadb" ]; then
    echo ""
    echo "⚠️  Encontrada pasta antiga .chromadb/"
    echo "   Deseja mover o conteúdo para .crewai_storage/? (s/N)"
    read -r resposta
    
    if [ "$resposta" = "s" ] || [ "$resposta" = "S" ]; then
        echo "📦 Movendo conteúdo de .chromadb/ para .crewai_storage/..."
        cp -r .chromadb/* .crewai_storage/ 2>/dev/null
        echo "✅ Conteúdo copiado!"
        echo "   Para remover a pasta antiga: rm -rf .chromadb/"
    fi
fi

echo ""
echo "📊 Estrutura atual:"
echo ""
tree -L 2 -a .crewai_storage/ 2>/dev/null || ls -lah .crewai_storage/

echo ""
echo "✨ Organização concluída!"
echo "   Storage path: $AULA11_DIR/.crewai_storage/"
