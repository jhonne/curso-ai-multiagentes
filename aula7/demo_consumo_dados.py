"""
Demonstração: Como o Agente Consome Dados Estruturados
======================================================

Este exemplo mostra exatamente como os dados do banco são transformados
em contexto textual que o agente CrewAI pode processar.

Execute: uv run aula7/demo_consumo_dados.py
"""

from dados_simulados import dados_medicos
import json


def demonstrar_transformacao_dados():
    """Mostra como dados estruturados viram contexto para o agente"""
    
    print("🔄 DEMONSTRAÇÃO: TRANSFORMAÇÃO DE DADOS ESTRUTURADOS")
    print("="*65)
    
    # Simular entrada do usuário
    sintomas_usuario = "dor no peito intensa, falta de ar, sudorese fria"
    lat_paciente = -5.0892  # Centro de Teresina
    lng_paciente = -42.8019
    
    print(f"👤 ENTRADA DO USUÁRIO:")
    print(f"   🩺 Sintomas: '{sintomas_usuario}'")
    print(f"   📍 Localização: ({lat_paciente}, {lng_paciente})")
    
    print(f"\n" + "="*65)
    print(f"📊 ETAPA 1: CONSULTAS AO BANCO DE DADOS")
    print("="*65)
    
    # 1. Análise de sintomas (consulta ao banco)
    print("🔍 1.1. Análise de Sintomas:")
    analise_sintomas = dados_medicos.classificar_urgencia_sintomas(sintomas_usuario)
    
    print(f"   📋 Dados brutos do banco:")
    print(f"   {json.dumps(analise_sintomas, indent=6, ensure_ascii=False)}")
    
    # 2. Busca geográfica (consulta ao banco)
    print(f"\n🌍 1.2. Busca Geográfica:")
    estabelecimentos = dados_medicos.buscar_estabelecimentos_proximos(
        lat_paciente, lng_paciente, raio_km=5
    )
    
    print(f"   🏥 Dados brutos do banco (primeiros 2):")
    for i, est in enumerate(estabelecimentos[:2], 1):
        print(f"   Estabelecimento {i}:")
        print(f"   {json.dumps(dict(est), indent=6, ensure_ascii=False)}")
    
    print(f"\n" + "="*65)
    print(f"🔄 ETAPA 2: TRANSFORMAÇÃO PARA CONTEXTO TEXTUAL")
    print("="*65)
    
    # Transformar análise de sintomas
    print("📝 2.1. Formatação da Análise de Sintomas:")
    
    contexto_sintomas = f"""
ANÁLISE DE SINTOMAS PROCESSADA:
• Texto analisado: "{sintomas_usuario}"
• Nível de urgência detectado: {analise_sintomas['nivel_urgencia']}/5
• Classificação: {analise_sintomas['classificacao']}
• Recomendação automática: {analise_sintomas['recomendacao']}
• Sintomas específicos encontrados: {len(analise_sintomas['sintomas_encontrados'])} sintoma(s)
"""
    
    if analise_sintomas['sintomas_encontrados']:
        contexto_sintomas += "\n• Detalhamento dos sintomas:\n"
        for sintoma in analise_sintomas['sintomas_encontrados']:
            contexto_sintomas += f"  - {sintoma['nome']} (criticidade: {sintoma['criticidade']}/5)\n"
    
    print(contexto_sintomas)
    
    # Transformar dados geográficos
    print("📍 2.2. Formatação dos Dados Geográficos:")
    
    contexto_geografico = f"""
ESTABELECIMENTOS DE SAÚDE PRÓXIMOS:
• Localização de referência: Latitude {lat_paciente}, Longitude {lng_paciente}
• Raio de busca: 5km
• Total encontrado: {len(estabelecimentos)} estabelecimento(s)

LISTA DE ESTABELECIMENTOS DISPONÍVEIS:
"""
    
    for i, est in enumerate(estabelecimentos, 1):
        emoji_tipo = {"HOSPITAL": "🏥", "UPA": "🚑", "UBS": "⚕️"}.get(est['tipo'], "🏢")
        contexto_geografico += f"""
{i}. {emoji_tipo} {est['nome']}
   • Tipo: {est['tipo']}
   • Distância: {est['distancia_km']}km
   • Telefone: {est['telefone']}
   • Horário: {est['horario_funcionamento']}
   • Município: {est['municipio']}
"""
    
    print(contexto_geografico)
    
    print(f"\n" + "="*65)
    print(f"🤖 ETAPA 3: CONTEXTO FINAL PARA O AGENTE")
    print("="*65)
    
    # Este é exatamente o contexto que o agente CrewAI recebe
    contexto_final = f"""
TRIAGEM MÉDICA COMPLETA - DADOS PRÉ-PROCESSADOS

CASO DO PACIENTE:
• Sintomas relatados: "{sintomas_usuario}"
• Localização: Latitude {lat_paciente}, Longitude {lng_paciente}

{contexto_sintomas}

{contexto_geografico}

INSTRUÇÕES PARA ANÁLISE:
1. Com base nos dados de sintomas pré-processados, valide ou ajuste a classificação de urgência
2. Considerando a urgência e os estabelecimentos disponíveis, faça sua recomendação
3. Priorize proximidade para casos urgentes
4. Inclua informações práticas (telefone, horário)
5. Forneça orientações claras sobre próximos passos
"""
    
    print("📋 CONTEXTO COMPLETO QUE O AGENTE RECEBE:")
    print("-" * 50)
    print(contexto_final)
    print("-" * 50)
    
    print(f"\n" + "="*65)
    print(f"💡 RESUMO DO PROCESSO")
    print("="*65)
    
    print(f"""
FLUXO DE CONSUMO DE DADOS:

1️⃣ DADOS ESTRUTURADOS (Banco SQLite):
   • Tabelas relacionais com dados médicos
   • Consultas SQL tradicionais
   • Resultados em formato Python (dict/list)

2️⃣ PROCESSAMENTO PYTHON:
   • Cálculos de distância (fórmula Haversine)
   • Classificação de urgência (algoritmo Python)
   • Filtros e ordenação de dados

3️⃣ FORMATAÇÃO TEXTUAL:
   • Conversão de dados estruturados para texto
   • Template de contexto para o agente
   • Instruções específicas incluídas

4️⃣ CONSUMO PELO AGENTE:
   • Agente recebe contexto via Task.description
   • Processa texto usando capacidades do LLM
   • Gera recomendação baseada no contexto fornecido

VANTAGENS DESTE MODELO:
✅ Controle total sobre os dados fornecidos ao agente
✅ Processamento otimizado antes da análise de IA
✅ Debug fácil - pode inspecionar cada etapa
✅ Segurança - agente não tem acesso direto ao banco
✅ Performance - dados pré-processados e filtrados
""")


def comparar_com_acesso_direto():
    """Compara modelo atual com acesso direto ao banco"""
    
    print(f"\n" + "🔍 COMPARAÇÃO: ACESSO INDIRETO vs DIRETO")
    print("="*55)
    
    print("""
❌ ACESSO DIRETO (NÃO usado na aula):
┌─────────────────────────────────────────────────────┐
│ Agente CrewAI                                       │
│   ↓ (faz query SQL diretamente)                    │
│ Banco de Dados                                      │
│   ↓ (retorna dados brutos)                         │
│ Agente interpreta dados SQL                         │
└─────────────────────────────────────────────────────┘

Problemas:
• Agente precisa saber SQL
• Sem controle sobre queries
• Difícil debug
• Possível segurança comprometida
• Performance não otimizada

✅ ACESSO INDIRETO (usado na aula):
┌─────────────────────────────────────────────────────┐
│ Python Application                                  │
│   ↓ (faz queries otimizadas)                      │
│ Banco de Dados                                      │
│   ↓ (dados processados em Python)                 │
│ Formatação para Contexto Textual                   │
│   ↓ (contexto estruturado)                        │
│ Agente CrewAI                                       │
└─────────────────────────────────────────────────────┘

Vantagens:
• Python controla todas as queries
• Processamento otimizado
• Debug em cada etapa
• Segurança garantida
• Agente foca na interpretação
""")


def exemplo_contexto_real():
    """Mostra um exemplo real de contexto que o agente recebe"""
    
    print(f"\n📝 EXEMPLO REAL: CONTEXTO DO AGENTE")
    print("="*45)
    
    # Dados reais que seriam enviados para o agente
    exemplo_contexto = """
TRIAGEM MÉDICA COMPLETA

SINTOMAS RELATADOS: "dor no peito intensa, falta de ar, sudorese fria"
LOCALIZAÇÃO DO PACIENTE: Latitude -5.0892, Longitude -42.8019

DADOS PRÉ-PROCESSADOS DISPONÍVEIS:
- Nível de urgência detectado automaticamente: 2/5
- Classificação inicial: LEVE
- Sintomas identificados: 1 sintoma(s)
- Sintoma específico: SUDORESE (criticidade: 2/5)

ESTABELECIMENTOS PRÓXIMOS:
• Hospital de Urgência de Teresina (HOSPITAL) - 0.0km - (86) 3216-1000
• UBS Centro (UBS) - 0.46km - (86) 3215-8100
• UBS Vila Operária (UBS) - 1.36km - (86) 3215-8000
• Hospital São Marcos (HOSPITAL) - 1.57km - (86) 3216-2000
• UPA Promorar (UPA) - 3.28km - (86) 3215-7800

EXECUTE ANÁLISE COMPLETA:
1. ANÁLISE CLÍNICA:
   • Interprete os sintomas relatados
   • Valide ou ajuste a classificação de urgência automática
   • Identifique sinais de alerta ou padrões críticos
   • Determine tipo de atendimento necessário

2. RECOMENDAÇÃO GEOGRÁFICA:
   • Com base na urgência, selecione estabelecimentos adequados
   • Priorize proximidade para casos urgentes
   • Para urgência 4-5: recomendar Hospital ou SAMU
   • Para urgência 2-3: recomendar UPA
   • Para urgência 1: recomendar UBS

3. ORIENTAÇÃO FINAL:
   • Forneça orientação clara e específica
   • Inclua próximos passos práticos
   • Adicione informações de contato
"""
    
    print("📋 CONTEXTO ENVIADO PARA O AGENTE:")
    print("-" * 45)
    print(exemplo_contexto)
    print("-" * 45)
    
    print(f"\n🎯 O QUE O AGENTE FAZ COM ESSE CONTEXTO:")
    print("""
1. 🧠 INTERPRETA o contexto usando capacidades do LLM
2. 🔍 ANALISA contradições (ex: "dor no peito" vs classificação "LEVE")
3. 🩺 APLICA conhecimento médico para reclassificar urgência
4. 📍 SELECIONA estabelecimentos adequados baseado na nova urgência
5. 💬 GERA resposta em linguagem natural para o paciente
""")


def main():
    """Executa todas as demonstrações"""
    
    print("🎓 AULA 7 - COMO O AGENTE CONSOME DADOS ESTRUTURADOS")
    print("="*65)
    print("Demonstração completa do fluxo de consumo de dados")
    
    demonstrar_transformacao_dados()
    comparar_com_acesso_direto()
    exemplo_contexto_real()
    
    print(f"\n🏆 CONCLUSÃO:")
    print("="*15)
    print("""
O agente CrewAI na Aula 7 consome dados estruturados através de:

1. 📊 CONTEXTUALIZAÇÃO: Dados do banco viram contexto textual estruturado
2. 🎯 INTERPRETAÇÃO: Agente usa LLM para interpretar contexto fornecido  
3. 🧠 RACIOCÍNIO: Aplica conhecimento médico aos dados pré-processados
4. 💬 GERAÇÃO: Produz recomendações em linguagem natural

Este modelo prepara os alunos para entender como integrar IA com dados
estruturados de forma controlada e eficiente.
""")


if __name__ == "__main__":
    main()