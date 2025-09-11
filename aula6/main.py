"""
Aula 6 - Sistema Completo de Chatbot Multi-Agente

Este é o arquivo principal que demonstra um sistema completo
de chatbot usando múltiplos agentes especializados.

🎯 Objetivo: Mostrar como orquestrar agentes para criar
um chatbot funcional que pode ser usado em aplicações reais.

Arquitetura:
- 4 agentes especializados trabalhando em sequência
- Sistema de tarefas interconectadas
- Orquestrador coordenando todo o processo
- Interface simples para interação
"""

import os
from orquestrador import OrquestradorChatbot


def configurar_ambiente():
    """
    Configura o ambiente necessário para o funcionamento do sistema
    """
    print("⚙️ Configurando ambiente...")

    # Verificar se a chave da OpenAI está configurada
    if not os.getenv("OPENAI_API_KEY"):
        print("⚠️ ATENÇÃO: Variável OPENAI_API_KEY não encontrada!")
        print("   Configure sua chave antes de executar o sistema.")
        return False

    # Configurar modelo padrão
    os.environ["OPENAI_MODEL_NAME"] = "gpt-3.5-turbo"

    print("✅ Ambiente configurado com sucesso!")
    return True


def exibir_introducao():
    """
    Exibe a introdução explicando o sistema
    """
    print("\n" + "=" * 60)
    print("🤖 CHATBOT MULTI-AGENTE - AULA 6")
    print("=" * 60)
    print()
    print("Este sistema usa 4 agentes especializados:")
    print()
    print("🔍 1. AGENTE DE TRIAGEM")
    print("   └─ Recebe e classifica mensagens")
    print()
    print("🎯 2. AGENTE DE INTENÇÃO")
    print("   └─ Analisa o que o usuário realmente quer")
    print()
    print("📚 3. AGENTE DE BUSCA")
    print("   └─ Processa e organiza informações")
    print()
    print("💬 4. AGENTE DE RESPOSTA")
    print("   └─ Cria a resposta final")
    print()
    print("Fluxo: Mensagem → Triagem → Intenção → Busca → Resposta")
    print("=" * 60)


def menu_principal():
    """
    Exibe o menu principal e retorna a opção escolhida
    """
    print("\n📋 MENU PRINCIPAL")
    print("-" * 20)
    print("1. 🎯 Demonstração com exemplos")
    print("2. 💬 Modo conversa interativa")
    print("3. 🧪 Teste com sua própria pergunta")
    print("4. 📊 Ver informações do sistema")
    print("5. 🚪 Sair")
    print()

    while True:
        opcao = input("Escolha uma opção (1-5): ").strip()
        if opcao in ["1", "2", "3", "4", "5"]:
            return opcao
        print("❌ Opção inválida. Digite um número de 1 a 5.")


def demonstracao_exemplos():
    """
    Executa demonstração com exemplos predefinidos
    """
    print("\n🎯 DEMONSTRAÇÃO COM EXEMPLOS")
    print("=" * 40)
    print("Vamos ver como o sistema processa diferentes tipos de perguntas!")
    print()

    orquestrador = OrquestradorChatbot(verbose=True)

    exemplos = [
        {
            "pergunta": "O que é inteligência artificial?",
            "categoria": "Pergunta conceitual",
        },
        {
            "pergunta": "Como posso aprender Python do zero?",
            "categoria": "Pedido de orientação",
        },
        {
            "pergunta": "Estou com dificuldades para entender machine learning",
            "categoria": "Pedido de ajuda",
        },
    ]

    for i, exemplo in enumerate(exemplos, 1):
        print(f"\n📝 EXEMPLO {i}: {exemplo['categoria']}")
        print("-" * 50)
        print(f"Pergunta: {exemplo['pergunta']}")
        print()

        resposta = orquestrador.processar_mensagem(exemplo["pergunta"])

        print(f"\n✅ RESPOSTA FINAL:")
        print(f"{resposta}")

        if i < len(exemplos):
            input("\n⏳ Pressione Enter para próximo exemplo...")

    print(f"\n📊 Resumo: {len(exemplos)} exemplos processados com sucesso!")


def teste_personalizado():
    """
    Permite ao usuário testar com sua própria pergunta
    """
    print("\n🧪 TESTE PERSONALIZADO")
    print("=" * 30)
    print("Digite sua pergunta e veja como o sistema processa!")
    print()

    pergunta = input("💭 Sua pergunta: ").strip()

    if not pergunta:
        print("❌ Pergunta vazia. Voltando ao menu...")
        return

    print(f"\n🚀 Processando: '{pergunta}'")
    print("=" * 50)

    orquestrador = OrquestradorChatbot(verbose=True)
    resposta = orquestrador.processar_mensagem(pergunta)

    print(f"\n✅ RESPOSTA FINAL:")
    print("=" * 20)
    print(f"{resposta}")

    print("\n🎯 Processo concluído!")


def informacoes_sistema():
    """
    Exibe informações técnicas sobre o sistema
    """
    print("\n📊 INFORMAÇÕES DO SISTEMA")
    print("=" * 35)
    print()
    print("🏗️ ARQUITETURA:")
    print("   └─ 4 agentes especializados")
    print("   └─ Processamento sequencial")
    print("   └─ Tarefas interconectadas")
    print()
    print("🤖 AGENTES:")
    print("   └─ Triagem: Classifica mensagens")
    print("   └─ Intenção: Analisa objetivos")
    print("   └─ Busca: Processa informações")
    print("   └─ Resposta: Formula respostas")
    print()
    print("⚙️ TECNOLOGIAS:")
    print("   └─ CrewAI Framework")
    print("   └─ OpenAI GPT-3.5-turbo")
    print("   └─ Python 3.8+")
    print()
    print("📈 CARACTERÍSTICAS:")
    print("   └─ Processamento contextual")
    print("   └─ Análise multi-perspectiva")
    print("   └─ Respostas estruturadas")
    print("   └─ Sistema extensível")


def modo_conversa():
    """
    Executa o modo de conversa interativa
    """
    print("\n💬 MODO CONVERSA INTERATIVA")
    print("=" * 40)
    print("Converse naturalmente com o sistema!")
    print()
    print("💡 Dicas:")
    print("   • Faça perguntas sobre qualquer tópico")
    print("   • Digite 'sair' para voltar ao menu")
    print("   • O sistema analisa cada mensagem profundamente")
    print()

    orquestrador = OrquestradorChatbot(verbose=False)
    contador = 0

    while True:
        mensagem = input(f"\n💭 Mensagem {contador + 1}: ").strip()

        if mensagem.lower() in ["sair", "exit", "voltar"]:
            print("🔙 Voltando ao menu principal...")
            break

        if not mensagem:
            print("⚠️ Digite uma mensagem válida")
            continue

        print("\n🤖 Analisando...")
        resposta = orquestrador.processar_mensagem(mensagem)

        print(f"\n🤖 Resposta: {resposta}")
        contador += 1

    print(f"\n📊 Total de mensagens processadas: {contador}")


def main():
    """
    Função principal que coordena todo o sistema
    """
    # Configurar ambiente
    if not configurar_ambiente():
        return

    # Exibir introdução
    exibir_introducao()

    # Loop principal do menu
    while True:
        opcao = menu_principal()

        try:
            if opcao == "1":
                demonstracao_exemplos()
            elif opcao == "2":
                modo_conversa()
            elif opcao == "3":
                teste_personalizado()
            elif opcao == "4":
                informacoes_sistema()
            elif opcao == "5":
                print("\n👋 Obrigado por testar o sistema!")
                print("🎓 Até a próxima aula!")
                break

        except KeyboardInterrupt:
            print("\n\n⚠️ Operação interrompida pelo usuário")
            print("🔙 Voltando ao menu...")
            continue
        except Exception as e:
            print(f"\n❌ Erro inesperado: {str(e)}")
            print("🔙 Voltando ao menu...")
            continue

        # Pausa antes de mostrar o menu novamente
        input("\nPressione Enter para voltar ao menu...")


if __name__ == "__main__":
    main()
