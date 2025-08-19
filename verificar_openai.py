"""
Verificador de Status da API OpenAI
Script para testar a conectividade e funcionalidade da chave API da OpenAI

Funcionalidades:
1. Verifica se a chave API está configurada
2. Testa a conectividade com a API
3. Lista modelos disponíveis
4. Faz um teste básico de chat
5. Exibe informações de uso e limites
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

try:
    from openai import OpenAI

    print("✅ Biblioteca OpenAI importada com sucesso")
except ImportError:
    print("❌ Erro: Biblioteca 'openai' não encontrada!")
    print("Execute: pip install openai")
    sys.exit(1)

# Carrega variáveis de ambiente
load_dotenv()


class VerificadorOpenAI:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
        self.client = None

    def verificar_chave_api(self):
        """Verifica se a chave API está configurada"""
        print("\n🔑 Verificando chave API...")

        if not self.api_key:
            print("❌ OPENAI_API_KEY não encontrada!")
            print("Configure no arquivo .env ou como variável de ambiente")
            print("Exemplo: OPENAI_API_KEY=sk-...")
            return False

        if not self.api_key.startswith("sk-"):
            print("⚠️  Formato da chave API suspeito (deve começar com 'sk-')")

        # Mascarar a chave para exibição
        chave_mascarada = f"{self.api_key[:7]}...{self.api_key[-4:]}"
        print(f"✅ Chave API encontrada: {chave_mascarada}")

        # Inicializar cliente OpenAI
        try:
            self.client = OpenAI(api_key=self.api_key)
            print("✅ Cliente OpenAI inicializado")
            return True
        except Exception as e:
            print(f"❌ Erro ao inicializar cliente: {e}")
            return False

    def testar_conectividade(self):
        """Testa a conectividade básica com a API"""
        print("\n🌐 Testando conectividade...")

        try:
            # Listar modelos disponíveis
            modelos = self.client.models.list()
            print("✅ Conectividade com API estabelecida")
            return True
        except Exception as e:
            print(f"❌ Erro de conectividade: {e}")
            if "401" in str(e):
                print("💡 Erro 401: Chave API inválida ou expirada")
            elif "429" in str(e):
                print("💡 Erro 429: Limite de rate excedido")
            elif "403" in str(e):
                print("💡 Erro 403: Acesso negado - verifique permissões")
            return False

    def listar_modelos(self):
        """Lista os modelos disponíveis"""
        print("\n📋 Listando modelos disponíveis...")

        try:
            modelos = self.client.models.list()
            modelos_gpt = []

            for modelo in modelos.data:
                if "gpt" in modelo.id.lower():
                    modelos_gpt.append(modelo.id)

            modelos_gpt.sort()

            print("✅ Modelos GPT disponíveis:")
            for i, modelo in enumerate(modelos_gpt[:10], 1):  # Mostra primeiros 10
                marca = "🎯" if modelo == self.model else "  "
                print(f"{marca} {i:2}. {modelo}")

            if len(modelos_gpt) > 10:
                print(f"   ... e mais {len(modelos_gpt) - 10} modelos")

            print(f"\n🎯 Modelo selecionado: {self.model}")
            return True

        except Exception as e:
            print(f"❌ Erro ao listar modelos: {e}")
            return False

    def teste_chat_simples(self):
        """Faz um teste básico de chat"""
        print(f"\n💬 Testando chat com modelo {self.model}...")

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "Você é um assistente amigável que responde em português.",
                    },
                    {
                        "role": "user",
                        "content": "Diga olá e se apresente brevemente em uma frase.",
                    },
                ],
                max_tokens=100,
                temperature=0.7,
            )

            resposta = response.choices[0].message.content
            tokens_usados = response.usage.total_tokens

            print("✅ Teste de chat bem-sucedido!")
            print(f"📝 Resposta: {resposta}")
            print(f"🔢 Tokens utilizados: {tokens_usados}")

            # Calcular custo aproximado
            if "gpt-4" in self.model.lower():
                custo = tokens_usados * 0.00003  # Aproximação GPT-4
            else:
                custo = tokens_usados * 0.000002  # Aproximação GPT-3.5

            print(f"💰 Custo aproximado: ${custo:.6f}")

            return True

        except Exception as e:
            print(f"❌ Erro no teste de chat: {e}")
            if "model" in str(e).lower():
                print("💡 Modelo pode não estar disponível ou ter nome incorreto")
            return False

    def informacoes_conta(self):
        """Tenta obter informações da conta (pode não estar disponível em todas as contas)"""
        print("\n📊 Informações da conta...")

        try:
            # Tentar obter informações de uso (nem sempre disponível)
            print("ℹ️  Informações detalhadas de billing requerem acesso especial à API")
            print("ℹ️  Verifique seu uso em: https://platform.openai.com/usage")

        except Exception as e:
            print(f"ℹ️  Informações de conta não disponíveis via API: {e}")

    def executar_verificacao_completa(self):
        """Executa todas as verificações"""
        print("=" * 60)
        print("🤖 VERIFICADOR DE STATUS DA API OPENAI")
        print("=" * 60)
        print(f"⏰ Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

        # Verificações sequenciais
        if not self.verificar_chave_api():
            return False

        if not self.testar_conectividade():
            return False

        self.listar_modelos()

        if not self.teste_chat_simples():
            return False

        self.informacoes_conta()

        print("\n" + "=" * 60)
        print("🎉 VERIFICAÇÃO CONCLUÍDA COM SUCESSO!")
        print("✅ Sua configuração está pronta para usar CrewAI")
        print("=" * 60)

        return True


def main():
    """Função principal"""
    verificador = VerificadorOpenAI()

    try:
        sucesso = verificador.executar_verificacao_completa()

        if sucesso:
            print("\n🚀 Próximos passos:")
            print("   1. Execute: python hello_crewai.py")
            print("   2. Ou execute: python hello_simples.py")
            sys.exit(0)
        else:
            print("\n❌ Configuração incompleta. Resolva os problemas acima.")
            sys.exit(1)

    except KeyboardInterrupt:
        print("\n\n⏹️  Verificação interrompida pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
