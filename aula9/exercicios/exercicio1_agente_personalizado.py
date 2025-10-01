#!/usr/bin/env python3
"""
🎓 EXERCÍCIO 1: Criando um 4º Agente Especializado - Agente Geográfico
======================================================================

OBJETIVO:
Adicionar um novo agente especializado ao sistema da Aula 9 que se foca
em análises geográficas e de localização dos estabelecimentos de saúde.

DESAFIO:
Implementar um "Agente Geográfico" que analisa:
- Distribuição geográfica de estabelecimentos
- Análise de cobertura por região
- Proximidade entre estabelecimentos
- Acessibilidade geográfica

EXECUÇÃO:
uv run aula9/exercicios/exercicio1_agente_personalizado.py

PRÉ-REQUISITOS:
1. Aula 9 funcionando: uv run aula9/main.py
2. Banco db/curso.db disponível
3. OpenAI API Key configurada
"""

import os
import sys
import sqlite3
from pathlib import Path
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI
import json
import math

# Configurações
load_dotenv()
PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "db" / "curso.db"

print("🎓 EXERCÍCIO 1: Agente Geográfico Especializado")
print("=" * 55)

# =============================================================================
# NOVA FERRAMENTA: GeograficoTool
# =============================================================================

class GeograficoTool(BaseTool):
    """
    🗺️ NOVA FERRAMENTA: Análises geográficas especializadas
    
    Focada em localização, proximidade e distribuição espacial
    dos estabelecimentos de saúde.
    """
    
    name: str = "geografico_tool"
    description: str = (
        "Realiza análises geográficas especializadas sobre estabelecimentos "
        "de saúde. Inclui distribuição por região, análise de proximidade, "
        "cobertura geográfica e acessibilidade por área."
    )
    
    def _run(self, tipo_analise: str = "distribuicao", filtro_regiao: str = "") -> str:
        """
        Executa análise geográfica específica
        
        Args:
            tipo_analise: Tipo de análise (distribuicao, proximidade, cobertura)
            filtro_regiao: Filtro opcional por região/bairro
        
        Returns:
            str: Análise geográfica formatada
        """
        
        try:
            if not DB_PATH.exists():
                return f"❌ Banco de dados não encontrado: {DB_PATH}"
            
            print(f"🗺️ Executando análise geográfica: {tipo_analise}")
            conn = sqlite3.connect(str(DB_PATH))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Roteamento por tipo de análise
            if tipo_analise == "distribuicao":
                resultado = self._analisar_distribuicao_regional(cursor, filtro_regiao)
            elif tipo_analise == "proximidade":
                resultado = self._analisar_proximidade(cursor, filtro_regiao)
            elif tipo_analise == "cobertura":
                resultado = self._analisar_cobertura_regional(cursor)
            elif tipo_analise == "acessibilidade":
                resultado = self._analisar_acessibilidade(cursor)
            else:
                resultado = self._analise_geografica_geral(cursor)
            
            conn.close()
            return resultado
            
        except Exception as erro:
            return f"❌ Erro na análise geográfica: {str(erro)}"
    
    def _analisar_distribuicao_regional(self, cursor, filtro_regiao: str) -> str:
        """Analisa distribuição de estabelecimentos por região"""
        
        where_clause = ""
        params = []
        
        if filtro_regiao:
            where_clause = "WHERE LOWER(e.bairro) LIKE LOWER(?)"
            params = [f"%{filtro_regiao}%"]
        
        query = f"""
            SELECT 
                e.bairro,
                COUNT(DISTINCT e.cnes) as num_estabelecimentos,
                COUNT(h.id) as total_atendimentos,
                ROUND(AVG(CASE WHEN h.id IS NOT NULL THEN 1.0 ELSE 0.0 END) * 100, 1) as taxa_utilizacao,
                GROUP_CONCAT(DISTINCT SUBSTR(e.nome, 1, 30)) as estabelecimentos_amostra
            FROM ia_estabelecimento e
            LEFT JOIN ia_historico_atendimento_sintoma h ON e.cnes = h.estabelecimento_cnes
            {where_clause}
            GROUP BY e.bairro
            HAVING e.bairro IS NOT NULL AND e.bairro != ''
            ORDER BY num_estabelecimentos DESC, total_atendimentos DESC
            LIMIT 15
        """
        
        cursor.execute(query, params)
        regioes = cursor.fetchall()
        
        resultado = f"🗺️ ANÁLISE DE DISTRIBUIÇÃO REGIONAL:\n\n"
        
        if filtro_regiao:
            resultado += f"🎯 **Filtro aplicado**: {filtro_regiao}\n\n"
        
        total_estabelecimentos = sum(r['num_estabelecimentos'] for r in regioes)
        total_atendimentos = sum(r['total_atendimentos'] for r in regioes)
        
        resultado += f"📊 **RESUMO GERAL**:\n"
        resultado += f"   🏥 Total de regiões analisadas: {len(regioes)}\n"
        resultado += f"   🏥 Total de estabelecimentos: {total_estabelecimentos}\n"
        resultado += f"   📋 Total de atendimentos: {total_atendimentos:,}\n\n"
        
        resultado += f"🏘️ **DISTRIBUIÇÃO POR REGIÃO**:\n\n"
        
        for i, regiao in enumerate(regioes, 1):
            percentual_estabelecimentos = (regiao['num_estabelecimentos'] / total_estabelecimentos * 100) if total_estabelecimentos > 0 else 0
            
            resultado += f"{i}. **{regiao['bairro']}**\n"
            resultado += f"   🏥 Estabelecimentos: {regiao['num_estabelecimentos']} ({percentual_estabelecimentos:.1f}% do total)\n"
            resultado += f"   📊 Atendimentos: {regiao['total_atendimentos']:,}\n"
            resultado += f"   📈 Taxa de utilização: {regiao['taxa_utilizacao']}%\n"
            
            # Mostrar amostra de estabelecimentos
            if regiao['estabelecimentos_amostra']:
                estabelecimentos = regiao['estabelecimentos_amostra'].split(',')[:2]
                resultado += f"   🏥 Principais: {', '.join(estabelecimentos)}\n"
                if len(regiao['estabelecimentos_amostra'].split(',')) > 2:
                    resultado += f"       (e mais {len(regiao['estabelecimentos_amostra'].split(',')) - 2})\n"
            
            resultado += "\n"
        
        return resultado
    
    def _analisar_proximidade(self, cursor, filtro_regiao: str) -> str:
        """Analisa proximidade entre estabelecimentos"""
        
        # Buscar estabelecimentos com suas localizações
        cursor.execute("""
            SELECT cnes, nome, endereco, bairro
            FROM ia_estabelecimento
            WHERE bairro IS NOT NULL AND bairro != ''
            ORDER BY bairro, nome
        """)
        
        estabelecimentos = cursor.fetchall()
        
        resultado = f"🗺️ ANÁLISE DE PROXIMIDADE:\n\n"
        
        # Agrupar por bairro para análise de proximidade
        bairros_estabelecimentos = {}
        for est in estabelecimentos:
            bairro = est['bairro']
            if bairro not in bairros_estabelecimentos:
                bairros_estabelecimentos[bairro] = []
            bairros_estabelecimentos[bairro].append(est)
        
        resultado += f"📊 **CONCENTRAÇÃO POR BAIRRO**:\n\n"
        
        # Analisar concentração por bairro
        bairros_ordenados = sorted(bairros_estabelecimentos.items(), 
                                 key=lambda x: len(x[1]), reverse=True)
        
        for bairro, estabelecimentos_bairro in bairros_ordenados[:10]:
            resultado += f"🏘️ **{bairro}**\n"
            resultado += f"   🏥 Quantidade: {len(estabelecimentos_bairro)} estabelecimentos\n"
            
            if len(estabelecimentos_bairro) > 1:
                resultado += f"   📍 Concentração: ALTA (múltiplos estabelecimentos)\n"
                resultado += f"   🔄 Redundância: Pode haver sobreposição de serviços\n"
            else:
                resultado += f"   📍 Concentração: BAIXA (estabelecimento único)\n"
                resultado += f"   🎯 Cobertura: Atende região específica\n"
            
            # Listar estabelecimentos do bairro
            for est in estabelecimentos_bairro[:3]:  # Mostrar apenas 3 primeiros
                resultado += f"   • {est['nome'][:40]}...\n"
            
            if len(estabelecimentos_bairro) > 3:
                resultado += f"   • (e mais {len(estabelecimentos_bairro) - 3} estabelecimentos)\n"
            
            resultado += "\n"
        
        # Análise de bairros sem cobertura (se aplicável)
        resultado += f"🔍 **ANÁLISE DE COBERTURA**:\n"
        resultado += f"   🏥 Bairros com estabelecimentos: {len(bairros_estabelecimentos)}\n"
        resultado += f"   📊 Média por bairro: {len(estabelecimentos) / len(bairros_estabelecimentos):.1f} estabelecimentos\n"
        
        # Identificar bairros com mais/menos estabelecimentos
        bairro_mais_estabelecimentos = max(bairros_estabelecimentos.items(), key=lambda x: len(x[1]))
        
        resultado += f"   🏆 Maior concentração: {bairro_mais_estabelecimentos[0]} ({len(bairro_mais_estabelecimentos[1])} estabelecimentos)\n"
        
        return resultado
    
    def _analisar_cobertura_regional(self, cursor) -> str:
        """Analisa cobertura geográfica geral"""
        
        # Análise de cobertura por tipos de estabelecimento
        cursor.execute("""
            SELECT 
                CASE 
                    WHEN UPPER(nome) LIKE '%HOSPITAL%' THEN 'Hospital'
                    WHEN UPPER(nome) LIKE '%UPA%' THEN 'UPA'
                    WHEN UPPER(nome) LIKE '%POSTO%' OR UPPER(nome) LIKE '%PSF%' THEN 'Posto de Saúde'
                    WHEN UPPER(nome) LIKE '%CLINICA%' THEN 'Clínica'
                    ELSE 'Outros'
                END as tipo_estabelecimento,
                bairro,
                COUNT(*) as quantidade
            FROM ia_estabelecimento
            WHERE bairro IS NOT NULL AND bairro != ''
            GROUP BY tipo_estabelecimento, bairro
            ORDER BY tipo_estabelecimento, quantidade DESC
        """)
        
        cobertura = cursor.fetchall()
        
        resultado = f"🗺️ ANÁLISE DE COBERTURA REGIONAL:\n\n"
        
        # Agrupar por tipo de estabelecimento
        tipos_cobertura = {}
        for item in cobertura:
            tipo = item['tipo_estabelecimento']
            if tipo not in tipos_cobertura:
                tipos_cobertura[tipo] = []
            tipos_cobertura[tipo].append(item)
        
        resultado += f"🏥 **COBERTURA POR TIPO DE ESTABELECIMENTO**:\n\n"
        
        for tipo, dados in tipos_cobertura.items():
            total_estabelecimentos = sum(d['quantidade'] for d in dados)
            total_bairros = len(dados)
            
            resultado += f"🏥 **{tipo}**:\n"
            resultado += f"   📊 Total: {total_estabelecimentos} estabelecimentos\n"
            resultado += f"   🏘️ Presente em: {total_bairros} bairros\n"
            resultado += f"   📈 Média por bairro: {total_estabelecimentos/total_bairros:.1f}\n"
            
            # Top 3 bairros para este tipo
            top_bairros = sorted(dados, key=lambda x: x['quantidade'], reverse=True)[:3]
            resultado += f"   🏆 Principais locais:\n"
            for i, bairro in enumerate(top_bairros, 1):
                resultado += f"      {i}. {bairro['bairro']} ({bairro['quantidade']} unidades)\n"
            
            resultado += "\n"
        
        # Análise de gaps de cobertura
        resultado += f"🔍 **ANÁLISE DE GAPS DE COBERTURA**:\n\n"
        
        # Identificar tipos com menor cobertura
        tipos_ordenados = sorted(tipos_cobertura.items(), 
                               key=lambda x: sum(d['quantidade'] for d in x[1]))
        
        tipo_menor_cobertura = tipos_ordenados[0]
        resultado += f"⚠️ **Menor cobertura**: {tipo_menor_cobertura[0]}\n"
        resultado += f"   📊 Apenas {sum(d['quantidade'] for d in tipo_menor_cobertura[1])} estabelecimentos\n"
        resultado += f"   🎯 Oportunidade de expansão identificada\n\n"
        
        tipo_maior_cobertura = tipos_ordenados[-1]
        resultado += f"✅ **Melhor cobertura**: {tipo_maior_cobertura[0]}\n"
        resultado += f"   📊 Total de {sum(d['quantidade'] for d in tipo_maior_cobertura[1])} estabelecimentos\n"
        resultado += f"   🏆 Boa distribuição regional\n"
        
        return resultado
    
    def _analisar_acessibilidade(self, cursor) -> str:
        """Analisa acessibilidade geográfica"""
        
        # Análise de acessibilidade baseada em distribuição e volume
        cursor.execute("""
            SELECT 
                e.bairro,
                COUNT(DISTINCT e.cnes) as num_estabelecimentos,
                COUNT(h.id) as total_atendimentos,
                COUNT(DISTINCT h.queixa_principal_id) as tipos_queixas,
                ROUND(COUNT(h.id) * 1.0 / COUNT(DISTINCT e.cnes), 1) as atendimentos_por_estabelecimento
            FROM ia_estabelecimento e
            LEFT JOIN ia_historico_atendimento_sintoma h ON e.cnes = h.estabelecimento_cnes
            WHERE e.bairro IS NOT NULL AND e.bairro != ''
            GROUP BY e.bairro
            ORDER BY atendimentos_por_estabelecimento DESC
        """)
        
        acessibilidade = cursor.fetchall()
        
        resultado = f"🗺️ ANÁLISE DE ACESSIBILIDADE:\n\n"
        
        # Calcular métricas de acessibilidade
        total_regioes = len(acessibilidade)
        media_atendimentos = sum(a['total_atendimentos'] for a in acessibilidade) / total_regioes if total_regioes > 0 else 0
        
        resultado += f"📊 **MÉTRICAS GERAIS DE ACESSIBILIDADE**:\n"
        resultado += f"   🏘️ Regiões analisadas: {total_regioes}\n"
        resultado += f"   📈 Média de atendimentos por região: {media_atendimentos:.1f}\n\n"
        
        # Classificar acessibilidade
        resultado += f"🎯 **CLASSIFICAÇÃO DE ACESSIBILIDADE**:\n\n"
        
        alta_acessibilidade = [a for a in acessibilidade if a['atendimentos_por_estabelecimento'] > media_atendimentos]
        baixa_acessibilidade = [a for a in acessibilidade if a['atendimentos_por_estabelecimento'] <= media_atendimentos]
        
        resultado += f"✅ **ALTA ACESSIBILIDADE** ({len(alta_acessibilidade)} regiões):\n"
        for regiao in alta_acessibilidade[:5]:
            resultado += f"   🏥 {regiao['bairro']}: {regiao['atendimentos_por_estabelecimento']} atendimentos/estabelecimento\n"
            resultado += f"      📊 {regiao['num_estabelecimentos']} estabelecimentos, {regiao['total_atendimentos']:,} atendimentos\n"
        
        if len(alta_acessibilidade) > 5:
            resultado += f"   ... e mais {len(alta_acessibilidade) - 5} regiões\n"
        
        resultado += f"\n⚠️ **BAIXA ACESSIBILIDADE** ({len(baixa_acessibilidade)} regiões):\n"
        for regiao in sorted(baixa_acessibilidade, key=lambda x: x['atendimentos_por_estabelecimento'])[:5]:
            resultado += f"   🔴 {regiao['bairro']}: {regiao['atendimentos_por_estabelecimento']} atendimentos/estabelecimento\n"
            resultado += f"      📊 {regiao['num_estabelecimentos']} estabelecimentos, {regiao['total_atendimentos']:,} atendimentos\n"
        
        # Recomendações
        resultado += f"\n💡 **RECOMENDAÇÕES PARA MELHORIA**:\n"
        resultado += f"   🎯 Focar nas {len(baixa_acessibilidade)} regiões de baixa acessibilidade\n"
        resultado += f"   🏥 Considerar novos estabelecimentos em áreas carentes\n"
        resultado += f"   📊 Redistribuir recursos para equilibrar atendimento\n"
        
        return resultado
    
    def _analise_geografica_geral(self, cursor) -> str:
        """Análise geográfica geral/overview"""
        
        resultado = f"🗺️ ANÁLISE GEOGRÁFICA GERAL:\n\n"
        
        # Estatísticas gerais
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT bairro) as total_bairros,
                COUNT(DISTINCT cnes) as total_estabelecimentos,
                ROUND(COUNT(DISTINCT cnes) * 1.0 / COUNT(DISTINCT bairro), 2) as estabelecimentos_por_bairro
            FROM ia_estabelecimento
            WHERE bairro IS NOT NULL AND bairro != ''
        """)
        
        stats = cursor.fetchone()
        
        resultado += f"📊 **ESTATÍSTICAS GEOGRÁFICAS**:\n"
        resultado += f"   🏘️ Total de bairros cobertos: {stats['total_bairros']}\n"
        resultado += f"   🏥 Total de estabelecimentos: {stats['total_estabelecimentos']}\n"
        resultado += f"   📈 Média por bairro: {stats['estabelecimentos_por_bairro']} estabelecimentos\n\n"
        
        # Top bairros por número de estabelecimentos
        cursor.execute("""
            SELECT bairro, COUNT(*) as num_estabelecimentos
            FROM ia_estabelecimento
            WHERE bairro IS NOT NULL AND bairro != ''
            GROUP BY bairro
            ORDER BY num_estabelecimentos DESC
            LIMIT 5
        """)
        
        top_bairros = cursor.fetchall()
        
        resultado += f"🏆 **TOP 5 BAIRROS (por número de estabelecimentos)**:\n"
        for i, bairro in enumerate(top_bairros, 1):
            resultado += f"   {i}. {bairro['bairro']}: {bairro['num_estabelecimentos']} estabelecimentos\n"
        
        # Resumo de tipos de análise disponíveis
        resultado += f"\n🔧 **TIPOS DE ANÁLISE DISPONÍVEIS**:\n"
        resultado += f"   📊 'distribuicao' - Distribuição regional detalhada\n"
        resultado += f"   🗺️ 'proximidade' - Análise de proximidade e concentração\n"
        resultado += f"   📍 'cobertura' - Cobertura por tipo de estabelecimento\n"
        resultado += f"   🎯 'acessibilidade' - Análise de acessibilidade regional\n"
        
        return resultado


# =============================================================================
# NOVO AGENTE: Especialista Geográfico
# =============================================================================

def criar_agente_geografico():
    """
    🗺️ NOVO AGENTE: Especialista em Análises Geográficas
    
    Focado em localização, distribuição espacial e acessibilidade
    dos estabelecimentos de saúde.
    """
    
    print("🗺️ Criando Agente Especialista Geográfico...")
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1  # Precisão para análises geográficas
    )
    
    ferramenta_geografica = GeograficoTool()
    
    agente = Agent(
        role="Especialista em Análises Geográficas de Saúde",
        goal=("Fornecer análises geográficas especializadas sobre distribuição, "
              "proximidade, cobertura e acessibilidade dos estabelecimentos "
              "de saúde, ajudando na compreensão espacial da rede de atendimento"),
        backstory=("""Sou um geógrafo especializado em saúde pública com expertise 
                   em análise espacial e planejamento territorial de serviços de saúde.
                   
                   Minha formação combina geografia, epidemiologia e planejamento urbano,
                   permitindo analisar a distribuição espacial de estabelecimentos,
                   identificar gaps de cobertura e avaliar acessibilidade geográfica.
                   
                   Trabalho com análises de proximidade, distribuição regional,
                   cobertura territorial e estudos de acessibilidade para otimizar
                   a localização e eficiência da rede de saúde."""),
        verbose=False,
        llm=llm,
        tools=[ferramenta_geografica]
    )
    
    print("✅ Agente Especialista Geográfico criado!")
    return agente


# =============================================================================
# SISTEMA MULTI-AGENTE EXPANDIDO (4 AGENTES)
# =============================================================================

def criar_classificador_expandido():
    """Atualiza o classificador para incluir análises geográficas"""
    
    # Palavras-chave para o novo agente geográfico
    palavras_geograficas = [
        "bairro", "região", "localização", "proximidade", "distância",
        "distribuição", "cobertura", "acessibilidade", "territorial",
        "espacial", "geográfico", "mapa", "área", "zona"
    ]
    
    return {
        "geografico": {
            "palavras": palavras_geograficas,
            "agente_recomendado": "Especialista Geográfico",
            "confidence_boost": 1.2  # Boost para análises geográficas claras
        }
    }


def executar_consulta_4_agentes(pergunta: str):
    """
    Executa consulta com sistema expandido de 4 agentes
    """
    
    print(f"🧠 Analisando pergunta: '{pergunta}'")
    print("🔄 Sistema com 4 agentes especializados...")
    
    # Análise simples de classificação
    pergunta_lower = pergunta.lower()
    classificador = criar_classificador_expandido()
    
    # Verificar se é consulta geográfica
    if any(palavra in pergunta_lower for palavra in classificador["geografico"]["palavras"]):
        agente_escolhido = criar_agente_geografico()
        tipo_analise = "geografico"
        nome_agente = "Especialista Geográfico"
        
        # Determinar subtipo de análise geográfica
        if any(p in pergunta_lower for p in ["distribuição", "distribuir", "regional"]):
            subtipo = "distribuicao"
        elif any(p in pergunta_lower for p in ["proximidade", "próximo", "distância"]):
            subtipo = "proximidade"
        elif any(p in pergunta_lower for p in ["cobertura", "cobrir", "alcance"]):
            subtipo = "cobertura"
        elif any(p in pergunta_lower for p in ["acessibilidade", "acesso", "acessível"]):
            subtipo = "acessibilidade"
        else:
            subtipo = "geral"
            
    else:
        # Fallback para sistema original (simplificado)
        print("🔄 Usando agente geográfico como demonstração...")
        agente_escolhido = criar_agente_geografico()
        subtipo = "geral"
        nome_agente = "Especialista Geográfico"
    
    print(f"🎯 Direcionando para: {nome_agente}")
    print(f"📊 Tipo de análise: {subtipo}")
    
    # Criar tarefa especializada
    tarefa = Task(
        description=f"""
        Responda à pergunta do usuário: "{pergunta}"
        
        Use a ferramenta geografico_tool com os parâmetros:
        - tipo_analise: {subtipo}
        - filtro_regiao: extrair da pergunta se houver
        
        DIRETRIZES:
        - Forneça análise geográfica detalhada e especializada
        - Use formatação clara com emojis
        - Inclua insights espaciais relevantes
        - Mencione implicações para planejamento de saúde
        - Sugira análises complementares quando apropriado
        """,
        agent=agente_escolhido,
        expected_output=("Análise geográfica detalhada com insights espaciais, "
                        "métricas de distribuição e recomendações para "
                        "planejamento territorial da saúde")
    )
    
    # Executar com crew simples
    crew = Crew(
        agents=[agente_escolhido],
        tasks=[tarefa],
        process=Process.sequential,
        verbose=False
    )
    
    try:
        resultado = crew.kickoff()
        return resultado.raw
    except Exception as e:
        return (f"❌ Erro no agente geográfico: {str(e)}\n"
                f"💡 Tente reformular sua pergunta com foco geográfico.")


# =============================================================================
# INTERFACE DE DEMONSTRAÇÃO
# =============================================================================

def demonstrar_agente_geografico():
    """Demonstração do novo agente geográfico"""
    
    print("\n🎬 DEMONSTRAÇÃO DO AGENTE GEOGRÁFICO")
    print("=" * 50)
    
    exemplos_geograficos = [
        {
            "pergunta": "Como estão distribuídos os estabelecimentos por região?",
            "tipo": "🗺️ Distribuição Regional"
        },
        {
            "pergunta": "Analise a proximidade entre estabelecimentos",
            "tipo": "📍 Análise de Proximidade"
        },
        {
            "pergunta": "Mostre a cobertura geográfica por tipo de estabelecimento",
            "tipo": "📊 Cobertura Regional"
        },
        {
            "pergunta": "Qual a acessibilidade dos serviços de saúde?",
            "tipo": "🎯 Análise de Acessibilidade"
        }
    ]
    
    for i, exemplo in enumerate(exemplos_geograficos, 1):
        print(f"\n📝 EXEMPLO {i}/4: {exemplo['pergunta']}")
        print(f"🎯 Tipo: {exemplo['tipo']}")
        print("-" * 50)
        
        resposta = executar_consulta_4_agentes(exemplo['pergunta'])
        print(resposta)
        
        if i < len(exemplos_geograficos):
            input("\n⏸️  Pressione ENTER para próximo exemplo...")
    
    print("\n🎉 Demonstração do Agente Geográfico concluída!")
    print("💡 Agora teste suas próprias perguntas geográficas!")


def modo_interativo_geografico():
    """Modo interativo focado no agente geográfico"""
    
    if not DB_PATH.exists():
        print(f"❌ Banco de dados não encontrado: {DB_PATH}")
        return
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OpenAI API Key não configurada!")
        return
    
    print("\n🗺️ MODO INTERATIVO - AGENTE GEOGRÁFICO")
    print("=" * 50)
    print("Faça perguntas sobre aspectos geográficos dos estabelecimentos!")
    print("\n💬 EXEMPLOS:")
    print("   • 'Distribuição de hospitais por bairro'")
    print("   • 'Proximidade entre UPAs'")
    print("   • 'Cobertura geográfica de postos de saúde'")
    print("   • 'Acessibilidade no centro da cidade'")
    print("\n⌨️ COMANDOS: 'demo', 'sair'")
    print("=" * 50)
    
    while True:
        try:
            entrada = input("\n🗺️ Pergunta geográfica: ").strip()
            
            if entrada.lower() in ['sair', 'quit', 'exit']:
                print("\n👋 Encerrando modo geográfico!")
                break
            elif entrada.lower() == 'demo':
                demonstrar_agente_geografico()
                continue
            elif not entrada:
                print("💭 Digite uma pergunta sobre aspectos geográficos")
                continue
            
            print("\n" + "=" * 60)
            resposta = executar_consulta_4_agentes(entrada)
            print("\n📋 RESPOSTA DO AGENTE GEOGRÁFICO:")
            print("-" * 40)
            print(resposta)
            print("=" * 60)
            
        except KeyboardInterrupt:
            print("\n\n⏹️ Interrompido. Finalizando...")
            break
        except Exception as e:
            print(f"\n❌ Erro: {str(e)}")


# =============================================================================
# FUNÇÃO PRINCIPAL DO EXERCÍCIO
# =============================================================================

def main():
    """Função principal do Exercício 1"""
    
    print("\n🎯 EXERCÍCIO 1: AGENTE GEOGRÁFICO ESPECIALIZADO")
    print("1. 🎬 Demonstração do Agente Geográfico")
    print("2. 🗺️ Modo Interativo Geográfico")  
    print("3. 🧪 Teste de Ferramenta Isolada")
    print("4. ❌ Sair")
    
    while True:
        escolha = input("\nEscolha uma opção (1-4): ").strip()
        
        if escolha == '1':
            demonstrar_agente_geografico()
            break
        elif escolha == '2':
            modo_interativo_geografico()
            break
        elif escolha == '3':
            # Teste da ferramenta isolada
            print("\n🧪 Testando GeograficoTool isoladamente...")
            tool = GeograficoTool()
            resultado = tool._run("distribuicao", "")
            print(resultado)
            break
        elif escolha == '4':
            print("👋 Finalizando exercício!")
            break
        else:
            print("⚠️ Opção inválida. Escolha 1, 2, 3 ou 4.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Exercício interrompido. Até mais!")
    except Exception as e:
        print(f"\n❌ Erro no exercício: {str(e)}")
        print("\n💡 VERIFICAÇÕES:")
        print("   • Banco db/curso.db existe?")
        print("   • OpenAI API Key configurada?")
        print("   • Dependências instaladas com uv sync?")