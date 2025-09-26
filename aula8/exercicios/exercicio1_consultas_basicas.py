#!/usr/bin/env python3
"""
🎓 EXERCÍCIO 1: Consultas Básicas com SQLite
============================================

OBJETIVO:
Aprender a criar consultas simples no banco SQLite através dos agentes CrewAI.
Modificar e estender as funcionalidades básicas do sistema.

NÍVEL: 🟢 BÁSICO

EXERCÍCIOS INCLUÍDOS:
1. Busca por tipo específico de estabelecimento
2. Filtros por região/bairro  
3. Análise de queixas por frequência
4. Estatísticas customizadas

EXECUÇÃO:
uv run aula8/exercicios/exercicio1_consultas_basicas.py
"""

import sqlite3
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI

# Configuração
load_dotenv()
PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "db" / "curso.db"

print("🎓 EXERCÍCIO 1: Consultas Básicas SQLite")
print("=" * 45)


class ConsultaBasicaTool(BaseTool):
    """Ferramenta simplificada para exercícios básicos"""
    
    name: str = "consulta_basica"
    description: str = "Executa consultas básicas no banco SQLite de saúde"
    
    def _run(self, tipo_consulta: str = "geral") -> str:
        """
        Executa consultas pré-definidas para aprendizado
        
        Tipos disponíveis:
        - 'upas': Apenas UPAs  
        - 'hospitais': Apenas hospitais
        - 'bairros': Estatísticas por bairro
        - 'queixas_top': Top 10 queixas
        - 'geral': Visão geral
        """
        
        try:
            if not DB_PATH.exists():
                return f"❌ Banco não encontrado: {DB_PATH}"
            
            conn = sqlite3.connect(str(DB_PATH))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if tipo_consulta.lower() == 'upas':
                return self._buscar_upas(cursor)
            elif tipo_consulta.lower() == 'hospitais':  
                return self._buscar_hospitais(cursor)
            elif tipo_consulta.lower() == 'bairros':
                return self._estatisticas_bairros(cursor)
            elif tipo_consulta.lower() == 'queixas_top':
                return self._top_queixas(cursor)
            else:
                return self._visao_geral(cursor)
                
        except Exception as e:
            return f"❌ Erro: {str(e)}"
        finally:
            if 'conn' in locals():
                conn.close()
    
    def _buscar_upas(self, cursor) -> str:
        """Busca apenas UPAs"""
        cursor.execute("""
            SELECT nome, endereco, bairro, fone
            FROM ia_estabelecimento  
            WHERE nome LIKE '%UPA%' OR nome LIKE '%Unidade de Pronto Atendimento%'
            ORDER BY nome
            LIMIT 15
        """)
        
        upas = cursor.fetchall()
        
        if not upas:
            return "❌ Nenhuma UPA encontrada"
        
        resultado = f"🏥 UPAs ENCONTRADAS ({len(upas)}):\n\n"
        
        for upa in upas:
            resultado += f"• **{upa['nome']}**\n"
            resultado += f"  📍 {upa['endereco']}\n"  
            resultado += f"  🏘️ {upa['bairro']}\n"
            if upa['fone']:
                resultado += f"  📞 {upa['fone']}\n"
            resultado += "\n"
            
        return resultado
    
    def _buscar_hospitais(self, cursor) -> str:
        """Busca apenas hospitais"""
        cursor.execute("""
            SELECT nome, endereco, bairro, fone
            FROM ia_estabelecimento
            WHERE nome LIKE '%Hospital%' OR nome LIKE '%HOSPITAL%'
            ORDER BY nome  
            LIMIT 15
        """)
        
        hospitais = cursor.fetchall()
        
        resultado = f"🏥 HOSPITAIS ENCONTRADOS ({len(hospitais)}):\n\n"
        
        for hospital in hospitais:
            resultado += f"• **{hospital['nome']}**\n"
            resultado += f"  📍 {hospital['endereco']}\n"
            resultado += f"  🏘️ {hospital['bairro']}\n" 
            if hospital['fone']:
                resultado += f"  📞 {hospital['fone']}\n"
            resultado += "\n"
            
        return resultado
    
    def _estatisticas_bairros(self, cursor) -> str:
        """Estatísticas por bairro"""
        cursor.execute("""
            SELECT 
                bairro,
                COUNT(*) as total_estabelecimentos
            FROM ia_estabelecimento
            WHERE bairro IS NOT NULL AND bairro != ''
            GROUP BY bairro
            ORDER BY total_estabelecimentos DESC
            LIMIT 20
        """)
        
        bairros = cursor.fetchall()
        
        resultado = f"🏘️ ESTABELECIMENTOS POR BAIRRO (Top 20):\n\n"
        
        for i, bairro in enumerate(bairros, 1):
            resultado += (f"{i:2d}. **{bairro['bairro']}**: "
                         f"{bairro['total_estabelecimentos']} estabelecimentos\n")
        
        return resultado
    
    def _top_queixas(self, cursor) -> str:
        """Top 10 queixas mais frequentes"""
        cursor.execute("""
            SELECT 
                q.nome,
                COUNT(*) as total_casos,
                ROUND(COUNT(*) * 100.0 / (
                    SELECT COUNT(*) FROM ia_historico_atendimento_sintoma
                ), 2) as percentual
            FROM ia_historico_atendimento_sintoma h
            JOIN ia_queixa_principal q ON h.queixa_principal_id = q.id  
            GROUP BY q.id, q.nome
            ORDER BY total_casos DESC
            LIMIT 10
        """)
        
        queixas = cursor.fetchall()
        
        resultado = f"🏥 TOP 10 QUEIXAS MAIS FREQUENTES:\n\n"
        
        for i, queixa in enumerate(queixas, 1):
            resultado += (f"{i:2d}. **{queixa['nome']}**\n"
                         f"    📊 {queixa['total_casos']:,} casos "
                         f"({queixa['percentual']}%)\n\n")
        
        return resultado
    
    def _visao_geral(self, cursor) -> str:
        """Visão geral do banco"""
        # Contar estabelecimentos
        cursor.execute("SELECT COUNT(*) FROM ia_estabelecimento")
        total_est = cursor.fetchone()[0]
        
        # Contar queixas
        cursor.execute("SELECT COUNT(*) FROM ia_queixa_principal")
        total_queixas = cursor.fetchone()[0]
        
        # Contar atendimentos
        cursor.execute("SELECT COUNT(*) FROM ia_historico_atendimento_sintoma")
        total_atend = cursor.fetchone()[0]
        
        return (f"📊 VISÃO GERAL DO BANCO:\n\n"
               f"🏥 Estabelecimentos: {total_est:,}\n"
               f"🏥 Queixas únicas: {total_queixas:,}\n"
               f"📋 Total atendimentos: {total_atend:,}\n")


def criar_agente_exercicio():
    """Cria agente para exercícios básicos"""
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    
    return Agent(
        role="Assistente de Exercícios de Banco de Dados",
        goal="Ajudar a aprender consultas básicas em bancos de saúde SQLite",
        backstory=("Sou um tutor especializado em ensinar consultas de banco "
                   "de dados para iniciantes. Ajudo a entender como buscar "
                   "informações específicas sobre estabelecimentos de saúde."),
        verbose=True,
        llm=llm,
        tools=[ConsultaBasicaTool()]
    )


def exercicio_1_tipos_estabelecimento():
    """Exercício: Buscar tipos específicos de estabelecimento"""
    
    print("\n🔍 EXERCÍCIO 1.1: Tipos de Estabelecimento")
    print("-" * 40)
    
    agente = criar_agente_exercicio()
    
    # Buscar UPAs
    tarefa_upas = Task(
        description="""
        Use a ferramenta consulta_basica com tipo_consulta='upas' 
        para buscar apenas as UPAs (Unidades de Pronto Atendimento).
        
        Forneça uma lista organizada e destaque informações importantes.
        """,
        agent=agente,
        expected_output="Lista formatada de UPAs com endereços e contatos"
    )
    
    crew = Crew(
        agents=[agente],
        tasks=[tarefa_upas],
        process=Process.sequential,
        verbose=False
    )
    
    resultado = crew.kickoff()
    print(resultado.raw)
    
    input("\n⏸️ Pressione ENTER para continuar para o próximo exercício...")


def exercicio_2_hospitais():
    """Exercício: Buscar hospitais específicos"""
    
    print("\n🏥 EXERCÍCIO 1.2: Hospitais") 
    print("-" * 40)
    
    agente = criar_agente_exercicio()
    
    tarefa_hospitais = Task(
        description="""
        Use a ferramenta consulta_basica com tipo_consulta='hospitais'
        para buscar apenas hospitais.
        
        Organize a lista de forma clara e destaque as informações de contato.
        """,
        agent=agente,
        expected_output="Lista de hospitais com informações completas"
    )
    
    crew = Crew(
        agents=[agente],
        tasks=[tarefa_hospitais],
        process=Process.sequential,
        verbose=False
    )
    
    resultado = crew.kickoff()
    print(resultado.raw)
    
    input("\n⏸️ Pressione ENTER para continuar...")


def exercicio_3_estatisticas():
    """Exercício: Análises estatísticas básicas"""
    
    print("\n📊 EXERCÍCIO 1.3: Estatísticas Básicas")
    print("-" * 40)
    
    agente = criar_agente_exercicio()
    
    # Estatísticas por bairro
    tarefa_bairros = Task(
        description="""
        Use a ferramenta consulta_basica com tipo_consulta='bairros'
        para ver a distribuição de estabelecimentos por bairro.
        
        Analise os dados e destaque quais bairros têm mais cobertura de saúde.
        """,
        agent=agente,
        expected_output="Análise da distribuição de estabelecimentos por bairro"
    )
    
    crew = Crew(
        agents=[agente],
        tasks=[tarefa_bairros],
        process=Process.sequential,
        verbose=False
    )
    
    resultado = crew.kickoff()
    print(resultado.raw)
    
    input("\n⏸️ Pressione ENTER para continuar...")


def exercicio_4_queixas():
    """Exercício: Análise de queixas mais frequentes"""
    
    print("\n🏥 EXERCÍCIO 1.4: Queixas Mais Frequentes")
    print("-" * 40)
    
    agente = criar_agente_exercicio()
    
    tarefa_queixas = Task(
        description="""
        Use a ferramenta consulta_basica com tipo_consulta='queixas_top'
        para ver as queixas de saúde mais comuns.
        
        Analise os padrões e destaque insights interessantes sobre 
        a saúde pública baseado nos dados.
        """,
        agent=agente,
        expected_output="Análise das queixas mais frequentes com insights"
    )
    
    crew = Crew(
        agents=[agente],
        tasks=[tarefa_queixas], 
        process=Process.sequential,
        verbose=False
    )
    
    resultado = crew.kickoff()
    print(resultado.raw)


def menu_exercicios():
    """Menu interativo dos exercícios"""
    
    print("\n🎯 ESCOLHA QUAL EXERCÍCIO EXECUTAR:")
    print("1. 🏥 Buscar UPAs")
    print("2. 🏥 Buscar Hospitais") 
    print("3. 📊 Estatísticas por Bairro")
    print("4. 🏥 Queixas Mais Frequentes")
    print("5. 🚀 Executar Todos os Exercícios")
    print("6. ❌ Sair")
    
    while True:
        escolha = input("\nEscolha (1-6): ").strip()
        
        if escolha == '1':
            exercicio_1_tipos_estabelecimento()
            break
        elif escolha == '2':
            exercicio_2_hospitais()
            break
        elif escolha == '3':
            exercicio_3_estatisticas()
            break
        elif escolha == '4':
            exercicio_4_queixas()
            break
        elif escolha == '5':
            print("\n🚀 EXECUTANDO TODOS OS EXERCÍCIOS...")
            exercicio_1_tipos_estabelecimento()
            exercicio_2_hospitais()
            exercicio_3_estatisticas()
            exercicio_4_queixas()
            print("\n✅ TODOS OS EXERCÍCIOS CONCLUÍDOS!")
            break
        elif escolha == '6':
            print("👋 Até mais!")
            break
        else:
            print("⚠️ Opção inválida. Escolha 1-6.")


def main():
    """Função principal"""
    
    # Verificações
    if not DB_PATH.exists():
        print(f"❌ Banco não encontrado: {DB_PATH}")
        print("💡 Verifique se o arquivo db/curso.db existe")
        return
    
    print("✅ Banco SQLite encontrado!")
    print("✅ Pronto para exercícios básicos!")
    
    menu_exercicios()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Interrompido. Até mais!")
    except Exception as e:
        print(f"\n❌ Erro: {str(e)}")