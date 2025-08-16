# 🚀 Guia Rápido - Teste da API OpenAI

## ⚡ Configuração Automática com UV (Recomendado)

```bash
# Instalar UV primeiro (se não tiver)
# Windows:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Configurar tudo automaticamente
uv run configurar-crewai
```

Este script irá:
- ✅ Verificar se UV está instalado
- ✅ Verificar sua versão do Python
- ✅ Inicializar projeto com pyproject.toml
- ✅ Instalar todas as dependências automaticamente
- ✅ Configurar o arquivo .env interativamente
- ✅ Testar a conexão com a OpenAI

## 🔧 Configuração Manual

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar chave API
```bash
# Copiar arquivo de exemplo
copy .env.example .env

# Editar .env com sua chave real
OPENAI_API_KEY=sk-sua_chave_aqui
OPENAI_MODEL_NAME=gpt-3.5-turbo
```

## 🧪 Scripts de Teste

### Teste Rápido
```bash
python teste_api.py
```
- Verifica se a chave API está funcionando
- Faz um teste básico de chat
- Mostra uso de tokens

### Teste Completo
```bash
python verificar_openai.py
```
- Análise completa da configuração
- Lista modelos disponíveis
- Informações detalhadas da conta

## 📚 Exemplos CrewAI

### Exemplo Simples
```bash
python hello_simples.py
```

### Exemplo Completo
```bash
python hello_crewai.py
```

## ❓ Problemas Comuns

### "OPENAI_API_KEY não encontrada"
- Verifique se o arquivo `.env` existe
- Confirme se a chave está no formato correto: `sk-...`

### "Erro 401: Unauthorized" 
- Chave API inválida ou expirada
- Verifique em: https://platform.openai.com/api-keys

### "Erro 429: Rate limit"
- Muitas requisições - aguarde alguns minutos
- Para contas gratuitas, há limites mais baixos

### "Erro de quota"
- Saldo esgotado na conta OpenAI
- Verifique em: https://platform.openai.com/usage

## 💰 Custos Estimados

| Modelo | Custo por teste | Curso completo |
|--------|----------------|----------------|
| GPT-3.5-turbo | ~$0.001 | ~$5-10 |
| GPT-4 | ~$0.01 | ~$15-30 |

## 🔗 Links Úteis

- [OpenAI API Keys](https://platform.openai.com/api-keys)
- [OpenAI Usage](https://platform.openai.com/usage)
- [CrewAI Docs](https://docs.crewai.com/)
- [Curso Completo](curso.md)