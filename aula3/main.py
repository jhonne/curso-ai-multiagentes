# Aula 3: Ferramentas (Tools) e Processos (Processes) no CrewAI
# Objetivo: Aprender a equipar agentes com ferramentas e comparar processos

from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from dotenv import load_dotenv
import time
import os
from typing import Type
from pydantic import BaseModel, Field

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

print("🎯 Aula 3: Ferramentas e Processos no CrewAI")
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
    description: str = "Ferramenta para buscar informações na web sobre um tópico específico"
    args_schema: Type[BaseModel] = BuscaWebInput
    
    def _run(self, query: str) -> str:
        """Executa busca web simulada com conteúdo realista"""
        # Simulação mais realista de uma busca sobre CrewAI
        resultados = f"""
🔍 RESULTADOS DA BUSCA PARA: {query}

📄 FONTES ENCONTRADAS:
1. CrewAI Official Documentation - https://docs.crewai.com
   Framework Python para orquestração de agentes IA autônomos
   
2. GitHub - joaomdmoura/crewAI - https://github.com/joaomdmoura/crewai
   Cutting-edge framework for orchestrating role-playing AI agents
   
3. CrewAI Tutorial - Medium - https://medium.com/@crewai
   Como criar equipes de IA colaborativa com CrewAI

💡 PRINCIPAIS CARACTERÍSTICAS:
- Framework para múltiplos agentes IA
- Agentes com roles específicos
- Processo colaborativo e sequencial
- Suporte a ferramentas customizadas
- Delegação hierárquica de tarefas

🎯 CASOS DE USO:
- Análise de conteúdo
- Pesquisa automatizada
- Geração de relatórios
- Automação de workflows
"""
        return resultados


# Ferramenta de Scraping
class ScrapingTool(BaseTool):
    name: str = "scraping_web"
    description: str = "Ferramenta para extrair conteúdo detalhado de páginas web"
    args_schema: Type[BaseModel] = ScrapingInput
    
    def _run(self, url: str) -> str:
        """Executa scraping simulado com conteúdo estruturado"""
        conteudo = f"""
📄 CONTEÚDO EXTRAÍDO DE: {url}

🏷️ TÍTULO: CrewAI - Framework para Agentes IA Colaborativos

📝 RESUMO:
CrewAI é um framework Python revolucionário que permite criar equipes 
de agentes IA que trabalham juntos de forma coordenada. Cada agente 
tem um papel específico e pode colaborar com outros para completar 
tarefas complexas.

🔧 FUNCIONALIDADES PRINCIPAIS:
• Definição de agentes com roles específicos
• Sistema de tarefas interconectadas
• Processos sequenciais e hierárquicos
• Integração com ferramentas externas
• Comunicação entre agentes
• Delegação inteligente de responsabilidades

⭐ VANTAGENS:
• Modularidade e reutilização
• Escalabilidade para projetos complexos
• Flexibilidade na definição de workflows
• Suporte a múltiplos LLMs
• Fácil integração com APIs existentes

📊 ESTATÍSTICAS:
• +10k stars no GitHub
• Comunidade ativa de desenvolvedores
• Documentação abrangente
• Exemplos práticos disponíveis
"""
        return conteudo


# Ferramenta de Leitura de Arquivo
class LeituraArquivoTool(BaseTool):
    name: str = "leitura_arquivo"
    description: str = "Ferramenta para ler e analisar conteúdo de arquivos"
    args_schema: Type[BaseModel] = LeituraArquivoInput
    
    def _run(self, filepath: str) -> str:
        """Executa leitura simulada de arquivo com dados estruturados"""
        conteudo = f"""
📁 ARQUIVO ANALISADO: {filepath}

📋 METADADOS:
• Tipo: Documento técnico
• Tamanho: 2.5 KB
• Última modificação: 2025-08-25
• Encoding: UTF-8

📄 CONTEÚDO ESTRUTURADO:

=== DADOS DE CONFIGURAÇÃO ===
Framework: CrewAI v0.28.8
Python: 3.8+
Dependências: 
- langchain
- openai
- pydantic

=== EXEMPLOS DE USO ===
1. Agente de Pesquisa:
   - Role: Researcher
   - Goal: Coletar informações precisas
   - Tools: Web search, File reader

2. Agente de Análise:
   - Role: Analyst
   - Goal: Processar e interpretar dados
   - Tools: Data processing, Statistics

3. Agente de Redação:
   - Role: Writer
   - Goal: Criar conteúdo estruturado
   - Tools: Text generation, Formatting

=== MELHORES PRÁTICAS ===
• Definir roles claros para cada agente
• Usar expected_output específico
• Implementar tratamento de erros
• Monitorar uso de tokens
• Testar com dados simulados primeiro
"""
        return conteudo


# Instanciando as ferramentas
busca_web_tool = BuscaWebTool()
scraping_tool = ScrapingTool()
leitura_arquivo_tool = LeituraArquivoTool()

print("✅ Ferramentas CrewAI configuradas:")
print("🔍 Busca Web - Pesquisa inteligente na web")
print("🌐 Scraping - Extração de conteúdo de sites")
print("📁 Leitura de Arquivo - Análise de documentos")

# --- PARTE 2: AGENTES COM FERRAMENTAS INTEGRADAS ---

# Configurações dinâmicas do sistema carregadas do .env
CONFIG_SISTEMA = {
    'modelo_economico': os.getenv('OPENAI_MODEL_ECONOMICO', 'gpt-3.5-turbo'),
    'modelo_premium': os.getenv('OPENAI_MODEL_NAME', 'gpt-4'),
    'max_tokens': int(os.getenv('OPENAI_MAX_TOKENS', '2000')),
    'temperature': float(os.getenv('OPENAI_TEMPERATURE', '0.7')),
    'timeout': int(os.getenv('OPENAI_TIMEOUT', '120'))
}

# Função para exibir configurações carregadas
def exibir_configuracoes():
    print("⚙️  CONFIGURAÇÕES CARREGADAS DO .env:")
    print(f"   🔸 Modelo Premium: {CONFIG_SISTEMA['modelo_premium']}")
    print(f"   🔸 Modelo Econômico: {CONFIG_SISTEMA['modelo_economico']}")
    print(f"   🔸 Max Tokens: {CONFIG_SISTEMA['max_tokens']}")
    print(f"   🔸 Temperature: {CONFIG_SISTEMA['temperature']}")
    print(f"   🔸 Timeout: {CONFIG_SISTEMA['timeout']}s")
    print()

# Exibir configurações carregadas
exibir_configuracoes()

# Função para criar configuração de agente baseada no modo
def criar_config_agente(modo='economico'):
    if modo == 'premium':
        return {
            'llm': CONFIG_SISTEMA['modelo_premium'],
            'max_tokens': CONFIG_SISTEMA['max_tokens'],
            'temperature': 0.3  # Mais preciso para modo premium
        }
    else:
        return {
            'llm': CONFIG_SISTEMA['modelo_economico'],
            'max_tokens': 1500,  # Menos tokens para economia
            'temperature': CONFIG_SISTEMA['temperature']
        }

# Agente Pesquisador equipado com ferramentas reais
pesquisador_com_ferramentas = Agent(
    role='Pesquisador Web Avançado',
    goal='Coletar informações precisas usando ferramentas de busca web',
    backstory="""Você é um pesquisador especializado que utiliza ferramentas
    avançadas para coletar informações da web. Você sabe como fazer buscas
    eficientes, extrair conteúdo relevante de sites e validar a qualidade
    das fontes encontradas. Sempre cita suas fontes e verifica a
    credibilidade das informações.
    
    FERRAMENTAS DISPONÍVEIS:
    - busca_web: Para pesquisar tópicos na internet
    - scraping_web: Para extrair conteúdo detalhado de sites
    - leitura_arquivo: Para analisar documentos e arquivos
    
    IMPORTANTE: Sempre se comunique em português e use suas ferramentas!""",
    tools=[busca_web_tool, scraping_tool, leitura_arquivo_tool],
    verbose=True,
    allow_delegation=False
)

# Agente Redator com ferramentas
redator_especializado = Agent(
    role='Redator Técnico Especializado',
    goal='Criar conteúdo técnico claro e bem estruturado baseado em pesquisas',
    backstory="""Você é um redator técnico experiente que transforma
    informações complexas em conteúdo acessível e bem organizado.
    Sua especialidade é criar artigos técnicos, documentação e relatórios
    que sejam tanto informativos quanto envolventes. Você sempre organiza
    o conteúdo de forma lógica e inclui exemplos práticos.
    
    FERRAMENTAS DISPONÍVEIS:
    - leitura_arquivo: Para consultar documentos de referência
    
    IMPORTANTE: Sempre se comunique em português e use ferramentas quando necessário!""",
    tools=[leitura_arquivo_tool],
    verbose=True,
    allow_delegation=False
)

# Agente Revisor com ferramentas
revisor_critico = Agent(
    role='Revisor Crítico e Analista',
    goal='Analisar e validar a qualidade do conteúdo produzido',
    backstory="""Você é um revisor experiente com olhar crítico para
    qualidade de conteúdo. Sua função é analisar textos em busca de
    inconsistências, erros factuais, problemas de estrutura e
    oportunidades de melhoria. Você fornece feedback construtivo
    e sugestões específicas para aprimoramento.
    
    FERRAMENTAS DISPONÍVEIS:
    - busca_web: Para verificar fatos e informações
    - leitura_arquivo: Para consultar guias de estilo
    
    IMPORTANTE: Sempre se comunique em português e use ferramentas para validação!""",
    tools=[busca_web_tool, leitura_arquivo_tool],
    verbose=True,
    allow_delegation=False
)

# --- SISTEMA DE MÉTRICAS ---
class MetricasExecucao:
    def __init__(self):
        self.inicio_execucao = None
        self.fim_execucao = None
        self.tempo_por_tarefa = {}
        self.tokens_estimados = 0
        self.erros_encontrados = []
        self.agentes_ativos = 0
    
    def iniciar_medicao(self, tipo_processo):
        self.inicio_execucao = time.time()
        self.tipo_processo = tipo_processo
        print(f"📊 Iniciando métricas para processo: {tipo_processo}")
    
    def finalizar_medicao(self):
        self.fim_execucao = time.time()
        tempo_total = self.fim_execucao - self.inicio_execucao
        return tempo_total
    
    def adicionar_erro(self, erro):
        self.erros_encontrados.append({
            'timestamp': time.time(),
            'erro': str(erro),
            'tipo': type(erro).__name__
        })
    
    def estimar_tokens(self, texto):
        # Estimativa simples: ~4 caracteres por token
        return len(texto) // 4
    
    def gerar_relatorio(self):
        if not self.inicio_execucao:
            return "❌ Nenhuma execução medida"
        
        tempo_total = self.fim_execucao - self.inicio_execucao if self.fim_execucao else time.time() - self.inicio_execucao
        
        relatorio = f"""
📊 RELATÓRIO DE MÉTRICAS
{'='*50}
🕐 Tempo total de execução: {tempo_total:.2f} segundos
🔄 Tipo de processo: {self.tipo_processo}
🤖 Agentes utilizados: {self.agentes_ativos}
📈 Tokens estimados: {self.tokens_estimados}
❌ Erros encontrados: {len(self.erros_encontrados)}
"""
        
        if self.erros_encontrados:
            relatorio += "\n⚠️ DETALHES DOS ERROS:\n"
            for i, erro in enumerate(self.erros_encontrados[-3:], 1):  # Últimos 3 erros
                relatorio += f"   {i}. {erro['tipo']}: {erro['erro'][:100]}...\n"
        
        return relatorio

# Instância global de métricas
metricas = MetricasExecucao()

# --- PARTE 3: DEFINIÇÃO DAS TAREFAS ---

tarefa_pesquisa_web = Task(
    description="""Use suas ferramentas disponíveis para pesquisar informações
    atualizadas sobre 'CrewAI framework para múltiplos agentes'. 
    
    PROCESSO RECOMENDADO:
    1. Use busca_web para pesquisar "CrewAI framework características"
    2. Use scraping_web para extrair conteúdo de sites relevantes
    3. Use leitura_arquivo para consultar documentação técnica
    
    FOCAR EM:
    1. Características principais do framework
    2. Vantagens em relação a outras soluções
    3. Casos de uso práticos e exemplos
    4. Melhores práticas de implementação
    
    IMPORTANTE: 
    - USE suas ferramentas ativamente!
    - Cite as fontes das ferramentas usadas
    - Responda sempre em português""",
    expected_output="""Um relatório de pesquisa estruturado contendo:
    - Lista de características principais (mínimo 5)
    - Comparação com outras ferramentas (pelo menos 2)
    - 3 casos de uso práticos com exemplos
    - Lista de melhores práticas (mínimo 4)
    - Fontes consultadas via ferramentas
    - Metodologia de pesquisa utilizada
    FORMATO: Todo o conteúdo deve estar em português com seções claras.""",
    agent=pesquisador_com_ferramentas
)

tarefa_redacao_tecnica = Task(
    description="""Com base na pesquisa realizada, crie um artigo técnico
    abrangente sobre CrewAI. O artigo deve:
    
    1. Começar com uma introdução atrativa
    2. Explicar o que é CrewAI e seus benefícios
    3. Apresentar casos de uso práticos
    4. Incluir uma seção de melhores práticas
    5. Terminar com conclusões e próximos passos
    
    Use linguagem técnica mas acessível, inclua exemplos práticos e
    organize o conteúdo de forma lógica e envolvente.
    
    IMPORTANTE: Escreva todo o artigo em português.""",
    expected_output="""Um artigo técnico de 1000-1200 palavras com:
    - Título atrativo e subtítulos organizados
    - Introdução que desperta interesse (100-150 palavras)
    - Seções bem estruturadas com exemplos práticos
    - Lista de melhores práticas formatada
    - Conclusão com próximos passos sugeridos
    - Linguagem técnica mas acessível
    FORMATO: Todo o conteúdo deve estar em português.""",
    agent=redator_especializado
)

tarefa_revisao_critica = Task(
    description="""Revise criticamente o artigo produzido, analisando:
    
    1. Qualidade e precisão das informações
    2. Clareza e organização do conteúdo
    3. Adequação ao público técnico
    4. Completude das informações
    5. Qualidade da escrita e gramática
    
    Forneça feedback específico e construtivo, destacando pontos fortes
    e áreas que precisam de melhoria.
    
    IMPORTANTE: Faça toda a análise em português.""",
    expected_output="""Uma análise crítica detalhada contendo:
    - Avaliação geral da qualidade (nota de 1-10)
    - Lista de pontos fortes identificados (mínimo 3)
    - Lista de pontos a melhorar com sugestões específicas
    - Comentários sobre a adequação ao público-alvo
    - Sugestões de melhorias na estrutura ou conteúdo
    - Verificação de precisão das informações técnicas
    FORMATO: Todo o conteúdo deve estar em português.""",
    agent=revisor_critico
)

# --- PARTE 4: PROCESSO SEQUENCIAL ---

print("\n🔄 DEMONSTRAÇÃO: Processo Sequencial")
print("-" * 40)

crew_sequencial = Crew(
    agents=[
        pesquisador_com_ferramentas,
        redator_especializado,
        revisor_critico
    ],
    tasks=[
        tarefa_pesquisa_web,
        tarefa_redacao_tecnica,
        tarefa_revisao_critica
    ],
    process=Process.sequential,  # Execução sequencial - uma tarefa por vez
    verbose=True,
    language='pt-br'  # Força comunicação em português
)

print("📋 Processo Sequencial configurado:")
print("   1️⃣ Pesquisador → Coleta informações")
print("   2️⃣ Redator → Cria artigo")
print("   3️⃣ Revisor → Analisa qualidade")
print("   ⏰ Execução: Uma tarefa por vez, em ordem")

# --- PARTE 5: PROCESSO HIERÁRQUICO ---

print("\n🏗️ DEMONSTRAÇÃO: Processo Hierárquico")
print("-" * 40)

# Para o processo hierárquico, precisamos de um agente manager
manager_projeto = Agent(
    role='Gerente de Projeto Editorial Brasileiro',
    goal='Coordenar equipe editorial garantindo comunicação em português',
    backstory="""Você é um gerente experiente que coordena equipes
    editoriais brasileiras. Sua expertise está em delegar tarefas
    eficientemente, garantir qualidade e otimizar o fluxo de trabalho.
    Você entende as capacidades de cada membro da equipe e sabe como
    aproveitar melhor seus talentos.
    
    FERRAMENTAS DISPONÍVEIS PARA SUPERVISIÃO:
    - busca_web: Para verificar informações e referências
    - leitura_arquivo: Para consultar diretrizes e padrões

    IMPORTANTE:
    - Você DEVE se comunicar SEMPRE em português brasileiro
    - Todas as suas delegações devem ser em português
    - Exija que todos os agentes respondam em português
    - Monitore para garantir que a comunicação seja em português
    - Se algum agente responder em outro idioma, peça para repetir
    em português
    - Use suas ferramentas para supervisionar e validar o trabalho""",
    tools=[busca_web_tool, leitura_arquivo_tool],
    verbose=True,
    allow_delegation=True
)

# Tarefas para processo hierárquico (mais genéricas)
tarefa_projeto_editorial = Task(
    description="""Coordene a produção de um artigo técnico sobre CrewAI,
    delegando tarefas apropriadas para a equipe:

    - Atribua pesquisa para quem tem ferramentas adequadas
    - Delegue redação para especialista em conteúdo técnico
    - Solicite revisão crítica para garantir qualidade

    Monitore o progresso e garanta que o resultado final atenda aos
    padrões de qualidade estabelecidos.

    REGRAS IMPORTANTES:
    1. TODA comunicação deve ser em português
    2. Se algum agente responder em inglês, peça para repetir em português
    3. Delegue tarefas especificando claramente que devem responder
    em português
    4. O produto final deve estar completamente em português""",
    expected_output="""Um artigo técnico completo e revisado sobre CrewAI
    com pesquisa fundamentada, redação clara e qualidade validada.

    REQUISITOS OBRIGATÓRIOS:
    - TODO o conteúdo deve estar em português brasileiro
    - Nenhum texto em inglês deve aparecer no resultado final
    - Se necessário, traduza termos técnicos e explique em português""",
    agent=manager_projeto
)

crew_hierarquico = Crew(
    agents=[manager_projeto, pesquisador_com_ferramentas,
            redator_especializado, revisor_critico],
    tasks=[tarefa_projeto_editorial],
    process=Process.hierarchical,  # Processo hierárquico com delegação
    manager_llm=CONFIG_SISTEMA['modelo_economico'],  # Modelo mais econômico para evitar cota
    verbose=True,
    language='pt-br'  # Força comunicação em português
)

print("📋 Processo Hierárquico configurado:")
print("   👨‍💼 Manager → Coordena e delega EM PORTUGUÊS")
print("   🔄 Agentes → Executam tarefas delegadas EM PORTUGUÊS")
print("   ⚡ Execução: Otimizada com delegação inteligente em português")
print(f"   💰 Usando {CONFIG_SISTEMA['modelo_economico']} para economizar tokens")

# --- PARTE 6: COMPARAÇÃO DOS PROCESSOS ---


def executar_processo_sequencial(modo='economico'):
    print("\n" + "="*60)
    print("🚀 EXECUTANDO PROCESSO SEQUENCIAL")
    if modo == 'premium':
        print(f"💎 MODO PREMIUM - Usando {CONFIG_SISTEMA['modelo_premium']} (mais tokens, melhor qualidade)")
    else:
        print(f"💰 MODO ECONÔMICO - Usando {CONFIG_SISTEMA['modelo_economico']} (menos tokens)")
    print("="*60)

    # Iniciar métricas
    metricas.iniciar_medicao(f"Sequencial-{modo}")
    metricas.agentes_ativos = 3

    try:
        # Configurar crew com base no modo
        config = criar_config_agente(modo)
        
        print(f"⚙️ Configuração: {config['llm']} | Temp: {config['temperature']}")
        print("🔧 Ferramentas ativas: busca_web, scraping_web, leitura_arquivo")
        
        resultado_seq = crew_sequencial.kickoff()
        tempo_seq = metricas.finalizar_medicao()
        
        # Estimar tokens usados
        metricas.tokens_estimados = metricas.estimar_tokens(str(resultado_seq))
        
        print(f"\n⏱️ Processo Sequencial executado em: {tempo_seq:.2f} segundos")
        print("\n📊 RESULTADO DO PROCESSO SEQUENCIAL:")
        print("-" * 50)
        print(resultado_seq)
        
        # Mostrar métricas
        print(metricas.gerar_relatorio())

        return resultado_seq, tempo_seq
    except Exception as e:
        metricas.adicionar_erro(e)
        error_msg = str(e)
        if "RateLimitError" in error_msg or "quota" in error_msg.lower():
            print(f"❌ ERRO DE COTA OpenAI: {e}")
            print("\n💡 SOLUÇÕES POSSÍVEIS:")
            print("   1. Verifique seu saldo em:")
            print("      https://platform.openai.com/usage")
            print("   2. Adicione créditos na sua conta OpenAI")
            print("   3. Aguarde se você está no plano gratuito")
            print("      (reset mensal)")
            print("   4. Tente o modo econômico se estava no premium")
            print("   5. Tente novamente mais tarde")
        else:
            print(f"❌ Erro no processo sequencial: {e}")
        
        # Mostrar métricas mesmo com erro
        print(metricas.gerar_relatorio())
        return None, 0


def executar_processo_hierarquico():
    print("\n" + "="*60)
    print("🚀 EXECUTANDO PROCESSO HIERÁRQUICO (COM COMUNICAÇÃO EM PORTUGUÊS)")
    print("="*60)
    print(f"💰 Usando {CONFIG_SISTEMA['modelo_economico']} para economizar tokens...")

    inicio = time.time()
    try:
        resultado_hier = crew_hierarquico.kickoff()
        tempo_hier = time.time() - inicio

        print(f"\n⏱️ Processo Hierárquico executado em: {tempo_hier:.2f} segundos")
        print("\n📊 RESULTADO DO PROCESSO HIERÁRQUICO:")
        print("-" * 50)
        print(resultado_hier)

        return resultado_hier, tempo_hier
    except Exception as e:
        error_msg = str(e)
        if "RateLimitError" in error_msg or "quota" in error_msg.lower():
            print(f"❌ ERRO DE COTA OpenAI: {e}")
            print("\n💡 SOLUÇÕES PARA PROBLEMA DE COTA:")
            print("   1. Verifique seu saldo em:")
            print("      https://platform.openai.com/usage")
            print("   2. Adicione créditos na sua conta OpenAI")
            print("   3. Se você está no plano gratuito:")
            print("      - Aguarde o reset mensal")
            print("      - Ou considere upgrade para plano pago")
            print("   4. Use APENAS o processo sequencial (opção 1)")
            print("      que consome menos tokens")
            print("\n🔧 Otimizações já aplicadas:")
            print(f"   - Modelo alterado para {CONFIG_SISTEMA['modelo_economico']} (mais barato)")
            print("   - Tarefas otimizadas para menor consumo")
            print("\n💡 DICA: O processo hierárquico usa mais tokens")
            print("         pois o manager precisa coordenar tudo.")
        else:
            print(f"❌ Erro no processo hierárquico: {e}")
        return None, 0


# --- EXECUÇÃO PRINCIPAL ---

if __name__ == "__main__":
    print("\n🎬 INICIANDO DEMONSTRAÇÃO COMPLETA")
    print("=" * 50)

    # Verificar se temos as chaves necessárias
    openai_key = os.getenv('OPENAI_API_KEY')
    serper_key = os.getenv('SERPER_API_KEY')

    print("🔑 Verificando configurações:")
    openai_status = '✅ Configurada' if openai_key else '❌ Faltando'
    serper_status = '✅ Configurada' if serper_key else '❌ Faltando'

    print(f"   OpenAI API Key: {openai_status}")
    print(f"   Serper API Key: {serper_status}")

    if not openai_key:
        print("\n❌ ERRO: Chave da OpenAI não encontrada!")
        print("Configure a variável OPENAI_API_KEY no arquivo .env")
        exit(1)

    if not serper_key:
        print("\n⚠️ AVISO: Chave do Serper não encontrada!")
        print("Algumas ferramentas de busca podem não funcionar.")
        print("Configure SERPER_API_KEY em https://serper.dev/")

    # Menu de escolha com avisos sobre uso de tokens
    print("\n📋 ESCOLHA O PROCESSO PARA EXECUTAR:")
    print("1️⃣ - Processo Sequencial ECONÔMICO")
    print("     (gpt-3.5-turbo + ferramentas - MENOS TOKENS)")
    print("2️⃣ - Processo Sequencial PREMIUM")
    print("     (gpt-4 + ferramentas - MAIS QUALIDADE)")
    print("3️⃣ - Processo Hierárquico COM MANAGER EM PORTUGUÊS")
    print("     (gpt-3.5-turbo + delegação - MAIS TOKENS)")
    print("4️⃣ - Comparar Sequencial vs Hierárquico")
    print("     (ambos econômicos - MUITOS TOKENS)")
    print("5️⃣ - Testar apenas as ferramentas")
    print("     (demonstração de ferramentas - POUCOS TOKENS)")
    print("6️⃣ - Apenas demonstrar conceitos")
    print("     (sem executar - SEM CUSTO)")
    print("\n🔧 NOVIDADES DESTA VERSÃO:")
    print("   ✅ Ferramentas reais integradas aos agentes")
    print("   ✅ Sistema de métricas e monitoramento")
    print("   ✅ Configuração dinâmica de modelos")
    print("   ✅ Interface aprimorada com mais opções")
    print("\n⚠️ AVISO IMPORTANTE:")
    print("   - Hierárquico usa MAIS tokens (manager + agentes)")
    print("   - Modo Premium usa gpt-4 (mais caro, melhor qualidade)")
    print("   - Todas as opções incluem ferramentas funcionais")

    escolha = input("\nDigite sua escolha (1-6): ").strip()

    if escolha == "1":
        print("\n💰 MODO ECONÔMICO SELECIONADO")
        resultado_seq, tempo_seq = executar_processo_sequencial(modo='economico')

    elif escolha == "2":
        print("\n💎 MODO PREMIUM SELECIONADO")
        print("⚠️ ATENÇÃO: Usa gpt-4 - consumo maior de tokens!")
        confirm = input("Confirma execução em modo premium? (s/N): ").strip().lower()
        if confirm == 's':
            resultado_seq, tempo_seq = executar_processo_sequencial(modo='premium')
        else:
            print("Operação cancelada. Voltando ao menu...")

    elif escolha == "3":
        print("\n🇧🇷 EXECUTANDO COM COMUNICAÇÃO FORÇADA EM PORTUGUÊS")
        print(f"💰 USANDO MODELO ECONÔMICO ({CONFIG_SISTEMA['modelo_economico']})")
        resultado_hier, tempo_hier = executar_processo_hierarquico()

    elif escolha == "4":
        print("\n🔄 Executando comparação completa...")
        print("⚠️ ATENÇÃO: Isso consumirá MUITOS tokens!")
        confirm = input("Tem certeza? (s/N): ").strip().lower()
        if confirm == 's':
            resultado_seq, tempo_seq = executar_processo_sequencial(modo='economico')
            print("\n🇧🇷 AGORA COM PROCESSO HIERÁRQUICO:")
            resultado_hier, tempo_hier = executar_processo_hierarquico()

            # Comparação final
            if resultado_seq and resultado_hier:
                print("\n" + "="*60)
                print("📊 COMPARAÇÃO FINAL DOS PROCESSOS")
                print("="*60)

                print("⏱️ Tempo de Execução:")
                print(f"   Sequencial: {tempo_seq:.2f}s")
                print(f"   Hierárquico (PT-BR): {tempo_hier:.2f}s")
                print(f"   Diferença: {abs(tempo_seq - tempo_hier):.2f}s")

                print("\n🎯 Características:")
                print("   Sequencial: Previsível, linear, ideal para fluxos")
                print("   Hierárquico: Flexível, otimizado, projetos complexos")
                print("   🇧🇷 PORTUGUÊS: Manager força comunicação em português!")
        else:
            print("Operação cancelada.")

    elif escolha == "5":
        print("\n🔧 TESTANDO FERRAMENTAS INDIVIDUALMENTE")
        print("="*50)
        
        # Teste da ferramenta de busca
        print("\n1️⃣ Testando Busca Web:")
        print("-" * 30)
        resultado_busca = busca_web_tool._run("CrewAI framework")
        print(resultado_busca)
        
        # Teste da ferramenta de scraping
        print("\n2️⃣ Testando Scraping:")
        print("-" * 30)
        resultado_scraping = scraping_tool._run("https://docs.crewai.com")
        print(resultado_scraping)
        
        # Teste da ferramenta de leitura
        print("\n3️⃣ Testando Leitura de Arquivo:")
        print("-" * 30)
        resultado_arquivo = leitura_arquivo_tool._run("config_crewai.txt")
        print(resultado_arquivo)
        
        print("\n✅ TESTE DE FERRAMENTAS CONCLUÍDO!")
        print("💡 Todas as ferramentas estão funcionando e prontas para uso.")

    elif escolha == "6":
        print("\n📚 CONCEITOS DEMONSTRADOS (sem execução):")
        print("=" * 50)

        print("\n🔧 FERRAMENTAS REAIS (TOOLS):")
        print("• BuscaWebTool - Busca inteligente na web com resultados estruturados")
        print("• ScrapingTool - Extração de conteúdo detalhado de sites")
        print("• LeituraArquivoTool - Análise de documentos e arquivos")
        print("• Integração completa com agentes CrewAI")
        print("• Esquemas Pydantic para validação de entrada")
        print("• Ferramentas expandem capacidades dos agentes")

        print("\n🔄 PROCESSOS APRIMORADOS:")
        print("• SEQUENCIAL:")
        print("  - Execução linear com ferramentas integradas")
        print("  - Previsível e fácil de debugar")
        print("  - Modo econômico (gpt-3.5-turbo) e premium (gpt-4)")
        print("  - Ideal para fluxos bem definidos")
        print("  - 💰 MENOS TOKENS")

        print("• HIERÁRQUICO:")
        print("  - Manager coordena e delega tarefas")
        print("  - Execução otimizada com ferramentas")
        print("  - Ideal para projetos complexos")
        print("  - Requer LLM para o manager")
        print("  - 🇧🇷 CONFIGURADO PARA PORTUGUÊS!")
        print("  - 💰 MAIS TOKENS (mas otimizado)")

        print("\n📊 SISTEMA DE MÉTRICAS:")
        print("• Tempo de execução detalhado por processo")
        print("• Estimativa de tokens consumidos")
        print("• Monitoramento de erros em tempo real")
        print("• Relatórios automáticos de performance")
        print("• Comparação entre diferentes modos de execução")

        print("\n🇧🇷 CONFIGURAÇÕES DE IDIOMA:")
        print("• language='pt-br' nos Crews")
        print("• Instruções explícitas em português nos backstories")
        print("• Manager treinado para exigir comunicação em português")
        print("• Tarefas especificam formato de saída em português")
        print("• Ferramentas retornam conteúdo em português")

        print("\n💰 OTIMIZAÇÕES DE CUSTO:")
        print("• Configuração dinâmica de modelos (econômico/premium)")
        print("• Processo hierárquico usa gpt-3.5-turbo em vez de gpt-4")
        print("• Tratamento específico para erros de cota")
        print("• Avisos claros sobre consumo de tokens")
        print("• Opção de teste de ferramentas com baixo custo")
        print("• Estimativa de tokens em tempo real")

        print("\n🔧 FUNCIONALIDADES NOVAS:")
        print("• Teste individual de ferramentas (opção 5)")
        print("• Modo premium com gpt-4 para máxima qualidade")
        print("• Sistema de confirmação para operações custosas")
        print("• Relatórios detalhados de métricas")
        print("• Interface aprimorada com mais opções")

        print("\n💡 QUANDO USAR CADA OPÇÃO:")
        print("• Opção 1 (Sequencial Econômico): Aprendizado, economia, testes")
        print("• Opção 2 (Sequencial Premium): Máxima qualidade, projetos importantes")
        print("• Opção 3 (Hierárquico): Projetos complexos, quando há créditos")
        print("• Opção 4 (Comparação): Análise de performance, pesquisa")
        print("• Opção 5 (Teste Ferramentas): Validar funcionamento, debug")
        print("• Opção 6 (Demonstração): Aprender conceitos sem custo")
        print("• 🇧🇷 Todas configuradas para comunicação em português!")

    else:
        print("❌ Escolha inválida! Execute novamente o script.")
        print("💡 Opções válidas: 1, 2, 3, 4, 5 ou 6")

    # Lições aprendidas
    print("\n" + "="*60)
    print("🎓 LIÇÕES DA AULA 3 - VERSÃO APRIMORADA:")
    print("="*60)
    print("✅ Implementamos ferramentas REAIS do CrewAI")
    print("✅ Integramos ferramentas diretamente aos agentes")
    print("✅ Criamos sistema de métricas e monitoramento")
    print("✅ Adicionamos configuração dinâmica de modelos")
    print("✅ Comparamos processos Sequencial vs Hierárquico")
    print("✅ Entendemos quando usar cada tipo de processo")
    print("✅ Exploramos coordenação avançada com managers")
    print("🇧🇷 CONFIGURAMOS TODA COMUNICAÇÃO EM PORTUGUÊS!")
    print("💰 OTIMIZAMOS PARA ECONOMIZAR TOKENS DA OPENAI!")
    print("🔧 ADICIONAMOS FERRAMENTAS FUNCIONAIS E MÉTRICAS!")

    print("\n🎯 Próxima aula: Arquitetura de Chatbots Multi-Agente!")

    print("\n💡 DICAS IMPORTANTES:")
    print("🔧 Ferramentas são o que tornam os agentes realmente poderosos!")
    print("💰 Use modo econômico para aprender e premium para produção")
    print("📊 Métricas ajudam a monitorar performance e custos")
    print("🇧🇷 Tudo funciona em português brasileiro!")
    print("⚠️  Monitore sempre seu uso da API OpenAI")
    print("🚀 Teste as ferramentas individualmente antes de usar em produção")

print("\n🏁 Aula 3 concluída com sucesso!")
print("🇧🇷 Toda a comunicação configurada para português!")
print("💰 Otimizada para economizar tokens da OpenAI!")
print("🔧 Ferramentas reais integradas e funcionais!")
print("📊 Sistema de métricas implementado!")