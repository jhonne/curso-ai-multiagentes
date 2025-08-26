# Dicas para Execução de Scripts Python com UV

## Passos para executar scripts nas aulas

### 1. Carregar o ambiente Python

Antes de executar qualquer script, certifique-se de que o ambiente virtual está ativo:

```bash
# Ativar o ambiente virtual com UV
source .venv/bin/activate  # No Linux/Mac
# ou
.venv\Scripts\activate     # No Windows
```

### 2. Instalar dependências (se necessário)

```bash
# Instalar todas as dependências do projeto
uv pip install -r requirements.txt

# Ou instalar dependências específicas
uv pip install crewai openai
```

### 3. Navegar para a pasta da aula

```bash
# Exemplo: entrar na aula1
cd aula1

# Exemplo: entrar na aula2
cd aula2

# Exemplo: entrar na aula3
cd aula3
```

### 4. Executar scripts Python com UV

```bash
# Executar o main.py da aula
uv run main.py

# Ou executar qualquer script específico
uv run nome_do_script.py

# Exemplo: executar solução de exercício
uv run exercicio1_solucao.py
```

### 5. Executar diretamente do diretório raiz

Você também pode executar scripts de qualquer aula sem navegar para a pasta:

```bash
# Executar main.py da aula1 a partir do diretório raiz
uv run aula1/main.py

# Executar main.py da aula2 a partir do diretório raiz
uv run aula2/main.py

# Executar exercício específico
uv run aula2/exercicio1_solucao.py
```

## Comandos úteis com UV

### Verificar versão do Python

```bash
uv python --version
```

### Listar pacotes instalados

```bash
uv pip list
```

### Instalar pacote específico

```bash
uv pip install nome_do_pacote
```

### Atualizar pacotes

```bash
uv pip install --upgrade nome_do_pacote
```

## Exemplo prático completo

```bash
# 1. Ativar ambiente
uv venv
.venv\Scripts\activate     # Windows

# 2. Instalar dependências
uv pip install -r requirements.txt

# 3. Navegar para aula
cd aula1

# 4. Executar script
uv run main.py
```

## Troubleshooting

### Se houver erro de módulo não encontrado

```bash
# Reinstalar dependências
uv pip install -r requirements.txt

# Verificar se o ambiente está ativo
uv venv --show-path
```

### Se houver erro de API Key

Certifique-se de que a variável de ambiente `OPENAI_API_KEY` está configurada:

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sua_chave_aqui"

# Windows CMD
set OPENAI_API_KEY=sua_chave_aqui

# Linux/Mac
export OPENAI_API_KEY="sua_chave_aqui"
```
