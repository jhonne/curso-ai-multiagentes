# 🚀 Curso de CrewAI - Desenvolvendo Chatbots com Múltiplos Agentes

**Curso Básico de 20 Horas:** Desenvolvendo Chatbots com Múltiplos Agentes usando CrewAI e OpenAI

Este repositório contém exemplos práticos, exercícios e projetos do curso completo de CrewAI, desde conceitos básicos até a implementação de chatbots avançados com múltiplos agentes de IA.

## 📚 Sobre o Curso

**Nível:** Iniciante  
**Carga Horária:** 20 horas  
**Framework Principal:** CrewAI + OpenAI  
**Linguagem:** Python 3.11

### 🎯 Objetivos do Curso

- Compreender o paradigma de sistemas multi-agente
- Dominar o framework CrewAI para orquestração de agentes
- Construir chatbots inteligentes e colaborativos
- Integrar modelos de linguagem da OpenAI
- Desenvolver soluções práticas com IA conversacional

## 🗂️ Estrutura do Projeto

```text
curso_crewai/
├── 📁 aula1/              # Módulo 1: Fundamentos
│   └── main.py            # Primeiro agente CrewAI
├── 📁 aula2/              # Módulo 1: Agentes e Tarefas
│   ├── main.py            # Crew com múltiplos agentes
│   ├── README.md          # Documentação da aula
│   ├── README_SOLUCOES.md # Guia das soluções
│   ├── exercicio1_agencia_marketing.md
│   ├── exercicio1_solucao.py  # Solução: Equipe de conteúdo
│   ├── exercicio2_atendimento_cliente.md
│   ├── exercicio2_solucao.py  # Solução: Atendimento ao cliente
│   ├── exercicio3_desenvolvimento_produto.md
│   └── exercicio3_solucao.py  # Solução: Desenvolvimento de produto
├── 📁 aula3/              # Módulo 1: Ferramentas e Processos
│   ├── main.py            # Comparação de processos com simulações
│   ├── README.md          # Documentação completa
│   └── exercicios.md      # Exercícios práticos
├── 📁 material_de_apoio/  # PDFs e documentação
├── 📁 podcasts/           # Conteúdo em áudio
├── hello_crewai.py        # Exemplo principal do curso
├── hello_simples.py       # Exemplo simplificado
├── teste_api.py           # Verificação de conexão OpenAI
├── configurar.py          # Script de configuração automática
└── verificar_openai.py    # Validação de ambiente
```

## 📋 Pré-requisitos

1. **Python 3.10+** instalado
2. **Chave de API da OpenAI** (obtenha em: <https://platform.openai.com/api-keys>)
3. **UV** (gerenciador de pacotes - recomendado) ou **pip**
4. **Git** para clonagem do repositório

## 🚀 Como executar

### Opção 1: Usando UV (Recomendado) ⚡

```bash
# Instalar UV (se ainda não tiver)
# Windows:
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Configurar projeto automaticamente
uv run configurar-crewai

# Ou manualmente:
uv sync  # Instala dependências
```

### Opção 2: Usando pip tradicional

```bash
pip install -r requirements.txt
```

### 2. Configurar variáveis de ambiente

1. Copie o arquivo de exemplo:

   ```bash
   copy .env.example .env
   ```

2. Edite o arquivo `.env` e adicione sua chave da OpenAI:

   ```text
   OPENAI_API_KEY=sua_chave_real_aqui
   ```

### 3. Executar o exemplo

```bash
# Com UV (recomendado)
uv run hello-crewai

# Com UV (recomendado)
uv run hello_crewai.py

# Usando o módulo
uv run -m curso_crewai.hello_crewai
```

## � Conteúdo do Curso

### 📚 Módulo 1: Fundamentos do CrewAI (6 horas) ✅

- **Aula 1:** Introdução à IA de Agentes e ao CrewAI (2h) ✅
  - 📁 `aula1/main.py` - Primeiro agente CrewAI
  - 📄 Configuração de ambiente e conceitos básicos
  
- **Aula 2:** Construindo seu Primeiro Crew (2h) ✅
  - 📁 `aula2/main.py` - Crew com múltiplos agentes (Pesquisador + Redator)
  - 📁 `aula2/README.md` - Documentação completa da aula
  - 📁 `aula2/README_SOLUCOES.md` - Guia das soluções dos exercícios
  - � **Exercício 1:** Agência de Marketing (`exercicio1_solucao.py`)
    - Equipe de conteúdo para redes sociais (Gerador de Ideias + Escritor)
  - 🛒 **Exercício 2:** Atendimento ao Cliente (`exercicio2_solucao.py`)
    - Processamento de reclamações (Analisador + Respondedor Amigável)
  - 📱 **Exercício 3:** Desenvolvimento de Produto (`exercicio3_solucao.py`)
    - Criação de app para estudantes (Descobridor + Criador de Ideias)
  - �📄 Agentes, tarefas e colaboração sequencial
  
- **Aula 3:** Ferramentas e Processos (2h) ✅
  - � `aula3/main.py` - Simulações de ferramentas e comparação de processos
  - 📁 `aula3/README.md` - Documentação completa com exemplos
  - 📁 `aula3/exercicios.md` - Exercícios práticos e desafios
  - 🔧 Simulações de ferramentas (pesquisa web, scraping, arquivos)
  - ⚙️ Processos sequenciais vs hierárquicos com medição de performance

### 🤖 Módulo 2: Chatbot Multi-Agente (10 horas)

- **Aula 4:** Arquitetura de Chatbot (2h)
- **Aula 5:** Implementação com OpenAI (3h)
- **Aula 6:** Fluxo de Conversa (3h)
- **Aula 7:** Interface de Chat (2h)

### 🚀 Módulo 3: Tópicos Avançados (4 horas)

- **Aula 8:** Memória e Ferramentas Personalizadas (2h)
- **Aula 9:** Debugging e Próximos Passos (2h)

## �📖 O que acontece quando executar

Quando você executa `uv run hello-crewai`, o sistema:

1. ✅ Verifica se a chave da OpenAI está configurada
2. 🤖 Cria um agente "Assistente Amigável em Português"
3. 📝 Define uma tarefa para criar mensagem de boas-vindas
4. ⚡ Executa o crew e processa a resposta
5. 📤 Exibe o resultado final

## 🔍 Exemplo de Saída Esperada

```console
🚀 Iniciando Hello CrewAI...

🤖 Executando o crew...
==================================================

> Entering new CrewAgentExecutor chain...

[Aqui você verá o processo de pensamento do agente em português]

==================================================
✅ Resultado final:
==================================================

Olá! 👋 Seja muito bem-vindo ao fantástico mundo do CrewAI!

O CrewAI é um framework revolucionário que permite criar equipes de 
agentes de inteligência artificial que trabalham juntos para resolver 
problemas complexos. Imagine ter uma equipe de especialistas virtuais, 
cada um com suas próprias habilidades e conhecimentos, colaborando 
para entregar resultados incríveis!

Continue explorando e aprendendo - você está prestes a descobrir como 
construir sistemas de IA verdadeiramente poderosos! 🚀

🎉 Hello CrewAI executado com sucesso!
```

## 🎓 Próximos Passos

Após configurar o ambiente e executar os primeiros exemplos:

1. **📚 Estude o material de apoio:**
   - 📄 `material_de_apoio/` - PDFs com conceitos fundamentais
   - 🎧 `podcasts/` - Conteúdo em áudio sobre CrewAI

2. **🔍 Explore os exemplos:**
   - `hello_simples.py` - Versão simplificada
   - `aula1/main.py` - Primeiro agente
   - `aula2/main.py` - Crew colaborativo (Pesquisador + Redator)
   - `aula2/exercicio*_solucao.py` - 3 soluções práticas de crews
   - `aula3/main.py` - Ferramentas e processos avançados

3. **🚀 Continue o curso:**
   - **Aula 3:** `aula3/main.py` - Ferramentas e processos avançados
   - **Módulo 2:** Construindo chatbot completo
   - **Módulo 3:** Funcionalidades avançadas

## 🔧 Comandos UV Úteis

### Execução de Exemplos

```bash
# Testar configuração da API
uv run teste-api

# Verificar ambiente OpenAI
uv run verificar_openai.py

# Executar configuração automática
uv run configurar-crewai

# Executar exemplos das aulas
uv run aula1/main.py
uv run aula2/main.py

# Executar exercícios específicos da aula2
uv run aula2/exercicio1_solucao.py  # Marketing
uv run aula2/exercicio2_solucao.py  # Atendimento
uv run aula2/exercicio3_solucao.py  # Desenvolvimento

# Executar aula3
uv run aula3/main.py
```

### Gerenciamento do Projeto

```bash
# Ver dependências instaladas
uv tree

# Adicionar nova dependência
uv add <package>

# Atualizar dependências
uv sync

# Executar em ambiente limpo
uv run --isolated hello_crewai.py

# Ver informações do projeto
uv show
```

### Desenvolvimento

```bash
# Instalar dependências de desenvolvimento
uv sync --group dev

# Executar testes (quando disponíveis)
uv run pytest

# Formatar código
uv run black .

# Verificar tipos
uv run mypy .
```

## 📚 Recursos Adicionais

### Documentação Oficial

- 📖 [CrewAI Documentation](https://docs.crewai.com/)
- 🤖 [OpenAI API Documentation](https://platform.openai.com/docs)
- ⚡ [UV Package Manager](https://docs.astral.sh/uv/)
- 🐍 [Python 3.11+ Documentation](https://docs.python.org/3/)

### 📑 Índice de Documentação

#### 🚀 Configuração e Início Rápido

- 📄 [INICIO_RAPIDO.md](docs/INICIO_RAPIDO.md) - Guia de início rápido
- ⚙️ [CONFIGURACAO_AMBIENTE.md](docs/CONFIGURACAO_AMBIENTE.md) - Guia detalhado de configuração
- 📦 [UV_GUIDE.md](docs/UV_GUIDE.md) - Guia completo do UV Package Manager
- 🔄 [MIGRACAO_UV.md](docs/MIGRACAO_UV.md) - Como migrar de pip para UV
- 📊 [STATUS_UV.md](docs/STATUS_UV.md) - Status da migração para UV

#### 📚 Referências e Guias

- 📚 [CREWAI_REFERENCE.md](docs/CREWAI_REFERENCE.md) - Guia completo sobre CrewAI
- 📖 [CURSO.md](docs/CURSO.md) - Cronograma completo do curso
- 💡 [DICAS.md](docs/DICAS.md) - Dicas e truques úteis
- 🎯 [GUIA_BOAS_PRATICAS_PROMPTS.md](docs/GUIA_BOAS_PRATICAS_PROMPTS.md) - Boas práticas para prompts

#### 🔒 Segurança e Otimização

- 🛡️ [GUIA_SEGURANCA.md](docs/GUIA_SEGURANCA.md) - Guia de segurança
- ⚡ [GUIA_OTIMIZACAO_OPENAI.md](docs/GUIA_OTIMIZACAO_OPENAI.md) - Otimização para OpenAI
- 📈 [README_OTIMIZACAO.md](docs/README_OTIMIZACAO.md) - Documentação de otimização
- 📋 [RESUMO_OTIMIZACAO_OPENAI.md](docs/RESUMO_OTIMIZACAO_OPENAI.md) - Resumo de otimização
- 📊 [INDICE_OTIMIZACAO.md](docs/INDICE_OTIMIZACAO.md) - Índice de otimização
- 🔐 [ATUALIZACAO_INSTRUCOES_SEGURANCA_ECONOMIA.md](docs/ATUALIZACAO_INSTRUCOES_SEGURANCA_ECONOMIA.md) - Atualizações de segurança

### Material do Curso

- 📁 `material_de_apoio/` - PDFs com conceitos fundamentais
- 🎧 `podcasts/` - Conteúdo em áudio sobre CrewAI
- 📄 `docs/CURSO.md` - Cronograma completo do curso
- ⚙️ `docs/CONFIGURACAO_AMBIENTE.md` - Guia detalhado de configuração
- 🤖 `aula2/` - Implementação completa de crews multi-agente
  - 👥 Colaboração entre Pesquisador e Redator
  - 📝 3 exercícios práticos com soluções completas
  - 💼 Cenários reais: marketing, atendimento e desenvolvimento
  - 🔄 Fluxo de trabalho sequencial detalhado
- 🔧 `aula3/` - Implementação completa de ferramentas e processos
  - 📊 Comparação de performance entre processos
  - 🛠️ Simulações de ferramentas (sem dependências externas)
  - 📚 Exercícios práticos e desafios avançados

### Repositórios e Comunidade

- 🌟 [Repositório Original](https://github.com/jhonne/curso-ai-multiagentes)
- 🤝 [CrewAI Community](https://github.com/joaomdmoura/crewAI)
- 💬 [OpenAI Community](https://community.openai.com/)

## ❓ Solução de Problemas Comuns

### 🔑 "OPENAI_API_KEY não encontrada!"

```bash
# Verificar se o arquivo .env existe
ls -la .env  # Linux/Mac
dir .env     # Windows

# Verificar conteúdo do arquivo
cat .env     # Linux/Mac
type .env    # Windows

# Testar a chave manualmente
uv run -c "import os; print('Chave:', os.getenv('OPENAI_API_KEY', 'NÃO ENCONTRADA'))"
```

**Soluções:**

- ✅ Verifique se criou o arquivo `.env` na raiz do projeto
- ✅ Confirme se a chave está correta (inicia com `sk-`)
- ✅ Remova espaços extras antes/depois da chave
- ✅ Reinicie o terminal após editar o `.env`

### 📦 Erro de Instalação de Dependências

```bash
# Limpar cache e reinstalar
uv cache clean
rm -rf .venv uv.lock  # Linux/Mac
Remove-Item -Recurse -Force .venv, uv.lock  # Windows
uv sync

# Alternativa com pip
pip install --upgrade pip
pip install -r requirements.txt
```

### 🌐 Timeout ou Erro de Conexão

```bash
# Testar conectividade
ping api.openai.com

# Verificar status da conta OpenAI
uv run teste-api

# Verificar saldo/créditos em: https://platform.openai.com/usage
```

### 🐍 Python não Encontrado

```powershell
# Windows - Adicionar ao PATH
$env:PATH += ";C:\Python311;C:\Python311\Scripts"

# Verificar instalação
python --version
which python  # Linux/Mac
where python  # Windows
```

### 🔧 Problemas de Permissão (Linux)

```bash
# Instalar UV no usuário local
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Ou usar sudo para instalação global
sudo python3.11 -m pip install uv
```

## 📊 Estimativa de Custos OpenAI

| Modelo | Custo por 1K tokens | Uso estimado/exemplo | Custo por execução |
|--------|-------------------|---------------------|-------------------|
| GPT-3.5-turbo | $0.0015/$0.002 | ~2K tokens | ~$0.007 |
| GPT-4 | $0.03/$0.06 | ~1K tokens | ~$0.09 |
| GPT-4-turbo | $0.01/$0.03 | ~1K tokens | ~$0.04 |

> 💡 **Dica:** Use GPT-3.5-turbo para desenvolvimento e testes para economizar custos.

## 🚀 Status do Projeto

- ✅ **Módulo 1:** Fundamentos **COMPLETOS** (Aulas 1, 2 e 3 implementadas)
  - ✅ Aula 1: Primeiro agente CrewAI
  - ✅ Aula 2: Crew com múltiplos agentes + 3 exercícios práticos resolvidos
  - ✅ Aula 3: Ferramentas e processos com simulações
- � **Módulo 2:** Chatbot Multi-Agente (planejado)
- 📋 **Módulo 3:** Tópicos Avançados (planejado)
- 🎯 **Versão atual:** 0.2.0
- 📈 **Progresso:** 15% do curso implementado (3/20 horas)

---

**📚 Curso:** Desenvolvendo Chatbots com Múltiplos Agentes usando CrewAI e OpenAI  
**🎯 Repositório:** [curso-ai-multiagentes](https://github.com/jhonne/curso-ai-multiagentes)  
**👨‍💻 Autor:** [@jhonne](https://github.com/jhonne)  
**📅 Última atualização:** Agosto 2025  
**📈 Progresso:** Módulo 1 completo (3/9 aulas implementadas)

---

> 💡 **Dica:** Para uma experiência completa de configuração, consulte sempre o arquivo **[CONFIGURACAO_AMBIENTE.md](docs/CONFIGURACAO_AMBIENTE.md)** antes de começar!
