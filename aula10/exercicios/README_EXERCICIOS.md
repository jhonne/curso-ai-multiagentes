# 🎯 Exercícios Práticos - Aula 10

## 📋 Visão Geral

Exercícios progressivos para dominar embeddings e busca semântica, comparando com SQL tradicional.

## 🟢 Exercício 1: Criar Embeddings (Iniciante)

**Arquivo:** `exercicio1_criar_embeddings.py`

**Objetivo:** Criar e armazenar embeddings para todos os sintomas do banco de dados

**O que você vai aprender:**

- Conectar ao banco SQLite
- Usar OpenAI Embeddings API
- Armazenar vetores em banco relacional
- Serializar/deserializar JSON

**Tarefas:**

1. Criar tabela `sintoma_embeddings`
2. Ler sintomas do banco
3. Criar embeddings usando OpenAI
4. Salvar embeddings no banco
5. Validar resultados

**Tempo estimado:** 30-45 minutos

**Executar:**

```bash
uv run aula10/exercicios/exercicio1_criar_embeddings.py
```

## 🟡 Exercício 2: Busca Semântica (Intermediário)

**Arquivo:** `exercicio2_busca_semantica.py`

**Objetivo:** Implementar busca por similaridade semântica

**O que você vai aprender:**

- Calcular similaridade coseno
- Buscar Top-K resultados
- Ordenar por score de similaridade
- Comparar com busca SQL tradicional

**Tarefas:**

1. Implementar cálculo de similaridade coseno
2. Criar função de busca semântica
3. Retornar Top-5 resultados
4. Comparar com SQL LIKE
5. Analisar diferenças

**Tempo estimado:** 45-60 minutos

**Executar:**

```bash
uv run aula10/exercicios/exercicio2_busca_semantica.py
```

## 🔴 Exercício 3: Sistema Híbrido (Avançado)

**Arquivo:** `exercicio3_sistema_hibrido.py`

**Objetivo:** Combinar SQL + Embeddings para busca inteligente

**O que você vai aprender:**

- Arquitetura híbrida
- Otimização de performance
- Filtros SQL + busca semântica
- Sistema de recomendação

**Tarefas:**

1. Filtrar estabelecimentos por região (SQL)
2. Buscar sintomas similares (Embeddings)
3. Combinar resultados
4. Recomendar estabelecimento apropriado
5. Benchmark de performance

**Tempo estimado:** 60-90 minutos

**Executar:**

```bash
uv run aula10/exercicios/exercicio3_sistema_hibrido.py
```

## 🎯 Critérios de Sucesso

### Exercício 1

- [ ] Tabela criada corretamente
- [ ] Todos os sintomas processados
- [ ] Embeddings salvos no banco
- [ ] Validação mostra 1536 dimensões
- [ ] Sem erros de API

### Exercício 2

- [ ] Similaridade coseno implementada
- [ ] Busca retorna Top-5 corretos
- [ ] Scores de 0 a 1
- [ ] Comparação com SQL funcional
- [ ] Resultados fazem sentido

### Exercício 3

- [ ] Filtros SQL rápidos
- [ ] Busca semântica precisa
- [ ] Combinação eficiente
- [ ] Recomendação inteligente
- [ ] Performance adequada

## 💡 Dicas e Truques

### Para Todos os Exercícios

- **API Key:** Certifique-se que `OPENAI_API_KEY` está configurada
- **Banco:** Verifique que `db/curso.db` existe
- **Cache:** Reutilize embeddings já criados
- **Erros:** Leia mensagens de erro com atenção

### Exercício 1

- Use `json.dumps()` para serializar vetores
- `INSERT OR REPLACE` para evitar duplicatas
- Mostre progresso ao processar muitos itens
- Teste com 1-2 sintomas antes de processar todos

### Exercício 2

- Use `numpy` para cálculos vetoriais
- Normalize vetores para melhor precisão
- Top-K deve ordenar por similaridade DESC
- Compare queries médicas vs coloquiais

### Exercício 3

- SQL primeiro, embeddings depois (mais rápido)
- Use LIMIT nas queries SQL
- Cache embeddings de queries frequentes
- Meça tempo de cada etapa

## 🐛 Troubleshooting

### Erro: "OPENAI_API_KEY not found"

```bash
# Solução:
uv run configurar.py
# ou
export OPENAI_API_KEY='sk-...'
```

### Erro: "Table already exists"

```bash
# Normal! Use CREATE TABLE IF NOT EXISTS
# ou DELETE a tabela antes:
sqlite3 db/curso.db "DROP TABLE sintoma_embeddings;"
```

### Erro: "Rate limit exceeded"

```bash
# Solução: Adicione delay entre chamadas
import time
time.sleep(0.5)  # 500ms entre embeddings
```

### Embeddings muito lentos

```bash
# Solução: Processar em batch
# Criar embeddings de 10-20 textos por vez
client.embeddings.create(input=[texto1, texto2, ...])
```

## 📊 Resultados Esperados

### Exercício 1

```text
✅ 266 embeddings criados
📊 Dimensões: 1536
💾 Tamanho: ~1.5 MB
⏱️  Tempo: ~2-3 minutos
💰 Custo: ~$0.01
```

### Exercício 2

```text
Query: "dor de cabeça"

Top-5 Resultados:
1. Cefaleia (95% similar)
2. Enxaqueca (89% similar)
3. Dor craniana (87% similar)
4. Migrânea (85% similar)
5. Dor de cabeça (92% similar)
```

### Exercício 3

```text
Filtro SQL: bairro = 'Centro'
→ 3 estabelecimentos (10ms)

Busca Semântica: "dor no peito e falta de ar"
→ Top-5 sintomas (15ms)

Recomendação: Hospital Central (urgência: ALTA)
Tempo total: 25ms
```

## 🎓 Próximos Passos

Após completar os exercícios:

1. **Experimente** com seus próprios dados
2. **Compare** performance em diferentes cenários
3. **Otimize** para seu caso de uso
4. **Estude** aula sobre pgvector (PostgreSQL)

## 📚 Recursos Adicionais

- `../main.py` - Implementação completa de referência
- `../COMPARACAO_DETALHADA.md` - Análise técnica profunda
- `../GUIA_DECISAO.md` - Quando usar cada abordagem
- `../exemplos/` - Exemplos passo a passo

## 🤝 Suporte

- 💬 **Dúvidas:** Discord do curso
- 🐛 **Problemas:** GitHub Issues
- 📖 **Documentação:** Arquivos `.md` da aula
- 💡 **Soluções:** Veja `main.py` e exemplos

---

**Boa sorte nos exercícios! 🚀**

*Lembre-se: O importante é aprender o conceito, não completar perfeitamente na primeira tentativa.*
