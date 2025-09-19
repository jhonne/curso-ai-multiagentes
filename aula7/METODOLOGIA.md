# Metodologia e Escopo da Aula 7

## 📚 Objetivo Educacional

Esta aula tem como foco ensinar **conceitos fundamentais** de integração entre agentes CrewAI e dados estruturados, usando o contexto médico como caso de uso prático e relevante.

## 🎯 O que os Alunos Aprendem

### ✅ **Conceitos Principais:**

1. **Integração Agentes + Dados**: Como conectar agentes CrewAI a fontes de dados estruturadas
2. **Fluxo de Trabalho Médico**: Orquestração de múltiplos agentes especializados
3. **Geolocalização Aplicada**: Cálculos de proximidade em sistemas de saúde
4. **Classificação Automática**: Algoritmos para priorização médica
5. **Consultas Otimizadas**: Estruturação eficiente de queries em domínio médico

### ✅ **Habilidades Técnicas:**

- Estruturação de dados relacionais para sistemas médicos
- Implementação de ferramentas personalizadas para agentes
- Cálculos geográficos (fórmula de Haversine)
- Design de prompts especializados para contexto médico
- Fluxo de dados entre agentes especializados

## 🛠️ Implementação Didática

### **Dados Simulados (Não PostgreSQL Real)**

- **SQLite em memória** para simplicidade e portabilidade
- **Dados baseados na realidade** do sistema de saúde do Piauí
- **10 estabelecimentos, 10 sintomas, 10 queixas** para demonstração eficaz
- **Coordenadas reais** de Teresina para cálculos geográficos

### **Por que Dados Simulados?**

1. **Foco no Aprendizado**: Elimina complexidade de setup de banco real
2. **Portabilidade**: Funciona em qualquer ambiente sem configuração
3. **Conceitos Transferíveis**: Mesma lógica aplicável ao PostgreSQL real
4. **Iteração Rápida**: Alunos podem experimentar sem riscos

## 🔄 Progressão Para Aula 8

Os conceitos aprendidos na Aula 7 serão **diretamente aplicados** na Aula 8 com:

- **PostgreSQL Real** + extensão pgvector
- **OpenAI Embeddings** para busca semântica
- **Similaridade vetorial** entre sintomas
- **Cache inteligente** de embeddings
- **Sistema de recomendação** baseado em IA

## 📖 Metodologia de Ensino

### **Abordagem Progressiva:**

1. **Conceitos Básicos** → Exercício 1 (consultas simples)
2. **Geolocalização** → Exercício 2 (busca geográfica)
3. **Integração Completa** → Sistema principal com múltiplos agentes
4. **Casos Reais** → Demonstrações com cenários médicos

### **Aprendizado Ativo:**

- **Exemplos Executáveis**: Todos os códigos funcionam imediatamente
- **Exercícios Práticos**: Do básico ao avançado com feedback
- **Casos Clínicos**: Cenários realistas para aplicação
- **Debug Transparente**: Logs detalhados para entendimento

## ⚠️ Nota sobre Ferramentas de Apoio

O desenvolvimento desta aula pode utilizar ferramentas auxiliares (como MCP para acesso a dados durante a criação), mas estas **NÃO fazem parte do conteúdo educacional**.

Os alunos aprendem:

- ✅ Integração CrewAI + dados estruturados
- ✅ Conceitos aplicáveis a qualquer banco de dados
- ✅ Lógica de negócio em sistemas médicos

Os alunos **NÃO precisam saber**:

- ❌ Ferramentas específicas de desenvolvimento
- ❌ Configurações complexas de banco
- ❌ Protocolos auxiliares não relacionados ao CrewAI

## 🎓 Resultado Esperado

Ao final da aula, os alunos devem ser capazes de:

1. **Conectar agentes CrewAI** a qualquer fonte de dados estruturada
2. **Implementar lógica de negócio complexa** usando múltiplos agentes
3. **Aplicar conceitos geográficos** em sistemas de informação
4. **Estruturar dados médicos** de forma eficiente
5. **Preparar-se para PostgreSQL real** com confiança na Aula 8

## 🚀 Aplicabilidade

Os conceitos desta aula são **diretamente aplicáveis** a:

- Sistemas de saúde reais
- E-commerce com geolocalização
- Sistemas de emergência
- Plataformas de recomendação
- Qualquer domínio que combine dados estruturados + IA
