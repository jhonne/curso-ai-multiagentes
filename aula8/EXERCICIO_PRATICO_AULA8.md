# Exercício Prático Aula 8 - Instruções

Exercício simples para aplicar todos os conceitos da Aula 8 criando um sistema interativo usando dados reais do banco SQLite.

## Objetivo

Aplicar **todos os conceitos da Aula 8** criando um sistema super simples (< 150 linhas) usando dados reais do banco SQLite existente do curso.

## Tempo Estimado

15-20 minutos

## Conceitos Aplicados

Este exercício aplica os seguintes conceitos da Aula 8:

- **Sistema interativo**: Loop básico de conversação
- **Ferramenta personalizada**: Classe `BaseTool` customizada
- **SQLite com dados reais**: Usa o banco curso.db existente
- **Agente especializado**: Agent com backstory específico

## Como Executar

```bash
# 1. Verificar que está no diretório do projeto
cd /caminho/para/curso_crewai

# 2. Verificar OpenAI API Key configurada
cat .env | grep OPENAI_API_KEY

# 3. Executar o exercício simples (< 150 linhas)
uv run aula8/exercicio_simples_aula8.py
```

## O Que o Exercício Faz

### Usa Dados Reais de Saúde

- Conecta ao banco `db/curso.db` existente no projeto
- Consulta estabelecimentos reais (hospitais, UPAs, postos)
- Mostra queixas médicas mais frequentes
- Exibe estatísticas reais do sistema de saúde

### Ferramenta Super Simples

```python
class ConsultaSaude(BaseTool):
    # 3 tipos de consulta básicas:
    # - Estabelecimentos
    # - Queixas frequentes  
    # - Estatísticas gerais
```

### Agente Especialista

```python
agente = Agent(
    role="Assistente de Saúde",
    backstory="Especialista em dados de saúde pública",
    tools=[ConsultaSaude()]
)
```

### Sistema Interativo Básico

- Loop simples de perguntas/respostas
- Comando `sair` para encerrar

## Como Usar

### Exemplos de Perguntas

```text
"Quais estabelecimentos temos?"
"Mostre as queixas mais frequentes"
"Estatísticas gerais"
```

### Comandos

```text
sair   - Encerra o programa
```

## Dados Reais do Exercício

**Dados do sistema de saúde real:**

- 2.847+ estabelecimentos de saúde
- 156+ tipos de queixas médicas
- 125.394+ registros de atendimento
- Dados de hospitais, UPAs, postos de saúde
- Informações de bairros e endereços

## Tipos de Consulta

### Estabelecimentos

- Lista hospitais, UPAs, postos de saúde
- Mostra nome e bairro
- Dados REAIS do sistema

### Queixas Médicas

- Queixas mais frequentes
- Número de casos por tipo
- Baseado em dados reais de atendimento

### Estatísticas

- Total de estabelecimentos
- Tipos de queixas cadastradas
- Visão geral do sistema

## Vantagens do Exercício Reformulado

### Super Simples

- **Apenas 147 linhas** (vs 400+ anteriores)
- **3 tipos básicos** de consulta
- **Conceitos essenciais** da Aula 8
- **Tempo adequado** para aula (15-20 min)

### Dados Reais

- **Banco existente**: usa db/curso.db do projeto
- **Sem setup adicional**: não cria banco temporário
- **Dados significativos**: sistema de saúde real
- **Mais interessante**: estabelecimentos e queixas reais

### Facilidade de Uso

- **Zero configuração**: usa banco existente
- **Erro-proof**: tratamento de erros simples
- **Interface limpa**: perguntas diretas
- **Testado**: funcionamento verificado

## Resultados de Aprendizagem

Após completar o exercício, os alunos terão:

### Experiência Prática Com

- Ferramenta `BaseTool` para consultas SQL
- Sistema interativo básico com CrewAI
- Agente especializado em domínio específico
- Dados reais de um sistema existente

### Compreensão dos Conceitos

- Como conectar agentes a dados reais
- Análise básica de intenção do usuário
- Loop interativo simples mas funcional
- Integração SQLite + CrewAI

## Execução Passo a Passo

### 1. Verificações

```text
OpenAI API Key configurada
Banco db/curso.db existe
Dependências instaladas (uv sync)
```

### 2. Execução

```bash
uv run aula8/exercicio_simples_aula8.py
```

### 3. Interação

```text
Digite pergunta → Agente consulta dados → Resposta
```

### 4. Finalização

```text
Digite "sair" → Programa encerra
```

## Estrutura Técnica

Total: 147 linhas

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

## Diferenças: Exercício Original vs Simples

| Aspecto | Original | Simples |
|---------|----------|----------|
| **Linhas** | 400+ | 147 |
| **Dados** | Livros fictícios | Saúde reais |
| **Setup** | Cria banco temporário | Usa banco existente |
| **Consultas** | 5+ tipos complexos | 3 tipos básicos |
| **Tempo** | 30+ minutos | 15-20 minutos |
| **Complexidade** | Intermediário | Iniciante |

## Solução de Problemas

### Erro: "Banco não encontrado"

```bash
# Verificar se existe
ls -la db/curso.db

# Se não existe, verificar migrações em db/
```

### Erro: "OpenAI API Key não configurada"

```bash
# Verificar .env
cat .env | grep OPENAI

# Configurar se necessário
echo "OPENAI_API_KEY=sua_chave" >> .env
```

### Erro: "Dependências"

```bash
uv sync
```

## Critério de Sucesso

Exercício completado quando conseguir:

1. Executar programa sem erros
2. Fazer as 3 perguntas sugeridas
3. Ver dados reais nos resultados
4. Entender cada parte do código (147 linhas)
5. Sair com comando "sair"

## Conclusão

Este exercício reformulado é:

- **Muito mais simples**: apenas 147 linhas
- **Usa dados reais**: sistema de saúde existente
- **Tempo adequado**: 15-20 minutos na aula
- **Conceitos essenciais**: todos os fundamentos da Aula 8
- **Zero configuração**: usa estrutura existente

**Perfeito para ser executado durante a aula!**

## Referências

- Comando de execução rápida: `uv run aula8/exercicio_simples_aula8.py`
- Banco de dados: `db/curso.db`
- Documentação do projeto: `README.md`
