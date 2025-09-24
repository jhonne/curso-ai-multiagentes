📚 GUIA DIDÁTICO: Agente CrewAI + PostgreSQL
==============================================

## 🎯 OBJETIVO EDUCACIONAL

Este exercício demonstra como integrar um agente CrewAI com banco de dados PostgreSQL,
mostrando o fluxo completo desde a criação da ferramenta até a execução prática.

## 📋 ESTRUTURA DIDÁTICA DO CÓDIGO

### MÓDULO 1: Imports e Configuração

```python
# Configuração inicial, imports necessários
# Carregamento de variáveis de ambiente
```

### MÓDULO 2: Ferramenta CrewAI (⭐ MAIS IMPORTANTE)

```python
class BuscadorEstabelecimentosTool(BaseTool):
    # Esta é a PONTE entre o agente e o PostgreSQL
    # Herda de BaseTool para integração automática com CrewAI
```

**PONTOS-CHAVE PARA EXPLICAR:**

- `BaseTool`: Classe base do CrewAI para ferramentas
- `args_schema`: Define quais parâmetros o agente pode usar
- `_run()`: Método onde acontece a consulta real ao PostgreSQL

### MÓDULO 3: Classe Auxiliar

```python
class BuscadorEstabelecimentos:
    # Apenas para demonstração de consultas diretas
    # NÃO é usada pelo agente CrewAI
```

### MÓDULO 4: Criação do Agente (🤖 PEÇA CENTRAL)

```python
def criar_agente_postgres():
    # 1. Configurar LLM
    # 2. Criar ferramenta
    # 3. Conectar ferramenta ao agente: tools=[ferramenta]
    # 4. Definir role, goal, backstory
```

**PONTO CRUCIAL:** `tools=[ferramenta_busca]` - É aqui que a ferramenta é conectada ao agente!

### MÓDULO 5: Execução Principal

```python
def executar_exercicio():
    # Fluxo didático completo:
    # 1. Testar conexão
    # 2. Preparar dados
    # 3. Criar agente
    # 4. Definir tarefa
    # 5. Executar e demonstrar
```

## 🔍 FLUXO DE EXECUÇÃO EXPLICADO

### PASSO 1: Preparação

1. Testa conexão PostgreSQL
2. Insere dados de exemplo
3. Confirma que tudo está funcionando

### PASSO 2: Criação do Sistema

1. Cria ferramenta `BuscadorEstabelecimentosTool`
2. Cria agente CrewAI com ferramenta conectada
3. Define tarefa que instrui o agente

### PASSO 3: Execução Real

1. Agente recebe tarefa
2. Agente identifica que precisa usar sua ferramenta
3. Agente chama automaticamente `buscar_estabelecimentos_postgres`
4. Ferramenta executa consulta SQL real no PostgreSQL
5. Ferramenta retorna resultados formatados
6. Agente organiza e apresenta relatório final

## 🎓 CONCEITOS DIDÁTICOS IMPORTANTES

### 1. Diferença entre Consulta Direta vs Agente

- **Consulta Direta**: `buscador.buscar_estabelecimentos()` - código Python normal
- **Agente CrewAI**: Agente decide quando e como usar sua ferramenta automaticamente

### 2. Como o Agente "Sabe" Usar a Ferramenta

- `description`: Descreve o que a ferramenta faz
- `args_schema`: Define quais parâmetros aceita
- Agente usa LLM para entender quando e como chamar a ferramenta

### 3. Vantagens da Abordagem com Agente

- **Inteligência**: Agente decide qual ferramenta usar baseado no contexto
- **Flexibilidade**: Pode combinar múltiplas ferramentas
- **Linguagem Natural**: Tarefa pode ser descrita em português
- **Autonomia**: Agente executa múltiplas consultas conforme necessário

## 🔧 PONTOS DE ATENÇÃO PARA SALA DE AULA

### 1. Configuração da Ferramenta

```python
class MinhaFerramenta(BaseTool):
    name: str = "nome_da_ferramenta"           # Como o agente vai chamar
    description: str = "O que a ferramenta faz" # Como o agente entende o uso
    args_schema: Type[BaseModel] = MeuSchema    # Quais parâmetros aceita
    
    def _run(self, parametros) -> str:          # O que realmente executa
        # Aqui acontece a lógica real
```

### 2. Conexão ao Agente

```python
agente = Agent(
    tools=[minha_ferramenta],  # ← CRUCIAL: Lista de ferramentas disponíveis
    # ... outras configurações
)
```

### 3. Tarefa que Instrui o Uso

```python
Task(
    description="Use sua ferramenta X para fazer Y",  # Instrução clara
    agent=agente,                                     # Agente que tem a ferramenta
)
```

## 🎯 EXERCÍCIOS PRÁTICOS SUGERIDOS

### Nível Iniciante

1. Modificar os filtros de busca (adicionar mais campos)
2. Criar consultas para tipos específicos de estabelecimentos
3. Alterar o formato de saída dos resultados

### Nível Intermediário

1. Criar segunda ferramenta (ex: inserir novos estabelecimentos)
2. Agente com múltiplas ferramentas
3. Validação de dados antes de inserir

### Nível Avançado

1. Sistema com múltiplos agentes especializados
2. Agente que analisa padrões nos dados
3. Integração com APIs externas

## 📊 LOGS DIDÁTICOS IMPORTANTES

Durante a execução, observe estes logs que mostram o agente funcionando:

```
🔧 Used buscar_estabelecimentos_postgres (1)
🔧 Used buscar_estabelecimentos_postgres (2)
🔧 Used buscar_estabelecimentos_postgres (3)
```

Isso confirma que o agente:

1. Entendeu a tarefa
2. Identificou que precisava usar sua ferramenta
3. Executou múltiplas consultas automaticamente
4. Organizou os resultados em um relatório

## 🚀 COMANDOS PARA DEMONSTRAÇÃO

```bash
# Executar o exercício completo
uv run aula7/exercicio_agente_postgres.py

# Verificar se PostgreSQL está rodando
sudo systemctl status postgresql

# Testar conexão direta
uv run python -c "import psycopg2; print('PostgreSQL OK')"
```

## 💡 DICAS DE APRESENTAÇÃO

1. **Mostrar primeiro** a consulta direta (Módulo 3)
2. **Explicar depois** como transformar em ferramenta CrewAI (Módulo 2)
3. **Demonstrar** a conexão da ferramenta ao agente (Módulo 4)
4. **Executar** e mostrar os logs em tempo real
5. **Comparar** resultado direto vs resultado do agente

## ❓ PERGUNTAS FREQUENTES DOS ALUNOS

**P: Por que não usar consulta direta ao PostgreSQL?**
R: Agente CrewAI permite linguagem natural, múltiplas ferramentas, e decisões inteligentes.

**P: Como o agente sabe quando usar a ferramenta?**
R: Pela description e contexto da tarefa. O LLM analisa e decide.

**P: Posso ter múltiplas ferramentas?**
R: Sim! `tools=[ferramenta1, ferramenta2, ferramenta3]`

**P: E se a ferramenta der erro?**
R: O agente recebe a mensagem de erro e pode tentar alternativas.

## 🎯 OBJETIVOS DE APRENDIZAGEM ALCANÇADOS

Ao final desta aula, os alunos devem conseguir:

✅ Criar ferramentas CrewAI personalizadas
✅ Conectar ferramentas a agentes
✅ Integrar agentes com bancos de dados
✅ Entender o fluxo de execução automática
✅ Distinguir consulta direta vs agente inteligente
✅ Configurar tarefas que usam ferramentas específicas

---

**📚 Arquivo de apoio ao exercício `exercicio_agente_postgres.py`**
