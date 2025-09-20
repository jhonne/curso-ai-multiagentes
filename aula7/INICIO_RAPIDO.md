# 🚀 Início Rápido - Aula 7 Avançada

## Sistema Médico com PostgreSQL + Embeddings + IA

### ⚡ Configuração Rápida (5 minutos)

```bash
# 1. PostgreSQL com Docker
docker run --name postgres-crewai \
  -e POSTGRES_PASSWORD=senha123 \
  -e POSTGRES_DB=crewai_medico \
  -p 5432:5432 \
  -d pgvector/pgvector:pg16

# 2. Instalar dependências
uv sync

# 3. Configurar OpenAI
echo "OPENAI_API_KEY=sua_chave_aqui" > .env

# 4. Executar sistema
uv run aula7/main.py
```

### 🎯 Menu Interativo

Ao executar o sistema, você terá:

1. **📋 Demonstração IA**: 5 casos clínicos reais com análise semântica
2. **🤖 Modo Interativo**: Digite sintomas e veja a análise completa
3. **📊 Estatísticas**: Métricas do sistema, cache, custos
4. **🧪 Teste Embeddings**: Valide o sistema de busca semântica

### 🔍 Casos de Teste Recomendados

Digite estes sintomas no modo interativo:

- **Emergência**: "dor forte no peito, suor frio, falta de ar"
- **Urgente**: "dor de cabeça súbita muito forte, vômito"
- **Moderado**: "febre alta há 3 dias, dor de garganta"
- **Leve**: "tosse seca há 1 semana, cansaço"

### 🏥 O Que o Sistema Faz

1. **Análise Semântica**: Usa embeddings para entender sintomas
2. **Busca Inteligente**: Encontra sintomas similares na base
3. **Classificação de Urgência**: IA determina prioridade (1-5)
4. **Geolocalização**: Encontra estabelecimentos próximos
5. **Recomendação Final**: Combina análise médica + geografia

### 💰 Custos Otimizados

- **Cache Inteligente**: Embeddings são reutilizados
- **Tokens Mínimos**: text-embedding-3-small (mais barato)
- **Análise Local**: PostgreSQL processa depois da IA
- **Custo típico**: $0.001-0.005 por consulta

### 🚨 Troubleshooting Rápido

**PostgreSQL não conecta?**
```bash
# Verificar se container está rodando
docker ps | grep postgres

# Ver logs do container
docker logs postgres-crewai
```

**OpenAI API Error?**
```bash
# Verificar se API key está configurada
cat .env

# Testar conexão
uv run teste_api.py
```

**Import Error?**
```bash
# Instalar dependências específicas
uv add psycopg2-binary pgvector-python openai
```

### 📈 Performance

- **Primeira execução**: ~10s (carrega dados + gera embeddings)  
- **Execuções seguintes**: ~2s (usa cache)
- **Busca semântica**: <100ms (índices HNSW)
- **Análise completa**: <5s (agentes + IA)

### 🎓 Próximos Passos

1. **Teste todos os casos** do menu de demonstração
2. **Experimente sintomas próprios** no modo interativo  
3. **Analise estatísticas** para entender performance
4. **Leia o código** para entender a implementação

---

**🎯 GOAL**: Dominar sistemas médicos reais com IA avançada!