"""Tela de Login do Cartometro"""

from nicegui import ui
from db import autenticar_usuario, set_usuario_logado, resetar_dados_demo, carregar_usuarios
from config import LOGO, LOGO_FULL_BRANCA, WORDMARK, FAVICON
from config_service import config_service
import config as cfg

@ui.page('/login')
def login_page():
    COR_PRIMARIA = config_service.get_primary_color()
    COR_ESCURA = config_service.get_primary_dark()
    
    beneficios = [
        ("📊", "Dashboard inteligente com KPIs em tempo real"),
        ("🤖", "Consultor financeiro com 30+ alertas"),
        ("💳", "Controle total de múltiplos cartões"),
        ("🎯", "Metas e orçamentos personalizados"),
        ("🔔", "Alertas antes de problemas acontecerem"),
    ]
    
    ui.add_head_html(f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700;14..32,800;14..32,900&display=swap" rel="stylesheet">
    <link rel="icon" type="image/x-icon" href="{FAVICON}">
    <style>
    *{{margin:0;padding:0;box-sizing:border-box}}
    html,body{{height:100%;width:100%;overflow:hidden;font-family:'Inter',sans-serif}}
    .login-page{{display:flex;height:100vh;width:100vw}}
    
    .login-brand{{flex:1;background:linear-gradient(160deg,{COR_ESCURA} 0%,{COR_PRIMARIA} 60%);display:flex;flex-direction:column;justify-content:center;align-items:center;padding:60px;position:relative;overflow:hidden}}
    .login-brand::before{{content:'';position:absolute;width:800px;height:800px;border-radius:50%;border:2px solid rgba(255,255,255,.05);top:-250px;right:-250px}}
    .login-brand-content{{position:relative;z-index:1;display:flex;flex-direction:column;align-items:center;max-width:500px}}
    .login-brand-logo{{width:640px;height:auto;margin-bottom:48px}}
    .login-brand-benefits{{text-align:left;width:100%}}
    .login-brand-title{{font-size:26px;font-weight:800;color:#fff;margin-bottom:10px;text-align:center}}
    .login-brand-subtitle{{font-size:14px;color:rgba(255,255,255,.7);margin-bottom:40px;text-align:center}}
    
    .benefit-item{{display:flex;align-items:center;gap:12px;margin-bottom:16px}}
    .benefit-icon{{width:36px;height:36px;background:rgba(255,255,255,.12);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px;flex-shrink:0}}
    .benefit-text{{font-size:13px;font-weight:500;color:#fff}}
    
    .login-form-side{{width:520px;flex-shrink:0;display:flex;align-items:center;justify-content:center;background:#fff;padding:48px;position:relative}}
    .login-form-container{{width:100%;max-width:380px}}
    .login-logo-icon{{width:180px;height:auto;margin:0 auto 20px;display:block}}
    .login-wordmark{{width:160px;height:auto;margin:0 auto 8px;display:block}}
    .login-title{{font-size:26px;font-weight:800;color:#111827;text-align:center;margin-bottom:4px}}
    .login-subtitle{{font-size:13px;color:#9ca3af;text-align:center;margin-bottom:32px}}
    
    .back-btn{{position:absolute;top:20px;left:20px;background:#fff;border:none;padding:10px 16px;border-radius:8px;font-size:12px;color:#6b7280;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.08);font-family:inherit;z-index:10;transition:all .2s}}
    .back-btn:hover{{color:#111827;box-shadow:0 4px 12px rgba(0,0,0,.12)}}
    
    .field{{margin-bottom:16px}}
    .field-label{{font-size:13px;font-weight:600;color:#374151;margin-bottom:6px;display:block}}
    
    .error{{display:none;font-size:13px;color:#ef4444;background:#fef2f2;border-left:3px solid #ef4444;padding:12px 16px;border-radius:8px;margin-bottom:16px}}
    .error.show{{display:block}}
    
    .btn-login{{width:100%;height:48px;background:{COR_PRIMARIA}!important;color:#fff;border:none;border-radius:10px;font-size:16px;font-weight:600;cursor:pointer;font-family:inherit;transition:all .2s;margin-top:8px;box-shadow:0 2px 8px rgba(37,99,235,.3)}}
    .btn-login:hover{{background:{COR_ESCURA}!important;box-shadow:0 4px 16px rgba(37,99,235,.38);transform:translateY(-1px)}}
    
    .demo-section{{margin-top:28px;padding-top:24px;border-top:1px solid #f1f5f9}}
    .demo-label{{font-size:11px;font-weight:700;color:#cbd5e1;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;text-align:center}}
    .demo-btn{{width:100%;padding:12px;background:{COR_PRIMARIA}20!important;color:{COR_PRIMARIA}!important;border:1px solid #bfdbfe;border-radius:10px;font-size:13px;font-weight:600;cursor:pointer;font-family:inherit;transition:all .2s;text-align:center}}
    .demo-btn:hover{{background:#dbeafe;border-color:{COR_PRIMARIA}}}
    
    .register-link{{text-align:center;margin-top:24px;font-size:13px}}
    .register-link .normal{{color:#9ca3af}}
    .register-link .destaque{{color:{COR_PRIMARIA}!important;font-weight:600;cursor:pointer}}
    .register-link .destaque:hover{{text-decoration:underline}}
    
    .q-field--outlined .q-field__control{{border-radius:10px!important;height:48px!important;background:#fafafa!important}}
    .q-field--outlined.q-field--focused .q-field__control{{border-color:{COR_PRIMARIA}!important;box-shadow:0 0 0 3px rgba(37,99,235,.1)!important}}
    
    @media(max-width:1024px){{
        .login-brand{{display:none}}
        .login-form-side{{width:100%;padding:0;display:flex;flex-direction:column;align-items:stretch;justify-content:flex-start;overflow-y:auto}}
        .login-mobile-header{{display:flex!important;flex-direction:column;align-items:center;justify-content:center;background:linear-gradient(160deg,{COR_ESCURA} 0%,{COR_PRIMARIA} 100%);padding:48px 24px 56px;position:relative}}
        .login-mobile-header::after{{content:'';position:absolute;bottom:-24px;left:0;right:0;height:48px;background:#fff;border-radius:28px 28px 0 0}}
        .login-mobile-logo{{width:120px;height:auto;margin-bottom:8px}}
        .login-form-container{{position:relative;z-index:1;padding:20px 24px 40px;width:100%;max-width:420px;margin:0 auto}}
        .login-logo-icon{{display:none!important}}
        .back-btn{{position:absolute;top:16px;right:16px;left:auto;background:rgba(255,255,255,.2);color:#fff;backdrop-filter:blur(10px);box-shadow:0 2px 10px rgba(0,0,0,.1);border-radius:8px;padding:8px 14px;font-size:12px;font-weight:600;z-index:10}}
        .back-btn:hover{{background:rgba(255,255,255,.3);color:#fff}}
    }}
    </style>
    """)
    
    def fazer_login():
        email = (email_input.value or '').strip()
        senha = senha_input.value or ''
        
        if not email or not senha:
            error_label.classes('error show')
            error_label.set_text('⚠️ Preencha todos os campos.')
            return
        
        usuario = autenticar_usuario(email, senha)
        
        if usuario:
            cfg.usuario_atual = usuario
            if email == 'demo':
                resetar_dados_demo(email)
            set_usuario_logado(email)
            ui.notify(f'✅ Bem-vindo, {usuario["nome"]}!', type='positive', position='top')
            ui.navigate.to('/app')
        else:
            error_label.classes('error show')
            error_label.set_text('❌ Email ou senha incorretos.')
    
    def preencher_demo():
        email_input.value = 'demo'
        senha_input.value = 'demo'
    
    with ui.element('div').classes('login-page'):
        with ui.element('div').classes('login-brand'):
            with ui.element('div').classes('login-brand-content'):
                ui.html(f'<img src="{LOGO_FULL_BRANCA}" alt="Cartometro" class="login-brand-logo">')
                with ui.element('div').classes('login-brand-benefits'):
                    ui.label('Controle inteligente do seu crédito').classes('login-brand-title')
                    ui.label('Tudo que você precisa para dominar suas finanças.').classes('login-brand-subtitle')
                    for icon, text in beneficios:
                        with ui.element('div').classes('benefit-item'):
                            ui.label(icon).classes('benefit-icon')
                            ui.label(text).classes('benefit-text')
        
        with ui.element('div').classes('login-form-side'):
            ui.html(f'<div class="login-mobile-header" style="display:none;"><img src="{LOGO}" alt="Cartometro" class="login-mobile-logo"></div>')
            ui.button('← Voltar', on_click=lambda: ui.navigate.to('/')).props('no-caps').classes('back-btn').style(f'background:{COR_PRIMARIA}!important')
            
            with ui.element('div').classes('login-form-container'):
                ui.html(f'<img src="{LOGO}" alt="Cartometro" class="login-logo-icon">')
                ui.html(f'<img src="{WORDMARK}" alt="Cartometro" class="login-wordmark">')
                ui.label('Bem-vindo de volta').classes('login-title')
                ui.label('Entre para continuar').classes('login-subtitle')
                
                with ui.element('div').classes('field'):
                    ui.label('Email').classes('field-label')
                    email_input = ui.input(placeholder='seu@email.com').props('outlined dense').classes('w-full')
                with ui.element('div').classes('field'):
                    ui.label('Senha').classes('field-label')
                    senha_input = ui.input(placeholder='••••••••', password=True, password_toggle_button=True).props('outlined dense').classes('w-full')
                
                error_label = ui.label('').classes('error')
                ui.button('Entrar', on_click=fazer_login).props('no-caps').classes('btn-login').style(f'background:{COR_PRIMARIA}!important')
                
                with ui.element('div').classes('demo-section'):
                    ui.label('Acesso rápido').classes('demo-label')
                    ui.button('👑 Demo: demo / demo', on_click=preencher_demo).classes('demo-btn').style(f'background:{COR_PRIMARIA}!important;border-color:{COR_PRIMARIA}!important')
                
                with ui.element('div').classes('register-link'):
                    ui.label('Não tem conta? ').classes('normal')
                    ui.label('Criar conta gratuita').classes('destaque').on('click', lambda: ui.navigate.to('/criar-conta'))