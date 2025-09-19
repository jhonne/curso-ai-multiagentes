"""
Agente Médico - Especialista em Análise de Sintomas
===================================================

Este agente é especializado em analisar sintomas médicos,
classificar urgência e correlacionar com protocolos de atendimento.

Funcionalidades:
- Análise de sintomas em texto livre
- Classificação de urgência médica (1-5)
- Correlação com queixas principais
- Recomendação de protocolos de atendimento
"""

from crewai import Agent
from crewai_tools import BaseTool
from langchain_openai import ChatOpenAI
from dados_simulados import dados_medicos
import re


class AnaliseSintomasAvancadaTool(BaseTool):
    """Ferramenta avançada para análise de sintomas médicos"""
    
    name: str = "analise_sintomas_avancada"
    description: str = (
        "Analisa sintomas descritos em linguagem natural e classifica urgência. "
        "Identifica sintomas críticos e correlaciona com protocolos médicos. "
        "Parâmetro: texto_sintomas"
    )
    
    def _run(self, texto_sintomas: str) -> str:
        """Executa análise avançada de sintomas"""
        
        # Análise usando dados médicos
        resultado_base = dados_medicos.classificar_urgencia_sintomas(texto_sintomas)
        
        # Análise adicional de padrões críticos
        padroes_criticos = self._identificar_padroes_criticos(texto_sintomas)
        
        # Formatar resultado completo
        relatorio = "🔍 ANÁLISE MÉDICA AVANÇADA\n"
        relatorio += "=" * 35 + "\n\n"
        
        relatorio += f"📝 TEXTO ANALISADO:\n"
        relatorio += f'"{texto_sintomas}"\n\n'
        
        # Sintomas identificados
        if resultado_base['sintomas_encontrados']:
            relatorio += "✅ SINTOMAS IDENTIFICADOS:\n"
            for sintoma in resultado_base['sintomas_encontrados']:
                criticidade_emoji = self._get_criticidade_emoji(sintoma['criticidade'])
                relatorio += f"   {criticidade_emoji} {sintoma['nome']} "
                relatorio += f"(criticidade: {sintoma['criticidade']}/5)\n"
        else:
            relatorio += "⚠️ Nenhum sintoma específico identificado na base\n"
        
        # Padrões críticos adicionais
        if padroes_criticos:
            relatorio += f"\n🚨 PADRÕES CRÍTICOS DETECTADOS:\n"
            for padrao in padroes_criticos:
                relatorio += f"   ⚠️ {padrao}\n"
        
        # Classificação de urgência
        urgencia_final = max(
            resultado_base['nivel_urgencia'],
            5 if padroes_criticos else 1
        )
        
        relatorio += f"\n📊 CLASSIFICAÇÃO FINAL:\n"
        relatorio += f"   🎯 Nível de urgência: {urgencia_final}/5\n"
        relatorio += f"   📋 Status: {self._get_status_urgencia(urgencia_final)}\n"
        relatorio += f"   💡 Recomendação: {self._get_recomendacao(urgencia_final)}\n"
        
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


class ConsultaProtocolosTool(BaseTool):
    """Ferramenta para consulta de protocolos médicos"""
    
    name: str = "consulta_protocolos"
    description: str = (
        "Consulta protocolos médicos para queixas específicas. "
        "Parâmetro: tipo_queixa"
    )
    
    def _run(self, tipo_queixa: str) -> str:
        """Consulta protocolos baseados em queixas principais"""
        
        # Buscar sintomas relacionados à queixa
        sintomas_relacionados = dados_medicos.buscar_sintomas_por_queixa(tipo_queixa)
        
        if not sintomas_relacionados:
            return f"❌ Protocolo não encontrado para queixa: {tipo_queixa}"
        
        resultado = f"📋 PROTOCOLO MÉDICO: {tipo_queixa.upper()}\n"
        resultado += "=" * (len(tipo_queixa) + 20) + "\n\n"
        
        # Sintomas associados
        resultado += "🔍 SINTOMAS ASSOCIADOS:\n"
        for sintoma in sintomas_relacionados:
            emoji = self._get_emoji_criticidade(sintoma['criticidade'])
            resultado += f"   {emoji} {sintoma['nome']} "
            resultado += f"(criticidade: {sintoma['criticidade']}/5)\n"
        
        # Protocolo de atendimento baseado na criticidade máxima
        max_criticidade = max([s['criticidade'] for s in sintomas_relacionados])
        
        resultado += f"\n📊 AVALIAÇÃO DO PROTOCOLO:\n"
        resultado += f"   • Criticidade máxima: {max_criticidade}/5\n"
        resultado += f"   • Tipo de atendimento: {self._get_tipo_atendimento(max_criticidade)}\n"
        resultado += f"   • Tempo recomendado: {self._get_tempo_atendimento(max_criticidade)}\n"
        
        # Sinais de alerta
        resultado += f"\n⚠️ SINAIS DE ALERTA:\n"
        resultado += self._get_sinais_alerta(tipo_queixa)
        
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


def criar_agente_medico(llm: ChatOpenAI = None) -> Agent:
    """
    Cria agente especializado em análise médica
    
    Args:
        llm: Modelo de linguagem (opcional)
        
    Returns:
        Agent configurado para análise médica
    """
    
    if llm is None:
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    
    return Agent(
        role="Especialista em Triagem e Protocolos Médicos",
        goal="Analisar sintomas e aplicar protocolos médicos adequados",
        backstory="""
        Sou um profissional de saúde especializado em triagem médica e protocolos
        de atendimento com mais de 15 anos de experiência. Minha expertise inclui:
        
        🩺 ESPECIALIDADES:
        • Análise clínica de sintomas e sinais
        • Protocolos de classificação de risco
        • Medicina de urgência e emergência  
        • Sistemas de triagem hospitalar (Manchester, START)
        
        🎯 COMPETÊNCIAS:
        • Identificação precoce de quadros críticos
        • Correlação sintoma-patologia
        • Priorização baseada em evidências
        • Comunicação clara com pacientes
        
        ⚕️ PRINCÍPIOS:
        • Segurança do paciente sempre em primeiro lugar
        • Aplicação de protocolos baseados em evidências
        • Comunicação empática e clara
        • Encaminhamento apropriado conforme complexidade
        
        Minha missão é garantir que cada paciente seja adequadamente avaliado,
        classificado quanto à urgência e direcionado ao nível de atenção correto,
        sempre priorizando a segurança e o melhor desfecho clínico.
        
        ⚠️ IMPORTANTE: Minhas análises são para triagem inicial. Casos suspeitos
        de emergência devem sempre buscar atendimento médico presencial imediato.
        """,
        tools=[
            AnaliseSintomasAvancadaTool(),
            ConsultaProtocolosTool()
        ],
        llm=llm,
        verbose=True
    )


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