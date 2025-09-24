#!/usr/bin/env python3
"""
🎓 AULA 7: Agente CrewAI + PostgreSQL - Exercício Didático
=========================================================

OBJETIVO EDUCACIONAL:
Demonstrar como integrar um agente CrewAI com banco de dados PostgreSQL,
mostrando o fluxo completo desde a criação da ferramenta até a execução.

EXECUÇÃO:
uv run aula7/exercicio_agente_postgres.py

PRÉ-REQUISITOS:
1. PostgreSQL rodando (localhost:5432)
2. Banco 'curso' criado
3. Variáveis de ambiente configuradas (.env)
"""

# =============================================================================
# MÓDULO 1: IMPORTS E CONFIGURAÇÃO INICIAL
# =============================================================================
import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel, Field
from typing import Type

print("🔧 Carregando configurações do ambiente...")
load_dotenv()


# =============================================================================
# MÓDULO 2: DEFINIÇÃO DA FERRAMENTA CREWAI (A PARTE MAIS IMPORTANTE!)
# =============================================================================

class BuscadorEstabelecimentosInput(BaseModel):
    """📝 Schema de entrada para a ferramenta - define quais parâmetros o agente pode usar"""
    tipo: str = Field(description="hospital, upa, clinica, ou 'todos'")
    municipio: str = Field(description="Nome do município ou 'todos'") 
    limite: int = Field(default=5, description="Máximo de resultados")


class BuscadorEstabelecimentosTool(BaseTool):
    """
    🛠️ FERRAMENTA PRINCIPAL: Esta é a ponte entre o agente CrewAI e o PostgreSQL
    
    IMPORTANTE: Esta classe herda de BaseTool, o que permite ao agente CrewAI
    usar esta ferramenta automaticamente quando necessário.
    """
    
    name: str = "buscar_estabelecimentos_postgres"
    description: str = (
        "Busca estabelecimentos médicos no PostgreSQL. "
        "Use para hospitais, UPAs, clínicas por tipo e município."
    )
    args_schema: Type[BaseModel] = BuscadorEstabelecimentosInput
    
    def _run(self, tipo: str, municipio: str, limite: int = 5) -> str:
        """
        🔍 MÉTODO PRINCIPAL: Aqui acontece a consulta REAL ao PostgreSQL
        
        Este método é chamado automaticamente pelo agente CrewAI quando
        ele precisa buscar estabelecimentos no banco de dados.
        """
        try:
            # Configuração da conexão PostgreSQL
            db_config = {
                'host': os.getenv('POSTGRES_HOST', 'localhost'),
                'port': os.getenv('POSTGRES_PORT', '5432'),
                'database': os.getenv('POSTGRES_DB', 'curso'),
                'user': os.getenv('POSTGRES_USER', 'postgres'),
                'password': os.getenv('POSTGRES_PASSWORD', 'arpus')
            }
            
            # Conectar ao PostgreSQL
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Montar query SQL dinâmica
            query = """SELECT nome, tipo, municipio, telefone, endereco 
                      FROM estabelecimentos WHERE 1=1"""
            params = []
            
            # Adicionar filtros conforme parâmetros do agente
            if tipo.lower() != 'todos':
                query += " AND LOWER(tipo) LIKE %s"
                params.append(f"%{tipo.lower()}%")
            
            if municipio.lower() != 'todos':
                query += " AND LOWER(municipio) LIKE %s"
                params.append(f"%{municipio.lower()}%")
            
            query += f" ORDER BY nome LIMIT {limite}"
            
            # Executar query
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            
            if not resultados:
                return f"❌ Nenhum resultado: tipo='{tipo}', município='{municipio}'"
            
            # Formatar resultados para o agente
            output = f"Encontrados {len(resultados)} estabelecimento(s):\n"
            for i, row in enumerate(resultados, 1):
                output += f"\n{i}. {row['nome']}"
                output += f"\n   Tipo: {row['tipo']}"
                output += f"\n   Município: {row['municipio']}"
                output += f"\n   Telefone: {row['telefone']}"
                output += f"\n   Endereço: {row['endereco']}"
                
            conn.close()
            return output
            
        except Exception as e:
            return f"❌ Erro PostgreSQL: {str(e)}"


# =============================================================================
# MÓDULO 3: CLASSE AUXILIAR PARA OPERAÇÕES DIRETAS (DEMONSTRAÇÃO)
# =============================================================================

class BuscadorEstabelecimentos:
    """
    📊 CLASSE AUXILIAR: Para demonstrar buscas diretas no PostgreSQL
    
    NOTA DIDÁTICA: Esta classe é usada apenas para preparar dados de exemplo
    e demonstrar consultas diretas. O agente CrewAI usa a BuscadorEstabelecimentosTool.
    """
    
    def __init__(self):
        self.db_config = {
            'host': os.getenv('POSTGRES_HOST', 'localhost'),
            'port': os.getenv('POSTGRES_PORT', '5432'),
            'database': os.getenv('POSTGRES_DB', 'curso'),
            'user': os.getenv('POSTGRES_USER', 'postgres'),
            'password': os.getenv('POSTGRES_PASSWORD', 'arpus')
        }
    
    def conectar_db(self):
        """Conecta ao PostgreSQL"""
        try:
            conn = psycopg2.connect(**self.db_config)
            return conn
        except Exception as e:
            print(f"❌ Erro PostgreSQL: {e}")
            return None
    
    def buscar_estabelecimentos(self, tipo=None, municipio=None, limite=5):
        """
        Busca estabelecimentos no banco
        
        Args:
            tipo: Tipo de estabelecimento (hospital, upa, clinica)
            municipio: Nome do município
            limite: Número máximo de resultados
        
        Returns:
            Lista de estabelecimentos encontrados
        """
        conn = self.conectar_db()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Query base
            query = "SELECT id, nome, tipo, municipio, telefone, endereco FROM estabelecimentos WHERE 1=1"
            params = []
            
            # Adicionar filtros
            if tipo:
                query += " AND LOWER(tipo) LIKE %s"
                params.append(f"%{tipo.lower()}%")
            
            if municipio:
                query += " AND LOWER(municipio) LIKE %s"
                params.append(f"%{municipio.lower()}%")
            
            query += f" ORDER BY nome LIMIT {limite}"
            
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            
            return [dict(row) for row in resultados]
            
        except Exception as e:
            print(f"❌ Erro na busca: {e}")
            return []
        finally:
            conn.close()
    
    def inserir_estabelecimento_exemplo(self, nome, tipo, municipio):
        """Insere um estabelecimento de exemplo"""
        conn = self.conectar_db()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO estabelecimentos (nome, tipo, latitude, longitude, municipio, telefone, endereco)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT DO NOTHING
            """, (
                nome, tipo, -23.5505, -46.6333,  # Coordenadas de São Paulo
                municipio, "(11) 9999-9999", f"Rua Exemplo, 123 - {municipio}"
            ))
            conn.commit()
            return True
        except Exception as e:
            print(f"❌ Erro ao inserir: {e}")
            return False
        finally:
            conn.close()


# =============================================================================
# MÓDULO 4: CRIAÇÃO DO AGENTE CREWAI (PEÇA CENTRAL!)
# =============================================================================

def criar_agente_postgres():
    """
    🤖 FUNÇÃO PRINCIPAL: Cria o agente CrewAI com ferramenta PostgreSQL
    
    PONTOS DIDÁTICOS IMPORTANTES:
    1. Configuramos o LLM (modelo de linguagem)
    2. Criamos a ferramenta de busca
    3. Conectamos a ferramenta ao agente (tools=[ferramenta])
    4. Definimos role, goal e backstory claros
    """
    
    print("🧠 Configurando modelo de linguagem...")
    llm = ChatOpenAI(
        model="gpt-4o-mini",  # Modelo econômico e eficiente
        temperature=0.1       # Baixa variabilidade para respostas consistentes
    )
    
    print("🛠️ Criando ferramenta de busca PostgreSQL...")
    ferramenta_busca = BuscadorEstabelecimentosTool()
    
    print("🤖 Criando agente especialista...")
    agente_busca = Agent(
        role="Especialista em Estabelecimentos Médicos",
        goal="Buscar estabelecimentos médicos no PostgreSQL de forma eficiente",
        backstory="""
        Sou especialista em busca de estabelecimentos de saúde.
        Tenho acesso direto ao banco PostgreSQL com dados de hospitais,
        UPAs e clínicas. Posso filtrar por tipo e município.
        """,
        verbose=False,  # Debug desligado para output mais limpo
        llm=llm,
        tools=[ferramenta_busca],  # ← PONTO CRUCIAL: Conecta ferramenta ao agente
        allow_delegation=False
    )
    
    print("✅ Agente criado com sucesso!")
    return agente_busca


# =============================================================================
# MÓDULO 5: EXECUÇÃO PRINCIPAL DO EXERCÍCIO
# =============================================================================

def executar_exercicio():
    """
    🎯 FUNÇÃO PRINCIPAL: Executa todo o exercício didático
    
    FLUXO DIDÁTICO:
    1. Testar conexão PostgreSQL
    2. Inserir dados de exemplo
    3. Criar agente com ferramenta
    4. Demonstrar consultas diretas (comparação)
    5. Executar agente CrewAI (demonstração real)
    """
    
    print("� AULA 7: AGENTE CREWAI + POSTGRESQL")
    print("=" * 45)
    print("📚 Demonstração didática de integração banco de dados")
    print()
    
    # Inicializar ferramenta de busca
    buscador = BuscadorEstabelecimentos()
    
    # Teste de conexão
    print("\n🔍 Testando conexão PostgreSQL...")
    conn = buscador.conectar_db()
    if not conn:
        print("❌ Não foi possível conectar ao PostgreSQL")
        print("\n💡 VERIFICAÇÕES NECESSÁRIAS:")
        print("   • PostgreSQL está rodando?")
        print("   • Banco 'curso' existe?")
        print("   • Credenciais corretas no .env?")
        return
    
    conn.close()
    print("✅ PostgreSQL conectado com sucesso!")
    
    # Inserir dados de exemplo se necessário
    print("\n📥 Inserindo dados de exemplo...")
    exemplos = [
        ("Hospital São Paulo", "hospital", "São Paulo"),
        ("UPA Central", "upa", "São Paulo"),
        ("Clínica Santa Maria", "clinica", "Santo André"),
        ("Hospital Municipal", "hospital", "Campinas")
    ]
    
    for nome, tipo, municipio in exemplos:
        buscador.inserir_estabelecimento_exemplo(nome, tipo, municipio)
    
    print("✅ Dados de exemplo inseridos!")
    
    # PASSO 3: Criar agente CrewAI com ferramenta
    print("\n📋 PASSO 3: Criando agente CrewAI...")
    agente = criar_agente_postgres()
    
    # PASSO 4: Definir tarefa que instrui o agente a usar sua ferramenta
    print("\n📝 PASSO 4: Definindo tarefa para o agente...")
    tarefa_agente = Task(
        description="""
        TAREFA DIDÁTICA: Use sua ferramenta PostgreSQL para buscar:
        
        1. Hospitais em São Paulo
        2. UPAs em qualquer cidade
        3. Clínicas em Santo André
        
        Use a ferramenta buscar_estabelecimentos_postgres com parâmetros corretos.
        """,
        agent=agente,
        expected_output="""
        Relatório com três seções:
        1. Hospitais em São Paulo
        2. UPAs disponíveis
        3. Clínicas em Santo André
        
        Para cada: nome, tipo, município e telefone.
        """
    )
    
    # Executar busca direta (simulando o que o agente faria)
    print("\n🔍 EXECUTANDO BUSCAS NO POSTGRESQL...")
    print("-" * 40)
    
    # Busca 1: Hospitais em São Paulo
    print("\n🏥 HOSPITAIS EM SÃO PAULO:")
    hospitais = buscador.buscar_estabelecimentos(tipo="hospital", municipio="São Paulo")
    for hosp in hospitais:
        print(f"   • {hosp['nome']} - {hosp['telefone']}")
        print(f"     Endereço: {hosp['endereco']}")
    
    # Busca 2: UPAs
    print("\n🚑 UPAS DISPONÍVEIS:")
    upas = buscador.buscar_estabelecimentos(tipo="upa")
    for upa in upas:
        print(f"   • {upa['nome']} - {upa['municipio']}")
        print(f"     Telefone: {upa['telefone']}")
    
    # Busca 3: Clínicas
    print("\n🩺 CLÍNICAS ENCONTRADAS:")
    clinicas = buscador.buscar_estabelecimentos(tipo="clinica")
    for clinica in clinicas:
        print(f"   • {clinica['nome']} - {clinica['municipio']}")
        print(f"     Telefone: {clinica['telefone']}")
    
    
    # PASSO 5: Demonstração prática - Agente usando sua ferramenta
    print("\n🎯 PASSO 5: DEMONSTRAÇÃO PRÁTICA")
    print("🤖 Agente CrewAI executando consultas reais no PostgreSQL")
    print("-" * 60)
    
    # Executar crew com agente que TEM ACESSO à ferramenta
    crew_didatico = Crew(
        agents=[agente],
        tasks=[tarefa_agente],
        process=Process.sequential,
        verbose=False  # Debug desligado para output limpo
    )
    
    print("🚀 EXECUTANDO: Agente consultando PostgreSQL...")
    print("⏳ Processando consultas...")
    resultado_agente = crew_didatico.kickoff()
    
    print("\n� RESULTADO FINAL DO AGENTE:")
    print("=" * 40)
    print(resultado_agente.raw)
    
    # CONCLUSÃO DIDÁTICA
    total_estabelecimentos = len(hospitais + upas + clinicas)
    print(f"\n✅ EXERCÍCIO DIDÁTICO CONCLUÍDO!")
    print(f"📊 Total encontrado: {total_estabelecimentos} estabelecimentos")
    print("🎓 Agente CrewAI integrado com PostgreSQL com sucesso!")
    
    print(f"\n📚 RESUMO DIDÁTICO:")
    print("   ✅ Ferramenta CrewAI criada (BuscadorEstabelecimentosTool)")
    print("   ✅ Agente conectado à ferramenta (tools=[ferramenta])")
    print("   ✅ Agente executou consultas PostgreSQL automaticamente")
    print("   ✅ Resultados formatados e apresentados pelo agente")


# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    try:
        executar_exercicio()
    except KeyboardInterrupt:
        print("\n⏹️ Exercício interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro no exercício: {e}")
        print("\n🔧 DICAS DE TROUBLESHOOTING:")
        print("   • Verificar se PostgreSQL está rodando")
        print("   • Confirmar credenciais no arquivo .env")
        print("   • Verificar se banco 'curso' existe")
        print("   • Executar: uv add psycopg2-binary")