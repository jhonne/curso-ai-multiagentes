# Guia de uso com UV

## Comandos básicos

### Instalação inicial
```bash
# Instalar UV (se ainda não tiver)
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Linux/Mac  
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Configuração do projeto
```bash
# Inicializar ambiente virtual e instalar dependências
uv sync

# Configurar ambiente
uv run configurar-crewai
```

### Executar exemplos
```bash
# Teste da API
uv run teste-api

# Hello CrewAI completo
uv run hello-crewai

# Hello CrewAI simples
uv run python src/curso_crewai/hello_simples.py
```

### Gerenciar dependências
```bash
# Adicionar nova dependência
uv add <package>

# Adicionar dependência de desenvolvimento  
uv add --dev <package>

# Remover dependência
uv remove <package>

# Atualizar dependências
uv sync --upgrade
```

### Scripts personalizados
```bash
# Definidos em pyproject.toml [project.scripts]
uv run hello-crewai
uv run teste-api
uv run configurar-crewai
```