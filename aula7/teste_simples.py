"""
Teste Simples - Aula 7: Verificação dos Dados Médicos
=====================================================

Teste simples para verificar se os dados médicos estão funcionando
antes de integrar com agentes CrewAI.

Execute: uv run aula7/teste_simples.py
"""

from dados_simulados import dados_medicos


def testar_dados_basicos():
    """Testa funcionalidades básicas dos dados médicos"""
    
    print("🏥 TESTE DOS DADOS MÉDICOS SIMULADOS")
    print("="*45)
    
    try:
        # Teste 1: Estatísticas
        print("📊 TESTE 1: Estatísticas do sistema")
        stats = dados_medicos.get_estatisticas()
        print(f"   ✅ {stats['total_estabelecimentos']} estabelecimentos carregados")
        print(f"   ✅ {stats['total_queixas']} queixas principais")
        print(f"   ✅ {stats['total_sintomas']} sintomas catalogados")
        
        # Teste 2: Busca geográfica
        print("\n📍 TESTE 2: Busca geográfica")
        lat_teresina = -5.0892
        lng_teresina = -42.8019
        
        estabelecimentos = dados_medicos.buscar_estabelecimentos_proximos(
            lat_teresina, lng_teresina, raio_km=10
        )
        
        print(f"   ✅ {len(estabelecimentos)} estabelecimentos encontrados num raio de 10km")
        
        if estabelecimentos:
            print("   📋 Primeiros 3 estabelecimentos:")
            for i, est in enumerate(estabelecimentos[:3], 1):
                print(f"      {i}. {est['nome']} - {est['distancia_km']}km")
        
        # Teste 3: Análise de sintomas
        print("\n🩺 TESTE 3: Análise de sintomas")
        
        casos_teste = [
            "dor no peito intensa",
            "febre alta", 
            "dor de cabeça leve"
        ]
        
        for caso in casos_teste:
            resultado = dados_medicos.classificar_urgencia_sintomas(caso)
            print(f"   • '{caso}': Urgência {resultado['nivel_urgencia']}/5")
        
        # Teste 4: Cálculo de distância
        print("\n📏 TESTE 4: Cálculo de distâncias")
        
        # Centro de Teresina para UPA Promorar
        lat1, lng1 = -5.0892, -42.8019  # Centro
        lat2, lng2 = -5.0650, -42.7850  # UPA Promorar
        
        distancia = dados_medicos.calcular_distancia(lat1, lng1, lat2, lng2)
        print(f"   ✅ Distância Centro → UPA Promorar: {distancia:.2f}km")
        
        print("\n✅ TODOS OS TESTES PASSARAM!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO no teste: {e}")
        return False


def demonstrar_cenario_medico():
    """Demonstra um cenário médico completo sem agentes"""
    
    print("\n🎯 CENÁRIO MÉDICO DEMONSTRATIVO")
    print("="*40)
    
    # Cenário: Paciente com dor no peito em Teresina
    print("👤 PACIENTE: Maria Silva")
    print("📍 LOCALIZAÇÃO: Centro de Teresina (-5.0892, -42.8019)")
    print("🩺 SINTOMAS: 'dor no peito intensa, falta de ar, sudorese'")
    
    sintomas = "dor no peito intensa, falta de ar, sudorese"
    lat_paciente = -5.0892
    lng_paciente = -42.8019
    
    # Etapa 1: Análise dos sintomas
    print("\n🔍 ETAPA 1: Análise dos sintomas")
    analise = dados_medicos.classificar_urgencia_sintomas(sintomas)
    
    print(f"   📊 Nível de urgência: {analise['nivel_urgencia']}/5")
    print(f"   📋 Classificação: {analise['classificacao']}")
    print(f"   💡 Recomendação: {analise['recomendacao']}")
    
    if analise['sintomas_encontrados']:
        print("   🔍 Sintomas identificados:")
        for sintoma in analise['sintomas_encontrados']:
            print(f"      • {sintoma['nome']} (criticidade: {sintoma['criticidade']})")
    
    # Etapa 2: Busca por estabelecimentos adequados
    print("\n🏥 ETAPA 2: Busca por estabelecimentos")
    
    # Baseado na urgência, definir parâmetros de busca
    if analise['nivel_urgencia'] >= 4:
        tipo_busca = "HOSPITAL"
        raio_busca = 15
    elif analise['nivel_urgencia'] >= 3:
        tipo_busca = "UPA"
        raio_busca = 10
    else:
        tipo_busca = None
        raio_busca = 5
    
    print(f"   🎯 Tipo prioritário: {tipo_busca or 'Qualquer'}")
    print(f"   📏 Raio de busca: {raio_busca}km")
    
    estabelecimentos = dados_medicos.buscar_estabelecimentos_proximos(
        lat_paciente, lng_paciente, raio_busca, tipo_busca
    )
    
    # Se não encontrou do tipo preferido, buscar qualquer tipo
    if not estabelecimentos and tipo_busca:
        print("   ⚠️ Nenhum estabelecimento do tipo preferido encontrado")
        print("   🔍 Buscando estabelecimentos de qualquer tipo...")
        estabelecimentos = dados_medicos.buscar_estabelecimentos_proximos(
            lat_paciente, lng_paciente, raio_busca, None
        )
    
    # Etapa 3: Recomendação final
    print("\n📋 ETAPA 3: Recomendações")
    
    if estabelecimentos:
        print(f"   ✅ {len(estabelecimentos)} estabelecimento(s) encontrado(s):")
        
        for i, est in enumerate(estabelecimentos[:3], 1):
            emoji = "🏥" if est['tipo'] == "HOSPITAL" else "🚑" if est['tipo'] == "UPA" else "⚕️"
            destaque = " ⭐ RECOMENDADO" if i == 1 else ""
            
            print(f"\n   {i}. {emoji} {est['nome']}{destaque}")
            print(f"      📏 Distância: {est['distancia_km']}km")
            print(f"      📞 Telefone: {est['telefone']}")
            print(f"      ⏰ Funcionamento: {est['horario_funcionamento']}")
    
    # Recomendação baseada na urgência
    print(f"\n🚨 RECOMENDAÇÃO FINAL:")
    if analise['nivel_urgencia'] >= 4:
        print("   ⚠️ URGÊNCIA ALTA - Procurar atendimento IMEDIATAMENTE")
        if estabelecimentos:
            print(f"   🏥 Ir para: {estabelecimentos[0]['nome']}")
            print(f"   📞 Ou ligar: {estabelecimentos[0]['telefone']}")
        print("   🚑 Considerar chamar SAMU: 192")
    else:
        print("   📋 Procurar atendimento médico conforme orientação")
    
    print("\n⚠️ IMPORTANTE: Esta análise é apenas educacional.")
    print("   Para situações reais, sempre procure ajuda médica profissional.")


def menu_interativo():
    """Menu para testar diferentes funcionalidades"""
    
    print("\n🎯 MENU INTERATIVO - TESTE DOS DADOS MÉDICOS")
    print("="*50)
    
    opcoes = [
        ("1", "Estatísticas do sistema", testar_dados_basicos),
        ("2", "Cenário médico demonstrativo", demonstrar_cenario_medico),
        ("3", "Teste personalizado", teste_personalizado),
        ("4", "Sair", None)
    ]
    
    for opcao, descricao, _ in opcoes:
        print(f"{opcao}. {descricao}")
    
    while True:
        try:
            escolha = input("\nEscolha uma opção (1-4): ").strip()
            
            if escolha == "1":
                testar_dados_basicos()
            elif escolha == "2":
                demonstrar_cenario_medico()
            elif escolha == "3":
                teste_personalizado()
            elif escolha == "4":
                print("👋 Até logo!")
                break
            else:
                print("❌ Opção inválida. Digite 1-4.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrompido pelo usuário. Até logo!")
            break
        except Exception as e:
            print(f"❌ Erro: {e}")


def teste_personalizado():
    """Permite ao usuário testar com sintomas personalizados"""
    
    print("\n🧪 TESTE PERSONALIZADO")
    print("="*25)
    
    try:
        # Sintomas
        sintomas = input("🩺 Digite os sintomas: ").strip()
        if not sintomas:
            print("❌ Nenhum sintoma informado.")
            return
        
        # Localização (opcional)
        print("\n📍 Localização (pressione Enter para usar Teresina centro):")
        lat_str = input("   Latitude (-5.0892): ").strip()
        lng_str = input("   Longitude (-42.8019): ").strip()
        
        latitude = float(lat_str) if lat_str else -5.0892
        longitude = float(lng_str) if lng_str else -42.8019
        
        print(f"\n🔍 ANALISANDO: '{sintomas}'")
        print(f"📍 LOCALIZAÇÃO: ({latitude}, {longitude})")
        print("-" * 40)
        
        # Análise
        resultado = dados_medicos.classificar_urgencia_sintomas(sintomas)
        print(f"📊 Urgência: {resultado['nivel_urgencia']}/5 - {resultado['classificacao']}")
        print(f"💡 Recomendação: {resultado['recomendacao']}")
        
        # Busca estabelecimentos
        raio = 10 if resultado['nivel_urgencia'] >= 3 else 5
        estabelecimentos = dados_medicos.buscar_estabelecimentos_proximos(
            latitude, longitude, raio
        )
        
        if estabelecimentos:
            print(f"\n🏥 ESTABELECIMENTOS PRÓXIMOS (raio {raio}km):")
            for i, est in enumerate(estabelecimentos[:3], 1):
                print(f"   {i}. {est['nome']} - {est['distancia_km']}km")
        else:
            print(f"\n❌ Nenhum estabelecimento encontrado num raio de {raio}km")
        
    except ValueError as e:
        print(f"❌ Erro nos dados: {e}")
    except Exception as e:
        print(f"❌ Erro no teste: {e}")


def main():
    """Função principal"""
    
    print("🧪 TESTE SIMPLES - DADOS MÉDICOS AULA 7")
    print("="*45)
    print("Verificação das funcionalidades básicas antes de integrar com CrewAI")
    
    # Executar teste básico automaticamente
    sucesso = testar_dados_basicos()
    
    if sucesso:
        print("\n🎉 Sistema funcionando corretamente!")
        
        # Demonstração automática
        demonstrar_cenario_medico()
        
        # Menu interativo
        menu_interativo()
    else:
        print("\n❌ Falhas detectadas no sistema. Verifique a configuração.")


if __name__ == "__main__":
    main()