# Aula 3: Ferramentas (Tools) e Processos (Processes) no CrewAI
# Objetivo: Aprender a equipar agentes com ferramentas e comparar processos

from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import time
import os
import requests
from bs4 import BeautifulSoup
from pathlib import Path

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

print("🎯 Aula 3: Ferramentas e Processos no CrewAI")
print("=" * 50)

# --- PARTE 1: SIMULAÇÃO DE FERRAMENTAS ---
print("🔧 Configurando ferramentas simuladas...")

# Simulação de ferramentas usando bibliotecas nativas
def simular_busca_web(query):
    """Simula uma busca na web"""
    return f"Resultados simulados para: {query}. CrewAI é um framework..."

def simular_scraping(url):
    """Simula extração de conteúdo de website"""
    return f"Conteúdo simulado de {url}: Artigo sobre CrewAI e suas capacidades..."

def simular_leitura_arquivo(filepath):
    """Simula leitura de arquivo"""
    return f"Conteúdo simulado do arquivo {filepath}: Dados de exemplo..."

print("✅ Simulações de ferramentas configuradas:")
print("✅ Busca Web Simulada")
print("✅ Scraping Simulado") 
print("✅ Leitura de Arquivo Simulada")

# --- PARTE 2: AGENTES COM FERRAMENTAS ---

# Agente Pesquisador equipado com ferramentas de busca
pesquisador_com_ferramentas = Agent(
    role='Pesquisador Web Avançado',
    goal='Coletar informações precisas e atualizadas usando ferramentas de busca na web',
    backstory="""Você é um pesquisador especializado que utiliza ferramentas
    avançadas para coletar informações da web. Você sabe como fazer buscas
    eficientes, extrair conteúdo relevante de sites e validar a qualidade
    das fontes encontradas. Sempre cita suas fontes e verifica a 
    credibilidade das informações.""",
    verbose=True,
    allow_delegation=False
)

# Agente Redator
redator_especializado = Agent(
    role='Redator Técnico Especializado',
    goal='Criar conteúdo técnico claro e bem estruturado baseado em pesquisas',
    backstory="""Você é um redator técnico experiente que transforma
    informações complexas em conteúdo acessível e bem organizado.
    Sua especialidade é criar artigos técnicos, documentação e relatórios
    que sejam tanto informativos quanto envolventes. Você sempre organiza
    o conteúdo de forma lógica e inclui exemplos práticos.""",
    verbose=True,
    allow_delegation=False
)

# Agente Revisor
revisor_critico = Agent(
    role='Revisor Crítico e Analista',
    goal='Analisar e validar a qualidade do conteúdo produzido',
    backstory="""Você é um revisor experiente com olhar crítico para
    qualidade de conteúdo. Sua função é analisar textos em busca de
    inconsistências, erros factuais, problemas de estrutura e
    oportunidades de melhoria. Você fornece feedback construtivo
    e sugestões específicas para aprimoramento.""",
    verbose=True,
    allow_delegation=False
)

# --- PARTE 3: DEFINIÇÃO DAS TAREFAS ---

tarefa_pesquisa_web = Task(
    description="""Use as ferramentas de busca para pesquisar informações 
    atualizadas sobre 'CrewAI framework para múltiplos agentes'. Foque em:
    
    1. Características principais do framework
    2. Vantagens em relação a outras soluções
    3. Casos de uso práticos e exemplos
    4. Melhores práticas de implementação
    
    Use a ferramenta de busca para encontrar artigos relevantes e, se necessário,
    use a ferramenta de scraping para extrair conteúdo detalhado dos sites
    mais promissores.""",
    expected_output="""Um relatório de pesquisa estruturado contendo:
    - Lista de características principais (mínimo 5)
    - Comparação com outras ferramentas (pelo menos 2)
    - 3 casos de uso práticos com exemplos
    - Lista de melhores práticas (mínimo 4)
    - Links das fontes utilizadas
    - Avaliação da credibilidade de cada fonte""",
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
    organize o conteúdo de forma lógica e envolvente.""",
    expected_output="""Um artigo técnico de 1000-1200 palavras com:
    - Título atrativo e subtítulos organizados
    - Introdução que desperta interesse (100-150 palavras)
    - Seções bem estruturadas com exemplos práticos
    - Lista de melhores práticas formatada
    - Conclusão com próximos passos sugeridos
    - Linguagem técnica mas acessível""",
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
    e áreas que precisam de melhoria.""",
    expected_output="""Uma análise crítica detalhada contendo:
    - Avaliação geral da qualidade (nota de 1-10)
    - Lista de pontos fortes identificados (mínimo 3)
    - Lista de pontos a melhorar com sugestões específicas
    - Comentários sobre a adequação ao público-alvo
    - Sugestões de melhorias na estrutura ou conteúdo
    - Verificação de precisão das informações técnicas""",
    agent=revisor_critico
)

# --- PARTE 4: PROCESSO SEQUENCIAL ---

print("\n🔄 DEMONSTRAÇÃO: Processo Sequencial")
print("-" * 40)

crew_sequencial = Crew(
    agents=[pesquisador_com_ferramentas, redator_especializado, revisor_critico],
    tasks=[tarefa_pesquisa_web, tarefa_redacao_tecnica, tarefa_revisao_critica],
    process=Process.sequential,  # Execução sequencial - uma tarefa por vez
    verbose=True
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
    role='Gerente de Projeto Editorial',
    goal='Coordenar e otimizar o trabalho da equipe editorial',
    backstory="""Você é um gerente experiente que coordena equipes editoriais.
    Sua expertise está em delegar tarefas eficientemente, garantir qualidade
    e otimizar o fluxo de trabalho. Você entende as capacidades de cada
    membro da equipe e sabe como aproveitar melhor seus talentos.""",
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
    padrões de qualidade estabelecidos.""",
    expected_output="""Um artigo técnico completo e revisado sobre CrewAI
    com pesquisa fundamentada, redação clara e qualidade validada.""",
    agent=manager_projeto
)

crew_hierarquico = Crew(
    agents=[manager_projeto, pesquisador_com_ferramentas, redator_especializado, revisor_critico],
    tasks=[tarefa_projeto_editorial],
    process=Process.hierarchical,  # Processo hierárquico com delegação
    manager_llm='gpt-4',  # LLM para o manager (pode usar gpt-3.5-turbo se preferir)
    verbose=True
)

print("📋 Processo Hierárquico configurado:")
print("   👨‍💼 Manager → Coordena e delega")
print("   🔄 Agentes → Executam tarefas delegadas")
print("   ⚡ Execução: Otimizada com delegação inteligente")

# --- PARTE 6: COMPARAÇÃO DOS PROCESSOS ---

def executar_processo_sequencial():
    print("\n" + "="*60)
    print("🚀 EXECUTANDO PROCESSO SEQUENCIAL")
    print("="*60)
    
    inicio = time.time()
    try:
        resultado_seq = crew_sequencial.kickoff()
        tempo_seq = time.time() - inicio
        
        print(f"\n⏱️ Processo Sequencial executado em: {tempo_seq:.2f} segundos")
        print("\n📊 RESULTADO DO PROCESSO SEQUENCIAL:")
        print("-" * 50)
        print(resultado_seq)
        
        return resultado_seq, tempo_seq
    except Exception as e:
        print(f"❌ Erro no processo sequencial: {e}")
        return None, 0

def executar_processo_hierarquico():
    print("\n" + "="*60)
    print("🚀 EXECUTANDO PROCESSO HIERÁRQUICO")  
    print("="*60)
    
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
    print(f"   OpenAI API Key: {'✅ Configurada' if openai_key else '❌ Faltando'}")
    print(f"   Serper API Key: {'✅ Configurada' if serper_key else '❌ Faltando'}")
    
    if not openai_key:
        print("\n❌ ERRO: Chave da OpenAI não encontrada!")
        print("Configure a variável OPENAI_API_KEY no arquivo .env")
        exit(1)
        
    if not serper_key:
        print("\n⚠️ AVISO: Chave do Serper não encontrada!")
        print("Algumas ferramentas de busca podem não funcionar.")
        print("Configure SERPER_API_KEY em https://serper.dev/")
        
    # Menu de escolha
    print("\n📋 ESCOLHA O PROCESSO PARA EXECUTAR:")
    print("1️⃣ - Processo Sequencial (recomendado para iniciantes)")
    print("2️⃣ - Processo Hierárquico (mais avançado)")
    print("3️⃣ - Comparar ambos os processos (demora mais)")
    print("4️⃣ - Apenas demonstrar conceitos (sem executar)")
    
    escolha = input("\nDigite sua escolha (1-4): ").strip()
    
    if escolha == "1":
        resultado_seq, tempo_seq = executar_processo_sequencial()
        
    elif escolha == "2":
        resultado_hier, tempo_hier = executar_processo_hierarquico()
        
    elif escolha == "3":
        print("\n🔄 Executando comparação completa...")
        resultado_seq, tempo_seq = executar_processo_sequencial()
        resultado_hier, tempo_hier = executar_processo_hierarquico()
        
        # Comparação final
        print("\n" + "="*60)
        print("📊 COMPARAÇÃO FINAL DOS PROCESSOS")
        print("="*60)
        
        print(f"⏱️ Tempo de Execução:")
        print(f"   Sequencial: {tempo_seq:.2f}s")
        print(f"   Hierárquico: {tempo_hier:.2f}s")
        print(f"   Diferença: {abs(tempo_seq - tempo_hier):.2f}s")
        
        print(f"\n🎯 Características:")
        print(f"   Sequencial: Previsível, linear, ideal para fluxos claros")
        print(f"   Hierárquico: Flexível, otimizado, ideal para projetos complexos")
        
    elif escolha == "4":
        print("\n📚 CONCEITOS DEMONSTRADOS (sem execução):")
        print("=" * 50)
        
        print("\n🔧 FERRAMENTAS (TOOLS):")
        print("• Simulação de Busca Web - Busca inteligente simulada")
        print("• Simulação de Scraping - Extração de conteúdo simulada")
        print("• Simulação de Leitura - Leitura de arquivos simulada")
        print("• Agentes podem usar múltiplas ferramentas")
        print("• Ferramentas expandem capacidades dos agentes")
        
        print("\n🔄 PROCESSOS:")
        print("• SEQUENCIAL:")
        print("  - Execução linear, uma tarefa por vez")
        print("  - Previsível e fácil de debugar") 
        print("  - Ideal para fluxos bem definidos")
        print("  - Menor complexidade de coordenação")
        
        print("• HIERÁRQUICO:")
        print("  - Manager coordena e delega tarefas")
        print("  - Execução otimizada e paralela quando possível")
        print("  - Ideal para projetos complexos")
        print("  - Requer LLM para o manager")
        
        print("\n💡 QUANDO USAR CADA UM:")
        print("• Sequencial: Projetos simples, fluxos lineares, aprendizado")
        print("• Hierárquico: Projetos complexos, otimização, produção")
        
    else:
        print("❌ Escolha inválida! Execute novamente o script.")
        
    # Lições aprendidas
    print("\n" + "="*60)
    print("🎓 LIÇÕES DA AULA 3:")
    print("="*60)
    print("✅ Aprendemos a equipar agentes com ferramentas")
    print("✅ Vimos como ferramentas expandem capacidades")
    print("✅ Comparamos processos Sequencial vs Hierárquico")
    print("✅ Entendemos quando usar cada tipo de processo")
    print("✅ Exploramos coordenação avançada com managers")
    
    print("\n🎯 Próxima aula: Arquitetura de Chatbots Multi-Agente!")
    
    print("\n💡 DICA IMPORTANTE:")
    print("Ferramentas são o que tornam os agentes realmente poderosos!")
    print("Experimente diferentes combinações e veja os resultados.")
    
print("\n🏁 Aula 3 concluída com sucesso!")