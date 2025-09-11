"""
Classe ChatbotCrew Simplificada para a Aula 7
Versão mínima funcional para demonstrar interface Streamlit
"""

import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

try:
    # Tentar importar CrewAI
    from crewai import Agent, Task, Crew, Process
    from langchain_openai import ChatOpenAI

    CREWAI_AVAILABLE = True
except ImportError:
    CREWAI_AVAILABLE = False
    print("⚠️ CrewAI não instalado. Usando simulação.")


class ChatbotSimplificado:
    """Versão simplificada para demonstrar interface quando CrewAI não disponível"""

    def __init__(self):
        self.historico = []

    def processar(self, mensagem):
        """Simula processamento do chatbot"""
        import time
        import random

        # Simular tempo de processamento
        time.sleep(1)

        respostas_exemplo = [
            f"Entendo sua pergunta: '{mensagem}'. Como um chatbot multi-agente, eu processaria isso através dos meus agentes especializados.",
            f"Interessante! Sobre '{mensagem}', posso dizer que nossos agentes trabalhariam em conjunto para fornecer a melhor resposta.",
            f"Recebi sua mensagem: '{mensagem}'. Em um sistema real, meus agentes de triagem, análise e resposta trabalhariam sequencialmente.",
            "Este é um exemplo de resposta do chatbot. Na versão completa, múltiplos agentes CrewAI processariam sua solicitação.",
        ]

        resposta = random.choice(respostas_exemplo)
        self.historico.append({"user": mensagem, "bot": resposta})
        return resposta


class ChatbotCrew:
    """Classe principal do chatbot com CrewAI"""

    def __init__(self):
        if not CREWAI_AVAILABLE:
            self.chatbot = ChatbotSimplificado()
            return

        # Verificar API key
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError("OPENAI_API_KEY não encontrada. Configure no arquivo .env")

        # Configurar LLM
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

        # Criar agentes simples
        self.agente_triagem = Agent(
            role="Recepcionista Digital",
            goal="Analisar e categorizar a mensagem do usuário de forma objetiva",
            backstory="""Você é um especialista em análise de comunicação que identifica
            rapidamente a intenção e o contexto das mensagens dos usuários.
            Você sempre fornece análises diretas e objetivas sem floreios.""",
            llm=self.llm,
            verbose=False,
        )

        self.agente_resposta = Agent(
            role="Assistente Especialista",
            goal="Fornecer respostas diretas e específicas baseadas na análise recebida",
            backstory="""Você é um assistente experiente que sempre responde
            de forma direta e útil. Nunca use frases como 'I can give a great answer'
            ou 'Now I can provide'. Vá direto ao ponto com informações concretas.
            Responda sempre em português brasileiro.""",
            llm=self.llm,
            verbose=False,
        )

        # Histórico da conversa
        self.historico = []

    def processar(self, mensagem):
        """Processa mensagem através dos agentes CrewAI"""
        if not CREWAI_AVAILABLE:
            return self.chatbot.processar(mensagem)

        try:
            # Incluir contexto do histórico
            contexto = self._obter_contexto(mensagem)

            # Criar tarefas
            tarefa_triagem = Task(
                description=f"""Analise objetivamente esta mensagem do usuário: {contexto}
                
                Identifique:
                1. A intenção principal do usuário
                2. Informações específicas solicitadas
                3. Contexto relevante da conversa""",
                expected_output="Análise objetiva: intenção, informações solicitadas e contexto (máximo 100 palavras)",
                agent=self.agente_triagem,
            )

            tarefa_resposta = Task(
                description="""Com base na análise anterior, forneça uma resposta DIRETA e específica.
                
                IMPORTANTE:
                - Responda em português brasileiro
                - Seja direto e objetivo
                - NÃO use frases como 'I can give', 'Now I can provide' ou similares
                - Forneça informações concretas e úteis
                - Se não souber algo específico, seja honesto""",
                expected_output="Resposta direta e específica em português, máximo 200 palavras",
                agent=self.agente_resposta,
                context=[tarefa_triagem],
            )

            # Executar crew
            crew = Crew(
                agents=[self.agente_triagem, self.agente_resposta],
                tasks=[tarefa_triagem, tarefa_resposta],
                process=Process.sequential,
                verbose=False,
            )

            resultado = crew.kickoff()

            # Pós-processar resultado para evitar respostas genéricas
            resultado_processado = self._filtrar_resposta(str(resultado))

            # Salvar no histórico
            self.historico.append(
                {
                    "user": mensagem,
                    "bot": resultado_processado,
                    "timestamp": self._obter_timestamp(),
                }
            )

            return resultado_processado

        except Exception as e:
            error_msg = f"Erro no processamento: {str(e)}"
            print(f"❌ {error_msg}")
            return "Desculpe, ocorreu um erro. Tente novamente."

    def _obter_contexto(self, mensagem_atual):
        """Inclui histórico recente no contexto"""
        if not self.historico:
            return mensagem_atual

        # Últimas 3 interações
        historico_recente = self.historico[-3:]
        contexto_historico = "\n".join(
            [f"Usuário: {h['user']}\nBot: {h['bot']}" for h in historico_recente]
        )

        return f"Histórico recente:\n{contexto_historico}\n\nNova mensagem: {mensagem_atual}"

    def _filtrar_resposta(self, resposta):
        """Filtra respostas problemáticas e genéricas"""
        import re

        # Remover frases problemáticas comuns
        frases_problematicas = [
            r"I now can give a great answer",
            r"Now I can provide",
            r"I can give you",
            r"Let me provide you",
            r"Here's what I can tell you",
            r"I'll be happy to help",
            r"Based on the analysis above",
        ]

        resposta_filtrada = resposta
        for frase in frases_problematicas:
            resposta_filtrada = re.sub(
                frase, "", resposta_filtrada, flags=re.IGNORECASE
            )

        # Limpar espaços extras e quebras de linha
        resposta_filtrada = re.sub(r"\n\s*\n", "\n", resposta_filtrada)
        resposta_filtrada = resposta_filtrada.strip()

        # Se a resposta ficou muito curta ou vazia, fornecer fallback
        if len(resposta_filtrada) < 10:
            return "Como um assistente especializado, posso ajudá-lo com sua dúvida. Por favor, seja mais específico sobre o que gostaria de saber."

        return resposta_filtrada

    def _obter_timestamp(self):
        """Retorna timestamp atual"""
        from datetime import datetime

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def limpar_historico(self):
        """Limpa o histórico de conversas"""
        self.historico = []


# Para compatibilidade com importações
if __name__ == "__main__":
    # Teste rápido
    chatbot = ChatbotCrew()
    print("🤖 Chatbot criado com sucesso!")

    resposta = chatbot.processar("Olá, como você funciona?")
    print(f"Resposta: {resposta}")
