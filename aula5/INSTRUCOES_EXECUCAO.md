# 🚀 Instruções de Execução - Aula 5

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter:

```bash
# Instalar dependências
pip install crewai openai python-dotenv pytest

# Configurar variável de ambiente
export OPENAI_API_KEY="sua_chave_aqui"
# No Windows PowerShell:
$env:OPENAI_API_KEY="sua_chave_aqui"
```

## 🎯 Ordem de Execução Recomendada

### 1. Arquivo Principal

```bash
python main.py
```

- Visão geral dos conceitos da aula
- Exemplos introdutórios de otimização

### 2. Exemplos Práticos (em ordem)

```bash
# Técnicas avançadas de prompts
python exemplos/01_prompt_engineering.py

# Configuração de modelos OpenAI
python exemplos/02_configuracao_modelos.py

# Testes unitários para agentes
python exemplos/03_testes_agentes.py

# Sistema de monitoramento
python exemplos/04_monitoramento.py
```

### 3. Templates (para estudo e reutilização)

```bash
# Template de agente otimizado
python templates/agente_otimizado.py

# Suite completa de testes
python templates/suite_testes.py

# Apenas testes rápidos
python templates/suite_testes.py rapido
```

### 4. Exercícios Práticos

```bash
# Exercício 1: Prompt Engineering
python exercicios/exercicio1_prompts.py

# Exercício 2: Configuração de Modelos
python exercicios/exercicio2_config.py

# Exercício 3: Testes e Monitoramento
python exercicios/exercicio3_testes.py
```

## 🔧 Executando com Pytest

Para executar testes unitários:

```bash
# Testes dos exercícios
pytest exercicios/exercicio3_testes.py -v

# Testes dos templates
pytest templates/suite_testes.py -v
```

## 📊 Monitoramento de Custos

Monitore seus gastos executando:

```bash
python exemplos/04_monitoramento.py
```

Este script mostra:

- Uso de tokens por agente
- Custo estimado das execuções
- Métricas de performance
- Alertas de problemas

## 🎓 Completando os Exercícios

### Exercício 1 - Prompt Engineering

1. Abra `exercicios/exercicio1_prompts.py`
2. Complete as funções marcadas com `# TODO:`
3. Execute para ver suas implementações
4. Compare com as soluções (descomente as funções de solução)

### Exercício 2 - Configuração

1. Abra `exercicios/exercicio2_config.py`
2. Configure agentes para diferentes cenários
3. Implemente sistema de fallback
4. Compare custos entre modelos

### Exercício 3 - Testes

1. Abra `exercicios/exercicio3_testes.py`
2. Complete a classe `ExercicioTestes`
3. Implemente sistema de monitoramento
4. Execute os testes: `python exercicios/exercicio3_testes.py`

## 💡 Dicas Importantes

### Performance

- Use `verbose=False` para execuções mais rápidas
- Monitore sempre o uso de tokens
- Implemente cache para prompts repetitivos

### Debugging

- Use `verbose=True` durante desenvolvimento
- Monitore logs de erro nos alertas
- Teste agentes individualmente antes da integração

### Custos

- GPT-3.5-turbo: ~$0.002 por 1K tokens
- GPT-4: ~$0.06 por 1K tokens  
- Use GPT-3.5 para desenvolvimento e testes

## 🚨 Troubleshooting

### Erro de API Key

```bash
# Verifique se a chave está configurada
echo $OPENAI_API_KEY  # Linux/Mac
echo $env:OPENAI_API_KEY  # Windows PowerShell
```

### Erro de Rate Limit

- Aguarde alguns segundos entre execuções
- Use configurações de fallback
- Considere usar temperature mais baixa

### Erro de Importação

```bash
# Reinstale as dependências
pip install --upgrade crewai openai python-dotenv
```

## 📈 Próximos Passos

Após completar a Aula 5:

1. ✅ Pratique otimização de prompts
2. ✅ Configure diferentes tipos de agentes  
3. ✅ Implemente testes robustos
4. ✅ Monitor sistema em produção
5. 🎯 **Próxima aula**: Orquestração e integração (Aula 6)

## 🔗 Recursos Úteis

- [Documentação CrewAI](https://docs.crewai.com/)
- [OpenAI API Reference](https://platform.openai.com/docs/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Python Testing with pytest](https://docs.pytest.org/)

---

**💪 Boa prática! Lembre-se: a otimização é um processo iterativo. Teste, monitore, ajuste e repita!**
