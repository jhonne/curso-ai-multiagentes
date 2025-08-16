"""
Configurador Automático para CrewAI + OpenAI
Este script ajuda a configurar o ambiente automaticamente
"""

import os
import sys
import subprocess
from pathlib import Path


def verificar_python():
    """Verifica a versão do Python"""
    print("🐍 Verificando Python...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"❌ Python {version.major}.{version.minor} detectado")
        print("💡 É necessário Python 3.10 ou superior para CrewAI")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def instalar_dependencias():
    """Instala as dependências necessárias"""
    print("\n📦 Instalando dependências...")
    
    packages = [
        "crewai>=0.95.0",
        "openai>=1.12.0", 
        "python-dotenv>=1.0.0"
    ]
    
    for package in packages:
        try:
            print(f"   Instalando {package}...")
            subprocess.run([
                sys.executable, "-m", "pip", "install", package
            ], check=True, capture_output=True, text=True)
            print(f"   ✅ {package}")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Erro ao instalar {package}: {e}")
            return False
    
    print("✅ Todas as dependências instaladas!")
    return True


def configurar_env():
    """Configura o arquivo .env"""
    print("\n⚙️ Configurando arquivo .env...")
    
    env_path = Path(".env")
    
    if env_path.exists():
        print("ℹ️  Arquivo .env já existe")
        resposta = input("Deseja recriar? (s/N): ").lower()
        if resposta not in ['s', 'sim', 'y', 'yes']:
            return True
    
    # Solicitar chave da OpenAI
    print("\n🔑 Configuração da chave OpenAI:")
    print("   1. Acesse: https://platform.openai.com/api-keys")
    print("   2. Crie uma nova chave API")
    print("   3. Cole a chave abaixo")
    
    while True:
        api_key = input("\nCole sua chave OpenAI (sk-...): ").strip()
        
        if not api_key:
            print("❌ Chave não pode estar vazia!")
            continue
            
        if not api_key.startswith("sk-"):
            print("⚠️  Chave deve começar com 'sk-'. Continuar mesmo assim? (s/N)")
            if input().lower() not in ['s', 'sim', 'y', 'yes']:
                continue
        
        break
    
    # Escolher modelo
    print("\n🤖 Escolha o modelo:")
    print("   1. gpt-3.5-turbo (mais barato)")
    print("   2. gpt-4 (mais avançado)")
    print("   3. gpt-4-turbo")
    
    modelos = {
        "1": "gpt-3.5-turbo",
        "2": "gpt-4", 
        "3": "gpt-4-turbo"
    }
    
    while True:
        escolha = input("Escolha (1-3): ").strip()
        if escolha in modelos:
            modelo = modelos[escolha]
            break
        print("❌ Escolha inválida!")
    
    # Criar arquivo .env
    conteudo_env = f"""# Configuração OpenAI para CrewAI
OPENAI_API_KEY={api_key}
OPENAI_MODEL_NAME={modelo}
OPENAI_TEMPERATURE=0.7
"""
    
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(conteudo_env)
        print("✅ Arquivo .env criado com sucesso!")
        return True
    except Exception as e:
        print(f"❌ Erro ao criar .env: {e}")
        return False


def testar_configuracao():
    """Testa se tudo está funcionando"""
    print("\n🧪 Testando configuração...")
    
    try:
        # Importar e testar
        from dotenv import load_dotenv
        from openai import OpenAI
        
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ OPENAI_API_KEY não encontrada no .env")
            return False
        
        client = OpenAI(api_key=api_key)
        
        # Teste básico
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo"),
            messages=[{"role": "user", "content": "Diga: Configuração OK!"}],
            max_tokens=20
        )
        
        resposta = response.choices[0].message.content
        print(f"✅ Teste bem-sucedido: {resposta}")
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False


def main():
    """Função principal do configurador"""
    print("=" * 50)
    print("🚀 CONFIGURADOR AUTOMÁTICO CREWAI + OPENAI")
    print("=" * 50)
    
    # Verificações e configurações sequenciais
    if not verificar_python():
        return False
    
    if not instalar_dependencias():
        return False
    
    if not configurar_env():
        return False
    
    if not testar_configuracao():
        return False
    
    # Sucesso!
    print("\n" + "=" * 50)
    print("🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 50)
    print("\n📝 Próximos passos:")
    print("   1. python teste_api.py      # Teste rápido")
    print("   2. python hello_simples.py  # Primeiro exemplo")
    print("   3. python hello_crewai.py   # Exemplo completo")
    print("\n🔗 Recursos úteis:")
    print("   • Documentação: https://docs.crewai.com/")
    print("   • OpenAI Usage: https://platform.openai.com/usage")
    
    return True


if __name__ == "__main__":
    try:
        sucesso = main()
        sys.exit(0 if sucesso else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Configuração cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)