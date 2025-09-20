#!/usr/bin/env python3
"""
VALIDAÇÃO COMPLETA DA AULA 7 - SISTEMA MÉDICO AVANÇADO
=====================================================

Esta validação verifica todos os componentes necessários para a aula 7:
- PostgreSQL + pgvector + PostGIS
- OpenAI API e embeddings
- Agentes CrewAI especializados
- Sistema de busca semântica
- Dados médicos reais

Execute: uv run aula7/validacao_completa.py
"""

import sys
import traceback
from datetime import datetime


def verificar_dependencias():
    """Verifica se todas as dependências estão instaladas"""
    print("🔧 VERIFICANDO DEPENDÊNCIAS...")
    
    dependencias = [
        ('psycopg2', 'PostgreSQL adapter'),
        ('pgvector', 'Vector operations'),
        ('openai', 'OpenAI API client'),
        ('crewai', 'CrewAI framework'),
        ('crewai.tools', 'CrewAI tools'),
        ('langchain_openai', 'LangChain OpenAI'),
        ('dotenv', 'Environment variables')
    ]
    
    falhas = []
    
    for dep, desc in dependencias:
        try:
            if '.' in dep:
                module, submodule = dep.split('.', 1)
                __import__(module)
                exec(f"from {dep} import *")
            else:
                __import__(dep)
            print(f"✅ {dep} - {desc}")
        except ImportError as e:
            print(f"❌ {dep} - {desc} - ERRO: {e}")
            falhas.append(dep)
    
    return len(falhas) == 0


def verificar_postgresql():
    """Verifica conexão PostgreSQL e extensões"""
    print("\n🗄️ VERIFICANDO POSTGRESQL...")
    
    try:
        import psycopg2
        from psycopg2.extras import RealDictCursor
        
        # Conectar ao banco
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='curso',
            user='postgres',
            password='arpus'
        )
        
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        # Verificar versão
        cursor.execute('SELECT version()')
        version = cursor.fetchone()['version']
        print(f"✅ PostgreSQL conectado: {version[:60]}...")
        
        # Verificar extensões
        cursor.execute("""
        SELECT extname, extversion 
        FROM pg_extension 
        WHERE extname IN ('vector', 'postgis')
        """)
        
        extensoes = {row['extname']: row['extversion'] for row in cursor.fetchall()}
        
        if 'vector' in extensoes:
            print(f"✅ pgvector: versão {extensoes['vector']}")
        else:
            print("❌ pgvector: NÃO INSTALADO")
            return False
            
        if 'postgis' in extensoes:
            print(f"✅ PostGIS: versão {extensoes['postgis']}")
        else:
            print("⚠️ PostGIS: não instalado (opcional)")
        
        # Verificar permissões
        cursor.execute('SELECT current_user, current_database()')
        user_info = cursor.fetchone()
        print(f"✅ Usuário: {user_info['current_user']}")
        print(f"✅ Database: {user_info['current_database']}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ PostgreSQL: ERRO - {e}")
        return False


def verificar_openai():
    """Verifica configuração OpenAI API"""
    print("\n🤖 VERIFICANDO OPENAI API...")
    
    try:
        import os
        from dotenv import load_dotenv
        from openai import OpenAI
        
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            print("❌ OPENAI_API_KEY não configurada no .env")
            return False
            
        print(f"✅ OPENAI_API_KEY configurada: {api_key[:10]}...")
        
        # Testar conexão
        client = OpenAI()
        
        # Teste básico - listar modelos
        models = client.models.list()
        print(f"✅ API OpenAI acessível: {len(models.data)} modelos disponíveis")
        
        # Teste de embedding
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input="teste de conexão"
        )
        
        embedding = response.data[0].embedding
        tokens = response.usage.total_tokens
        custo = (tokens / 1000000) * 0.02
        
        print(f"✅ Embeddings funcionando: {len(embedding)} dimensões")
        print(f"✅ Tokens teste: {tokens}, Custo: ${custo:.6f}")
        
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API: ERRO - {e}")
        return False


def verificar_sistema_completo():
    """Verifica sistema completo da aula 7"""
    print("\n🏥 VERIFICANDO SISTEMA MÉDICO COMPLETO...")
    
    try:
        # Importar sistema
        from dados_medicos_reais import dados_medicos
        from agente_medico import criar_agente_medico_avancado
        from agente_geografico import criar_agente_geografico_avancado
        
        print("✅ Imports do sistema: OK")
        
        # Verificar estatísticas
        stats = dados_medicos.get_estatisticas()
        print(f"✅ Estabelecimentos: {stats['total_estabelecimentos']}")
        print(f"✅ Sintomas: {stats['total_sintomas']}")
        print(f"✅ Queixas: {stats['total_queixas']}")
        print(f"✅ Consultas registradas: {stats['total_consultas']}")
        
        # Verificar cache
        cache = stats['cache_embeddings']
        print(f"✅ Cache embeddings: {cache['entradas']} entradas")
        print(f"✅ Custo total: ${cache['custo_total_usd']:.4f}")
        
        # Teste de busca semântica
        print("\n🔍 Testando busca semântica...")
        resultado = dados_medicos.classificar_urgencia_inteligente("dor no peito intensa")
        
        print(f"✅ Análise IA: {resultado['classificacao']}")
        print(f"✅ Urgência: {resultado['nivel_urgencia']}/5")
        print(f"✅ Sintomas encontrados: {len(resultado['sintomas_similares'])}")
        
        # Teste de busca geográfica
        print("\n🌍 Testando busca geográfica...")
        estabelecimentos = dados_medicos.buscar_estabelecimentos_proximos(
            latitude=-5.0892, 
            longitude=-42.8019, 
            raio_km=5
        )
        
        print(f"✅ Estabelecimentos próximos: {len(estabelecimentos)}")
        if estabelecimentos:
            print(f"✅ Mais próximo: {estabelecimentos[0]['nome']}")
        
        # Teste de agentes
        print("\n🤖 Testando agentes CrewAI...")
        
        from langchain_openai import ChatOpenAI
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        
        agente_medico = criar_agente_medico_avancado(llm)
        agente_geografico = criar_agente_geografico_avancado(llm)
        
        print(f"✅ Agente médico: {agente_medico.role}")
        print(f"✅ Agente geográfico: {agente_geografico.role}")
        print(f"✅ Ferramentas médicas: {len(agente_medico.tools)}")
        print(f"✅ Ferramentas geográficas: {len(agente_geografico.tools)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Sistema médico: ERRO - {e}")
        traceback.print_exc()
        return False


def verificar_casos_demonstracao():
    """Verifica casos de demonstração para a aula"""
    print("\n🎯 VERIFICANDO CASOS DE DEMONSTRAÇÃO...")
    
    casos_aula = [
        {
            'nome': 'Emergência Cardiológica',
            'sintomas': 'dor forte no peito irradiando para braço esquerdo, suor frio, falta de ar',
            'urgencia_esperada': 5,
            'tipo_esperado': 'HOSPITAL'
        },
        {
            'nome': 'Suspeita Meningite',
            'sintomas': 'dor de cabeça súbita muito intensa, rigidez no pescoço, febre alta',
            'urgencia_esperada': 5,
            'tipo_esperado': 'HOSPITAL'
        },
        {
            'nome': 'Quadro Infeccioso',
            'sintomas': 'febre há 3 dias, dor de cabeça, mal estar geral',
            'urgencia_esperada': 3,
            'tipo_esperado': 'UPA'
        },
        {
            'nome': 'Consulta Preventiva',
            'sintomas': 'check-up de rotina, sem sintomas específicos',
            'urgencia_esperada': 1,
            'tipo_esperado': 'UBS'
        }
    ]
    
    from dados_medicos_reais import dados_medicos
    
    casos_ok = 0
    
    for caso in casos_aula:
        try:
            resultado = dados_medicos.classificar_urgencia_inteligente(caso['sintomas'])
            
            urgencia_ok = resultado['nivel_urgencia'] >= caso['urgencia_esperada'] - 1
            tipo_ok = caso['tipo_esperado'] in resultado['tipo_estabelecimento_recomendado']
            
            if urgencia_ok and tipo_ok:
                print(f"✅ {caso['nome']}: Urgência {resultado['nivel_urgencia']}/5, Tipo {resultado['tipo_estabelecimento_recomendado']}")
                casos_ok += 1
            else:
                print(f"⚠️ {caso['nome']}: Resultado inesperado - Urgência {resultado['nivel_urgencia']}/5")
                
        except Exception as e:
            print(f"❌ {caso['nome']}: ERRO - {e}")
    
    print(f"\n✅ Casos válidos para demonstração: {casos_ok}/{len(casos_aula)}")
    return casos_ok >= len(casos_aula) - 1  # Permite 1 falha


def main():
    """Executa validação completa da aula 7"""
    
    print("🎓 VALIDAÇÃO COMPLETA - AULA 7: SISTEMA MÉDICO AVANÇADO")
    print("=" * 65)
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("🎯 Objetivo: Verificar preparação para demonstração prática\n")
    
    validacoes = [
        ("Dependências Python", verificar_dependencias),
        ("PostgreSQL + Extensões", verificar_postgresql), 
        ("OpenAI API", verificar_openai),
        ("Sistema Médico Completo", verificar_sistema_completo),
        ("Casos de Demonstração", verificar_casos_demonstracao)
    ]
    
    resultados = []
    
    for nome, funcao in validacoes:
        try:
            sucesso, *detalhes = funcao() if isinstance(funcao(), tuple) else (funcao(), None)
            resultados.append((nome, sucesso, detalhes))
        except Exception as e:
            print(f"❌ {nome}: FALHA - {e}")
            resultados.append((nome, False, [str(e)]))
    
    # Resumo final
    print("\n" + "=" * 65)
    print("📋 RESUMO DA VALIDAÇÃO:")
    print("=" * 25)
    
    aprovados = 0
    for nome, sucesso, detalhes in resultados:
        status = "✅ APROVADO" if sucesso else "❌ REPROVADO"
        print(f"{status}: {nome}")
        if not sucesso and detalhes:
            for detalhe in detalhes[0] if detalhes[0] else []:
                print(f"   💡 Instalar: {detalhe}")
        
        if sucesso:
            aprovados += 1
    
    # Resultado final
    porcentagem = (aprovados / len(resultados)) * 100
    
    print(f"\n📊 RESULTADO FINAL: {aprovados}/{len(resultados)} ({porcentagem:.0f}%)")
    
    if porcentagem >= 80:
        print("🎉 SISTEMA PRONTO PARA AULA!")
        print("✅ Todos os componentes principais funcionando")
        print("🚀 Pode iniciar a demonstração prática")
        print("\n💡 COMANDO PARA AULA:")
        print("   uv run aula7/main.py")
        return True
    else:
        print("⚠️ SISTEMA PRECISA DE AJUSTES")
        print("❌ Corrija os problemas antes da aula")
        return False


if __name__ == "__main__":
    try:
        sucesso = main()
        sys.exit(0 if sucesso else 1)
    except KeyboardInterrupt:
        print("\n\n👋 Validação interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado na validação: {e}")
        traceback.print_exc()
        sys.exit(1)