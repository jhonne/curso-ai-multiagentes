"""
Utils para RAG no CrewAI - Aula 11
"""

from .rag_helper import (
    verificar_storage,
    limpar_storage,
    tamanho_storage,
    verificar_knowledge_source,
    criar_knowledge_source_automatico,
    listar_knowledge_sources
)

from .knowledge_loader import (
    carregar_texto,
    carregar_multiplos_textos,
    criar_string_knowledge,
    criar_text_file_knowledge,
    criar_pdf_knowledge,
    criar_csv_knowledge,
    criar_json_knowledge,
    criar_knowledge_automatico,
    carregar_diretorio_completo,
    criar_protocolo_exemplo
)

__all__ = [
    # rag_helper
    'verificar_storage',
    'limpar_storage',
    'tamanho_storage',
    'verificar_knowledge_source',
    'criar_knowledge_source_automatico',
    'listar_knowledge_sources',
    # knowledge_loader
    'carregar_texto',
    'carregar_multiplos_textos',
    'criar_string_knowledge',
    'criar_text_file_knowledge',
    'criar_pdf_knowledge',
    'criar_csv_knowledge',
    'criar_json_knowledge',
    'criar_knowledge_automatico',
    'carregar_diretorio_completo',
    'criar_protocolo_exemplo'
]
