# Exercício Aula 7: Agente CrewAI + PostgreSQL

## 📋 Exercícios Disponíveis

### 1. **Exercício Simples** (Recomendado para começar)
```bash
uv run aula7/exercicio_simples_postgres.py
```
- ✅ **Não precisa de PostgreSQL** (usa dados simulados)
- ✅ Demonstra integração CrewAI com dados estruturados
- ✅ Funciona imediatamente após configurar OpenAI
- 🎯 **Ideal para entender conceitos básicos**

### 2. **Exercício Completo** (PostgreSQL Real)
```bash
uv run aula7/exercicio_agente_postgres.py
```
- 🔧 **Requer PostgreSQL configurado**
- 🗄️ Conecta ao banco real
- 📊 Busca, insere e consulta dados
- 🎯 **Para quem quer experiência completa**

## 🚀 Início Rápido (Exercício Simples)

1. **Configurar OpenAI** (apenas)
```bash
# No arquivo .env
OPENAI_API_KEY=sua_chave_aqui
```

2. **Executar**
```bash
uv run aula7/exercicio_simples_postgres.py
```

3. **Ver resultado**: Agente analisa dados médicos simulados

## 🔧 Configuração Completa (PostgreSQL Real)

### Pre-requisitos
```bash
# Instalar dependência
uv add psycopg2-binary

# Docker PostgreSQL (recomendado)
docker run --name postgres-crewai \
  -e POSTGRES_PASSWORD=arpus \
  -e POSTGRES_DB=curso \
  -p 5432:5432 \
  -d postgres:16
```

### Variáveis de Ambiente
```env
OPENAI_API_KEY=sua_chave_aqui
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=curso
POSTGRES_USER=postgres
POSTGRES_PASSWORD=arpus
```

### Executar Exercício Completo
```bash
uv run aula7/exercicio_agente_postgres.py
```

## 📚 O Que Você Vai Aprender

### Conceitos Fundamentais
1. **Integração CrewAI + Banco de Dados**
2. **Processamento de dados estruturados**
3. **Agentes especializados em consulta**
4. **Tratamento de erros e conexões**

### Estrutura do Código
```python
# Classe para gerenciar dados
class BuscadorEstabelecimentos:
    def buscar_estabelecimentos(self, tipo, municipio)
    
# Agente especializado
agente = Agent(
    role="Consultor de Estabelecimentos Médicos",
    goal="Analisar dados médicos",
    backstory="Especialista em saúde..."
)

# Execução
crew = Crew(agents=[agente], tasks=[tarefa])
resultado = crew.kickoff()
```

## 📊 Exemplo de Saída

```
🏥 EXERCÍCIO CREWAI + POSTGRESQL (SIMPLES)
=============================================

🤖 Criando agente...
🚀 Executando análise...

📋 RESULTADO DA ANÁLISE:
**Relatório de Estabelecimentos Médicos**

**1. Lista por tipo de estabelecimento:**
- **Hospitais:**
  - Hospital São Paulo - São Paulo - (11) 1111-1111

- **UPAs:** 
  - UPA Central - São Paulo - (11) 2222-2222

- **Clínicas:**
  - Clínica Santa Maria - Santo André - (11) 3333-3333

**3. Recomendações de uso:**
- **Hospital:** Para emergências e internações
- **UPA:** Para urgências sem internação  
- **Clínica:** Para consultas e exames de rotina

✅ EXERCÍCIO CONCLUÍDO!
```

## 🎯 Próximos Passos

1. **Comece pelo exercício simples** para entender os conceitos
2. **Configure PostgreSQL** para o exercício completo
3. **Explore `aula7/main.py`** para funcionalidades avançadas
4. **Experimente modificar** os prompts do agente

## 🔧 Troubleshooting

### Erro OpenAI API Key
```bash
echo "OPENAI_API_KEY=sua_chave" >> .env
```

### Erro PostgreSQL (Exercício Completo)
```bash
# Verificar se container está rodando
docker ps

# Recriar se necessário
docker rm -f postgres-crewai && \
docker run --name postgres-crewai \
  -e POSTGRES_PASSWORD=arpus \
  -e POSTGRES_DB=curso \
  -p 5432:5432 \
  -d postgres:16
```

### Dependência não encontrada
```bash
uv add psycopg2-binary python-dotenv
```

---

**💡 Dica**: Comece sempre pelo **exercício simples** para entender os conceitos, depois avance para o PostgreSQL real quando se sentir confortável!