"""
Main - Aula 7: Sistema Médico Avançado CrewAI + PostgreSQL + Embeddings
======================================================================

Sistema completo com tecnologias modernas:
- PostgreSQL + pgvector para embeddings
- Busca semântica avançada de sintomas
- Análise geoespacial com PostGIS
- Cache inteligente de embeddings
- Dados médicos reais do Piauí
- Agentes especializados com IA

Este sistema integra o que seria das aulas 7 e 8, oferecendo:
• Análise semântica de sintomas com OpenAI embeddings
• Busca geográfica otimizada com PostgreSQL
• Cache para redução de custos
• Dados reais de estabelecimentos de saúde

Execute: uv run aula7/main.py
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI

# Importar agentes modernizados
from agente_medico import criar_agente_medico_avancado
from agente_geografico import criar_agente_geografico_avancado
from dados_medicos_reais import dados_medicos

# Carregar variáveis de ambiente
load_dotenv()

# Configurar LLM otimizado para uso médico
llm_medico = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1,  # Baixa para consistência médica
    max_tokens=1500   # Suficiente para análises detalhadas
)


class SistemaMedicoAvancado:
    """Sistema médico avançado com PostgreSQL, embeddings e agentes IA"""
    
    def __init__(self):
        """Inicializa sistema com tecnologias avançadas"""
        self.agente_medico = criar_agente_medico_avancado(llm_medico)
        self.agente_geografico = criar_agente_geografico_avancado(llm_medico)
        
        # Estatísticas do sistema
        self.stats = dados_medicos.get_estatisticas()
        
        print("🚀 SISTEMA MÉDICO AVANÇADO INICIADO")
        print("="*45)
        print("🤖 PostgreSQL + pgvector + OpenAI embeddings")
        print(f"📊 Estabelecimentos: {self.stats['total_estabelecimentos']}")
        print(f"🔍 Sintomas: {self.stats['total_sintomas']}")
        print(f"📋 Queixas: {self.stats['total_queixas']}")
        print(f"📝 Consultas registradas: {self.stats['total_consultas']}")
        
        # Stats do cache de embeddings
        cache_stats = self.stats['cache_embeddings']
        print(f"💾 Cache embeddings: {cache_stats['entradas']} entradas")
        if cache_stats['custo_total_usd'] > 0:
            custo = cache_stats['custo_total_usd']
            print(f"💰 Custo total embeddings: ${custo:.4f}")
        
        print("✅ Agentes IA especializados carregados\n")
    
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
    """Demonstra sistema avançado com casos clínicos realistas"""
    
    sistema = SistemaMedicoAvancado()
    
    casos = [
        {
            'nome': 'João Silva',
            'sintomas': 'dor intensa no peito há 30 minutos, suor frio, falta de ar, dor no braço esquerdo',
            'lat': -5.0892, 'lng': -42.8019,  # Centro de Teresina
            'contexto': 'EMERGÊNCIA: Suspeita síndrome coronariana aguda'
        },
        {
            'nome': 'Maria Santos',
            'sintomas': 'febre alta de 39°C há 3 dias, dor de cabeça forte, vômito, rigidez no pescoço',
            'lat': -5.0650, 'lng': -42.7850,  # Zona Norte
            'contexto': 'URGENTE: Suspeita meningite - sinais neurológicos'
        },
        {
            'nome': 'Ana Costa',
            'sintomas': 'dor abdominal intensa no lado direito, náusea, febre baixa',
            'lat': -5.0800, 'lng': -42.8100,  # Zona Sul
            'contexto': 'URGENTE: Suspeita apendicite aguda'
        },
        {
            'nome': 'Carlos Mendes',
            'sintomas': 'tosse seca persistente há 2 semanas, cansaço, perda de peso',
            'lat': -5.0500, 'lng': -42.8200,  # Zona Norte
            'contexto': 'MODERADO: Investigação de doença pulmonar'
        },
        {
            'nome': 'Lucia Oliveira',
            'sintomas': 'consulta de rotina para check-up anual, sem sintomas específicos',
            'lat': -5.0920, 'lng': -42.8050,  # Centro
            'contexto': 'ROTINA: Medicina preventiva'
        }
    ]
    
    print("🎯 DEMONSTRAÇÃO: CASOS CLÍNICOS COM IA AVANÇADA")
    print("=" * 55)
    print("🤖 Análise semântica + Busca geográfica otimizada")
    
    for i, caso in enumerate(casos, 1):
        print(f"\n📋 CASO {i}: {caso['nome']}")
        print(f"🩺 Sintomas: {caso['sintomas']}")
        print(f"📍 Localização: ({caso['lat']}, {caso['lng']})")
        print(f"🎯 Contexto: {caso['contexto']}")
        print("-" * 70)
        
        resultado = sistema.triagem_completa(
            sintomas=caso['sintomas'],
            latitude=caso['lat'],
            longitude=caso['lng'],
            nome_paciente=caso['nome']
        )
        
        print(f"\n📄 ANÁLISE COMPLETA PARA {caso['nome']}:")
        print("=" * 50)
        print(resultado.raw)
        print("\n" + "=" * 70)


def modo_interativo():
    """Permite teste interativo do sistema avançado"""
    
    sistema = SistemaMedicoAvancado()
    
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
    
    print("🚀 SISTEMA MÉDICO AVANÇADO - AULA 7")
    print("=" * 50)
    print("🤖 CrewAI + PostgreSQL + pgvector + OpenAI Embeddings")
    print("🏥 Análise Semântica + Busca Geoespacial Avançada")
    
    print("\n🎯 FUNCIONALIDADES AVANÇADAS:")
    print("1. 📋 Demonstração com casos clínicos IA (recomendado)")
    print("2. 🤖 Modo interativo com análise semântica")
    print("3. 📊 Estatísticas completas do sistema")
    print("4. 🧪 Teste de embeddings e cache")
    print("5. ❌ Sair")
    
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
                print("\n📊 ESTATÍSTICAS COMPLETAS DO SISTEMA:")
                print("=" * 45)
                print(f"🏥 Estabelecimentos: {stats['total_estabelecimentos']}")
                print(f"🔍 Sintomas: {stats['total_sintomas']}")
                print(f"📋 Queixas: {stats['total_queixas']}")
                print(f"📝 Consultas: {stats['total_consultas']}")
                
                print("\n🏢 Por tipo de estabelecimento:")
                for tipo, qtd in stats['tipos_estabelecimentos'].items():
                    print(f"   • {tipo}: {qtd} unidades")
                
                print("\n� Cache de embeddings:")
                cache = stats['cache_embeddings']
                print(f"   • Entradas: {cache['entradas']}")
                print(f"   • Tokens consumidos: {cache['tokens_total']:,}")
                print(f"   • Custo total: ${cache['custo_total_usd']:.4f}")
                print(f"   • Acessos: {cache['acessos_total']}")
                
                print("\n�💡 Sistema totalmente funcional com IA!")
                
            elif opcao == '4':
                print("\n🧪 TESTE DE EMBEDDINGS E CACHE")
                print("=" * 40)
                teste_texto = "dor de cabeça intensa e náusea"
                print(f"📝 Testando: '{teste_texto}'")
                
                resultado = dados_medicos.classificar_urgencia_inteligente(teste_texto)
                print(f"🎯 Urgência detectada: {resultado['classificacao']}")
                print(f"🔍 Sintomas similares: {len(resultado['sintomas_similares'])}")
                print(f"📋 Queixas correlatas: {len(resultado['queixas_similares'])}")
                
                if resultado['sintomas_similares']:
                    print("\nMais similar:")
                    s = resultado['sintomas_similares'][0]
                    print(f"   • {s['nome']} ({s['similaridade']:.1%})")
                
                print("\n✅ Sistema de embeddings funcionando!")
                
            elif opcao == '5':
                print("👋 Até logo! Sistema médico avançado encerrado.")
                break
            else:
                print("❌ Opção inválida. Digite 1, 2, 3, 4 ou 5.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrompido pelo usuário. Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()