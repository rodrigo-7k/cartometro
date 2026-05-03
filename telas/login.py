"""
Tela de Login - Versão Moderna com Design System
"""

from nicegui import ui
from config_service import config_service
from datetime import datetime
import hashlib
import os

USUARIOS_ARQ = 'usuarios.json'


def hash_senha(senha):
    """Gera hash SHA-256 da senha"""
    return hashlib.sha256(senha.encode()).hexdigest()


def carregar_usuarios():
    """Carrega usuários do arquivo JSON"""
    import json
    
    if not os.path.exists(USUARIOS_ARQ):
        # Criar usuários padrão
        usuarios = [
            {
                "id": 1,
                "nome": "Administrador",
                "email": "admin@fincontrol.com",
                "senha": hash_senha("admin123"),
                "role": "admin",
                "avatar": "👨‍💻",
                "ativo": True,
                "data_cadastro": datetime.now().isoformat()
            },
            {
                "id": 2,
                "nome": "Visitante",
                "email": "visitante@fincontrol.com",
                "senha": hash_senha("visitante123"),
                "role": "visitante",
                "avatar": "👤",
                "ativo": True,
                "data_cadastro": datetime.now().isoformat()
            }
        ]
        with open(USUARIOS_ARQ, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, indent=2, ensure_ascii=False)
        return usuarios
    
    with open(USUARIOS_ARQ, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_usuarios(usuarios):
    """Salva usuários no arquivo JSON"""
    import json
    with open(USUARIOS_ARQ, "w", encoding="utf-8") as f:
        json.dump(usuarios, f, indent=2, ensure_ascii=False)


def autenticar_usuario(email, senha):
    """Autentica usuário por email e senha"""
    usuarios = carregar_usuarios()
    senha_hash = hash_senha(senha)
    
    for usuario in usuarios:
        if (usuario.get("email") == email and 
            usuario.get("senha") == senha_hash and 
            usuario.get("ativo", True)):
            return usuario
    return None


CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

* {
    box-sizing: border-box !important;
}

.login-overlay {
    position: fixed !important;
    inset: 0 !important;
    z-index: 999 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    background: #f8f9fb !important;
    font-family: 'Inter', 'DM Sans', sans-serif !important;
}

.login-container {
    display: flex !important;
    width: 100% !important;
    max-width: 900px !important;
    min-height: 540px !important;
    border-radius: 20px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05), 0 20px 50px -10px rgba(0,0,0,0.1) !important;
    margin: 20px !important;
    background: white !important;
}

/* Painel esquerdo - Branding */
.login-brand {
    flex: 1 !important;
    padding: 48px 40px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    color: white !important;
    position: relative !important;
    overflow: hidden !important;
}

.login-brand::before {
    content: '' !important;
    position: absolute !important;
    top: -50% !important;
    right: -50% !important;
    width: 200% !important;
    height: 200% !important;
    background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%) !important;
}

.login-brand-eyebrow {
    font-size: 10px !important;
    font-weight: 600 !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    margin-bottom: 12px !important;
    opacity: 0.8 !important;
}

.login-brand-title {
    font-size: 36px !important;
    font-weight: 700 !important;
    letter-spacing: -1px !important;
    line-height: 1.15 !important;
    margin-bottom: 16px !important;
    position: relative !important;
}

.login-brand-subtitle {
    font-size: 14px !important;
    opacity: 0.7 !important;
    line-height: 1.6 !important;
    position: relative !important;
}

.login-features {
    margin-top: 32px !important;
    display: flex !important;
    flex-direction: column !important;
    gap: 16px !important;
    position: relative !important;
}

.login-feature-item {
    display: flex !important;
    align-items: flex-start !important;
    gap: 10px !important;
}

.login-feature-icon {
    width: 20px !important;
    height: 20px !important;
    border-radius: 50% !important;
    background: rgba(255,255,255,0.2) !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 10px !important;
    flex-shrink: 0 !important;
    margin-top: 2px !important;
}

.login-feature-text {
    font-size: 13px !important;
    opacity: 0.85 !important;
}

/* Painel direito - Formulário */
.login-form-panel {
    width: 380px !important;
    flex-shrink: 0 !important;
    padding: 48px 36px !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important;
    background: white !important;
}

.login-logo {
    display: flex !important;
    align-items: center !important;
    gap: 10px !important;
    margin-bottom: 32px !important;
}

.login-logo-icon {
    width: 36px !important;
    height: 36px !important;
    border-radius: 9px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    font-size: 18px !important;
}

.login-logo-text {
    font-size: 15px !important;
    font-weight: 600 !important;
    color: #111827 !important;
    letter-spacing: -0.3px !important;
}

.login-form-title {
    font-size: 22px !important;
    font-weight: 700 !important;
    color: #111827 !important;
    letter-spacing: -0.4px !important;
    margin-bottom: 4px !important;
}

.login-form-sub {
    font-size: 13px !important;
    color: #9ca3af !important;
    margin-bottom: 28px !important;
}

.login-input {
    width: 100% !important;
    margin-bottom: 16px !important;
}

.login-input .q-field__control {
    border-radius: 10px !important;
    height: 44px !important;
}

.login-error {
    font-size: 12px !important;
    color: #ef4444 !important;
    margin-bottom: 12px !important;
    display: none !important;
}

.login-error.show {
    display: block !important;
}

.btn-login {
    width: 100% !important;
    height: 44px !important;
    border-radius: 10px !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    letter-spacing: -0.2px !important;
    text-transform: none !important;
    margin-top: 4px !important;
    transition: all 0.2s ease !important;
}

.btn-login:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
}

.login-demo {
    margin-top: 24px !important;
    padding: 16px !important;
    background: #f9fafb !important;
    border-radius: 10px !important;
    border: 1px solid #f3f4f6 !important;
}

.login-demo-title {
    font-size: 11px !important;
    font-weight: 600 !important;
    color: #9ca3af !important;
    text-transform: uppercase !important;
    letter-spacing: 0.05em !important;
    margin-bottom: 8px !important;
}

.login-demo-item {
    font-size: 11px !important;
    color: #6b7280 !important;
    padding: 3px 0 !important;
    cursor: pointer !important;
    transition: color 0.15s ease !important;
}

.login-demo-item:hover {
    color: #111827 !important;
}

/* Mobile */
@media (max-width: 768px) {
    .login-overlay {
        align-items: flex-start !important;
        background: white !important;
    }
    
    .login-container {
        flex-direction: column !important;
        max-width: 100% !important;
        min-height: 100vh !important;
        border-radius: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
    }
    
    .login-brand {
        flex: 0 0 auto !important;
        padding: 40px 28px 32px !important;
        min-height: auto !important;
    }
    
    .login-brand-title {
        font-size: 28px !important;
    }
    
    .login-features {
        display: none !important;
    }
    
    .login-form-panel {
        width: 100% !important;
        flex: 1 !important;
        padding: 0 !important;
        display: flex !important;
        flex-direction: column !important;
    }
    
    .login-form-inner {
        flex: 1 !important;
        background: white !important;
        border-radius: 24px 24px 0 0 !important;
        padding: 32px 24px 40px !important;
        margin-top: -24px !important;
        box-shadow: 0 -4px 24px rgba(0,0,0,0.06) !important;
    }
    
    .login-logo {
        display: none !important;
    }
}
</style>
"""


def tela_login(container, on_login_success=None):
    """
    Tela de login moderna
    
    Args:
        container: Container onde renderizar a tela
        on_login_success: Callback chamado após login bem-sucedido (recebe o usuário)
    """
    
    container.clear()
    container.classes('p-0 m-0')
    container.style('padding: 0 !important; margin: 0 !important; width: 100% !important; height: 100% !important;')
    
    ui.add_head_html(CUSTOM_CSS)
    
    cor_primaria = config_service.get_primary_color()
    cor_escura = config_service.get_primary_dark()
    
    with container:
        with ui.element('div').classes('login-overlay'):
            with ui.element('div').classes('login-container'):
                
                # ─── PAINEL ESQUERDO: BRANDING ───
                with ui.element('div').classes('login-brand').style(
                    f'background: linear-gradient(150deg, {cor_escura} 0%, {cor_primaria} 100%)'
                ):
                    ui.label('Finanças inteligentes').classes('login-brand-eyebrow')
                    ui.label('Controle total\nsobre o seu\ndinheiro.').classes('login-brand-title')
                    ui.label(
                        'Acompanhe receitas, despesas e metas em um só lugar, '
                        'com clareza e simplicidade.'
                    ).classes('login-brand-subtitle')
                    
                    # Features
                    with ui.element('div').classes('login-features'):
                        features = [
                            ("📊", "Dashboard inteligente com visão em tempo real"),
                            ("🎯", "Controle de metas e objetivos financeiros"),
                            ("📈", "Relatórios detalhados por categoria"),
                        ]
                        for icon, text in features:
                            with ui.element('div').classes('login-feature-item'):
                                ui.element('div').classes('login-feature-icon').style(f'background: rgba(255,255,255,0.2)'):
                                    ui.label(icon).style('font-size: 10px')
                                ui.label(text).classes('login-feature-text')
                
                # ─── PAINEL DIREITO: FORMULÁRIO ───
                with ui.element('div').classes('login-form-panel'):
                    
                    # Mobile: formulário dentro de card flutuante
                    with ui.element('div').classes('login-form-inner'):
                        
                        # Logo
                        with ui.element('div').classes('login-logo'):
                            with ui.element('div').classes('login-logo-icon').style(f'background: {cor_primaria}'):
                                ui.label('💳').style('font-size: 18px')
                            with ui.element('div'):
                                ui.label('Controle Cartão').classes('login-logo-text')
                        
                        ui.label('Entrar na conta').classes('login-form-title')
                        ui.label('Bem-vindo de volta! 👋').classes('login-form-sub')
                        
                        # Campos
                        email_input = ui.input(
                            'E-mail',
                            placeholder='seu@email.com'
                        ).props('outlined').classes('login-input')
                        
                        senha_input = ui.input(
                            'Senha',
                            password=True,
                            password_toggle_button=True,
                            placeholder='••••••••'
                        ).props('outlined').classes('login-input')
                        
                        error_label = ui.label('').classes('login-error')
                        
                        def fazer_login():
                            email = email_input.value or ''
                            senha = senha_input.value or ''
                            
                            if not email or not senha:
                                error_label.set_text('⚠️ Preencha todos os campos.')
                                error_label.classes('login-error show')
                                return
                            
                            usuario = autenticar_usuario(email, senha)
                            
                            if usuario:
                                error_label.classes('login-error')
                                ui.notify(f'✅ Bem-vindo, {usuario.get("nome", "Usuário")}!', 
                                         type='positive', position='top')
                                
                                if on_login_success:
                                    on_login_success(usuario)
                            else:
                                error_label.set_text('❌ E-mail ou senha incorretos.')
                                error_label.classes('login-error show')
                        
                        ui.button(
                            'Entrar',
                            on_click=fazer_login,
                            icon='login'
                        ).classes('btn-login').props('unelevated').style(
                            f'background: {cor_primaria} !important; color: white !important;'
                        )
                        
                        # Demonstração
                        with ui.element('div').classes('login-demo'):
                            ui.label('Acessos de demonstração').classes('login-demo-title')
                            
                            def preencher_admin():
                                email_input.value = 'admin@fincontrol.com'
                                senha_input.value = 'admin123'
                            
                            def preencher_visitante():
                                email_input.value = 'visitante@fincontrol.com'
                                senha_input.value = 'visitante123'
                            
                            ui.label('👑 Admin: admin@fincontrol.com / admin123') \
                                .classes('login-demo-item').on('click', preencher_admin)
                            ui.label('👤 Visitante: visitante@fincontrol.com / visitante123') \
                                .classes('login-demo-item').on('click', preencher_visitante)
        

__all__ = ['tela_login']