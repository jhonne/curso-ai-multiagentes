"""
Dados Médicos Simulados para Aula 7
=====================================

Este arquivo contém dados simulados baseados na estrutura real do sistema de saúde do Piauí.
Implementação didática usando SQLite em memória para demonstrar conceitos de:
- Integração agentes CrewAI com banco de dados
- Consultas otimizadas em sistemas médicos
- Geolocalização e classificação de urgência

Nota: Os conceitos aqui demonstrados serão aplicados com PostgreSQL real na Aula 8.
"""

import sqlite3
import os
from typing import List, Dict, Any
import math

class DadosMedicos:
    """Classe para gerenciar dados médicos simulados"""
    
    def __init__(self):
        self.db_path = ":memory:"  # Banco em memória para simulação
        self._criar_banco()
        self._inserir_dados_exemplo()
    
    def _criar_banco(self):
        """Cria estrutura do banco de dados simulado"""
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Para retornar dicionários
        cursor = self.conn.cursor()
        
        # Tabela de estabelecimentos de saúde
        cursor.execute("""
        CREATE TABLE estabelecimentos (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            tipo TEXT NOT NULL,
            latitude REAL NOT NULL,
            longitude REAL NOT NULL,
            municipio TEXT NOT NULL,
            telefone TEXT,
            endereco TEXT,
            horario_funcionamento TEXT DEFAULT '24h'
        )
        """)
        
        # Tabela de queixas principais
        cursor.execute("""
        CREATE TABLE queixas_principais (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            descricao TEXT,
            nivel_urgencia INTEGER DEFAULT 2
        )
        """)
        
        # Tabela de sintomas
        cursor.execute("""
        CREATE TABLE sintomas (
            id INTEGER PRIMARY KEY,
            nome TEXT NOT NULL,
            criticidade INTEGER DEFAULT 2,
            descricao TEXT
        )
        """)
        
        # Tabela de relacionamento queixa-sintoma
        cursor.execute("""
        CREATE TABLE queixa_sintoma (
            queixa_id INTEGER,
            sintoma_id INTEGER,
            FOREIGN KEY (queixa_id) REFERENCES queixas_principais (id),
            FOREIGN KEY (sintoma_id) REFERENCES sintomas (id)
        )
        """)
        
        self.conn.commit()
    
    def _inserir_dados_exemplo(self):
        """Insere dados de exemplo baseados na realidade do Piauí"""
        cursor = self.conn.cursor()
        
        # Estabelecimentos de saúde (baseado em Teresina e região)
        estabelecimentos = [
            (1, "Hospital de Urgência de Teresina", "HOSPITAL", -5.0892, -42.8019, "Teresina", "(86) 3216-1000", "Rua Olavo Bilac, 2335 - Centro", "24h"),
            (2, "UPA Promorar", "UPA", -5.0650, -42.7850, "Teresina", "(86) 3215-7800", "Av. Promorar, 1500 - Promorar", "24h"),
            (3, "Hospital São Marcos", "HOSPITAL", -5.0950, -42.7890, "Teresina", "(86) 3216-2000", "Rua Senador Teodoro Pacheco, 2267", "24h"),
            (4, "UPA Cidade Verde", "UPA", -5.0450, -42.7650, "Teresina", "(86) 3215-7900", "Av. Cidade Verde, 800", "24h"),
            (5, "Hospital Regional de Parnaíba", "HOSPITAL", -2.9048, -41.7767, "Parnaíba", "(86) 3321-3000", "Av. São Sebastião, 2000", "24h"),
            (6, "UBS Vila Operária", "UBS", -5.0800, -42.8100, "Teresina", "(86) 3215-8000", "Rua da Paz, 100 - Vila Operária", "06h-18h"),
            (7, "Hospital Municipal de Picos", "HOSPITAL", -7.0759, -41.4669, "Picos", "(89) 3422-1000", "Rua Major Luiz Antônio, 500", "24h"),
            (8, "UPA Norte", "UPA", -5.0500, -42.8200, "Teresina", "(86) 3215-7700", "Av. Universitária, 1200", "24h"),
            (9, "Hospital Dr. João Machado", "HOSPITAL", -8.7619, -40.5008, "Petrolina", "(87) 3866-5000", "Av. Cardoso de Sá, 789", "24h"),
            (10, "UBS Centro", "UBS", -5.0920, -42.8050, "Teresina", "(86) 3215-8100", "Praça da Bandeira, 50", "06h-18h")
        ]
        
        cursor.executemany("""
        INSERT INTO estabelecimentos 
        (id, nome, tipo, latitude, longitude, municipio, telefone, endereco, horario_funcionamento)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, estabelecimentos)
        
        # Queixas principais (baseado em dados reais do SUS)
        queixas = [
            (1, "CEFALEIA", "Dor de cabeça", 2),
            (2, "DOR NO PEITO", "Dor torácica", 5),
            (3, "FEBRE", "Elevação da temperatura corporal", 3),
            (4, "DOR ABDOMINAL", "Dor na região do abdome", 3),
            (5, "FALTA DE AR", "Dificuldade respiratória", 4),
            (6, "NÁUSEA", "Enjoo", 2),
            (7, "TONTURA", "Vertigem ou desequilíbrio", 2),
            (8, "ALERGIA", "Reação alérgica", 3),
            (9, "TRAUMA", "Lesão por acidente", 4),
            (10, "CONVULSÕES", "Episódio convulsivo", 5)
        ]
        
        cursor.executemany("""
        INSERT INTO queixas_principais (id, nome, descricao, nivel_urgencia)
        VALUES (?, ?, ?, ?)
        """, queixas)
        
        # Sintomas
        sintomas = [
            (1, "DOR INTENSA", 4, "Dor severa que interfere nas atividades"),
            (2, "FEBRE ALTA", 3, "Temperatura acima de 38.5°C"),
            (3, "VÔMITO", 2, "Episódios de vômito"),
            (4, "DIFICULDADE RESPIRATÓRIA", 4, "Falta de ar ou respiração laboriosa"),
            (5, "PERDA DE CONSCIÊNCIA", 5, "Desmaio ou alteração do nível de consciência"),
            (6, "SUDORESE", 2, "Suor excessivo"),
            (7, "PALPITAÇÕES", 3, "Batimentos cardíacos acelerados"),
            (8, "SANGRAMENTO", 4, "Hemorragia ativa"),
            (9, "INCHAÇO", 2, "Edema em membros"),
            (10, "FRAQUEZA", 2, "Sensação de fraqueza generalizada")
        ]
        
        cursor.executemany("""
        INSERT INTO sintomas (id, nome, criticidade, descricao)
        VALUES (?, ?, ?, ?)
        """, sintomas)
        
        # Relacionamentos queixa-sintoma
        relacionamentos = [
            (1, 1), (1, 6),  # CEFALEIA -> DOR INTENSA, SUDORESE
            (2, 1), (2, 4), (2, 7),  # DOR NO PEITO -> DOR INTENSA, DIFICULDADE RESPIRATÓRIA, PALPITAÇÕES
            (3, 2), (3, 10),  # FEBRE -> FEBRE ALTA, FRAQUEZA
            (4, 1), (4, 3),  # DOR ABDOMINAL -> DOR INTENSA, VÔMITO
            (5, 4), (5, 7),  # FALTA DE AR -> DIFICULDADE RESPIRATÓRIA, PALPITAÇÕES
            (6, 3),  # NÁUSEA -> VÔMITO
            (7, 5), (7, 10),  # TONTURA -> PERDA DE CONSCIÊNCIA, FRAQUEZA
            (9, 8), (9, 1),  # TRAUMA -> SANGRAMENTO, DOR INTENSA
            (10, 5)  # CONVULSÕES -> PERDA DE CONSCIÊNCIA
        ]
        
        cursor.executemany("""
        INSERT INTO queixa_sintoma (queixa_id, sintoma_id)
        VALUES (?, ?)
        """, relacionamentos)
        
        self.conn.commit()
    
    def calcular_distancia(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """
        Calcula distância entre duas coordenadas usando fórmula de Haversine
        
        Args:
            lat1, lng1: Latitude e longitude do ponto 1
            lat2, lng2: Latitude e longitude do ponto 2
            
        Returns:
            Distância em quilômetros
        """
        # Converter para radianos
        lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])
        
        # Fórmula de Haversine
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng/2)**2
        c = 2 * math.asin(math.sqrt(a))
        
        # Raio da Terra em km
        r = 6371
        
        return c * r
    
    def buscar_estabelecimentos_proximos(self, latitude: float, longitude: float, 
                                       raio_km: float = 10, tipo: str = None) -> List[Dict]:
        """
        Busca estabelecimentos próximos a uma coordenada
        
        Args:
            latitude, longitude: Coordenadas do ponto de referência
            raio_km: Raio de busca em quilômetros
            tipo: Tipo de estabelecimento (opcional)
            
        Returns:
            Lista de estabelecimentos ordenados por distância
        """
        cursor = self.conn.cursor()
        
        if tipo:
            cursor.execute("""
            SELECT * FROM estabelecimentos WHERE tipo = ?
            """, (tipo,))
        else:
            cursor.execute("SELECT * FROM estabelecimentos")
        
        estabelecimentos = cursor.fetchall()
        
        # Calcular distâncias e filtrar por raio
        resultados = []
        for est in estabelecimentos:
            distancia = self.calcular_distancia(
                latitude, longitude, est['latitude'], est['longitude']
            )
            
            if distancia <= raio_km:
                resultado = dict(est)
                resultado['distancia_km'] = round(distancia, 2)
                resultados.append(resultado)
        
        # Ordenar por distância
        resultados.sort(key=lambda x: x['distancia_km'])
        
        return resultados
    
    def buscar_sintomas_por_queixa(self, queixa_nome: str) -> List[Dict]:
        """Busca sintomas relacionados a uma queixa principal"""
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT s.* FROM sintomas s
        JOIN queixa_sintoma qs ON s.id = qs.sintoma_id
        JOIN queixas_principais q ON q.id = qs.queixa_id
        WHERE q.nome = ?
        """, (queixa_nome.upper(),))
        
        return [dict(row) for row in cursor.fetchall()]
    
    def classificar_urgencia_sintomas(self, sintomas_texto: str) -> Dict:
        """
        Classifica urgência baseado em sintomas mencionados
        
        Args:
            sintomas_texto: Texto descrevendo sintomas
            
        Returns:
            Dict com classificação de urgência e recomendações
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM sintomas")
        sintomas_db = cursor.fetchall()
        
        # Buscar sintomas mencionados no texto
        sintomas_encontrados = []
        urgencia_maxima = 1
        
        for sintoma in sintomas_db:
            if sintoma['nome'].lower() in sintomas_texto.lower():
                sintomas_encontrados.append(dict(sintoma))
                urgencia_maxima = max(urgencia_maxima, sintoma['criticidade'])
        
        # Classificação de urgência
        if urgencia_maxima >= 5:
            classificacao = "EMERGÊNCIA"
            recomendacao = "Procure atendimento IMEDIATAMENTE ou chame SAMU"
        elif urgencia_maxima >= 4:
            classificacao = "URGENTE"
            recomendacao = "Procure UPA ou Hospital rapidamente"
        elif urgencia_maxima >= 3:
            classificacao = "MODERADO"
            recomendacao = "Procure UPA ou agende consulta"
        elif urgencia_maxima >= 2:
            classificacao = "LEVE"
            recomendacao = "Pode procurar UBS ou agendar consulta"
        else:
            classificacao = "NÃO CLASSIFICADO"
            recomendacao = "Descreva os sintomas com mais detalhes"
        
        return {
            'sintomas_encontrados': sintomas_encontrados,
            'nivel_urgencia': urgencia_maxima,
            'classificacao': classificacao,
            'recomendacao': recomendacao
        }
    
    def get_estatisticas(self) -> Dict:
        """Retorna estatísticas dos dados médicos"""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM estabelecimentos")
        total_estabelecimentos = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM queixas_principais")
        total_queixas = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM sintomas")
        total_sintomas = cursor.fetchone()['total']
        
        cursor.execute("SELECT tipo, COUNT(*) as quantidade FROM estabelecimentos GROUP BY tipo")
        tipos_estabelecimentos = {row['tipo']: row['quantidade'] for row in cursor.fetchall()}
        
        return {
            'total_estabelecimentos': total_estabelecimentos,
            'total_queixas': total_queixas,
            'total_sintomas': total_sintomas,
            'tipos_estabelecimentos': tipos_estabelecimentos
        }
    
    def __del__(self):
        """Fecha conexão com banco ao destruir objeto"""
        if hasattr(self, 'conn'):
            self.conn.close()


# Instância global para uso nos exemplos
dados_medicos = DadosMedicos()


def exemplo_uso():
    """Demonstra como usar a classe DadosMedicos"""
    print("🏥 DADOS MÉDICOS SIMULADOS - EXEMPLO DE USO")
    print("=" * 50)
    
    # Estatísticas gerais
    stats = dados_medicos.get_estatisticas()
    print(f"📊 Estatísticas:")
    print(f"   • {stats['total_estabelecimentos']} estabelecimentos")
    print(f"   • {stats['total_queixas']} queixas principais")
    print(f"   • {stats['total_sintomas']} sintomas catalogados")
    print()
    
    # Busca geográfica (coordenadas de Teresina centro)
    print("🌍 Busca Geográfica - Estabelecimentos próximos ao centro de Teresina:")
    proximos = dados_medicos.buscar_estabelecimentos_proximos(-5.0892, -42.8019, raio_km=5)
    for est in proximos[:3]:
        print(f"   • {est['nome']} ({est['tipo']}) - {est['distancia_km']}km")
    print()
    
    # Análise de sintomas
    print("🔍 Análise de Sintomas:")
    resultado = dados_medicos.classificar_urgencia_sintomas("dor no peito intensa e falta de ar")
    print(f"   • Urgência: {resultado['classificacao']} (nível {resultado['nivel_urgencia']})")
    print(f"   • Recomendação: {resultado['recomendacao']}")
    print(f"   • Sintomas encontrados: {len(resultado['sintomas_encontrados'])}")


if __name__ == "__main__":
    exemplo_uso()