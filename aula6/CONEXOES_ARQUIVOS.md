# 🔗 Como os Arquivos da Aula 6 Estão Conectados

## 📊 **Hierarquia de Dependências:**

```
📁 aula6/
├── 🎯 main.py                    # ARQUIVO PRINCIPAL
│   └── imports: orquestrador
│
├── 🎭 orquestrador.py           # COORDENADOR CENTRAL
│   ├── imports: agentes
│   └── imports: tarefas
│
├── 🤖 agentes.py                # DEFINIÇÕES DOS AGENTES
│   └── imports: crewai.Agent
│
├── 📋 tarefas.py                # DEFINIÇÕES DAS TAREFAS
│   └── imports: crewai.Task
│
├── 🟢 exemplo_basico.py         # EXEMPLO INDEPENDENTE
│   └── imports: crewai (tudo interno)
│
├── 💬 chatbot_simples.py        # EXEMPLO INDEPENDENTE
│   └── imports: crewai (tudo interno)
│
└── 🔧 verificar_configuracao.py # UTILITÁRIO DE TESTE
    ├── imports: agentes
    ├── imports: tarefas
    └── imports: orquestrador
```

---

## 🔄 **Fluxo de Conexões:**

### **1. Sistema Completo (main.py):**

```python
# main.py - Arquivo Principal
from orquestrador import OrquestradorChatbot

# Usa o orquestrador para coordenar tudo
orquestrador = OrquestradorChatbot()
resposta = orquestrador.processar_mensagem(mensagem)
```

### **2. Orquestrador (orquestrador.py):**

```python
# orquestrador.py - Coordenador Central  
from agentes import criar_todos_agentes
from tarefas import criar_tarefas_completas

class OrquestradorChatbot:
    def __init__(self):
        self.agentes = criar_todos_agentes()  # Pega agentes de agentes.py
    
    def processar_mensagem(self, mensagem):
        tarefas = criar_tarefas_completas(mensagem, self.agentes)  # Pega tarefas de tarefas.py
```

### **3. Agentes (agentes.py):**

```python
# agentes.py - Definições dos Agentes
from crewai import Agent

def criar_todos_agentes():
    return {
        "triagem": criar_agente_triagem(),
        "intencao": criar_agente_intencao(), 
        "busca": criar_agente_busca(),
        "resposta": criar_agente_resposta()
    }
```

### **4. Tarefas (tarefas.py):**

```python
# tarefas.py - Definições das Tarefas
from crewai import Task

def criar_tarefas_completas(mensagem, agentes):
    # Cria tarefas que usam os agentes e se conectam via context=[]
    return [tarefa_triagem, tarefa_intencao, tarefa_busca, tarefa_resposta]
```

---

## 🎯 **Arquivos Independentes:**

### **📚 Exemplos Didáticos:**

- **`exemplo_basico.py`** - Sistema simples auto-contido (3 agentes internos)
- **`chatbot_simples.py`** - Versão didática interativa (agentes internos)

### **🔧 Utilitários:**

- **`verificar_configuracao.py`** - Testa se todos os módulos funcionam
- **`README.md`** - Documentação
- **`EXERCICIOS.md`** - Exercícios práticos

---

## 🔀 **Fluxo de Dados Entre Arquivos:**

```
1. main.py → chama → orquestrador.py
2. orquestrador.py → importa → agentes.py + tarefas.py  
3. agentes.py → define → 4 agentes especializados
4. tarefas.py → cria → tarefas que conectam os agentes
5. orquestrador.py → coordena → execução do Crew
6. main.py → recebe → resposta final
```

---

## 💡 **Vantagens desta Estrutura:**

### ✅ **Modularidade:**

- Cada arquivo tem uma responsabilidade específica
- Fácil de modificar partes isoladamente
- Código reutilizável

### ✅ **Progressão Didática:**

- `exemplo_basico.py` → conceitos básicos
- `chatbot_simples.py` → interação
- `main.py` → sistema completo

### ✅ **Testabilidade:**

- `verificar_configuracao.py` testa todos os módulos
- Cada arquivo pode ser testado independentemente

---

## 🎓 **Para o Aluno:**

### **Sequência de Estudo Recomendada:**

1. **`README.md`** - Entender conceitos
2. **`exemplo_basico.py`** - Executar exemplo simples  
3. **`agentes.py`** - Ver definições dos agentes
4. **`tarefas.py`** - Ver como tarefas se conectam
5. **`orquestrador.py`** - Entender coordenação
6. **`main.py`** - Sistema completo

### **Como Executar (a partir da raiz do projeto):**

```bash
# Teste básico
uv run aula6/exemplo_basico.py

# Sistema interativo
uv run aula6/chatbot_simples.py

# Sistema completo
uv run aula6/main.py

# Verificar se tudo funciona
uv run aula6/verificar_configuracao.py
```

---

## 🔧 **Arquitetura Técnica:**

### **Padrão de Design Utilizado:**

1. **Separação de Responsabilidades:**
   - `agentes.py` → Criação de agentes
   - `tarefas.py` → Definição de tarefas
   - `orquestrador.py` → Coordenação
   - `main.py` → Interface principal

2. **Dependency Injection:**
   - Agentes são criados uma vez e reutilizados
   - Tarefas recebem agentes como parâmetro
   - Orquestrador coordena tudo

3. **Factory Pattern:**
   - Funções `criar_*` para instanciar objetos
   - Facilita modificação e teste
   - Padroniza criação de componentes

### **Fluxo de Execução Detalhado:**

```
Usuario Input
     ↓
main.py (interface)
     ↓
orquestrador.py (coordenação)
     ↓
agentes.py (criação dos agentes)
     ↓
tarefas.py (definição das tarefas)
     ↓
CrewAI (execução)
     ↓
Resultado Final
```

---

## 🚀 **Benefícios desta Arquitetura:**

1. **Facilidade de Manutenção:** Cada arquivo tem uma função clara
2. **Reutilização de Código:** Agentes e tarefas podem ser usados em outros contextos
3. **Facilidade de Teste:** Cada componente pode ser testado isoladamente
4. **Escalabilidade:** Novos agentes ou tarefas podem ser adicionados facilmente
5. **Aprendizado Progressivo:** Permite estudar cada conceito separadamente

Esta estrutura permite aprender **progressivamente** e **modificar componentes específicos** sem quebrar o sistema todo! 🚀

---

**📝 Nota:** Este documento serve como guia de referência para entender a arquitetura e conexões entre os arquivos da Aula 6. Use-o junto com os exemplos práticos para uma compreensão completa do sistema.
