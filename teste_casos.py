#!/usr/bin/env python3
from aula7.dados_medicos_reais import dados_medicos

casos = [
    ('Emergência Cardiológica', 'dor forte no peito irradiando para braço esquerdo, suor frio, falta de ar', 5),
    ('Quadro Infeccioso', 'febre há 3 dias, dor de cabeça, mal estar geral', 3),
    ('Consulta Preventiva', 'check-up de rotina, sem sintomas específicos', 1),
]

print('🎯 TESTE DOS CASOS AJUSTADOS:')
for nome, sintomas, esperado in casos:
    resultado = dados_medicos.classificar_urgencia_inteligente(sintomas)
    urgencia = resultado['nivel_urgencia']
    
    status = '✅' if urgencia <= esperado + 1 and urgencia >= esperado - 1 else '❌'
    print(f'{status} {nome}: {urgencia}/5 (esperado: ~{esperado})')
    if resultado['padroes_criticos']:
        print(f'   Padrões: {resultado["padroes_criticos"]}')