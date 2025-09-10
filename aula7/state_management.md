# 🗂️ State Management com Streamlit - Aula 7

## 🎯 O que é State Management?

State Management (Gerenciamento de Estado) é o processo de **preservar informações** entre interações do usuário em uma aplicação web. No Streamlit, isso é feito com `st.session_state`.

## 🔄 Como Funciona no Streamlit

### Problema sem State Management

```python
# ❌ PROBLEMA: A cada interação, as variáveis são perdidas
messages = []  # Sempre volta para lista vazia!

if user_input:
    messages.append(user_input)  # Perdido na próxima interação
```

### ✅ Solução com `st.session_state`

```python
# ✅ SOLUÇÃO: Dados persistem entre interações
if "messages" not in st.session_state:
    st.session_state.messages = []  # Inicializa apenas uma vez

if user_input:
    st.session_state.messages.append(user_input)  # Persiste!
```

## 🛠️ Implementação na Aula 7

### 1. Inicialização do Estado

```python
# Inicializar histórico de mensagens (uma única vez)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Inicializar instância do chatbot (uma única vez) 
if "chatbot" not in st.session_state:
    st.session_state.chatbot = ChatbotCrew()
```

### 2. Uso do Estado para Histórico

```python
# Mostrar todas as mensagens salvas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
```

### 3. Adicionando ao Estado

```python
# Adicionar nova mensagem do usuário
st.session_state.messages.append({
    "role": "user", 
    "content": prompt
})

# Adicionar resposta do chatbot
st.session_state.messages.append({
    "role": "assistant", 
    "content": response
})
```

### 4. Limpando o Estado

```python
# Botão para limpar conversa
if st.button("🗑️ Limpar Conversa"):
    st.session_state.messages = []         # Limpa histórico
    st.session_state.chatbot = ChatbotCrew() # Reseta chatbot
    st.rerun()  # Força atualização da interface
```

## 📊 Estados Gerenciados na Aula 7

| Estado | Tipo | Propósito | Inicialização |
|--------|------|-----------|---------------|
| `messages` | Lista | Histórico do chat | `[]` |
| `chatbot` | Objeto | Instância do ChatbotCrew | `ChatbotCrew()` |

## 💡 Conceitos Importantes

### 🔑 **Verificação de Existência**

```python
# Sempre verificar se o estado já existe
if "meu_estado" not in st.session_state:
    st.session_state.meu_estado = valor_inicial
```

### 🔄 **Persistência**

- Os dados em `st.session_state` **persistem** entre interações
- Cada usuário tem seu próprio `session_state` independente
- Os dados são perdidos quando a aba/sessão é fechada

### ⚡ **Performance**

- Objetos pesados (como o chatbot) são criados **apenas uma vez**
- Histórico cresce incrementalmente, não é recriado a cada interação
- `st.rerun()` força atualização sem perder o estado

## 🎯 Vantagens do State Management

### ✅ **Para o Usuário**

- Chat com histórico completo
- Conversa contínua natural
- Interface responsiva
- Experiência profissional

### ✅ **Para o Desenvolvedor**

- Código limpo e organizado
- Performance otimizada
- Fácil depuração
- Escalabilidade garantida

## 🧪 Exemplo Prático: Contador

```python
import streamlit as st

# Inicializar contador
if "contador" not in st.session_state:
    st.session_state.contador = 0

# Interface
st.title(f"Contador: {st.session_state.contador}")

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("➕ Incrementar"):
        st.session_state.contador += 1
        st.rerun()

with col2:
    if st.button("➖ Decrementar"):
        st.session_state.contador -= 1
        st.rerun()

with col3:
    if st.button("🔄 Resetar"):
        st.session_state.contador = 0
        st.rerun()
```

## 🛡️ Boas Práticas

### ✅ **Faça**

- Sempre verificar existência antes de usar
- Usar nomes descritivos para os estados
- Inicializar com valores apropriados
- Limpar estados quando necessário

### ❌ **Não Faça**

- Assumir que o estado existe
- Usar nomes genéricos como `data` ou `info`
- Armazenar dados sensíveis no estado
- Criar estados desnecessários

## 🔍 Debugging de Estados

```python
# Ver todos os estados ativos
st.sidebar.write("🐛 Debug - Estados ativos:")
for key, value in st.session_state.items():
    st.sidebar.write(f"- {key}: {type(value)}")
```

## 📚 Recursos Avançados

### Estado com Classes

```python
from dataclasses import dataclass

@dataclass
class ChatState:
    messages: list
    user_name: str
    theme: str = "default"

if "chat_state" not in st.session_state:
    st.session_state.chat_state = ChatState(
        messages=[],
        user_name="Usuário"
    )
```

### Estado com Callbacks

```python
def on_message_add():
    """Callback executado ao adicionar mensagem"""
    if len(st.session_state.messages) > 100:
        # Limitar histórico
        st.session_state.messages = st.session_state.messages[-50:]

# Usar callback
st.session_state.messages.append(nova_mensagem)
on_message_add()
```

## 🎉 Resultado na Aula 7

Com o state management implementado, nossa interface tem:

- ✅ **Histórico persistente** de conversas
- ✅ **Chatbot sempre disponível** (não recriado)
- ✅ **Performance otimizada**
- ✅ **Experiência profissional** para o usuário

O state management é a **base fundamental** que torna nossa interface funcional e profissional!
