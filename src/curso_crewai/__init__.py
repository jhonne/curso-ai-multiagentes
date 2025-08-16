"""
Curso CrewAI - Pacote Python
Desenvolvendo Chatbots com Múltiplos Agentes usando CrewAI e OpenAI
"""

__version__ = "0.1.0"
__author__ = "Curso CrewAI"
__email__ = "curso@example.com"

# Exportações principais
from .hello_crewai import main as hello_crewai_main
from .teste_api import teste_rapido_openai
from .configurar import main as configurar_main

__all__ = [
    "hello_crewai_main",
    "teste_rapido_openai", 
    "configurar_main",
]