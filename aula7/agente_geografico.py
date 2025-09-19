"""
Agente Geográfico - Especialista em Geolocalização Médica
=========================================================

Este agente é especializado em buscar estabelecimentos de saúde
baseado em localização geográfica e calcular distâncias.

Funcionalidades:
- Calcular distâncias entre coordenadas (fórmula de Haversine)
- Buscar estabelecimentos próximos por tipo
- Filtrar por raio de busca
- Recomendar baseado em urgência médica
"""

from crewai import Agent
from crewai_tools import BaseTool
from langchain_openai import ChatOpenAI
from dados_simulados import dados_medicos
import math


class BuscaGeograficaTool(BaseTool):
    """Ferramenta especializada em busca geográfica de estabelecimentos"""
    
    name: str = "busca_geografica"
    description: str = (
        "Busca estabelecimentos de saúde próximos por coordenadas e tipo. "
        "Parâmetros: latitude, longitude, raio_km, tipo_estabelecimento"
    )
    
    def _run(self, latitude: float, longitude: float, 
             raio_km: float = 10, tipo_estabelecimento: str = None) -> str:
        """Executa busca geográfica otimizada"""
        
        # Buscar estabelecimentos
        estabelecimentos = dados_medicos.buscar_estabelecimentos_proximos(
            latitude, longitude, raio_km, tipo_estabelecimento
        )
        
        if not estabelecimentos:
            return (f"❌ Nenhum estabelecimento encontrado em um raio de "
                   f"{raio_km}km da coordenada ({latitude}, {longitude})")
        
        # Formatar resultado detalhado
        resultado = f"🌍 BUSCA GEOGRÁFICA - Raio: {raio_km}km\n"
        resultado += f"📍 Coordenadas de referência: ({latitude}, {longitude})\n"
        
        if tipo_estabelecimento:
            resultado += f"🏥 Tipo filtrado: {tipo_estabelecimento}\n"
        
        resultado += f"\n✅ {len(estabelecimentos)} estabelecimento(s) encontrado(s):\n\n"
        
        for i, est in enumerate(estabelecimentos, 1):
            # Emoji por tipo
            emoji_tipo = {
                'HOSPITAL': '🏥',
                'UPA': '🚑',
                'UBS': '⚕️'
            }.get(est['tipo'], '🏢')
            
            resultado += f"{i}. {emoji_tipo} {est['nome']}\n"
            resultado += f"   📊 Tipo: {est['tipo']}\n"
            resultado += f"   📏 Distância: {est['distancia_km']}km\n"
            resultado += f"   🏙️ Município: {est['municipio']}\n"
            resultado += f"   📞 Telefone: {est['telefone']}\n"
            resultado += f"   ⏰ Funcionamento: {est['horario_funcionamento']}\n"
            resultado += f"   📍 Coordenadas: ({est['latitude']}, {est['longitude']})\n\n"
        
        return resultado


class CalculoDistanciaTool(BaseTool):
    """Ferramenta para cálculos precisos de distância"""
    
    name: str = "calculo_distancia"
    description: str = (
        "Calcula distância exata entre duas coordenadas geográficas. "
        "Parâmetros: lat1, lng1, lat2, lng2"
    )
    
    def _run(self, lat1: float, lng1: float, lat2: float, lng2: float) -> str:
        """Calcula distância usando fórmula de Haversine"""
        
        distancia = dados_medicos.calcular_distancia(lat1, lng1, lat2, lng2)
        
        resultado = f"📏 CÁLCULO DE DISTÂNCIA\n"
        resultado += f"📍 Origem: ({lat1}, {lng1})\n"
        resultado += f"📍 Destino: ({lat2}, {lng2})\n"
        resultado += f"📏 Distância: {distancia:.2f}km\n"
        
        # Classificações de distância
        if distancia <= 2:
            classe = "🟢 MUITO PRÓXIMO"
        elif distancia <= 5:
            classe = "🟡 PRÓXIMO"
        elif distancia <= 15:
            classe = "🟠 MODERADO"
        else:
            classe = "🔴 DISTANTE"
        
        resultado += f"📊 Classificação: {classe}\n"
        
        return resultado


class RecomendacaoUrgenciaTool(BaseTool):
    """Ferramenta que recomenda tipo de estabelecimento baseado em urgência"""
    
    name: str = "recomendacao_urgencia"
    description: str = (
        "Recomenda tipo de estabelecimento baseado no nível de urgência médica. "
        "Parâmetro: nivel_urgencia (1-5)"
    )
    
    def _run(self, nivel_urgencia: int) -> str:
        """Gera recomendação baseada em protocolos médicos"""
        
        if nivel_urgencia >= 5:
            tipo_recomendado = "HOSPITAL"
            urgencia_desc = "EMERGÊNCIA MÁXIMA"
            orientacao = "Procure IMEDIATAMENTE um hospital ou chame SAMU (192)"
            emoji = "🚨"
        elif nivel_urgencia >= 4:
            tipo_recomendado = "UPA ou HOSPITAL"
            urgencia_desc = "URGENTE"
            orientacao = "Procure UPA ou hospital rapidamente"
            emoji = "⚠️"
        elif nivel_urgencia >= 3:
            tipo_recomendado = "UPA"
            urgencia_desc = "MODERADO"
            orientacao = "Procure UPA ou agende consulta médica"
            emoji = "🟡"
        elif nivel_urgencia >= 2:
            tipo_recomendado = "UBS"
            urgencia_desc = "LEVE"
            orientacao = "Procure UBS ou agende consulta"
            emoji = "🟢"
        else:
            tipo_recomendado = "UBS"
            urgencia_desc = "NÃO URGENTE"
            orientacao = "Consulta de rotina em UBS"
            emoji = "ℹ️"
        
        resultado = f"{emoji} RECOMENDAÇÃO POR URGÊNCIA\n"
        resultado += f"📊 Nível: {nivel_urgencia}/5 - {urgencia_desc}\n"
        resultado += f"🏥 Tipo recomendado: {tipo_recomendado}\n"
        resultado += f"💡 Orientação: {orientacao}\n"
        
        return resultado


def criar_agente_geografico(llm: ChatOpenAI = None) -> Agent:
    """
    Cria agente especializado em geolocalização médica
    
    Args:
        llm: Modelo de linguagem (opcional)
        
    Returns:
        Agent configurado para busca geográfica
    """
    
    if llm is None:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    
    return Agent(
        role="Especialista em Geolocalização Médica",
        goal="Encontrar os estabelecimentos de saúde mais próximos e adequados",
        backstory="""
        Sou um especialista em sistemas de geolocalização médica com conhecimento 
        detalhado da rede de saúde do Piauí. Minha especialidade é:
        
        🎯 EXPERTISE:
        • Cálculos precisos de distância geográfica
        • Conhecimento da rede hospitalar regional
        • Otimização de rotas para emergências médicas
        • Classificação de estabelecimentos por capacidade
        
        🌟 DIFERENCIAIS:
        • Considero sempre o nível de urgência do caso
        • Priorizo proximidade para emergências
        • Conheço horários de funcionamento
        • Recomendo alternativas quando necessário
        
        Minha missão é garantir que pacientes encontrem o atendimento adequado
        no menor tempo possível, considerando distância, tipo de estabelecimento
        e nível de urgência médica.
        """,
        tools=[
            BuscaGeograficaTool(),
            CalculoDistanciaTool(), 
            RecomendacaoUrgenciaTool()
        ],
        llm=llm,
        verbose=True
    )


# Exemplo de uso do agente geográfico
def exemplo_agente_geografico():
    """Demonstra uso do agente geográfico"""
    
    from crewai import Task, Crew, Process
    
    print("🌍 EXEMPLO: AGENTE GEOGRÁFICO MÉDICO")
    print("="*45)
    
    # Criar agente
    agente = criar_agente_geografico()
    
    # Cenários de teste
    cenarios = [
        {
            'nome': 'Emergência no Centro de Teresina',
            'tarefa': """
            SITUAÇÃO: Paciente com dor no peito intensa no centro de Teresina.
            Coordenadas: Latitude -5.0892, Longitude -42.8019
            
            SOLICITAÇÃO:
            1. Classifique como nível de urgência 5 (emergência máxima)
            2. Busque estabelecimentos apropriados num raio de 5km
            3. Calcule distâncias exatas para os 3 mais próximos
            4. Forneça recomendação baseada na urgência
            
            PRIORIZE: Hospitais e UPAs com atendimento 24h
            """
        },
        {
            'nome': 'Consulta de Rotina na Zona Norte',
            'tarefa': """
            SITUAÇÃO: Paciente precisa de consulta de rotina na zona norte.
            Coordenadas: Latitude -5.0500, Longitude -42.8200
            
            SOLICITAÇÃO:
            1. Classifique como nível de urgência 1 (não urgente)
            2. Busque UBS num raio de 3km
            3. Inclua informações de horário de funcionamento
            4. Recomende agendamento
            """
        }
    ]
    
    for i, cenario in enumerate(cenarios, 1):
        print(f"\n🎯 CENÁRIO {i}: {cenario['nome']}")
        print("-" * 50)
        
        # Criar tarefa
        tarefa = Task(
            description=cenario['tarefa'],
            agent=agente,
            expected_output="Relatório detalhado com análise geográfica e recomendações específicas"
        )
        
        # Executar
        crew = Crew(
            agents=[agente],
            tasks=[tarefa],
            process=Process.sequential,
            verbose=False
        )
        
        resultado = crew.kickoff()
        print(f"📋 RESULTADO:\n{resultado.raw}")
        print("\n" + "="*50)


if __name__ == "__main__":
    exemplo_agente_geografico()