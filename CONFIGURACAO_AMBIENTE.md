# 🚀 Guia Completo de Configuração do Ambiente

Este guia contém instruções detalhadas para configurar o ambiente de desenvolvimento do projeto **Curso CrewAI** em Windows e Linux, incluindo instalação do Python 3.11, UV, ambientes virtuais e todas as dependências necessárias.

## 📋 Índice

- [Requisitos Mínimos](#requisitos-mínimos)
- [Windows](#windows)
  - [Instalação do Python 3.11](#windows-python)
  - [Instalação do UV](#windows-uv)
  - [Configuração do Projeto](#windows-projeto)
- [Linux (Ubuntu/Debian)](#linux)
  - [Instalação do Python 3.11](#linux-python)
  - [Instalação do UV](#linux-uv)
  - [Configuração do Projeto](#linux-projeto)
- [Configuração Comum](#configuracao-comum)
- [Verificação da Instalação](#verificacao)
- [Solução de Problemas](#problemas)

---

## 📊 Requisitos Mínimos

- **Sistema Operacional**: Windows 10+ ou Linux (Ubuntu 20.04+, Debian 11+)
- **Python**: 3.10+ (recomendado: 3.11)
- **RAM**: 4GB mínimo (8GB recomendado)
- **Espaço em disco**: 2GB livres
- **Internet**: Conexão estável para download de dependências
- **Chave da OpenAI**: Necessária para executar os exemplos

---

## 🪟 Windows

### <a id="windows-python"></a>🐍 1. Instalação do Python 3.11

#### Opção 1: Download Oficial (Recomendado)

1. **Baixe o Python 3.11:**
   - Acesse: <https://www.python.org/downloads/>
   - Clique em "Download Python 3.11.x"
   - Baixe o instalador para Windows (x86-64)

2. **Execute a instalação:**

   ```powershell
   # Execute como administrador e marque as opções:
   # ✅ Add Python to PATH
   # ✅ Install for all users (opcional)
   ```

3. **Verifique a instalação:**

   ```powershell
   python --version
   # Deve exibir: Python 3.11.x
   
   pip --version
   # Deve exibir a versão do pip
   ```

#### Opção 2: Usando Chocolatey

1. **Instale o Chocolatey** (se não tiver):

   ```powershell
   # Execute como administrador
   Set-ExecutionPolicy Bypass -Scope Process -Force
   [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
   iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
   ```

2. **Instale o Python:**

   ```powershell
   choco install python311 -y
   refreshenv
   ```

#### Opção 3: Usando Winget

```powershell
# Execute no PowerShell
winget install Python.Python.3.11
```

### <a id="windows-uv"></a>⚡ 2. Instalação do UV

UV é um gerenciador de pacotes Python ultrarrápido que substitui pip, poetry e pipenv.

```powershell
# Método 1: PowerShell (Recomendado)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Método 2: pip
pip install uv

# Método 3: Chocolatey
choco install uv -y

# Verifique a instalação
uv --version
```

### <a id="windows-projeto"></a>📦 3. Configuração do Projeto

1. **Clone ou baixe o projeto:**

   ```powershell
   git clone https://github.com/jhonne/curso-ai-multiagentes.git
   cd curso-ai-multiagentes
   ```

2. **Configure o ambiente automaticamente:**

   ```powershell
   # UV irá criar automaticamente um ambiente virtual e instalar dependências
   uv sync
   ```

3. **Ou configure manualmente:**

   ```powershell
   # Criar ambiente virtual
   uv venv
   
   # Ativar ambiente virtual
   .\.venv\Scripts\Activate.ps1
   
   # Instalar dependências
   uv pip install -r requirements.txt
   ```

---

## 🐧 Linux

### <a id="linux-python"></a>🐍 1. Instalação do Python 3.11

#### Ubuntu/Debian

```bash
# Atualize o sistema
sudo apt update && sudo apt upgrade -y

# Instale dependências necessárias
sudo apt install -y software-properties-common build-essential

# Adicione o repositório deadsnakes (para Ubuntu < 22.04)
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update

# Instale Python 3.11
sudo apt install -y python3.11 python3.11-dev python3.11-venv python3.11-distutils

# Instale pip para Python 3.11
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11

# Crie um link simbólico (opcional)
sudo ln -sf /usr/bin/python3.11 /usr/local/bin/python
sudo ln -sf /usr/bin/python3.11 /usr/local/bin/python3

# Verifique a instalação
python3.11 --version
pip3.11 --version
```

#### CentOS/RHEL/Fedora

```bash
# CentOS/RHEL
sudo yum install -y epel-release
sudo yum groupinstall -y "Development Tools"
sudo yum install -y python3.11 python3.11-devel python3.11-pip

# Fedora
sudo dnf install -y python3.11 python3.11-devel python3.11-pip

# Verifique a instalação
python3.11 --version
```

#### Arch Linux

```bash
# Instale Python 3.11
sudo pacman -S python python-pip python-virtualenv

# Verifique a instalação
python --version
```

### <a id="linux-uv"></a>⚡ 2. Instalação do UV

```bash
# Método 1: Curl (Recomendado)
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Método 2: pip
python3.11 -m pip install uv

# Método 3: Usar Python diretamente
python3.11 -c "import urllib.request; urllib.request.urlretrieve('https://astral.sh/uv/install.sh', 'install.sh')"
bash install.sh
rm install.sh

# Verifique a instalação
uv --version
```

### <a id="linux-projeto"></a>📦 3. Configuração do Projeto

```bash
# Clone o projeto
git clone https://github.com/seu-usuario/curso-crewai.git
cd curso-crewai

# Configure automaticamente com UV
uv sync

# Ou configure manualmente
uv venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

---

## <a id="configuracao-comum"></a>🔧 Configuração Comum (Windows & Linux)

### 1. Configurar Variáveis de Ambiente

1. **Crie o arquivo .env:**

   ```bash
   # Copie o template
   cp .env.example .env
   
   # Windows (PowerShell)
   Copy-Item .env.example .env
   ```

2. **Edite o arquivo .env:**

   ```env
   # Sua chave da OpenAI (obrigatório)
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   
   # Configurações opcionais
   OPENAI_MODEL=gpt-4
   OPENAI_TEMPERATURE=0.7
   CREWAI_TELEMETRY_OPT_OUT=true
   ```

3. **Obtenha sua chave da OpenAI:**
   - Acesse: <https://platform.openai.com/api-keys>
   - Faça login/cadastro
   - Clique em "Create new secret key"
   - Copie e cole no arquivo .env

### 2. Instalar Dependências Opcionais

```bash
# Para desenvolvimento
uv add --group dev pytest pytest-cov black flake8 mypy pre-commit

# Para interface web
uv add --group web streamlit flask

# Para ferramentas extras
uv add --group tools requests pydantic rich

# Ou instalar todas de uma vez
uv sync --group dev --group web --group tools
```

### 3. Configurar Git Hooks (Opcional)

```bash
# Instalar pre-commit
uv add --group dev pre-commit

# Configurar hooks
uv run pre-commit install

# Testar hooks
uv run pre-commit run --all-files
```

---

## <a id="verificacao"></a>✅ Verificação da Instalação

Execute estes comandos para verificar se tudo está funcionando:

### 1. Verificar Python e UV

```bash
# Verificar versões
python --version          # Deve mostrar Python 3.11.x
uv --version              # Deve mostrar a versão do UV

# Verificar instalação do projeto
uv run hello-crewai       # Executa o exemplo principal
uv run teste-api          # Testa conexão com OpenAI
```

### 2. Executar Configuração Automática

```bash
# Execute o configurador do projeto
uv run configurar-crewai

# Ou execute manualmente
uv run python src/curso_crewai/configurar.py
```

### 3. Testar Funcionalidades

```bash
# Teste básico
uv run python src/curso_crewai/hello_simples.py

# Teste com CrewAI
uv run python src/curso_crewai/hello_crewai.py

# Verificar dependências
uv tree
```

### 4. Saída Esperada

Se tudo estiver correto, você deve ver algo como:

```
🚀 Iniciando Hello CrewAI...
✅ Chave da OpenAI configurada!
✅ CrewAI instalado e funcionando!
🤖 Executando o crew...

[... processo de pensamento do agente ...]

✅ Resultado final:
Olá! 👋 Seja muito bem-vindo ao fantástico mundo do CrewAI!
🎉 Hello CrewAI executado com sucesso!
```

---

## <a id="problemas"></a>🔧 Solução de Problemas

### Python não encontrado

**Windows:**

```powershell
# Adicionar ao PATH manualmente
$env:PATH += ";C:\Python311;C:\Python311\Scripts"

# Ou criar alias
Set-Alias python "C:\Python311\python.exe"
```

**Linux:**

```bash
# Adicionar ao PATH
echo 'export PATH="/usr/bin/python3.11:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Ou criar link simbólico
sudo ln -sf /usr/bin/python3.11 /usr/local/bin/python
```

### UV não instalado corretamente

```bash
# Reinstalar UV
python -m pip uninstall uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Erro "OPENAI_API_KEY não encontrada"

1. Verifique se o arquivo `.env` existe
2. Confirme se a chave está correta
3. Reinicie o terminal
4. Teste manualmente:

   ```bash
   uv run python -c "import os; print('Chave:', os.getenv('OPENAI_API_KEY', 'NÃO ENCONTRADA'))"
   ```

### Problemas de dependências

```bash
# Limpar cache e reinstalar
uv cache clean
rm -rf .venv uv.lock
uv sync

# Windows
Remove-Item -Recurse -Force .venv, uv.lock
uv sync
```

### Erro de permissões (Linux)

```bash
# Instalar no usuário local
python3.11 -m pip install --user uv

# Ou usar sudo
sudo python3.11 -m pip install uv
```

### Problemas de SSL/Certificados

```bash
# Atualizar certificados
pip install --upgrade certifi

# Usar HTTP ao invés de HTTPS (temporário)
uv pip install --index-url http://pypi.org/simple/ --trusted-host pypi.org package_name
```

### Performance lenta

```bash
# Usar mirror local (Brasil)
uv pip install --index-url https://pypi.org/simple/ -i https://pypi.douban.com/simple/

# Aumentar timeout
uv pip install --timeout 300 package_name
```

---

## 📚 Recursos Adicionais

### Documentação Útil

- [Python.org](https://www.python.org/downloads/)
- [UV Documentation](https://docs.astral.sh/uv/)
- [CrewAI Documentation](https://docs.crewai.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)

### Comandos UV Essenciais

```bash
# Gerenciamento de projeto
uv init                    # Inicializar projeto
uv sync                    # Sincronizar dependências
uv add package             # Adicionar dependência
uv remove package          # Remover dependência
uv tree                    # Ver árvore de dependências

# Gerenciamento de ambiente
uv venv                    # Criar ambiente virtual
uv venv --python 3.11      # Criar com Python específico
uv pip list                # Listar pacotes instalados
uv pip freeze              # Exportar dependências

# Execução
uv run script.py           # Executar script
uv run --python 3.11 script.py  # Executar com Python específico
uv shell                   # Ativar shell do ambiente
```

### Scripts de Automação

**Windows (PowerShell):**

```powershell
# Criar script setup.ps1
@"
# Instalação automática
winget install Python.Python.3.11
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
git clone https://github.com/seu-usuario/curso-crewai.git
cd curso-crewai
uv sync
uv run configurar-crewai
"@ | Out-File -FilePath setup.ps1
```

**Linux (Bash):**

```bash
# Criar script setup.sh
cat > setup.sh << 'EOF'
#!/bin/bash
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-pip
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc
git clone https://github.com/seu-usuario/curso-crewai.git
cd curso-crewai
uv sync
uv run configurar-crewai
EOF

chmod +x setup.sh
./setup.sh
```

---

## 🎯 Próximos Passos

Após configurar o ambiente com sucesso:

1. **Execute o teste inicial:**

   ```bash
   uv run hello-crewai
   ```

2. **Explore os exemplos:**

   ```bash
   uv run python src/curso_crewai/hello_simples.py
   uv run teste-api
   ```

3. **Continue com o curso:**
   - Leia o arquivo `README.md` para mais informações
   - Explore os módulos em `src/curso_crewai/`
   - Consulte `curso.md` para conteúdo adicional

4. **Personalize seu ambiente:**
   - Configure seu editor preferido
   - Instale extensões VS Code para Python
   - Configure debugger e linting

---

**📧 Suporte:** Se encontrar problemas, consulte a seção [Solução de Problemas](#problemas) ou abra uma issue no repositório do projeto.

**🚀 Boa sorte com seu aprendizado em CrewAI!**
