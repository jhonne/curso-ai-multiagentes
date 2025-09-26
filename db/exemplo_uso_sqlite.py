#!/usr/bin/env python3
"""
Exemplos de uso do banco SQLite migrado
Demonstra como usar os dados em aplicações Python

Autor: Gerado pelo GitHub Copilot  
Data: 26 de setembro de 2025
"""

import sqlite3
import pandas as pd
import json
from datetime import datetime

class BancoCursoSQLite:
    """Classe para interagir com o banco SQLite do curso"""
    
    def __init__(self, db_path='curso.db'):
        self.db_path = db_path
        self.conn = None
    
    def conectar(self):
        """Conecta ao banco SQLite"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row  # Permite acesso por nome das colunas
            return True
        except Exception as e:
            print(f"Erro ao conectar: {e}")
            return False
    
    def desconectar(self):
        """Fecha a conexão com o banco"""
        if self.conn:
            self.conn.close()
    
    def obter_estabelecimentos(self):
        """Retorna todos os estabelecimentos de saúde"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT cnes, nome, endereco, fone, bairro, longitude, latitude
            FROM ia_estabelecimento
            ORDER BY nome
        """)
        return [dict(row) for row in cursor.fetchall()]
    
    def buscar_estabelecimento_por_bairro(self, bairro):
        """Busca estabelecimentos por bairro"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT cnes, nome, endereco, fone, bairro
            FROM ia_estabelecimento
            WHERE bairro LIKE ?
            ORDER BY nome
        """, (f'%{bairro}%',))
        return [dict(row) for row in cursor.fetchall()]
    
    def obter_queixas_mais_frequentes(self, limite=10):
        """Retorna as queixas principais mais frequentes"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                q.id,
                q.nome,
                COUNT(*) as total_atendimentos,
                ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM ia_historico_atendimento_sintoma), 2) as percentual
            FROM ia_historico_atendimento_sintoma h
            JOIN ia_queixa_principal q ON h.queixa_principal_id = q.id
            GROUP BY q.id, q.nome
            ORDER BY total_atendimentos DESC
            LIMIT ?
        """, (limite,))
        return [dict(row) for row in cursor.fetchall()]
    
    def obter_sintomas_por_queixa(self, queixa_id):
        """Retorna os sintomas associados a uma queixa específica"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                s.id,
                s.nome as sintoma,
                COUNT(*) as frequencia
            FROM ia_historico_atendimento_sintoma h
            JOIN ia_sintoma s ON h.sintoma_id = s.id
            WHERE h.queixa_principal_id = ?
            GROUP BY s.id, s.nome
            ORDER BY frequencia DESC
        """, (queixa_id,))
        return [dict(row) for row in cursor.fetchall()]
    
    def estatisticas_por_estabelecimento(self):
        """Retorna estatísticas de atendimento por estabelecimento"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                e.cnes,
                e.nome,
                e.bairro,
                COUNT(*) as total_atendimentos,
                COUNT(DISTINCT h.queixa_principal_id) as queixas_distintas,
                COUNT(DISTINCT h.sintoma_id) as sintomas_distintos
            FROM ia_estabelecimento e
            JOIN ia_historico_atendimento_sintoma h ON e.cnes = h.estabelecimento_cnes
            GROUP BY e.cnes, e.nome, e.bairro
            ORDER BY total_atendimentos DESC
        """)
        return [dict(row) for row in cursor.fetchall()]
    
    def exportar_para_json(self, nome_arquivo=None):
        """Exporta dados do banco para arquivo JSON"""
        if not nome_arquivo:
            nome_arquivo = f"dados_curso_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        dados = {
            'estabelecimentos': self.obter_estabelecimentos(),
            'queixas_frequentes': self.obter_queixas_mais_frequentes(20),
            'estatisticas_estabelecimentos': self.estatisticas_por_estabelecimento(),
            'metadados': {
                'data_exportacao': datetime.now().isoformat(),
                'total_registros': self._contar_total_registros()
            }
        }
        
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        
        return nome_arquivo
    
    def gerar_dataframe_atendimentos(self):
        """Cria DataFrame pandas com dados completos de atendimentos"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                h.id as atendimento_id,
                e.nome as estabelecimento,
                e.bairro,
                q.nome as queixa_principal,
                s.nome as sintoma,
                h.estabelecimento_cnes,
                h.queixa_principal_id,
                h.sintoma_id
            FROM ia_historico_atendimento_sintoma h
            JOIN ia_estabelecimento e ON h.estabelecimento_cnes = e.cnes
            JOIN ia_queixa_principal q ON h.queixa_principal_id = q.id
            JOIN ia_sintoma s ON h.sintoma_id = s.id
        """)
        
        # Verificar se pandas está disponível
        try:
            import pandas as pd
            dados = cursor.fetchall()
            colunas = [description[0] for description in cursor.description]
            df = pd.DataFrame(dados, columns=colunas)
            return df
        except ImportError:
            print("❌ Pandas não está instalado. Instale com: uv add pandas")
            return None
    
    def _contar_total_registros(self):
        """Conta total de registros no histórico"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM ia_historico_atendimento_sintoma")
        return cursor.fetchone()[0]

def exemplo_uso_basico():
    """Exemplo básico de uso da classe"""
    print("🔍 EXEMPLO DE USO BÁSICO")
    print("="*50)
    
    # Conectar ao banco
    banco = BancoCursoSQLite()
    if not banco.conectar():
        print("❌ Falha na conexão")
        return
    
    try:
        # 1. Listar estabelecimentos
        print("\n1️⃣ Estabelecimentos de Saúde:")
        estabelecimentos = banco.obter_estabelecimentos()
        for i, est in enumerate(estabelecimentos[:3], 1):
            print(f"   {i}. {est['nome']} - {est['bairro']} ({est['cnes']})")
        
        # 2. Queixas mais frequentes
        print("\n2️⃣ Top 5 Queixas Mais Frequentes:")
        queixas = banco.obter_queixas_mais_frequentes(5)
        for i, queixa in enumerate(queixas, 1):
            print(f"   {i}. {queixa['nome'][:40]}... ({queixa['total_atendimentos']} atendimentos - {queixa['percentual']}%)")
        
        # 3. Buscar por bairro
        print("\n3️⃣ Estabelecimentos no PROMORAR:")
        promorar = banco.buscar_estabelecimento_por_bairro('PROMORAR')
        for est in promorar:
            print(f"   • {est['nome']} - {est['endereco']}")
        
        # 4. Sintomas de uma queixa específica
        print("\n4️⃣ Sintomas associados à 'DOR DE GARGANTA':")
        sintomas = banco.obter_sintomas_por_queixa(22)  # ID 22 = DOR DE GARGANTA
        for i, sintoma in enumerate(sintomas[:5], 1):
            print(f"   {i}. {sintoma['sintoma'][:40]}... ({sintoma['frequencia']} vezes)")
        
    finally:
        banco.desconectar()

def exemplo_analise_avancada():
    """Exemplo de análise mais avançada"""
    print("\n📊 EXEMPLO DE ANÁLISE AVANÇADA")
    print("="*50)
    
    banco = BancoCursoSQLite()
    if not banco.conectar():
        return
    
    try:
        # Estatísticas por estabelecimento
        print("\n📈 Estatísticas Detalhadas por Estabelecimento:")
        stats = banco.estatisticas_por_estabelecimento()
        for est in stats[:3]:
            print(f"\n🏥 {est['nome'][:40]}...")
            print(f"   📍 Bairro: {est['bairro']}")
            print(f"   📊 Atendimentos: {est['total_atendimentos']:,}")
            print(f"   🎯 Queixas distintas: {est['queixas_distintas']}")
            print(f"   💊 Sintomas distintos: {est['sintomas_distintos']}")
        
        # Exportar dados
        print(f"\n💾 Exportando dados para JSON...")
        arquivo_json = banco.exportar_para_json()
        print(f"✅ Dados exportados para: {arquivo_json}")
        
    finally:
        banco.desconectar()

def exemplo_pandas():
    """Exemplo de uso com pandas"""
    print("\n🐼 EXEMPLO COM PANDAS")
    print("="*50)
    
    banco = BancoCursoSQLite()
    if not banco.conectar():
        return
    
    try:
        # Gerar DataFrame
        print("\n📊 Criando DataFrame dos atendimentos...")
        df = banco.gerar_dataframe_atendimentos()
        
        if df is not None:
            print(f"✅ DataFrame criado com {len(df):,} registros")
            print("\n📋 Primeiras linhas:")
            print(df.head())
            
            print(f"\n📊 Estatísticas rápidas:")
            print(f"   • Estabelecimentos únicos: {df['estabelecimento'].nunique()}")
            print(f"   • Queixas únicas: {df['queixa_principal'].nunique()}")
            print(f"   • Sintomas únicos: {df['sintoma'].nunique()}")
            
            # Análise por bairro
            print(f"\n🏘️ Atendimentos por bairro:")
            bairros = df['bairro'].value_counts()
            for bairro, count in bairros.head().items():
                print(f"   • {bairro}: {count:,} atendimentos")
        
    finally:
        banco.desconectar()

def main():
    """Função principal com exemplos"""
    print("="*60)
    print("🚀 EXEMPLOS DE USO DO BANCO SQLite MIGRADO")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # Executar exemplos
    exemplo_uso_basico()
    exemplo_analise_avancada() 
    exemplo_pandas()
    
    print("\n" + "="*60)
    print("✅ EXEMPLOS CONCLUÍDOS!")
    print("📚 Use essas funções como base para suas aplicações")
    print("="*60)

if __name__ == "__main__":
    main()