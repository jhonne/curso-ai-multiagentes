# 🚀 Guia de Configuração do Ambiente CrewAI

**Objetivo:** Configurar o ambiente para executar o curso de CrewAI de forma simples e rápida.

## 🎯 O que você precisa

- **Python 3.11** instalado no seu computador
- **Chave da OpenAI** (gratuita para começar)
- **10 minutos** para seguir este guia

## 📋 Passo a Passo Simples

**Escolha seu sistema operacional:**

- [🪟 Windows](#-windows)
- [🐧 Linux](#-linux)

Depois siga para:

- [⚙️ Configuração Final](#-configuração-final)
- [✅ Teste](#-teste)

---

## 🪟 Windows

### 1. Instalar Python 3.11

1. **Baixe o Python:**
   - Acesse: <https://www.python.org/downloads/>
   - Clique em "Download Python 3.11.x"

2. **Execute o instalador:**
   - ⚠️ **IMPORTANTE:** Marque "Add Python to PATH"
   - Clique em "Install Now"

3. **Teste se funcionou:**
   - Abra o PowerShell
   - Digite: `python --version`
   - Deve aparecer: `Python 3.11.x`

### 2. Instalar UV (gerenciador de pacotes)

Abra o PowerShell e execute:

```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Teste se funcionou:

```powershell
uv --version
```

### 3. Baixar e configurar o projeto

1. **Baixe o projeto:**

   ```powershell
   git clone https://github.com/jhonne/curso-ai-multiagentes.git
   cd curso-ai-multiagentes
   ```

2. **Instale as dependências:**

   ```powershell
   uv sync
   ```

   💡 **O UV faz tudo automaticamente:** cria ambiente virtual + instala pacotes

3. **Ativar o ambiente virtual (opcional):**

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   💡 **Dica:** Com UV você pode usar `uv run` sem ativar o ambiente, mas se preferir trabalhar com o ambiente ativado, use o comando acima.

---

## 🐧 Linux

### 1. Instalar Python 3.11

**Ubuntu/Debian:**

```bash
# Atualizar sistema
sudo apt update

# Instalar Python 3.11
sudo apt install -y python3.11 python3.11-venv python3.11-pip

# Testar
python3.11 --version
```

**Outras distribuições:**

- **CentOS/RHEL:** `sudo yum install -y python3.11`
- **Fedora:** `sudo dnf install -y python3.11`
- **Arch:** `sudo pacman -S python`

### 2. Instalar UV

```bash
# Instalar UV
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Testar
uv --version
```

### 3. Baixar e configurar o projeto

```bash
# Baixar projeto
git clone https://github.com/jhonne/curso-ai-multiagentes.git
cd curso-ai-multiagentes

# Instalar dependências
uv sync

# Ativar ambiente virtual (opcional)
source .venv/bin/activate
```

💡 **Dica:** Com UV você pode usar `uv run` sem ativar o ambiente, mas se preferir trabalhar com o ambiente ativado, use o comando acima.

---

## ⚙️ Configuração Final

### 1. Obter chave da OpenAI

1. **Acesse:** <https://platform.openai.com/api-keys>
2. **Faça login** (ou crie conta grátis)
3. **Clique em:** "Create new secret key"
4. **Copie a chave** (começa com `sk-`)

### 2. Configurar arquivo .env

**Copie o arquivo de exemplo:**

```bash
# Windows
copy .env.example .env

# Linux
cp .env.example .env
```

**Edite o arquivo .env** e coloque sua chave:

```env
OPENAI_API_KEY=sk-sua_chave_real_aqui
```

💡 **Dica:** Use qualquer editor de texto (Notepad, VS Code, etc.)

---

## ✅ Teste

### Teste se tudo está funcionando

```bash
# Testar API da OpenAI
uv run teste-api

# Executar exemplo principal
uv run hello-crewai
```

### Resultado esperado

```text
🚀 Iniciando Hello CrewAI...
✅ Chave da OpenAI configurada!
🤖 Executando o crew...

[... processo do agente ...]

✅ Resultado final:
Olá! 👋 Seja muito bem-vindo ao fantástico mundo do CrewAI!
🎉 Hello CrewAI executado com sucesso!
```

🎉 **Parabéns!** Se você viu essa mensagem, tudo está funcionando!

---

## 🔧 Problemas Comuns

### ❌ "OPENAI_API_KEY não encontrada"

**Soluções:**

1. Verifique se o arquivo `.env` existe
2. Confirme se a chave está correta (inicia com `sk-`)
3. Reinicie o terminal

### ❌ "Python não encontrado"

**Windows:**

```powershell
# Adicionar ao PATH
$env:PATH += ";C:\Python311;C:\Python311\Scripts"
```

**Linux:**

```bash
# Criar link simbólico
sudo ln -sf /usr/bin/python3.11 /usr/local/bin/python
```

### ❌ "UV não instalado"

```bash
# Reinstalar UV
python -m pip install uv
```

### ❌ Erro 401 (Unauthorized)

- Chave da OpenAI inválida
- Verifique em: <https://platform.openai.com/api-keys>

### ❌ Erro 429 (Rate limit)

- Muitas requisições - aguarde alguns minutos
- Para contas gratuitas há limites menores

### ❌ "Ambiente virtual não ativado"

**Windows:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux:**

```bash
source .venv/bin/activate
```

💡 **Lembre-se:** Com UV você pode usar `uv run comando` sem ativar o ambiente!

---

## 🎯 Próximos Passos

✅ **Ambiente configurado!** Agora você pode:

1. **Ler o README.md** para entender o projeto
2. **Explorar os exemplos** em `aula1/` e `aula2/`
3. **Começar o curso** seguindo o `CURSO.md`

---

**📧 Precisa de ajuda?** Abra uma issue no repositório: <https://github.com/jhonne/curso-ai-multiagentes>

**🚀 Boa sorte com seu aprendizado em CrewAI!**
