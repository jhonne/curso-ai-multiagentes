# 📚 EXERCÍCIO SIMPLES AULA 8 - INSTRUÇÕES

## 🎯 OBJETIVO

Aplicar **TODOS os conceitos da Aula 8** criando um sistema super simples (< 150 linhas) usando dados REAIS do banco SQLite existente do curso.

## ⏱️ TEMPO ESTIMADO: 15-20 minutos

## 🎓 CONCEITOS APLICADOS (da Aula 8)

- ✅ **Sistema interativo** - Loop básico de conversação
- ✅ **Ferramenta personalizada** - Classe `BaseTool` customizada
- ✅ **SQLite com dados REAIS** - Usa o banco curso.db existente
- ✅ **Agente especializado** - Agent com backstory específico

## 🚀 COMO EXECUTAR

```bash
# 1. Verificar que está no diretório do projeto
cd /caminho/para/curso_crewai

# 2. Verificar OpenAI API Key configurada
cat .env | grep OPENAI_API_KEY

# 3. Executar o exercício simples (< 150 linhas)
uv run aula8/exercicio_simples_aula8.py
```

## 📋 O QUE O EXERCÍCIO FAZ

### 🏥 **Usa dados REAIS de saúde**

- Conecta ao banco `db/curso.db` existente no projeto
- Consulta estabelecimentos reais (hospitais, UPAs, postos)
- Mostra queixas médicas mais frequentes
- Exibe estatísticas reais do sistema de saúde

### 🛠️ **Ferramenta super simples**

```python
class ConsultaSaude(BaseTool):
    # 3 tipos de consulta básicas:
    # - Estabelecimentos
    # - Queixas frequentes  
    # - Estatísticas gerais
```

### 🤖 **Agente especialista**

```python
agente = Agent(
    role="Assistente de Saúde",
    backstory="Especialista em dados de saúde pública",
    tools=[ConsultaSaude()]
)
```

### 💬 **Sistema interativo básico**

- Loop simples de perguntas/respostas
- Comando `sair` para encerrar

## 🎮 COMO USAR

### ✨ Exemplos de perguntas

```
💬 "Quais estabelecimentos temos?"
💬 "Mostre as queixas mais frequentes"
💬 "Estatísticas gerais"
```

### ⌨️ Comandos

```
sair   - Encerra o programa
```

## 📊 DADOS REAIS DO EXERCÍCIO

**Dados do sistema de saúde real:**

- 2.847+ estabelecimentos de saúde
- 156+ tipos de queixas médicas
- 125.394+ registros de atendimento
- Dados de hospitais, UPAs, postos de saúde
- Informações de bairros e endereços

## 🔍 TIPOS DE CONSULTA

### 🏥 **Estabelecimentos:**

- Lista hospitais, UPAs, postos de saúde
- Mostra nome e bairro
- Dados REAIS do sistema

### 🏥 **Queixas médicas:**

- Queixas mais frequentes
- Número de casos por tipo
- Baseado em dados reais de atendimento

### 📊 **Estatísticas:**

- Total de estabelecimentos
- Tipos de queixas cadastradas
- Visão geral do sistema

## 💡 VANTAGENS DO EXERCÍCIO REFORMULADO

### 🎯 **Super simples:**

- ✅ **Apenas 147 linhas** (vs 400+ anteriores)
- ✅ **3 tipos básicos** de consulta
- ✅ **Conceitos essenciais** da Aula 8
- ✅ **Tempo adequado** para aula (15-20 min)

### 🏥 **Dados REAIS:**

- ✅ **Banco existente** - usa db/curso.db do projeto
- ✅ **Sem setup adicional** - não cria banco temporário
- ✅ **Dados significativos** - sistema de saúde real
- ✅ **Mais interessante** - estabelecimentos e queixas reais

### 🔧 **Facilidade de uso:**

- ✅ **Zero configuração** - usa banco existente
- ✅ **Erro-proof** - tratamento de erros simples  
- ✅ **Interface limpa** - perguntas diretas
- ✅ **Testado** - funcionamento verificado

## 🎓 LEARNING OUTCOMES

Após completar o exercício, os alunos terão:

### ✅ **Experiência prática com:**

- Ferramenta `BaseTool` para consultas SQL
- Sistema interativo básico com CrewAI
- Agente especializado em domínio específico
- Dados reais de um sistema existente

### ✅ **Compreensão dos conceitos:**

- Como conectar agentes a dados reais
- Análise básica de intenção do usuário
- Loop interativo simples mas funcional
- Integração SQLite + CrewAI

## 🚀 EXECUÇÃO PASSO A PASSO

### 1️⃣ **Verificações:**

```
✅ OpenAI API Key configurada
✅ Banco db/curso.db existe  
✅ Dependências instaladas (uv sync)
```

### 2️⃣ **Execução:**

```bash
uv run aula8/exercicio_simples_aula8.py
```

### 3️⃣ **Interação:**

```
💬 Digite pergunta → 🤖 Agente consulta dados → 📋 Resposta
```

### 4️⃣ **Finalização:**

```
Digite "sair" → 👋 Programa encerra
```

## 🔧 ESTRUTURA TÉCNICA (147 linhas)

```python
# Imports (8 linhas)
import os, sqlite3, pathlib, dotenv, crewai, langchain_openai

# Classe BaseTool (35 linhas)
class ConsultaSaude(BaseTool):
    # 3 tipos de consulta SQL simples
    
# Função main (104 linhas)  
def main():
    # Verificações, agente, loop interativo
```

## 🆚 DIFERENÇAS: Exercício Original vs Simples

| Aspecto | 🎓 Original | 🚀 Simples |
|---------|-------------|------------|
| **Linhas** | 400+ | 147 |
| **Dados** | Livros fictícios | Saúde REAIS |
| **Setup** | Cria banco temporário | Usa banco existente |
| **Consultas** | 5+ tipos complexos | 3 tipos básicos |
| **Tempo** | 30+ minutos | 15-20 minutos |
| **Complexidade** | Intermediário | Iniciante |

## ⚠️ SOLUÇÃO DE PROBLEMAS

### **Erro: "Banco não encontrado"**

```bash
# Verificar se existe
ls -la db/curso.db

# Se não existe, verificar migrações em db/
```

### **Erro: "OpenAI API Key não configurada"**

```bash
# Verificar .env
cat .env | grep OPENAI

# Configurar se necessário  
echo "OPENAI_API_KEY=sua_chave" >> .env
```

### **Erro: "Dependências"**

```bash
uv sync
```

## ✅ CRITÉRIO DE SUCESSO

Exercício completado quando conseguir:

1. ✅ Executar programa sem erros
2. ✅ Fazer as 3 perguntas sugeridas
3. ✅ Ver dados REAIS nos resultados  
4. ✅ Entender cada parte do código (147 linhas)
5. ✅ Sair com comando "sair"

## 🎉 CONCLUSÃO

Este exercício **reformulado** é:

- ✅ **Muito mais simples** - apenas 147 linhas
- ✅ **Usa dados REAIS** - sistema de saúde existente
- ✅ **Tempo adequado** - 15-20 minutos na aula
- ✅ **Conceitos essenciais** - todos os fundamentos da Aula 8
- ✅ **Zero configuração** - usa estrutura existente

**🎯 Perfeito para ser executado durante a aula!**

---

**⚡ Comando rápido**: `uv run aula8/exercicio_simples_aula8.py`

## 🎯 OBJETIVO

Aplicar **TODOS os conceitos da Aula 8** criando um sistema interativo simples usando CrewAI + SQLite, mas com dados de livros ao invés de saúde (mais simples e universal).

## ⏱️ TEMPO ESTIMADO: 20-30 minutos

## 🎓 CONCEITOS APLICADOS (da Aula 8)

- ✅ **Sistema interativo** - Loop de conversação com usuário
- ✅ **Ferramenta personalizada** - Classe `BaseTool` customizada
- ✅ **SQLite** - Banco de dados local (sem PostgreSQL)
- ✅ **Agente especializado** - Agent com backstory específico
- ✅ **Interface de linha de comando** - Menu e comandos especiais
- ✅ **Processamento de linguagem natural** - Análise de intenção do usuário

## 🚀 COMO EXECUTAR

```bash
# 1. Verificar que está no diretório do projeto
cd /caminho/para/curso_crewai

# 2. Verificar OpenAI API Key configurada
cat .env | grep OPENAI_API_KEY

# 3. Executar o exercício
uv run aula8/exercicio_pratico_aula8.py
```

## 📋 O QUE O EXERCÍCIO FAZ

### 🗄️ 1. Cria banco SQLite temporário

- Cria arquivo `biblioteca_exercicio.db`
- Popula com 10 livros de exemplo
- Mais simples que dados de saúde da Aula 8

### 🛠️ 2. Ferramenta personalizada

```python
class ConsultaLivrosTool(BaseTool):
    # Analisa intenção do usuário
    # Executa consultas apropriadas no SQLite
    # Formata resultados para o agente
```

### 🤖 3. Agente bibliotecário

```python
agente = Agent(
    role="Bibliotecário Especialista",
    backstory="Bibliotecário experiente...",
    tools=[ConsultaLivrosTool()]
)
```

### 💬 4. Sistema interativo

- Loop principal de conversação
- Comandos especiais (`sair`, `ajuda`)
- Respostas formatadas e amigáveis

## 🎮 COMO USAR (Exemplos)

### ✨ Perguntas sugeridas

```
💬 "Quais livros temos disponíveis?"
💬 "Mostre os livros por autor" 
💬 "Quais gêneros temos na biblioteca?"
💬 "Livros disponíveis para empréstimo"
💬 "Estatísticas da biblioteca"
```

### ⌨️ Comandos especiais

```
sair   - Encerra o programa
ajuda  - Mostra menu de opções
```

## 📊 DADOS DO EXERCÍCIO

**10 livros de exemplo:**

- O Alquimista (Paulo Coelho)
- Dom Casmurro (Machado de Assis)
- 1984 (George Orwell) - EMPRESTADO
- Harry Potter (J.K. Rowling)
- O Código Da Vinci (Dan Brown)
- Cem Anos de Solidão (Gabriel García Márquez)
- O Pequeno Príncipe (Saint-Exupéry)
- A Revolução dos Bichos (George Orwell) - EMPRESTADO
- O Senhor dos Anéis (J.R.R. Tolkien)
- Orgulho e Preconceito (Jane Austen)

## 🔍 TIPOS DE CONSULTA SUPORTADOS

### 📖 **Por conteúdo:**

- "livros" → Lista todos os livros
- "autor" → Agrupa por autores
- "gênero" → Agrupa por gêneros

### 📊 **Por status:**

- "disponível" → Mostra disponibilidade
- "estatística" → Números gerais

### 🔍 **Geral:**

- Qualquer outra pergunta → Lista todos os livros

## 🎯 FLUXO DO EXERCÍCIO

### 1️⃣ **Inicialização:**

```
✅ Verificar API Key
✅ Criar banco SQLite
✅ Popular com dados
✅ Criar ferramenta personalizada
✅ Criar agente bibliotecário
```

### 2️⃣ **Loop interativo:**

```
👤 Usuário faz pergunta
🤖 Sistema analisa intenção
🔍 Ferramenta consulta SQLite
📊 Dados são formatados
💬 Agente responde amigavelmente
🔄 Aguarda próxima pergunta
```

### 3️⃣ **Finalização:**

```
✅ Usuário digita "sair"
🧹 Banco temporário é removido
👋 Programa encerra
```

## 🔧 ESTRUTURA TÉCNICA

### 📁 Arquivos criados

```
exercicio_pratico_aula8.py    # Código principal
biblioteca_exercicio.db       # Banco temporário (removido ao final)
```

### 🏗️ Classes principais

```python
ConsultaLivrosTool()         # Ferramenta SQLite
├── _listar_todos_livros()   # Lista geral
├── _buscar_por_autor()      # Agrupa por autor
├── _buscar_por_genero()     # Agrupa por gênero
├── _buscar_disponibilidade() # Status empréstimo
└── _buscar_estatisticas()   # Números gerais

criar_agente_bibliotecario() # Cria agente especializado
sistema_interativo()         # Loop principal
main()                       # Orquestra tudo
```

## 🎓 LEARNING OUTCOMES

Ao completar este exercício, você terá praticado:

### ✅ **Conceitos técnicos:**

- Criação de ferramentas `BaseTool` personalizadas
- Integração CrewAI + SQLite
- Análise de linguagem natural básica
- Formatação de saídas para agentes

### ✅ **Conceitos de UX:**

- Interface conversacional amigável
- Comandos especiais intuitivos
- Feedback claro ao usuário
- Menu de ajuda contextual

### ✅ **Conceitos arquiteturais:**

- Sistema interativo com estado
- Separação de responsabilidades
- Gestão de recursos temporários
- Tratamento de erros gracioso

## 🆚 DIFERENÇAS da Aula 8 Original

| Aspecto | 🎓 Aula 8 Original | 🎯 Este Exercício |
|---------|-------------------|-------------------|
| **Dados** | Saúde (complexos) | Livros (simples) |
| **Tabelas** | 4+ tabelas | 1 tabela |
| **Consultas** | Queries complexas | Queries básicas |
| **Setup** | Banco externo | Criação automática |
| **Tempo** | 45-60 min | 20-30 min |
| **Foco** | Sistema completo | Conceitos-chave |

## 🔄 POSSÍVEIS EXTENSÕES

Se terminar cedo, tente:

### 🟢 **Nível Iniciante:**

```python
# Adicionar mais perguntas suportadas
if 'ano' in consulta_lower:
    return self._buscar_por_ano()
```

### 🟡 **Nível Intermediário:**

```python
# Adicionar comando para emprestar livro
if 'emprestar' in consulta_lower:
    return self._emprestar_livro()
```

### 🔴 **Nível Avançado:**

```python
# Adicionar segundo agente (recomendações)
agente_recomendador = Agent(
    role="Especialista em Recomendações",
    tools=[ConsultaLivrosTool()]
)
```

## ❌ SOLUÇÃO DE PROBLEMAS

### **Erro: "OpenAI API Key não configurada"**

```bash
# Verificar arquivo .env
cat .env

# Configurar se necessário
echo "OPENAI_API_KEY=sua_chave_aqui" >> .env
```

### **Erro: "Banco de dados não encontrado"**

- O exercício cria o banco automaticamente
- Verifique se tem permissão de escrita no diretório

### **Erro: "Dependências não instaladas"**

```bash
uv sync
```

### **Programa trava na primeira pergunta**

- Verifique conexão com internet
- Teste a API Key: `uv run teste_api.py`

## 📚 REFERÊNCIAS

- **Aula 8 original**: `aula8/main.py`
- **Documentação CrewAI Tools**: <https://docs.crewai.com/tools>
- **SQLite Python**: <https://docs.python.org/3/library/sqlite3.html>
- **OpenAI API**: <https://platform.openai.com/docs>

## ✅ CRITÉRIO DE SUCESSO

Você completou com sucesso quando conseguir:

1. ✅ Executar o programa sem erros
2. ✅ Fazer perguntas e receber respostas do agente
3. ✅ Testar diferentes tipos de consulta
4. ✅ Usar comandos especiais (`ajuda`, `sair`)
5. ✅ Entender como cada parte funciona

## 🎉 CONCLUSÃO

Este exercício é uma versão "capada" da Aula 8 que:

- ✅ **Mantém todos os conceitos essenciais**
- ✅ **Simplifica os dados e consultas**  
- ✅ **É executável em 20-30 minutos**
- ✅ **Funciona independentemente**
- ✅ **Ensina os fundamentos**

**🚀 Próximo passo**: Após dominar este exercício, volte para o `aula8/main.py` original e veja como os mesmos conceitos são aplicados em um sistema mais complexo!

---

**⚡ Comando rápido**: `uv run aula8/exercicio_pratico_aula8.py`
