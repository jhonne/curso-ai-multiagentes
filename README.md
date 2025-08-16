# Hello CrewAI - Exemplo Básico

Este é um exemplo introdutório baseado no **Módulo 1, Aula 1** do curso "Desenvolvendo Chatbots com Múltiplos Agentes usando CrewAI e OpenAI".

## 🎯 O que este exemplo demonstra

- Como criar seu primeiro agente CrewAI
- Como definir uma tarefa simples
- Como executar um crew com um único agente
- Configuração básica do ambiente

## 📋 Pré-requisitos

1. **Python 3.8+** instalado
2. **Chave de API da OpenAI** (obtenha em: https://platform.openai.com/api-keys)
3. **pip** para instalação de pacotes

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
   ```
   OPENAI_API_KEY=sua_chave_real_aqui
   ```

### 3. Executar o exemplo

```bash
# Com UV (recomendado)
uv run hello-crewai

# Com Python tradicional
python hello_crewai.py

# Usando o módulo
uv run python -m curso_crewai.hello_crewai
```

## 📖 O que acontece quando executar

1. O programa verifica se a chave da OpenAI está configurada
2. Cria um agente "Assistente Amigável" com papel e objetivo definidos
3. Define uma tarefa para o agente criar uma mensagem de boas-vindas
4. Executa o crew e exibe o resultado

## 🔍 Exemplo de saída esperada

```
🚀 Iniciando Hello CrewAI...

🤖 Executando o crew...
==================================================

[Aqui você verá o processo de pensamento do agente]

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

## 🎓 Próximos passos

Este é apenas o primeiro exemplo do curso! Continue com:

- **Aula 2**: Construindo seu Primeiro Crew com múltiplos agentes
- **Aula 3**: Adicionando ferramentas e processos  
- **Módulo 2**: Construindo um chatbot completo

## 🔧 Comandos UV úteis

```bash
# Testar configuração
uv run teste-api

# Executar exemplo simples
uv run python src/curso_crewai/hello_simples.py

# Adicionar nova dependência
uv add <package>

# Ver dependências instaladas
uv tree
```

## 📚 Recursos adicionais

- [Documentação oficial do CrewAI](https://docs.crewai.com/)
- [Documentação da OpenAI](https://platform.openai.com/docs)
- [Repositório do curso completo](link_do_repositorio)

## ❓ Problemas comuns

### "OPENAI_API_KEY não encontrada!"
- Verifique se você criou o arquivo `.env`
- Confirme se a chave está correta e sem espaços extras

### Erro de instalação do CrewAI
- Atualize o pip: `pip install --upgrade pip`
- Use um ambiente virtual: `python -m venv venv` e ative-o

### Timeout ou erro de conexão
- Verifique sua conexão com a internet
- Confirme se sua chave da OpenAI está ativa e com créditos

---

**Curso:** Desenvolvendo Chatbots com Múltiplos Agentes usando CrewAI e OpenAI  
**Módulo:** 1 - Fundamentos do CrewAI  
**Aula:** 1 - Introdução à IA de Agentes e ao CrewAI
