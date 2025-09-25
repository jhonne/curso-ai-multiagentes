#!/usr/bin/env python3
"""
🎓 AULA 7: Agente CrewAI + PostgreSQL - VERSÃO INICIANTE
======================================================

OBJETIVO SIMPLES:
Mostrar como um agente CrewAI pode buscar dados em um banco PostgreSQL
usando uma ferramenta básica e fácil de entender.

EXECUÇÃO:
uv run aula7/exercicio_iniciante_postgres.py

PRÉ-REQUISITOS MÍNIMOS:
1. PostgreSQL rodando (localhost:5432)
2. Banco 'curso' criado
3. Credenciais: user='postgres', password='arpus'
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI
import psycopg2

# Carregar configurações
load_dotenv()

print("🎓 Versão INICIANTE - CrewAI + PostgreSQL")
print("=" * 45)

# =============================================================================
# PARTE 1: FERRAMENTA SIMPLES (SEM PYDANTIC!)
# =============================================================================

class BuscaSimples(BaseTool):
    """
    Ferramenta SIMPLES para buscar hospitais no PostgreSQL
    
    Sem configurações complexas - só o essencial!
    """
    
    name: str = "buscar_hospitais"
    description: str = ("Busca TODOS os hospitais no PostgreSQL. "
                        "Retorna lista completa para que você possa "
                        "analisar e filtrar conforme necessário")
    
    def _run(self, query: str = "") -> str:
        """
        Método simples que busca TODOS os hospitais no PostgreSQL
        O LLM fará a filtragem necessária baseada na tarefa solicitada.
        
        Args:
            query: parâmetro ignorado - sempre retorna todos os hospitais
        
        Returns:
            str: lista completa de hospitais formatada
        """
        
        try:
            print("🔍 Agente conectando no PostgreSQL para buscar "
                  "todos os hospitais...")
            
            # Conexão SIMPLES - credenciais fixas para começar
            conn = psycopg2.connect(
                host="localhost",
                port="5432",
                database="curso",
                user="postgres",
                password="arpus"
            )
            
            cursor = conn.cursor()
            
            # SQL SIMPLES - sempre busca TODOS os hospitais
            sql = ("SELECT nome, cidade, telefone FROM hospitais_exemplo "
                   "ORDER BY nome")
            
            print("📋 Agente buscando TODOS os hospitais para "
                  "análise do LLM...")
            cursor.execute(sql)
            resultados = cursor.fetchall()
            
            # Fechar conexão
            conn.close()
            print("✅ Agente obteve os dados!")
            
            # Verificar se encontrou dados
            if not resultados:
                return "❌ Nenhum hospital encontrado no banco."
            
            # Formatar resultado SIMPLES - TODOS os hospitais
            resposta = (f"🏥 TODOS OS HOSPITAIS NO BANCO "
                        f"({len(resultados)} no total):\n\n")
            
            for i, (nome, cidade, telefone) in enumerate(resultados, 1):
                resposta += f"{i}. **{nome}**\n"
                resposta += f"   📍 Cidade: {cidade}\n"
                resposta += f"   📞 Telefone: {telefone}\n\n"
            
            resposta += ("✅ Lista completa obtida! Agora analise e filtre "
                        "conforme a tarefa.")
            return resposta
            
        except Exception as erro:
            return f"❌ Erro ao buscar hospitais: {str(erro)}"


# =============================================================================
# PARTE 2: CRIAR AGENTE SIMPLES
# =============================================================================

def criar_agente_simples():
    """Cria um agente básico para iniciantes"""
    
    print("🤖 Criando agente simples...")
    
    # Modelo de linguagem
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1
    )
    
    # Nossa ferramenta simples
    ferramenta = BuscaSimples()
    
    # Agente SIMPLES
    agente = Agent(
        role="Assistente de Hospitais",
        goal="Ajudar a encontrar hospitais usando o banco de dados",
        backstory=("Eu sei como buscar hospitais no banco PostgreSQL "
                   "e apresentar as informações de forma clara."),
        verbose=False,
        llm=llm,
        tools=[ferramenta]  # Conecta a ferramenta ao agente
    )
    
    print("✅ Agente criado!")
    return agente


# =============================================================================
# PARTE 3: EXECUTAR EXEMPLO SIMPLES
# =============================================================================

def executar_exemplo_iniciante():
    """Executa exemplo básico para iniciantes"""
    
    print("\n📚 EXEMPLO PARA INICIANTES")
    print("-" * 30)
    
    # Testar se PostgreSQL está funcionando
    try:
        print("🔍 Testando PostgreSQL...")
        conn = psycopg2.connect(
            host="localhost",
            port="5432", 
            database="curso",
            user="postgres",
            password="arpus"
        )
        conn.close()
        print("✅ PostgreSQL funcionando!")
    except Exception as e:
        print(f"❌ PostgreSQL não conectou: {e}")
        print("\n💡 VERIFIQUE:")
        print("   • PostgreSQL está rodando?")
        print("   • Banco 'curso' existe?")
        return
    
    # Inserir dados de exemplo (SIMPLES)
    print("\n📥 Preparando dados de exemplo...")
    try:
        conn = psycopg2.connect(
            host="localhost",
            port="5432", 
            database="curso", 
            user="postgres",
            password="arpus"
        )
        cursor = conn.cursor()
        
        # Primeiro verificar se a tabela existe, se não, criar uma simples
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS hospitais_exemplo (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(255),
            cidade VARCHAR(255),
            telefone VARCHAR(20)
        )
        """)
        
        # Inserir dados de exemplo (MAIS HOSPITAIS para testar o LLM)
        cursor.execute("""
        INSERT INTO hospitais_exemplo (nome, cidade, telefone) 
        VALUES ('Hospital São Paulo', 'São Paulo', '(11) 1234-5678')
        ON CONFLICT DO NOTHING
        """)
        
        cursor.execute("""
        INSERT INTO hospitais_exemplo (nome, cidade, telefone) 
        VALUES ('Hospital das Clínicas', 'São Paulo', '(11) 9876-5432')
        ON CONFLICT DO NOTHING  
        """)
        
        cursor.execute("""
        INSERT INTO hospitais_exemplo (nome, cidade, telefone) 
        VALUES ('Hospital Albert Einstein', 'São Paulo', '(11) 5555-1234')
        ON CONFLICT DO NOTHING  
        """)
        
        cursor.execute("""
        INSERT INTO hospitais_exemplo (nome, cidade, telefone) 
        VALUES ('Hospital Louis Pasteur', 'Rio de Janeiro', '(21) 1111-2222')
        ON CONFLICT DO NOTHING  
        """)
        
        cursor.execute("""
        INSERT INTO hospitais_exemplo (nome, cidade, telefone) 
        VALUES ('Hospital Marie Curie', 'Belo Horizonte', '(31) 3333-4444')
        ON CONFLICT DO NOTHING  
        """)
        
        cursor.execute("""
        INSERT INTO hospitais_exemplo (nome, cidade, telefone) 
        VALUES ('Hospital Santa Casa', 'Porto Alegre', '(51) 5555-6666')
        ON CONFLICT DO NOTHING  
        """)
        
        cursor.execute("""
        INSERT INTO hospitais_exemplo (nome, cidade, telefone) 
        VALUES ('Hospital São José', 'Fortaleza', '(85) 7777-8888')
        ON CONFLICT DO NOTHING  
        """)
        
        conn.commit()
        conn.close()
        print("✅ Tabela e dados de exemplo criados!")
        
    except Exception as e:
        print(f"⚠️ Aviso: {e}")
    
    # Criar agente
    agente = criar_agente_simples()
    
    # Tarefa que CONFIA NO LLM para fazer a filtragem
    print("\n📋 Definindo tarefa que usa inteligência do LLM...")
    tarefa = Task(
        description="""
        Use a ferramenta buscar_hospitais para obter a lista completa de hospitais.
        Em seguida, analise os nomes e identifique APENAS aqueles que tenham 
        nomes de CIENTISTAS famosos (como Einstein, Pasteur, Curie, Darwin, 
        Newton, Tesla, etc).

        IMPORTANTE: A ferramenta retornará SOMENTE o hospital que contenha a palavra "Pasteur".
        """,
        agent=agente,
        expected_output=("Lista FILTRADA pelo LLM contendo apenas os hospitais "
                         "com nomes de cientistas, incluindo nome, cidade e telefone")
    )
    
    # Executar
    print("\n🚀 Executando agente...")
    crew = Crew(
        agents=[agente],
        tasks=[tarefa],
        process=Process.sequential,
        verbose=False
    )
    
    resultado = crew.kickoff()
    
    print("\n📋 RESULTADO:")
    print("=" * 30)
    print(resultado.raw)
    
    print("\n✅ EXEMPLO CONCLUÍDO!")
    print("🎓 Parabéns! O LLM analisou todos os hospitais e filtrou "
          "os com nomes de cientistas!")


# =============================================================================
# EXECUTAR
# =============================================================================

if __name__ == "__main__":
    try:
        executar_exemplo_iniciante()
    except KeyboardInterrupt:
        print("\n⏹️ Interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("\n🆘 AJUDA:")
        print("   • Verificar se PostgreSQL está rodando")
        print("   • Confirmar credenciais (postgres/arpus)")
        print("   • Verificar se banco 'curso' existe")