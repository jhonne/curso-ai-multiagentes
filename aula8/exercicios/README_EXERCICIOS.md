# 🎓 Exercícios Práticos - Aula 8

## 📋 Visão Geral dos Exercícios

A **Aula 8** inclui uma série de exercícios progressivos para praticar os conceitos de sistemas interativos com CrewAI e SQLite.

## 🎯 Objetivos dos Exercícios

- ✅ **Dominar consultas SQLite** através de agentes CrewAI
- ✅ **Criar interfaces interativas** amigáveis ao usuário
- ✅ **Implementar funcionalidades avançadas** como histórico e favoritos
- ✅ **Trabalhar com dados reais** de estabelecimentos de saúde
- ✅ **Desenvolver sistemas conversacionais** naturais

---

## 🟢 Exercício 1: Consultas Básicas

### 📁 Arquivo: `exercicio1_consultas_basicas.py`

**Objetivo:** Aprender fundamentos de consultas SQLite através de agentes CrewAI

### 🔧 Funcionalidades

- Busca por tipos específicos (UPAs, Hospitais, Postos)
- Estatísticas por bairro
- Análise de queixas mais frequentes
- Visão geral do sistema de saúde

### 🚀 Execução

```bash
uv run aula8/exercicios/exercicio1_consultas_basicas.py
```

### 📚 O que você aprende

- Como criar ferramentas CrewAI para SQLite
- Técnicas de consulta SQL básicas
- Interface de menu simples
- Formatação de resultados para usuário

### 💡 Conceitos Técnicos

```python
class ConsultaBasicaTool(BaseTool):
    name: str = "consulta_basica"
    description: str = "Executa consultas básicas no SQLite"
    
    def _run(self, tipo_consulta: str) -> str:
        # Lógica de consulta baseada no tipo solicitado
        if tipo_consulta == 'upas':
            return self._buscar_upas(cursor)
        # ... mais tipos
```

### 🎯 Exercícios Incluídos

#### 1.1 Buscar UPAs Específicas

- Filtra apenas Unidades de Pronto Atendimento
- Mostra endereços e contatos completos
- Lista organizada e formatada

#### 1.2 Listar Hospitais

- Busca hospitais na base de dados
- Informações de localização e contato
- Análise de distribuição geográfica

#### 1.3 Estatísticas por Bairro

- Ranking de bairros por número de estabelecimentos
- Cobertura de saúde por região
- Insights sobre distribuição de serviços

#### 1.4 Queixas Mais Frequentes

- Top 10 queixas no sistema
- Percentuais e análise estatística
- Padrões de saúde pública

---

## 🟡 Exercício 2: Interface Melhorada

### 📁 Arquivo: `exercicio2_interface_melhorada.py`

**Objetivo:** Implementar funcionalidades avançadas de interface e experiência do usuário

### 🔧 Funcionalidades Avançadas

- **Histórico de Sessão** - Rastreia todas as consultas realizadas
- **Sistema de Favoritos** - Permite salvar itens de interesse
- **Exportação de Dados** - Salva sessão em arquivo JSON
- **Interface Melhorada** - Comandos avançados e formatação

### 🚀 Execução

```bash
uv run aula8/exercicios/exercicio2_interface_melhorada.py
```

### 📚 O que você aprende

- Gerenciamento de estado de sessão
- Persistência de dados da sessão
- Comandos avançados de interface
- Exportação de resultados
- Sistema de favoritos

### 💡 Conceitos Técnicos

```python
class HistoricoSessao:
    def __init__(self):
        self.consultas = []
        self.favoritos = []
        self.sessao_inicio = datetime.now()
    
    def adicionar_consulta(self, pergunta, resposta):
        # Armazena consulta com timestamp
    
    def exportar_sessao(self):
        # Exporta dados da sessão para JSON
```

### 🎯 Funcionalidades Implementadas

#### 2.1 Histórico Inteligente

```bash
# Ver histórico da sessão
'historico' - Mostra todas as consultas realizadas

# Exemplo de saída:
📝 HISTÓRICO DA SESSÃO (iniciada em 14:30):
1. [14:32:15] Quantos hospitais existem?
   📋 Encontrados 247 hospitais no sistema...
2. [14:35:22] Mostre UPAs por bairro
   📋 Distribuição de UPAs: Centro (5), Dirceu (3)...
```

#### 2.2 Sistema de Favoritos

```bash
# Adicionar aos favoritos
'favoritar Hospital São Marcos' - Adiciona item aos favoritos

# Ver favoritos
'favoritos' - Lista todos os itens salvos

# Exemplo:
⭐ SEUS FAVORITOS (3):
1. Hospital São Marcos
2. UPA do Dirceu  
3. Relatório de distribuição por bairros
```

#### 2.3 Exportação Inteligente

```bash
# Exportar sessão completa
'exportar' - Salva tudo em arquivo JSON

# Resultado:
✅ Sessão exportada para: sessao_saude_20240126_143052.json
```

**Conteúdo do arquivo exportado:**

```json
{
  "sessao_inicio": "2024-01-26T14:30:52",
  "sessao_fim": "2024-01-26T15:15:30", 
  "total_consultas": 8,
  "consultas": [
    {
      "timestamp": "2024-01-26T14:32:15",
      "pergunta": "Quantos hospitais existem?",
      "resposta": "Encontrados 247 hospitais..."
    }
  ],
  "favoritos": ["Hospital São Marcos", "UPA do Dirceu"],
  "duracao_minutos": 45
}
```

#### 2.4 Consultas Avançadas

```bash
# Mapa de distribuição
'mapa centro' - Mostra estabelecimentos na região central

# Ranking de atendimentos  
'ranking' - Top estabelecimentos por volume de atendimento

# Relatório detalhado
'relatorio detalhado' - Análise completa do sistema

# Comparação entre regiões
'comparacao bairros' - Compara cobertura entre bairros
```

---

## 📊 Estrutura dos Dados (Banco SQLite)

### 🗄️ Tabelas Principais

```sql
-- Estabelecimentos de saúde
ia_estabelecimento
├── cnes (ID único)
├── nome (Nome do estabelecimento)  
├── endereco (Endereço completo)
├── bairro (Bairro/região)
├── fone (Telefone de contato)
├── longitude/latitude (Coordenadas geográficas)

-- Queixas principais
ia_queixa_principal
├── id (ID da queixa)
└── nome (Descrição da queixa)

-- Sintomas catalogados
ia_sintoma  
├── id (ID do sintoma)
└── nome (Descrição do sintoma)

-- Histórico de atendimentos
ia_historico_atendimento_sintoma
├── estabelecimento_cnes (Referência ao estabelecimento)
├── queixa_principal_id (Referência à queixa)  
└── sintoma_id (Referência ao sintoma)
```

### 📈 Exemplos de Dados Reais

**Estabelecimentos:**

- Hospital de Urgência de Teresina (HUT)
- UPA do Promorar
- UPA Sul  
- Hospital São Paulo
- Centro Médico do Piauí
- - 2.800 outros estabelecimentos

**Queixas Mais Frequentes:**

1. CEFALEIA (dor de cabeça) - 8,234 casos (6.57%)
2. FEBRE - 7,891 casos (6.29%)  
3. DOR ABDOMINAL - 6,547 casos (5.22%)
4. TOSSE - 5,234 casos (4.17%)
5. NÁUSEAS - 4,891 casos (3.90%)

---

## 🎓 Progressão de Aprendizado

### 📈 Nível de Dificuldade

```
🟢 Exercício 1: BÁSICO
├── Consultas SQL simples
├── Interface menu básica
├── Conceitos fundamentais CrewAI + SQLite
└── Formatação de resultados

🟡 Exercício 2: INTERMEDIÁRIO  
├── Gerenciamento de sessão
├── Funcionalidades avançadas de UI
├── Persistência de dados
├── Comandos complexos
└── Exportação estruturada
```

### 🚀 Sequência Recomendada

1. **Comece com Exercício 1** - Fundamentos sólidos
2. **Pratique cada sub-exercício** - Não pule etapas
3. **Modifique o código** - Experimente variações
4. **Avance para Exercício 2** - Funcionalidades avançadas
5. **Explore livremente** - Crie suas próprias consultas

---

## 💡 Dicas de Implementação

### 🔧 Para Exercício 1 (Básico)

```python
# Dica: Modificar tipos de consulta
def _buscar_clinicas(self, cursor):
    """Adicione busca por clínicas"""
    cursor.execute("""
        SELECT nome, bairro FROM ia_estabelecimento  
        WHERE nome LIKE '%Clínica%'
        ORDER BY nome
    """)
    # Processar resultados...

# Dica: Filtros por região
def _filtrar_por_regiao(self, cursor, regiao):
    """Filtrar estabelecimentos por região específica"""
    cursor.execute("""
        SELECT * FROM ia_estabelecimento
        WHERE bairro LIKE ?
    """, (f'%{regiao}%',))
```

### 🚀 Para Exercício 2 (Avançado)

```python
# Dica: Adicionar mais tipos de favoritos
def categorizar_favorito(self, item, categoria):
    """Categorizar favoritos por tipo"""
    self.favoritos_categorizados[categoria].append(item)

# Dica: Histórico com busca
def buscar_no_historico(self, termo):
    """Buscar consultas anteriores por termo"""
    return [c for c in self.consultas if termo in c['pergunta']]

# Dica: Exportar em múltiplos formatos
def exportar_csv(self):
    """Exportar dados em formato CSV"""
    import pandas as pd
    df = pd.DataFrame(self.consultas)
    return df.to_csv('sessao.csv')
```

---

## 🎯 Exercícios Extras (Desafios)

### 🔴 Desafio 1: Agente Especializado

Crie um terceiro exercício com agente especializado:

```python
# exercicio3_agente_especializado.py
class AgenteMedico(Agent):
    """Agente com conhecimento médico especializado"""
    
    def analisar_sintomas(self, sintomas):
        """Analisa correlação entre sintomas"""
        # Implementar lógica de correlação
        
    def recomendar_estabelecimento(self, urgencia):
        """Recomenda tipo de estabelecimento por urgência"""
        # Lógica de triagem médica
```

### 🔴 Desafio 2: API REST  

Transforme o sistema em API REST:

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/consulta', methods=['POST'])
def consulta_api():
    dados = request.json
    resultado = agente.processar(dados['pergunta'])
    return jsonify({'resposta': resultado})
```

### 🔴 Desafio 3: Interface Web

Crie interface web com Streamlit:

```python
import streamlit as st

st.title("🏥 Sistema de Saúde CrewAI")
pergunta = st.text_input("Sua consulta:")
if pergunta:
    resposta = agente.processar(pergunta)
    st.write(resposta)
```

---

## 📚 Recursos de Apoio

### 📖 Documentação

- [SQLite Python](https://docs.python.org/3/library/sqlite3.html)
- [CrewAI Tools](https://docs.crewai.com/tools)
- [Langchain OpenAI](https://python.langchain.com/docs/integrations/llms/openai)

### 🔗 Arquivos Relacionados

- `../main.py` - Sistema principal da aula 8  
- `../../db/curso.db` - Banco de dados SQLite
- `../README.md` - Documentação completa da aula

### 💬 Suporte

- **Discord do curso** - Dúvidas e discussões
- **GitHub Issues** - Problemas técnicos  
- **Documentação local** - Pasta `/docs/`

---

## ✅ Checklist de Conclusão

### 📋 Ao completar os exercícios, você deve saber

**Exercício 1 Concluído:**

- [ ] Executar consultas básicas no SQLite
- [ ] Criar ferramentas CrewAI personalizadas  
- [ ] Implementar menu de opções simples
- [ ] Formatar resultados para usuário
- [ ] Trabalhar com dados reais de saúde

**Exercício 2 Concluído:**

- [ ] Gerenciar histórico de sessão
- [ ] Implementar sistema de favoritos
- [ ] Exportar dados em formato JSON
- [ ] Criar interface avançada com comandos
- [ ] Desenvolver consultas personalizadas

**Conhecimentos Gerais:**

- [ ] Diferenças entre SQLite e PostgreSQL
- [ ] Vantagens de sistemas interativos
- [ ] Padrões de interface conversacional  
- [ ] Estruturação de dados de saúde
- [ ] Integração CrewAI com bancos de dados

---

**🎯 Parabéns!** Ao completar estes exercícios, você terá dominado os conceitos fundamentais de sistemas interativos com CrewAI e SQLite, preparando-se para desafios mais avançados nas próximas aulas!

**🚀 Próximo Passo:** Aula 9 - Múltiplos agentes especializados trabalhando em colaboração!
