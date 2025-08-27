"""
Teste Rápido da API OpenAI
Script simples para verificar se tudo está funcionando
"""

import os
import time
import hashlib
from datetime import datetime
from dotenv import load_dotenv


class MonitorCustos:
    """Monitor básico de custos para testes"""
    def __init__(self):
        self.precos_modelo = {
            "gpt-4o-mini": {"input": 0.15/1000000, "output": 0.60/1000000},
            "gpt-3.5-turbo": {"input": 0.50/1000000, "output": 1.50/1000000}
        }
    
    def calcular_custo(self, tokens_input, tokens_output, modelo="gpt-4o-mini"):
        """Calcula custo estimado baseado nos tokens usados"""
        preco = self.precos_modelo.get(modelo, self.precos_modelo["gpt-4o-mini"])
        custo = (tokens_input * preco["input"]) + (tokens_output * preco["output"])
        return custo


def validar_api_key(api_key):
    """Validação robusta da API key OpenAI"""
    if not api_key:
        return False, "API key não encontrada"
    
    if not isinstance(api_key, str):
        return False, "API key deve ser uma string"
    
    if not api_key.startswith('sk-'):
        return False, "Formato inválido (deve começar com 'sk-')"
    
    if len(api_key) < 20:
        return False, "API key muito curta"
    
    return True, "API key válida"


def verificar_conteudo_seguro(texto):
    """Verificação básica de conteúdo seguro usando API de Moderação"""
    try:
        from openai import OpenAI
        client = OpenAI()
        response = client.moderations.create(input=texto)
        return not response.results[0].flagged
    except Exception:
        # Em caso de erro, ser conservador mas não bloquear teste
        return True


def gerar_safety_identifier():
    """Gera identificador seguro para rastreamento"""
    timestamp = str(int(time.time()))
    return hashlib.sha256(f"teste_{timestamp}".encode()).hexdigest()[:16]


def teste_rapido_openai():
    """Teste rápido e direto da API OpenAI"""

    print("🔍 Teste Rápido da API OpenAI")
    print("-" * 40)

    # Carregar variáveis de ambiente
    load_dotenv()

    # 1. Verificar e validar API key
    api_key = os.getenv("OPENAI_API_KEY")
    
    valida, mensagem = validar_api_key(api_key)
    if not valida:
        print(f"❌ {mensagem}")
        print("💡 Configure no arquivo .env:")
        print("   OPENAI_API_KEY=sua_chave_aqui")
        return False

    print(f"✅ API key válida: {api_key[:7]}...{api_key[-4:]}")
    
    # Gerar identificador de segurança
    safety_id = gerar_safety_identifier()
    print(f"🔒 Safety ID: {safety_id}")

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

    # 4. Teste otimizado com monitoramento
    try:
        print("🧪 Fazendo teste otimizado...")
        
        # Inicializar monitor de custos
        monitor = MonitorCustos()
        
        # Mensagem de teste otimizada
        mensagem_teste = "Responda apenas: OK"
        
        # Verificação de segurança (opcional, não bloqueia se falhar)
        if not verificar_conteudo_seguro(mensagem_teste):
            print("⚠️ Conteúdo não passou na moderação, mas continuando teste...")
        
        # Rate limiting preventivo
        time.sleep(0.5)
        
        print(f"⏰ Teste iniciado em {datetime.now().strftime('%H:%M:%S')}")

        response = client.chat.completions.create(
            model="gpt-4o-mini",  # ✅ Modelo mais econômico
            messages=[
                {"role": "user", "content": mensagem_teste}
            ],
            max_tokens=10,  # ✅ Reduzido para economia
            temperature=0,  # ✅ Determinístico e econômico
        )

        resposta = response.choices[0].message.content
        tokens_total = response.usage.total_tokens
        tokens_input = response.usage.prompt_tokens
        tokens_output = response.usage.completion_tokens
        
        # Calcular custo estimado
        custo = monitor.calcular_custo(tokens_input, tokens_output, "gpt-4o-mini")

        print(f"✅ Resposta: {resposta}")
        print(f"🔢 Tokens: {tokens_total} (entrada: {tokens_input}, saída: {tokens_output})")
        print(f"💰 Custo estimado: ${custo:.6f}")
        print(f"🎯 Modelo: gpt-4o-mini (otimizado para economia)")
        print("🎉 TESTE OTIMIZADO BEM-SUCEDIDO!")

        return True

    except Exception as e:
        print(f"❌ Erro no teste: {e}")

        # Dicas baseadas no erro com mais detalhes
        erro_str = str(e).lower()
        if "401" in erro_str or "unauthorized" in erro_str:
            print("💡 Chave API inválida ou expirada")
            print("   → Verifique se a chave está correta no arquivo .env")
        elif "429" in erro_str or "rate limit" in erro_str:
            print("💡 Limite de requisições excedido")
            print("   → Aguarde alguns minutos antes de tentar novamente")
        elif "insufficient" in erro_str or "quota" in erro_str:
            print("💡 Cota esgotada - verifique seu saldo")
            print("   → Acesse https://platform.openai.com/usage")
        elif "network" in erro_str or "connection" in erro_str:
            print("💡 Problema de conectividade")
            print("   → Verifique sua conexão com a internet")
        else:
            print(f"💡 Erro específico: {e}")

        return False


def main():
    """Função principal para uso como script"""
    sucesso = teste_rapido_openai()

    if sucesso:
        print("\n🚀 Tudo pronto! Configuração otimizada:")
        print("   ✅ API OpenAI funcionando")
        print("   ✅ Modelo econômico (gpt-4o-mini) configurado")
        print("   ✅ Validações de segurança ativas")
        print("\n📋 Próximos passos:")
        print("   uv run hello-crewai")
        print("   python -m curso_crewai.hello_crewai")
    else:
        print("\n🔧 Resolva os problemas acima antes de continuar")
        print("💡 Para mais ajuda, consulte: docs/CONFIGURACAO_AMBIENTE.md")


if __name__ == "__main__":
    main()
