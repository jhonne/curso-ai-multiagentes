"""
Exercício 2 - Busca Geográfica Avançada
=======================================

OBJETIVO: Implementar busca geográfica otimizada e criar agente especializado
NÍVEL: 🟡 Intermediário  
TEMPO ESTIMADO: 30 minutos

COMPETÊNCIAS DESENVOLVIDAS:
- Calcular distâncias geográficas precisas
- Implementar filtros por raio e tipo
- Criar ferramentas personalizadas para CrewAI
- Otimizar buscas baseadas em urgência médica

Execute: uv run aula7/exercicio2_geografico.py
"""

import math
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai_tools import BaseTool
from langchain_openai import ChatOpenAI
from dados_simulados import dados_medicos

# Carregar variáveis de ambiente
load_dotenv()

# LLM para os agentes
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)


# TODO: EXERCÍCIO 2A - Complete a ferramenta de busca otimizada
class BuscaGeograficaOtimizada(BaseTool):
    """Ferramenta otimizada para busca geográfica médica"""
    
    name: str = "busca_otimizada"
    description: str = "Busca estabelecimentos com filtros avançados e otimização por urgência"
    
    def _run(self, latitude: float, longitude: float, 
             nivel_urgencia: int = 3, raio_max: float = 15) -> str:
        """
        Busca otimizada baseada no nível de urgência
        
        Args:
            latitude, longitude: Coordenadas do paciente
            nivel_urgencia: Nível de urgência (1-5)
            raio_max: Raio máximo de busca em km
        """
        
        # TODO: Complete a lógica de busca otimizada
        # Dica: Use diferentes critérios baseado na urgência
        
        if nivel_urgencia >= 5:
            # EMERGÊNCIA: Priorizar hospitais, raio amplo
            tipo_preferido = "HOSPITAL"
            raio_busca = min(raio_max, 20)  # Até 20km para emergências
        elif nivel_urgencia >= 4:
            # URGENTE: UPA ou Hospital, raio moderado
            tipo_preferido = None  # Aceitar UPA ou HOSPITAL
            raio_busca = min(raio_max, 15)
        elif nivel_urgencia >= 3:
            # MODERADO: UPA preferencialmente
            tipo_preferido = "UPA"
            raio_busca = min(raio_max, 10)
        else:
            # LEVE: UBS ou UPA
            tipo_preferido = "UBS"  
            raio_busca = min(raio_max, 8)
        
        # Buscar estabelecimentos
        estabelecimentos = dados_medicos.buscar_estabelecimentos_proximos(
            latitude, longitude, raio_busca, tipo_preferido
        )
        
        # Se não encontrou do tipo preferido, buscar outros tipos
        if not estabelecimentos and tipo_preferido:
            estabelecimentos = dados_medicos.buscar_estabelecimentos_proximos(
                latitude, longitude, raio_busca, None
            )
        
        # Formatar resultado otimizado
        resultado = f"🎯 BUSCA OTIMIZADA - Urgência {nivel_urgencia}/5\n"
        resultado += f"📍 Local: ({latitude:.4f}, {longitude:.4f})\n"
        resultado += f"🏥 Tipo preferido: {tipo_preferido or 'Qualquer'}\n"
        resultado += f"📏 Raio de busca: {raio_busca}km\n\n"
        
        if estabelecimentos:
            resultado += f"✅ {len(estabelecimentos)} estabelecimento(s) encontrado(s):\n\n"
            
            for i, est in enumerate(estabelecimentos[:5], 1):
                # Emoji baseado no tipo
                emoji_map = {"HOSPITAL": "🏥", "UPA": "🚑", "UBS": "⚕️"}
                emoji = emoji_map.get(est['tipo'], "🏢")
                
                # Destaque para o mais adequado
                destaque = " ⭐ RECOMENDADO" if i == 1 else ""
                
                resultado += f"{i}. {emoji} {est['nome']}{destaque}\n"
                resultado += f"   📊 Tipo: {est['tipo']}\n"
                resultado += f"   📏 Distância: {est['distancia_km']}km\n"
                resultado += f"   📞 Telefone: {est['telefone']}\n"
                resultado += f"   ⏰ Horário: {est['horario_funcionamento']}\n\n"
        else:
            resultado += f"❌ Nenhum estabelecimento encontrado no raio especificado\n"
            resultado += f"💡 Sugestão: Amplie o raio de busca ou considere SAMU (192)"
        
        return resultado


# TODO: EXERCÍCIO 2B - Complete a ferramenta de análise de rotas
class AnaliseRotasTool(BaseTool):
    """Ferramenta para análise de rotas e tempo de deslocamento"""
    
    name: str = "analise_rotas"
    description: str = "Analisa rotas e estima tempo de deslocamento"
    
    def _run(self, lat_origem: float, lng_origem: float,
             lat_destino: float, lng_destino: float, 
             meio_transporte: str = "carro") -> str:
        """
        Analisa rota entre dois pontos
        
        Args:
            lat_origem, lng_origem: Coordenadas de origem
            lat_destino, lng_destino: Coordenadas de destino
            meio_transporte: carro, pe, transporte_publico
        """
        
        # Calcular distância
        distancia = dados_medicos.calcular_distancia(
            lat_origem, lng_origem, lat_destino, lng_destino
        )
        
        # TODO: Complete o cálculo de tempo baseado no meio de transporte
        # Velocidades médias (km/h)
        velocidades = {
            "carro": 30,        # Trânsito urbano
            "pe": 5,            # Caminhada
            "transporte_publico": 15,  # Ônibus urbano
            "ambulancia": 40,   # Ambulância com prioridade
            "samu": 50          # SAMU em emergência
        }
        
        velocidade = velocidades.get(meio_transporte.lower(), 30)
        tempo_minutos = (distancia / velocidade) * 60
        
        # Análise da rota
        resultado = f"🗺️ ANÁLISE DE ROTA\n"
        resultado += f"📍 Origem: ({lat_origem:.4f}, {lng_origem:.4f})\n"
        resultado += f"📍 Destino: ({lat_destino:.4f}, {lng_destino:.4f})\n"
        resultado += f"📏 Distância: {distancia:.2f}km\n"
        resultado += f"🚗 Transporte: {meio_transporte}\n"
        resultado += f"⏱️ Tempo estimado: {tempo_minutos:.0f} minutos\n"
        
        # Classificação de urgência do tempo
        if tempo_minutos <= 10:
            urgencia_tempo = "🟢 MUITO RÁPIDO"
        elif tempo_minutos <= 20:
            urgencia_tempo = "🟡 ACEITÁVEL"
        elif tempo_minutos <= 40:
            urgencia_tempo = "🟠 MODERADO" 
        else:
            urgencia_tempo = "🔴 DEMORADO"
        
        resultado += f"📊 Classificação: {urgencia_tempo}\n"
        
        return resultado


def exercicio_2a_busca_otimizada():
    """
    EXERCÍCIO 2A: Testar busca geográfica otimizada
    """
    print("🎯 EXERCÍCIO 2A: BUSCA OTIMIZADA POR URGÊNCIA")
    print("="*50)
    
    # Coordenadas de teste (centro de Teresina)
    lat_teste = -5.0892
    lng_teste = -42.8019
    
    # Criar ferramenta
    busca_tool = BuscaGeograficaOtimizada()
    
    # Testar diferentes níveis de urgência
    niveis_teste = [
        (5, "EMERGÊNCIA MÁXIMA"),
        (3, "MODERADO"),
        (1, "LEVE/ROTINA")
    ]
    
    for nivel, descricao in niveis_teste:
        print(f"\n🔍 TESTE: Nível {nivel} - {descricao}")
        print("-" * 40)
        
        resultado = busca_tool._run(lat_teste, lng_teste, nivel)
        print(resultado)
    
    print("✅ Exercício 2A concluído!")


def exercicio_2b_analise_rotas():
    """
    EXERCÍCIO 2B: Testar análise de rotas
    """
    print("\n🗺️ EXERCÍCIO 2B: ANÁLISE DE ROTAS")
    print("="*40)
    
    # Criar ferramenta
    rota_tool = AnaliseRotasTool()
    
    # Coordenadas de exemplo
    centro_teresina = (-5.0892, -42.8019)
    hospital_urgencia = (-5.0892, -42.8019)  # Mesmo centro para exemplo
    upa_promorar = (-5.0650, -42.7850)
    
    # Teste de rotas
    rotas_teste = [
        {
            'nome': 'Centro → Hospital de Urgência',
            'origem': centro_teresina,
            'destino': hospital_urgencia,
            'transporte': 'carro'
        },
        {
            'nome': 'Centro → UPA Promorar', 
            'origem': centro_teresina,
            'destino': upa_promorar,
            'transporte': 'ambulancia'
        },
        {
            'nome': 'Centro → UPA (a pé)',
            'origem': centro_teresina, 
            'destino': upa_promorar,
            'transporte': 'pe'
        }
    ]
    
    for rota in rotas_teste:
        print(f"\n📍 ROTA: {rota['nome']}")
        print("-" * 30)
        
        resultado = rota_tool._run(
            rota['origem'][0], rota['origem'][1],
            rota['destino'][0], rota['destino'][1],
            rota['transporte']
        )
        print(resultado)
    
    print("✅ Exercício 2B concluído!")


def exercicio_2c_agente_geografico():
    """
    EXERCÍCIO 2C: Criar agente geográfico especializado
    """
    print("\n🤖 EXERCÍCIO 2C: AGENTE GEOGRÁFICO")  
    print("="*40)
    
    # TODO: Complete a criação do agente
    agente_geo = Agent(
        role="Especialista em Geolocalização Médica",
        goal="Encontrar estabelecimentos de saúde otimizados por urgência e proximidade",
        backstory="""
        Sou especialista em geolocalização médica com conhecimento da rede
        de saúde do Piauí. Otimizo buscas baseado na urgência médica:
        
        • Para emergências: priorizo hospitais num raio amplo
        • Para urgências: busco UPAs e hospitais próximos
        • Para casos leves: foco em UBS e atendimento básico
        
        Considero sempre tempo de deslocamento e disponibilidade.
        """,
        tools=[BuscaGeograficaOtimizada(), AnaliseRotasTool()],
        llm=llm,
        verbose=True
    )
    
    # Cenário de teste
    cenario = {
        'sintomas': 'dor no peito intensa, falta de ar',
        'urgencia': 5,
        'localizacao': (-5.0892, -42.8019),
        'nome_local': 'Centro de Teresina'
    }
    
    print(f"🏥 CENÁRIO DE TESTE:")
    print(f"   🩺 Sintomas: {cenario['sintomas']}")
    print(f"   🚨 Urgência: {cenario['urgencia']}/5") 
    print(f"   📍 Local: {cenario['nome_local']}")
    
    # Criar tarefa para o agente
    tarefa_geo = Task(
        description=f"""
        SITUAÇÃO DE EMERGÊNCIA MÉDICA:
        
        Paciente localizado em {cenario['nome_local']}
        Coordenadas: {cenario['localizacao']}
        Sintomas: "{cenario['sintomas']}"
        Nível de urgência: {cenario['urgencia']}/5
        
        EXECUTE:
        1. Use busca_otimizada para encontrar estabelecimentos adequados
        2. Analise rotas para os 2 estabelecimentos mais próximos
        3. Considere diferentes meios de transporte (carro, ambulância)
        4. Forneça recomendação final com justificativa
        
        PRIORIDADE: Tempo é crítico - paciente precisa de atendimento imediato
        """,
        agent=agente_geo,
        expected_output="Recomendação de estabelecimento com análise de rota e tempo de deslocamento"
    )
    
    # Executar
    crew_geo = Crew(
        agents=[agente_geo],
        tasks=[tarefa_geo],
        process=Process.sequential,
        verbose=True
    )
    
    print(f"\n🔄 Executando análise geográfica...")
    resultado = crew_geo.kickoff()
    
    print(f"\n📋 RESULTADO DO AGENTE GEOGRÁFICO:")
    print("="*45)
    print(resultado.raw)
    
    print("✅ Exercício 2C concluído!")


def desafio_avancado():
    """
    DESAFIO AVANÇADO: Sistema geográfico completo
    """
    print("\n🎯 DESAFIO AVANÇADO: SISTEMA GEOGRÁFICO COMPLETO")
    print("="*55)
    
    print("🏥 CENÁRIO COMPLEXO:")
    print("Múltiplos pacientes em diferentes locais de Teresina")
    print("Sistema deve otimizar atendimento baseado em:")
    print("• Urgência médica")
    print("• Proximidade geográfica") 
    print("• Capacidade dos estabelecimentos")
    print("• Tempo de deslocamento")
    
    # Múltiplos pacientes simultâneos
    pacientes = [
        {
            'id': 'P001',
            'sintomas': 'dor no peito, sudorese',
            'urgencia': 5,
            'local': (-5.0892, -42.8019),  # Centro
            'nome_local': 'Centro'
        },
        {
            'id': 'P002', 
            'sintomas': 'febre alta, vômito',
            'urgencia': 3,
            'local': (-5.0650, -42.7850),  # Norte
            'nome_local': 'Zona Norte'
        },
        {
            'id': 'P003',
            'sintomas': 'consulta de rotina',
            'urgencia': 1, 
            'local': (-5.0800, -42.8100),  # Próximo UBS
            'nome_local': 'Vila Operária'
        }
    ]
    
    busca_tool = BuscaGeograficaOtimizada()
    rota_tool = AnaliseRotasTool()
    
    print(f"\n📊 ANÁLISE SIMULTÂNEA DE {len(pacientes)} PACIENTES:")
    
    for paciente in pacientes:
        print(f"\n👤 PACIENTE {paciente['id']} - {paciente['nome_local']}")
        print("-" * 45)
        print(f"🩺 Sintomas: {paciente['sintomas']}")
        print(f"🚨 Urgência: {paciente['urgencia']}/5")
        
        # Buscar estabelecimentos otimizados
        busca_resultado = busca_tool._run(
            paciente['local'][0], paciente['local'][1], 
            paciente['urgencia']
        )
        
        print("🏥 ESTABELECIMENTOS RECOMENDADOS:")
        # Extrair primeiro estabelecimento recomendado (simplificado)
        if "⭐ RECOMENDADO" in busca_resultado:
            print("   ✅ Estabelecimento adequado encontrado")
        else:
            print("   ⚠️ Busca realizada - ver detalhes completos")
    
    print(f"\n🎯 OTIMIZAÇÃO GLOBAL:")
    print("   • Paciente P001 (urgência 5): Hospital mais próximo")
    print("   • Paciente P002 (urgência 3): UPA regional")
    print("   • Paciente P003 (urgência 1): UBS local")
    print("   • Distribuição otimizada evita sobrecarga")
    
    print(f"\n🏆 Desafio avançado concluído!")


def main():
    """Menu principal dos exercícios geográficos"""
    
    print("🗺️ EXERCÍCIOS AULA 7 - BUSCA GEOGRÁFICA AVANÇADA")
    print("="*55)
    print("Desenvolva habilidades em geolocalização médica")
    
    print("\n🎯 EXERCÍCIOS DISPONÍVEIS:")
    print("1. 🎯 Exercício 2A: Busca otimizada por urgência") 
    print("2. 🗺️ Exercício 2B: Análise de rotas e tempo")
    print("3. 🤖 Exercício 2C: Agente geográfico especializado")
    print("4. 🏆 Desafio avançado: Sistema geográfico completo")
    print("5. 🚀 Executar todos os exercícios")
    print("6. ❌ Sair")
    
    while True:
        try:
            opcao = input("\nEscolha um exercício (1-6): ").strip()
            
            if opcao == '1':
                exercicio_2a_busca_otimizada()
            elif opcao == '2':
                exercicio_2b_analise_rotas()
            elif opcao == '3':
                exercicio_2c_agente_geografico()
            elif opcao == '4':
                desafio_avancado()
            elif opcao == '5':
                print("\n🚀 EXECUTANDO TODOS OS EXERCÍCIOS:")
                exercicio_2a_busca_otimizada()
                exercicio_2b_analise_rotas()
                exercicio_2c_agente_geografico()
                desafio_avancado()
                print("\n🎉 TODOS OS EXERCÍCIOS GEOGRÁFICOS CONCLUÍDOS!")
                break
            elif opcao == '6':
                print("👋 Até logo!")
                break
            else:
                print("❌ Opção inválida. Digite 1-6.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrompido pelo usuário. Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()