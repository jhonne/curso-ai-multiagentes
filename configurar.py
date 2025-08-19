"""
Configurador Automático para CrewAI + OpenAI com UV
Este script ajuda a configurar o ambiente automaticamente usando UV
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def verificar_uv():
    """Verifica se UV está instalado"""
    print("🔍 Verificando UV...")
    
    if not shutil.which("uv"):
        print("❌ UV não encontrado!")
        print("💡 Instale o UV primeiro:")
        print("   Windows: powershell -c \"irm https://astral.sh/uv/install.ps1 | iex\"")
        print("   Linux/Mac: curl -LsSf https://astral.sh/uv/install.sh | sh")
        return False
    
    try:
        result = subprocess.run(
            ["uv", "--version"], 
            capture_output=True, 
            text=True, 
            check=True
        )
        version = result.stdout.strip()
        print(f"✅ UV {version}")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao verificar versão do UV")
        return False


def verificar_python():
    """Verifica a versão do Python"""
    print("\n🐍 Verificando Python...")
    version = sys.version_info
    
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print(f"❌ Python {version.major}.{version.minor} detectado")
        print("💡 É necessário Python 3.10 ou superior para CrewAI")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def inicializar_projeto():
    """Inicializa o projeto com UV"""
    print("\n📦 Inicializando projeto com UV...")
    
    # Verificar se já existe pyproject.toml
    if Path("pyproject.toml").exists():
        print("ℹ️  Projeto já inicializado (pyproject.toml encontrado)")
        return True
    
    try:
        subprocess.run(
            ["uv", "init", "--no-readme"], 
            check=True,
            capture_output=True
        )
        print("✅ Projeto inicializado com UV")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao inicializar projeto: {e}")
        return False


def instalar_dependencias():
    """Instala as dependências necessárias com UV"""
    print("\n📦 Instalando dependências com UV...")
    
    packages = [
        "crewai>=0.95.0",
        "openai>=1.12.0", 
        "python-dotenv>=1.0.0"
    ]
    
    for package in packages:
        try:
            print(f"   Adicionando {package}...")
            subprocess.run([
                "uv", "add", package
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
            print("⚠️  Chave deve começar com 'sk-'. Continuar? (s/N)")
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
    """Testa se tudo está funcionando com UV"""
    print("\n🧪 Testando configuração com UV...")
    
    try:
        # Testar com UV run
        result = subprocess.run([
            "uv", "run", "python", "-c", 
            """
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError('OPENAI_API_KEY não encontrada')

client = OpenAI(api_key=api_key)
response = client.chat.completions.create(
    model=os.getenv('OPENAI_MODEL_NAME', 'gpt-3.5-turbo'),
    messages=[{'role': 'user', 'content': 'Diga: Configuração UV OK!'}],
    max_tokens=20
)
print(f'Resposta: {response.choices[0].message.content}')
            """
        ], capture_output=True, text=True, check=True)
        
        print(f"✅ Teste bem-sucedido: {result.stdout.strip()}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro no teste: {e}")
        if e.stderr:
            print(f"Detalhes: {e.stderr}")
        return False


def main():
    """Função principal do configurador"""
    print("=" * 60)
    print("🚀 CONFIGURADOR AUTOMÁTICO CREWAI + OPENAI + UV")
    print("=" * 60)
    
    # Verificações e configurações sequenciais
    if not verificar_uv():
        return False
    
    if not verificar_python():
        return False
    
    if not inicializar_projeto():
        return False
    
    if not instalar_dependencias():
        return False
    
    if not configurar_env():
        return False
    
    if not testar_configuracao():
        return False
    
    # Sucesso!
    print("\n" + "=" * 60)
    print("🎉 CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print("\n📝 Comandos disponíveis com UV:")
    print("   uv run teste-api           # Teste rápido")
    print("   uv run hello-crewai        # Primeiro exemplo")
    print("   uv run python hello_simples.py  # Exemplo simples")
    print("\n📝 Comandos alternativos:")
    print("   uv run python -m curso_crewai.teste_api")
    print("   uv run python -m curso_crewai.hello_crewai")
    print("\n🔗 Recursos úteis:")
    print("   • Documentação UV: https://docs.astral.sh/uv/")
    print("   • CrewAI Docs: https://docs.crewai.com/")
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