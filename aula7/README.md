# Aula 7: Interface Web com Streamlit

**Duração:** 2 horas  
**Objetivo:** Criar uma interface web funcional para o chatbot em 30 minutos

## 🎯 O que você vai aprender

- Criar interface web profissional com Streamlit
- Implementar chat com histórico de mensagens
- Fazer deploy local em 1 comando
- Integrar com o chatbot CrewAI das aulas anteriores

## 🚀 Execução Rápida

```bash
# 1. Instalar dependência (se necessário)
uv add streamlit

# 2. Executar interface
uv run streamlit run app.py

# 3. Abrir no navegador
# http://localhost:8501
```

## 📁 Estrutura dos Arquivos

```
aula7/
├── README.md              # Este arquivo
├── app.py                # Interface Streamlit (PRINCIPAL)
├── chatbot_crew.py       # Classe do chatbot simplificada
├── exemplo_basico.py     # Exemplo sem interface
├── exercicios.md         # Exercícios práticos
└── state_management.md   # Guia completo de gerenciamento de estado
```

## 🏃‍♂️ Começar Agora

1. **Execute o exemplo básico:**

   ```bash
   uv run exemplo_basico.py
   ```

2. **Lance a interface web:**

   ```bash
   uv run streamlit run app.py
   ```

3. **Faça os exercícios:**
   - Leia `exercicios.md`
   - Modifique `app.py`
   - Estude `state_management.md`

## 💡 Conceitos Chave

### Interface Mínima Funcional

- **45 linhas de código** para chat completo
- **State management** com `st.session_state` (veja `state_management.md`)
- **Chat history** automático
- **Deploy instantâneo** com Streamlit

### Integração CrewAI

- **Classe simplificada** `ChatbotCrew`
- **Processamento assíncrono** com `st.spinner`
- **Tratamento de erros** básico

## 🎉 Resultado Esperado

Ao final desta aula você terá:

- ✅ Interface web funcionando
- ✅ Chat com histórico
- ✅ Botão de limpar conversa
- ✅ Deploy local funcionando
- ✅ Chatbot integrado

## 🆘 Problemas Comuns

### Erro: "streamlit not found"

```bash
uv add streamlit
```

### Erro: "ChatbotCrew não encontrado"

```bash
# Copie o arquivo da aula anterior ou use o exemplo fornecido
```

### Interface não abre

- Verifique se está executando: `uv run streamlit run app.py`
- Acesse: <http://localhost:8501>

## 📚 Próximos Passos

Após dominar esta aula:

- **Aula 8:** Adicionar memória ao chatbot
- **Aula 9:** Tratamento de erros
- **Aula 10:** Projeto final
