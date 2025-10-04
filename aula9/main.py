#!/usr/bin/env python3
"""
🎓 AULA 9: CrewAI + Múltiplos Agentes Especializados 
=====================================================

EVOLUÇÃO da Aula 8: Agora com múltiplos agentes trabalhando em equipe!

PRINCIPAIS NOVIDADES:
- 🤖 Múltiplos agentes especializados trabalhando em conjunto
- 🧠 Agente Analisador de Consultas (NOVO!) - classifica perguntas automaticamente
- 🏥 Agente Especialista em Dados de Saúde (evoluído da Aula 8)
- 📊 Agente Estatístico - focado em análises e relatórios
- 🔄 Processo hierarchical para coordenação inteligente
- 🎯 Delegação automática baseada no tipo de consulta

OBJETIVO:
Demonstrar como criar um sistema com múltiplos agentes especializados
que trabalham em conjunto, cada um com suas expertise específicas,
coordenados por um processo hierarchical do CrewAI.

EXECUÇÃO:
uv run aula9/main.py

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
from typing import Any, Dict, List, Tuple
import json

# Carregar configurações
load_dotenv()

# Configurar paths relativos ao projeto
PROJECT_ROOT = Path(__file__).parent.parent
DB_PATH = PROJECT_ROOT / "db" / "curso.db"

print("🎓 AULA 9: CrewAI + Múltiplos Agentes Especializados")
print("=" * 58)

# =============================================================================
# PARTE 1: FERRAMENTAS ESPECIALIZADAS
# =============================================================================

class AnalisadorConsultaTool(BaseTool):
    """
    🧠 NOVA FERRAMENTA: Analisa e classifica tipos de consulta
    
    Esta ferramenta é usada pelo Agente Analisador para identificar
    automaticamente o tipo de consulta e sugerir qual agente deve responder.
    """
    
    name: str = "analisador_consulta"
    description: str = (
        "Analisa perguntas dos usuários e classifica o tipo de consulta "
        "para determinar qual agente especializado deve responder. "
        "Identifica: consultas sobre estabelecimentos, estatísticas, "
        "queixas/sintomas, distribuição geográfica, ou visão geral."
    )
    
    def _run(self, pergunta: str = "") -> str:
        """
        Analisa a pergunta e retorna classificação estruturada
        
        Args:
            pergunta: Pergunta do usuário em linguagem natural
        
        Returns:
            str: Análise estruturada em JSON com tipo, confiança e justificativa
        """
        
        pergunta_lower = pergunta.lower().strip()
        
        # Definir palavras-chave para cada tipo de consulta
        tipos_consulta = {
            "estabelecimentos": {
                "palavras": ["hospital", "upa", "posto", "estabelecimento", "clínica", "ambulatório", "unidade", "endereço", "telefone", "contato"],
                "descrição": "Consultas sobre estabelecimentos de saúde específicos",
                "agente_recomendado": "Especialista em Dados de Saúde"
            },
            "estatisticas": {
                "palavras": ["estatística", "número", "quantidade", "total", "contar", "quantos", "ranking", "top", "maior", "menor", "percentual"],
                "descrição": "Consultas que requerem análises numéricas e estatísticas",
                "agente_recomendado": "Agente Estatístico"
            },
            "queixas_sintomas": {
                "palavras": ["queixa", "sintoma", "doença", "problema", "dor", "febre", "cefaleia", "frequente", "comum", "paciente"],
                "descrição": "Consultas sobre queixas principais e sintomas",
                "agente_recomendado": "Especialista em Dados de Saúde"
            },
            "geografico": {
                "palavras": ["bairro", "região", "localização", "área", "zona", "distrito", "onde", "local", "distribuição"],
                "descrição": "Consultas sobre distribuição geográfica",
                "agente_recomendado": "Agente Estatístico"
            },
            "visao_geral": {
                "palavras": ["geral", "overview", "resumo", "completo", "tudo", "todas", "principais", "importante"],
                "descrição": "Consultas que pedem visão ampla do sistema",
                "agente_recomendado": "Especialista em Dados de Saúde"
            }
        }
        
        # Calcular pontuação para cada tipo
        pontuacoes = {}
        for tipo, config in tipos_consulta.items():
            pontuacao = 0
            palavras_encontradas = []
            
            for palavra in config["palavras"]:
                if palavra in pergunta_lower:
                    pontuacao += 1
                    palavras_encontradas.append(palavra)
            
            pontuacoes[tipo] = {
                "pontuacao": pontuacao,
                "palavras_encontradas": palavras_encontradas,
                "config": config
            }
        
        # Encontrar tipo com maior pontuação
        tipo_principal = max(pontuacoes.keys(), key=lambda x: pontuacoes[x]["pontuacao"])
        maior_pontuacao = pontuacoes[tipo_principal]["pontuacao"]
        
        # Calcular confiança
        total_palavras_consulta = len(pergunta_lower.split())
        confianca = min(100, (maior_pontuacao / max(1, total_palavras_consulta)) * 100)
        
        # Se pontuação muito baixa, classificar como geral
        if maior_pontuacao == 0:
            tipo_principal = "visao_geral"
            confianca = 50  # Confiança média para consultas gerais
        
        # Preparar resultado estruturado
        resultado = {
            "pergunta_original": pergunta,
            "tipo_identificado": tipo_principal,
            "confianca_percentual": round(confianca, 1),
            "agente_recomendado": pontuacoes[tipo_principal]["config"]["agente_recomendado"],
            "justificativa": {
                "descrição": pontuacoes[tipo_principal]["config"]["descrição"],
                "palavras_chave_encontradas": pontuacoes[tipo_principal]["palavras_encontradas"],
                "todas_pontuacoes": {k: v["pontuacao"] for k, v in pontuacoes.items()}
            },
            "recomendacao": f"Baseado na análise, recomendo encaminhar para o {pontuacoes[tipo_principal]['config']['agente_recomendado']}"
        }
        
        return json.dumps(resultado, ensure_ascii=False, indent=2)


class ConsultaSaudeAvancadaTool(BaseTool):
    """
    🏥 FERRAMENTA EVOLUÍDA: Versão avançada da ConsultaSaudeTool da Aula 8
    
    Agora com funcionalidades aprimoradas e melhor integração com múltiplos agentes.
    """
    
    name: str = "consulta_saude_avancada"
    description: str = (
        "Consulta avançada de dados de estabelecimentos de saúde no SQLite. "
        "Suporta filtros específicos, buscas direcionadas e formatação otimizada "
        "para diferentes tipos de agentes especializados."
    )
    
    def _run(self, tipo_consulta: str = "", filtros: str = "", limite: int = 20) -> str:
        """
        Executa consulta direcionada baseada no tipo identificado
        
        Args:
            tipo_consulta: Tipo específico (estabelecimentos, queixas, geografico, etc.)
            filtros: Filtros adicionais específicos
            limite: Limite de resultados
        
        Returns:
            str: Dados formatados específicos para o tipo de consulta
        """
        
        try:
            if not DB_PATH.exists():
                return (f"❌ Banco de dados não encontrado em: {DB_PATH}")
            
            print(f"🔍 Consulta avançada: {tipo_consulta}")
            conn = sqlite3.connect(str(DB_PATH))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Roteamento baseado no tipo de consulta
            if tipo_consulta == "estabelecimentos":
                resultado = self._consulta_estabelecimentos_detalhada(cursor, filtros, limite)
            elif tipo_consulta == "queixas_sintomas":
                resultado = self._consulta_queixas_detalhada(cursor, filtros, limite)
            elif tipo_consulta == "geografico":
                resultado = self._consulta_geografica_detalhada(cursor, filtros, limite)
            elif tipo_consulta == "estatisticas":
                resultado = self._consulta_estatisticas_avancadas(cursor, filtros)
            else:
                resultado = self._consulta_overview_completa(cursor)
            
            conn.close()
            return resultado
            
        except Exception as erro:
            return f"❌ Erro na consulta avançada: {str(erro)}"
    
    def _consulta_estabelecimentos_detalhada(self, cursor, filtros: str, limite: int) -> str:
        """Consulta detalhada de estabelecimentos com filtros opcionais"""
        
        query_base = """
            SELECT cnes, nome, endereco, fone, bairro,
                   COUNT(h.id) as total_atendimentos
            FROM ia_estabelecimento e
            LEFT JOIN ia_historico_atendimento_sintoma h ON e.cnes = h.estabelecimento_cnes
        """
        
        # Aplicar filtros se especificados
        where_clause = ""
        if filtros:
            if "bairro" in filtros.lower():
                where_clause = "WHERE e.bairro IS NOT NULL"
            elif "hospital" in filtros.lower():
                where_clause = "WHERE e.nome LIKE '%HOSPITAL%'"
            elif "upa" in filtros.lower():
                where_clause = "WHERE e.nome LIKE '%UPA%'"
        
        query_final = f"""
            {query_base}
            {where_clause}
            GROUP BY e.cnes, e.nome, e.endereco, e.fone, e.bairro
            ORDER BY total_atendimentos DESC, e.nome
            LIMIT {limite}
        """
        
        cursor.execute(query_final)
        estabelecimentos = cursor.fetchall()
        
        if not estabelecimentos:
            return "❌ Nenhum estabelecimento encontrado com os critérios especificados."
        
        resultado = f"🏥 ESTABELECIMENTOS DE SAÚDE DETALHADOS ({len(estabelecimentos)} encontrados):\n\n"
        
        for est in estabelecimentos:
            resultado += f"🏥 **{est['nome']}**\n"
            resultado += f"   📍 Endereço: {est['endereco']}\n"
            resultado += f"   🏘️ Bairro: {est['bairro']}\n"
            resultado += f"   📞 Telefone: {est['fone'] or 'Não informado'}\n"
            resultado += f"   📊 Atendimentos registrados: {est['total_atendimentos']:,}\n"
            resultado += f"   🆔 CNES: {est['cnes']}\n\n"
        
        return resultado
    
    def _consulta_queixas_detalhada(self, cursor, filtros: str, limite: int) -> str:
        """Consulta detalhada de queixas e sintomas"""
        
        cursor.execute("""
            SELECT 
                q.nome,
                COUNT(*) as total_atendimentos,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM ia_historico_atendimento_sintoma), 2) as percentual,
                COUNT(DISTINCT h.estabelecimento_cnes) as estabelecimentos_atenderam
            FROM ia_historico_atendimento_sintoma h
            JOIN ia_queixa_principal q ON h.queixa_principal_id = q.id
            GROUP BY q.id, q.nome
            ORDER BY total_atendimentos DESC
            LIMIT ?
        """, (limite,))
        
        queixas = cursor.fetchall()
        
        resultado = f"🏥 ANÁLISE DETALHADA DE QUEIXAS PRINCIPAIS:\n\n"
        
        for i, queixa in enumerate(queixas, 1):
            resultado += (f"{i}. **{queixa['nome']}**\n"
                         f"   📊 Total de atendimentos: {queixa['total_atendimentos']:,}\n"
                         f"   📈 Percentual do total: {queixa['percentual']}%\n"
                         f"   🏥 Estabelecimentos que atendem: {queixa['estabelecimentos_atenderam']}\n\n")
        
        return resultado
    
    def _consulta_geografica_detalhada(self, cursor, filtros: str, limite: int) -> str:
        """Consulta detalhada por distribuição geográfica"""
        
        cursor.execute("""
            SELECT 
                e.bairro,
                COUNT(DISTINCT e.cnes) as num_estabelecimentos,
                COUNT(h.id) as total_atendimentos,
                COUNT(DISTINCT h.queixa_principal_id) as tipos_queixas_diferentes,
                GROUP_CONCAT(DISTINCT e.nome) as nomes_estabelecimentos
            FROM ia_estabelecimento e
            LEFT JOIN ia_historico_atendimento_sintoma h ON e.cnes = h.estabelecimento_cnes
            WHERE e.bairro IS NOT NULL AND e.bairro != ''
            GROUP BY e.bairro
            ORDER BY total_atendimentos DESC
            LIMIT ?
        """, (limite,))
        
        bairros = cursor.fetchall()
        
        resultado = f"🏘️ ANÁLISE GEOGRÁFICA DETALHADA:\n\n"
        
        for bairro in bairros:
            resultado += f"📍 **{bairro['bairro']}**\n"
            resultado += f"   🏥 Estabelecimentos: {bairro['num_estabelecimentos']}\n"
            resultado += f"   📊 Total de atendimentos: {bairro['total_atendimentos']:,}\n"
            resultado += f"   🏥 Tipos de queixas diferentes: {bairro['tipos_queixas_diferentes']}\n"
            
            # Mostrar nomes dos estabelecimentos (limitado)
            nomes = bairro['nomes_estabelecimentos']
            if nomes:
                nomes_list = nomes.split(',')[:3]  # Mostrar apenas 3 primeiros
                resultado += f"   🏥 Principais: {', '.join(nomes_list)}"
                if len(nomes.split(',')) > 3:
                    resultado += f" (e mais {len(nomes.split(',')) - 3})"
                resultado += "\n"
            
            resultado += "\n"
        
        return resultado
    
    def _consulta_estatisticas_avancadas(self, cursor, filtros: str) -> str:
        """Consulta estatísticas avançadas e métricas do sistema"""
        
        # Estatísticas básicas
        stats = {}
        
        cursor.execute("SELECT COUNT(*) FROM ia_estabelecimento")
        stats['estabelecimentos'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ia_queixa_principal")
        stats['queixas'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ia_sintoma")
        stats['sintomas'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ia_historico_atendimento_sintoma")
        stats['atendimentos'] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT bairro) FROM ia_estabelecimento WHERE bairro IS NOT NULL")
        stats['bairros'] = cursor.fetchone()[0]
        
        # Média de atendimentos por estabelecimento
        cursor.execute("""
            SELECT AVG(atendimentos_por_estabelecimento) as media
            FROM (
                SELECT COUNT(*) as atendimentos_por_estabelecimento
                FROM ia_historico_atendimento_sintoma
                GROUP BY estabelecimento_cnes
            )
        """)
        media_result = cursor.fetchone()
        stats['media_atendimentos'] = round(media_result[0], 1) if media_result[0] else 0
        
        # Estabelecimento mais ativo
        cursor.execute("""
            SELECT e.nome, COUNT(*) as total
            FROM ia_estabelecimento e
            JOIN ia_historico_atendimento_sintoma h ON e.cnes = h.estabelecimento_cnes
            GROUP BY e.cnes, e.nome
            ORDER BY total DESC
            LIMIT 1
        """)
        mais_ativo = cursor.fetchone()
        
        resultado = f"📊 ESTATÍSTICAS AVANÇADAS DO SISTEMA:\n\n"
        resultado += f"📈 **MÉTRICAS GERAIS:**\n"
        resultado += f"   🏥 Total de estabelecimentos: {stats['estabelecimentos']:,}\n"
        resultado += f"   🏥 Queixas catalogadas: {stats['queixas']:,}\n"
        resultado += f"   💊 Sintomas únicos: {stats['sintomas']:,}\n"
        resultado += f"   📋 Total de atendimentos: {stats['atendimentos']:,}\n"
        resultado += f"   🏘️ Bairros cobertos: {stats['bairros']:,}\n\n"
        
        resultado += f"📊 **MÉTRICAS AVANÇADAS:**\n"
        resultado += f"   📈 Média de atendimentos por estabelecimento: {stats['media_atendimentos']:,}\n"
        
        if mais_ativo:
            resultado += f"   🏆 Estabelecimento mais ativo: {mais_ativo['nome']} ({mais_ativo['total']:,} atendimentos)\n"
        
        # Taxa de ocupação por bairro
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT e.cnes) as estabelecimentos,
                COUNT(h.id) as atendimentos,
                ROUND(COUNT(h.id) * 1.0 / COUNT(DISTINCT e.cnes), 1) as taxa_atendimento
            FROM ia_estabelecimento e
            LEFT JOIN ia_historico_atendimento_sintoma h ON e.cnes = h.estabelecimento_cnes
        """)
        
        taxa_result = cursor.fetchone()
        if taxa_result:
            resultado += f"   📊 Taxa média de atendimentos por estabelecimento: {taxa_result['taxa_atendimento']}\n"
        
        resultado += "\n"
        
        return resultado
    
    def _consulta_overview_completa(self, cursor) -> str:
        """Consulta overview completa do sistema"""
        
        resultado = f"🔍 VISÃO GERAL COMPLETA DO SISTEMA DE SAÚDE:\n\n"
        
        # Top 3 estabelecimentos
        cursor.execute("""
            SELECT 
                e.nome,
                e.bairro,
                COUNT(*) as total_atendimentos
            FROM ia_estabelecimento e
            JOIN ia_historico_atendimento_sintoma h ON e.cnes = h.estabelecimento_cnes
            GROUP BY e.cnes, e.nome, e.bairro
            ORDER BY total_atendimentos DESC
            LIMIT 3
        """)
        
        top_estabelecimentos = cursor.fetchall()
        resultado += f"🏆 **TOP 3 ESTABELECIMENTOS:**\n"
        for i, est in enumerate(top_estabelecimentos, 1):
            resultado += f"   {i}. {est['nome']} ({est['bairro']}) - {est['total_atendimentos']:,} atendimentos\n"
        
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
        resultado += f"\n🏥 **TOP 3 QUEIXAS:**\n"
        for i, queixa in enumerate(top_queixas, 1):
            resultado += f"   {i}. {queixa['nome']} - {queixa['total']:,} casos\n"
        
        # Top 3 bairros
        cursor.execute("""
            SELECT 
                e.bairro,
                COUNT(h.id) as total_atendimentos
            FROM ia_estabelecimento e
            JOIN ia_historico_atendimento_sintoma h ON e.cnes = h.estabelecimento_cnes
            WHERE e.bairro IS NOT NULL
            GROUP BY e.bairro
            ORDER BY total_atendimentos DESC
            LIMIT 3
        """)
        
        top_bairros = cursor.fetchall()
        resultado += f"\n🏘️ **TOP 3 BAIRROS (por atendimentos):**\n"
        for i, bairro in enumerate(top_bairros, 1):
            resultado += f"   {i}. {bairro['bairro']} - {bairro['total_atendimentos']:,} atendimentos\n"
        
        return resultado


# =============================================================================
# PARTE 2: MÚLTIPLOS AGENTES ESPECIALIZADOS
# =============================================================================

def criar_agente_analisador():
    """
    🧠 NOVO AGENTE: Analisador de Consultas
    
    Este agente é responsável por analisar as perguntas dos usuários
    e determinar qual agente especializado deve responder.
    """
    
    print("🧠 Criando Agente Analisador de Consultas...")
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1  # Baixa criatividade para análises precisas
    )
    
    ferramenta_analisador = AnalisadorConsultaTool()
    
    agente = Agent(
        role="Analisador de Consultas Especializado",
        goal=("Analisar perguntas dos usuários sobre dados de saúde e determinar "
              "qual agente especializado deve responder, classificando o tipo "
              "de consulta e fornecendo recomendações precisas"),
        backstory=("""Sou um especialista em processamento de linguagem natural 
                   com foco na classificação de consultas sobre dados de saúde. 
                   
                   Minha função é analisar cuidadosamente cada pergunta do usuário, 
                   identificar o tipo de informação solicitada e recomendar qual 
                   agente especializado está melhor preparado para responder. 
                   
                   Trabalho como o primeiro ponto de contato, garantindo que cada 
                   consulta seja direcionada ao especialista mais adequado, 
                   maximizando a qualidade e relevância das respostas."""),
        verbose=False,
        llm=llm,
        tools=[ferramenta_analisador],
        allow_delegation=True  # Pode delegar para outros agentes
    )
    
    print("✅ Agente Analisador criado!")
    return agente


def criar_agente_especialista_saude():
    """
    🏥 AGENTE EVOLUÍDO: Especialista em Dados de Saúde
    
    Versão aprimorada do agente da Aula 8, agora otimizado para
    trabalhar em equipe com outros agentes especializados.
    """
    
    print("🏥 Criando Agente Especialista em Dados de Saúde...")
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.2
    )
    
    ferramenta_saude = ConsultaSaudeAvancadaTool()
    
    agente = Agent(
        role="Especialista em Dados de Saúde",
        goal=("Fornecer informações detalhadas sobre estabelecimentos de saúde, "
              "queixas principais, sintomas e visões gerais do sistema, "
              "trabalhando em coordenação com outros agentes especializados"),
        backstory=("""Sou um especialista sênior em dados de saúde pública com 
                   mais de 15 anos de experiência em sistemas hospitalares. 
                   
                   Minha expertise inclui análise de estabelecimentos de saúde,
                   interpretação de padrões de queixas e sintomas, e fornecimento
                   de visões abrangentes sobre redes de atendimento.
                   
                   Trabalho em equipe com outros especialistas, focando nas
                   questões relacionadas a estabelecimentos, queixas médicas
                   e aspectos clínicos do sistema de saúde."""),
        verbose=False,
        llm=llm,
        tools=[ferramenta_saude]
    )
    
    print("✅ Agente Especialista em Saúde criado!")
    return agente


def criar_agente_estatistico():
    """
    📊 NOVO AGENTE: Especialista em Estatísticas e Análises
    
    Focado em análises numéricas, estatísticas avançadas e
    relatórios quantitativos sobre os dados de saúde.
    """
    
    print("📊 Criando Agente Especialista em Estatísticas...")
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1  # Precisão para cálculos estatísticos
    )
    
    ferramenta_saude = ConsultaSaudeAvancadaTool()
    
    agente = Agent(
        role="Especialista em Estatísticas de Saúde",
        goal=("Realizar análises estatísticas avançadas, gerar relatórios "
              "quantitativos e fornecer insights baseados em dados sobre "
              "distribuição geográfica e métricas do sistema de saúde"),
        backstory=("""Sou um estatístico especializado em dados de saúde pública 
                   com formação em epidemiologia e análise de dados.
                   
                   Minha expertise está em transformar dados brutos em insights
                   estatísticos meaningful, criar relatórios quantitativos
                   precisos e identificar padrões numéricos relevantes.
                   
                   Foco especificamente em análises geográficas, métricas de
                   performance do sistema de saúde e estatísticas descritivas
                   que ajudam na tomada de decisões."""),
        verbose=False,
        llm=llm,
        tools=[ferramenta_saude]
    )
    
    print("✅ Agente Especialista em Estatísticas criado!")
    return agente


# =============================================================================
# PARTE 3: SISTEMA MULTI-AGENTE COORDENADO
# =============================================================================

def criar_crew_multiagente():
    """
    👥 NOVA FUNCIONALIDADE: Crew com múltiplos agentes especializados
    
    Utiliza Process.hierarchical para coordenação inteligente entre agentes.
    """
    
    print("👥 Criando Crew Multi-Agente...")
    
    # Criar todos os agentes
    agente_analisador = criar_agente_analisador()
    agente_saude = criar_agente_especialista_saude()
    agente_estatistico = criar_agente_estatistico()
    
    # Configurar crew com processo hierarchical
    crew = Crew(
        agents=[agente_analisador, agente_saude, agente_estatistico],
        tasks=[],  # Tarefas serão criadas dinamicamente
        process=Process.hierarchical,  # NOVA: Processo hierárquico
        manager_llm=ChatOpenAI(model="gpt-4o-mini", temperature=0.2),
        verbose=False
    )
    
    print("✅ Crew Multi-Agente configurada!")
    return crew, agente_analisador, agente_saude, agente_estatistico


def executar_consulta_multiagente(crew: Crew, agentes: Tuple[Agent, Agent, Agent], pergunta: str) -> str:
    """
    🎯 NOVA FUNCIONALIDADE: Execução coordenada com múltiplos agentes
    
    1. Agente Analisador classifica a pergunta
    2. Sistema direciona para o agente apropriado
    3. Agente especializado responde
    4. Resultado coordenado é retornado
    """
    
    agente_analisador, agente_saude, agente_estatistico = agentes
    
    print(f"\n🧠 Analisando pergunta: '{pergunta}'")
    print("🔄 Iniciando processo multi-agente...")
    
    try:
        # ETAPA 1: Análise da consulta
        tarefa_analise = Task(
            description=f"""
            Analise esta pergunta do usuário sobre dados de saúde: "{pergunta}"
            
            Use a ferramenta analisador_consulta para:
            1. Classificar o tipo de consulta
            2. Determinar qual agente deve responder
            3. Fornecer análise detalhada
            
            Seja preciso na classificação para garantir que a pergunta
            seja direcionada ao agente mais especializado.
            """,
            agent=agente_analisador,
            expected_output=("Análise estruturada em JSON com tipo de consulta, "
                           "agente recomendado e justificativa detalhada")
        )
        
        # ETAPA 2: Criar tarefa para agente especializado baseado na análise
        # Por simplicidade, vamos inferir o tipo baseado nas palavras-chave
        pergunta_lower = pergunta.lower()
        
        if any(palavra in pergunta_lower for palavra in ['estatística', 'número', 'quantidade', 'total', 'ranking', 'bairro', 'distribuição']):
            agente_escolhido = agente_estatistico
            tipo_consulta = "estatisticas" if any(p in pergunta_lower for p in ['estatística', 'número', 'total']) else "geografico"
            nome_agente = "Agente Estatístico"
        else:
            agente_escolhido = agente_saude
            tipo_consulta = "estabelecimentos" if any(p in pergunta_lower for p in ['hospital', 'upa', 'posto']) else "visao_geral"
            nome_agente = "Especialista em Dados de Saúde"
        
        print(f"🎯 Direcionando para: {nome_agente}")
        
        tarefa_resposta = Task(
            description=f"""
            Responda à pergunta do usuário: "{pergunta}"
            
            Use a ferramenta consulta_saude_avancada com os parâmetros:
            - tipo_consulta: {tipo_consulta}
            - filtros: baseado na pergunta do usuário
            - limite: 15
            
            DIRETRIZES:
            - Forneça resposta completa e bem estruturada
            - Use formatação clara com emojis
            - Inclua insights relevantes baseados nos dados
            - Mencione que trabalha em equipe com outros especialistas
            - Se apropriado, sugira consultas relacionadas que outros agentes poderiam responder
            """,
            agent=agente_escolhido,
            expected_output=("Resposta detalhada e bem formatada com dados específicos, "
                           "insights relevantes e sugestões de consultas complementares")
        )
        
        # ETAPA 3: Executar as tarefas em sequência
        crew.tasks = [tarefa_analise, tarefa_resposta]
        resultado = crew.kickoff()
        
        return resultado.raw
        
    except Exception as e:
        return (f"❌ Erro no processo multi-agente: {str(e)}\n"
                f"💡 Tente reformular sua pergunta ou use o modo simplificado.")


# =============================================================================
# PARTE 4: INTERFACE INTERATIVA APRIMORADA
# =============================================================================

def mostrar_menu_multiagente():
    """📋 Menu aprimorado para sistema multi-agente"""
    
    print("\n" + "="*70)
    print("🤖 SISTEMA MULTI-AGENTE INTELIGENTE DE DADOS DE SAÚDE")
    print("="*70)
    print("Agora com 3 agentes especializados trabalhando em equipe!")
    print()
    print("🧠 **AGENTE ANALISADOR**: Classifica suas perguntas automaticamente")
    print("🏥 **ESPECIALISTA EM SAÚDE**: Estabelecimentos, queixas e visão geral")  
    print("📊 **ESPECIALISTA ESTATÍSTICO**: Análises numéricas e distribuição geográfica")
    print()
    print("💬 **EXEMPLOS DE PERGUNTAS:**")
    print("   🏥 'Quais hospitais atendem mais pacientes?'")
    print("   📊 'Mostre estatísticas por bairro'")
    print("   🏥 'Quais são as principais queixas?'") 
    print("   📊 'Qual a média de atendimentos por estabelecimento?'")
    print("   🏥 'Visão geral do sistema de saúde'")
    print("   📊 'Ranking dos bairros com mais atendimentos'")
    print()
    print("⌨️  **COMANDOS ESPECIAIS:**")
    print("   • 'ajuda' - Mostra este menu")
    print("   • 'agentes' - Informações sobre os agentes")
    print("   • 'demo' - Demonstração automática")
    print("   • 'sair' - Encerra o programa")
    print("="*70)


def mostrar_info_agentes():
    """ℹ️ Informações detalhadas sobre os agentes"""
    
    print("\n" + "="*60)
    print("🤖 INFORMAÇÕES DOS AGENTES ESPECIALIZADOS")
    print("="*60)
    
    print("🧠 **AGENTE ANALISADOR DE CONSULTAS:**")
    print("   • Função: Classifica automaticamente o tipo de pergunta")
    print("   • Especialidade: Processamento de linguagem natural")
    print("   • Decisão: Qual agente deve responder cada consulta")
    print()
    
    print("🏥 **ESPECIALISTA EM DADOS DE SAÚDE:**")
    print("   • Função: Informações sobre estabelecimentos e queixas")
    print("   • Especialidade: Sistemas hospitalares e atendimento")
    print("   • Foco: Hospitais, UPAs, postos, sintomas, visão geral")
    print()
    
    print("📊 **ESPECIALISTA EM ESTATÍSTICAS:**")
    print("   • Função: Análises numéricas e relatórios quantitativos")
    print("   • Especialidade: Estatísticas de saúde pública")
    print("   • Foco: Métricas, rankings, distribuição geográfica")
    print()
    
    print("🔄 **COORDENAÇÃO:**")
    print("   • Processo: Hierarchical (CrewAI)")
    print("   • Decisão: Automática baseada na pergunta")
    print("   • Colaboração: Agentes trabalham em equipe")
    print("="*60)


def processar_comando_multiagente(entrada: str, crew, agentes) -> bool:
    """
    ⚙️ Processamento de comandos especiais para sistema multi-agente
    
    Returns:
        bool: True se deve continuar, False se deve sair
    """
    
    entrada = entrada.lower().strip()
    
    if entrada in ['sair', 'quit', 'exit', 'q']:
        print("\n👋 Obrigado por usar o sistema multi-agente! Até mais!")
        return False
    
    elif entrada in ['ajuda', 'help', 'h']:
        mostrar_menu_multiagente()
        return True
    
    elif entrada in ['agentes', 'info', 'agents']:
        mostrar_info_agentes()
        return True
    
    elif entrada in ['demo', 'demonstracao']:
        executar_demo_multiagente(crew, agentes)
        return True
    
    elif entrada in ['limpar', 'clear', 'cls']:
        os.system('clear' if os.name == 'posix' else 'cls')
        mostrar_menu_multiagente()
        return True
    
    elif entrada == '':
        print("💭 Digite sua pergunta ou 'ajuda' para ver opções")
        return True
    
    return True  # Continuar processamento normal


def executar_demo_multiagente(crew: Crew, agentes: Tuple[Agent, Agent, Agent]):
    """🎬 Demonstração automática do sistema multi-agente"""
    
    print("\n🎬 DEMONSTRAÇÃO DO SISTEMA MULTI-AGENTE")
    print("="*50)
    print("Vou executar 4 consultas diferentes para mostrar")
    print("como cada agente especializado trabalha:")
    
    exemplos = [
        {
            "pergunta": "Quantos estabelecimentos existem no total?",
            "tipo": "📊 Estatística",
            "agente_esperado": "Estatístico"
        },
        {
            "pergunta": "Quais são os principais hospitais?", 
            "tipo": "🏥 Estabelecimentos",
            "agente_esperado": "Especialista em Saúde"
        },
        {
            "pergunta": "Mostre a distribuição por bairros",
            "tipo": "📊 Análise Geográfica", 
            "agente_esperado": "Estatístico"
        },
        {
            "pergunta": "Quais são as queixas mais comuns?",
            "tipo": "🏥 Dados Clínicos",
            "agente_esperado": "Especialista em Saúde"
        }
    ]
    
    for i, exemplo in enumerate(exemplos, 1):
        print(f"\n📝 EXEMPLO {i}/4: {exemplo['pergunta']}")
        print(f"🎯 Tipo: {exemplo['tipo']}")
        print(f"🤖 Agente esperado: {exemplo['agente_esperado']}")
        print("-" * 50)
        
        resposta = executar_consulta_multiagente(crew, agentes, exemplo['pergunta'])
        print(resposta)
        
        if i < len(exemplos):
            input("\n⏸️  Pressione ENTER para próximo exemplo...")
    
    print("\n🎉 Demonstração concluída!")
    print("💡 Agora faça suas próprias perguntas ao sistema!")


def sistema_multiagente_interativo():
    """🔄 Sistema principal multi-agente interativo"""
    
    # Verificar pré-requisitos
    if not DB_PATH.exists():
        print(f"❌ ERRO: Banco de dados não encontrado!")
        print(f"📁 Esperado em: {DB_PATH}")
        return
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ ERRO: OpenAI API Key não configurada!")
        return
    
    print("🔄 Iniciando sistema multi-agente...")
    
    # Criar crew e agentes
    crew, agente_analisador, agente_saude, agente_estatistico = criar_crew_multiagente()
    agentes = (agente_analisador, agente_saude, agente_estatistico)
    
    # Testar conexão
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
    
    # Mostrar menu
    mostrar_menu_multiagente()
    
    print("\n🚀 Sistema multi-agente pronto! Digite sua primeira pergunta:")
    
    # Loop principal
    while True:
        try:
            entrada = input("\n💬 Sua pergunta: ").strip()
            
            # Processar comandos especiais
            if not processar_comando_multiagente(entrada, crew, agentes):
                break
            
            # Pular entradas vazias ou comandos já processados
            if entrada.lower() in ['ajuda', 'help', 'agentes', 'info', 'demo', 'limpar', 'clear', 'cls', '']:
                continue
            
            # Executar consulta multi-agente
            print("\n" + "="*60)
            resposta = executar_consulta_multiagente(crew, agentes, entrada)
            print("\n📋 RESPOSTA DO SISTEMA MULTI-AGENTE:")
            print("-" * 40)
            print(resposta)
            print("="*60)
            
        except KeyboardInterrupt:
            print("\n\n⏹️ Interrompido pelo usuário. Finalizando...")
            break
            
        except Exception as e:
            print(f"\n❌ Erro inesperado: {str(e)}")
            print("💡 Tente novamente ou digite 'sair' para encerrar")


# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

def main():
    """Função principal da Aula 9"""
    
    print("\n🎯 ESCOLHA O MODO DE EXECUÇÃO:")
    print("1. 🤖 Sistema Multi-Agente Interativo (NOVO!)")
    print("2. 🎬 Demonstração Multi-Agente")
    print("3. ❌ Sair")
    
    while True:
        escolha = input("\nEscolha uma opção (1-3): ").strip()
        
        if escolha == '1':
            sistema_multiagente_interativo()
            break
        elif escolha == '2':
            print("🔄 Iniciando demonstração...")
            crew, agente_analisador, agente_saude, agente_estatistico = criar_crew_multiagente()
            agentes = (agente_analisador, agente_saude, agente_estatistico)
            executar_demo_multiagente(crew, agentes)
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