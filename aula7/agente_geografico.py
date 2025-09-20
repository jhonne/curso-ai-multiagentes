"""
Agente Geográfico Avançado - Especialista em Geolocalização Médica
=================================================================

Este agente utiliza PostgreSQL + PostGIS para busca geográfica avançada:

Funcionalidades Modernas:
- Busca geográfica otimizada com PostGIS
- Índices espaciais para performance
- Cálculos precisos de distância em banco
- Recomendações inteligentes baseadas em urgência
- Integração com dados médicos reais

Substitui completamente o sistema simulado anterior.
"""

from crewai import Agent
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI

try:
    from .dados_medicos_reais import dados_medicos
except ImportError:
    from dados_medicos_reais import dados_medicos


class BuscaGeograficaAvancadaTool(BaseTool):
    """Ferramenta avançada para busca geográfica com PostgreSQL + PostGIS"""
    
    name: str = "busca_geografica_avancada"
    description: str = (
        "Busca estabelecimentos usando PostgreSQL com índices espaciais. "
        "Parâmetros: latitude, longitude, raio_km, tipo_estabelecimento"
    )
    
    def _run(self, latitude: float, longitude: float,
             raio_km: float = 10, tipo_estabelecimento: str = None) -> str:
        """Executa busca geográfica otimizada com PostgreSQL"""
        
        # Buscar estabelecimentos usando PostgreSQL + PostGIS
        estabelecimentos = dados_medicos.buscar_estabelecimentos_proximos(
            latitude, longitude, raio_km, tipo_estabelecimento
        )
        
        if not estabelecimentos:
            resultado = f"❌ BUSCA SEM RESULTADOS\n"
            resultado += f"📍 Local: ({latitude}, {longitude})\n"
            resultado += f"🔍 Raio: {raio_km}km\n"
            if tipo_estabelecimento:
                resultado += f"🏥 Tipo: {tipo_estabelecimento}\n"
            resultado += "\n💡 Sugestões:\n"
            resultado += "• Aumentar raio de busca\n"
            resultado += "• Remover filtro de tipo\n"
            resultado += "• Verificar coordenadas\n"
            return resultado
        
        # Formatar resultado detalhado
        resultado = f"🌍 BUSCA GEOGRÁFICA AVANÇADA\n"
        resultado += "=" * 35 + "\n\n"
        resultado += f"📍 Referência: ({latitude}, {longitude})\n"
        resultado += f"🔍 Raio: {raio_km}km\n"
        
        if tipo_estabelecimento:
            resultado += f"🏥 Filtro: {tipo_estabelecimento}\n"
        
        resultado += f"\n✅ {len(estabelecimentos)} resultado(s) encontrado(s):\n\n"
        
        for i, est in enumerate(estabelecimentos, 1):
            # Emoji e classificação por tipo
            info_tipo = {
                'HOSPITAL': {'emoji': '🏥', 'desc': 'Hospital'},
                'UPA': {'emoji': '🚑', 'desc': 'Unidade de Pronto Atendimento'},
                'UBS': {'emoji': '⚕️', 'desc': 'Unidade Básica de Saúde'},
                'MATERNIDADE': {'emoji': '👶', 'desc': 'Maternidade'}
            }
            tipo_info = info_tipo.get(est['tipo'], {'emoji': '🏢', 'desc': est['tipo']})
            
            # Classificação de distância
            distancia = est['distancia_km']
            if distancia <= 2:
                dist_emoji = "🟢"
                dist_classe = "MUITO PRÓXIMO"
            elif distancia <= 5:
                dist_emoji = "🟡"
                dist_classe = "PRÓXIMO"
            elif distancia <= 10:
                dist_emoji = "🟠"
                dist_classe = "MODERADO"
            else:
                dist_emoji = "🔴"
                dist_classe = "DISTANTE"
            
            resultado += f"{i}. {tipo_info['emoji']} **{est['nome']}**\n"
            resultado += f"   � Tipo: {tipo_info['desc']}\n"
            resultado += f"   {dist_emoji} Distância: {distancia:.1f}km ({dist_classe})\n"
            resultado += f"   🏙️ Município: {est['municipio']}\n"
            resultado += f"   📞 Contato: {est['telefone']}\n"
            resultado += f"   📍 Endereço: {est['endereco']}\n"
            resultado += f"   ⏰ Funcionamento: {est['horario_funcionamento']}\n"
            
            # Especialidades se disponível
            if est.get('especialidades'):
                especialidades = est['especialidades'][:3]  # Máximo 3
                resultado += f"   🩺 Especialidades: {', '.join(especialidades)}"
                if len(est['especialidades']) > 3:
                    resultado += f" (+{len(est['especialidades'])-3} outras)"
                resultado += "\n"
            
            resultado += f"   📍 Coordenadas: ({est['latitude']}, {est['longitude']})\n\n"
        
        # Estatísticas da busca
        resultado += "📊 ESTATÍSTICAS DA BUSCA:\n"
        resultado += f"• Total encontrado: {len(estabelecimentos)}\n"
        resultado += f"• Mais próximo: {min(est['distancia_km'] for est in estabelecimentos):.1f}km\n"
        resultado += f"• Mais distante: {max(est['distancia_km'] for est in estabelecimentos):.1f}km\n"
        
        # Tipos encontrados
        tipos_encontrados = {}
        for est in estabelecimentos:
            tipos_encontrados[est['tipo']] = tipos_encontrados.get(est['tipo'], 0) + 1
        
        resultado += "• Tipos: "
        resultado += ", ".join([f"{tipo} ({qtd})" for tipo, qtd in tipos_encontrados.items()])
        
        return resultado


class CalculoDistanciaPostGISTool(BaseTool):
    """Ferramenta para cálculos de distância usando PostgreSQL + PostGIS"""
    
    name: str = "calculo_distancia_postgis"
    description: str = (
        "Calcula distância precisa usando PostGIS (mais eficiente). "
        "Parâmetros: lat1, lng1, lat2, lng2"
    )
    
    def _run(self, lat1: float, lng1: float, lat2: float, lng2: float) -> str:
        """Calcula distância usando PostgreSQL ST_Distance"""
        
        # Usar função do sistema que pode aproveitar PostGIS se disponível
        distancia = dados_medicos.db.calcular_distancia(lat1, lng1, lat2, lng2)
        
        resultado = "📏 CÁLCULO DE DISTÂNCIA (PostGIS)\n"
        resultado += "=" * 35 + "\n\n"
        resultado += f"📍 Origem: ({lat1:.4f}, {lng1:.4f})\n"
        resultado += f"📍 Destino: ({lat2:.4f}, {lng2:.4f})\n"
        resultado += f"📏 Distância: {distancia:.3f}km\n\n"
        
        # Análise detalhada da distância
        if distancia <= 1:
            classe = "🟢 MUITO PRÓXIMO"
            tempo_carro = "2-5 min de carro"
            tempo_pe = "10-15 min a pé"
        elif distancia <= 3:
            classe = "🟡 PRÓXIMO"
            tempo_carro = "5-10 min de carro"
            tempo_pe = "30-45 min a pé"
        elif distancia <= 8:
            classe = "🟠 MODERADO"
            tempo_carro = "10-20 min de carro"
            tempo_pe = "Não recomendado a pé"
        elif distancia <= 20:
            classe = "🔴 DISTANTE"
            tempo_carro = "20-40 min de carro"
            tempo_pe = "Usar transporte"
        else:
            classe = "⚫ MUITO DISTANTE"
            tempo_carro = "40+ min de carro"
            tempo_pe = "Necessário transporte"
        
        resultado += f"📊 Classificação: {classe}\n"
        resultado += f"🚗 Tempo estimado: {tempo_carro}\n"
        resultado += f"🚶 Caminhada: {tempo_pe}\n"
        
        # Recomendações baseadas na distância
        resultado += "\n💡 RECOMENDAÇÕES:\n"
        if distancia <= 3:
            resultado += "• Distância adequada para emergências\n"
            resultado += "• Acesso fácil por qualquer meio de transporte\n"
        elif distancia <= 10:
            resultado += "• Aceitável para casos não urgentes\n"
            resultado += "• Usar carro ou transporte público\n"
        else:
            resultado += "• Considerar estabelecimentos mais próximos\n"
            resultado += "• Apenas se for especialidade específica\n"
        
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


def criar_agente_geografico_avancado(llm: ChatOpenAI = None) -> Agent:
    """
    Cria agente especializado em geolocalização médica com PostgreSQL
    
    Args:
        llm: Modelo de linguagem (opcional)
        
    Returns:
        Agent configurado para busca geográfica avançada
    """
    
    if llm is None:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    
    return Agent(
        role="Especialista em GIS Médico e Análise Espacial",
        goal="Otimizar acesso médico através de análise geoespacial avançada",
        backstory="""
        Sou um especialista em Sistemas de Informação Geográfica (GIS) aplicados
        à saúde, com domínio em PostgreSQL + PostGIS e análise espacial médica.
        
        🗺️ TECNOLOGIAS AVANÇADAS:
        • PostgreSQL com extensão PostGIS para análise espacial
        • Índices espaciais (GIST) para busca ultra-rápida
        • Cálculos de distância otimizados em banco
        • Análise de proximidade com filtros inteligentes
        • Integração com dados reais de estabelecimentos de saúde
        
        🎯 EXPERTISE MÉDICA:
        • Mapeamento completo da rede de saúde do Piauí
        • Análise de acessibilidade geográfica a serviços médicos
        • Otimização de rotas para emergências médicas
        • Classificação de estabelecimentos por especialidade
        • Análise de cobertura populacional de serviços
        
        🚀 DIFERENCIAIS TECNOLÓGICOS:
        • Busca espacial em milissegundos com índices otimizados
        • Cálculos de distância precisos usando elipsoides terrestres
        • Filtros inteligentes por tipo, especialidade e horário
        • Análise de clusters de estabelecimentos
        • Recomendações baseadas em múltiplos critérios
        
        ⚕️ METODOLOGIA INTELIGENTE:
        • Priorização automática baseada na urgência médica
        • Consideração de horários de funcionamento
        • Análise de capacidade e especialidades
        • Rotas alternativas para casos de sobrecarga
        • Integração com protocolos de triagem
        
        🌟 MISSÃO:
        Garantir que cada paciente encontre o atendimento médico mais adequado
        no menor tempo possível, usando tecnologia GIS avançada para otimizar
        o acesso à saúde e salvar vidas através de decisões geoespaciais precisas.
        
        📊 DADOS EM TEMPO REAL:
        Trabalho com base de dados atualizada de estabelecimentos reais,
        incluindo coordenadas precisas, especialidades, horários e capacidade
        de atendimento, garantindo recomendações sempre atualizadas.
        """,
        tools=[
            BuscaGeograficaAvancadaTool(),
            CalculoDistanciaPostGISTool(),
            RecomendacaoUrgenciaTool()
        ],
        llm=llm,
        verbose=True
    )


# Manter compatibilidade com código existente
def criar_agente_geografico(llm: ChatOpenAI = None) -> Agent:
    """Função de compatibilidade - usa a versão avançada"""
    return criar_agente_geografico_avancado(llm)


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