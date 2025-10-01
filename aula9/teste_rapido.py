#!/usr/bin/env python3
"""
🧪 TESTE RÁPIDO: Aula 9 - Verificação de Funcionamento
======================================================

Script para verificar se todos os componentes da Aula 9 estão funcionando
corretamente antes de começar os exercícios.

EXECUÇÃO:
uv run aula9/teste_rapido.py

OBJETIVO:
- Verificar configuração do ambiente
- Testar conexão com banco de dados  
- Validar criação de agentes
- Confirmar funcionamento das ferramentas
"""

import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv

# Configurações
load_dotenv()
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "db" / "curso.db"

print("🧪 TESTE RÁPIDO - Aula 9: Sistema Multi-Agente")
print("=" * 55)

# =============================================================================
# TESTES DE CONFIGURAÇÃO
# =============================================================================

def teste_configuracao_basica():
    """Testa configuração básica do ambiente"""
    
    print("\n🔧 TESTE 1: Configuração Básica")
    print("-" * 30)
    
    # Teste 1.1: Arquivo .env
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print("✅ OpenAI API Key configurada")
        print(f"   Key: {api_key[:8]}...{api_key[-4:] if len(api_key) > 12 else 'curta'}")
    else:
        print("❌ OpenAI API Key NÃO configurada")
        print("   💡 Configure no arquivo .env: OPENAI_API_KEY=sua_chave")
        return False
    
    # Teste 1.2: Banco de dados
    if DB_PATH.exists():
        print(f"✅ Banco de dados encontrado: {DB_PATH}")
        print(f"   Tamanho: {DB_PATH.stat().st_size / 1024:.1f} KB")
    else:
        print(f"❌ Banco de dados NÃO encontrado: {DB_PATH}")
        print("   💡 Verifique se o arquivo db/curso.db existe")
        return False
    
    return True


def teste_conexao_banco():
    """Testa conexão e estrutura do banco"""
    
    print("\n🗄️ TESTE 2: Conexão com Banco de Dados")
    print("-" * 30)
    
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        # Verificar tabelas principais
        tabelas_necessarias = [
            'ia_estabelecimento',
            'ia_queixa_principal',
            'ia_sintoma',
            'ia_historico_atendimento_sintoma'
        ]
        
        for tabela in tabelas_necessarias:
            cursor.execute(f"SELECT COUNT(*) FROM {tabela}")
            count = cursor.fetchone()[0]
            print(f"✅ Tabela {tabela}: {count:,} registros")
        
        # Teste de uma query típica
        cursor.execute("""
            SELECT COUNT(DISTINCT bairro) 
            FROM ia_estabelecimento 
            WHERE bairro IS NOT NULL
        """)
        bairros = cursor.fetchone()[0]
        print(f"✅ Query teste: {bairros} bairros únicos encontrados")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro na conexão com banco: {str(e)}")
        return False


def teste_importacoes():
    """Testa importação das bibliotecas necessárias"""
    
    print("\n📦 TESTE 3: Importações de Bibliotecas")
    print("-" * 30)
    
    try:
        from crewai import Agent, Task, Crew, Process
        print("✅ CrewAI importado com sucesso")
        
        from crewai.tools import BaseTool
        print("✅ CrewAI Tools importado com sucesso")
        
        from langchain_openai import ChatOpenAI
        print("✅ LangChain OpenAI importado com sucesso")
        
        # Teste de criação de LLM
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        print("✅ LLM ChatOpenAI criado com sucesso")
        
        return True
        
    except ImportError as e:
        print(f"❌ Erro de importação: {str(e)}")
        print("   💡 Execute: uv sync")
        return False
    except Exception as e:
        print(f"❌ Erro ao criar LLM: {str(e)}")
        print("   💡 Verifique a API Key da OpenAI")
        return False


def teste_ferramenta_simples():
    """Testa criação de ferramenta básica"""
    
    print("\n🛠️ TESTE 4: Criação de Ferramenta")
    print("-" * 30)
    
    try:
        from crewai.tools import BaseTool
        
        class FerramentaTeste(BaseTool):
            name: str = "ferramenta_teste"
            description: str = "Ferramenta de teste"
            
            def _run(self, input_text: str = "teste") -> str:
                return f"✅ Ferramenta funcionando! Input: {input_text}"
        
        # Testar ferramenta
        ferramenta = FerramentaTeste()
        resultado = ferramenta._run("teste_rapido")
        print(f"✅ Ferramenta criada e testada")
        print(f"   Resultado: {resultado}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar ferramenta: {str(e)}")
        return False


def teste_agente_simples():
    """Testa criação de agente básico"""
    
    print("\n🤖 TESTE 5: Criação de Agente")
    print("-" * 30)
    
    try:
        from crewai import Agent
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        
        agente = Agent(
            role="Agente de Teste",
            goal="Testar funcionalidade básica",
            backstory="Sou um agente criado para testes rápidos.",
            llm=llm,
            verbose=False
        )
        
        print("✅ Agente criado com sucesso")
        print(f"   Role: {agente.role}")
        print(f"   Goal: {agente.goal}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar agente: {str(e)}")
        return False


def teste_crew_basica():
    """Testa criação de crew básica"""
    
    print("\n👥 TESTE 6: Criação de Crew")
    print("-" * 30)
    
    try:
        from crewai import Agent, Task, Crew, Process
        from langchain_openai import ChatOpenAI
        
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        
        agente = Agent(
            role="Agente de Teste",
            goal="Executar tarefa de teste",
            backstory="Agente para teste de crew.",
            llm=llm,
            verbose=False
        )
        
        tarefa = Task(
            description="Diga 'Teste concluído com sucesso!'",
            agent=agente,
            expected_output="Mensagem de confirmação"
        )
        
        crew = Crew(
            agents=[agente],
            tasks=[tarefa],
            process=Process.sequential,
            verbose=False
        )
        
        print("✅ Crew criada com sucesso")
        print(f"   Agentes: {len(crew.agents)}")
        print(f"   Tarefas: {len(crew.tasks)}")
        print(f"   Processo: {crew.process}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao criar crew: {str(e)}")
        return False


# =============================================================================
# EXECUÇÃO DOS TESTES
# =============================================================================

def executar_todos_os_testes():
    """Executa todos os testes em sequência"""
    
    testes = [
        ("Configuração Básica", teste_configuracao_basica),
        ("Conexão com Banco", teste_conexao_banco),
        ("Importações", teste_importacoes),
        ("Ferramenta Simples", teste_ferramenta_simples),
        ("Agente Simples", teste_agente_simples),
        ("Crew Básica", teste_crew_basica)
    ]
    
    resultados = []
    
    for nome, funcao_teste in testes:
        try:
            resultado = funcao_teste()
            resultados.append((nome, resultado))
        except Exception as e:
            print(f"❌ Erro no teste {nome}: {str(e)}")
            resultados.append((nome, False))
    
    return resultados


def mostrar_resumo_final(resultados):
    """Mostra resumo final dos testes"""
    
    print("\n" + "=" * 55)
    print("📊 RESUMO FINAL DOS TESTES")
    print("=" * 55)
    
    sucessos = sum(1 for _, resultado in resultados if resultado)
    total = len(resultados)
    
    print(f"\n✅ Testes bem-sucedidos: {sucessos}/{total}")
    print(f"📈 Taxa de sucesso: {sucessos/total*100:.1f}%")
    
    print(f"\n📋 Detalhamento:")
    for nome, resultado in resultados:
        status = "✅ PASSOU" if resultado else "❌ FALHOU"
        print(f"   {status}: {nome}")
    
    if sucessos == total:
        print(f"\n🎉 TODOS OS TESTES PASSARAM!")
        print(f"🚀 Sistema pronto para usar!")
        print(f"\n⚡ Próximos passos:")
        print(f"   • Execute: uv run aula9/main.py")
        print(f"   • Ou tente: uv run aula9/exercicios/exercicio1_agente_personalizado.py")
    else:
        print(f"\n⚠️ ALGUNS TESTES FALHARAM")
        print(f"🔧 Resolva os problemas antes de continuar")
        print(f"\n💡 Dicas:")
        print(f"   • Verifique OpenAI API Key no .env")
        print(f"   • Execute: uv sync")
        print(f"   • Confirme que db/curso.db existe")


# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    """Função principal do teste rápido"""
    
    print("🔄 Iniciando testes...")
    
    try:
        resultados = executar_todos_os_testes()
        mostrar_resumo_final(resultados)
        
    except KeyboardInterrupt:
        print("\n⏹️ Testes interrompidos pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro fatal nos testes: {str(e)}")


if __name__ == "__main__":
    main()