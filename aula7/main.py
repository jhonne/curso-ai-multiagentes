"""
Aula 7: Interface Web com Streamlit - Script Principal
Execute este arquivo para testar toda a funcionalidade
"""

import subprocess
import sys
from pathlib import Path


def verificar_dependencias():
    """Verifica se as dependências estão instaladas"""
    print("🔍 Verificando dependências...")

    try:
        import streamlit

        print("✅ Streamlit encontrado")
    except ImportError:
        print("❌ Streamlit não encontrado")
        print("📦 Instalando Streamlit...")
        subprocess.run([sys.executable, "-m", "uv", "add", "streamlit"])

    try:
        import crewai

        print("✅ CrewAI encontrado")
    except ImportError:
        print("⚠️ CrewAI não encontrado - usando modo simulação")

    try:
        import openai

        print("✅ OpenAI encontrado")
    except ImportError:
        print("❌ OpenAI não encontrado")
        print("📦 Instalando OpenAI...")
        subprocess.run([sys.executable, "-m", "uv", "add", "openai"])


def executar_exemplo_basico():
    """Executa o exemplo básico para teste"""
    print("\n🧪 Executando teste básico...")
    print("=" * 50)

    try:
        from exemplo_basico import main

        main()
        return True
    except Exception as e:
        print(f"❌ Erro no teste básico: {e}")
        return False


def iniciar_streamlit():
    """Inicia a interface Streamlit"""
    print("\n🚀 Iniciando interface Streamlit...")
    print("=" * 50)
    print("📱 A interface será aberta em: http://localhost:8501")
    print("🛑 Para parar, pressione Ctrl+C")
    print("-" * 50)

    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(Path(__file__).parent / "app.py"),
            ]
        )
    except KeyboardInterrupt:
        print("\n👋 Interface encerrada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao iniciar Streamlit: {e}")


def mostrar_menu():
    """Mostra menu de opções"""
    print("\n" + "=" * 60)
    print("🎓 AULA 7: INTERFACE WEB COM STREAMLIT")
    print("=" * 60)
    print("Escolha uma opção:")
    print("1. 🧪 Executar teste básico")
    print("2. 🚀 Iniciar interface web")
    print("3. 🔍 Verificar dependências")
    print("4. 📚 Mostrar exercícios")
    print("0. 🚪 Sair")
    print("-" * 60)


def mostrar_exercicios():
    """Mostra resumo dos exercícios"""
    print("\n📚 EXERCÍCIOS DISPONÍVEIS:")
    print("=" * 40)
    print("1. 🎨 Personalização Básica (15min)")
    print("   - Alterar título e ícone")
    print("   - Adicionar CSS customizado")
    print()
    print("2. ⚙️ Melhorias na Interface (20min)")
    print("   - Controles na sidebar")
    print("   - Export de histórico")
    print()
    print("3. 🚀 Recursos Avançados (25min)")
    print("   - Upload de arquivos")
    print("   - Avatar personalizado")
    print()
    print("4. 🌐 Deploy Online (30min)")
    print("   - GitHub + Streamlit Cloud")
    print()
    print("📖 Detalhes completos em: exercicios.md")


def main():
    """Função principal"""
    while True:
        mostrar_menu()

        try:
            opcao = input("Sua escolha: ").strip()

            if opcao == "0":
                print("👋 Até logo!")
                break
            elif opcao == "1":
                if executar_exemplo_basico():
                    print("\n✅ Teste básico concluído com sucesso!")
                    input("Pressione Enter para continuar...")
                else:
                    print("\n❌ Teste básico falhou. Verifique as dependências.")
                    input("Pressione Enter para continuar...")
            elif opcao == "2":
                iniciar_streamlit()
            elif opcao == "3":
                verificar_dependencias()
                input("Pressione Enter para continuar...")
            elif opcao == "4":
                mostrar_exercicios()
                input("Pressione Enter para continuar...")
            else:
                print("❌ Opção inválida! Tente novamente.")

        except KeyboardInterrupt:
            print("\n👋 Programa encerrado pelo usuário")
            break
        except Exception as e:
            print(f"\n❌ Erro: {e}")
            input("Pressione Enter para continuar...")


if __name__ == "__main__":
    main()
