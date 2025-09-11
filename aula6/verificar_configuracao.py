"""
Aula 6 - Configuração e Testes

Este arquivo ajuda a verificar se tudo está configurado corretamente
antes de executar os exemplos da aula 6.
"""

import os
import sys


def verificar_python():
    """Verifica se a versão do Python é adequada"""
    versao = sys.version_info
    if versao.major >= 3 and versao.minor >= 8:
        print(f"✅ Python {versao.major}.{versao.minor}.{versao.micro} - OK")
        return True
    else:
        print(f"❌ Python {versao.major}.{versao.minor} - Necessário Python 3.8+")
        return False


def verificar_bibliotecas():
    """Verifica se as bibliotecas necessárias estão instaladas"""
    bibliotecas_necessarias = ["crewai", "openai"]
    bibliotecas_ok = []
    bibliotecas_erro = []

    for lib in bibliotecas_necessarias:
        try:
            __import__(lib)
            bibliotecas_ok.append(lib)
            print(f"✅ {lib} - Instalado")
        except ImportError:
            bibliotecas_erro.append(lib)
            print(f"❌ {lib} - NÃO instalado")

    return len(bibliotecas_erro) == 0, bibliotecas_erro


def verificar_openai_key():
    """Verifica se a chave da OpenAI está configurada"""
    chave = os.getenv("OPENAI_API_KEY")
    if chave:
        # Ocultar a chave, mostrando apenas alguns caracteres
        chave_mascarada = f"{chave[:8]}...{chave[-4:]}"
        print(f"✅ OPENAI_API_KEY configurada: {chave_mascarada}")
        return True
    else:
        print("❌ OPENAI_API_KEY não encontrada")
        return False


def exibir_instrucoes_instalacao(bibliotecas_erro):
    """Exibe instruções para instalar bibliotecas faltantes"""
    if bibliotecas_erro:
        print("\n📦 INSTALAÇÃO NECESSÁRIA:")
        print("-" * 30)
        for lib in bibliotecas_erro:
            print(f"uv add {lib}")
        print("\nOu instale todas de uma vez:")
        print("uv add " + " ".join(bibliotecas_erro))


def exibir_instrucoes_openai():
    """Exibe instruções para configurar a chave da OpenAI"""
    print("\n🔑 CONFIGURAR OPENAI_API_KEY:")
    print("-" * 35)
    print("1. Crie uma conta em: https://platform.openai.com")
    print("2. Gere uma chave API")
    print("3. Configure a variável de ambiente:")
    print()
    print("No projeto com UV (recomendado):")
    print("echo OPENAI_API_KEY=sua-chave-aqui >> .env")
    print()
    print("Windows (PowerShell):")
    print('$env:OPENAI_API_KEY="sua-chave-aqui"')
    print()
    print("Windows (CMD):")
    print("set OPENAI_API_KEY=sua-chave-aqui")
    print()
    print("Linux/Mac:")
    print('export OPENAI_API_KEY="sua-chave-aqui"')
    print()
    print("Arquivo .env na raiz do projeto:")
    print("OPENAI_API_KEY=sua-chave-aqui")


def teste_importacao_agentes():
    """Testa se consegue importar os módulos da aula"""
    try:
        from agentes import criar_todos_agentes

        print("✅ Módulo 'agentes' - OK")

        from tarefas import criar_tarefas_completas

        print("✅ Módulo 'tarefas' - OK")

        from orquestrador import OrquestradorChatbot

        print("✅ Módulo 'orquestrador' - OK")

        return True
    except ImportError as e:
        print(f"❌ Erro ao importar módulos: {e}")
        return False


def teste_criacao_agentes():
    """Testa se consegue criar os agentes"""
    try:
        from agentes import criar_todos_agentes

        agentes = criar_todos_agentes()
        print(f"✅ Agentes criados: {list(agentes.keys())}")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar agentes: {e}")
        return False


def main():
    """Função principal de verificação"""
    print("🔧 VERIFICAÇÃO DE CONFIGURAÇÃO - AULA 6")
    print("=" * 50)
    print()

    # Lista de verificações
    verificacoes = []

    # 1. Verificar Python
    print("1️⃣ Verificando Python...")
    verificacoes.append(verificar_python())
    print()

    # 2. Verificar bibliotecas
    print("2️⃣ Verificando bibliotecas...")
    libs_ok, libs_erro = verificar_bibliotecas()
    verificacoes.append(libs_ok)
    print()

    # 3. Verificar chave OpenAI
    print("3️⃣ Verificando chave OpenAI...")
    verificacoes.append(verificar_openai_key())
    print()

    # 4. Teste de importação (só se bibliotecas estiverem OK)
    if libs_ok:
        print("4️⃣ Testando importação de módulos...")
        verificacoes.append(teste_importacao_agentes())
        print()

        # 5. Teste de criação de agentes
        print("5️⃣ Testando criação de agentes...")
        verificacoes.append(teste_criacao_agentes())
        print()
    else:
        verificacoes.extend([False, False])

    # Resumo final
    print("=" * 50)
    print("📊 RESUMO DA VERIFICAÇÃO")
    print("=" * 50)

    if all(verificacoes):
        print("🎉 TUDO CONFIGURADO CORRETAMENTE!")
        print("✅ Você pode executar todos os exemplos da Aula 6")
        print()
        print("🚀 Arquivos para testar:")
        print("   • uv run aula6/exemplo_basico.py")
        print("   • uv run aula6/chatbot_simples.py")
        print("   • uv run aula6/main.py")
    else:
        print("⚠️  ALGUMAS CONFIGURAÇÕES PRECISAM SER AJUSTADAS")
        print()

        # Instruções específicas
        if not libs_ok:
            exibir_instrucoes_instalacao(libs_erro)

        if not verificacoes[2]:  # Chave OpenAI
            exibir_instrucoes_openai()

        print("\n🔄 Execute este script novamente após as correções")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
