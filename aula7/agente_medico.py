"""
Agente Médico Avançado - Especialista em Análise Semântica de Sintomas
=====================================================================

Este agente utiliza PostgreSQL + embeddings para análise médica avançada:

Funcionalidades Modernas:
- Análise semântica de sintomas usando OpenAI embeddings
- Busca por similaridade em base de dados médica real
- Classificação inteligente de urgência (1-5)
- Correlação com protocolos médicos baseados em evidência
- Integração com sistema PostgreSQL + pgvector

Substitui completamente o sistema simulado anterior.
"""

from crewai import Agent
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI

try:
    from .dados_medicos_reais import dados_medicos
except ImportError:
    from dados_medicos_reais import dados_medicos
import re


class AnaliseSemanticaSintomasTool(BaseTool):
    """Ferramenta avançada para análise semântica de sintomas com embeddings"""
    
    name: str = "analise_semantica_sintomas"
    description: str = (
        "Analisa sintomas usando busca semântica por embeddings. "
        "Identifica sintomas similares e classifica urgência inteligentemente. "
        "Parâmetro: texto_sintomas"
    )
    
    def _run(self, texto_sintomas: str) -> str:
        """Executa análise semântica avançada de sintomas"""
        
        # Análise inteligente usando embeddings
        resultado = dados_medicos.classificar_urgencia_inteligente(texto_sintomas)
        
        # Formatar resultado completo
        relatorio = "🧠 ANÁLISE SEMÂNTICA AVANÇADA\n"
        relatorio += "=" * 40 + "\n\n"
        
        relatorio += "📝 TEXTO ANALISADO:\n"
        relatorio += f'"{texto_sintomas}"\n\n'
        
        # Sintomas identificados por similaridade
        if resultado['sintomas_similares']:
            relatorio += "🔍 SINTOMAS SIMILARES ENCONTRADOS:\n"
            for sintoma in resultado['sintomas_similares'][:5]:
                emoji = self._get_criticidade_emoji(sintoma['criticidade'])
                similarity = sintoma['similaridade']
                relatorio += f"   {emoji} {sintoma['nome']} "
                relatorio += f"(similaridade: {similarity:.1%}, "
                relatorio += f"criticidade: {sintoma['criticidade']}/5)\n"
                if sintoma.get('categoria'):
                    relatorio += f"      📂 Categoria: {sintoma['categoria']}\n"
        else:
            relatorio += "⚠️ Nenhum sintoma similar encontrado na base\n"
        
        # Queixas principais correlacionadas
        if resultado['queixas_similares']:
            relatorio += "\n📋 QUEIXAS PRINCIPAIS CORRELACIONADAS:\n"
            for queixa in resultado['queixas_similares'][:3]:
                urgencia_emoji = self._get_urgencia_emoji(queixa['nivel_urgencia'])
                similarity = queixa['similaridade']
                relatorio += f"   {urgencia_emoji} {queixa['nome']} "
                relatorio += f"(similaridade: {similarity:.1%})\n"
                relatorio += f"      📝 {queixa['descricao']}\n"
        
        # Padrões críticos identificados
        if resultado['padroes_criticos']:
            relatorio += "\n🚨 PADRÕES CRÍTICOS IDENTIFICADOS:\n"
            for padrao in resultado['padroes_criticos']:
                relatorio += f"   ⚠️ {padrao}\n"
        
        # Classificação final
        nivel = resultado['nivel_urgencia']
        relatorio += "\n📊 CLASSIFICAÇÃO INTELIGENTE:\n"
        relatorio += f"   🎯 Nível de urgência: {nivel}/5\n"
        relatorio += f"   📋 Status: {resultado['classificacao']}\n"
        relatorio += f"   💡 Recomendação: {resultado['recomendacao']}\n"
        relatorio += f"   🏥 Estabelecimento recomendado: "
        relatorio += f"{resultado['tipo_estabelecimento_recomendado']}\n"
        relatorio += f"   🔍 Confiança da análise: "
        relatorio += f"{resultado['confianca_analise']} correlações\n"
        
        return relatorio
    
    def _identificar_padroes_criticos(self, texto: str) -> list:
        """Identifica padrões que indicam emergência médica"""
        texto_lower = texto.lower()
        padroes_criticos = []
        
        # Padrões cardíacos críticos
        if any(word in texto_lower for word in ['dor no peito', 'dor torácica', 'aperto no peito']):
            if any(word in texto_lower for word in ['intensa', 'forte', 'severa']):
                padroes_criticos.append("Dor torácica intensa - suspeita de síndrome coronariana")
        
        # Padrões respiratórios críticos
        if any(word in texto_lower for word in ['falta de ar', 'faltando ar', 'não consigo respirar']):
            padroes_criticos.append("Insuficiência respiratória - necessita avaliação imediata")
        
        # Padrões neurológicos
        if any(word in texto_lower for word in ['desmaio', 'perdi consciência', 'convulsão']):
            padroes_criticos.append("Alteração neurológica - requer atenção médica urgente")
        
        # Padrões de trauma
        if any(word in texto_lower for word in ['acidente', 'queda', 'batida', 'sangramento']):
            padroes_criticos.append("Trauma físico - avaliação de lesões necessária")
        
        return padroes_criticos
    
    def _get_criticidade_emoji(self, nivel: int) -> str:
        """Retorna emoji baseado no nível de criticidade"""
        emojis = {1: "🟢", 2: "🟡", 3: "🟠", 4: "🔴", 5: "🚨"}
        return emojis.get(nivel, "❓")
    
    def _get_urgencia_emoji(self, nivel: int) -> str:
        """Retorna emoji baseado no nível de urgência"""
        emojis = {1: "🟢", 2: "🟡", 3: "🟠", 4: "🔴", 5: "🚨"}
        return emojis.get(nivel, "❓")
    
    def _get_status_urgencia(self, nivel: int) -> str:
        """Retorna status textual da urgência"""
        status = {
            1: "NÃO URGENTE",
            2: "LEVE", 
            3: "MODERADO",
            4: "URGENTE",
            5: "EMERGÊNCIA"
        }
        return status.get(nivel, "INDETERMINADO")
    
    def _get_recomendacao(self, nivel: int) -> str:
        """Retorna recomendação baseada no nível"""
        recomendacoes = {
            1: "Consulta de rotina em UBS quando conveniente",
            2: "Procure UBS ou agende consulta médica", 
            3: "Procure UPA ou médico em até 24h",
            4: "Procure UPA ou hospital rapidamente",
            5: "Procure atendimento IMEDIATAMENTE ou chame SAMU (192)"
        }
        return recomendacoes.get(nivel, "Consulte profissional de saúde")


class ConsultaProtocolosAvancadosTool(BaseTool):
    """Ferramenta avançada para consulta de protocolos médicos com busca semântica"""
    
    name: str = "consulta_protocolos_avancados"
    description: str = (
        "Consulta protocolos médicos usando busca semântica. "
        "Encontra protocolos relevantes mesmo com termos similares. "
        "Parâmetro: descricao_caso"
    )
    
    def _run(self, descricao_caso: str) -> str:
        """Consulta protocolos usando busca semântica"""
        
        # Buscar queixas similares usando embeddings
        queixas_similares = dados_medicos.buscar_queixas_por_similaridade(
            descricao_caso
        )
        
        if not queixas_similares:
            return f"❌ Nenhum protocolo encontrado para: {descricao_caso}"
        
        # Selecionar a queixa mais similar
        queixa_principal = queixas_similares[0]
        
        resultado = "📋 PROTOCOLO MÉDICO AVANÇADO\n"
        resultado += "=" * 35 + "\n\n"
        
        resultado += f"📝 CASO ANALISADO:\n"
        resultado += f'"{descricao_caso}"\n\n'
        
        # Queixa principal identificada
        resultado += "🎯 PROTOCOLO IDENTIFICADO:\n"
        resultado += f"   📋 {queixa_principal['nome']}\n"
        resultado += f"   📝 {queixa_principal['descricao']}\n"
        resultado += f"   🔍 Similaridade: "
        resultado += f"{queixa_principal['similaridade']:.1%}\n"
        resultado += f"   🚨 Urgência: {queixa_principal['nivel_urgencia']}/5\n\n"
        
        # Protocolo detalhado se disponível
        if queixa_principal.get('protocolo_atendimento'):
            resultado += "⚕️ PROTOCOLO DE ATENDIMENTO:\n"
            resultado += f"{queixa_principal['protocolo_atendimento']}\n\n"
        
        # Tempo limite para atendimento
        if queixa_principal.get('tempo_limite_atendimento'):
            resultado += "⏱️ TEMPO LIMITE PARA ATENDIMENTO:\n"
            tempo = queixa_principal['tempo_limite_atendimento']
            resultado += f"   🕐 Máximo: {tempo}\n\n"
        
        # Outras queixas similares (diagnósticos diferenciais)
        if len(queixas_similares) > 1:
            resultado += "� DIAGNÓSTICOS DIFERENCIAIS:\n"
            for queixa in queixas_similares[1:3]:
                resultado += f"   • {queixa['nome']} "
                resultado += f"(similaridade: {queixa['similaridade']:.1%})\n"
        
        # Recomendações específicas baseadas na urgência
        nivel = queixa_principal['nivel_urgencia']
        resultado += "\n💡 RECOMENDAÇÕES ESPECÍFICAS:\n"
        
        if nivel >= 5:
            resultado += "   🚨 EMERGÊNCIA - Atendimento imediato\n"
            resultado += "   📞 Considerar chamar SAMU (192)\n"
            resultado += "   🏥 Direto para sala de emergência\n"
        elif nivel >= 4:
            resultado += "   🔴 URGENTE - Atendimento prioritário\n"
            resultado += "   🏥 UPA ou Hospital rapidamente\n"
            resultado += "   📋 Triagem imediata\n"
        elif nivel >= 3:
            resultado += "   🟠 MODERADO - Avaliação em algumas horas\n"
            resultado += "   🏥 UPA ou consulta médica em 24h\n"
        elif nivel >= 2:
            resultado += "   🟡 LEVE - Acompanhamento recomendado\n"
            resultado += "   🏥 UBS ou consulta agendada\n"
        else:
            resultado += "   🟢 NÃO URGENTE - Rotina médica\n"
            resultado += "   🏥 Consulta quando conveniente\n"
        
        return resultado
    
    def _get_emoji_criticidade(self, nivel: int) -> str:
        """Emoji para nível de criticidade"""
        emojis = {1: "🟢", 2: "🟡", 3: "🟠", 4: "🔴", 5: "🚨"}
        return emojis.get(nivel, "❓")
    
    def _get_tipo_atendimento(self, criticidade: int) -> str:
        """Tipo de atendimento baseado na criticidade"""
        tipos = {
            1: "UBS - Consulta programada",
            2: "UBS ou UPA - Consulta no mesmo dia",
            3: "UPA - Atendimento em algumas horas", 
            4: "UPA/Hospital - Atendimento prioritário",
            5: "Hospital/SAMU - Atendimento imediato"
        }
        return tipos.get(criticidade, "Avaliação médica")
    
    def _get_tempo_atendimento(self, criticidade: int) -> str:
        """Tempo recomendado para atendimento"""
        tempos = {
            1: "Até 7 dias",
            2: "Até 48h",
            3: "Até 12h",
            4: "Até 2h", 
            5: "Imediato (< 15 min)"
        }
        return tempos.get(criticidade, "Conforme orientação médica")
    
    def _get_sinais_alerta(self, queixa: str) -> str:
        """Sinais de alerta específicos por tipo de queixa"""
        alertas = {
            'DOR NO PEITO': '• Dor irradiando para braço/mandíbula\n• Sudorese fria\n• Falta de ar\n• Palpitações',
            'CEFALEIA': '• Dor súbita e intensa\n• Febre alta\n• Rigidez de nuca\n• Alterações visuais',
            'FEBRE': '• Temperatura > 39°C\n• Dificuldade respiratória\n• Manchas na pele\n• Convulsões',
            'FALTA DE AR': '• Respiração muito rápida\n• Lábios roxos\n• Dor no peito\n• Ansiedade extrema'
        }
        return alertas.get(queixa.upper(), '• Procure ajuda se sintomas piorarem\n• Não ignore sinais de alarme')


def criar_agente_medico_avancado(llm: ChatOpenAI = None) -> Agent:
    """
    Cria agente médico especializado com análise semântica avançada
    
    Args:
        llm: Modelo de linguagem (opcional)
        
    Returns:
        Agent configurado para análise médica com embeddings
    """
    
    if llm is None:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    
    return Agent(
        role="Especialista em Medicina Baseada em IA e Análise Semântica",
        goal="Analisar sintomas usando inteligência artificial e busca semântica",
        backstory="""
        Sou um médico especialista em medicina digital e sistemas de IA médica,
        com experiência em análise semântica de sintomas e protocolos inteligentes.
        
        🤖 TECNOLOGIAS AVANÇADAS:
        • Análise semântica com OpenAI embeddings
        • Busca por similaridade em bases médicas extensas
        • Classificação inteligente de urgência
        • Correlação automática sintoma-protocolo
        • Sistema PostgreSQL com pgvector integrado
        
        🩺 ESPECIALIDADES MÉDICAS:
        • Triagem médica inteligente
        • Protocolos de emergência (Manchester, START)
        • Medicina de urgência e emergência
        • Análise preditiva de risco
        • Telemedicina e medicina digital
        
        🎯 METODOLOGIA AVANÇADA:
        • Uso embeddings para encontrar sintomas similares
        • Análise de padrões críticos automática
        • Correlação com base de dados médica real
        • Classificação multi-dimensional de urgência
        • Recomendações baseadas em evidência científica
        
        ⚕️ PRINCÍPIOS FUNDAMENTAIS:
        • Segurança do paciente como prioridade absoluta
        • Precisão diagnóstica com suporte de IA
        • Transparência nas análises e recomendações
        • Integração humano-IA para melhores resultados
        • Melhoria contínua através de feedback
        
        🔬 DIFERENCIAL TECNOLÓGICO:
        Utilizo sistema avançado de PostgreSQL + pgvector para busca semântica
        de sintomas, permitindo identificar correlações que análises tradicionais
        podem não detectar. Minha análise combina experiência médica com 
        capacidades de IA para oferecer diagnósticos mais precisos.
        
        ⚠️ DISCLAIMER MÉDICO:
        Minhas análises são ferramentas de suporte diagnóstico. Emergências
        médicas reais sempre requerem atendimento presencial imediato.
        Não substituo consulta médica profissional.
        """,
        tools=[
            AnaliseSemanticaSintomasTool(),
            ConsultaProtocolosAvancadosTool()
        ],
        llm=llm,
        verbose=True
    )


# Manter compatibilidade com código existente
def criar_agente_medico(llm: ChatOpenAI = None) -> Agent:
    """Função de compatibilidade - usa a versão avançada"""
    return criar_agente_medico_avancado(llm)


# Exemplo de uso do agente médico
def exemplo_agente_medico():
    """Demonstra uso do agente médico especializado"""
    
    from crewai import Task, Crew, Process
    
    print("🩺 EXEMPLO: AGENTE MÉDICO ESPECIALIZADO")
    print("="*42)
    
    # Criar agente
    agente = criar_agente_medico()
    
    # Casos clínicos para teste
    casos_clinicos = [
        {
            'nome': 'Suspeita de Infarto',
            'sintomas': 'dor no peito muito forte, suando frio, falta de ar, dor no braço esquerdo',
            'tarefa': """
            CASO CLÍNICO: Paciente masculino, 55 anos, relata dor torácica intensa.
            
            SINTOMAS: "dor no peito muito forte, suando frio, falta de ar, dor no braço esquerdo"
            
            ANÁLISE SOLICITADA:
            1. Faça análise completa dos sintomas descritos
            2. Identifique padrões críticos de emergência
            3. Classifique o nível de urgência (1-5)
            4. Consulte protocolo para "DOR NO PEITO"
            5. Forneça recomendação imediata
            
            PRIORIDADE: Máxima - suspeita de síndrome coronariana aguda
            """
        },
        {
            'nome': 'Cefaleia com Sinais de Alerta', 
            'sintomas': 'dor de cabeça súbita e muito intensa, nunca senti igual, com vômito',
            'tarefa': """
            CASO CLÍNICO: Paciente feminina, 42 anos, cefaleia súbita e intensa.
            
            SINTOMAS: "dor de cabeça súbita e muito intensa, nunca senti igual, com vômito"
            
            ANÁLISE SOLICITADA:
            1. Analise padrão da cefaleia (súbita, intensa, diferente do habitual)
            2. Avalie sintomas associados (vômito)
            3. Consulte protocolo para "CEFALEIA"
            4. Identifique sinais de alerta neurológicos
            5. Determine urgência e conduta
            
            ATENÇÃO: Cefaleia "thunderclap" requer investigação imediata
            """
        }
    ]
    
    for i, caso in enumerate(casos_clinicos, 1):
        print(f"\n🎯 CASO CLÍNICO {i}: {caso['nome']}")
        print("-" * 60)
        
        # Criar tarefa
        tarefa = Task(
            description=caso['tarefa'],
            agent=agente,
            expected_output="Análise médica completa com classificação de risco e conduta recomendada"
        )
        
        # Executar análise
        crew = Crew(
            agents=[agente],
            tasks=[tarefa],
            process=Process.sequential,
            verbose=False
        )
        
        resultado = crew.kickoff()
        print(f"📋 ANÁLISE MÉDICA:\n{resultado.raw}")
        print("\n" + "="*60)


if __name__ == "__main__":
    exemplo_agente_medico()