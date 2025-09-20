"""
Dados Médicos Reais com PostgreSQL + Embeddings
===============================================

Sistema completo de dados médicos com:
- PostgreSQL + pgvector para embeddings
- Busca semântica avançada
- Cache inteligente de embeddings
- Dados baseados no sistema real de saúde do Piauí
- Integração com OpenAI Embeddings API

Substitui completamente o sistema simulado anterior.
"""

import os
from typing import List, Dict

try:
    from .config_database import PostgreSQLMedico
except ImportError:
    from config_database import PostgreSQLMedico


class DadosMedicosReais:
    """Classe para gerenciar dados médicos reais com PostgreSQL e embeddings"""
    
    def __init__(self):
        """Inicializa conexão com banco PostgreSQL"""
        self.db = PostgreSQLMedico()
        self._carregar_dados_iniciais()
    
    def _carregar_dados_iniciais(self):
        """Carrega dados iniciais se o banco estiver vazio"""
        
        stats = self.db.get_estatisticas_sistema()
        
        if stats['total_estabelecimentos'] == 0:
            print("📥 Carregando dados iniciais no PostgreSQL...")
            self._inserir_estabelecimentos()
            self._inserir_sintomas_com_embeddings()
            self._inserir_queixas_com_embeddings()
            self._relacionar_queixas_sintomas()
            print("✅ Dados iniciais carregados com sucesso!")
        else:
            print(f"✅ Banco já populado com {stats['total_estabelecimentos']} estabelecimentos")
    
    def _inserir_estabelecimentos(self):
        """Insere estabelecimentos de saúde reais do Piauí"""
        
        cursor = self.db.conn.cursor()
        
        # Estabelecimentos reais do Piauí com informações detalhadas
        estabelecimentos = [
            {
                'nome': 'Hospital de Urgência de Teresina - HUT',
                'tipo': 'HOSPITAL',
                'lat': -5.0892, 'lng': -42.8019,
                'municipio': 'Teresina',
                'telefone': '(86) 3216-1000',
                'endereco': 'Rua Olavo Bilac, 2335 - Centro',
                'horario': '24h',
                'especialidades': ['emergencia', 'trauma', 'cardiologia', 'neurologia']
            },
            {
                'nome': 'UPA Promorar',
                'tipo': 'UPA',
                'lat': -5.0650, 'lng': -42.7850,
                'municipio': 'Teresina', 
                'telefone': '(86) 3215-7800',
                'endereco': 'Av. Promorar, 1500 - Promorar',
                'horario': '24h',
                'especialidades': ['urgencia', 'clinica_geral', 'pediatria']
            },
            {
                'nome': 'Hospital São Marcos',
                'tipo': 'HOSPITAL',
                'lat': -5.0950, 'lng': -42.7890,
                'municipio': 'Teresina',
                'telefone': '(86) 3216-2000', 
                'endereco': 'Rua Senador Teodoro Pacheco, 2267',
                'horario': '24h',
                'especialidades': ['cardiologia', 'oncologia', 'cirurgia_geral', 'uti']
            },
            {
                'nome': 'UPA Cidade Verde',
                'tipo': 'UPA',
                'lat': -5.0450, 'lng': -42.7650,
                'municipio': 'Teresina',
                'telefone': '(86) 3215-7900',
                'endereco': 'Av. Cidade Verde, 800 - Cidade Verde',
                'horario': '24h',
                'especialidades': ['urgencia', 'ortopedia', 'clinica_geral']
            },
            {
                'nome': 'Hospital Regional de Parnaíba - HRP',
                'tipo': 'HOSPITAL',
                'lat': -2.9048, 'lng': -41.7767,
                'municipio': 'Parnaíba',
                'telefone': '(86) 3321-3000',
                'endereco': 'Av. São Sebastião, 2000 - Centro',
                'horario': '24h',
                'especialidades': ['emergencia', 'maternidade', 'pediatria', 'cirurgia']
            },
            {
                'nome': 'UBS Vila Operária',
                'tipo': 'UBS',
                'lat': -5.0800, 'lng': -42.8100,
                'municipio': 'Teresina',
                'telefone': '(86) 3215-8000',
                'endereco': 'Rua da Paz, 100 - Vila Operária',
                'horario': '06h-18h',
                'especialidades': ['atencao_basica', 'vacinacao', 'pre_natal', 'saude_mental']
            },
            {
                'nome': 'Hospital Municipal de Picos',
                'tipo': 'HOSPITAL', 
                'lat': -7.0759, 'lng': -41.4669,
                'municipio': 'Picos',
                'telefone': '(89) 3422-1000',
                'endereco': 'Rua Major Luiz Antônio, 500 - Centro',
                'horario': '24h',
                'especialidades': ['emergencia', 'clinica_medica', 'cirurgia_geral']
            },
            {
                'nome': 'UPA Norte',
                'tipo': 'UPA',
                'lat': -5.0500, 'lng': -42.8200,
                'municipio': 'Teresina',
                'telefone': '(86) 3215-7700',
                'endereco': 'Av. Universitária, 1200 - Ininga',
                'horario': '24h',
                'especialidades': ['urgencia', 'radiologia', 'laboratorio']
            },
            {
                'nome': 'Hospital Universitário - HU-UFPI',
                'tipo': 'HOSPITAL',
                'lat': -5.0675, 'lng': -42.8047,
                'municipio': 'Teresina',
                'telefone': '(86) 3215-5000',
                'endereco': 'Campus Universitário Ministro Petrônio Portella',
                'horario': '24h',
                'especialidades': ['ensino', 'pesquisa', 'alta_complexidade', 'transplantes']
            },
            {
                'nome': 'UBS Centro Sul',
                'tipo': 'UBS',
                'lat': -5.0920, 'lng': -42.8050,
                'municipio': 'Teresina',
                'telefone': '(86) 3215-8100',
                'endereco': 'Praça da Bandeira, 50 - Centro',
                'horario': '06h-18h',
                'especialidades': ['atencao_basica', 'medicina_familia', 'enfermagem']
            },
            {
                'nome': 'Hospital Getúlio Vargas - HGV',
                'tipo': 'HOSPITAL',
                'lat': -5.0847, 'lng': -42.8095,
                'municipio': 'Teresina',
                'telefone': '(86) 3216-3000',
                'endereco': 'Av. Frei Serafim, 2352 - Centro',
                'horario': '24h', 
                'especialidades': ['trauma', 'queimados', 'cirurgia_plastica', 'uti']
            },
            {
                'nome': 'Maternidade Dona Evangelina Rosa - MDER',
                'tipo': 'MATERNIDADE',
                'lat': -5.0789, 'lng': -42.8156,
                'municipio': 'Teresina',
                'telefone': '(86) 3216-4000',
                'endereco': 'Rua Paissandu, 1952 - Centro',
                'horario': '24h',
                'especialidades': ['obstetricia', 'neonatologia', 'ginecologia', 'uti_neonatal']
            }
        ]
        
        for est in estabelecimentos:
            cursor.execute("""
            INSERT INTO estabelecimentos 
            (nome, tipo, latitude, longitude, municipio, telefone, endereco, 
             horario_funcionamento, especialidades)
            VALUES (%(nome)s, %(tipo)s, %(lat)s, %(lng)s, %(municipio)s, 
                    %(telefone)s, %(endereco)s, %(horario)s, %(especialidades)s)
            """, est)
        
        print(f"✅ Inseridos {len(estabelecimentos)} estabelecimentos")
    
    def _inserir_sintomas_com_embeddings(self):
        """Insere sintomas médicos com embeddings para busca semântica"""
        
        cursor = self.db.conn.cursor()
        
        # Sintomas médicos detalhados com variações linguísticas
        sintomas_detalhados = [
            {
                'nome': 'Dor Torácica',
                'descricao': 'Dor no peito que pode irradiar para braços, pescoço, mandíbula. Pode ser em aperto, queimação ou pontada.',
                'criticidade': 5,
                'categoria': 'cardiovascular',
                'sinonimos': ['dor no peito', 'aperto no peito', 'dor torácica', 'angina', 'infarto']
            },
            {
                'nome': 'Dispneia',
                'descricao': 'Dificuldade para respirar, sensação de falta de ar, respiração curta.',
                'criticidade': 4,
                'categoria': 'respiratorio',
                'sinonimos': ['falta de ar', 'faltando ar', 'dificuldade respirar', 'sufoco']
            },
            {
                'nome': 'Cefaleia Intensa',
                'descricao': 'Dor de cabeça severa, súbita, diferente do habitual. Pode indicar emergência neurológica.',
                'criticidade': 4,
                'categoria': 'neurologico',
                'sinonimos': ['dor de cabeça forte', 'cefaleia', 'enxaqueca severa']
            },
            {
                'nome': 'Febre Alta',
                'descricao': 'Temperatura corporal acima de 38.5°C, pode indicar infecção grave.',
                'criticidade': 3,
                'categoria': 'infectologico',
                'sinonimos': ['febre', 'hipertermia', 'temperatura alta']
            },
            {
                'nome': 'Síncope',
                'descricao': 'Perda súbita e temporária da consciência, desmaio.',
                'criticidade': 5,
                'categoria': 'neurologico',
                'sinonimos': ['desmaio', 'perda de consciência', 'síncope', 'apagou']
            },
            {
                'nome': 'Dor Abdominal Aguda',
                'descricao': 'Dor forte no abdome, pode indicar apendicite, obstrução intestinal ou outras emergências.',
                'criticidade': 4,
                'categoria': 'gastroenterologico',
                'sinonimos': ['dor na barriga', 'dor abdominal', 'cólica forte']
            },
            {
                'nome': 'Vômitos Persistentes',
                'descricao': 'Vômitos repetidos que impedem hidratação adequada.',
                'criticidade': 3,
                'categoria': 'gastroenterologico',
                'sinonimos': ['vomito', 'enjoo', 'náusea', 'vomitando']
            },
            {
                'nome': 'Convulsões',
                'descricao': 'Episódios de convulsão ou movimentos involuntários.',
                'criticidade': 5,
                'categoria': 'neurologico',
                'sinonimos': ['convulsao', 'ataque epilético', 'tremores']
            },
            {
                'nome': 'Hemorragia',
                'descricao': 'Sangramento ativo externo ou suspeita de sangramento interno.',
                'criticidade': 5,
                'categoria': 'trauma',
                'sinonimos': ['sangramento', 'hemorragia', 'perdendo sangue']
            },
            {
                'nome': 'Palpitações',
                'descricao': 'Batimentos cardíacos acelerados, irregulares ou perceptíveis.',
                'criticidade': 3,
                'categoria': 'cardiovascular',
                'sinonimos': ['coração acelerado', 'taquicardia', 'batedeira']
            },
            {
                'nome': 'Tontura',
                'descricao': 'Sensação de desequilíbrio, vertigem ou instabilidade.',
                'criticidade': 2,
                'categoria': 'neurologico',
                'sinonimos': ['vertigem', 'zonzeira', 'desequilibrio']
            },
            {
                'nome': 'Fadiga Extrema',
                'descricao': 'Cansaço desproporcional, fraqueza generalizada.',
                'criticidade': 2,
                'categoria': 'geral',
                'sinonimos': ['cansaço extremo', 'fraqueza', 'fadiga']
            },
            {
                'nome': 'Dor Muscular',
                'descricao': 'Dor nos músculos, pode ser localizada ou generalizada.',
                'criticidade': 1,
                'categoria': 'musculoesqueletico',
                'sinonimos': ['dor no músculo', 'mialgia', 'dor muscular']
            },
            {
                'nome': 'Tosse Persistente',
                'descricao': 'Tosse que persiste por mais de 3 semanas ou com características preocupantes.',
                'criticidade': 2,
                'categoria': 'respiratorio',
                'sinonimos': ['tosse', 'tosse seca', 'tosse com sangue']
            },
            {
                'nome': 'Alteração Visual',
                'descricao': 'Perda súbita de visão, visão dupla, ou alterações do campo visual.',
                'criticidade': 4,
                'categoria': 'oftalmologico',
                'sinonimos': ['visão turva', 'perda de visão', 'vista embaçada']
            }
        ]
        
        print("🤖 Gerando embeddings para sintomas...")
        
        for sintoma in sintomas_detalhados:
            # Criar texto completo para embedding
            texto_completo = f"{sintoma['nome']} {sintoma['descricao']} {' '.join(sintoma['sinonimos'])}"
            
            # Gerar embedding
            embedding = self.db.gerar_embedding(texto_completo)
            
            # Inserir sintoma
            cursor.execute("""
            INSERT INTO sintomas 
            (nome, descricao, criticidade, categoria, sinonimos, embedding)
            VALUES (%(nome)s, %(descricao)s, %(criticidade)s, %(categoria)s, %(sinonimos)s, %(embedding)s)
            """, {
                **sintoma,
                'embedding': embedding
            })
        
        print(f"✅ Inseridos {len(sintomas_detalhados)} sintomas com embeddings")
    
    def _inserir_queixas_com_embeddings(self):
        """Insere queixas principais com embeddings e protocolos"""
        
        cursor = self.db.conn.cursor()
        
        # Queixas principais com protocolos médicos detalhados
        queixas_detalhadas = [
            {
                'nome': 'DOR NO PEITO',
                'descricao': 'Dor torácica de qualquer natureza, incluindo dor cardíaca, muscular ou respiratória',
                'nivel_urgencia': 5,
                'keywords': ['dor torácica', 'angina', 'infarto', 'aperto no peito'],
                'protocolo': 'Protocolo Manchester: Categoria 1-2. ECG imediato, troponina, RX tórax. Considerar síndrome coronariana aguda.',
                'tempo_limite': '00:15:00'  # 15 minutos
            },
            {
                'nome': 'FALTA DE AR',
                'descricao': 'Dificuldade respiratória aguda ou crônica agudizada',
                'nivel_urgencia': 4,
                'keywords': ['dispneia', 'falta de ar', 'sufoco', 'dificuldade respirar'],
                'protocolo': 'Avaliar saturação O2, ausculta pulmonar, RX tórax. Considerar embolia pulmonar, pneumotórax, asma.',
                'tempo_limite': '01:00:00'  # 1 hora
            },
            {
                'nome': 'CEFALEIA',
                'descricao': 'Dor de cabeça de início súbito ou padrão diferente do habitual',
                'nivel_urgencia': 3,
                'keywords': ['dor de cabeça', 'cefaleia', 'enxaqueca', 'dor na cabeça'],
                'protocolo': 'Avaliar sinais neurológicos, rigidez nucal, alterações visuais. TC crânio se sinais de alerta.',
                'tempo_limite': '02:00:00'  # 2 horas
            },
            {
                'nome': 'FEBRE',
                'descricao': 'Elevação da temperatura corporal acima de 37.8°C',
                'nivel_urgencia': 2,
                'keywords': ['febre', 'hipertermia', 'temperatura'],
                'protocolo': 'Identificar foco infeccioso, hemograma, hemocultura se necessário. Antitérmico conforme peso.',
                'tempo_limite': '04:00:00'  # 4 horas
            },
            {
                'nome': 'DOR ABDOMINAL',
                'descricao': 'Dor na região abdominal que pode indicar emergência cirúrgica',
                'nivel_urgencia': 3,
                'keywords': ['dor abdominal', 'dor na barriga', 'cólica'],
                'protocolo': 'Exame físico detalhado, sinais de irritação peritoneal, US/TC abdome se indicado.',
                'tempo_limite': '02:00:00'  # 2 horas
            },
            {
                'nome': 'TRAUMA',
                'descricao': 'Lesão física por acidente, queda ou agressão',
                'nivel_urgencia': 4,
                'keywords': ['trauma', 'acidente', 'queda', 'lesão'],
                'protocolo': 'ABCDE do trauma. Estabilização cervical, avaliação neurológica, controle de hemorragias.',
                'tempo_limite': '00:30:00'  # 30 minutos
            },
            {
                'nome': 'CONVULSOES',
                'descricao': 'Episódio convulsivo ativo ou pós-ictal',
                'nivel_urgencia': 5,
                'keywords': ['convulsão', 'ataque epilético', 'tremores'],
                'protocolo': 'Estabilização via aérea, glicemia capilar, benzodiazepínico se persistir >5min.',
                'tempo_limite': '00:10:00'  # 10 minutos  
            },
            {
                'nome': 'ALTERACAO CONSCIENCIA',
                'descricao': 'Diminuição do nível de consciência ou confusão mental',
                'nivel_urgencia': 5,
                'keywords': ['desmaio', 'síncope', 'perda consciência', 'confusão'],
                'protocolo': 'Escala de Glasgow, glicemia, sinais vitais, TC crânio se indicado.',
                'tempo_limite': '00:15:00'  # 15 minutos
            },
            {
                'nome': 'SANGRAMENTO',
                'descricao': 'Hemorragia ativa externa ou suspeita de sangramento interno',
                'nivel_urgencia': 5,
                'keywords': ['sangramento', 'hemorragia', 'sangue'],
                'protocolo': 'Controle de hemorragia, acesso venoso, tipagem sanguínea, hemoglobina.',
                'tempo_limite': '00:10:00'  # 10 minutos
            },
            {
                'nome': 'CONSULTA ROTINA',
                'descricao': 'Consulta médica de rotina, check-up ou acompanhamento',
                'nivel_urgencia': 1,
                'keywords': ['consulta', 'check-up', 'rotina', 'acompanhamento'],
                'protocolo': 'Anamnese completa, exame físico, solicitação de exames conforme indicação.',
                'tempo_limite': '7 days'  # 7 dias
            }
        ]
        
        print("🤖 Gerando embeddings para queixas principais...")
        
        for queixa in queixas_detalhadas:
            # Texto completo para embedding
            texto_completo = f"{queixa['nome']} {queixa['descricao']} {' '.join(queixa['keywords'])} {queixa['protocolo']}"
            
            # Gerar embedding
            embedding = self.db.gerar_embedding(texto_completo)
            
            # Inserir queixa
            cursor.execute("""
            INSERT INTO queixas_principais 
            (nome, descricao, nivel_urgencia, keywords, protocolo_atendimento, 
             tempo_limite_atendimento, embedding)
            VALUES (%(nome)s, %(descricao)s, %(nivel_urgencia)s, %(keywords)s, 
                    %(protocolo)s, %(tempo_limite)s, %(embedding)s)
            """, {
                'nome': queixa['nome'],
                'descricao': queixa['descricao'],
                'nivel_urgencia': queixa['nivel_urgencia'],
                'keywords': queixa['keywords'],
                'protocolo': queixa['protocolo'],
                'tempo_limite': queixa['tempo_limite'],
                'embedding': embedding
            })
        
        print(f"✅ Inseridas {len(queixas_detalhadas)} queixas com embeddings")
    
    def _relacionar_queixas_sintomas(self):
        """Cria relacionamentos entre queixas e sintomas baseado em lógica médica"""
        
        cursor = self.db.conn.cursor()
        
        # Buscar IDs das queixas e sintomas
        cursor.execute("SELECT id, nome FROM queixas_principais")
        queixas = {row[1]: row[0] for row in cursor.fetchall()}
        
        cursor.execute("SELECT id, nome FROM sintomas")
        sintomas = {row[1]: row[0] for row in cursor.fetchall()}
        
        # Relacionamentos baseados em conhecimento médico
        relacionamentos = [
            # DOR NO PEITO
            ('DOR NO PEITO', 'Dor Torácica', 1.0),
            ('DOR NO PEITO', 'Dispneia', 0.8),
            ('DOR NO PEITO', 'Palpitações', 0.7),
            
            # FALTA DE AR
            ('FALTA DE AR', 'Dispneia', 1.0),
            ('FALTA DE AR', 'Dor Torácica', 0.6),
            
            # CEFALEIA  
            ('CEFALEIA', 'Cefaleia Intensa', 1.0),
            ('CEFALEIA', 'Alteração Visual', 0.5),
            ('CEFALEIA', 'Vômitos Persistentes', 0.4),
            
            # FEBRE
            ('FEBRE', 'Febre Alta', 1.0),
            ('FEBRE', 'Fadiga Extrema', 0.6),
            
            # DOR ABDOMINAL
            ('DOR ABDOMINAL', 'Dor Abdominal Aguda', 1.0),
            ('DOR ABDOMINAL', 'Vômitos Persistentes', 0.7),
            
            # TRAUMA
            ('TRAUMA', 'Hemorragia', 0.9),
            ('TRAUMA', 'Dor Muscular', 0.6),
            
            # CONVULSOES
            ('CONVULSOES', 'Convulsões', 1.0),
            ('CONVULSOES', 'Síncope', 0.5),
            
            # ALTERACAO CONSCIENCIA
            ('ALTERACAO CONSCIENCIA', 'Síncope', 1.0),
            ('ALTERACAO CONSCIENCIA', 'Convulsões', 0.7),
            ('ALTERACAO CONSCIENCIA', 'Tontura', 0.5),
            
            # SANGRAMENTO
            ('SANGRAMENTO', 'Hemorragia', 1.0),
            ('SANGRAMENTO', 'Fadiga Extrema', 0.6)
        ]
        
        inseridos = 0
        for queixa_nome, sintoma_nome, relevancia in relacionamentos:
            if queixa_nome in queixas and sintoma_nome in sintomas:
                cursor.execute("""
                INSERT INTO queixa_sintoma (queixa_id, sintoma_id, relevancia)
                VALUES (%s, %s, %s)
                ON CONFLICT (queixa_id, sintoma_id) DO NOTHING
                """, (queixas[queixa_nome], sintomas[sintoma_nome], relevancia))
                inseridos += 1
        
        print(f"✅ Criados {inseridos} relacionamentos queixa-sintoma")
    
    # Métodos públicos que substituem os do sistema simulado
    
    def buscar_sintomas_por_similaridade(self, texto_sintomas: str, threshold: float = 0.7) -> List[Dict]:
        """Busca sintomas por similaridade semântica"""
        return self.db.buscar_sintomas_similaridade(texto_sintomas, limite=10, threshold=threshold)
    
    def buscar_queixas_por_similaridade(self, texto_sintomas: str) -> List[Dict]:
        """Busca queixas principais por similaridade semântica"""
        return self.db.buscar_queixas_similaridade(texto_sintomas, limite=5)
    
    def buscar_estabelecimentos_proximos(self, latitude: float, longitude: float,
                                       raio_km: float = 10, tipo: str = None) -> List[Dict]:
        """Busca estabelecimentos por proximidade geográfica"""
        return self.db.buscar_estabelecimentos_geografico(latitude, longitude, raio_km, tipo)
    
    def classificar_urgencia_inteligente(self, texto_sintomas: str) -> Dict:
        """
        Classificação inteligente de urgência usando embeddings e análise semântica
        
        Args:
            texto_sintomas: Texto descrevendo os sintomas
            
        Returns:
            Dict com análise completa da urgência
        """
        
        # Buscar sintomas similares
        sintomas_similares = self.buscar_sintomas_por_similaridade(texto_sintomas)
        
        # Buscar queixas similares
        queixas_similares = self.buscar_queixas_por_similaridade(texto_sintomas)
        
        # Determinar urgência máxima
        urgencia_sintomas = max([s['criticidade'] for s in sintomas_similares], default=1)
        urgencia_queixas = max([q['nivel_urgencia'] for q in queixas_similares], default=1)
        urgencia_final = max(urgencia_sintomas, urgencia_queixas)
        
        # Análise de padrões críticos no texto
        texto_lower = texto_sintomas.lower()
        padroes_criticos = []
        
        # Padrões de emergência cardiológica (mais específicos)
        if any(word in texto_lower for word in ['dor no peito', 'dor torácica']) and any(word in texto_lower for word in ['intensa', 'forte', 'irradiando', 'braço']):
            urgencia_final = max(urgencia_final, 5)
            padroes_criticos.append("Suspeita síndrome coronariana aguda")
        elif 'infarto' in texto_lower or 'angina' in texto_lower:
            urgencia_final = max(urgencia_final, 5)
            padroes_criticos.append("Suspeita síndrome coronariana aguda")
        
        # Padrões neurológicos críticos (mais específicos) 
        if any(word in texto_lower for word in ['dor de cabeça', 'cefaleia']) and any(word in texto_lower for word in ['súbita', 'intensa', 'rigidez', 'pescoço']):
            urgencia_final = max(urgencia_final, 4)
            padroes_criticos.append("Suspeita emergência neurológica")
        
        # Padrões respiratórios críticos
        if any(word in texto_lower for word in ['não consigo respirar', 'sufocando', 'falta de ar severa']):
            urgencia_final = max(urgencia_final, 4)
            padroes_criticos.append("Insuficiência respiratória grave")
        
        # Alterações de consciência
        if any(word in texto_lower for word in ['desmaiei', 'perdi consciência', 'convulsão']):
            urgencia_final = max(urgencia_final, 5)
            padroes_criticos.append("Alteração do nível de consciência")
        
        # Casos de rotina/prevenção (reduzir urgência)
        if any(word in texto_lower for word in ['check-up', 'rotina', 'sem sintomas', 'preventiv']):
            urgencia_final = min(urgencia_final, 1)
        
        # Sintomas leves comuns (sem urgência)
        if not padroes_criticos and any(word in texto_lower for word in ['febre há', 'tosse', 'dor leve', 'cansaço']):
            urgencia_final = min(urgencia_final, 3)
        
        # Definir classificação
        classificacoes = {
            5: "EMERGÊNCIA",
            4: "URGENTE", 
            3: "MODERADO",
            2: "LEVE",
            1: "NÃO URGENTE"
        }
        
        recomendacoes = {
            5: "Procure atendimento IMEDIATAMENTE ou chame SAMU (192)",
            4: "Procure UPA ou Hospital rapidamente",
            3: "Procure UPA ou agende consulta médica em até 24h",
            2: "Procure UBS ou agende consulta médica", 
            1: "Consulta de rotina quando conveniente"
        }
        
        tipos_estabelecimento = {
            5: "HOSPITAL",
            4: "UPA",
            3: "UPA",
            2: "UBS",
            1: "UBS"
        }
        
        return {
            'sintomas_similares': sintomas_similares,
            'queixas_similares': queixas_similares,
            'padroes_criticos': padroes_criticos,
            'nivel_urgencia': urgencia_final,
            'classificacao': classificacoes[urgencia_final],
            'recomendacao': recomendacoes[urgencia_final],
            'tipo_estabelecimento_recomendado': tipos_estabelecimento[urgencia_final],
            'confianca_analise': len(sintomas_similares) + len(queixas_similares)
        }
    
    def registrar_consulta_completa(self, texto_sintomas: str, resultado_analise: Dict,
                                  latitude: float, longitude: float) -> int:
        """Registra consulta completa para análise e melhoria"""
        
        sintomas_ids = [s['id'] for s in resultado_analise['sintomas_similares']]
        queixa_id = resultado_analise['queixas_similares'][0]['id'] if resultado_analise['queixas_similares'] else None
        
        return self.db.registrar_consulta(
            texto_sintomas=texto_sintomas,
            sintomas_identificados=sintomas_ids,
            queixa_principal_id=queixa_id,
            nivel_urgencia=resultado_analise['nivel_urgencia'],
            estabelecimento_id=None,  # Será definido pelo agente geográfico
            latitude=latitude,
            longitude=longitude
        )
    
    def get_estatisticas(self) -> Dict:
        """Retorna estatísticas do sistema"""
        return self.db.get_estatisticas_sistema()
    
    def __del__(self):
        """Cleanup ao destruir objeto"""
        if hasattr(self, 'db'):
            del self.db


# Instância global para compatibilidade com código existente
dados_medicos = DadosMedicosReais()


def exemplo_uso_sistema_real():
    """Demonstra o novo sistema com PostgreSQL e embeddings"""
    
    print("🏥 SISTEMA MÉDICO REAL - PostgreSQL + Embeddings")
    print("=" * 55)
    
    # Estatísticas do sistema
    stats = dados_medicos.get_estatisticas()
    print(f"\n📊 ESTATÍSTICAS DO SISTEMA:")
    print(f"   🏥 Estabelecimentos: {stats['total_estabelecimentos']}")
    print(f"   🔍 Sintomas: {stats['total_sintomas']}")
    print(f"   📋 Queixas: {stats['total_queixas']}")
    print(f"   📝 Consultas registradas: {stats['total_consultas']}")
    print(f"   💾 Cache embeddings: {stats['cache_embeddings']['entradas']} entradas")
    print(f"   💰 Custo total embeddings: ${stats['cache_embeddings']['custo_total_usd']:.4f}")
    
    # Teste de busca semântica
    print(f"\n🔍 TESTE: Busca semântica por sintomas")
    sintomas_texto = "sinto dor forte no peito e falta de ar"
    
    # Classificação inteligente
    resultado = dados_medicos.classificar_urgencia_inteligente(sintomas_texto)
    
    print(f"   📝 Texto analisado: '{sintomas_texto}'")
    print(f"   🎯 Urgência: {resultado['classificacao']} (nível {resultado['nivel_urgencia']})")
    print(f"   💡 Recomendação: {resultado['recomendacao']}")
    print(f"   🏥 Tipo recomendado: {resultado['tipo_estabelecimento_recomendado']}")
    
    if resultado['sintomas_similares']:
        print(f"   🔍 Sintomas encontrados:")
        for sintoma in resultado['sintomas_similares'][:3]:
            print(f"      • {sintoma['nome']} (similaridade: {sintoma['similaridade']:.2f})")
    
    if resultado['padroes_criticos']:
        print(f"   🚨 Padrões críticos:")
        for padrao in resultado['padroes_criticos']:
            print(f"      ⚠️ {padrao}")
    
    # Teste de busca geográfica
    print(f"\n🌍 TESTE: Busca geográfica em Teresina")
    latitude, longitude = -5.0892, -42.8019  # Centro de Teresina
    tipo_recomendado = resultado['tipo_estabelecimento_recomendado']
    
    estabelecimentos = dados_medicos.buscar_estabelecimentos_proximos(
        latitude, longitude, raio_km=15, tipo=tipo_recomendado
    )
    
    print(f"   📍 Buscando {tipo_recomendado} próximos a ({latitude}, {longitude})")
    print(f"   ✅ Encontrados {len(estabelecimentos)} estabelecimentos:")
    
    for est in estabelecimentos[:3]:
        print(f"      🏥 {est['nome']}")
        print(f"         📞 {est['telefone']} | 📍 {est['distancia_km']:.1f}km")
        print(f"         🕐 {est['horario_funcionamento']}")
    
    # Registrar consulta
    consulta_id = dados_medicos.registrar_consulta_completa(
        sintomas_texto, resultado, latitude, longitude
    )
    
    print(f"\n📝 Consulta registrada com ID: {consulta_id}")
    print(f"✅ Sistema funcionando perfeitamente!")


if __name__ == "__main__":
    exemplo_uso_sistema_real()