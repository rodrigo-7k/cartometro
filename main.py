"""
Cartometro - Controle Inteligente do seu Crédito
"""

from nicegui import ui
from db import (
    inicializar, autenticar_usuario, criar_usuario,
    set_usuario_logado, get_usuario_logado_email,
    buscar_usuario_por_email, get_plano_usuario,
    verificar_limite_lancamentos, tem_consultor_premium,
    carregar, atualizar_config
)
from config_service import config_service
from auth_service import get_usuario_logado
import admin  # Painel administrativo
import os

# ============================================================
# URLS DAS IMAGENS (CLOUDINARY)
# ============================================================
LOGO_BRANCA = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845617/logo_branca_mmgwof.png"
LOGO_FULL_BRANCA = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845630/logo_full_branca_wlx97y.png"
LOGO = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845521/logo_bvchvv.png"
WORDMARK = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845635/wordmark_nf3put.png"
FAVICON = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845656/favicon_crsq9e.ico"

# ============================================================
# VARIÁVEIS GLOBAIS
# ============================================================
usuario_atual = None
container_principal = None


# =========================
# TELA DE LOGIN
# =========================
@ui.page('/')
def login():
    cor        = config_service.get_primary_color()
    cor_escura = config_service.get_primary_dark()

    ui.add_head_html(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
    
    <link rel="icon" type="image/x-icon" href="{FAVICON}">
    <link rel="icon" type="image/png" sizes="16x16" href="{LOGO}">
    <link rel="icon" type="image/png" sizes="32x32" href="{LOGO}">

    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

    html, body {{
        height: 100%;
        width: 100%;
        overflow: hidden;
        font-family: 'DM Sans', sans-serif;
    }}

    .lp-root {{
        display: flex;
        height: 100vh;
        height: 100dvh;
        width: 100%;
        overflow: hidden;
    }}

    .lp-brand {{
        flex: 1;
        background: linear-gradient(160deg, {cor_escura} 0%, {cor} 60%, {cor}bb 100%);
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 64px 56px;
        position: relative;
        overflow: hidden;
    }}

    .lp-brand::before {{
        content: '';
        position: absolute;
        width: 500px; 
        height: 500px;
        border-radius: 50%;
        border: 80px solid rgba(255,255,255,0.04);
        top: -150px; 
        right: -150px;
    }}

    .lp-brand::after {{
        content: '';
        position: absolute;
        width: 350px; 
        height: 350px;
        border-radius: 50%;
        border: 50px solid rgba(255,255,255,0.04);
        bottom: -80px; 
        left: -80px;
    }}

    .lp-brand-logo {{
        width: 420px;
        height: auto;
        position: relative;
        z-index: 1;
        filter: drop-shadow(0 20px 40px rgba(0,0,0,0.25));
    }}

    .lp-form-side {{
        width: 480px; 
        height: 100%; 
        flex-shrink: 0;
        display: flex; 
        align-items: center; 
        justify-content: center;
        background: #fff; 
        padding: 48px 44px;
    }}

    .lp-form-box {{
        width: 100%; 
        max-width: 380px; 
        height: 100%;
        display: flex; 
        flex-direction: column; 
        justify-content: center;
    }}

    .lp-form-logo {{
        width: 220px;
        height: auto;
        margin-bottom: 32px;
        align-self: center;
    }}

    .lp-form-desc {{
        font-size: 14px;
        color: #9ca3af;
        margin-bottom: 36px;
        text-align: center;
        line-height: 1.5;
    }}

    .lp-form-box h2 {{
        font-size: 26px; 
        font-weight: 700; 
        letter-spacing: -0.8px;
        color: #0f0f0f; 
        margin-bottom: 32px; 
        line-height: 1.15;
    }}

    .lp-field-wrap {{ margin-bottom: 16px; }}

    .lp-field-label {{
        font-size: 13px; 
        font-weight: 500; 
        color: #4b5563;
        margin-bottom: 6px; 
        display: block;
    }}

    .lp-field-wrap .q-field--outlined .q-field__control {{
        border-radius: 10px !important; 
        height: 48px !important;
        background: #fafafa !important; 
        font-size: 14px !important;
    }}

    .lp-field-wrap .q-field--outlined.q-field--focused .q-field__control {{
        border-color: {cor} !important;
        box-shadow: 0 0 0 3px {cor}22 !important;
    }}

    .lp-error {{
        font-size: 13px; 
        color: #ef4444; 
        background: #fef2f2;
        border-radius: 8px; 
        padding: 10px 14px; 
        margin-top: 12px;
        display: none; 
        border-left: 3px solid #ef4444;
    }}

    .lp-hint {{
        margin-top: 28px; 
        padding-top: 20px; 
        border-top: 1px solid #f3f4f6;
    }}

    .lp-hint-label {{
        font-size: 11px; 
        font-weight: 600; 
        color: #d1d5db;
        text-transform: uppercase; 
        letter-spacing: 0.08em; 
        margin-bottom: 8px;
    }}

    .lp-hint-item {{
        font-size: 12.5px; 
        color: #9ca3af; 
        cursor: pointer;
        transition: color 0.15s; 
        padding: 3px 0;
    }}

    .lp-hint-item:hover {{ color: #374151; }}

    .lp-criar-conta {{
        margin-top: 20px;
        text-align: center;
    }}

    .lp-criar-conta span {{
        font-size: 13px;
        color: #9ca3af;
    }}

    .lp-criar-conta a {{
        color: {cor};
        font-weight: 600;
        cursor: pointer;
        text-decoration: none;
    }}

    .lp-criar-conta a:hover {{ text-decoration: underline; }}

    @media (max-width: 768px) {{
        body {{ background: #fff; }}
        .lp-root {{ flex-direction: column; height: 100dvh; }}
        .lp-brand {{ display: none; }}
        .lp-form-side {{
            width: 100%; 
            height: 100%; 
            padding: 0;
            align-items: stretch; 
            background: transparent;
        }}
        .lp-form-box {{
            max-width: 100%; 
            width: 100%; 
            height: 100%;
            display: flex; 
            flex-direction: column;
        }}
        .lp-mobile-header {{
            background: linear-gradient(160deg, {cor_escura} 0%, {cor} 100%);
            padding: 56px 28px 46px; 
            position: relative; 
            overflow: hidden; 
            flex-shrink: 0;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        .lp-mobile-header::after {{
            content: ''; 
            position: absolute;
            width: 250px; 
            height: 250px; 
            border-radius: 50%;
            border: 40px solid rgba(255,255,255,0.05);
            top: -60px; 
            right: -60px;
        }}
        .lp-mobile-header::before {{
            content: ''; 
            position: absolute;
            width: 180px; 
            height: 180px; 
            border-radius: 50%;
            border: 30px solid rgba(255,255,255,0.04);
            bottom: -40px; 
            left: -40px;
        }}
        .lp-mobile-header-logo {{
            width: 250px;
            height: auto;
            position: relative;
            z-index: 1;
            filter: drop-shadow(0 10px 20px rgba(0,0,0,0.25));
        }}
        .lp-mobile-form-card {{
            flex: 1; 
            background: #fff;
            border-radius: 28px 28px 0 0; 
            margin-top: -24px;
            padding: 36px 24px 48px; 
            position: relative;
            display: flex; 
            flex-direction: column;
            justify-content: flex-start; 
            overflow-y: auto;
        }}
        .lp-form-logo {{ 
            width: 200px; 
            margin-bottom: 24px;
            align-self: center;
        }}
        .lp-form-desc {{
            font-size: 13px;
            margin-bottom: 28px;
        }}
        .lp-form-box h2 {{ 
            font-size: 22px; 
            margin-bottom: 28px; 
        }}
    }}
    </style>
    """)

    def fazer_login():
        email = email_input.value.strip() if email_input.value else ''
        senha = senha_input.value or ''

        if not email or not senha:
            error_label.style('display: block')
            error_label.set_text('⚠️ Preencha todos os campos.')
            return

        usuario = autenticar_usuario(email, senha)
        if usuario:
            global usuario_atual
            usuario_atual = usuario
            set_usuario_logado(email)
            ui.notify(f'✅ Bem-vindo, {usuario["nome"]}!', type='positive', position='top')
            ui.navigate.to('/app')
        else:
            error_label.style('display: block')
            error_label.set_text('❌ Email ou senha incorretos.')

    def preencher_admin():
        email_input.value = 'admin'
        senha_input.value = 'admin'

    def abrir_cadastro():
        ui.navigate.to('/criar-conta')

    with ui.element('div').classes('lp-root'):

        with ui.element('div').classes('lp-brand'):
            ui.image(LOGO_BRANCA).classes('lp-brand-logo')

        with ui.element('div').classes('lp-form-side'):
            with ui.element('div').classes('lp-form-box'):
                
                with ui.element('div').classes('lp-mobile-header'):
                    ui.image(LOGO).classes('lp-mobile-header-logo')

                with ui.element('div').classes('lp-mobile-form-card'):
                    
                    with ui.element('div').classes('flex justify-center'):
                        ui.image(WORDMARK).classes('lp-form-logo')

                    ui.label('Acompanhe gastos do cartão, defina limites e organize suas finanças com simplicidade.').classes('lp-form-desc')

                    ui.label('Entrar na conta').style(
                        'font-size:26px;font-weight:700;letter-spacing:-0.8px;'
                        'color:#0f0f0f;line-height:1.15;')

                    with ui.element('div').classes('lp-field-wrap'):
                        ui.label('E-mail').classes('lp-field-label')
                        email_input = ui.input(placeholder='admin').props('outlined dense').classes('w-full')

                    with ui.element('div').classes('lp-field-wrap'):
                        ui.label('Senha').classes('lp-field-label')
                        senha_input = ui.input(placeholder='••••••••', password=True, password_toggle_button=True).props('outlined dense').classes('w-full')

                    error_label = ui.label('').classes('lp-error')

                    ui.button('Entrar', on_click=fazer_login).props('no-caps').style(
                        f'width: 100%; height: 48px; border-radius: 11px; '
                        f'background: {cor} !important; color: white !important; '
                        f'border: none; font-size: 15px; font-weight: 600; cursor: pointer; '
                        f'margin-top: 10px; letter-spacing: 0.01em; font-family: "DM Sans", sans-serif;'
                    )

                    with ui.element('div').classes('lp-hint'):
                        ui.label('Acesso rápido').classes('lp-hint-label')
                        ui.label('👑 admin / admin (Demo)').classes('lp-hint-item').on('click', preencher_admin)

                    with ui.element('div').classes('lp-criar-conta'):
                        ui.label('Não tem conta?').classes('text-sm text-gray-400')
                        ui.label('Criar conta gratuita').classes('text-sm font-semibold cursor-pointer').style(f'color: {cor}').on('click', abrir_cadastro)


# =========================
# TELA DE CADASTRO
# =========================
@ui.page('/criar-conta')
def criar_conta():
    cor = config_service.get_primary_color()

    ui.add_head_html(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
    
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    
    html, body {{
        height: 100%;
        width: 100%;
        overflow: hidden;
        font-family: 'DM Sans', sans-serif;
        background: #f3f4f6;
    }}
    
    .cadastro-container {{
        display: flex;
        height: 100vh;
        width: 100%;
        align-items: center;
        justify-content: center;
        padding: 20px;
    }}
    
    .cadastro-card {{
        background: white;
        border-radius: 20px;
        padding: 40px 32px;
        max-width: 440px;
        width: 100%;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
    }}
    
    .cadastro-logo {{
        width: 150px;
        height: auto;
        margin: 0 auto 24px auto;
        display: block;
    }}
    
    .planos-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-bottom: 24px;
    }}
    
    .plano-card {{
        border: 2px solid #e5e7eb;
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        cursor: pointer;
        transition: all 0.2s;
    }}
    
    .plano-card:hover {{
        border-color: {cor};
    }}
    
    .plano-card.selecionado {{
        border-color: {cor};
        background: {cor}08;
    }}
    
    .plano-card h3 {{
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 8px;
    }}
    
    .plano-card p {{
        font-size: 11px;
        color: #6b7280;
        line-height: 1.5;
    }}
    
    .plano-preco {{
        font-size: 24px;
        font-weight: 700;
        color: {cor};
        margin: 8px 0;
    }}
    
    .campo {{
        margin-bottom: 16px;
    }}
    
    .campo label {{
        font-size: 13px;
        font-weight: 500;
        color: #374151;
        margin-bottom: 4px;
        display: block;
    }}
    
    .voltar-link {{
        text-align: center;
        margin-top: 16px;
    }}
    
    .voltar-link span {{
        color: {cor};
        cursor: pointer;
        font-size: 14px;
    }}
    
    .voltar-link span:hover {{
        text-decoration: underline;
    }}
    </style>
    """)

    plano_selecionado = {"plano": "gratuito"}
    
    with ui.element('div').classes('cadastro-container'):
        with ui.element('div').classes('cadastro-card'):
            ui.image(WORDMARK).classes('cadastro-logo')
            
            ui.label('Criar sua Conta').style('font-size:24px;font-weight:700;text-align:center;color:#1f2937;margin-bottom:4px;')
            ui.label('Comece gratuitamente e faça upgrade quando precisar').style('font-size:14px;color:#9ca3af;text-align:center;margin-bottom:24px;')
            
            with ui.element('div').classes('planos-grid'):
                with ui.element('div').classes('plano-card selecionado').on('click', lambda: selecionar_plano('gratuito')):
                    ui.label('🆓 Gratuito').style('font-size:16px;font-weight:700;color:#1f2937;')
                    ui.label('R$ 0').classes('plano-preco')
                    ui.label('• 20 lançamentos/mês').style('font-size:11px;color:#6b7280;')
                    ui.label('• 1 cartão').style('font-size:11px;color:#6b7280;')
                    ui.label('• Modo Unificado').style('font-size:11px;color:#6b7280;')
                    ui.label('• Alertas básicos').style('font-size:11px;color:#6b7280;')
                
                with ui.element('div').classes('plano-card').on('click', lambda: selecionar_plano('premium')):
                    ui.label('💎 Premium').style('font-size:16px;font-weight:700;color:#1f2937;')
                    ui.label('R$ 19,90/mês').classes('plano-preco')
                    ui.label('• Lançamentos ilimitados').style('font-size:11px;color:#6b7280;')
                    ui.label('• Múltiplos cartões').style('font-size:11px;color:#6b7280;')
                    ui.label('• Modo Individual').style('font-size:11px;color:#6b7280;')
                    ui.label('• Consultor Premium').style('font-size:11px;color:#6b7280;')
            
            with ui.element('div').classes('campo'):
                ui.label('Nome completo')
                nome_input = ui.input(placeholder='Seu nome').props('outlined dense').classes('w-full')
            
            with ui.element('div').classes('campo'):
                ui.label('E-mail')
                email_input = ui.input(placeholder='seu@email.com').props('outlined dense').classes('w-full')
            
            with ui.element('div').classes('campo'):
                ui.label('Senha')
                senha_input = ui.input(placeholder='Mínimo 4 caracteres', password=True, password_toggle_button=True).props('outlined dense').classes('w-full')
            
            with ui.element('div').classes('campo'):
                ui.label('Confirmar Senha')
                confirmar_input = ui.input(placeholder='Repita a senha', password=True, password_toggle_button=True).props('outlined dense').classes('w-full')
            
            erro_label = ui.label('').style('color:#ef4444;font-size:13px;text-align:center;display:none;margin-bottom:12px;')
            
            def selecionar_plano(plano):
                plano_selecionado["plano"] = plano
            
            def cadastrar():
                nome = nome_input.value.strip() if nome_input.value else ''
                email = email_input.value.strip() if email_input.value else ''
                senha = senha_input.value or ''
                confirmar = confirmar_input.value or ''
                
                if not nome or not email or not senha:
                    erro_label.style('display:block')
                    erro_label.set_text('⚠️ Preencha todos os campos')
                    return
                
                if senha != confirmar:
                    erro_label.style('display:block')
                    erro_label.set_text('⚠️ Senhas não conferem')
                    return
                
                sucesso, msg, usuario = criar_usuario(nome, email, senha, plano_selecionado["plano"])
                
                if sucesso:
                    ui.notify(f'✅ {msg}', type='positive', position='top', timeout=3000)
                    ui.timer(1.5, lambda: ui.navigate.to('/'), once=True)
                else:
                    erro_label.style('display:block')
                    erro_label.set_text(f'❌ {msg}')
            
            ui.button('Criar Conta', on_click=cadastrar).props('no-caps').style(
                f'width:100%;height:48px;border-radius:11px;'
                f'background:{cor};color:white;border:none;'
                f'font-size:15px;font-weight:600;cursor:pointer;'
                f'font-family:"DM Sans",sans-serif;'
            )
            
            with ui.element('div').classes('voltar-link'):
                ui.label('Já tem conta? Fazer login').on('click', lambda: ui.navigate.to('/'))


# =========================
# TELA PRINCIPAL (PÓS-LOGIN)
# =========================
@ui.page('/app')
def app():
    global usuario_atual, container_principal
    
    if not usuario_atual:
        ui.navigate.to('/')
        return
    
    from telas.lancamentos import tela_lancamentos
    container_principal = ui.element('div').classes('w-full h-screen')
    tela_lancamentos(container_principal)


# =========================
# INICIALIZAÇÃO
# =========================
inicializar()
admin.inicializar_admin()  # Inicializa o painel admin
set_usuario_logado(None)

PORT = int(os.environ.get('PORT', 8080))

ui.run(
    title="Cartometro - Controle Inteligente do seu Crédito",
    favicon=FAVICON,
    reload=False,
    show=False,
    host='0.0.0.0',
    port=PORT,
    storage_secret='cartometro-2024-secret'
)