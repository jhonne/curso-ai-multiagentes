# 🎯 ONDE EXATAMENTE O AGENTE SE CONECTA E CONSOME DADOS DO BANCO

## 📍 LOCALIZAÇÃO PRECISA NO CÓDIGO

O agente **NÃO se conecta diretamente** ao banco PostgreSQL. Ele usa sua **ferramenta integrada** para fazer isso. Vou mostrar exatamente onde cada parte acontece:

## 🔗 PONTO 1: CONEXÃO DA FERRAMENTA AO AGENTE

### **📍 Localização: Linhas 257-258**

```python
agente_busca = Agent(
    role="Especialista em Estabelecimentos Médicos",
    # ... outras configurações ...
    tools=[ferramenta_busca],  # ← AQUI: Agente RECEBE a ferramenta
    llm=llm
)
```

**✅ O que acontece aqui:**

- A ferramenta `BuscadorEstabelecimentosTool` é **conectada** ao agente
- Agente agora **pode** usar a ferramenta quando necessário
- Esta linha dá ao agente a **"habilidade"** de acessar PostgreSQL

---

## 🔗 PONTO 2: CONEXÃO REAL COM POSTGRESQL (O MAIS IMPORTANTE!)

### **📍 Localização: Linhas 70-82 (Método `_run` da ferramenta)**

```python
def _run(self, tipo: str, municipio: str, limite: int = 5) -> str:
    try:
        # ┌─────────────────────────────────────────────────────────┐
        # │  🔥 AQUI É ONDE A CONEXÃO REAL ACONTECE!               │
        # └─────────────────────────────────────────────────────────┘
        
        # 1. CONFIGURAÇÃO da conexão
        db_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': os.getenv('POSTGRES_PORT', '5432'),
            'database': os.getenv('POSTGRES_DB', 'curso'),
            'user': os.getenv('POSTGRES_USER', 'postgres'),
            'password': os.getenv('POSTGRES_PASSWORD', 'arpus')
        }
        
        # 2. CONECTAR ao PostgreSQL (MOMENTO EXATO DA CONEXÃO!)
        conn = psycopg2.connect(**db_config)  # ← CONEXÃO REAL!
        cursor = conn.cursor(cursor_factory=RealDictCursor)
```

**✅ O que acontece aqui:**

- **Momento exato** da conexão com PostgreSQL
- Usa credenciais do arquivo `.env`
- Cria cursor para executar comandos SQL

---

## 🔗 PONTO 3: CONSUMO DOS DADOS (QUERY SQL)

### **📍 Localização: Linhas 84-98 (Dentro do método `_run`)**

```python
        # ┌─────────────────────────────────────────────────────────┐
        # │  💾 AQUI É ONDE OS DADOS SÃO CONSUMIDOS!               │
        # └─────────────────────────────────────────────────────────┘
        
        # 3. MONTAR query SQL dinâmica baseada nos parâmetros do agente
        query = """SELECT nome, tipo, municipio, telefone, endereco 
                   FROM estabelecimentos WHERE 1=1"""
        params = []
        
        # 4. ADICIONAR filtros conforme o que o agente pediu
        if tipo.lower() != 'todos':
            query += " AND LOWER(tipo) LIKE %s"
            params.append(f"%{tipo.lower()}%")
        
        if municipio.lower() != 'todos':
            query += " AND LOWER(municipio) LIKE %s"
            params.append(f"%{municipio.lower()}%")
        
        query += f" ORDER BY nome LIMIT {limite}"
        
        # 5. EXECUTAR a query (MOMENTO EXATO DO CONSUMO!)
        cursor.execute(query, params)  # ← EXECUTA SQL!
        resultados = cursor.fetchall()  # ← CONSOME DADOS!
```

**✅ O que acontece aqui:**

- **Monta SQL dinâmico** baseado nos parâmetros do agente
- **Executa a query** no PostgreSQL
- **Consome os dados** retornados pelo banco

---

## 🔗 PONTO 4: FORMATAÇÃO E RETORNO DOS DADOS

### **📍 Localização: Linhas 100-115**

```python
        # ┌─────────────────────────────────────────────────────────┐
        # │  📊 AQUI OS DADOS SÃO FORMATADOS PARA O AGENTE!        │
        # └─────────────────────────────────────────────────────────┘
        
        # 6. VERIFICAR se encontrou dados
        if not resultados:
            return f"❌ Nenhum resultado: tipo='{tipo}', município='{municipio}'"
        
        # 7. FORMATAR resultados para o agente entender
        output = f"Encontrados {len(resultados)} estabelecimento(s):\n"
        for i, row in enumerate(resultados, 1):
            output += f"\n{i}. {row['nome']}"
            output += f"\n   Tipo: {row['tipo']}"
            output += f"\n   Município: {row['municipio']}"
            output += f"\n   Telefone: {row['telefone']}"
            output += f"\n   Endereço: {row['endereco']}"
        
        # 8. FECHAR conexão
        conn.close()
        
        # 9. RETORNAR dados formatados para o agente
        return output
```

**✅ O que acontece aqui:**

- **Dados do PostgreSQL** são formatados em texto estruturado
- **Conexão é fechada** adequadamente
- **Resultado é retornado** para o agente usar

---

## 🎯 FLUXO COMPLETO DE CONEXÃO E CONSUMO

### **📊 Sequência Temporal:**

```
1. [AGENTE] Recebe tarefa: "buscar hospitais em São Paulo"
          ↓
2. [AGENTE] Decide: "preciso usar minha ferramenta PostgreSQL"
          ↓  
3. [AGENTE] Chama: buscar_estabelecimentos_postgres(tipo="hospital", municipio="São Paulo")
          ↓
4. [FERRAMENTA] Executa método _run() com parâmetros do agente
          ↓
5. [FERRAMENTA] CONECTA: conn = psycopg2.connect(**db_config)  ← CONEXÃO!
          ↓
6. [FERRAMENTA] MONTA SQL: "SELECT * FROM estabelecimentos WHERE tipo LIKE '%hospital%'"
          ↓
7. [FERRAMENTA] EXECUTA: cursor.execute(query, params)  ← CONSUMO!
          ↓
8. [FERRAMENTA] RECEBE: resultados = cursor.fetchall()  ← DADOS!
          ↓
9. [FERRAMENTA] FORMATA: dados em texto estruturado
          ↓
10. [FERRAMENTA] RETORNA: texto formatado para o agente
          ↓
11. [AGENTE] RECEBE: dados da ferramenta e organiza em relatório final
```

---

## 💡 EXEMPLO PRÁTICO REAL

### **Quando você executa:**

```bash
uv run aula7/exercicio_agente_postgres.py
```

### **Isso acontece internamente:**

#### **🔸 MOMENTO 1: Agente decide usar ferramenta**

```python
# O agente "pensa": "Preciso buscar hospitais, vou usar minha ferramenta"
# Agente chama automaticamente:
ferramenta.buscar_estabelecimentos_postgres(
    tipo="hospital", 
    municipio="São Paulo", 
    limite=5
)
```

#### **🔸 MOMENTO 2: Ferramenta conecta no banco (LINHA 79)**

```python
# AQUI É A CONEXÃO REAL!
conn = psycopg2.connect(
    host='localhost',
    port='5432', 
    database='curso',
    user='postgres',
    password='arpus'
)
```

#### **🔸 MOMENTO 3: Ferramenta consome dados (LINHA 97-98)**

```python
# SQL gerado dinamicamente:
query = "SELECT nome, tipo, municipio, telefone, endereco FROM estabelecimentos WHERE 1=1 AND LOWER(tipo) LIKE '%hospital%' AND LOWER(municipio) LIKE '%são paulo%' ORDER BY nome LIMIT 5"

# AQUI É O CONSUMO REAL!
cursor.execute(query, params)
resultados = cursor.fetchall()  # ← DADOS DO POSTGRESQL!
```

#### **🔸 MOMENTO 4: Dados retornam para o agente**

```python
# Ferramenta retorna para o agente:
return """Encontrados 4 estabelecimento(s):

1. Hospital São Paulo
   Tipo: hospital
   Município: São Paulo
   Telefone: (11) 9999-9999"""
```

---

## 🎯 RESUMO DOS PONTOS CRÍTICOS

### **🔍 ONDE:** Linha 257-258

**O QUE:** Agente recebe acesso à ferramenta

```python
tools=[ferramenta_busca]  # ← Agente ganha "habilidade PostgreSQL"
```

### **🔍 ONDE:** Linha 79  

**O QUE:** Conexão real com PostgreSQL

```python
conn = psycopg2.connect(**db_config)  # ← CONEXÃO FÍSICA!
```

### **🔍 ONDE:** Linhas 97-98

**O QUE:** Execução e consumo de dados

```python
cursor.execute(query, params)      # ← EXECUTA SQL
resultados = cursor.fetchall()     # ← CONSOME DADOS
```

### **🔍 ONDE:** Linhas 104-113

**O QUE:** Formatação para o agente

```python
output = f"Encontrados {len(resultados)} estabelecimento(s):\n"
# ← FORMATA DADOS PARA O AGENTE ENTENDER
```

---

## ⚡ PONTO CRUCIAL DE ENTENDIMENTO

**❌ O AGENTE NÃO:**

- Se conecta diretamente no PostgreSQL
- Sabe SQL
- Conhece detalhes do banco de dados

**✅ O AGENTE APENAS:**

- Usa sua ferramenta quando precisa de dados
- Passa parâmetros em linguagem natural
- Recebe dados já formatados da ferramenta

**🛠️ A FERRAMENTA FAZ TUDO:**

- Conecta no PostgreSQL (linha 79)
- Monta SQL dinâmico (linhas 84-95)  
- Executa queries (linha 97)
- Consome dados (linha 98)
- Formata resultados (linhas 104-113)
- Retorna para o agente (linha 116)

**🎯 EM RESUMO:** O agente usa a ferramenta como uma "API interna" - ele pede dados em linguagem natural, e a ferramenta faz toda a parte técnica de conectar, consultar e formatar os dados do PostgreSQL!
