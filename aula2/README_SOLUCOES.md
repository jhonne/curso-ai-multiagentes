# Soluções dos Exercícios - Aula 2

Este diretório contém as soluções para os 3 exercícios propostos na Aula 2 do curso de CrewAI.

## 📋 Exercícios Resolvidos

### 1. **Exercício 1: Equipe de Conteúdo** (`exercicio1_solucao.py`)

- **Cenário**: Criar post para Instagram da Padaria do João
- **Agentes**: Gerador de Ideias + Escritor de Posts
- **Objetivo**: Gerar conteúdo criativo para redes sociais

### 2. **Exercício 2: Atendimento ao Cliente** (`exercicio2_solucao.py`)

- **Cenário**: Responder reclamação de cliente de loja online
- **Agentes**: Analisador de Problemas + Respondedor Amigável
- **Objetivo**: Processar e responder reclamações de forma profissional

### 3. **Exercício 3: Desenvolvimento de Produto** (`exercicio3_solucao.py`)

- **Cenário**: Criar ideia de app para estudantes universitários
- **Agentes**: Descobridor de Problemas + Criador de Ideias
- **Objetivo**: Identificar problemas e criar soluções tecnológicas

## 🚀 Como Executar

### Pré-requisitos

1. **Chave da OpenAI configurada** no arquivo `.env`:

   ```
   OPENAI_API_KEY=sua_chave_aqui
   ```

2. **Dependências instaladas**:

   ```bash
   uv sync
   ```

### Executando os Exercícios

**Exercício 1 - Marketing Digital:**

```bash
uv run aula2/exercicio1_solucao.py
```

**Exercício 2 - Atendimento ao Cliente:**

```bash
uv run aula2/exercicio2_solucao.py
```

**Exercício 3 - Desenvolvimento de Produto:**

```bash
uv run aula2/exercicio3_solucao.py
```

## 🎯 Conceitos Aplicados

Todas as soluções demonstram os conceitos fundamentais da Aula 2:

- ✅ **Criação de Agentes** com `role`, `goal` e `backstory`
- ✅ **Definição de Tarefas** com `description` e `expected_output`
- ✅ **Montagem de Crews** com processo sequencial
- ✅ **Colaboração entre Agentes** para resolver problemas complexos
- ✅ **Aplicação prática** em cenários reais de negócio

## 💡 Dicas de Aprendizado

1. **Execute um por vez** para entender melhor cada conceito
2. **Leia os comentários** no código para compreender a estrutura
3. **Modifique os prompts** para experimentar diferentes resultados
4. **Compare as saídas** para ver como os agentes colaboram

## 🔧 Resolução de Problemas

Se encontrar erros:

- Verifique se a chave OpenAI está correta no `.env`
- Confirme se tem créditos suficientes na conta OpenAI
- Teste sua conexão com a internet
- Execute novamente (às vezes é temporário)

## 📚 Próximos Passos

Após executar todos os exercícios, você estará pronto para:

- Criar seus próprios agentes personalizados
- Definir tarefas mais complexas
- Explorar diferentes tipos de processo (sequencial vs paralelo)
- Avançar para a Aula 3 com ferramentas e processos avançados

---

**Bom aprendizado!** 🎓
