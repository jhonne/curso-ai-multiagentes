# 🚀 Instruções Rápidas - Aula 4

## Para Executar os Exemplos

### 1. Configurar API Key

```powershell
# No PowerShell (Windows)
$env:OPENAI_API_KEY="sua_chave_openai_aqui"
```

### 2. Executar Exemplo Simples

```powershell
python exemplo_simples.py
```

### 3. Executar Exemplo Completo

```powershell
python main.py
```

## 📋 O que Você Vai Ver

### Exemplo Simples (`exemplo_simples.py`)

- Demonstração básica dos 4 agentes
- Uma pergunta pré-definida
- Processo completo em sequência

### Exemplo Completo (`main.py`)

- Sistema completo de atendimento
- Base de dados de produtos
- Opções interativas
- Múltiplos exemplos

## 🔍 Observando o Processo

Quando executar, você verá:

1. **🏢 Recepcionista**: Limpeza da pergunta
2. **🔍 Analista**: Extração da intenção
3. **📊 Pesquisador**: Busca de informações
4. **💬 Comunicador**: Resposta final

Cada agente mostra seu processo de raciocínio!

## 🎯 Conceitos Demonstrados

- ✅ **Especialização**: Cada agente tem uma função específica
- ✅ **Sequência**: Um agente passa resultado para o próximo
- ✅ **Context**: Informações compartilhadas entre agentes
- ✅ **Verbose**: Visualização do processo de raciocínio

## 🛠️ Dicas para Teste

1. **Modifique as perguntas** no `main.py`
2. **Adicione produtos** na base de dados
3. **Altere o backstory** dos agentes
4. **Observe como cada agente contribui** para o resultado final

## ❓ Perguntas para Testar

- "quanto custa o notebook gamer?"
- "tem smartphone em estoque?"
- "preciso de informações sobre fones bluetooth"
- "qual o preço do celular mais barato?"

---

*🎓 Esta aula demonstra como dividir tarefas complexas em etapas especializadas!*
