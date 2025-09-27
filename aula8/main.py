#!/usr/bin/env python3
"""
🎓 AULA 8: CrewAI + SQLite - VERSÃO INTERATIVA
===============================================

EVOLUÇÃO da Aula 7: Agora com prompt interativo e SQLite!

PRINCIPAIS NOVIDADES:
- 🗣️ Prompt interativo para conversar com os agentes
- 🗄️ Uso do banco SQLite (curso.db) ao invés de PostgreSQL  
- 📊 Dados reais de estabelecimentos de saúde
- 🔄 Interface de linha de comando amigável
- 💬 Múltiplas consultas em uma sessão

OBJETIVO:
Mostrar como criar um sistema interativo onde usuários podem
fazer perguntas naturais aos agentes CrewAI conectados ao banco de dados.

EXECUÇÃO:
uv run aula8/main.py

PRÉ-REQUISITOS:
1. Arquivo db/curso.db (já disponível no projeto)
2. OpenAI API Key configurada no .env
3. Dependências instaladas: uv sync
"""

import os
import sys
import sqlite3
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI
from typing import Any, Dict, List

# Carregar configurações
load_dotenv()

# Configurar paths relativos ao projeto
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "db" / "curso.db"

print("🎓 AULA 8: CrewAI + SQLite - VERSÃO INTERATIVA")
print("=" * 55)

# =============================================================================
# PARTE 1: FERRAMENTA SQLITE PARA DADOS DE SAÚDE
# =============================================================================

class ConsultaSaudeTool(BaseTool):
    """
    Ferramenta especializada para consultar dados de saúde no SQLite
    
    Baseada nos dados reais migrados do PostgreSQL:
    - Estabelecimentos de saúde (hospitais, UPAs, postos)
    - Queixas principais e sintomas
    - Histórico de atendimentos
    """
    
    name: str = "consulta_saude"
    description: str = (
        "Consulta dados de estabelecimentos de saúde, sintomas e atendimentos "
        "no banco SQLite. Pode buscar por: estabelecimentos, queixas mais "
        "frequentes, sintomas, estatísticas por bairro ou estabelecimento."
    )
    
    def _run(self, consulta: str = "") -> str:
        """
        Executa consulta inteligente no banco de dados de saúde
        
        Args:
            consulta: Descrição natural do que o usuário quer buscar
        
        Returns:
            str: Dados formatados para análise do agente
        """
        
        try:
            # Verificar se banco existe
            if not DB_PATH.exists():
                return (f"❌ Banco de dados não encontrado em: {DB_PATH}\n"
                       "Verifique se o arquivo db/curso.db existe no projeto.")
            
            print(f"🔍 Conectando ao SQLite: {DB_PATH}")
            conn = sqlite3.connect(str(DB_PATH))
            conn.row_factory = sqlite3.Row  # Permite acesso por nome das colunas
            cursor = conn.cursor()
            
            # Analisar tipo de consulta baseada na descrição
            consulta_lower = consulta.lower()
            
            if any(palavra in consulta_lower for palavra in ['estabelecimento', 'hospital', 'upa', 'posto']):
                resultado = self._buscar_estabelecimentos(cursor, consulta)
                
            elif any(palavra in consulta_lower for palavra in ['queixa', 'sintoma', 'doenca']):
                resultado = self._buscar_queixas_sintomas(cursor, consulta)
                
            elif any(palavra in consulta_lower for palavra in ['bairro', 'regiao', 'localizacao']):
                resultado = self._buscar_por_bairro(cursor, consulta)
                
            elif any(palavra in consulta_lower for palavra in ['estatistica', 'numero', 'quantidade']):
                resultado = self._buscar_estatisticas(cursor, consulta)
                
            else:
                # Consulta geral - retornar overview
                resultado = self._buscar_overview_geral(cursor)
            
            conn.close()
            print("✅ Dados obtidos do SQLite!")
            return resultado
            
        except Exception as erro:
            return f"❌ Erro ao consultar banco: {str(erro)}"
    
    def _buscar_estabelecimentos(self, cursor, consulta: str) -> str:
        """Busca informações sobre estabelecimentos de saúde"""
        
        # Buscar estabelecimentos com informações completas
        cursor.execute("""
            SELECT cnes, nome, endereco, fone, bairro
            FROM ia_estabelecimento
            ORDER BY nome
            LIMIT 20
        """)
        
        estabelecimentos = cursor.fetchall()
        
        if not estabelecimentos:
            return "❌ Nenhum estabelecimento encontrado no banco."
        
        resultado = f"🏥 ESTABELECIMENTOS DE SAÚDE ({len(estabelecimentos)} encontrados):\n\n"
        
        for est in estabelecimentos:
            resultado += f"• **{est['nome']}**\n"
            resultado += f"  📍 Endereço: {est['endereco']}\n"
            resultado += f"  🏘️ Bairro: {est['bairro']}\n"
            resultado += f"  📞 Telefone: {est['fone'] or 'Não informado'}\n"
            resultado += f"  🆔 CNES: {est['cnes']}\n\n"
        
        return resultado
    
    def _buscar_queixas_sintomas(self, cursor, consulta: str) -> str:
        """Busca queixas principais e sintomas mais frequentes"""
        
        # Buscar queixas mais frequentes
        cursor.execute("""
            SELECT 
                q.nome,
                COUNT(*) as total_atendimentos,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM ia_historico_atendimento_sintoma), 2) as percentual
            FROM ia_historico_atendimento_sintoma h
            JOIN ia_queixa_principal q ON h.queixa_principal_id = q.id
            GROUP BY q.id, q.nome
            ORDER BY total_atendimentos DESC
            LIMIT 15
        """)
        
        queixas = cursor.fetchall()
        
        resultado = f"🏥 QUEIXAS PRINCIPAIS MAIS FREQUENTES:\n\n"
        
        for i, queixa in enumerate(queixas, 1):
            resultado += (f"{i}. **{queixa['nome']}**\n"
                         f"   📊 {queixa['total_atendimentos']} atendimentos "
                         f"({queixa['percentual']}% do total)\n\n")
        
        return resultado
    
    def _buscar_por_bairro(self, cursor, consulta: str) -> str:
        """Busca estabelecimentos por bairros"""
        
        # Buscar estatísticas por bairro
        cursor.execute("""
            SELECT 
                e.bairro,
                COUNT(*) as num_estabelecimentos,
                COUNT(DISTINCT h.queixa_principal_id) as tipos_queixas
            FROM ia_estabelecimento e
            LEFT JOIN ia_historico_atendimento_sintoma h ON e.cnes = h.estabelecimento_cnes
            GROUP BY e.bairro
            HAVING e.bairro IS NOT NULL AND e.bairro != ''
            ORDER BY num_estabelecimentos DESC
            LIMIT 15
        """)
        
        bairros = cursor.fetchall()
        
        resultado = f"🏘️ ESTABELECIMENTOS POR BAIRRO:\n\n"
        
        for bairro in bairros:
            resultado += (f"• **{bairro['bairro']}**\n"
                         f"  🏥 {bairro['num_estabelecimentos']} estabelecimentos\n"
                         f"  🏥 {bairro['tipos_queixas']} tipos de queixas atendidas\n\n")
        
        return resultado
    
    def _buscar_estatisticas(self, cursor, consulta: str) -> str:
        """Retorna estatísticas gerais do banco"""
        
        # Contar registros principais
        cursor.execute("SELECT COUNT(*) FROM ia_estabelecimento")
        total_estabelecimentos = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ia_queixa_principal") 
        total_queixas = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ia_sintoma")
        total_sintomas = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ia_historico_atendimento_sintoma")
        total_atendimentos = cursor.fetchone()[0]
        
        # Buscar bairros únicos
        cursor.execute("SELECT COUNT(DISTINCT bairro) FROM ia_estabelecimento WHERE bairro IS NOT NULL")
        total_bairros = cursor.fetchone()[0]
        
        resultado = f"📊 ESTATÍSTICAS DO SISTEMA DE SAÚDE:\n\n"
        resultado += f"🏥 **Estabelecimentos**: {total_estabelecimentos:,}\n"
        resultado += f"🏥 **Queixas cadastradas**: {total_queixas:,}\n"
        resultado += f"💊 **Sintomas únicos**: {total_sintomas:,}\n"
        resultado += f"📋 **Total de atendimentos**: {total_atendimentos:,}\n"
        resultado += f"🏘️ **Bairros atendidos**: {total_bairros:,}\n\n"
        
        return resultado
    
    def _buscar_overview_geral(self, cursor) -> str:
        """Retorna visão geral do banco de dados"""
        
        resultado = f"🔍 VISÃO GERAL DO BANCO DE SAÚDE:\n\n"
        
        # Top 5 estabelecimentos com mais atendimentos
        cursor.execute("""
            SELECT 
                e.nome,
                e.bairro,
                COUNT(*) as total_atendimentos
            FROM ia_estabelecimento e
            JOIN ia_historico_atendimento_sintoma h ON e.cnes = h.estabelecimento_cnes
            GROUP BY e.cnes, e.nome, e.bairro
            ORDER BY total_atendimentos DESC
            LIMIT 5
        """)
        
        top_estabelecimentos = cursor.fetchall()
        resultado += f"🏆 TOP 5 ESTABELECIMENTOS (por atendimentos):\n"
        for i, est in enumerate(top_estabelecimentos, 1):
            resultado += f"{i}. {est['nome']} ({est['bairro']}) - {est['total_atendimentos']:,} atendimentos\n"
        
        resultado += "\n"
        
        # Top 3 queixas
        cursor.execute("""
            SELECT q.nome, COUNT(*) as total
            FROM ia_queixa_principal q
            JOIN ia_historico_atendimento_sintoma h ON q.id = h.queixa_principal_id
            GROUP BY q.id, q.nome
            ORDER BY total DESC
            LIMIT 3
        """)
        
        top_queixas = cursor.fetchall()
        resultado += f"🏥 TOP 3 QUEIXAS MAIS FREQUENTES:\n"
        for i, queixa in enumerate(top_queixas, 1):
            resultado += f"{i}. {queixa['nome']} - {queixa['total']:,} casos\n"
        
        return resultado


# =============================================================================
# PARTE 2: AGENTE ESPECIALISTA EM SAÚDE
# =============================================================================

def criar_agente_saude():
    """Cria agente especializado em dados de saúde"""
    
    print("🤖 Criando agente especialista em saúde...")
    
    # Modelo de linguagem otimizado
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2  # Um pouco mais criativo para respostas naturais
    )
    
    # Ferramenta de consulta
    ferramenta_saude = ConsultaSaudeTool()
    
    # Agente especializado
    agente = Agent(
        role="Especialista em Dados de Saúde",
        goal=("Ajudar usuários a encontrar informações sobre estabelecimentos "
              "de saúde, sintomas, queixas e estatísticas usando dados reais "
              "do sistema de saúde"),
        backstory=("""Sou um especialista em análise de dados de saúde pública 
                   com ampla experiência em sistemas hospitalares e atendimento. 
                   Tenho acesso a uma base completa de dados sobre estabelecimentos 
                   de saúde, incluindo hospitais, UPAs, postos de saúde e clínicas.
                   
                   Minha especialidade é interpretar dados de atendimento, identificar 
                   padrões em queixas e sintomas, e fornecer informações úteis sobre 
                   a rede de saúde de forma clara e acessível."""),
        verbose=False,
        llm=llm,
        tools=[ferramenta_saude]
    )
    
    print("✅ Agente especialista criado!")
    return agente


# =============================================================================
# PARTE 3: SISTEMA INTERATIVO
# =============================================================================

def mostrar_menu_inicial():
    """Mostra opções disponíveis para o usuário"""
    
    print("\n" + "="*60)
    print("🏥 SISTEMA INTERATIVO DE DADOS DE SAÚDE")
    print("="*60)
    print("Converse naturalmente com o agente! Exemplos:")
    print()
    print("💬 PERGUNTAS SUGERIDAS:")
    print("   • 'Quais são os hospitais disponíveis?'")
    print("   • 'Mostre as queixas mais frequentes'") 
    print("   • 'Quantos estabelecimentos existem por bairro?'")
    print("   • 'Quais são as estatísticas gerais?'")
    print("   • 'Hospitais na região central'")
    print("   • 'Sintomas mais relatados pelos pacientes'")
    print()
    print("⌨️  COMANDOS ESPECIAIS:")
    print("   • 'ajuda' - Mostra este menu novamente")
    print("   • 'sair' ou 'quit' - Encerra o programa")
    print("   • 'limpar' - Limpa a tela")
    print("="*60)


def processar_comando_especial(entrada: str) -> bool:
    """
    Processa comandos especiais do usuário
    
    Returns:
        bool: True se deve continuar, False se deve sair
    """
    
    entrada = entrada.lower().strip()
    
    if entrada in ['sair', 'quit', 'exit', 'q']:
        print("\n👋 Obrigado por usar o sistema! Até mais!")
        return False
    
    elif entrada in ['ajuda', 'help', 'h']:
        mostrar_menu_inicial()
        return True
    
    elif entrada in ['limpar', 'clear', 'cls']:
        os.system('clear' if os.name == 'posix' else 'cls')
        mostrar_menu_inicial()
        return True
    
    elif entrada == '':
        print("💭 Digite sua pergunta ou 'ajuda' para ver opções")
        return True
    
    return True  # Continuar processamento normal


def executar_consulta_interativa(agente: Agent, pergunta: str) -> str:
    """Executa uma consulta do usuário usando o agente"""
    
    print(f"\n🤔 Analisando: '{pergunta}'")
    print("⏳ Agente trabalhando...")
    
    # Criar tarefa dinâmica baseada na pergunta do usuário
    tarefa = Task(
        description=f"""
        O usuário fez esta pergunta sobre dados de saúde: "{pergunta}"
        
        Use a ferramenta consulta_saude para buscar as informações relevantes
        e forneça uma resposta completa e útil ao usuário.
        
        DIRETRIZES:
        - Seja amigável e profissional
        - Organize as informações de forma clara
        - Use emojis para tornar a resposta mais legível
        - Se não encontrar dados específicos, explique e sugira alternativas
        - Mencione insights interessantes dos dados quando apropriado
        """,
        agent=agente,
        expected_output=("Resposta clara e bem formatada com as informações "
                        "solicitadas pelo usuário, incluindo dados específicos "
                        "e contexto relevante")
    )
    
    # Executar com crew
    crew = Crew(
        agents=[agente],
        tasks=[tarefa],
        process=Process.sequential,
        verbose=False  # Reduzir ruído na interface
    )
    
    try:
        resultado = crew.kickoff()
        return resultado.raw
        
    except Exception as e:
        return f"❌ Erro ao processar consulta: {str(e)}\n💡 Tente reformular sua pergunta."


def sistema_interativo():
    """Sistema principal de interação com o usuário"""
    
    # Verificar pré-requisitos
    if not DB_PATH.exists():
        print(f"❌ ERRO: Banco de dados não encontrado!")
        print(f"📁 Esperado em: {DB_PATH}")
        print("\n💡 SOLUÇÃO:")
        print("   1. Verifique se o arquivo db/curso.db existe")
        print("   2. Execute a migração se necessário")
        return
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ ERRO: OpenAI API Key não configurada!")
        print("\n💡 SOLUÇÃO:")
        print("   1. Configure no arquivo .env: OPENAI_API_KEY=sua_chave")
        print("   2. Ou execute: uv run configurar.py")
        return
    
    print("🔄 Iniciando sistema interativo...")
    
    # Criar agente
    agente_saude = criar_agente_saude()
    
    # Testar conexão com banco
    try:
        print("🔍 Testando conexão com SQLite...")
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM ia_estabelecimento")
        total = cursor.fetchone()[0]
        conn.close()
        print(f"✅ Banco conectado! {total} estabelecimentos disponíveis")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
        return
    
    # Mostrar menu inicial
    mostrar_menu_inicial()
    
    print("\n🚀 Sistema pronto! Digite sua primeira pergunta:")
    
    # Loop principal de interação
    while True:
        try:
            # Obter entrada do usuário
            entrada = input("\n💬 Sua pergunta: ").strip()
            
            # Processar comandos especiais
            if not processar_comando_especial(entrada):
                break  # Sair do loop
            
            # Pular entradas vazias ou comandos especiais já processados
            if entrada.lower() in ['ajuda', 'help', 'limpar', 'clear', 'cls', '']:
                continue
            
            # Executar consulta real
            print("\n" + "="*50)
            resposta = executar_consulta_interativa(agente_saude, entrada)
            print("\n📋 RESPOSTA DO AGENTE:")
            print("-" * 30)
            print(resposta)
            print("="*50)
            
        except KeyboardInterrupt:
            print("\n\n⏹️  Interrompido pelo usuário. Finalizando...")
            break
            
        except Exception as e:
            print(f"\n❌ Erro inesperado: {str(e)}")
            print("💡 Tente novamente ou digite 'sair' para encerrar")


# =============================================================================
# PARTE 4: EXEMPLOS DEMONSTRATIVOS
# =============================================================================

def executar_demo_automatico():
    """Executa demonstração automática do sistema"""
    
    print("\n🎬 EXECUTANDO DEMONSTRAÇÃO AUTOMÁTICA")
    print("="*50)
    
    agente = criar_agente_saude()
    
    exemplos = [
        "Quantos estabelecimentos de saúde existem no total?",
        "Quais são as 5 queixas mais frequentes?", 
        "Mostre estabelecimentos por bairro",
        "Quais hospitais têm mais atendimentos?"
    ]
    
    for i, exemplo in enumerate(exemplos, 1):
        print(f"\n📝 EXEMPLO {i}: {exemplo}")
        print("-" * 40)
        
        resposta = executar_consulta_interativa(agente, exemplo)
        print(resposta)
        
        if i < len(exemplos):
            input("\n⏸️  Pressione ENTER para continuar...")


# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    """Função principal do programa"""
    
    print("🎯 ESCOLHA O MODO DE EXECUÇÃO:")
    print("1. 💬 Modo Interativo (recomendado)")
    print("2. 🎬 Demonstração Automática")
    print("3. ❌ Sair")
    
    while True:
        escolha = input("\nEscolha uma opção (1-3): ").strip()
        
        if escolha == '1':
            sistema_interativo()
            break
        elif escolha == '2':
            executar_demo_automatico()
            break
        elif escolha == '3':
            print("👋 Até mais!")
            break
        else:
            print("⚠️ Opção inválida. Escolha 1, 2 ou 3.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Programa interrompido. Até mais!")
    except Exception as e:
        print(f"\n❌ Erro fatal: {str(e)}")
        print("\n🆘 AJUDA:")
        print("   • Verifique se o arquivo db/curso.db existe")
        print("   • Confirme a OpenAI API Key no .env")
        print("   • Execute: uv sync para instalar dependências")