"""
Exemplo Básico - Aula 7: Integração PostgreSQL e CrewAI
========================================================

Este exemplo demonstra como conectar agentes CrewAI a dados médicos simulados.
É o primeiro passo para entender como agentes podem consultar bancos de dados.

OBJETIVO:
- Criar agente que consulta dados médicos
- Demonstrar busca por estabelecimentos próximos
- Classificar urgência de sintomas automaticamente

Execute: uv run aula7/exemplo_basico.py
"""

import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from typing import Any
from dados_simulados import dados_medicos

# Carregar variáveis de ambiente
load_dotenv()

# Configurar LLM
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.1  # Baixa temperatura para consistência médica
)


class ConsultaEstabelecimentosTool:
    """Ferramenta para consultar estabelecimentos de saúde próximos"""
    
    def __init__(self):
        self.name = "consulta_estabelecimentos"
        self.description = (
            "Busca estabelecimentos de saúde próximos a uma coordenada. "
            "Use quando precisar encontrar hospitais, UPAs ou UBS próximos. "
            "Parâmetros: latitude, longitude, raio_km (opcional), tipo (opcional)"
        )
    
    def run(self, latitude: float, longitude: float, 
             raio_km: float = 10, tipo: str = None) -> str:
        """Executa busca por estabelecimentos próximos"""
        try:
            resultados = dados_medicos.buscar_estabelecimentos_proximos(
                latitude, longitude, raio_km, tipo
            )
            
            if not resultados:
                return f"Nenhum estabelecimento encontrado num raio de {raio_km}km"
            
            # Formatar resultados
            texto_resultado = f"🏥 ESTABELECIMENTOS PRÓXIMOS (raio: {raio_km}km):\n\n"
            
            for i, est in enumerate(resultados[:5], 1):
                texto_resultado += f"{i}. {est['nome']}\n"
                texto_resultado += f"   • Tipo: {est['tipo']}\n"
                texto_resultado += f"   • Distância: {est['distancia_km']}km\n"
                texto_resultado += f"   • Município: {est['municipio']}\n"
                texto_resultado += f"   • Telefone: {est['telefone']}\n"
                texto_resultado += f"   • Horário: {est['horario_funcionamento']}\n\n"
            
            return texto_resultado
            
        except Exception as e:
            return f"Erro ao consultar estabelecimentos: {str(e)}"


class AnaliseSintomasTool:
    """Ferramenta para análise e classificação de sintomas"""
    
    def __init__(self):
        self.name = "analise_sintomas"
        self.description = (
            "Analisa sintomas descritos em texto livre e classifica o nível de urgência. "
            "Use quando o usuário descrever sintomas para determinar a urgência. "
            "Parâmetro: sintomas_texto (descrição dos sintomas)"
        )
    
    def run(self, sintomas_texto: str) -> str:
        """Executa análise de sintomas"""
        try:
            resultado = dados_medicos.classificar_urgencia_sintomas(sintomas_texto)
            
            texto_resultado = f"🔍 ANÁLISE DE SINTOMAS:\n\n"
            texto_resultado += f"📝 Sintomas analisados: {sintomas_texto}\n\n"
            
            if resultado['sintomas_encontrados']:
                texto_resultado += f"✅ Sintomas identificados:\n"
                for sintoma in resultado['sintomas_encontrados']:
                    texto_resultado += f"   • {sintoma['nome']} (criticidade: {sintoma['criticidade']}/5)\n"
            else:
                texto_resultado += f"⚠️ Nenhum sintoma específico identificado\n"
            
            texto_resultado += f"\n🚨 CLASSIFICAÇÃO DE URGÊNCIA:\n"
            texto_resultado += f"   • Nível: {resultado['nivel_urgencia']}/5\n"
            texto_resultado += f"   • Status: {resultado['classificacao']}\n"
            texto_resultado += f"   • Recomendação: {resultado['recomendacao']}\n\n"
            
            return texto_resultado
            
        except Exception as e:
            return f"Erro ao analisar sintomas: {str(e)}"


# Criar agente especializado em triagem médica
agente_triagem = Agent(
    role="Especialista em Triagem Médica",
    goal="Analisar sintomas e recomendar estabelecimentos adequados",
    backstory="""
    Sou um profissional de saúde especializado em triagem e atendimento inicial.
    Minha função é analisar sintomas relatados pelos pacientes, classificar o nível
    de urgência e recomendar o estabelecimento de saúde mais adequado para cada caso.
    
    Tenho conhecimento da rede de saúde do Piauí e sempre priorizo a segurança
    e bem-estar do paciente, recomendando atendimento imediato quando necessário.
    """,
    tools=[ConsultaEstabelecimentosTool(), AnaliseSintomasTool()],
    llm=llm,
    verbose=True
)


def executar_triagem_completa(sintomas: str, latitude: float = -5.0892, 
                             longitude: float = -42.8019):
    """
    Executa triagem médica completa com análise de sintomas e busca de estabelecimentos
    
    Args:
        sintomas: Descrição dos sintomas do paciente
        latitude: Latitude da localização do paciente (padrão: Teresina centro)
        longitude: Longitude da localização do paciente (padrão: Teresina centro)
    """
    
    # Criar tarefa de triagem
    tarefa_triagem = Task(
        description=f"""
        Analise os seguintes sintomas relatados por um paciente:
        "{sintomas}"
        
        Localização do paciente: Latitude {latitude}, Longitude {longitude}
        
        Execute as seguintes etapas:
        
        1. ANÁLISE DE SINTOMAS:
           - Use a ferramenta analise_sintomas para classificar a urgência
           - Identifique sintomas críticos que requerem atenção imediata
        
        2. BUSCA DE ESTABELECIMENTOS:
           - Use a ferramenta consulta_estabelecimentos para encontrar locais próximos
           - Considere o nível de urgência para determinar o tipo de estabelecimento
           - Para emergências (urgência 4-5): busque HOSPITAL ou UPA
           - Para casos moderados (urgência 2-3): busque UPA ou UBS
           - Para casos leves (urgência 1): busque UBS
        
        3. RECOMENDAÇÃO FINAL:
           - Forneça orientação clara e específica
           - Inclua informações de contato dos estabelecimentos recomendados
           - Sempre inclua disclaimer sobre procurar ajuda profissional
        """,
        agent=agente_triagem,
        expected_output="""
        Relatório de triagem médica estruturado contendo:
        - Análise dos sintomas com classificação de urgência
        - Lista de estabelecimentos recomendados com distâncias
        - Orientações específicas para o paciente
        - Disclaimer médico apropriado
        """
    )
    
    # Criar e executar crew
    crew_triagem = Crew(
        agents=[agente_triagem],
        tasks=[tarefa_triagem],
        process=Process.sequential,
        verbose=True
    )
    
    print("\n" + "="*60)
    print("🏥 INICIANDO TRIAGEM MÉDICA AUTOMÁTICA")
    print("="*60)
    
    resultado = crew_triagem.kickoff()
    
    print("\n" + "="*60)
    print("✅ TRIAGEM CONCLUÍDA")
    print("="*60)
    
    return resultado


def exemplos_predefinidos():
    """Demonstra diferentes cenários médicos"""
    
    cenarios = [
        {
            'nome': 'Emergência Cardíaca',
            'sintomas': 'dor no peito intensa, falta de ar, sudorese fria',
            'lat': -5.0892, 'lng': -42.8019  # Centro de Teresina
        },
        {
            'nome': 'Febre e Mal-estar',
            'sintomas': 'febre alta, dor de cabeça, fraqueza',
            'lat': -5.0650, 'lng': -42.7850  # Próximo à UPA Promorar
        },
        {
            'nome': 'Consulta de Rotina',
            'sintomas': 'check-up de rotina, sem sintomas específicos',
            'lat': -5.0800, 'lng': -42.8100  # Próximo à UBS
        }
    ]
    
    print("\n🎯 EXEMPLOS PREDEFINIDOS DE TRIAGEM MÉDICA")
    print("="*50)
    
    for i, cenario in enumerate(cenarios, 1):
        print(f"\n{i}. {cenario['nome']}")
        print(f"Sintomas: {cenario['sintomas']}")
        print("-" * 40)
        
        resultado = executar_triagem_completa(
            cenario['sintomas'], 
            cenario['lat'], 
            cenario['lng']
        )
        
        print(f"\n📋 RESULTADO DA TRIAGEM {i}:")
        print(resultado.raw)
        print("\n" + "="*50)


def exemplo_interativo():
    """Permite ao usuário testar com sintomas personalizados"""
    
    print("\n🤖 MODO INTERATIVO - TRIAGEM MÉDICA")
    print("="*40)
    print("Digite sintomas para análise ou 'sair' para terminar")
    print("Exemplo: 'dor de cabeça forte e enjoo'")
    
    while True:
        print("\n" + "-"*40)
        sintomas = input("🩺 Descreva os sintomas: ").strip()
        
        if sintomas.lower() in ['sair', 'quit', 'exit', '']:
            print("👋 Encerrando triagem. Até logo!")
            break
        
        # Usar coordenadas padrão (Teresina centro)
        resultado = executar_triagem_completa(sintomas)
        
        print("\n📋 RESULTADO:")
        print(resultado.raw)


def main():
    """Função principal do exemplo"""
    
    print("🏥 EXEMPLO BÁSICO - AULA 7: INTEGRAÇÃO POSTGRESQL E CREWAI")
    print("="*65)
    
    # Mostrar estatísticas dos dados
    stats = dados_medicos.get_estatisticas()
    print(f"\n📊 DADOS MÉDICOS DISPONÍVEIS:")
    print(f"   • {stats['total_estabelecimentos']} estabelecimentos de saúde")
    print(f"   • {stats['total_queixas']} queixas principais catalogadas")
    print(f"   • {stats['total_sintomas']} sintomas médicos")
    print(f"   • Tipos: {', '.join(stats['tipos_estabelecimentos'].keys())}")
    
    print("\n🎯 OPÇÕES DISPONÍVEIS:")
    print("1. Executar exemplos predefinidos")
    print("2. Modo interativo (você descreve sintomas)")
    print("3. Sair")
    
    while True:
        try:
            opcao = input("\nEscolha uma opção (1-3): ").strip()
            
            if opcao == '1':
                exemplos_predefinidos()
                break
            elif opcao == '2':
                exemplo_interativo()
                break
            elif opcao == '3':
                print("👋 Até logo!")
                break
            else:
                print("❌ Opção inválida. Digite 1, 2 ou 3.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrompido pelo usuário. Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()