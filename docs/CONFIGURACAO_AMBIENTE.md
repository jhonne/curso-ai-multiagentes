# 🚀 Guia de Configuração do Ambiente CrewAI

**Objetivo:** Configurar o ambiente para executar o curso de CrewAI de forma simples e rápida.

## 🎯 O que você precisa

- **Python 3.11** instalado no seu computador
- **Chave da OpenAI** (gratuita para começar)
- **10 minutos** para seguir este guia

## 📋 Passo a Passo Simples

**Escolha seu sistema operacional:**

- [🪟 Windows com WSL](#-windows-com-wsl-recomendado)
- [🐧 Linux](#-linux-nativo)

Depois siga para:

- [⚙️ Configuração Final](#-configuração-final)
- [✅ Teste](#-teste)

---

## 🪟 Windows com WSL (Recomendado)

### Por que usar WSL?

✅ **Vantagens do WSL para desenvolvimento:**

- **Compatibilidade:** Ambiente Linux nativo no Windows
- **Performance:** Melhor performance para ferramentas de desenvolvimento
- **Simplicidade:** Comandos Unix/Linux funcionam naturalmente
- **Integração:** Funciona perfeitamente com VS Code
- **Sem dual boot:** Não precisa reiniciar para usar Linux

### 1. Instalar WSL (Windows Subsystem for Linux)

O WSL oferece um ambiente Linux completo no Windows, facilitando o desenvolvimento.

1. **Abra o PowerShell como Administrador:**
   - Pressione `Win + X`
   - Clique em "Windows PowerShell (Admin)" ou "Terminal (Admin)"

2. **Instale o WSL:**

   ```powershell
   wsl --install
   ```

3. **Reinicie o computador** quando solicitado

4. **Configure o Ubuntu:**
   - Após reiniciar, o Ubuntu será iniciado automaticamente
   - Crie um nome de usuário e senha
   - Aguarde a instalação finalizar

5. **Teste se funcionou:**

   ```bash
   lsb_release -a
   ```

   - Deve mostrar informações do Ubuntu

6. **Instalar Git (se não estiver instalado):**

   ```bash
   sudo apt install -y git
   ```

### 2. Instalar Python 3.11 no WSL

### 2. Instalar Python 3.11 no WSL

Dentro do terminal do WSL (Ubuntu):

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python 3.11 e dependências
sudo apt install -y python3.11 python3.11-venv python3.11-pip python3.11-dev

# Testar se funcionou
python3.11 --version
```

### 3. Instalar UV no WSL

```bash
# Instalar UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Recarregar configurações do shell
source ~/.bashrc

# Testar se funcionou
uv --version
```

### 4. Baixar e configurar o projeto no WSL

```bash
# Navegar para o diretório home do usuário
cd ~

# Baixar o projeto
git clone https://github.com/jhonne/curso-ai-multiagentes.git
cd curso-ai-multiagentes

# Instalar as dependências
uv sync

# Ativar o ambiente virtual (opcional)
source .venv/bin/activate
```

💡 **Dicas importantes para WSL:**

- Seus arquivos do Windows ficam em `/mnt/c/Users/SeuUsuario/`
- É recomendado trabalhar dentro do sistema de arquivos do Linux (`~`)
- Para acessar o projeto do VS Code no Windows: `code .` (dentro da pasta do projeto)

### 5. Instalar VS Code com WSL (Opcional)

Para uma melhor experiência de desenvolvimento:

1. **Instale o VS Code** no Windows: <https://code.visualstudio.com/>
2. **Instale a extensão WSL:**
   - Abra o VS Code
   - Vá em Extensions (Ctrl+Shift+X)
   - Procure por "WSL" e instale a extensão oficial da Microsoft
3. **Abra o projeto no VS Code:**

   ```bash
   # No terminal do WSL, dentro da pasta do projeto
   code .
   ```

---

## 🐧 Linux (Nativo)

### 1. Instalar Python 3.11 (Linux Nativo)

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

### 2. Instalar UV (Linux Nativo)

```bash
# Instalar UV
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Testar
uv --version
```

### 3. Configurar o projeto (Linux Nativo)

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

**⚠️ IMPORTANTE:** Execute estes comandos no ambiente onde você instalou o projeto:

- Se você usou **WSL**: execute no terminal do WSL
- Se você usou **Linux nativo**: execute no terminal do Linux

**Copie o arquivo de exemplo:**

```bash
# Dentro da pasta do projeto
cp .env.example .env
```

**Edite o arquivo .env** e coloque sua chave:

```env
OPENAI_API_KEY=sk-sua_chave_real_aqui
```

💡 **Dica:** Use qualquer editor de texto (nano, vim, VS Code, etc.)

```bash
# Editar com nano
nano .env

# Ou abrir VS Code
code .env
```

---

## ✅ Teste

### ✅ Teste no WSL

Execute os testes dentro do terminal WSL:

```bash
# Testar API da OpenAI
uv run teste-api

# Executar exemplo principal
uv run hello-crewai
```

### 🔄 Trabalhando entre WSL e Windows

**Acessar arquivos do Windows no WSL:**

```bash
# Seus arquivos do Windows estão em:
cd /mnt/c/Users/SeuUsuario/Documents/
```

**Acessar arquivos do WSL no Windows:**

- Abra o Explorador de Arquivos
- Digite na barra de endereços: `\\wsl$\Ubuntu\home\seuusuario\`

**Comandos úteis:**

```bash
# Abrir explorador do Windows na pasta atual
explorer.exe .

# Abrir VS Code na pasta atual
code .
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

### ❌ Problemas específicos do WSL

**❌ "WSL não está instalado"**

```powershell
# Habilitar recursos do Windows necessários
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# Reiniciar e tentar novamente
wsl --install
```

**❌ "WSL 1 em vez de WSL 2"**

```powershell
# Verificar versão
wsl -l -v

# Atualizar para WSL 2
wsl --set-default-version 2
wsl --set-version Ubuntu 2
```

**❌ "Git não configurado no WSL"**

```bash
# Configurar Git no WSL
git config --global user.name "Seu Nome"
git config --global user.email "seu.email@exemplo.com"
```

**❌ "Permissões de arquivo no WSL"**

```bash
# Corrigir permissões se necessário
chmod +x .venv/bin/activate
```

### ❌ "Ambiente virtual não ativado"

**Windows:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux/WSL:**

```bash
source .venv/bin/activate
```

💡 **Lembre-se:** Com UV você pode usar `uv run comando` sem ativar o ambiente!

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
