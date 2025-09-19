"""
Main - Aula 7: Sistema Médico Integrado CrewAI + Dados Estruturados
===================================================================

Sistema completo demonstrando integração entre agentes especializados:
- Agente Médico: Análise de sintomas e protocolos
- Agente Geográfico: Busca por estabelecimentos próximos
- Fluxo de triagem médica automatizada
- Conceitos aplicáveis ao PostgreSQL real

Execute: uv run aula7/main.py
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Importar agentes especializados
from agente_medico import criar_agente_medico
from agente_geografico import criar_agente_geografico
from dados_simulados import dados_medicos

# Carregar variáveis de ambiente
load_dotenv()

# Configurar LLM otimizado para uso médico
llm_medico = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1,  # Baixa para consistência médica
    max_tokens=1500   # Suficiente para análises detalhadas
)


class SistemaMedicoIntegrado:
    """Sistema médico completo com múltiplos agentes especializados"""
    
    def __init__(self):
        """Inicializa sistema com agentes especializados"""
        self.agente_medico = criar_agente_medico(llm_medico)
        self.agente_geografico = criar_agente_geografico(llm_medico)
        
        # Estatísticas do sistema
        self.stats = dados_medicos.get_estatisticas()
        
        print("🏥 SISTEMA MÉDICO INTEGRADO INICIADO")
        print("="*45)
        print(f"📊 Base de dados: {self.stats['total_estabelecimentos']} estabelecimentos")
        print(f"🔍 Sintomas catalogados: {self.stats['total_sintomas']}")
        print(f"📋 Queixas principais: {self.stats['total_queixas']}")
        print("✅ Agentes especializados carregados\n")
    
    def triagem_completa(self, sintomas: str, latitude: float = -5.0892, 
                        longitude: float = -42.8019, nome_paciente: str = "Paciente"):
        """
        Executa triagem médica completa com análise e busca geográfica
        
        Args:
            sintomas: Descrição dos sintomas do paciente
            latitude: Coordenada do paciente (padrão: Teresina centro)  
            longitude: Coordenada do paciente (padrão: Teresina centro)
            nome_paciente: Nome do paciente (opcional)
        """
        
        print(f"🔄 INICIANDO TRIAGEM PARA: {nome_paciente}")
        print("="*50)
        
        # ETAPA 1: Análise Médica dos Sintomas
        tarefa_analise_medica = Task(
            description=f"""
            ANÁLISE MÉDICA - ETAPA 1
            
            Paciente: {nome_paciente}
            Sintomas relatados: "{sintomas}"
            
            EXECUTE ANÁLISE COMPLETA:
            
            1. ANÁLISE DE SINTOMAS:
               - Use analise_sintomas_avancada para processar o texto
               - Identifique padrões críticos de emergência
               - Classifique nível de urgência (1-5)
            
            2. CONSULTA DE PROTOCOLOS:
               - Identifique a queixa principal mais relevante
               - Consulte protocolo médico correspondente
               - Avalie sinais de alerta específicos
            
            3. CLASSIFICAÇÃO FINAL:
               - Determine urgência final baseada na análise
               - Defina tipo de atendimento necessário
               - Estabeleça tempo máximo para atendimento
            
            IMPORTANTE: Seja preciso na classificação, pois isso determinará
            o tipo de estabelecimento que será buscado na próxima etapa.
            """,
            agent=self.agente_medico,
            expected_output="""
            Relatório médico estruturado contendo:
            - Sintomas identificados com criticidade
            - Nível de urgência (1-5) com justificativa
            - Protocolo médico aplicável
            - Tipo de estabelecimento recomendado
            - Tempo máximo para atendimento
            """
        )
        
        # ETAPA 2: Busca Geográfica de Estabelecimentos
        tarefa_busca_geografica = Task(
            description=f"""
            BUSCA GEOGRÁFICA - ETAPA 2
            
            Paciente: {nome_paciente}
            Localização: Latitude {latitude}, Longitude {longitude}
            
            Com base na análise médica da ETAPA 1, execute:
            
            1. INTERPRETAÇÃO DA URGÊNCIA:
               - Analise o nível de urgência determinado pelo agente médico
               - Use recomendacao_urgencia para definir tipo de estabelecimento
            
            2. BUSCA OTIMIZADA:
               - Para urgência 4-5: busque HOSPITAL num raio de 15km
               - Para urgência 3: busque UPA num raio de 10km  
               - Para urgência 1-2: busque UBS num raio de 5km
               - Use busca_geografica com parâmetros apropriados
            
            3. ANÁLISE DE DISTÂNCIAS:
               - Calcule distâncias exatas para os 3 estabelecimentos mais próximos
               - Use calculo_distancia para validar proximidade
               - Considere horários de funcionamento
            
            4. PRIORIZAÇÃO:
               - Ordene por adequação ao caso (tipo + distância)
               - Priorize atendimento 24h para urgências altas
               - Considere capacidade do estabelecimento
            """,
            agent=self.agente_geografico,
            expected_output="""
            Relatório geográfico com:
            - Tipo de estabelecimento recomendado baseado na urgência
            - Lista de 3-5 estabelecimentos mais adequados
            - Distâncias calculadas e tempo estimado de deslocamento
            - Informações de contato e horário de funcionamento
            - Justificativa para recomendação final
            """,
            context=[tarefa_analise_medica]  # Usa resultado da análise médica
        )
        
        # ETAPA 3: Síntese e Recomendação Final
        tarefa_recomendacao_final = Task(
            description=f"""
            RECOMENDAÇÃO FINAL - ETAPA 3
            
            Paciente: {nome_paciente}
            
            Com base nas análises médica e geográfica anteriores:
            
            1. SÍNTESE INTEGRADA:
               - Combine os achados da análise médica com a busca geográfica
               - Valide se as recomendações são consistentes
               - Ajuste se necessário baseado no contexto completo
            
            2. ORIENTAÇÃO CLARA:
               - Forneça orientação específica e acionável
               - Use linguagem clara e empática
               - Inclua próximos passos concretos
            
            3. INFORMAÇÕES PRÁTICAS:
               - Estabelecimento mais recomendado com justificativa
               - Informações de contato e localização
               - O que levar/preparar para a consulta
               - Quando procurar atendimento (urgência do tempo)
            
            4. DISCLAIMERS IMPORTANTES:
               - Não substituição de avaliação médica presencial
               - Quando chamar SAMU (192)
               - Orientações de segurança
            
            TOME: O paciente deve ter uma orientação clara e tranquilizadora,
            mas sem minimizar riscos quando aplicável.
            """,
            agent=self.agente_medico,  # Agente médico faz a síntese final
            expected_output="""
            Recomendação final clara e estruturada:
            - Resumo da condição e urgência
            - Estabelecimento específico recomendado
            - Orientações práticas imediatas
            - Informações de contato e localização
            - Disclaimers médicos apropriados
            """,
            context=[tarefa_analise_medica, tarefa_busca_geografica]
        )
        
        # Criar e executar crew integrada
        crew_sistema_medico = Crew(
            agents=[self.agente_medico, self.agente_geografico],
            tasks=[tarefa_analise_medica, tarefa_busca_geografica, tarefa_recomendacao_final],
            process=Process.sequential,
            verbose=True
        )
        
        # Executar triagem completa
        resultado = crew_sistema_medico.kickoff()
        
        print("\n" + "="*60)
        print("✅ TRIAGEM MÉDICA COMPLETA FINALIZADA")
        print("="*60)
        
        return resultado


def casos_clinicos_demonstrativos():
    """Demonstra sistema com casos clínicos realistas"""
    
    sistema = SistemaMedicoIntegrado()
    
    casos = [
        {
            'nome': 'João Silva',
            'sintomas': 'dor no peito há 30 minutos, irradiando para braço esquerdo, suor frio',
            'lat': -5.0892, 'lng': -42.8019,  # Centro de Teresina
            'contexto': 'Emergência cardiológica - Alta prioridade'
        },
        {
            'nome': 'Maria Santos', 
            'sintomas': 'febre de 38.5°C há 2 dias, dor de cabeça, mal estar',
            'lat': -5.0650, 'lng': -42.7850,  # Zona Norte
            'contexto': 'Quadro infeccioso - Prioridade moderada'
        },
        {
            'nome': 'Pedro Costa',
            'sintomas': 'check-up de rotina, sem sintomas específicos',
            'lat': -5.0800, 'lng': -42.8100,  # Próximo UBS
            'contexto': 'Prevenção - Baixa prioridade'
        }
    ]
    
    print("🎯 DEMONSTRAÇÃO: CASOS CLÍNICOS REALISTAS")
    print("="*50)
    
    for i, caso in enumerate(casos, 1):
        print(f"\n📋 CASO {i}: {caso['nome']}")
        print(f"🩺 Sintomas: {caso['sintomas']}")
        print(f"📍 Localização: ({caso['lat']}, {caso['lng']})")
        print(f"🎯 Contexto: {caso['contexto']}")
        print("-" * 50)
        
        resultado = sistema.triagem_completa(
            sintomas=caso['sintomas'],
            latitude=caso['lat'],
            longitude=caso['lng'], 
            nome_paciente=caso['nome']
        )
        
        print(f"\n📄 RESULTADO FINAL PARA {caso['nome']}:")
        print(resultado.raw)
        print("\n" + "="*70)


def modo_interativo():
    """Permite teste interativo do sistema"""
    
    sistema = SistemaMedicoIntegrado()
    
    print("\n🤖 MODO INTERATIVO - SISTEMA MÉDICO INTEGRADO")
    print("="*55)
    print("Digite sintomas para triagem completa ou 'sair' para terminar")
    print("O sistema fará análise médica + busca geográfica integrada")
    
    while True:
        try:
            print("\n" + "-"*50)
            
            # Coleta dados do paciente
            nome = input("👤 Nome do paciente (opcional): ").strip()
            if nome.lower() in ['sair', 'quit', 'exit']:
                break
            if not nome:
                nome = "Paciente"
            
            sintomas = input("🩺 Descreva os sintomas: ").strip()
            if sintomas.lower() in ['sair', 'quit', 'exit', '']:
                break
            
            # Localização (opcional - usa padrão se não informado)
            print("📍 Localização (pressione Enter para usar Teresina-PI):")
            lat_input = input("  Latitude (-5.0892): ").strip()
            lng_input = input("  Longitude (-42.8019): ").strip()
            
            latitude = float(lat_input) if lat_input else -5.0892
            longitude = float(lng_input) if lng_input else -42.8019
            
            # Executar triagem
            print(f"\n🔄 Processando triagem para {nome}...")
            resultado = sistema.triagem_completa(sintomas, latitude, longitude, nome)
            
            print(f"\n📋 TRIAGEM COMPLETA PARA {nome}:")
            print("="*50)
            print(resultado.raw)
            
        except KeyboardInterrupt:
            print("\n\n👋 Interrompido pelo usuário. Até logo!")
            break
        except ValueError as e:
            print(f"❌ Erro nos dados informados: {e}")
        except Exception as e:
            print(f"❌ Erro no sistema: {e}")


def main():
    """Função principal com menu de opções"""
    
    print("🏥 SISTEMA MÉDICO INTEGRADO - AULA 7")
    print("="*45)
    print("Integração CrewAI + PostgreSQL + Dados Médicos")
    
    print("\n🎯 FUNCIONALIDADES DISPONÍVEIS:")
    print("1. 📋 Demonstração com casos clínicos (recomendado)")
    print("2. 🤖 Modo interativo (você informa sintomas)")
    print("3. 📊 Mostrar estatísticas do sistema")
    print("4. ❌ Sair")
    
    while True:
        try:
            opcao = input("\nEscolha uma opção (1-4): ").strip()
            
            if opcao == '1':
                casos_clinicos_demonstrativos()
                break
            elif opcao == '2':
                modo_interativo()
                break
            elif opcao == '3':
                stats = dados_medicos.get_estatisticas()
                print("\n📊 ESTATÍSTICAS DO SISTEMA:")
                print("="*35)
                print(f"🏥 Total de estabelecimentos: {stats['total_estabelecimentos']}")
                print(f"🔍 Sintomas catalogados: {stats['total_sintomas']}")
                print(f"📋 Queixas principais: {stats['total_queixas']}")
                print("\n🏢 Por tipo de estabelecimento:")
                for tipo, qtd in stats['tipos_estabelecimentos'].items():
                    print(f"   • {tipo}: {qtd} unidades")
                print("\n💡 Dica: Escolha opção 1 para ver o sistema funcionando!")
            elif opcao == '4':
                print("👋 Até logo!")
                break
            else:
                print("❌ Opção inválida. Digite 1, 2, 3 ou 4.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrompido pelo usuário. Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()