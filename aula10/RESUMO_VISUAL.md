# 🎓 Aula 10 - Resumo Visual: SQLite vs Embeddings

## 📊 Comparação Visual Rápida

```text
┌─────────────────────────────────────────────────────────────────────┐
│                    SQL LIKE vs EMBEDDINGS                           │
└─────────────────────────────────────────────────────────────────────┘

CENÁRIO: Buscar sintomas relacionados a "dor de cabeça"

┌─────────────────────────────────┬─────────────────────────────────┐
│     🗄️  SQL TRADICIONAL         │    🧠 BUSCA SEMÂNTICA          │
├─────────────────────────────────┼─────────────────────────────────┤
│                                 │                                 │
│ SELECT * FROM ia_sintoma        │ query_embedding =               │
│ WHERE nome LIKE '%dor%cabeça%'  │   criar_embedding(query)        │
│                                 │                                 │
│ RESULTADOS: 2 encontrados       │ buscar_similares(embedding)     │
│                                 │                                 │
│ ✅ "Dor de cabeça forte"        │ RESULTADOS: 5 encontrados       │
│ ✅ "Dor de cabeça leve"         │                                 │
│                                 │ ✅ Cefaleia (95%)               │
│ ❌ Cefaleia não encontrada      │ ✅ Enxaqueca (89%)              │
│ ❌ Enxaqueca não encontrada     │ ✅ Dor craniana (87%)           │
│                                 │ ✅ Dor de cabeça forte (92%)    │
│                                 │ ✅ Migrânea (85%)               │
│                                 │                                 │
│ Performance: ⚡ 0.5ms           │ Performance: 🔄 5ms (com cache) │
│ Precisão: 📊 40%                │ Precisão: 🎯 95%                │
│ Custo: 💰 $0                    │ Custo: 💰 $0 (após setup)       │
└─────────────────────────────────┴─────────────────────────────────┘
```

## 🔬 Fluxo de Processamento

### SQL Tradicional

```text
┌──────────┐
│  Query   │ "dor de cabeça"
└────┬─────┘
     │
     ▼
┌────────────────────┐
│  Pattern Match     │ '%dor%cabeça%'
└────┬───────────────┘
     │
     ▼
┌────────────────────┐
│  Scan Table        │ Percorre registros
│  com índices       │ Busca substring
└────┬───────────────┘
     │
     ▼
┌────────────────────┐
│  Resultados        │
│  • Match exato     │ ✅ "Dor de cabeça forte"
│  • Case-insensitive│ ✅ "Dor de cabeça leve"
│  • Literal apenas  │
└────────────────────┘
     │
     ▼
    ⚡ < 1ms
```

### Busca Semântica com Embeddings

```text
┌──────────┐
│  Query   │ "dor de cabeça"
└────┬─────┘
     │
     ▼
┌────────────────────┐
│  OpenAI API        │ text-embedding-3-small
│  (primeira vez)    │
└────┬───────────────┘
     │
     ▼
┌────────────────────┐
│  Vetor 1536D       │ [0.12, -0.45, 0.78, ...]
│  Representação     │ (captura significado)
│  semântica         │
└────┬───────────────┘
     │
     ▼
┌────────────────────┐
│  Comparar com      │ Para cada sintoma:
│  todos embeddings  │ calcular similaridade
└────┬───────────────┘
     │
     ▼
┌────────────────────┐
│  Ordenar por       │ Top-K mais similares
│  similaridade      │
└────┬───────────────┘
     │
     ▼
┌────────────────────┐
│  Resultados        │
│  • Por significado │ ✅ Cefaleia (95%)
│  • Com sinônimos   │ ✅ Enxaqueca (89%)
│  • Contexto        │ ✅ Dor craniana (87%)
└────────────────────┘
     │
     ▼
    🔄 ~5ms (cache)
   📡 ~200ms (primeira vez)
```

## 🎯 Matriz de Decisão Visual

```text
                    SIMPLES ────────────────────── COMPLEXO
                       │                                │
                       │                                │
SQL LIKE ──────────────┼────────X                       │
  • Busca exata        │        │                       │
  • Dados estruturados │        │                       │
  • Performance crítica│        │                       │
                       │        │                       │
                       │        │                       │
EMBEDDINGS ────────────┼────────┼────────────────X      │
  • Linguagem natural  │        │                │      │
  • Sinônimos          │        │                │      │
  • Contexto semântico │        │                │      │
                       │        │                │      │
                       │        │                │      │
HÍBRIDO ───────────────┼────────┼────────────────┼──────X
  • SQL + Embeddings   │        │                │      │
  • Filtros + Semântica│        │                │      │
  • Máxima performance │        │                │      │
                       │        │                │      │
                    BARATO ────────────────────── CARO
```

## 💡 Quando Usar Cada Um

```text
╔═══════════════════════════════════════════════════════════════════╗
║                    GUIA DE DECISÃO RÁPIDA                         ║
╚═══════════════════════════════════════════════════════════════════╝

PERGUNTA 1: Usuário digita linguagem natural?
   ├─ SIM → EMBEDDINGS ou HÍBRIDO
   └─ NÃO → SQL

PERGUNTA 2: Precisa encontrar sinônimos?
   ├─ SIM → EMBEDDINGS
   └─ NÃO → SQL

PERGUNTA 3: Performance < 10ms é crítica?
   ├─ SIM → SQL (ou HÍBRIDO com cache)
   └─ NÃO → EMBEDDINGS ok

PERGUNTA 4: Tem orçamento para API?
   ├─ SIM → EMBEDDINGS
   └─ NÃO → SQL

PERGUNTA 5: Precisa de agregações (SUM, COUNT)?
   ├─ SIM → SQL
   └─ NÃO → Qualquer um

RESULTADO RECOMENDADO:
   • 100% SQL: Dados estruturados, sem NLP
   • 100% Embeddings: Busca semântica pura
   • HÍBRIDO: Melhor de ambos (RECOMENDADO!)
```

## 📈 Evolução Sugerida

```text
FASE 1: MVP          FASE 2: Inteligente    FASE 3: Escala
┌───────────┐       ┌───────────┐          ┌───────────┐
│  SQLite   │  ──▶  │  SQLite   │   ──▶    │PostgreSQL │
│   LIKE    │       │     +     │          │     +     │
│           │       │ Embeddings│          │ pgvector  │
└───────────┘       └───────────┘          └───────────┘
     │                    │                      │
     ▼                    ▼                      ▼
  Grátis             ~$20/mês              ~$50/mês
  Simples            Inteligente          Industrial
  Rápido             Rápido + Smart       Ultra-rápido
```

## 🎓 Aprendizados Principais

### 1. SQL é Ótimo para

```text
✅ Busca exata:      SELECT WHERE id = 123
✅ Filtros rápidos:  WHERE bairro = 'Centro'
✅ Agregações:       SELECT COUNT(*), AVG(idade)
✅ Joins:            FROM a INNER JOIN b
```

### 2. Embeddings São Ótimos para

```text
✅ Busca semântica:  "dor forte no peito" → encontra "angina"
✅ Sinônimos:        "febre" → encontra "hipertermia"
✅ Contexto:         Entende intenção do usuário
✅ Recomendações:    Baseado em similaridade
```

### 3. Híbrido É Melhor para

```text
✅ Filtrar com SQL:           WHERE bairro = 'Centro'
✅ Buscar com embeddings:     sintomas similares
✅ Combinar resultados:       Recomendação inteligente
✅ Performance + Inteligência: Rápido E preciso
```

## 💰 Análise de Custos

```text
┌────────────────────────────────────────────────────────┐
│              CUSTO POR 1000 BUSCAS                     │
├────────────────────────────────────────────────────────┤
│                                                        │
│  SQL LIKE:           $0                                │
│  ██ Grátis                                            │
│                                                        │
│  Embeddings (setup): $0.02  (uma vez)                 │
│  █ Quase grátis                                       │
│                                                        │
│  Embeddings (busca): $0     (cálculo local)           │
│  ██ Grátis após setup                                 │
│                                                        │
│  HÍBRIDO:            $0.02  (setup) + $0 (busca)      │
│  █ Melhor ROI                                         │
│                                                        │
└────────────────────────────────────────────────────────┘

CONCLUSÃO: Embeddings têm custo inicial MÍNIMO,
depois as buscas são GRÁTIS (cálculo local)!
```

## 🚀 Próximos Passos

```text
VOCÊ ESTÁ AQUI → [Aula 10: Embeddings + SQLite]
                         │
                         ▼
              [Aula 11: pgvector + PostgreSQL]
                         │
                         ▼
              [Aula 12: Índices Vetoriais HNSW]
                         │
                         ▼
              [Aula 13: RAG (Retrieval-Augmented Generation)]
                         │
                         ▼
              [Aula 14: API REST com Busca Semântica]
```

## 📚 Recursos Criados

```text
aula10/
├── README.md                    ✅ Documentação principal
├── main.py                      ✅ Sistema comparativo interativo
├── COMPARACAO_DETALHADA.md      ✅ Análise técnica profunda
├── GUIA_DECISAO.md              ✅ Quando usar cada um
├── RESUMO_VISUAL.md             ✅ Este arquivo
├── exemplos/
│   ├── 01_sqlite_tradicional.py ✅ SQL LIKE
│   └── 02_embeddings_basico.py  ✅ Introdução embeddings
└── exercicios/
    ├── exercicio1_criar_embeddings.py  ✅ Prática
    └── README_EXERCICIOS.md            ✅ Guia exercícios
```

---

**🎯 Execute:** `uv run aula10/main.py` e veja a mágica acontecer!
