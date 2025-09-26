#!/usr/bin/env python3
"""
🎓 EXERCÍCIO 2: Interface Melhorada e Funcionalidades Avançadas
===============================================================

OBJETIVO:
Implementar melhorias na interface do sistema interativo e adicionar
funcionalidades mais avançadas como histórico, favoritos e exportação.

NÍVEL: 🟡 INTERMEDIÁRIO

NOVIDADES:
- Histórico de consultas da sessão
- Sistema de favoritos do usuário  
- Exportação de resultados para arquivo
- Interface com cores e formatação melhorada
- Comandos avançados de navegação

EXECUÇÃO:
uv run aula8/exercicios/exercicio2_interface_melhorada.py
"""

import os
import sqlite3
import json
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI

# Configuração
load_dotenv()
PROJECT_ROOT = Path(__file__).parent.parent.parent
DB_PATH = PROJECT_ROOT / "db" / "curso.db"

print("🎓 EXERCÍCIO 2: Interface Melhorada")
print("=" * 45)


class HistoricoSessao:
    """Gerencia histórico de consultas da sessão atual"""
    
    def __init__(self):
        self.consultas = []
        self.favoritos = []
        self.sessao_inicio = datetime.now()
    
    def adicionar_consulta(self, pergunta: str, resposta: str):
        """Adiciona consulta ao histórico"""
        self.consultas.append({
            'timestamp': datetime.now().isoformat(),
            'pergunta': pergunta,
            'resposta': resposta[:200] + '...' if len(resposta) > 200 else resposta
        })
    
    def adicionar_favorito(self, item: str):
        """Adiciona item aos favoritos"""
        if item not in self.favoritos:
            self.favoritos.append(item)
            return True
        return False
    
    def remover_favorito(self, item: str):
        """Remove item dos favoritos"""
        if item in self.favoritos:
            self.favoritos.remove(item)
            return True
        return False
    
    def obter_historico(self) -> str:
        """Retorna histórico formatado"""
        if not self.consultas:
            return "📝 Nenhuma consulta realizada ainda nesta sessão."
        
        resultado = f"📝 HISTÓRICO DA SESSÃO (iniciada em {self.sessao_inicio.strftime('%H:%M')}):\n\n"
        
        for i, consulta in enumerate(self.consultas[-10:], 1):  # Últimas 10
            tempo = datetime.fromisoformat(consulta['timestamp']).strftime('%H:%M:%S')
            resultado += f"{i:2d}. [{tempo}] {consulta['pergunta']}\n"
            resultado += f"    📋 {consulta['resposta']}\n\n"
        
        return resultado
    
    def obter_favoritos(self) -> str:
        """Retorna favoritos formatados"""
        if not self.favoritos:
            return "⭐ Nenhum item favoritado ainda."
        
        resultado = f"⭐ SEUS FAVORITOS ({len(self.favoritos)}):\n\n"
        for i, item in enumerate(self.favoritos, 1):
            resultado += f"{i:2d}. {item}\n"
        
        return resultado
    
    def exportar_sessao(self, arquivo: str = None) -> str:
        """Exporta histórico da sessão para arquivo JSON"""
        if not arquivo:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            arquivo = f"sessao_saude_{timestamp}.json"
        
        dados = {
            'sessao_inicio': self.sessao_inicio.isoformat(),
            'sessao_fim': datetime.now().isoformat(),
            'total_consultas': len(self.consultas),
            'consultas': self.consultas,
            'favoritos': self.favoritos,
            'duracao_minutos': (datetime.now() - self.sessao_inicio).seconds // 60
        }
        
        try:
            with open(arquivo, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
            return f"✅ Sessão exportada para: {arquivo}"
        except Exception as e:
            return f"❌ Erro ao exportar: {e}"


class ConsultaAvancadaTool(BaseTool):
    """Ferramenta avançada com mais opções de consulta"""
    
    name: str = "consulta_avancada"
    description: str = "Ferramenta avançada para consultas detalhadas no banco de saúde"
    
    def _run(self, consulta: str = "", filtros: str = "") -> str:
        """
        Executa consulta avançada com filtros opcionais
        
        Args:
            consulta: Tipo de consulta desejada
            filtros: Filtros adicionais (bairro, tipo, etc)
        """
        
        try:
            if not DB_PATH.exists():
                return f"❌ Banco não encontrado: {DB_PATH}"
            
            conn = sqlite3.connect(str(DB_PATH))
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            # Análise inteligente da consulta
            consulta_lower = consulta.lower()
            filtros_lower = filtros.lower()
            
            if 'mapa' in consulta_lower or 'distribuicao' in consulta_lower:
                return self._mapa_estabelecimentos(cursor, filtros)
            elif 'ranking' in consulta_lower or 'top' in consulta_lower:
                return self._ranking_estabelecimentos(cursor)
            elif 'detalhado' in consulta_lower:
                return self._relatorio_detalhado(cursor, filtros)
            elif 'comparacao' in consulta_lower:
                return self._comparacao_bairros(cursor)
            else:
                return self._busca_personalizada(cursor, consulta, filtros)
                
        except Exception as e:
            return f"❌ Erro na consulta avançada: {str(e)}"
        finally:
            if 'conn' in locals():
                conn.close()
    
    def _mapa_estabelecimentos(self, cursor, filtros: str) -> str:
        """Gera mapa de distribuição de estabelecimentos"""
        
        where_clause = ""
        if filtros:
            where_clause = f"WHERE bairro LIKE '%{filtros}%' OR nome LIKE '%{filtros}%'"
        
        cursor.execute(f"""
            SELECT 
                bairro,
                COUNT(*) as total,
                COUNT(CASE WHEN nome LIKE '%Hospital%' THEN 1 END) as hospitais,
                COUNT(CASE WHEN nome LIKE '%UPA%' THEN 1 END) as upas,
                COUNT(CASE WHEN nome LIKE '%Posto%' OR nome LIKE '%PSF%' THEN 1 END) as postos
            FROM ia_estabelecimento
            {where_clause}
            GROUP BY bairro
            HAVING bairro IS NOT NULL AND bairro != ''
            ORDER BY total DESC
            LIMIT 25
        """)
        
        dados = cursor.fetchall()
        
        resultado = f"🗺️ MAPA DE DISTRIBUIÇÃO DE ESTABELECIMENTOS:\n\n"
        
        if filtros:
            resultado += f"🔍 Filtro aplicado: '{filtros}'\n\n"
        
        for bairro in dados:
            resultado += f"📍 **{bairro['bairro']}** (Total: {bairro['total']})\n"
            resultado += f"   🏥 Hospitais: {bairro['hospitais']}\n"
            resultado += f"   🚑 UPAs: {bairro['upas']}\n"
            resultado += f"   🏥 Postos/PSF: {bairro['postos']}\n\n"
        
        return resultado
    
    def _ranking_estabelecimentos(self, cursor) -> str:
        """Ranking de estabelecimentos por atendimento"""
        
        cursor.execute("""
            SELECT 
                e.nome,
                e.bairro,
                COUNT(*) as total_atendimentos,
                COUNT(DISTINCT h.queixa_principal_id) as tipos_queixas
            FROM ia_estabelecimento e
            JOIN ia_historico_atendimento_sintoma h ON e.cnes = h.estabelecimento_cnes
            GROUP BY e.cnes, e.nome, e.bairro
            ORDER BY total_atendimentos DESC
            LIMIT 20
        """)
        
        ranking = cursor.fetchall()
        
        resultado = f"🏆 RANKING TOP 20 ESTABELECIMENTOS (por atendimentos):\n\n"
        
        for i, est in enumerate(ranking, 1):
            resultado += f"{i:2d}. **{est['nome'][:50]}**\n"
            resultado += f"    📍 {est['bairro']}\n"
            resultado += f"    📊 {est['total_atendimentos']:,} atendimentos\n"
            resultado += f"    🎯 {est['tipos_queixas']} tipos de queixas\n\n"
        
        return resultado
    
    def _relatorio_detalhado(self, cursor, filtro: str = "") -> str:
        """Relatório detalhado com estatísticas completas"""
        
        # Estatísticas gerais
        cursor.execute("SELECT COUNT(*) FROM ia_estabelecimento")
        total_est = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT bairro) FROM ia_estabelecimento WHERE bairro IS NOT NULL")
        total_bairros = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM ia_historico_atendimento_sintoma")
        total_atendimentos = cursor.fetchone()[0]
        
        # Top 5 queixas
        cursor.execute("""
            SELECT q.nome, COUNT(*) as total
            FROM ia_queixa_principal q
            JOIN ia_historico_atendimento_sintoma h ON q.id = h.queixa_principal_id
            GROUP BY q.id, q.nome
            ORDER BY total DESC
            LIMIT 5
        """)
        top_queixas = cursor.fetchall()
        
        resultado = f"📊 RELATÓRIO DETALHADO DO SISTEMA DE SAÚDE\n"
        resultado += f"{'='*60}\n\n"
        
        resultado += f"📈 ESTATÍSTICAS GERAIS:\n"
        resultado += f"   🏥 Total de estabelecimentos: {total_est:,}\n"
        resultado += f"   🏘️ Bairros atendidos: {total_bairros:,}\n"
        resultado += f"   📋 Total de atendimentos: {total_atendimentos:,}\n\n"
        
        resultado += f"🏥 TOP 5 QUEIXAS MAIS COMUNS:\n"
        for i, queixa in enumerate(top_queixas, 1):
            porcentagem = (queixa['total'] / total_atendimentos) * 100
            resultado += f"   {i}. {queixa['nome']}: {queixa['total']:,} ({porcentagem:.1f}%)\n"
        
        return resultado
    
    def _comparacao_bairros(self, cursor) -> str:
        """Comparação entre bairros com mais e menos cobertura"""
        
        cursor.execute("""
            SELECT 
                bairro,
                COUNT(*) as estabelecimentos,
                SUM(CASE WHEN nome LIKE '%Hospital%' THEN 1 ELSE 0 END) as hospitais,
                SUM(CASE WHEN nome LIKE '%UPA%' THEN 1 ELSE 0 END) as upas
            FROM ia_estabelecimento
            WHERE bairro IS NOT NULL AND bairro != ''
            GROUP BY bairro
            HAVING estabelecimentos >= 3
            ORDER BY estabelecimentos DESC
            LIMIT 10
        """)
        
        top_bairros = cursor.fetchall()
        
        resultado = f"📊 COMPARAÇÃO: BAIRROS COM MELHOR COBERTURA\n\n"
        
        for i, bairro in enumerate(top_bairros, 1):
            resultado += f"{i:2d}. **{bairro['bairro']}**\n"
            resultado += f"    🏥 {bairro['estabelecimentos']} estabelecimentos totais\n"
            resultado += f"    🏥 {bairro['hospitais']} hospitais\n"
            resultado += f"    🚑 {bairro['upas']} UPAs\n\n"
        
        return resultado
    
    def _busca_personalizada(self, cursor, consulta: str, filtros: str) -> str:
        """Busca personalizada baseada na entrada do usuário"""
        
        where_conditions = []
        params = []
        
        if filtros:
            where_conditions.append("(nome LIKE ? OR bairro LIKE ? OR endereco LIKE ?)")
            params.extend([f"%{filtros}%", f"%{filtros}%", f"%{filtros}%"])
        
        where_clause = f"WHERE {' AND '.join(where_conditions)}" if where_conditions else ""
        
        cursor.execute(f"""
            SELECT nome, endereco, bairro, fone
            FROM ia_estabelecimento
            {where_clause}
            ORDER BY nome
            LIMIT 20
        """, params)
        
        resultados = cursor.fetchall()
        
        if not resultados:
            return f"❌ Nenhum resultado encontrado para: '{consulta}' com filtros '{filtros}'"
        
        resultado = f"🔍 BUSCA PERSONALIZADA: '{consulta}'\n"
        if filtros:
            resultado += f"🔍 Filtros: '{filtros}'\n"
        resultado += f"📋 {len(resultados)} resultados encontrados:\n\n"
        
        for est in resultados:
            resultado += f"• **{est['nome']}**\n"
            resultado += f"  📍 {est['endereco']}\n"
            resultado += f"  🏘️ {est['bairro']}\n"
            if est['fone']:
                resultado += f"  📞 {est['fone']}\n"
            resultado += "\n"
        
        return resultado


def criar_agente_avancado():
    """Cria agente para funcionalidades avançadas"""
    
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)
    
    return Agent(
        role="Especialista Avançado em Dados de Saúde",
        goal="Fornecer análises detalhadas e relatórios avançados sobre dados de saúde",
        backstory=("""Sou um analista sênior especializado em sistemas de informação
                   em saúde. Tenho experiência em criar relatórios executivos,
                   análises comparativas e mapas de distribuição de serviços.
                   Minha expertise inclui análise estatística avançada e
                   visualização de dados de saúde pública."""),
        verbose=True,
        llm=llm,
        tools=[ConsultaAvancadaTool()]
    )


def mostrar_menu_avancado():
    """Menu com opções avançadas"""
    
    print("\n" + "="*60)
    print("🚀 SISTEMA AVANÇADO DE CONSULTAS DE SAÚDE")
    print("="*60)
    print("Comandos disponíveis:")
    print()
    print("📊 CONSULTAS AVANÇADAS:")
    print("   • 'mapa [filtro]' - Mapa de distribuição de estabelecimentos")
    print("   • 'ranking' - Ranking dos melhores estabelecimentos")
    print("   • 'relatorio detalhado' - Relatório completo do sistema")
    print("   • 'comparacao bairros' - Comparar cobertura entre bairros")
    print()
    print("🔍 BUSCA PERSONALIZADA:")
    print("   • 'buscar [termo]' - Busca personalizada")
    print()
    print("📝 FUNCIONALIDADES DA SESSÃO:")
    print("   • 'historico' - Ver histórico de consultas")
    print("   • 'favoritos' - Ver items favoritados")
    print("   • 'favoritar [item]' - Adicionar aos favoritos")
    print("   • 'exportar' - Exportar sessão para arquivo")
    print()
    print("⌨️ COMANDOS BÁSICOS:")
    print("   • 'ajuda' - Mostrar este menu")
    print("   • 'limpar' - Limpar tela")
    print("   • 'sair' - Encerrar programa")
    print("="*60)


def processar_comando_avancado(entrada: str, historico: HistoricoSessao) -> tuple[bool, str]:
    """
    Processa comandos avançados
    
    Returns:
        tuple[bool, str]: (continuar, resposta/comando)
    """
    
    entrada = entrada.strip()
    
    # Comandos básicos
    if entrada.lower() in ['sair', 'quit', 'exit']:
        return False, "👋 Encerrando sessão..."
    
    elif entrada.lower() in ['ajuda', 'help']:
        mostrar_menu_avancado()
        return True, ""
    
    elif entrada.lower() in ['limpar', 'clear']:
        os.system('clear' if os.name == 'posix' else 'cls')
        mostrar_menu_avancado()
        return True, ""
    
    # Comandos do histórico
    elif entrada.lower() == 'historico':
        return True, historico.obter_historico()
    
    elif entrada.lower() == 'favoritos':
        return True, historico.obter_favoritos()
    
    elif entrada.lower().startswith('favoritar '):
        item = entrada[10:]  # Remove 'favoritar '
        sucesso = historico.adicionar_favorito(item)
        if sucesso:
            return True, f"⭐ '{item}' adicionado aos favoritos!"
        else:
            return True, f"⚠️ '{item}' já está nos favoritos."
    
    elif entrada.lower() == 'exportar':
        resultado = historico.exportar_sessao()
        return True, resultado
    
    # Comando é uma consulta normal
    return True, entrada


def executar_consulta_avancada(agente: Agent, entrada: str) -> str:
    """Executa consulta avançada usando o agente"""
    
    # Analisar entrada para determinar tipo de consulta
    entrada_lower = entrada.lower()
    
    if entrada_lower.startswith('mapa'):
        filtro = entrada[4:].strip() if len(entrada) > 4 else ""
        consulta = "mapa"
    elif entrada_lower.startswith('buscar'):
        filtro = entrada[6:].strip() if len(entrada) > 6 else ""
        consulta = "busca personalizada"
    else:
        consulta = entrada
        filtro = ""
    
    tarefa = Task(
        description=f"""
        Execute uma consulta avançada baseada na solicitação do usuário: "{entrada}"
        
        Use a ferramenta consulta_avancada com:
        - consulta: "{consulta}"
        - filtros: "{filtro}"
        
        Forneça uma resposta completa, bem formatada e com insights úteis.
        Se apropriado, destaque padrões interessantes nos dados.
        """,
        agent=agente,
        expected_output="Análise detalhada e bem formatada dos dados solicitados"
    )
    
    crew = Crew(
        agents=[agente],
        tasks=[tarefa],
        process=Process.sequential,
        verbose=False
    )
    
    try:
        resultado = crew.kickoff()
        return resultado.raw
    except Exception as e:
        return f"❌ Erro ao processar consulta: {str(e)}"


def sistema_avancado():
    """Sistema principal com funcionalidades avançadas"""
    
    # Verificações iniciais
    if not DB_PATH.exists():
        print(f"❌ Banco não encontrado: {DB_PATH}")
        return
    
    print("🚀 Iniciando sistema avançado...")
    
    # Inicializar componentes
    agente = criar_agente_avancado()
    historico = HistoricoSessao()
    
    mostrar_menu_avancado()
    
    print(f"\n💡 Sistema pronto! Digite sua consulta ou comando:")
    
    # Loop principal
    while True:
        try:
            entrada = input("\n🔍 Consulta avançada: ").strip()
            
            if not entrada:
                continue
            
            # Processar comando
            continuar, resposta = processar_comando_avancado(entrada, historico)
            
            if not continuar:
                print(resposta)
                break
            
            if resposta and not entrada.lower().startswith(('ajuda', 'limpar')):
                print(f"\n📋 {resposta}")
                continue
            
            # Executar consulta avançada
            if entrada.lower() not in ['historico', 'favoritos', 'exportar'] and not entrada.lower().startswith('favoritar'):
                print("\n⏳ Executando consulta avançada...")
                resposta_agente = executar_consulta_avancada(agente, entrada)
                
                print("\n" + "="*60)
                print("📊 RESULTADO DA ANÁLISE AVANÇADA:")
                print("-" * 60)
                print(resposta_agente)
                print("="*60)
                
                # Adicionar ao histórico
                historico.adicionar_consulta(entrada, resposta_agente)
                
        except KeyboardInterrupt:
            print("\n\n⏹️ Interrompido. Finalizando...")
            break
        except Exception as e:
            print(f"\n❌ Erro: {str(e)}")


def main():
    """Função principal"""
    
    print("🎯 EXERCÍCIO 2: Interface Melhorada")
    print("Testando funcionalidades avançadas do sistema!")
    
    if not os.getenv('OPENAI_API_KEY'):
        print("❌ OpenAI API Key não configurada")
        return
    
    sistema_avancado()
    
    print("\n✅ Exercício 2 concluído!")
    print("📚 Você aprendeu sobre:")
    print("   • Histórico de sessão")
    print("   • Sistema de favoritos")
    print("   • Exportação de dados")
    print("   • Interface avançada")
    print("   • Consultas personalizadas")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⏹️ Programa interrompido")
    except Exception as e:
        print(f"\n❌ Erro fatal: {e}")