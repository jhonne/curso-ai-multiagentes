# Exercícios Práticos - Aula 7

## 🎯 Objetivo

Personalizar e expandir a interface Streamlit do chatbot.

## 📋 Exercício 1: Personalização Básica (15 min)

### Tarefa

Modifique `app.py` para personalizar a interface:

1. **Altere o título** para incluir seu nome
2. **Mude o ícone** da página (page_icon)
3. **Adicione uma mensagem de boas-vindas** inicial
4. **Customize as cores** usando st.markdown com CSS

### Dicas

```python
# Exemplo de CSS customizado
st.markdown("""
<style>
.main-header {
    color: #FF6B6B;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)
```

### Resultado esperado

- Interface com sua identidade visual
- Mensagem de boas-vindas personalizada

---

## 📋 Exercício 2: Melhorias na Interface (20 min)

### Tarefa

Adicione funcionalidades na sidebar:

1. **Contador de tokens** (simulado)
2. **Seletor de modelo** (GPT-3.5/GPT-4)
3. **Configurações de temperatura**
4. **Export do histórico** em formato texto

### Exemplo de implementação

```python
# Na sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    
    modelo = st.selectbox("🤖 Modelo", ["gpt-4o-mini", "gpt-4o"])
    temperatura = st.slider("🌡️ Temperatura", 0.0, 1.0, 0.1)
    
    if st.button("📥 Exportar Chat"):
        # Implementar export
        pass
```

### Resultado esperado

- Sidebar com controles funcionais
- Opção de exportar conversa

---

## 📋 Exercício 3: Recursos Avançados (25 min)

### Tarefa

Implemente recursos extras:

1. **Upload de arquivo** para contexto
2. **Diferentes tipos de chat** (formal/casual)
3. **Avatar personalizado** para o bot
4. **Indicador de "digitando"** mais realista

### Funcionalidades avançadas

```python
# Upload de arquivo
uploaded_file = st.file_uploader("📎 Anexar arquivo", type=['txt', 'pdf'])

# Avatar personalizado
with st.chat_message("assistant", avatar="🤖"):
    st.write("Resposta com avatar customizado")

# Progress bar animado
progress_bar = st.progress(0)
for i in range(100):
    time.sleep(0.01)
    progress_bar.progress(i + 1)
```

### Resultado esperado

- Interface profissional completa
- Recursos interativos funcionando

---

## 🏆 Desafio Bonus: Deploy Online (30 min)

### Tarefa

Deploy gratuito no Streamlit Community Cloud:

1. **Criar repositório** no GitHub
2. **Upload dos arquivos** da aula7
3. **Configurar secrets** (OPENAI_API_KEY)
4. **Deploy no Streamlit Cloud**

### Passos detalhados

#### 1. Preparar repositório

```bash
git init
git add .
git commit -m "Aula 7: Interface Streamlit"
git push origin main
```

#### 2. Deploy no Streamlit

- Acesse: <https://share.streamlit.io>
- Conecte seu GitHub
- Escolha o repositório
- Configure OPENAI_API_KEY nos secrets
- Deploy!

### Resultado esperado

- Chatbot online e acessível
- URL pública funcionando

---

## 🎯 Critérios de Avaliação

### Exercício 1 - Básico (✅/❌)

- [ ] Título personalizado
- [ ] Ícone alterado
- [ ] Mensagem de boas-vindas
- [ ] CSS aplicado

### Exercício 2 - Intermediário (✅/❌)

- [ ] Controles na sidebar funcionais
- [ ] Export de histórico
- [ ] Interface organizada
- [ ] Funcionalidades integradas

### Exercício 3 - Avançado (✅/❌)

- [ ] Upload de arquivo
- [ ] Múltiplos modos de chat
- [ ] Avatar personalizado
- [ ] Interface polida

### Desafio Bonus - Expert (✅/❌)

- [ ] Repositório no GitHub
- [ ] Deploy online funcionando
- [ ] Secrets configurados
- [ ] URL acessível

---

## 💡 Dicas Importantes

### Performance

- Use `st.cache_data` para operações pesadas
- Evite reprocessar dados desnecessariamente
- Implemente lazy loading quando necessário

### UX/UI

- Mantenha interface limpa e intuitiva
- Use ícones consistentes
- Forneça feedback visual claro
- Trate erros graciosamente

### Debugging

- Use `st.write()` para debug temporário
- Verifique logs no terminal
- Teste em diferentes navegadores
- Valide responsividade

---

## 📚 Recursos Úteis

- [Documentação Streamlit](https://docs.streamlit.io)
- [Streamlit Community Cloud](https://share.streamlit.io)
- [Componentes Streamlit](https://streamlit.io/components)
- [CSS para Streamlit](https://github.com/streamlit/streamlit/wiki/CSS-Tricks)

---

## 🆘 Problemas Comuns

### "ModuleNotFoundError: No module named 'streamlit'"

```bash
uv add streamlit
```

### Interface não atualiza

- Use `st.rerun()` após mudanças de estado
- Verifique `st.session_state`

### CSS não aplicado

- Use `unsafe_allow_html=True`
- Verifique sintaxe do CSS
- Teste em modo incognito

### Deploy falha

- Verifique requirements.txt
- Configure secrets corretamente
- Valide paths dos arquivos
