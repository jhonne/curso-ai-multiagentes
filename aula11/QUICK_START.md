# 🚀 Quick Start - RAG em 30 Minutos

**Bem-vindo à Aula 11!** Este guia rápido te ensina RAG em apenas 30 minutos.

## O Que Você Vai Aprender

- ✅ O que é RAG (5 min)
- ✅ Memory System na prática (10 min)
- ✅ Knowledge Sources na prática (10 min)
- ✅ Seu primeiro sistema RAG (5 min)

**Tempo total:** ~30 minutos

---

## 1️⃣ O Que É RAG? (5 min)

### Conceito Simples

**RAG** = Retrieval Augmented Generation

```text
Sem RAG:                    Com RAG:
User: "Protocolo 2024?"     User: "Protocolo 2024?"
LLM: "Não sei" ❌           System: [busca em docs]
                            LLM: "Segundo doc X..." ✅
```

### Componentes

1. **Memory** 🧠 - Agente lembra de conversas
2. **Knowledge** 📚 - Agente consulta documentos
3. **RAG** 🚀 - Memory + Knowledge juntos!

---

## 2️⃣ Execute Seu Primeiro Exemplo (15 min)

### Passo 1: Verificar Setup

```bash
cd /home/lotus/supra/curso_crewai/aula11
uv run quick_start.py
```

### Passo 2: Ver a Diferença

O script mostrará 3 comparações:

**A) Sem Memory vs Com Memory**

```python
# SEM memory
User: "Meu nome é João"
Bot: "Olá!"
User: "Qual meu nome?"
Bot: "Não sei" ❌

# COM memory
User: "Meu nome é João"
Bot: "Prazer, João!"
User: "Qual meu nome?"
Bot: "João!" ✅
```

**B) Sem Knowledge vs Com Knowledge**

```python
# SEM knowledge
User: "Dor no peito"
Bot: "Procure médico" ❌ (genérico)

# COM knowledge
Bot: "VERMELHO - Emergência!" ✅ (protocolo)
```

**C) RAG Completo**

```python
# Memory + Knowledge
User: "João, 45 anos, dor no peito"
Bot: "João, sua idade agrava.
     Protocolo: VERMELHO" ✅
```

---

## 3️⃣ Faça Seu Exercício Rápido (10 min)

```bash
uv run exercicio_rapido.py
```

**Objetivo:** Criar chatbot que lembra do paciente E consulta protocolos

**Tempo:** 10 minutos

**Gabarito:** Incluído no arquivo

---

## 4️⃣ Próximos Passos

### ✅ Você Já Sabe o Básico

Agora escolha seu caminho:

### 🟢 Para Iniciantes

```bash
# Explorar módulos individualmente
cd modulos/01_memory
uv run exemplo.py        # Memory profundo
uv run exercicio.py      # Praticar

cd ../02_knowledge
uv run exemplo.py        # Knowledge profundo
uv run exercicio.py      # Praticar
```

**Tempo:** +2h (1h por módulo)

### 🟡 Para Intermediários

```bash
# Ir direto para RAG avançado
cd modulos/03_rag_avancado
uv run exemplo_multiagent.py     # 3 agentes
uv run exemplo_embeddings.py     # Integra Aula 10
```

**Tempo:** +1-2h

### 🔴 Para Avançados

```bash
# Documentação completa
cat docs/GUIA_COMPLETO.md        # Tudo sobre RAG
cat docs/CASOS_DE_USO.md         # Inspiração

# Criar seu próprio RAG
code meu_projeto_rag/
```

---

## 📊 Checklist de Progresso

### Quick Start (30 min)

- [ ] Entendi o conceito de RAG
- [ ] Executei quick_start.py
- [ ] Fiz exercicio_rapido.py
- [ ] Vi a diferença entre com/sem Memory e Knowledge

### Aprofundamento (Opcional)

- [ ] Módulo 1: Memory System
- [ ] Módulo 2: Knowledge Sources
- [ ] Módulo 3: RAG Avançado
- [ ] Integração com Aula 10 (Embeddings)

### Maestria (Opcional)

- [ ] Li documentação completa
- [ ] Criei meu próprio sistema RAG
- [ ] Deploy em produção

---

## ❓ FAQ Rápido

**P: Preciso fazer tudo hoje?**
R: Não! Quick Start em 30 min. Resto quando quiser.

**P: Posso pular módulos?**
R: Sim! Cada módulo é independente.

**P: E se travar?**
R: Veja `docs/TROUBLESHOOTING.md`

**P: Quanto custa (OpenAI)?**
R: Quick Start: ~$0.01. Curso completo: ~$0.10-0.50

---

## 🎯 Começar Agora

```bash
# Execute o Quick Start
cd /home/lotus/supra/curso_crewai/aula11
uv run quick_start.py
```

**Divirta-se aprendendo RAG! 🚀**

---

**Próximo:** [README.md](README.md) para visão completa da aula
