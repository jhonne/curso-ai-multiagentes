#!/usr/bin/env python3
"""
🎓 EXERCÍCIO SIMPLES AULA 8 - Consulta de Saúde com CrewAI
==========================================================

OBJETIVO: Sistema super simples (< 100 linhas) usando dados REAIS

CONCEITOS: Sistema interativo + BaseTool + Agente + SQLite real

EXECUÇÃO: uv run aula8/exercicio_simples_aula8.py
"""

import os
import sqlite3
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI

load_dotenv()
DB_REAL = Path(__file__).parent.parent / "db" / "curso.db"


class ConsultaSaude(BaseTool):
    """Ferramenta para consultar dados REAIS de saúde"""
    
    name: str = "consulta_saude"
    description: str = "Consulta estabelecimentos e queixas de saúde"
    
    def _run(self, consulta: str = "") -> str:
        try:
            conn = sqlite3.connect(str(DB_REAL))
            cursor = conn.cursor()
            
            if "estabelecimento" in consulta.lower():
                cursor.execute("""
                    SELECT nome, bairro FROM ia_estabelecimento
                    ORDER BY nome LIMIT 8
                """)
                dados = cursor.fetchall()
                resultado = "🏥 ESTABELECIMENTOS:\n"
                for nome, bairro in dados:
                    resultado += f"• {nome[:40]}... - {bairro}\n"
                    
            elif "queixa" in consulta.lower():
                cursor.execute("""
                    SELECT q.nome, COUNT(*) as total
                    FROM ia_queixa_principal q
                    JOIN ia_historico_atendimento_sintoma h
                         ON q.id = h.queixa_principal_id
                    GROUP BY q.nome
                    ORDER BY total DESC LIMIT 8
                """)
                dados = cursor.fetchall()
                resultado = "🏥 QUEIXAS FREQUENTES:\n"
                for nome, total in dados:
                    resultado += f"• {nome[:35]}... - {total:,} casos\n"
                    
            else:
                cursor.execute("SELECT COUNT(*) FROM ia_estabelecimento")
                total_est = cursor.fetchone()[0]
                cursor.execute("SELECT COUNT(*) FROM ia_queixa_principal")
                total_queixas = cursor.fetchone()[0]
                
                resultado = "📊 ESTATÍSTICAS:\n"
                resultado += f"• Estabelecimentos: {total_est:,}\n"
                resultado += f"• Tipos de queixas: {total_queixas:,}\n"
            
            conn.close()
            return resultado
            
        except Exception as e:
            return f"❌ Erro: {str(e)}"


def main():
    """Função principal - Sistema completo em < 100 linhas!"""
    
    print("🏥 EXERCÍCIO AULA 8: CONSULTA SAÚDE SIMPLES")
    print("=" * 45)
    
    # Verificações
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ Configure OPENAI_API_KEY no .env")
        return
    if not DB_REAL.exists():
        print(f"❌ Banco não encontrado: {DB_REAL}")
        return
    
    # Criar agente
    agente = Agent(
        role="Assistente de Saúde",
        goal="Responder sobre estabelecimentos e queixas",
        backstory="Especialista em dados de saúde pública",
        tools=[ConsultaSaude()],
        llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.1),
        verbose=False
    )
    
    print("✅ Sistema pronto!")
    print("\n💬 Exemplos:")
    print("• 'Quais estabelecimentos temos?'")
    print("• 'Mostre as queixas frequentes'")
    print("• 'Estatísticas gerais'")
    print("\n⌨️  Digite 'sair' para encerrar\n")
    
    # Loop interativo
    while True:
        try:
            pergunta = input("💬 Pergunta: ").strip()
            
            if pergunta.lower() in ['sair', 'quit']:
                print("👋 Até logo!")
                break
                
            if not pergunta:
                continue
            
            print("⏳ Consultando...")
            
            tarefa = Task(
                description=f"Responda sobre saúde: {pergunta}",
                agent=agente,
                expected_output="Resposta clara com dados"
            )
            
            crew = Crew(
                agents=[agente],
                tasks=[tarefa],
                process=Process.sequential,
                verbose=False
            )
            
            resultado = crew.kickoff()
            print(f"\n📋 RESPOSTA:\n{resultado.raw}")
            print("=" * 45)
            
        except KeyboardInterrupt:
            print("\n👋 Interrompido!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()