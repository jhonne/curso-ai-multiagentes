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
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel, Field
from typing import Type

# Carregar variáveis de ambiente
load_dotenv()


class BuscadorEstabelecimentosInput(BaseModel):
    """Input schema para a ferramenta de busca"""
    tipo: str = Field(description="Tipo de estabelecimento (hospital, upa, clinica, ou 'todos')")
    municipio: str = Field(description="Nome do município (ou 'todos' para qualquer cidade)")
    limite: int = Field(default=5, description="Número máximo de resultados (padrão: 5)")


class BuscadorEstabelecimentosTool(BaseTool):
    """Ferramenta CrewAI para buscar estabelecimentos médicos no PostgreSQL"""
    
    name: str = "buscar_estabelecimentos_postgres"
    description: str = (
        "Busca estabelecimentos médicos no banco PostgreSQL. "
        "Use para encontrar hospitais, UPAs, clínicas por tipo e/ou município. "
        "Parâmetros: tipo (hospital/upa/clinica/todos), municipio (nome ou 'todos'), limite (número)"
    )
    args_schema: Type[BaseModel] = BuscadorEstabelecimentosInput
    
    def _run(self, tipo: str, municipio: str, limite: int = 5) -> str:
        """Executa a busca no PostgreSQL"""
        try:
            # Configuração do banco (dentro do método para evitar problemas com BaseTool)
            db_config = {
                'host': os.getenv('POSTGRES_HOST', 'localhost'),
                'port': os.getenv('POSTGRES_PORT', '5432'),
                'database': os.getenv('POSTGRES_DB', 'curso'),
                'user': os.getenv('POSTGRES_USER', 'postgres'),
                'password': os.getenv('POSTGRES_PASSWORD', 'arpus')
            }
            
            conn = psycopg2.connect(**db_config)
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            # Query base
            query = "SELECT nome, tipo, municipio, telefone, endereco FROM estabelecimentos WHERE 1=1"
            params = []
            
            # Adicionar filtros
            if tipo.lower() != 'todos':
                query += " AND LOWER(tipo) LIKE %s"
                params.append(f"%{tipo.lower()}%")
            
            if municipio.lower() != 'todos':
                query += " AND LOWER(municipio) LIKE %s"
                params.append(f"%{municipio.lower()}%")
            
            query += f" ORDER BY nome LIMIT {limite}"
            
            cursor.execute(query, params)
            resultados = cursor.fetchall()
            
            if not resultados:
                return f"Nenhum estabelecimento encontrado para: tipo='{tipo}', município='{municipio}'"
            
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
            return f"Erro ao consultar PostgreSQL: {str(e)}"


class BuscadorEstabelecimentos:
    """Classe auxiliar para operações diretas no PostgreSQL (fora do agente)"""
    
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
    
    # Criar ferramenta de busca
    ferramenta_busca = BuscadorEstabelecimentosTool()
    
    # Agente especialista em estabelecimentos médicos
    agente_busca = Agent(
        role="Especialista em Busca de Estabelecimentos Médicos",
        goal="Encontrar estabelecimentos médicos adequados usando o banco PostgreSQL",
        backstory="""
        Sou um especialista em localizar estabelecimentos médicos em bancos de dados.
        Tenho acesso direto ao sistema PostgreSQL com informações completas sobre hospitais,
        UPAs, clínicas e outros serviços de saúde.
        
        Posso realizar buscas precisas por tipo de estabelecimento, município ou 
        combinações de filtros, sempre retornando informações organizadas e úteis.
        """,
        verbose=True,
        llm=llm,
        tools=[ferramenta_busca],  # CONECTAR A FERRAMENTA AO AGENTE
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
    
    # Definir tarefa REAL que usa a ferramenta do agente
    tarefa_busca_real = Task(
        description="""
        Use sua ferramenta de busca PostgreSQL para encontrar estabelecimentos médicos:
        
        1. Busque hospitais em São Paulo
        2. Busque UPAs em qualquer cidade  
        3. Busque clínicas em Santo André
        
        Para cada busca, use a ferramenta buscar_estabelecimentos_postgres com os 
        parâmetros apropriados. Organize os resultados de forma clara e profissional.
        """,
        agent=agente,
        expected_output="""
        Relatório estruturado com três seções:
        1. Hospitais em São Paulo (resultados da consulta PostgreSQL)
        2. UPAs disponíveis (resultados da consulta PostgreSQL) 
        3. Clínicas em Santo André (resultados da consulta PostgreSQL)
        
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
    
    
    # DEMONSTRAÇÃO REAL: Agente usando sua ferramenta PostgreSQL
    print("\n🤖 DEMONSTRAÇÃO REAL: AGENTE + FERRAMENTA POSTGRESQL")
    print("-" * 55)
    
    # Executar crew com agente que TEM ACESSO à ferramenta
    crew_real = Crew(
        agents=[agente],
        tasks=[tarefa_busca_real],
        process=Process.sequential,
        verbose=True
    )
    
    print("🚀 Executando agente CrewAI com acesso REAL ao PostgreSQL...")
    resultado_real = crew_real.kickoff()
    
    print("\n📋 RESULTADO DA BUSCA REAL (AGENTE + POSTGRESQL):")
    print("-" * 50)
    print(resultado_real.raw)
    
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