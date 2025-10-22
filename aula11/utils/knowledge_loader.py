"""
Carregadores de conhecimento para diferentes formatos
"""

from pathlib import Path
from typing import List, Union


def carregar_texto(file_path: str) -> str:
    """Carrega conteúdo de arquivo de texto"""
    
    with open(file_path, 'r', encoding='utf-8') as f:
        conteudo = f.read()
    
    return conteudo


def carregar_multiplos_textos(
    file_paths: List[str],
    separador: str = "\n\n---\n\n"
) -> str:
    """Carrega múltiplos arquivos de texto em uma string única"""
    
    conteudos = []
    
    for file_path in file_paths:
        try:
            conteudo = carregar_texto(file_path)
            conteudos.append(f"=== {Path(file_path).name} ===\n{conteudo}")
        except Exception as e:
            print(f"Erro ao carregar {file_path}: {e}")
    
    return separador.join(conteudos)


def criar_string_knowledge(texto: str):
    """Cria StringKnowledgeSource a partir de texto"""
    
    from crewai.knowledge.source.string_knowledge_source import (
        StringKnowledgeSource
    )
    
    return StringKnowledgeSource(content=texto)


def criar_text_file_knowledge(file_paths: Union[str, List[str]]):
    """Cria TextFileKnowledgeSource"""
    
    from crewai.knowledge.source.text_file_knowledge_source import (
        TextFileKnowledgeSource
    )
    
    if isinstance(file_paths, str):
        file_paths = [file_paths]
    
    return TextFileKnowledgeSource(file_paths=file_paths)


def criar_pdf_knowledge(file_paths: Union[str, List[str]]):
    """Cria PDFKnowledgeSource"""
    
    from crewai.knowledge.source.pdf_knowledge_source import (
        PDFKnowledgeSource
    )
    
    if isinstance(file_paths, str):
        file_paths = [file_paths]
    
    return PDFKnowledgeSource(file_paths=file_paths)


def criar_csv_knowledge(file_paths: Union[str, List[str]]):
    """Cria CSVKnowledgeSource"""
    
    from crewai.knowledge.source.csv_knowledge_source import (
        CSVKnowledgeSource
    )
    
    if isinstance(file_paths, str):
        file_paths = [file_paths]
    
    return CSVKnowledgeSource(file_paths=file_paths)


def criar_json_knowledge(file_paths: Union[str, List[str]]):
    """Cria JSONKnowledgeSource"""
    
    from crewai.knowledge.source.json_knowledge_source import (
        JSONKnowledgeSource
    )
    
    if isinstance(file_paths, str):
        file_paths = [file_paths]
    
    return JSONKnowledgeSource(file_paths=file_paths)


def criar_knowledge_automatico(file_path: str):
    """Cria knowledge source apropriado baseado na extensão do arquivo"""
    
    extensao = Path(file_path).suffix.lower()
    
    mapeamento = {
        '.txt': criar_text_file_knowledge,
        '.pdf': criar_pdf_knowledge,
        '.csv': criar_csv_knowledge,
        '.json': criar_json_knowledge,
    }
    
    funcao = mapeamento.get(extensao)
    
    if funcao is None:
        raise ValueError(
            f"Extensão não suportada: {extensao}. "
            f"Suportadas: {list(mapeamento.keys())}"
        )
    
    return funcao(file_path)


def carregar_diretorio_completo(
    diretorio: str,
    extensoes: List[str] = None
) -> List:
    """Carrega todos os arquivos de um diretório como knowledge sources"""
    
    if extensoes is None:
        extensoes = ['.txt', '.pdf', '.csv', '.json']
    
    dir_path = Path(diretorio)
    
    if not dir_path.exists():
        raise FileNotFoundError(f"Diretório não encontrado: {diretorio}")
    
    sources = []
    
    for ext in extensoes:
        arquivos = list(dir_path.rglob(f"*{ext}"))
        
        for arquivo in arquivos:
            try:
                source = criar_knowledge_automatico(str(arquivo))
                sources.append(source)
                print(f"✅ Carregado: {arquivo.name}")
            except Exception as e:
                print(f"❌ Erro em {arquivo.name}: {e}")
    
    return sources


def criar_protocolo_exemplo():
    """Cria um protocolo de exemplo em texto"""
    
    protocolo = """
    PROTOCOLO DE TRIAGEM - SISTEMA MANCHESTER
    
    CLASSIFICAÇÃO POR CORES:
    
    🔴 VERMELHO (Emergência - Atendimento Imediato)
    - Parada cardiorrespiratória
    - Dor torácica com sinais de IAM
    - Trauma grave
    - Choque
    
    🟠 LARANJA (Muito Urgente - 10 minutos)
    - Dor torácica sem sinais de IAM
    - Dificuldade respiratória moderada
    - Sangramento importante
    - Alteração aguda do nível de consciência
    
    🟡 AMARELO (Urgente - 60 minutos)
    - Dor moderada
    - Febre alta
    - Vômitos persistentes
    - Trauma leve a moderado
    
    🟢 VERDE (Pouco Urgente - 120 minutos)
    - Problemas crônicos
    - Sintomas leves
    - Resfriados
    
    🔵 AZUL (Não Urgente - 240 minutos)
    - Consultas de rotina
    - Renovação de receitas
    - Atestados
    """
    
    return protocolo.strip()


def exemplo_uso():
    """Exemplo de uso dos carregadores"""
    
    print("\n=== 📚 EXEMPLO DE USO DOS CARREGADORES ===\n")
    
    # 1. Criar protocolo de exemplo
    print("1️⃣ Criando protocolo de exemplo...")
    protocolo = criar_protocolo_exemplo()
    print(f"Protocolo criado ({len(protocolo)} caracteres)")
    
    # 2. Criar StringKnowledgeSource
    print("\n2️⃣ Criando StringKnowledgeSource...")
    source = criar_string_knowledge(protocolo)
    print(f"Source criado: {type(source).__name__}")
    
    # 3. Verificar arquivo se existe
    arquivo_teste = "conhecimento_medico/protocolos/urgencia_emergencia.txt"
    if Path(arquivo_teste).exists():
        print(f"\n3️⃣ Carregando arquivo: {arquivo_teste}")
        source_arquivo = criar_text_file_knowledge(arquivo_teste)
        print(f"Source criado: {type(source_arquivo).__name__}")
    else:
        print(f"\n3️⃣ Arquivo não encontrado: {arquivo_teste}")
    
    # 4. Listar arquivos em diretório
    dir_conhecimento = "conhecimento_medico"
    if Path(dir_conhecimento).exists():
        print(f"\n4️⃣ Carregando diretório: {dir_conhecimento}")
        sources = carregar_diretorio_completo(dir_conhecimento)
        print(f"Total de sources carregados: {len(sources)}")
    else:
        print(f"\n4️⃣ Diretório não encontrado: {dir_conhecimento}")
    
    print("\n✅ Exemplo concluído!")


if __name__ == "__main__":
    exemplo_uso()
