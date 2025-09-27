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
