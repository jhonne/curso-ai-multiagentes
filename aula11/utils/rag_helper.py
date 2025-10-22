"""
Funções auxiliares para RAG no CrewAI
"""

import os
from pathlib import Path
from crewai.utilities.paths import db_storage_path


def verificar_storage():
    """Verifica e exibe informações do storage do CrewAI"""
    
    storage_path = db_storage_path()
    
    print("\n=== 📁 INFORMAÇÕES DE STORAGE ===")
    print(f"Caminho base: {storage_path}")
    print(f"Existe: {storage_path.exists()}")
    
    if storage_path.exists():
        # Listar arquivos
        arquivos = list(storage_path.rglob("*"))
        print(f"\nTotal de arquivos: {len(arquivos)}")
        
        # Separar por tipo
        dbs = [f for f in arquivos if f.suffix == '.db']
        outros = [f for f in arquivos if f.suffix != '.db']
        
        if dbs:
            print(f"\n📊 Bancos SQLite ({len(dbs)}):")
            for db in dbs:
                size = db.stat().st_size / 1024  # KB
                print(f"  - {db.name} ({size:.2f} KB)")
        
        if outros:
            print(f"\n📦 Outros arquivos ({len(outros)}):")
            for arquivo in outros[:5]:  # Mostrar primeiros 5
                print(f"  - {arquivo.name}")
            if len(outros) > 5:
                print(f"  ... e mais {len(outros) - 5} arquivos")
    else:
        print("\n⚠️ Storage ainda não foi criado.")
        print("Execute um exemplo com memory=True para criar.")
    
    print("=" * 40)


def limpar_storage():
    """Limpa o storage do CrewAI (cuidado!)"""
    
    storage_path = db_storage_path()
    
    if not storage_path.exists():
        print("✅ Storage já está limpo (não existe)")
        return
    
    # Pedir confirmação
    print(f"⚠️  ATENÇÃO: Isso vai deletar TODO o storage em:")
    print(f"   {storage_path}")
    resposta = input("Confirma? (sim/não): ")
    
    if resposta.lower() != 'sim':
        print("❌ Operação cancelada")
        return
    
    # Deletar arquivos
    import shutil
    try:
        shutil.rmtree(storage_path)
        print("✅ Storage limpo com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao limpar: {e}")


def tamanho_storage():
    """Retorna tamanho total do storage em MB"""
    
    storage_path = db_storage_path()
    
    if not storage_path.exists():
        return 0
    
    total = sum(
        f.stat().st_size 
        for f in storage_path.rglob("*") 
        if f.is_file()
    )
    
    return total / (1024 * 1024)  # MB


def verificar_knowledge_source(file_path):
    """Verifica se arquivo existe e pode ser usado como knowledge source"""
    
    path = Path(file_path)
    
    print(f"\n=== 📚 VERIFICAÇÃO DE KNOWLEDGE SOURCE ===")
    print(f"Arquivo: {file_path}")
    print(f"Existe: {path.exists()}")
    
    if not path.exists():
        print("❌ ERRO: Arquivo não encontrado!")
        return False
    
    # Verificar extensão
    extensoes_suportadas = {
        '.txt': 'TextFileKnowledgeSource',
        '.pdf': 'PDFKnowledgeSource',
        '.csv': 'CSVKnowledgeSource',
        '.json': 'JSONKnowledgeSource',
        '.xlsx': 'ExcelKnowledgeSource',
    }
    
    extensao = path.suffix.lower()
    if extensao in extensoes_suportadas:
        print(f"✅ Extensão suportada: {extensao}")
        print(f"📦 Usar: {extensoes_suportadas[extensao]}")
    else:
        print(f"⚠️  Extensão não reconhecida: {extensao}")
        print("Extensões suportadas:", list(extensoes_suportadas.keys()))
    
    # Verificar tamanho
    tamanho_kb = path.stat().st_size / 1024
    print(f"📏 Tamanho: {tamanho_kb:.2f} KB")
    
    if tamanho_kb > 10000:  # 10 MB
        print("⚠️  Arquivo muito grande (>10MB)")
        print("Considere dividir em arquivos menores")
    
    # Tentar ler primeiras linhas (se for texto)
    if extensao in ['.txt', '.csv']:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                linhas = f.readlines()[:5]
            print(f"\n📄 Primeiras linhas:")
            for i, linha in enumerate(linhas, 1):
                print(f"  {i}. {linha.strip()[:60]}...")
        except Exception as e:
            print(f"⚠️  Não foi possível ler: {e}")
    
    print("=" * 40)
    return True


def criar_knowledge_source_automatico(file_path):
    """Cria o knowledge source apropriado automaticamente"""
    
    from pathlib import Path
    
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    extensao = path.suffix.lower()
    
    # Importar classe apropriada
    if extensao == '.txt':
        from crewai.knowledge.source.text_file_knowledge_source import (
            TextFileKnowledgeSource
        )
        return TextFileKnowledgeSource(file_paths=[str(path)])
    
    elif extensao == '.pdf':
        from crewai.knowledge.source.pdf_knowledge_source import (
            PDFKnowledgeSource
        )
        return PDFKnowledgeSource(file_paths=[str(path)])
    
    elif extensao == '.csv':
        from crewai.knowledge.source.csv_knowledge_source import (
            CSVKnowledgeSource
        )
        return CSVKnowledgeSource(file_paths=[str(path)])
    
    elif extensao == '.json':
        from crewai.knowledge.source.json_knowledge_source import (
            JSONKnowledgeSource
        )
        return JSONKnowledgeSource(file_paths=[str(path)])
    
    else:
        raise ValueError(
            f"Extensão não suportada: {extensao}. "
            f"Use: .txt, .pdf, .csv, .json"
        )


def listar_knowledge_sources(diretorio="conhecimento_medico"):
    """Lista todos os arquivos válidos para knowledge source em um diretório"""
    
    from pathlib import Path
    
    dir_path = Path(diretorio)
    
    if not dir_path.exists():
        print(f"❌ Diretório não encontrado: {diretorio}")
        return []
    
    extensoes = ['.txt', '.pdf', '.csv', '.json', '.xlsx']
    arquivos = []
    
    for ext in extensoes:
        arquivos.extend(dir_path.rglob(f"*{ext}"))
    
    print(f"\n=== 📚 KNOWLEDGE SOURCES EM {diretorio} ===")
    print(f"Total: {len(arquivos)} arquivos")
    
    for arquivo in sorted(arquivos):
        tamanho_kb = arquivo.stat().st_size / 1024
        print(f"  📄 {arquivo.relative_to(dir_path)} ({tamanho_kb:.1f} KB)")
    
    print("=" * 40)
    
    return arquivos


def exemplo_uso():
    """Exemplo de uso das funções auxiliares"""
    
    print("\n=== 🧪 EXEMPLO DE USO DAS FUNÇÕES RAG ===\n")
    
    # 1. Verificar storage
    print("1️⃣ Verificando storage...")
    verificar_storage()
    
    # 2. Tamanho do storage
    tamanho = tamanho_storage()
    print(f"\n2️⃣ Tamanho do storage: {tamanho:.2f} MB")
    
    # 3. Listar knowledge sources disponíveis
    print("\n3️⃣ Listando knowledge sources disponíveis...")
    arquivos = listar_knowledge_sources("conhecimento_medico")
    
    # 4. Verificar um arquivo específico
    if arquivos:
        print("\n4️⃣ Verificando primeiro arquivo encontrado...")
        verificar_knowledge_source(str(arquivos[0]))
    
    print("\n✅ Exemplo concluído!")


if __name__ == "__main__":
    exemplo_uso()
