# Migração para UV

Este projeto agora suporta UV (ferramenta moderna de gerenciamento Python) além do pip tradicional.

## 🆕 Por que UV?

- ⚡ **Muito mais rápido** que pip (instalações em segundos)
- 🔒 **Lock files automáticos** para reproduzibilidade
- 🏗️ **Ambientes virtuais automáticos**
- 📦 **Gerenciamento de dependências melhorado**
- 🚀 **Execução de scripts simplificada**

## 🔄 Como migrar

### Se você já tem o projeto configurado com pip

1. **Instalar UV:**

   ```bash
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Linux/Mac
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Migrar para UV:**

   ```bash
   # Criar pyproject.toml (se não existir)
   uv init --no-readme
   
   # Sincronizar dependências existentes
   uv sync
   ```

3. **Testar:**

   ```bash
   uv run teste-api
   ```

### Se você está começando do zero

```bash
# Clonar e configurar automaticamente
git clone <repo>
cd curso-crewai
uv run configurar-crewai
```

## 📋 Comandos equivalentes

| Tarefa | Pip tradicional | UV |
|--------|----------------|------|
| Instalar deps | `pip install -r requirements.txt` | `uv sync` |
| Adicionar pacote | `pip install package` | `uv add package` |
| Executar script | `python script.py` | `uv run script.py` |
| Ativar venv | `source venv/bin/activate` | *(automático)* |
| Hello CrewAI | `python hello_crewai.py` | `uv run hello-crewai` |
| Teste API | `python teste_api.py` | `uv run teste-api` |

## 🏃‍♂️ Scripts rápidos

Com UV, você pode executar scripts diretamente sem ativar ambiente virtual:

```bash
# Scripts definidos no pyproject.toml
uv run hello-crewai      # Exemplo principal
uv run teste-api         # Teste da API  
uv run configurar-crewai # Configuração

# Scripts Python diretos
uv run hello_simples.py
uv run -m curso_crewai.hello_crewai
```

## 🔍 Verificação

Para verificar se migrou corretamente:

```bash
# Ver dependências instaladas
uv tree

# Status do projeto
uv show

# Executar teste
uv run teste-api
```

## 🆘 Troubleshooting

### "uv: command not found"

- UV não está instalado ou não está no PATH
- Reinicie o terminal após instalação

### "No pyproject.toml found"

```bash
uv init --no-readme
uv sync
```

### Dependências não encontradas

```bash
# Reinstalar todas as dependências
uv sync --reinstall
```

## 🤝 Compatibilidade

O projeto mantém compatibilidade com pip:

- `requirements.txt` ainda funciona
- Scripts Python podem ser executados tradicionalmente
- `.env` funciona da mesma forma

**UV é recomendado, mas não obrigatório!**
