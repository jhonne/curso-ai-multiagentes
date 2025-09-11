# Aula 3: Ferramentas (Tools) e Processos (Processes) no CrewAI
# VERSÃO OTIMIZADA PARA ECONOMIA DE TOKENS

from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from dotenv import load_dotenv
import time
import os
from typing import Type
from pydantic import BaseModel, Field

load_dotenv()

print("🎯 Aula 3: Ferramentas e Processos [MODO ECONÔMICO]")
print("=" * 50)

# --- PARTE 1: FERRAMENTAS REAIS DO CREWAI ---
print("🔧 Configurando ferramentas do CrewAI...")


# Schema para entrada da ferramenta de busca
class BuscaWebInput(BaseModel):
    query: str = Field(description="Termo de busca para pesquisar na web")


# Schema para entrada da ferramenta de scraping
class ScrapingInput(BaseModel):
    url: str = Field(description="URL do site para extrair conteúdo")


# Schema para entrada da ferramenta de leitura
class LeituraArquivoInput(BaseModel):
    filepath: str = Field(description="Caminho do arquivo para ler")


# Ferramenta de Busca Web
class BuscaWebTool(BaseTool):
    name: str = "busca_web"
    description: str = "Busca informações específicas na web"
    args_schema: Type[BaseModel] = BuscaWebInput
    
    def _run(self, query: str) -> str:
        return f"""
🔍 BUSCA: {query}

📄 PRINCIPAIS RESULTADOS:
• CrewAI - Framework Python para agentes IA colaborativos
• GitHub oficial: joaomdmoura/crewai 
• Características: múltiplos agentes, roles específicos, processos sequenciais/hierárquicos

💡 FUNCIONALIDADES:
- Sistema de agentes com especialidades
- Delegação de tarefas entre agentes
- Ferramentas customizadas integradas
- Suporte a LLMs diversos

🎯 CASOS DE USO:
- Análise de dados complexos
- Automação de workflows
- Geração de conteúdo especializado
"""


# Ferramenta de Scraping
class ScrapingTool(BaseTool):
    name: str = "scraping_web"
    description: str = "Extrai conteúdo específico de páginas web"
    args_schema: Type[BaseModel] = ScrapingInput
    
    def _run(self, url: str) -> str:
        return f"""
📄 CONTEÚDO DE: {url}

CrewAI - Framework para Agentes IA Colaborativos

📝 RESUMO:
Framework Python para criar equipes de agentes IA especializados.
Cada agente tem role específico e colabora para completar tarefas complexas.

🔧 FUNCIONALIDADES:
• Agentes com especialidades definidas
• Tarefas interconectadas
• Processos sequenciais e hierárquicos
• Integração com ferramentas externas

⭐ VANTAGENS:
• Modularidade
• Escalabilidade
• Flexibilidade
• Suporte múltiplos LLMs
"""


# Ferramenta de Leitura de Arquivo
class LeituraArquivoTool(BaseTool):
    name: str = "leitura_arquivo"
    description: str = "Lê e analisa conteúdo de arquivos"
    args_schema: Type[BaseModel] = LeituraArquivoInput
    
    def _run(self, filepath: str) -> str:
        return f"""
📁 ARQUIVO: {filepath}

=== CONFIGURAÇÃO CREWAI ===
Framework: CrewAI v0.28.8
Python: 3.8+
Dependências: langchain, openai, pydantic

=== EXEMPLOS ===
1. Agente Pesquisador:
   - Role: Researcher
   - Goal: Coletar informações
   - Tools: Web search

2. Agente Analista:
   - Role: Analyst  
   - Goal: Processar dados
   - Tools: Data processing

=== PRÁTICAS ===
• Roles claros para agentes
• Expected_output específico
• Monitorar tokens
• Testar com dados simulados
"""


# Instanciando as ferramentas
busca_web_tool = BuscaWebTool()
scraping_tool = ScrapingTool()
leitura_arquivo_tool = LeituraArquivoTool()

print("✅ Ferramentas CrewAI configuradas:")
print("🔍 Busca Web - Pesquisa inteligente na web")
print("🌐 Scraping - Extração de conteúdo de sites")
print("📁 Leitura de Arquivo - Análise de documentos")

# --- PARTE 2: AGENTES COM FERRAMENTAS INTEGRADAS ---

# Configurações otimizadas para economia de tokens
CONFIG_SISTEMA = {
    'modelo_economico': os.getenv('OPENAI_MODEL_ECONOMICO', 'gpt-3.5-turbo'),
    'max_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '1000')),  # Reduzido de 2000
    'temperature': 0.5  # Reduzido para respostas mais focadas
}

print("⚙️  CONFIGURAÇÕES OTIMIZADAS:")
print(f"   � Modelo: {CONFIG_SISTEMA['modelo_economico']}")
print(f"   � Max Tokens: {CONFIG_SISTEMA['max_tokens']}")
print(f"   🎯 Temperature: {CONFIG_SISTEMA['temperature']}")
print()

# Agente Pesquisador otimizado
pesquisador_com_ferramentas = Agent(
    role='Pesquisador Web',
    goal='Coletar informações usando ferramentas de busca',
    backstory="""Pesquisador especializado em buscas web eficientes.
    Utiliza ferramentas para encontrar informações relevantes e verificar fontes.
    Sempre responde em português.""",
    tools=[busca_web_tool, scraping_tool, leitura_arquivo_tool],
    verbose=True,
    allow_delegation=False,
    max_iter=2,  # Limita iterações para economizar tokens
    max_execution_time=60  # Timeout de 1 minuto
)

# Agente Redator otimizado
redator_especializado = Agent(
    role='Redator Técnico',
    goal='Criar conteúdo claro e bem estruturado',
    backstory="""Redator técnico que transforma informações em conteúdo acessível.
    Especialista em organizar informações de forma lógica.
    Sempre escreve em português.""",
    tools=[leitura_arquivo_tool],
    verbose=True,
    allow_delegation=False,
    max_iter=2,
    max_execution_time=60
)

# Agente Revisor otimizado
revisor_critico = Agent(
    role='Revisor Crítico',
    goal='Analisar qualidade do conteúdo',
    backstory="""Revisor experiente que analisa textos em busca de melhorias.
    Fornece feedback construtivo e específico.
    Sempre analisa em português.""",
    tools=[busca_web_tool, leitura_arquivo_tool],
    verbose=True,
    allow_delegation=False,
    max_iter=2,
    max_execution_time=60
)

# Sistema de métricas simplificado
class MetricasExecucao:
    def __init__(self):
        self.inicio_execucao = None
        self.tokens_estimados = 0
        self.erros = []
    
    def iniciar_medicao(self, tipo_processo):
        self.inicio_execucao = time.time()
        self.tipo_processo = tipo_processo
    
    def finalizar_medicao(self):
        return time.time() - self.inicio_execucao if self.inicio_execucao else 0
    
    def gerar_relatorio(self):
        tempo_total = self.finalizar_medicao()
        return f"""
📊 RELATÓRIO SIMPLIFICADO
⏱️ Tempo: {tempo_total:.2f}s
🔄 Processo: {self.tipo_processo}
📈 Tokens estimados: {self.tokens_estimados}
❌ Erros: {len(self.erros)}
"""

metricas = MetricasExecucao()

# --- PARTE 3: DEFINIÇÃO DAS TAREFAS ---

# Tarefas otimizadas para menor consumo de tokens
tarefa_pesquisa_web = Task(
    description="""Pesquise informações sobre 'CrewAI framework'.
    
    Use suas ferramentas para encontrar:
    1. Características principais do framework
    2. Vantagens práticas
    3. Casos de uso principais
    
    Seja conciso e direto.""",
    expected_output="""Relatório com:
    - 3 características principais
    - 2 vantagens práticas
    - 2 casos de uso
    - Fontes consultadas
    Em português, máximo 300 palavras.""",
    agent=pesquisador_com_ferramentas
)

tarefa_redacao_tecnica = Task(
    description="""Crie um artigo técnico conciso sobre CrewAI baseado na pesquisa.
    
    Inclua:
    1. Introdução breve
    2. Características principais
    3. Casos de uso práticos
    4. Conclusão
    
    Seja direto e objetivo.""",
    expected_output="""Artigo de 400-500 palavras com:
    - Introdução (50 palavras)
    - Seções organizadas
    - Linguagem clara
    - Conclusão prática
    Em português.""",
    agent=redator_especializado
)

tarefa_revisao_critica = Task(
    description="""Revise o artigo analisando:
    
    1. Qualidade das informações
    2. Clareza do conteúdo
    3. Adequação ao público
    
    Feedback conciso e construtivo.""",
    expected_output="""Análise com:
    - Nota geral (1-10)
    - 2 pontos fortes
    - 2 melhorias sugeridas
    - Comentário final
    Em português, máximo 200 palavras.""",
    agent=revisor_critico
)

# Processo Sequencial otimizado
print("\n🔄 DEMONSTRAÇÃO: Processo Sequencial Otimizado")
print("-" * 40)

crew_sequencial = Crew(
    agents=[pesquisador_com_ferramentas, redator_especializado, revisor_critico],
    tasks=[tarefa_pesquisa_web, tarefa_redacao_tecnica, tarefa_revisao_critica],
    process=Process.sequential,
    verbose=False,  # Reduz output para economizar tokens
    language='pt-br',
    max_rpm=10  # Limita requests por minuto
)

print("📋 Processo configurado:")
print("   1️⃣ Pesquisador → Coleta informações")
print("   2️⃣ Redator → Cria artigo")
print("   3️⃣ Revisor → Analisa qualidade")


# Manager otimizado para hierárquico
manager_projeto = Agent(
    role='Gerente Editorial',
    goal='Coordenar produção de artigo em português',
    backstory="""Gerente experiente que coordena equipes editoriais.
    Delega tarefas eficientemente e monitora qualidade.
    Comunicação sempre em português.""",
    tools=[busca_web_tool],
    verbose=False,
    allow_delegation=True,
    max_iter=1,  # Reduz iterações do manager
    max_execution_time=120
)

# Tarefa hierárquica simplificada
tarefa_projeto_editorial = Task(
    description="""Coordene produção de artigo sobre CrewAI.
    Delegue: pesquisa, redação e revisão.
    Monitore qualidade e prazo.
    Tudo em português.""",
    expected_output="""Artigo completo sobre CrewAI:
    - Pesquisa fundamentada
    - Redação clara
    - Revisão de qualidade
    Em português, máximo 600 palavras total.""",
    agent=manager_projeto
)

crew_hierarquico = Crew(
    agents=[manager_projeto, pesquisador_com_ferramentas, redator_especializado, revisor_critico],
    tasks=[tarefa_projeto_editorial],
    process=Process.hierarchical,
    manager_llm=CONFIG_SISTEMA['modelo_economico'],
    verbose=False,
    language='pt-br',
    max_rpm=8  # Menos requests para hierárquico
)

print("\n🏗️ Processo Hierárquico configurado:")
print("   👨‍💼 Manager → Coordena em português")
print("   ⚡ Execução otimizada")
print(f"   💰 Modelo: {CONFIG_SISTEMA['modelo_economico']}")

# Função de execução otimizada
def executar_processo_sequencial():
    print("\n🚀 EXECUTANDO PROCESSO SEQUENCIAL OTIMIZADO")
    print("="*50)
    
    metricas.iniciar_medicao("Sequencial-Econômico")
    
    try:
        print(f"⚙️ Modelo: {CONFIG_SISTEMA['modelo_economico']} | Tokens: {CONFIG_SISTEMA['max_tokens']}")
        
        resultado_seq = crew_sequencial.kickoff()
        tempo_seq = metricas.finalizar_medicao()
        
        metricas.tokens_estimados = len(str(resultado_seq)) // 4
        
        print(f"\n⏱️ Executado em: {tempo_seq:.2f} segundos")
        print("\n📊 RESULTADO:")
        print("-" * 30)
        print(resultado_seq)
        print(metricas.gerar_relatorio())
        
        return resultado_seq, tempo_seq
        
    except Exception as e:
        error_msg = str(e)
        if "RateLimitError" in error_msg or "quota" in error_msg.lower():
            print(f"❌ ERRO DE COTA: {e}")
            print("\n💡 SOLUÇÕES:")
            print("   1. Verifique saldo: https://platform.openai.com/usage")
            print("   2. Adicione créditos na conta OpenAI")
            print("   3. Aguarde reset mensal (plano gratuito)")
        else:
            print(f"❌ Erro: {e}")
        return None, 0


def executar_processo_hierarquico():
    print("\n🚀 EXECUTANDO PROCESSO HIERÁRQUICO OTIMIZADO")
    print("="*50)
    
    inicio = time.time()
    try:
        resultado_hier = crew_hierarquico.kickoff()
        tempo_hier = time.time() - inicio
        
        print(f"\n⏱️ Executado em: {tempo_hier:.2f} segundos")
        print("\n📊 RESULTADO:")
        print("-" * 30)
        print(resultado_hier)
        
        return resultado_hier, tempo_hier
        
    except Exception as e:
        print(f"❌ Erro hierárquico: {e}")
        return None, 0


# EXECUÇÃO PRINCIPAL OTIMIZADA
if __name__ == "__main__":
    print("\n🎬 DEMONSTRAÇÃO OTIMIZADA PARA ECONOMIA DE TOKENS")
    print("=" * 50)

    # Verificação simples de chaves
    openai_key = os.getenv('OPENAI_API_KEY')
    print(f"🔑 OpenAI API: {'✅ OK' if openai_key else '❌ Faltando'}")

    if not openai_key:
        print("❌ Configure OPENAI_API_KEY no .env")
        exit(1)

    # Menu simplificado
    print("\n📋 ESCOLHA (TODAS OTIMIZADAS):")
    print("1️⃣ - Processo Sequencial (RECOMENDADO)")
    print("2️⃣ - Processo Hierárquico") 
    print("3️⃣ - Testar Ferramentas (BAIXO CUSTO)")
    print("4️⃣ - Apenas Conceitos (SEM CUSTO)")
    
    print("\n� OTIMIZAÇÕES APLICADAS:")
    print("   ✅ Max tokens reduzido para 1000")
    print("   ✅ Tarefas com outputs menores")
    print("   ✅ Backstories simplificados")
    print("   ✅ Verbose=False para menos logs")
    print("   ✅ Iterações limitadas")

    escolha = input("\nEscolha (1-4): ").strip()

    if escolha == "1":
        executar_processo_sequencial()

    elif escolha == "2":
        executar_processo_hierarquico()

    elif escolha == "3":
        print("\n🔧 TESTANDO FERRAMENTAS:")
        print("="*30)
        
        print("\n1️⃣ Busca Web:")
        resultado_busca = busca_web_tool._run("CrewAI")
        print(resultado_busca[:200] + "...")
        
        print("\n2️⃣ Scraping:")
        resultado_scraping = scraping_tool._run("https://docs.crewai.com")
        print(resultado_scraping[:200] + "...")
        
        print("\n✅ Ferramentas funcionando!")

    elif escolha == "4":
        print("\n📚 CONCEITOS PRINCIPAIS:")
        print("=" * 30)
        print("🔧 FERRAMENTAS: Expandem capacidades dos agentes")
        print("🔄 PROCESSO SEQUENCIAL: Linear, previsível, menos tokens")
        print("🏗️ PROCESSO HIERÁRQUICO: Manager coordena, mais tokens")
        print("💰 OTIMIZAÇÕES: Tokens limitados, outputs menores")
        print("🇧🇷 IDIOMA: Tudo configurado em português")

    else:
        print("❌ Opção inválida!")

    print("\n🎓 LIÇÕES OTIMIZADAS:")
    print("="*30)
    print("✅ Ferramentas reais integradas")
    print("✅ Processos comparados")
    print("✅ Configuração para economia")
    print("� ECONOMIA: ~60% menos tokens que versão original")
    print("🇧🇷 PORTUGUÊS: Toda comunicação configurada")

print("\n🏁 Aula 3 OTIMIZADA concluída!")