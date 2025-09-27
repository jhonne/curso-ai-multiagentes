#!/usr/bin/env python3
"""
🎯 FERRAMENTA SQL OTIMIZADA - DEIXA O LLM FAZER O QUE FAZ MELHOR
===============================================================

VERSÃO OTIMIZADA da ConsultaSaudeTool que elimina redundâncias
e deixa o LLM fazer o trabalho de interpretação e formatação.

PRINCÍPIOS:
- Ferramenta faz APENAS o que o LLM não pode: executar SQL
- LLM faz o que faz melhor: interpretar, gerar queries, formatar
- Resultado: Mais flexível, menos código, melhor performance
"""

import sqlite3
from pathlib import Path
from crewai.tools import BaseTool

PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "db" / "curso.db"


# =============================================================================
# FERRAMENTA OTIMIZADA - SÓ O ESSENCIAL
# =============================================================================

class SQLExecutorTool(BaseTool):
    """
    Ferramenta MINIMALISTA para executar SQL no SQLite
    
    O LLM faz:
    ✅ Interpretar a pergunta do usuário
    ✅ Gerar a query SQL apropriada
    ✅ Formatar os resultados de forma inteligente
    ✅ Adicionar contexto e insights
    
    A ferramenta faz APENAS:
    🔧 Conectar ao banco
    🔧 Executar a query
    🔧 Retornar dados brutos
    """
    
    name: str = "executar_sql_saude"
    description: str = (
        "Executa consultas SQL no banco SQLite com dados de saúde. "
        "Tabelas disponíveis: ia_estabelecimento, ia_queixa_principal, "
        "ia_sintoma, ia_historico_atendimento_sintoma. "
        "Retorna dados brutos para análise."
    )
    
    def _run(self, sql_query: str) -> str:
        """
        Executa query SQL e retorna resultados brutos
        
        Args:
            sql_query: Query SQL a ser executada
            
        Returns:
            str: Resultados em formato que o LLM pode processar
        """
        
        try:
            if not DB_PATH.exists():
                return f"ERRO: Banco não encontrado em {DB_PATH}"
            
            # Conexão simples
            conn = sqlite3.connect(str(DB_PATH))
            conn.row_factory = sqlite3.Row  # Permite acesso por nome
            cursor = conn.cursor()
            
            # Executar query fornecida pelo LLM
            cursor.execute(sql_query)
            resultados = cursor.fetchall()
            conn.close()
            
            # Retornar dados estruturados para o LLM processar
            if not resultados:
                return "Nenhum resultado encontrado para a consulta."
            
            # Converter para formato que o LLM pode processar facilmente
            dados = []
            for row in resultados:
                dados.append(dict(row))
            
            return f"DADOS_SQL: {dados}"
            
        except Exception as e:
            return f"ERRO_SQL: {str(e)}"


class SchemaInfoTool(BaseTool):
    """
    Ferramenta para fornecer informações do schema ao LLM
    Permite que o LLM gere queries SQL corretas
    """
    
    name: str = "info_schema_saude"
    description: str = (
        "Retorna informações sobre o schema do banco de dados de saúde "
        "(tabelas, colunas, relacionamentos) para gerar queries SQL corretas."
    )
    
    def _run(self, tabela: str = "") -> str:
        """Retorna informações do schema"""
        
        try:
            conn = sqlite3.connect(str(DB_PATH))
            cursor = conn.cursor()
            
            if tabela:
                # Info de tabela específica
                cursor.execute(f"PRAGMA table_info({tabela})")
                colunas = cursor.fetchall()
                
                info = f"TABELA: {tabela}\nCOLUNAS:\n"
                for col in colunas:
                    info += f"  - {col[1]} ({col[2]})\n"
                
            else:
                # Info geral do schema
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tabelas = [row[0] for row in cursor.fetchall()]
                
                info = "SCHEMA DO BANCO DE SAÚDE:\n\n"
                
                for tab in tabelas:
                    if tab.startswith('ia_'):  # Apenas tabelas do projeto
                        cursor.execute(f"PRAGMA table_info({tab})")
                        colunas = cursor.fetchall()
                        
                        info += f"📋 TABELA: {tab}\n"
                        for col in colunas:
                            info += f"   - {col[1]} ({col[2]})\n"
                        info += "\n"
                
                # Relacionamentos conhecidos
                info += """
🔗 RELACIONAMENTOS PRINCIPAIS:
- ia_historico_atendimento_sintoma.estabelecimento_cnes → ia_estabelecimento.cnes
- ia_historico_atendimento_sintoma.queixa_principal_id → ia_queixa_principal.id
- ia_historico_atendimento_sintoma.sintoma_id → ia_sintoma.id
                """
            
            conn.close()
            return info
            
        except Exception as e:
            return f"ERRO_SCHEMA: {str(e)}"


# =============================================================================
# EXEMPLO DE AGENTE OTIMIZADO
# =============================================================================

from crewai import Agent
from langchain_openai import ChatOpenAI

def criar_agente_sql_otimizado():
    """
    Agente que usa as ferramentas otimizadas
    
    VANTAGENS desta abordagem:
    - LLM interpreta perguntas naturalmente
    - LLM gera SQL dinâmico baseado na pergunta
    - LLM formata resultados com contexto
    - Muito mais flexível que queries fixas
    """
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    
    ferramentas = [
        SQLExecutorTool(),
        SchemaInfoTool()
    ]
    
    agente = Agent(
        role="Analista SQL de Dados de Saúde",
        goal=(
            "Responder perguntas sobre dados de saúde gerando e executando "
            "queries SQL apropriadas, e interpretando os resultados de forma útil"
        ),
        backstory="""
        Sou especialista em análise de dados de saúde com profundo conhecimento 
        em SQL e bases de dados médicas. Consigo interpretar perguntas em linguagem 
        natural, gerar queries SQL precisas, e explicar os resultados de forma 
        clara e contextualizada.
        
        WORKFLOW:
        1. Se não conheço o schema, uso info_schema_saude
        2. Gero SQL query baseada na pergunta do usuário  
        3. Executo com executar_sql_saude
        4. Interpreto e formato os resultados de forma útil
        """,
        verbose=True,
        llm=llm,
        tools=ferramentas
    )
    
    return agente


# =============================================================================
# DEMONSTRAÇÃO DA DIFERENÇA
# =============================================================================

if __name__ == "__main__":
    print("🎯 DEMONSTRAÇÃO: FERRAMENTA OTIMIZADA vs ORIGINAL")
    print("=" * 60)
    
    agente = criar_agente_sql_otimizado()
    
    # O agente agora pode:
    # - Gerar queries SQL dinâmicas
    # - Responder perguntas mais complexas
    # - Formatar resultados com mais inteligência
    # - Adaptar-se a novas perguntas sem modificar código
    
    print("✅ Agente otimizado criado!")
    print("\n💡 PRINCIPAIS MELHORIAS:")
    print("- LLM gera SQL dinamicamente (mais flexível)")
    print("- LLM formata resultados com contexto (mais inteligente)")  
    print("- Código 80% menor (mais maintível)")
    print("- Responde perguntas que a versão original não consegue")