"""
Exercício 1 - Consultas Básicas a Dados Médicos Estruturados
===============================================================

OBJETIVO: Aprender integração de dados estruturados com sistemas médicos
NÍVEL: 🟢 Básico
TEMPO ESTIMADO: 20 minutos

COMPETÊNCIAS DESENVOLVIDAS:
- Consultar dados médicos estruturados
- Entender arquitetura de sistemas de saúde
- Implementar filtros e classificações
- Interpretar resultados para tomada de decisão

Execute: uv run aula7/exercicio1_consulta.py
"""

from dados_simulados import dados_medicos
import sqlite3


def exercicio_1_estatisticas_basicas():
    """
    EXERCÍCIO 1A: Estatísticas Básicas
    Objetivo: Entender a estrutura dos dados disponíveis
    """
    print("📊 EXERCÍCIO 1A: ESTATÍSTICAS BÁSICAS")
    print("="*45)
    
    # TODO: Complete o código abaixo
    # Use dados_medicos.get_estatisticas() para obter as estatísticas
    stats = dados_medicos.get_estatisticas()
    
    print("📈 ESTATÍSTICAS DO SISTEMA DE SAÚDE:")
    print(f"🏥 Total de estabelecimentos: {stats['total_estabelecimentos']}")
    print(f"📋 Queixas principais catalogadas: {stats['total_queixas']}")
    print(f"🩺 Sintomas médicos: {stats['total_sintomas']}")
    
    print("\n🏢 DISTRIBUIÇÃO POR TIPO:")
    for tipo, quantidade in stats['tipos_estabelecimentos'].items():
        print(f"   • {tipo}: {quantidade} unidades")
    
    # DESAFIO: Calcule qual tipo de estabelecimento é mais comum
    tipo_mais_comum = max(stats['tipos_estabelecimentos'], 
                         key=stats['tipos_estabelecimentos'].get)
    print(f"\n🎯 Tipo mais comum: {tipo_mais_comum}")
    
    print("\n✅ Exercício 1A concluído!")


def exercicio_1b_busca_geografica():
    """
    EXERCÍCIO 1B: Busca Geográfica Básica
    Objetivo: Encontrar estabelecimentos por localização
    """
    print("\n📍 EXERCÍCIO 1B: BUSCA GEOGRÁFICA")
    print("="*40)
    
    # Coordenadas de Teresina (centro da cidade)
    lat_teresina = -5.0892
    lng_teresina = -42.8019
    
    print(f"🌍 Buscando estabelecimentos próximos a Teresina")
    print(f"📍 Coordenadas: ({lat_teresina}, {lng_teresina})")
    
    # TODO: Complete o código
    # Use dados_medicos.buscar_estabelecimentos_proximos()
    # Parâmetros: latitude, longitude, raio_km=5
    estabelecimentos = dados_medicos.buscar_estabelecimentos_proximos(
        lat_teresina, lng_teresina, raio_km=5
    )
    
    print(f"\n🏥 ESTABELECIMENTOS ENCONTRADOS (raio 5km):")
    for i, est in enumerate(estabelecimentos, 1):
        print(f"{i}. {est['nome']}")
        print(f"   • Tipo: {est['tipo']}")
        print(f"   • Distância: {est['distancia_km']}km")
        print(f"   • Telefone: {est['telefone']}")
    
    # DESAFIO: Encontre apenas UPAs num raio de 10km
    print(f"\n🚑 DESAFIO: Apenas UPAs num raio de 10km:")
    upas = dados_medicos.buscar_estabelecimentos_proximos(
        lat_teresina, lng_teresina, raio_km=10, tipo="UPA"
    )
    
    for upa in upas:
        print(f"• {upa['nome']} - {upa['distancia_km']}km")
    
    print(f"\n✅ Exercício 1B concluído!")


def exercicio_1c_analise_sintomas():
    """
    EXERCÍCIO 1C: Análise de Sintomas
    Objetivo: Classificar urgência baseado em sintomas
    """
    print("\n🩺 EXERCÍCIO 1C: ANÁLISE DE SINTOMAS")
    print("="*40)
    
    # Casos para analisar
    casos = [
        "dor de cabeça leve",
        "dor no peito intensa com falta de ar", 
        "febre alta de 39°C",
        "check-up de rotina"
    ]
    
    print("🔍 ANALISANDO DIFERENTES CASOS:")
    
    for i, caso in enumerate(casos, 1):
        print(f"\n{i}. Caso: '{caso}'")
        
        # TODO: Complete o código
        # Use dados_medicos.classificar_urgencia_sintomas(caso)
        resultado = dados_medicos.classificar_urgencia_sintomas(caso)
        
        print(f"   📊 Urgência: {resultado['nivel_urgencia']}/5")
        print(f"   📋 Status: {resultado['classificacao']}")
        print(f"   💡 Recomendação: {resultado['recomendacao']}")
        
        if resultado['sintomas_encontrados']:
            print(f"   🔍 Sintomas identificados:")
            for sintoma in resultado['sintomas_encontrados']:
                print(f"      • {sintoma['nome']} (criticidade: {sintoma['criticidade']})")
        else:
            print(f"   ⚠️ Nenhum sintoma específico identificado")
    
    print(f"\n✅ Exercício 1C concluído!")


def exercicio_1d_consultas_personalizadas():
    """
    EXERCÍCIO 1D: Consultas Personalizadas
    Objetivo: Fazer consultas SQL diretas no banco
    """
    print("\n🔍 EXERCÍCIO 1D: CONSULTAS PERSONALIZADAS")
    print("="*45)
    
    # Acesso direto ao banco para consultas avançadas
    conn = dados_medicos.conn
    cursor = conn.cursor()
    
    print("📊 CONSULTAS SQL DIRETAS:")
    
    # Consulta 1: Estabelecimentos por município
    print("\n1. 🏙️ Estabelecimentos por município:")
    cursor.execute("""
        SELECT municipio, COUNT(*) as quantidade 
        FROM estabelecimentos 
        GROUP BY municipio 
        ORDER BY quantidade DESC
    """)
    
    for row in cursor.fetchall():
        print(f"   • {row['municipio']}: {row['quantidade']} estabelecimentos")
    
    # Consulta 2: Sintomas mais críticos
    print("\n2. 🚨 Sintomas mais críticos (criticidade >= 4):")
    cursor.execute("""
        SELECT nome, criticidade, descricao 
        FROM sintomas 
        WHERE criticidade >= 4 
        ORDER BY criticidade DESC
    """)
    
    for row in cursor.fetchall():
        print(f"   • {row['nome']} ({row['criticidade']}/5): {row['descricao']}")
    
    # Consulta 3: Queixas com mais sintomas associados
    print("\n3. 📋 Queixas com mais sintomas associados:")
    cursor.execute("""
        SELECT q.nome, COUNT(qs.sintoma_id) as num_sintomas
        FROM queixas_principais q
        LEFT JOIN queixa_sintoma qs ON q.id = qs.queixa_id
        GROUP BY q.id, q.nome
        ORDER BY num_sintomas DESC
    """)
    
    for row in cursor.fetchall():
        print(f"   • {row['nome']}: {row['num_sintomas']} sintomas associados")
    
    print(f"\n✅ Exercício 1D concluído!")


def desafio_extra():
    """
    DESAFIO EXTRA: Integração de Funcionalidades
    Objetivo: Combinar múltiplas consultas para resolver um caso
    """
    print("\n🎯 DESAFIO EXTRA: CASO CLÍNICO INTEGRADO")
    print("="*47)
    
    # Cenário: Paciente com sintomas em localização específica
    print("🏥 CENÁRIO CLÍNICO:")
    print("Paciente no centro de Teresina relatando:")
    print("'dor no peito forte, suando frio, falta de ar'")
    
    sintomas = "dor no peito forte, suando frio, falta de ar"
    lat_paciente = -5.0892
    lng_paciente = -42.8019
    
    # 1. Analisar sintomas
    print("\n🔍 ETAPA 1: Análise dos sintomas")
    analise = dados_medicos.classificar_urgencia_sintomas(sintomas)
    print(f"   📊 Urgência detectada: {analise['nivel_urgencia']}/5")
    print(f"   📋 Classificação: {analise['classificacao']}")
    
    # 2. Determinar tipo de estabelecimento necessário
    if analise['nivel_urgencia'] >= 4:
        tipo_necessario = "HOSPITAL"
        raio_busca = 15  # Maior raio para emergências
    elif analise['nivel_urgencia'] >= 3:
        tipo_necessario = "UPA"  
        raio_busca = 10
    else:
        tipo_necessario = None  # Qualquer tipo
        raio_busca = 5
    
    print(f"\n🏥 ETAPA 2: Busca por estabelecimentos")
    print(f"   🎯 Tipo necessário: {tipo_necessario or 'Qualquer'}")
    print(f"   📏 Raio de busca: {raio_busca}km")
    
    # 3. Buscar estabelecimentos adequados
    estabelecimentos = dados_medicos.buscar_estabelecimentos_proximos(
        lat_paciente, lng_paciente, raio_busca, tipo_necessario
    )
    
    # 4. Recomendar os 3 mais próximos
    print(f"\n📍 ETAPA 3: Recomendações (3 mais próximos)")
    for i, est in enumerate(estabelecimentos[:3], 1):
        emoji = "🏥" if est['tipo'] == "HOSPITAL" else "🚑" if est['tipo'] == "UPA" else "⚕️"
        print(f"   {i}. {emoji} {est['nome']}")
        print(f"      📏 Distância: {est['distancia_km']}km")
        print(f"      📞 Telefone: {est['telefone']}")
        print(f"      ⏰ Funcionamento: {est['horario_funcionamento']}")
    
    # 5. Recomendação final
    if analise['nivel_urgencia'] >= 4:
        print(f"\n🚨 RECOMENDAÇÃO FINAL:")
        print(f"   ⚠️ URGÊNCIA ALTA - Procurar atendimento IMEDIATAMENTE")
        print(f"   🏥 Recomendado: {estabelecimentos[0]['nome']}")
        print(f"   📞 Ligar: {estabelecimentos[0]['telefone']}")
        print(f"   🚑 Considerar chamar SAMU: 192")
    else:
        print(f"\n✅ RECOMENDAÇÃO FINAL:")
        print(f"   📋 Procurar atendimento conforme orientação médica")
    
    print(f"\n🎓 Desafio extra concluído!")


def main():
    """Menu principal dos exercícios"""
    
    print("📚 EXERCÍCIOS AULA 7 - CONSULTAS BÁSICAS")
    print("="*45)
    print("Pratique consultas ao banco de dados médicos")
    
    print("\n🎯 EXERCÍCIOS DISPONÍVEIS:")
    print("1. 📊 Exercício 1A: Estatísticas básicas")
    print("2. 📍 Exercício 1B: Busca geográfica")  
    print("3. 🩺 Exercício 1C: Análise de sintomas")
    print("4. 🔍 Exercício 1D: Consultas personalizadas")
    print("5. 🎯 Desafio extra: Caso clínico integrado")
    print("6. 🚀 Executar todos os exercícios")
    print("7. ❌ Sair")
    
    while True:
        try:
            opcao = input("\nEscolha um exercício (1-7): ").strip()
            
            if opcao == '1':
                exercicio_1_estatisticas_basicas()
            elif opcao == '2':
                exercicio_1b_busca_geografica()
            elif opcao == '3':
                exercicio_1c_analise_sintomas()
            elif opcao == '4':
                exercicio_1d_consultas_personalizadas()
            elif opcao == '5':
                desafio_extra()
            elif opcao == '6':
                print("\n🚀 EXECUTANDO TODOS OS EXERCÍCIOS:")
                exercicio_1_estatisticas_basicas()
                exercicio_1b_busca_geografica() 
                exercicio_1c_analise_sintomas()
                exercicio_1d_consultas_personalizadas()
                desafio_extra()
                print("\n🎉 TODOS OS EXERCÍCIOS CONCLUÍDOS!")
                break
            elif opcao == '7':
                print("👋 Até logo!")
                break
            else:
                print("❌ Opção inválida. Digite 1-7.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrompido pelo usuário. Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")


if __name__ == "__main__":
    main()