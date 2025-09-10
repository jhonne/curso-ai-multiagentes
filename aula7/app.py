"""
Aula 7: Interface Web com Streamlit
Interface completa do chatbot CrewAI em menos de 50 linhas
"""

import streamlit as st
import os
from pathlib import Path

# Adicionar o caminho da aula6 para importar o chatbot
import sys

sys.path.append(str(Path(__file__).parent.parent / "aula6"))

try:
    from chatbot_crew import ChatbotCrew
except ImportError:
    # Fallback para classe local se não encontrar a da aula6
    from chatbot_crew import ChatbotSimplificado as ChatbotCrew

# Configuração da página
st.set_page_config(page_title="💬 Chatbot CrewAI", page_icon="🤖", layout="centered")

# Título da aplicação
st.title("💬 Chatbot Multi-Agente CrewAI")
st.caption("Desenvolvido na Aula 7 - Interface Web com Streamlit")

# Inicializar histórico de mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Inicializar instância do chatbot
if "chatbot" not in st.session_state:
    st.session_state.chatbot = ChatbotCrew()

# Sidebar com opções
with st.sidebar:
    st.header("🛠️ Opções")

    # Botão para limpar conversa
    if st.button("🗑️ Limpar Conversa", type="secondary"):
        st.session_state.messages = []
        st.session_state.chatbot = ChatbotCrew()  # Resetar chatbot
        st.rerun()

    st.divider()

    # Informações do chatbot
    st.subheader("📊 Status")
    st.write(f"💬 Mensagens: {len(st.session_state.messages)}")

    # API Key status
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        st.success("✅ API Key configurada")
    else:
        st.error("❌ API Key não encontrada")
        st.info("Configure OPENAI_API_KEY no arquivo .env")

# Mostrar histórico de mensagens
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Input do usuário
if prompt := st.chat_input("Digite sua mensagem..."):
    # Adicionar mensagem do usuário ao histórico
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Mostrar mensagem do usuário
    with st.chat_message("user"):
        st.write(prompt)

    # Processar com o chatbot
    with st.chat_message("assistant"):
        with st.spinner("🤔 Pensando..."):
            try:
                response = st.session_state.chatbot.processar(prompt)
                st.write(response)

                # Adicionar resposta ao histórico
                st.session_state.messages.append(
                    {"role": "assistant", "content": response}
                )

            except Exception as e:
                error_msg = f"❌ Erro: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )

# Footer
st.divider()
st.caption("🚀 Execute com: `uv run streamlit run app.py`")
