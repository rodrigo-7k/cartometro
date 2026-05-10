"""Tela principal do App - Pós-login"""

from nicegui import ui
import config
from config_service import config_service

@ui.page('/app')
def app_page():
    if not config.usuario_atual:
        ui.navigate.to('/login')
        return
    
    # Obter cores do usuário
    cores = config.get_cores_usuario()
    
    # Atualizar o config_service com as cores do usuário
    # (isso já deve estar sendo feito na tela de configurações)
    
    from telas.lancamentos import tela_lancamentos
    container_principal = ui.element('div').classes('w-full h-screen')
    
    # Passar as cores para a tela de lançamentos, se necessário
    tela_lancamentos(container_principal)