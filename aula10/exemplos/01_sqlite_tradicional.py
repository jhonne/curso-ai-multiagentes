#!/usr/bin/env python3
"""
Exemplo 1: Busca SQL Tradicional

Demonstra busca usando SQL LIKE para comparação.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent.parent / "db" / "curso.db"


def buscar_sintomas_like(termo_busca: str):
    """Busca sintomas usando SQL LIKE"""
    print(f"\n🔍 Buscando: '{termo_busca}'")
    print("-" * 60)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Busca case-insensitive
    pattern = f"%{termo_busca}%"
    cursor.execute("""
        SELECT id, nome
        FROM ia_sintoma
        WHERE LOWER(nome) LIKE LOWER(?)
        ORDER BY nome
        LIMIT 10
    """, (pattern,))
    
    resultados = cursor.fetchall()
    conn.close()
    
    if resultados:
        print(f"✅ Encontrados {len(resultados)} resultado(s):\n")
        for idx, (sid, nome) in enumerate(resultados, 1):
            print(f"  {idx}. {nome} (ID: {sid})")
    else:
        print("❌ Nenhum resultado encontrado")
    
    return resultados


def demonstracao_limitacoes():
    """Demonstra limitações do SQL LIKE"""
    print("\n" + "=" * 80)
    print("🔬 DEMONSTRAÇÃO: LIMITAÇÕES DO SQL LIKE")
    print("=" * 80)
    
    exemplos = [
        ("dor", "Encontra tudo com 'dor'"),
        ("cefaleia", "Termo médico exato"),
        ("dor de cabeça", "Termo coloquial"),
        ("problemas respiratorios", "Termo amplo - poucos resultados"),
        ("febre alta", "Combinação de termos")
    ]
    
    for termo, descricao in exemplos:
        print(f"\n📌 {descricao}")
        resultados = buscar_sintomas_like(termo)
        
        # Análise
        print(f"\n💡 Análise:")
        if len(resultados) == 0:
            print("   ❌ SQL LIKE precisa de match exato na substring")
            print("   ❌ Não entende sinônimos ou contexto")
        elif len(resultados) > 20:
            print("   ⚠️  Muitos resultados - busca muito ampla")
        else:
            print("   ✅ Resultados encontrados, mas limitados ao termo exato")
        
        input("\n➡️  Pressione ENTER para próximo exemplo...")


def comparacao_termos():
    """Compara busca de termos médicos vs coloquiais"""
    print("\n" + "=" * 80)
    print("🏥 COMPARAÇÃO: TERMOS MÉDICOS vs COLOQUIAIS")
    print("=" * 80)
    
    pares = [
        ("cefaleia", "dor de cabeça"),
        ("dispneia", "falta de ar"),
        ("hipertermia", "febre"),
        ("náusea", "enjoo")
    ]
    
    for termo_medico, termo_coloquial in pares:
        print(f"\n📊 Comparando: '{termo_medico}' vs '{termo_coloquial}'")
        
        print(f"\n🏥 Termo médico: {termo_medico}")
        r1 = buscar_sintomas_like(termo_medico)
        
        print(f"\n💬 Termo coloquial: {termo_coloquial}")
        r2 = buscar_sintomas_like(termo_coloquial)
        
        print(f"\n📈 Resultado:")
        print(f"   Médico: {len(r1)} resultado(s)")
        print(f"   Coloquial: {len(r2)} resultado(s)")
        
        if len(r1) > 0 and len(r2) == 0:
            print(f"   ⚠️  SQL não conecta os dois termos!")
        
        input("\n➡️  Pressione ENTER para próximo par...")


if __name__ == "__main__":
    print("🎓 EXEMPLO 1: BUSCA SQL TRADICIONAL (LIKE)")
    print("=" * 80)
    
    # Verificar banco
    if not DB_PATH.exists():
        print(f"❌ Banco não encontrado: {DB_PATH}")
        exit(1)
    
    # Menu
    while True:
        print("\n📋 OPÇÕES:")
        print("1. Busca livre")
        print("2. Demonstração de limitações")
        print("3. Comparação médico vs coloquial")
        print("4. Sair")
        
        escolha = input("\n👉 Escolha: ").strip()
        
        if escolha == "1":
            termo = input("\n📝 Digite o termo de busca: ").strip()
            if termo:
                buscar_sintomas_like(termo)
        
        elif escolha == "2":
            demonstracao_limitacoes()
        
        elif escolha == "3":
            comparacao_termos()
        
        elif escolha == "4":
            print("\n👋 Até logo!")
            break
        
        else:
            print("\n❌ Opção inválida!")
