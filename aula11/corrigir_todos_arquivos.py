#!/usr/bin/env python3
"""
Script para adicionar configuração de storage em TODOS os arquivos Python da aula11

Este script adiciona automaticamente o import e configuração do setup_storage
em todos os arquivos Python que importam CrewAI.
"""

import re
from pathlib import Path


# Template de configuração baseado na profundidade do arquivo
TEMPLATES = {
    'raiz': '''import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# ✅ Configurar storage ANTES de importar CrewAI
load_dotenv()
from setup_storage import configurar_storage
config = configurar_storage(__file__)
''',
    'exemplos': '''import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# ✅ Configurar storage ANTES de importar CrewAI
load_dotenv()
sys.path.insert(0, str(Path(__file__).parent.parent))
from setup_storage import configurar_storage
config = configurar_storage(__file__)
''',
    'modulos': '''import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# ✅ Configurar storage ANTES de importar CrewAI
load_dotenv()
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from setup_storage import configurar_storage
config = configurar_storage(__file__)
''',
    'exercicios': '''import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# ✅ Configurar storage ANTES de importar CrewAI
load_dotenv()
sys.path.insert(0, str(Path(__file__).parent.parent))
from setup_storage import configurar_storage
config = configurar_storage(__file__)
'''
}


def detectar_tipo_arquivo(arquivo_path):
    """Detecta o tipo de arquivo baseado no path"""
    path = Path(arquivo_path)
    
    if 'modulos' in path.parts:
        return 'modulos'
    elif 'exemplos' in path.parts:
        return 'exemplos'
    elif 'exercicios' in path.parts:
        return 'exercicios'
    else:
        return 'raiz'


def arquivo_importa_crewai(conteudo):
    """Verifica se o arquivo importa CrewAI"""
    return bool(re.search(r'from crewai import', conteudo))


def arquivo_ja_configurado(conteudo):
    """Verifica se o arquivo já tem configuração de storage"""
    return 'from setup_storage import' in conteudo or 'configurar_storage' in conteudo


def processar_arquivo(arquivo_path):
    """Processa um arquivo Python adicionando configuração se necessário"""
    arquivo = Path(arquivo_path)
    
    # Ler conteúdo
    conteudo = arquivo.read_text(encoding='utf-8')
    
    # Verificar se precisa configurar
    if not arquivo_importa_crewai(conteudo):
        return False, "Não importa CrewAI"
    
    if arquivo_ja_configurado(conteudo):
        return False, "Já configurado"
    
    # Detectar tipo
    tipo = detectar_tipo_arquivo(arquivo)
    template = TEMPLATES[tipo]
    
    # Encontrar onde está o primeiro import do CrewAI
    linhas = conteudo.split('\n')
    indice_import_crewai = None
    
    for i, linha in enumerate(linhas):
        if re.search(r'from crewai import', linha):
            indice_import_crewai = i
            break
    
    if indice_import_crewai is None:
        return False, "CrewAI import não encontrado"
    
    # Remover imports antigos de configuração
    linhas_limpas = []
    skip_next = False
    
    for i, linha in enumerate(linhas):
        if skip_next:
            skip_next = False
            continue
            
        # Remover linhas de configuração antiga
        if any(x in linha for x in [
            'AULA11_ROOT = Path(__file__)',
            'STORAGE_DIR = AULA11_ROOT',
            'CHROMADB_DIR =',
            'os.environ["CREWAI_STORAGE_DIR"]',
            'os.environ["CHROMA_PERSIST_DIRECTORY"]',
            'os.chdir(str(AULA11_ROOT))',
            'os.chdir(str(STORAGE_DIR))',
        ]):
            continue
        
        linhas_limpas.append(linha)
    
    # Encontrar onde inserir nova configuração
    # Inserir antes do import do CrewAI
    linhas_finais = []
    inserido = False
    
    for i, linha in enumerate(linhas_limpas):
        if not inserido and re.search(r'from crewai import', linha):
            # Inserir configuração antes
            linhas_finais.append(template.rstrip())
            linhas_finais.append('')
            linhas_finais.append('# ✅ AGORA importar CrewAI')
            inserido = True
        
        linhas_finais.append(linha)
    
    # Salvar
    novo_conteudo = '\n'.join(linhas_finais)
    arquivo.write_text(novo_conteudo, encoding='utf-8')
    
    return True, f"Configurado como tipo '{tipo}'"


def main():
    """Processa todos os arquivos Python da aula11"""
    aula11_dir = Path(__file__).parent
    
    # Arquivos a processar
    arquivos_python = list(aula11_dir.rglob('*.py'))
    
    # Excluir alguns arquivos
    excluir = {'setup_storage.py', 'corrigir_todos_arquivos.py', '__init__.py'}
    arquivos_python = [
        f for f in arquivos_python 
        if f.name not in excluir and '__pycache__' not in str(f)
    ]
    
    print(f"\n🔍 Encontrados {len(arquivos_python)} arquivos Python\n")
    print("=" * 80)
    
    processados = 0
    ja_configurados = 0
    nao_precisa = 0
    
    for arquivo in sorted(arquivos_python):
        rel_path = arquivo.relative_to(aula11_dir)
        sucesso, mensagem = processar_arquivo(arquivo)
        
        if sucesso:
            print(f"✅ {rel_path}: {mensagem}")
            processados += 1
        elif "Já configurado" in mensagem:
            print(f"⏭️  {rel_path}: {mensagem}")
            ja_configurados += 1
        else:
            print(f"⏸️  {rel_path}: {mensagem}")
            nao_precisa += 1
    
    print("\n" + "=" * 80)
    print(f"\n📊 RESUMO:")
    print(f"  ✅ Configurados: {processados}")
    print(f"  ⏭️  Já configurados: {ja_configurados}")
    print(f"  ⏸️  Não precisam: {nao_precisa}")
    print(f"  📁 Total: {len(arquivos_python)}")
    
    print("\n✅ Processo concluído!")
    print("\n💡 Agora execute:")
    print("  uv run aula11/setup_storage.py  # Para limpar locks da raiz")


if __name__ == "__main__":
    main()
