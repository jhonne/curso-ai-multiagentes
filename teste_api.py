"""
Teste Rápido da API OpenAI
Script simples para verificar se tudo está funcionando
"""

import os
from dotenv import load_dotenv


def teste_rapido_openai():
    """Teste rápido e direto da API OpenAI"""
    
    print("🔍 Teste Rápido da API OpenAI")
    print("-" * 40)
    
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # 1. Verificar se a chave existe
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY não encontrada!")
        print("💡 Configure no arquivo .env:")
        print("   OPENAI_API_KEY=sua_chave_aqui")
        return False
    
    print(f"✅ Chave API encontrada: {api_key[:7]}...{api_key[-4:]}")
    
    # 2. Tentar importar e usar OpenAI
    try:
        from openai import OpenAI
        print("✅ Biblioteca openai importada")
    except ImportError:
        print("❌ Biblioteca openai não encontrada!")
        print("💡 Execute: uv add openai")
        return False
    
    # 3. Inicializar cliente
    try:
        client = OpenAI(api_key=api_key)
        print("✅ Cliente OpenAI inicializado")
    except Exception as e:
        print(f"❌ Erro ao inicializar: {e}")
        return False
    
    # 4. Teste básico
    try:
        print("🧪 Fazendo teste básico...")
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user", 
                    "content": "Diga apenas: Olá! Teste bem-sucedido!"
                }
            ],
            max_tokens=50
        )
        
        resposta = response.choices[0].message.content
        tokens = response.usage.total_tokens
        
        print(f"✅ Resposta: {resposta}")
        print(f"🔢 Tokens usados: {tokens}")
        print("🎉 TESTE BEM-SUCEDIDO!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        
        # Dicas baseadas no erro
        erro_str = str(e).lower()
        if "401" in erro_str or "unauthorized" in erro_str:
            print("💡 Chave API inválida ou expirada")
        elif "429" in erro_str or "rate limit" in erro_str:
            print("💡 Limite de requisições excedido")
        elif "insufficient" in erro_str or "quota" in erro_str:
            print("💡 Cota esgotada - verifique seu saldo")
        
        return False


def main():
    """Função principal para uso como script"""
    sucesso = teste_rapido_openai()
    
    if sucesso:
        print("\n🚀 Tudo pronto! Você pode executar:")
        print("   uv run hello-crewai")
        print("   python -m curso_crewai.hello_crewai")
    else:
        print("\n🔧 Resolva os problemas acima antes de continuar")


if __name__ == "__main__":
    main()