# 🚀 Aula 10: Embeddings e Busca Semântica - Início Rápido

## ⚡ Execute em 30 Segundos

```bash
# 1. Certifique-se que tem o banco de dados
ls db/curso.db  # Deve existir

# 2. Configure API Key (se ainda não fez)
export OPENAI_API_KEY='sua-chave-aqui'

# 3. Execute o sistema principal
uv run aula10/main.py
```

## 🎯 O Que Você Vai Ver

### Comparação Lado a Lado

**SQL Tradicional:**

- Busca: "dor"
- Resultados: 15 sintomas com palavra "dor"
- Limitação: Não encontra "cefaleia" (sinônimo)

**Busca Semântica:**

- Busca: "dor de cabeça"
- Resultados: Cefaleia (95%), Enxaqueca (89%), etc.
- Vantagem: Entende significado, não apenas texto

## 💡 Principal Aprendizado

```text
┌─────────────────────────────────────────────────────┐
│  SQL é ÓTIMO para busca EXATA                       │
│  Embeddings são ÓTIMOS para busca INTELIGENTE       │
│  HÍBRIDO é o MELHOR para projetos reais             │
└─────────────────────────────────────────────────────┘
```

## 📚 Arquivos Importantes

1. **`README.md`** - Documentação completa (COMECE AQUI)
2. **`main.py`** - Sistema interativo (EXECUTE ISTO)
3. **`GUIA_DECISAO.md`** - Quando usar cada um (MUITO ÚTIL)
4. **`exercicios/`** - Aprenda fazendo (PRATIQUE)

## 🎓 Próximo Passo

Após explorar a aula 10:

→ **Aula 11:** pgvector + PostgreSQL (busca em escala industrial)

---

**Dúvidas?** Veja `INDICE.md` para navegação completa!
