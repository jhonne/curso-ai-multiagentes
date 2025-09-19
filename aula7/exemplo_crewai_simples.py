"""
Exemplo CrewAI - Aula 7: Agente com Integração de Dados Médicos
================================================================

Demonstra como integrar agentes CrewAI com dados estruturados:
- Conexão com banco de dados simulado
- Processamento de dados médicos
- Análise de sintomas e geolocalização
- Fluxo de trabalho entre múltiplos agentes

Execute: uv run aula7/exemplo_crewai_simples.py
"""

from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from dados_simulados import dados_medicos

# Carregar variáveis de ambiente
load_dotenv()

# Configurar LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1  # Baixa temperatura para consistência médica
)


def criar_agente_triagem():
    """Cria agente de triagem médica sem ferramentas customizadas"""
    
    # Preparar contexto dos dados médicos para o agente
    stats = dados_medicos.get_estatisticas()
    
    contexto_medico = f"""
    SISTEMA DE SAÚDE DISPONÍVEL:
    • {stats['total_estabelecimentos']} estabelecimentos de saúde catalogados
    • {stats['total_sintomas']} sintomas médicos com classificação de criticidade
    • {stats['total_queixas']} queixas principais identificadas
    • Tipos: Hospital, UPA, UBS
    • Região: Piauí (dados reais)
    
    CAPACIDADES DISPONÍVEIS:
    - Análise de sintomas e classificação de urgência (1-5)
    - Busca por estabelecimentos próximos por coordenadas
    - Cálculo de distâncias geográficas
    - Recomendação de tipos de estabelecimento adequados
    """
    
    return Agent(
        role="Especialista em Triagem Médica Digital",
        goal="Analisar sintomas e recomendar atendimento médico adequado",
        backstory=f"""
        Sou um profissional de saúde especializado em triagem médica com acesso
        a um sistema digital de dados de saúde do Piauí. Minha função é:
        
        🩺 ANÁLISE MÉDICA:
        • Interpretar sintomas relatados em linguagem natural
        • Classificar urgência médica em escala de 1-5
        • Aplicar protocolos de triagem baseados em evidências
        
        📍 ORIENTAÇÃO GEOGRÁFICA:
        • Conhecer a rede de saúde regional do Piauí
        • Recomendar estabelecimentos por proximidade e adequação
        • Considerar horários de funcionamento e tipos de atendimento
        
        ⚕️ RESPONSABILIDADES:
        • Priorizar segurança do paciente sempre
        • Orientar quando procurar atendimento imediato
        • Fornecer informações claras e acionáveis
        • Incluir disclaimers médicos apropriados
        
        {contexto_medico}
        
        IMPORTANTE: Minhas recomendações são para triagem inicial. 
        Casos de emergência devem sempre buscar atendimento presencial imediato.
        """,
        llm=llm,
        verbose=True
    )


def executar_triagem_simples(sintomas: str, latitude: float = -5.0892, 
                           longitude: float = -42.8019):
    """
    Executa triagem médica simples usando agente CrewAI
    
    Args:
        sintomas: Descrição dos sintomas
        latitude: Coordenada do paciente (padrão: Teresina centro)
        longitude: Coordenada do paciente (padrão: Teresina centro)
    """
    
    print(f"🔄 INICIANDO TRIAGEM MÉDICA")
    print("="*40)
    
    # Preparar dados contextuais para o agente
    analise_previa = dados_medicos.classificar_urgencia_sintomas(sintomas)
    estabelecimentos_proximos = dados_medicos.buscar_estabelecimentos_proximos(
        latitude, longitude, raio_km=10
    )
    
    # Formatar dados para o contexto da tarefa
    contexto_estabelecimentos = ""
    if estabelecimentos_proximos:
        contexto_estabelecimentos = "ESTABELECIMENTOS PRÓXIMOS:\n"
        for est in estabelecimentos_proximos[:5]:
            contexto_estabelecimentos += f"• {est['nome']} ({est['tipo']}) - {est['distancia_km']}km - {est['telefone']}\n"
    
    # Criar agente
    agente_triagem = criar_agente_triagem()
    
    # Criar tarefa de triagem
    tarefa_triagem = Task(
        description=f"""
        TRIAGEM MÉDICA COMPLETA
        
        SINTOMAS RELATADOS: "{sintomas}"
        LOCALIZAÇÃO DO PACIENTE: Latitude {latitude}, Longitude {longitude}
        
        DADOS PRÉ-PROCESSADOS DISPONÍVEIS:
        - Nível de urgência detectado automaticamente: {analise_previa['nivel_urgencia']}/5
        - Classificação inicial: {analise_previa['classificacao']}
        - Sintomas identificados: {len(analise_previa['sintomas_encontrados'])} sintoma(s)
        
        {contexto_estabelecimentos}
        
        EXECUTE ANÁLISE COMPLETA:
        
        1. ANÁLISE CLÍNICA:
           • Interprete os sintomas relatados
           • Valide ou ajuste a classificação de urgência automática
           • Identifique sinais de alerta ou padrões críticos
           • Determine tipo de atendimento necessário
        
        2. RECOMENDAÇÃO GEOGRÁFICA:
           • Com base na urgência, selecione estabelecimentos adequados
           • Priorize proximidade para casos urgentes
           • Considere horários de funcionamento
           • Para urgência 4-5: recomendar Hospital ou SAMU
           • Para urgência 2-3: recomendar UPA
           • Para urgência 1: recomendar UBS
        
        3. ORIENTAÇÃO FINAL:
           • Forneça orientação clara e específica
           • Inclua próximos passos práticos
           • Adicione informações de contato
           • Quando necessário, orientar chamada de emergência (SAMU 192)
        
        FORMATO DA RESPOSTA:
        Estruture a resposta como um relatório médico profissional,
        mas em linguagem acessível ao paciente, incluindo:
        - Resumo da análise dos sintomas
        - Classificação de urgência com justificativa
        - Estabelecimento(s) recomendado(s) com detalhes
        - Orientações práticas imediatas
        - Disclaimer médico apropriado
        """,
        agent=agente_triagem,
        expected_output="""
        Relatório de triagem médica estruturado e acessível contendo:
        - Análise dos sintomas com classificação de urgência justificada
        - Recomendação específica de estabelecimento com informações de contato
        - Orientações práticas sobre quando e como procurar atendimento
        - Disclaimers médicos sobre não substituição de avaliação presencial
        """
    )
    
    # Criar e executar crew
    crew_triagem = Crew(
        agents=[agente_triagem],
        tasks=[tarefa_triagem],
        process=Process.sequential,
        verbose=True
    )
    
    resultado = crew_triagem.kickoff()
    
    print("\n" + "="*50)
    print("✅ TRIAGEM MÉDICA CONCLUÍDA")
    print("="*50)
    
    return resultado


def casos_demonstrativos():
    """Demonstra diferentes casos médicos"""
    
    casos = [
        {
            'nome': 'Emergência Cardíaca',
            'sintomas': 'dor no peito muito forte irradiando para braço esquerdo, suor frio, falta de ar',
            'coordenadas': (-5.0892, -42.8019),  # Centro Teresina
            'contexto': 'Suspeita de síndrome coronariana aguda - máxima prioridade'
        },
        {
            'nome': 'Quadro Febril',
            'sintomas': 'febre de 38.8°C há 24h, dor de cabeça, mal estar geral',
            'coordenadas': (-5.0650, -42.7850),  # Zona Norte
            'contexto': 'Possível infecção - prioridade moderada'
        },
        {
            'nome': 'Consulta Preventiva',
            'sintomas': 'sem sintomas específicos, gostaria de fazer check-up de rotina',
            'coordenadas': (-5.0800, -42.8100),  # Vila Operária
            'contexto': 'Medicina preventiva - baixa prioridade'
        }
    ]
    
    print("🎯 CASOS DEMONSTRATIVOS - TRIAGEM MÉDICA COM CREWAI")
    print("="*60)
    
    for i, caso in enumerate(casos, 1):
        print(f"\n📋 CASO {i}: {caso['nome']}")
        print(f"🩺 Sintomas: {caso['sintomas']}")
        print(f"📍 Coordenadas: {caso['coordenadas']}")
        print(f"💡 Contexto: {caso['contexto']}")
        print("-" * 60)
        
        resultado = executar_triagem_simples(
            caso['sintomas'],
            caso['coordenadas'][0],
            caso['coordenadas'][1]
        )
        
        print(f"\n📄 RESULTADO PARA CASO {i}:")
        print("="*40)
        print(resultado.raw)
        print("\n" + "="*70)
    
    return True


def modo_interativo_crewai():
    """Modo interativo usando CrewAI"""
    
    print("\n🤖 MODO INTERATIVO - TRIAGEM COM CREWAI")
    print("="*45)
    print("Digite sintomas para triagem com inteligência artificial")
    print("Digite 'sair' para terminar")
    
    while True:
        try:
            print("\n" + "-"*40)
            
            sintomas = input("🩺 Descreva os sintomas: ").strip()
            if sintomas.lower() in ['sair', 'quit', 'exit', '']:
                break
            
            # Localização opcional
            print("📍 Localização (Enter para Teresina centro):")
            lat_input = input("  Latitude (-5.0892): ").strip()
            lng_input = input("  Longitude (-42.8019): ").strip()
            
            latitude = float(lat_input) if lat_input else -5.0892
            longitude = float(lng_input) if lng_input else -42.8019
            
            # Executar triagem com CrewAI
            resultado = executar_triagem_simples(sintomas, latitude, longitude)
            
            print(f"\n📋 ANÁLISE DO AGENTE DE IA:")
            print("="*35)
            print(resultado.raw)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrompido pelo usuário. Até logo!")
            break
        except ValueError as e:
            print(f"❌ Erro nos dados: {e}")
        except Exception as e:
            print(f"❌ Erro: {e}")


def main():
    """Função principal"""
    
    print("🤖 EXEMPLO CREWAI - TRIAGEM MÉDICA INTELIGENTE")
    print("="*50)
    print("Demonstração de agentes CrewAI com dados médicos reais")
    
    print("\n🎯 OPÇÕES DISPONÍVEIS:")
    print("1. 📋 Casos demonstrativos (recomendado)")
    print("2. 🤖 Modo interativo com IA")
    print("3. 📊 Ver estatísticas do sistema")
    print("4. ❌ Sair")
    
    while True:
        try:
            opcao = input("\nEscolha uma opção (1-4): ").strip()
            
            if opcao == '1':
                casos_demonstrativos()
                break
            elif opcao == '2':
                modo_interativo_crewai()
                break
            elif opcao == '3':
                stats = dados_medicos.get_estatisticas()
                print("\n📊 ESTATÍSTICAS DO SISTEMA:")
                print("="*35)
                print(f"🏥 Estabelecimentos: {stats['total_estabelecimentos']}")
                print(f"🩺 Sintomas: {stats['total_sintomas']}")
                print(f"📋 Queixas: {stats['total_queixas']}")
                print("\n🏢 Por tipo:")
                for tipo, qtd in stats['tipos_estabelecimentos'].items():
                    print(f"   • {tipo}: {qtd}")
            elif opcao == '4':
                print("👋 Até logo!")
                break
            else:
                print("❌ Opção inválida. Digite 1-4.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrompido pelo usuário. Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()