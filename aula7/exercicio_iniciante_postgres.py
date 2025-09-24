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
    description: str = "Busca hospitais no PostgreSQL. Use sempre que precisar listar hospitais."
    
    def _run(self, query: str = "") -> str:
        """
        Método simples que busca hospitais no PostgreSQL
        
        Args:
            query: texto de entrada (pode ser qualquer coisa)
        
        Returns:
            str: lista de hospitais formatada
        """
        
        try:
            print("🔍 Agente está conectando no PostgreSQL...")
            
            # Conexão SIMPLES - credenciais fixas para começar
            conn = psycopg2.connect(
                host="localhost",
                port="5432", 
                database="curso",
                user="postgres",
                password="arpus"
            )
            
            cursor = conn.cursor()
            
            # SQL SIMPLES - usando nossa tabela de exemplo
            sql = "SELECT nome, cidade, telefone FROM hospitais_exemplo LIMIT 5"
            
            print("📋 Agente executando consulta SQL...")
            cursor.execute(sql)
            resultados = cursor.fetchall()
            
            # Fechar conexão
            conn.close()
            print("✅ Agente obteve os dados!")
            
            # Verificar se encontrou dados
            if not resultados:
                return "❌ Nenhum hospital encontrado no banco."
            
            # Formatar resultado SIMPLES
            resposta = f"🏥 HOSPITAIS ENCONTRADOS ({len(resultados)} no total):\n\n"
            
            for i, (nome, cidade, telefone) in enumerate(resultados, 1):
                resposta += f"{i}. **{nome}**\n"
                resposta += f"   📍 Cidade: {cidade}\n"
                resposta += f"   📞 Telefone: {telefone}\n\n"
            
            resposta += "✅ Consulta realizada com sucesso!"
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
        backstory="Eu sei como buscar hospitais no banco PostgreSQL e apresentar as informações de forma clara.",
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
        
        # Inserir dados de exemplo na tabela simples
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
        
        conn.commit()
        conn.close()
        print("✅ Tabela e dados de exemplo criados!")
        
    except Exception as e:
        print(f"⚠️ Aviso: {e}")
    
    # Criar agente
    agente = criar_agente_simples()
    
    # Tarefa SIMPLES e CLARA
    print("\n📋 Definindo tarefa simples...")
    tarefa = Task(
        description="""
        Por favor, use a ferramenta buscar_hospitais para encontrar todos os hospitais 
        disponíveis no banco de dados e apresente a lista de forma organizada.
        """,
        agent=agente,
        expected_output="Lista clara de hospitais com nome, cidade e telefone"
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
    
    print(f"\n✅ EXEMPLO CONCLUÍDO!")
    print("🎓 Parabéns! Você criou um agente que busca dados no PostgreSQL!")


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