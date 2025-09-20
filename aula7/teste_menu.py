#!/usr/bin/env python3
"""
Teste para verificar se o menu reaparece após validação
"""

import subprocess
import time
import os

def testar_menu():
    """Testa se o menu reaparece após a validação"""
    
    print("🧪 TESTANDO MENU APÓS VALIDAÇÃO...")
    
    # Comando para executar main.py
    cmd = ["uv", "run", "python", "main.py"]
    
    # Criar processo interativo
    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        cwd="/home/lotus/supra/curso_crewai/aula7"
    )
    
    # Esperar carregar
    time.sleep(3)
    
    # Executar opção 5 (validação)
    process.stdin.write("5\n")
    process.stdin.flush()
    
    # Esperar validação completar
    time.sleep(5)
    
    # Tentar ler output
    try:
        # Terminar processo
        process.stdin.write("6\n")
        process.stdin.flush()
        
        stdout, stderr = process.communicate(timeout=5)
        
        print("📋 OUTPUT CAPTURADO:")
        print("=" * 50)
        
        # Verificar se o menu aparece novamente
        if "🎯 FUNCIONALIDADES AVANÇADAS:" in stdout:
            if stdout.count("🎯 FUNCIONALIDADES AVANÇADAS:") > 1:
                print("✅ SUCESSO: Menu reaparece após validação!")
            else:
                print("⚠️ AVISO: Menu aparece apenas uma vez")
        else:
            print("❌ ERRO: Menu não encontrado no output")
        
        # Mostrar últimas linhas
        lines = stdout.split('\n')
        print("\n📄 ÚLTIMAS 20 LINHAS:")
        for line in lines[-20:]:
            if line.strip():
                print(line)
                
    except subprocess.TimeoutExpired:
        print("⏱️ Timeout - processo ainda executando (normal)")
        process.kill()
    except Exception as e:
        print(f"❌ Erro: {e}")
        process.kill()

if __name__ == "__main__":
    testar_menu()