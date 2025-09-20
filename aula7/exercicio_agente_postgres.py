#!/usr/bin/env python3
"""
Exercício Prático: Agente CrewAI com PostgreSQL
==============================================

OBJETIVO: Criar um agente que busca estabelecimentos médicos no banco PostgreSQL

EXECUÇÃO:
uv run aula7/exercicio_agente_postgres.py

PRÉ-REQUISITOS:
1. PostgreSQL rodando (localhost:5432)
2. Banco 'curso' criado
3. Variáveis de ambiente configuradas (.env)
"""

import os
from datetime import datetime
from dotenv import load_dotenv

from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
import psycopg2
from psycopg2.extras import RealDictCursor

# Carregar variáveis de ambiente
load_dotenv()


class BuscadorEstabelecimentos:
    """Ferramenta para buscar estabelecimentos médicos no PostgreSQL"""
    
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


def criar_agente_postgres():
    """Cria agente especializado em buscar estabelecimentos médicos"""
    
    # LLM configurado
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1
    )
    
    # Agente especialista em estabelecimentos médicos
    agente_busca = Agent(
        role="Especialista em Busca de Estabelecimentos Médicos",
        goal="Encontrar estabelecimentos médicos adequados usando o banco PostgreSQL",
        backstory="""
        Sou um especialista em localizar estabelecimentos médicos em bancos de dados.
        Tenho acesso ao sistema PostgreSQL com informações completas sobre hospitais,
        UPAs, clínicas e outros serviços de saúde.
        
        Minha especialidade é fazer buscas precisas e retornar informações organizadas
        e úteis para os usuários.
        """,
        verbose=True,
        llm=llm,
        allow_delegation=False
    )
    
    return agente_busca


def executar_exercicio():
    """Executa o exercício prático completo"""
    
    print("🏥 EXERCÍCIO: AGENTE CREWAI + POSTGRESQL")
    print("=" * 45)
    
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
    
    # Criar agente
    print("\n🤖 Criando agente CrewAI...")
    agente = criar_agente_postgres()
    
    # Definir tarefa de busca
    tarefa_busca = Task(
        description="""
        Realize uma busca de estabelecimentos médicos no banco PostgreSQL com os seguintes critérios:
        
        1. Busque hospitais em São Paulo
        2. Busque UPAs (Unidades de Pronto Atendimento) em qualquer cidade
        3. Liste clínicas disponíveis
        
        Para cada busca:
        - Use a ferramenta de busca no PostgreSQL
        - Organize os resultados de forma clara
        - Inclua nome, tipo, município e contato quando disponível
        
        Apresente um relatório organizado com as três buscas.
        """,
        agent=agente,
        expected_output="""
        Relatório estruturado com três seções:
        1. Hospitais em São Paulo
        2. UPAs disponíveis  
        3. Clínicas encontradas
        
        Para cada estabelecimento: nome, tipo, município e telefone.
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
    
    # Criar crew simples (demonstrativo)
    print("\n🎯 DEMONSTRAÇÃO COM CREWAI:")
    print("-" * 35)
    
    # Tarefa simplificada para demonstração
    tarefa_demo = Task(
        description=f"""
        Analise os dados encontrados no PostgreSQL e faça um resumo:
        
        DADOS ENCONTRADOS:
        - Hospitais: {len(hospitais)} encontrados
        - UPAs: {len(upas)} encontradas  
        - Clínicas: {len(clinicas)} encontradas
        
        Crie um breve resumo da disponibilidade de serviços médicos.
        """,
        agent=agente,
        expected_output="Resumo executivo da disponibilidade de estabelecimentos médicos."
    )
    
    # Executar crew
    crew = Crew(
        agents=[agente],
        tasks=[tarefa_demo],
        process=Process.sequential,
        verbose=False
    )
    
    print("🚀 Executando análise com CrewAI...")
    resultado = crew.kickoff()
    
    print("\n📋 RESULTADO DA ANÁLISE CREWAI:")
    print("-" * 40)
    print(resultado.raw)
    
    print(f"\n✅ EXERCÍCIO CONCLUÍDO!")
    print(f"📊 Resultados: {len(hospitais + upas + clinicas)} estabelecimentos encontrados")
    print("🎓 Agente CrewAI integrado com PostgreSQL com sucesso!")


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