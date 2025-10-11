# Nível de Complexidade - Aula 10

Análise detalhada da complexidade, progressão de aprendizado e pontos críticos da Aula 10 sobre Embeddings e Busca Semântica.

## Classificação Geral

**Nível: Intermediário** com ramp-up suave para quem completou a Aula 9

### Distribuição por Componente

| Componente | Nível | Descrição |
|------------|-------|-----------|
| **Conceitos Básicos** | 🟢 Fácil | SQL vs embeddings, similaridade coseno |
| **Implementação Prática** | 🟡 Médio | Criar/armazenar embeddings, Top-K |
| **Abordagem Híbrida** | 🟡 Médio-Alto | SQL + semântica com métricas |
| **Otimização/Escala** | 🔴 Avançado | FAISS, pgvector, índices vetoriais |

## Progressão de Aprendizado

### Fase 1: Fundamentos (Fácil)

**Tempo estimado:** 30-45 minutos

**Conteúdo:**

- Diferença entre busca exata (SQL) e busca semântica
- Como textos viram vetores numéricos (embeddings)
- Similaridade coseno e sua interpretação
- Quando usar cada abordagem

**Pré-requisitos:**

- SQL básico (SELECT, WHERE, LIKE)
- Python básico (loops, funções, listas)
- Conceitos de distância/similaridade (opcional)
- Aula 9 concluída (recomendado)

**Arquivos:**

- `aula10/INICIO_RAPIDO.md`
- `aula10/RESUMO_VISUAL.md`
- `aula10/exemplos/01_sqlite_tradicional.py`

### Fase 2: Implementação Prática (Médio)

**Tempo estimado:** 1-2 horas

**Conteúdo:**

- Chamar API de embeddings da OpenAI
- Armazenar vetores no SQLite (BLOB/JSON)
- Calcular similaridade coseno em Python
- Implementar busca Top-K por relevância
- Gerenciar cache e batching

**Pré-requisitos:**

- Fase 1 completa
- Familiaridade com APIs REST
- Noções de NumPy/arrays (útil)
- Conceitos de normalização de textos

**Arquivos:**

- `aula10/exemplos/02_embeddings_basico.py`
- `aula10/exercicios/exercicio1_criar_embeddings.py`
- `aula10/main.py`

**Desafios típicos:**

- Normalização inconsistente entre corpus e queries
- Entender dimensionalidade dos vetores (1536)
- Serialização arrays NumPy para BLOB/JSON
- Performance na primeira criação de embeddings

### Fase 3: Abordagem Híbrida (Médio-Alto)

**Tempo estimado:** 2-3 horas

**Conteúdo:**

- Combinar filtros SQL com ranking semântico
- Calibrar threshold de similaridade
- Medir precision, recall e F1-score
- Otimizar latência vs qualidade
- Estratégias de fallback

**Pré-requisitos:**

- Fase 2 completa
- Conhecimento de métricas de avaliação
- Experiência com otimização de consultas
- Noções de trade-offs (velocidade/precisão/custo)

**Arquivos:**

- `aula10/GUIA_DECISAO.md`
- `aula10/COMPARACAO_DETALHADA.md`
- Exemplos de busca híbrida no `main.py`

**Desafios típicos:**

- Calibrar número ideal de resultados (K)
- Ajustar threshold por contexto
- Balancear quando usar SQL vs semântica
- Criar dataset de validação manualmente

### Fase 4: Otimização e Escala (Avançado)

**Tempo estimado:** 3-5 horas

**Conteúdo (preview para Aulas 11-13):**

- Índices vetoriais (HNSW, IVFFlat)
- Migração para pgvector
- Compressão de embeddings (float16, quantização)
- Biblioteca FAISS para busca aproximada
- Estratégias de sharding e particionamento

**Pré-requisitos:**

- Fase 3 completa
- Experiência com banco de dados em produção
- Conhecimento de estruturas de dados avançadas
- Familiaridade com Docker/PostgreSQL

**Arquivos:**

- Documentação em `aula10/COMPARACAO_DETALHADA.md`
- Preparação para Aula 11 (PostgreSQL + pgvector)

## Pontos Críticos de Atenção

### 🔴 Críticos (podem quebrar o sistema)

#### 1. Consistência de Pré-processamento

**Por que é crítico:** Embeddings diferentes para mesmo texto semântico causam falhas.

**Solução:**

```python
def normalizar_texto(texto):
    """Pipeline de normalização padrão"""
    import unicodedata
    
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto)
    texto = texto.encode('ASCII', 'ignore').decode('ASCII')
    texto = ' '.join(texto.split())
    
    return texto
```

**Checklist:**

- Mesmo pipeline em corpus e queries
- Documentar transformações
- Testar com acentos e espaços
- Validar que não quebra pt-br

#### 2. Armazenamento de Vetores

**Por que é crítico:** Corrupção de dados ou incompatibilidade.

**Solução:**

```python
import json
from datetime import datetime

def salvar_embedding(conn, texto_id, texto, embedding, modelo="text-embedding-3-small"):
    embedding_list = embedding.tolist()
    
    metadados = {
        "model": modelo,
        "created_at": datetime.now().isoformat(),
        "dimension": len(embedding_list),
        "version": "1.0"
    }
    
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO embeddings (texto_id, texto_original, embedding, metadados)
        VALUES (?, ?, ?, ?)
    """, (texto_id, texto, json.dumps(embedding_list), json.dumps(metadados)))
    
    conn.commit()
```

**Checklist:**

- Validar dimensão do vetor (1536)
- Salvar metadados (modelo, data, versão)
- Testar serialização/desserialização
- Planejar migração de esquema

#### 3. Gerenciamento de API Keys

**Por que é crítico:** Vazamento de chaves ou custos descontrolados.

**Solução:**

```python
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY não encontrada")

print("✅ API Key carregada com sucesso")
```

**Checklist:**

- API key em `.env`, não hardcoded
- `.env` no `.gitignore`
- Validar chave antes de usar
- Não logar chaves nem tokens

### 🟡 Importantes (afetam qualidade/custo)

#### 4. Cache e Batching

**Impacto:** Reduz latência em 90% e custos em até 100%.

```python
import hashlib
import pickle

class CacheEmbeddings:
    def __init__(self, cache_dir="./cache_embeddings"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get(self, texto, modelo):
        chave = hashlib.md5(f"{modelo}:{texto}".encode()).hexdigest()
        cache_path = os.path.join(self.cache_dir, f"{chave}.pkl")
        
        if os.path.exists(cache_path):
            with open(cache_path, 'rb') as f:
                return pickle.load(f)
        return None
```

#### 5. Calibração de Threshold

**Impacto:** Falsos positivos/negativos comprometem UX.

```python
def encontrar_threshold_otimo(dataset_validacao, thresholds=[0.5, 0.6, 0.7, 0.8, 0.9]):
    resultados = []
    
    for threshold in thresholds:
        tp = fp = fn = 0
        
        for item in dataset_validacao:
            # Calcular métricas
            pass
        
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
        
        resultados.append({"threshold": threshold, "f1": f1})
    
    return sorted(resultados, key=lambda x: x["f1"], reverse=True)
```

#### 6. Monitoramento de Custos

**Impacto:** Custos podem crescer rapidamente.

```python
class MonitorCustosEmbeddings:
    def __init__(self, orcamento_limite=5.0):
        self.orcamento_limite = orcamento_limite
        self.gasto_atual = 0.0
        self.precos = {
            "text-embedding-3-small": 0.02 / 1_000_000
        }
    
    def registrar_request(self, texto, modelo="text-embedding-3-small"):
        tokens = len(texto) / 4
        custo = tokens * self.precos[modelo]
        self.gasto_atual += custo
        
        if self.gasto_atual > self.orcamento_limite * 0.8:
            print(f"⚠️ 80% do orçamento atingido")
```

## Armadilhas Comuns

### ❌ Criar Embeddings On-the-Fly

**Problema:** Latência alta e custos desnecessários.

**Solução:**

```python
# ❌ RUIM
def buscar_ruim(query):
    query_emb = criar_embedding(query)
    for doc in corpus:
        doc_emb = criar_embedding(doc)  # API call TODA VEZ!

# ✅ BOM
def indexar_corpus(corpus):
    embeddings = [criar_embedding_com_cache(doc) for doc in corpus]
    salvar_embeddings(embeddings)
    return embeddings
```

### ❌ Misturar Pré-processamentos

**Problema:** Resultados inconsistentes.

**Solução:**

```python
# ❌ RUIM
corpus_emb = [criar_embedding(doc.lower()) for doc in corpus]
query_emb = criar_embedding(query.upper())  # Diferente!

# ✅ BOM
pipeline = lambda t: normalizar_texto(t)
corpus_emb = [criar_embedding(pipeline(doc)) for doc in corpus]
query_emb = criar_embedding(pipeline(query))
```

### ❌ Top-K Fixo sem Threshold

**Problema:** Retorna resultados irrelevantes.

**Solução:**

```python
# ❌ RUIM
def buscar_ruim(query, k=5):
    return scores[:k]  # Pode incluir scores baixos!

# ✅ BOM
def buscar_bom(query, k=5, threshold=0.7):
    scores_filtrados = [s for s in scores if s >= threshold]
    return scores_filtrados[:k]
```

## Checklist de Prontidão

### Nível Básico (Fase 1)

- [ ] Entendo diferença entre SQL e busca semântica
- [ ] Sei o que são embeddings
- [ ] Consigo calcular similaridade coseno
- [ ] Rodei exemplos básicos

### Nível Intermediário (Fase 2)

- [ ] Criei embeddings via API OpenAI
- [ ] Armazenei vetores no SQLite
- [ ] Implementei busca Top-K
- [ ] Configurei cache
- [ ] Testei com meu dataset

### Nível Avançado (Fase 3)

- [ ] Combinei SQL + semântica
- [ ] Calibrei threshold
- [ ] Medi precision/recall/F1
- [ ] Implementei fallback
- [ ] Monitorei custos e performance

### Produção-Ready (Fase 4)

- [ ] Implementei retry e rate limiting
- [ ] Configurei logs
- [ ] Documentei pipeline
- [ ] Tenho estratégia de migração
- [ ] Sistema < 200ms por busca (P95)

## Métricas de Sucesso

### Performance

- Latência de busca: < 200ms (P95)
- Hit rate do cache: > 70%
- Throughput: > 100 buscas/segundo

### Qualidade

- Precision: > 0.8
- Recall: > 0.7
- F1-Score: > 0.75

### Custos

- Indexação: < $1 para 10k documentos
- Busca: ~$0 (cache + local)
- Total mensal: < $10 para 100k docs + 10k buscas/dia

## Recursos de Apoio

### Documentação Oficial

- [OpenAI Embeddings Guide](https://platform.openai.com/docs/guides/embeddings)
- [OpenAI Pricing](https://openai.com/pricing)

### Arquivos do Curso

- `aula10/README.md` - Visão geral
- `aula10/INICIO_RAPIDO.md` - Início rápido
- `aula10/GUIA_DECISAO.md` - Quando usar cada abordagem
- `aula10/COMPARACAO_DETALHADA.md` - Comparação técnica

## Próximos Passos

### Após Dominar a Aula 10

1. Aula 11: PostgreSQL + pgvector
2. Aula 12: Índices HNSW e IVFFlat
3. Aula 13: RAG (Retrieval-Augmented Generation)
4. Aula 14: API REST com busca semântica

### Projetos Práticos Sugeridos

1. Sistema de busca em documentação técnica
2. Recomendação de artigos similares
3. Chatbot com memória semântica
4. Sistema de FAQ inteligente
5. Classificação automática de tickets

## Conclusão

A Aula 10 oferece progressão estruturada do básico ao avançado em busca semântica.

**Tempo total estimado:** 6-10 horas (incluindo prática)

**Dificuldade geral:** Intermediária com picos avançados opcionais

### Objetivos ao Final

- Implementar busca semântica em produção
- Otimizar custos e performance
- Calibrar métricas de qualidade
- Decidir entre SQL, embeddings ou híbrido
- Preparar migração para soluções escaláveis

---

**Última atualização:** 11 de outubro de 2025  
**Versão:** 1.0
