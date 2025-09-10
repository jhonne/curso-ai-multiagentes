"""
Exemplo Básico - Aula 7
Teste do chatbot sem interface para verificar funcionamento
Execute: uv run exemplo_basico.py
"""

from chatbot_crew import ChatbotCrew


def main():
    """Função principal para testar o chatbot"""
    print("🚀 Aula 7: Teste do Chatbot")
    print("=" * 50)

    # Criar instância do chatbot
    print("📦 Carregando chatbot...")
    try:
        chatbot = ChatbotCrew()
        print("✅ Chatbot carregado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao carregar chatbot: {e}")
        return

    print("\n💬 Testando conversa básica...")
    print("-" * 30)

    # Teste 1
    mensagem1 = "Olá! Como você funciona?"
    print(f"👤 Usuário: {mensagem1}")
    try:
        resposta1 = chatbot.processar(mensagem1)
        print(f"🤖 Bot: {resposta1}")
    except Exception as e:
        print(f"❌ Erro: {e}")

    print("-" * 30)

    # Teste 2
    mensagem2 = "Você pode me ajudar com CrewAI?"
    print(f"👤 Usuário: {mensagem2}")
    try:
        resposta2 = chatbot.processar(mensagem2)
        print(f"🤖 Bot: {resposta2}")
    except Exception as e:
        print(f"❌ Erro: {e}")

    print("\n🎉 Teste concluído!")
    print("📝 Próximo passo: Execute 'uv run streamlit run app.py'")


if __name__ == "__main__":
    main()
