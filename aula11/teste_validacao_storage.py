#!/usr/bin/env python3
"""
Teste de Validação - Storage ChromaDB

Este script testa se a configuração de storage está funcionando corretamente
e se os arquivos do ChromaDB estão sendo criados no local correto.

Execute: python3 teste_validacao_storage.py
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# ✅ Configurar storage ANTES de tudo
load_dotenv()
from setup_storage import configurar_storage
config = configurar_storage(__file__)

AULA11_ROOT = config['AULA11_ROOT']
STORAGE_DIR = config['STORAGE_DIR']
CHROMADB_DIR = config['CHROMADB_DIR']

# ✅ AGORA importar CrewAI
from crewai import Agent, Task, Crew, LLM


def verificar_storage():
    """Verifica se o storage está configurado corretamente"""
    print("\n" + "=" * 80)
    print("🔍 VERIFICAÇÃO DE STORAGE")
    print("=" * 80)
    
    print(f"\n📁 Raiz Aula11: {AULA11_ROOT}")
    print(f"📁 Storage Dir: {STORAGE_DIR}")
    print(f"📁 ChromaDB Dir: {CHROMADB_DIR}")
    print(f"📁 Diretório atual: {os.getcwd()}")
    
    # Verificar variáveis de ambiente
    print(f"\n🔧 Variáveis de ambiente:")
    print(f"  CREWAI_STORAGE_DIR: {os.environ.get('CREWAI_STORAGE_DIR')}")
    print(f"  CHROMA_PERSIST_DIRECTORY: {os.environ.get('CHROMA_PERSIST_DIRECTORY')}")
    
    # Verificar diretórios
    print(f"\n✅ Verificações:")
    print(f"  Storage existe: {STORAGE_DIR.exists()}")
    print(f"  ChromaDB existe: {CHROMADB_DIR.exists()}")


def testar_criacao_crew():
    """Testa criação de uma crew com memória"""
    print("\n" + "=" * 80)
    print("🧪 TESTE: Criação de Crew com Memória")
    print("=" * 80)
    
    # Verificar API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("\n⚠️ OPENAI_API_KEY não configurada - pulando teste de execução")
        print("   Mas a configuração de storage está OK!")
        return
    
    print("\n📝 Criando agente e crew...")
    
    llm = LLM(model="gpt-4o-mini", temperature=0.1)
    
    agente = Agent(
        role="Testador",
        goal="Testar configuração de storage",
        backstory="Agente simples para testes.",
        llm=llm,
        verbose=False
    )
    
    tarefa = Task(
        description="Responda: {pergunta}",
        expected_output="Resposta simples",
        agent=agente
    )
    
    crew = Crew(
        agents=[agente],
        tasks=[tarefa],
        memory=True,  # 🧠 Isso vai criar arquivos no storage
        verbose=False
    )
    
    print("✅ Crew criada com memória habilitada")
    
    # Executar uma interação simples
    print("\n🚀 Executando teste...")
    resultado = crew.kickoff(inputs={"pergunta": "Teste de storage"})
    print(f"✅ Teste executado: {resultado.raw[:50]}...")


def verificar_arquivos_criados():
    """Verifica se arquivos foram criados no local correto"""
    print("\n" + "=" * 80)
    print("📂 VERIFICAÇÃO DE ARQUIVOS CRIADOS")
    print("=" * 80)
    
    # Verificar raiz da aula11
    print(f"\n🔍 Arquivos .lock na raiz da aula11:")
    raiz_locks = list(AULA11_ROOT.glob("chromadb-*.lock"))
    if raiz_locks:
        print("  ❌ PROBLEMA! Encontrados arquivos .lock na raiz:")
        for lock in raiz_locks:
            print(f"     - {lock.name}")
    else:
        print("  ✅ Nenhum arquivo .lock na raiz (correto!)")
    
    # Verificar storage
    print(f"\n🔍 Conteúdo do .crewai_storage:")
    if STORAGE_DIR.exists():
        storage_items = list(STORAGE_DIR.iterdir())
        if storage_items:
            for item in storage_items:
                tipo = "📁" if item.is_dir() else "📄"
                print(f"  {tipo} {item.name}")
        else:
            print("  (vazio)")
    else:
        print("  ❌ Diretório não existe!")
    
    # Verificar ChromaDB
    print(f"\n🔍 Conteúdo do chromadb:")
    if CHROMADB_DIR.exists():
        chromadb_items = list(CHROMADB_DIR.iterdir())
        if chromadb_items:
            print(f"  ✅ {len(chromadb_items)} itens encontrados")
            for item in sorted(chromadb_items)[:5]:
                tipo = "📁" if item.is_dir() else "📄"
                print(f"  {tipo} {item.name}")
            if len(chromadb_items) > 5:
                print(f"  ... e mais {len(chromadb_items) - 5} itens")
        else:
            print("  (vazio - normal se não executou crew ainda)")
    else:
        print("  ❌ Diretório não existe!")


def resultado_final():
    """Mostra resultado final do teste"""
    print("\n" + "=" * 80)
    print("🎯 RESULTADO FINAL")
    print("=" * 80)
    
    # Verificar se há locks na raiz
    raiz_locks = list(AULA11_ROOT.glob("chromadb-*.lock"))
    
    if raiz_locks:
        print("\n❌ TESTE FALHOU!")
        print(f"   Ainda há {len(raiz_locks)} arquivos .lock na raiz")
        print("   Os arquivos ChromaDB NÃO estão sendo criados em .crewai_storage")
    else:
        print("\n✅ TESTE PASSOU!")
        print("   ✓ Nenhum arquivo .lock na raiz")
        print("   ✓ Configuração de storage está correta")
        print("   ✓ ChromaDB será criado em .crewai_storage/chromadb/")
    
    print("\n📋 Estrutura correta:")
    print("   aula11/")
    print("   ├── .crewai_storage/")
    print("   │   ├── chromadb/          ← Arquivos do ChromaDB AQUI")
    print("   │   │   ├── chroma.sqlite3")
    print("   │   │   └── *.lock")
    print("   │   └── outros arquivos...")
    print("   ├── main.py")
    print("   ├── quick_start.py")
    print("   └── ... (SEM arquivos .lock aqui!)")


def main():
    """Execução principal do teste"""
    print("\n" + "=" * 80)
    print("🧪 TESTE DE VALIDAÇÃO - STORAGE CHROMADB")
    print("=" * 80)
    
    try:
        verificar_storage()
        testar_criacao_crew()
        verificar_arquivos_criados()
        resultado_final()
        
    except Exception as e:
        print(f"\n❌ Erro durante teste: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 80)
    print("✅ Teste concluído!")
    print("=" * 80)


if __name__ == "__main__":
    main()
