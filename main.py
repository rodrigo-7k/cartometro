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
    """Tela de cadastro otimizada para mobile"""

    # ============================================================
    # URLs DAS IMAGENS (CLOUDINARY)
    # ============================================================
    WORDMARK = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845635/wordmark_nf3put.png"
    
    ui.add_head_html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: 'DM Sans', sans-serif;
            background: #f3f4f6;
            overflow-y: auto !important;
            height: auto !important;
        }
        
        .cadastro-page {
            min-height: 100vh;
            width: 100%;
            padding: 20px 16px;
            display: flex;
            flex-direction: column;
        }
        
        .cadastro-card {
            background: white;
            border-radius: 20px;
            padding: 32px 20px;
            width: 100%;
            max-width: 440px;
            margin: 0 auto;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        }
        
        .logo-img {
            width: 140px;
            height: auto;
            margin: 0 auto 20px auto;
            display: block;
        }
        
        .planos-container {
            display: flex;
            gap: 10px;
            margin-bottom: 24px;
        }
        
        .plano-card {
            flex: 1;
            border: 2px solid #e5e7eb;
            border-radius: 14px;
            padding: 14px 10px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
            background: white;
            position: relative;
        }
        
        .plano-card:active {
            transform: scale(0.97);
        }
        
        .plano-card.selecionado {
            border-color: #8b5cf6;
            background: #faf5ff;
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
        }
        
        .plano-icone {
            font-size: 28px;
            margin-bottom: 6px;
        }
        
        .plano-nome {
            font-size: 14px;
            font-weight: 700;
            margin-bottom: 4px;
        }
        
        .plano-preco {
            font-size: 22px;
            font-weight: 700;
            color: #8b5cf6;
            margin-bottom: 2px;
        }
        
        .plano-periodo {
            font-size: 11px;
            color: #9ca3af;
            margin-bottom: 8px;
        }
        
        .plano-beneficios {
            text-align: left;
            font-size: 10px;
            color: #6b7280;
            line-height: 1.6;
        }
        
        .plano-beneficios div {
            padding: 1px 0;
        }
        
        .campo {
            margin-bottom: 14px;
        }
        
        .campo label {
            font-size: 12px;
            font-weight: 600;
            color: #374151;
            margin-bottom: 4px;
            display: block;
        }
        
        .campo input {
            width: 100%;
            padding: 12px 14px;
            border: 1.5px solid #e5e7eb;
            border-radius: 10px;
            font-size: 14px;
            font-family: 'DM Sans', sans-serif;
            transition: border-color 0.2s;
            background: #fafafa;
        }
        
        .campo input:focus {
            outline: none;
            border-color: #8b5cf6;
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
            background: white;
        }
        
        .btn-criar {
            width: 100%;
            padding: 14px;
            border-radius: 12px;
            border: none;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            font-family: 'DM Sans', sans-serif;
            transition: all 0.2s;
        }
        
        .btn-criar:active {
            transform: scale(0.98);
        }
        
        .erro-msg {
            color: #ef4444;
            font-size: 12px;
            text-align: center;
            padding: 8px;
            background: #fef2f2;
            border-radius: 8px;
            margin-bottom: 12px;
            display: none;
        }
        
        .erro-msg.show {
            display: block;
        }
        
        .login-link {
            text-align: center;
            margin-top: 16px;
            font-size: 13px;
            color: #9ca3af;
        }
        
        .login-link a {
            color: #8b5cf6;
            font-weight: 600;
            cursor: pointer;
            text-decoration: none;
        }
        
        .selo-garantia {
            text-align: center;
            margin-top: 12px;
            font-size: 11px;
            color: #9ca3af;
        }
    </style>
    """)
    
    # Estado
    plano_selecionado = {"plano": "gratuito"}
    planos_refs = {}
    
    with ui.element('div').classes('cadastro-page'):
        with ui.element('div').classes('cadastro-card'):
            # Logo
            ui.image(WORDMARK).classes('logo-img')
            
            ui.label('Criar sua Conta').style('font-size:22px;font-weight:700;text-align:center;color:#1e293b;margin-bottom:4px;')
            ui.label('Comece grátis, faça upgrade quando quiser').style('font-size:13px;color:#9ca3af;text-align:center;margin-bottom:20px;')
            
            # ============================================================
            # PLANOS (seleção visual)
            # ============================================================
            with ui.element('div').classes('planos-container'):
                # Gratuito
                plano_gratuito = ui.element('div').classes('plano-card selecionado')
                with plano_gratuito:
                    ui.label('🆓').classes('plano-icone')
                    ui.label('Gratuito').classes('plano-nome')
                    ui.label('R$ 0').classes('plano-preco')
                    ui.label('para sempre').classes('plano-periodo')
                    with ui.element('div').classes('plano-beneficios'):
                        ui.label('✓ 20 lançamentos/mês')
                        ui.label('✓ 1 cartão')
                        ui.label('✓ Alertas básicos')
                plano_gratuito.on('click', lambda: selecionar_plano('gratuito'))
                planos_refs['gratuito'] = plano_gratuito
                
                # Premium
                plano_premium = ui.element('div').classes('plano-card')
                with plano_premium:
                    ui.label('💎').classes('plano-icone')
                    ui.label('Premium').classes('plano-nome')
                    ui.label('R$ 4,99').classes('plano-preco')
                    ui.label('/mês').classes('plano-periodo')
                    with ui.element('div').classes('plano-beneficios'):
                        ui.label('✓ Lançamentos ilimitados')
                        ui.label('✓ Múltiplos cartões')
                        ui.label('✓ Modo Individual')
                        ui.label('✓ Consultor Premium')
                plano_premium.on('click', lambda: selecionar_plano('premium'))
                planos_refs['premium'] = plano_premium
            
            def selecionar_plano(plano):
                plano_selecionado["plano"] = plano
                # Atualizar visual dos cards
                for nome, ref in planos_refs.items():
                    if nome == plano:
                        ref.classes('plano-card selecionado')
                        ref.style('border-color:#8b5cf6;background:#faf5ff;box-shadow:0 0 0 3px rgba(139,92,246,0.1);')
                    else:
                        ref.classes(remove='selecionado')
                        ref.style('border-color:#e5e7eb;background:white;box-shadow:none;')
                
                # Atualizar texto e cor do botão
                if plano == 'premium':
                    btn_criar.style('background:#8b5cf6;')
                    btn_criar.set_text('Criar Conta Premium')
                else:
                    btn_criar.style('background:#3b82f6;')
                    btn_criar.set_text('Criar Conta Gratuita')
            
            # ============================================================
            # CAMPOS
            # ============================================================
            with ui.element('div').classes('campo'):
                ui.label('Nome completo')
                nome_input = ui.input(placeholder='Seu nome completo').props('outlined dense').classes('w-full')
            
            with ui.element('div').classes('campo'):
                ui.label('E-mail')
                email_input = ui.input(placeholder='seu@email.com').props('outlined dense').classes('w-full')
            
            with ui.element('div').classes('campo'):
                ui.label('Senha')
                senha_input = ui.input(placeholder='Mínimo 4 caracteres', password=True, password_toggle_button=True).props('outlined dense').classes('w-full')
            
            with ui.element('div').classes('campo'):
                ui.label('Confirmar Senha')
                confirmar_input = ui.input(placeholder='Repita a senha', password=True, password_toggle_button=True).props('outlined dense').classes('w-full')
            
            # Erro
            erro_label = ui.label('').classes('erro-msg')
            
            # ============================================================
            # BOTÃO CRIAR
            # ============================================================
            def cadastrar():
                nome = nome_input.value.strip() if nome_input.value else ''
                email = email_input.value.strip() if email_input.value else ''
                senha = senha_input.value or ''
                confirmar = confirmar_input.value or ''
                
                # Reset erro
                erro_label.classes(remove='show')
                erro_label.style('display:none;')
                
                if not nome or not email or not senha:
                    erro_label.classes('erro-msg show')
                    erro_label.style('display:block;')
                    erro_label.set_text('⚠️ Preencha todos os campos')
                    return
                
                if senha != confirmar:
                    erro_label.classes('erro-msg show')
                    erro_label.style('display:block;')
                    erro_label.set_text('⚠️ Senhas não conferem')
                    return
                
                if len(senha) < 4:
                    erro_label.classes('erro-msg show')
                    erro_label.style('display:block;')
                    erro_label.set_text('⚠️ Senha deve ter pelo menos 4 caracteres')
                    return
                
                sucesso, msg, usuario = criar_usuario(nome, email, senha, plano_selecionado["plano"])
                
                if sucesso:
                    plano_nome = 'Premium' if plano_selecionado["plano"] == 'premium' else 'Gratuito'
                    ui.notify(f'✅ Conta {plano_nome} criada! Faça login.', type='positive', position='top', timeout=3000)
                    ui.timer(1.5, lambda: ui.navigate.to('/'), once=True)
                else:
                    erro_label.classes('erro-msg show')
                    erro_label.style('display:block;')
                    erro_label.set_text(f'❌ {msg}')
            
            btn_criar = ui.button('Criar Conta Gratuita', on_click=cadastrar).props('no-caps')
            btn_criar.style(
                'width:100%;padding:14px;border-radius:12px;'
                'background:#3b82f6;color:white;border:none;'
                'font-size:15px;font-weight:600;cursor:pointer;'
                'font-family:"DM Sans",sans-serif;transition:all 0.2s;'
            )
            
            # Link login
            with ui.element('div').classes('login-link'):
                ui.label('Já tem conta? ').style('display:inline;font-size:13px;color:#9ca3af;')
                ui.label('Fazer login').style('display:inline;color:#8b5cf6;font-weight:600;cursor:pointer;font-size:13px;').on('click', lambda: ui.navigate.to('/'))
            
            # Selo
            with ui.element('div').classes('selo-garantia'):
                ui.label('🔒 Seus dados estão seguros')
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

@ui.page('/upgrade')
def tela_upgrade():
    """Tela de upgrade para Premium - Cartometro"""
    
    # URLs das imagens
    WORDMARK = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845635/wordmark_nf3put.png"
    
    ui.add_head_html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: 'DM Sans', sans-serif;
            background: #f3f4f6;
            overflow-y: auto !important;
            height: auto !important;
        }
        
        .upgrade-page {
            min-height: 100vh;
            width: 100%;
            padding: 20px 16px 40px;
        }
        
        .upgrade-header {
            text-align: center;
            margin-bottom: 32px;
        }
        
        .upgrade-logo {
            width: 120px;
            height: auto;
            margin: 0 auto 16px auto;
            display: block;
        }
        
        .upgrade-title {
            font-size: 28px;
            font-weight: 800;
            color: #1e293b;
            margin-bottom: 8px;
        }
        
        .upgrade-subtitle {
            font-size: 15px;
            color: #64748b;
            line-height: 1.5;
        }
        
        .preco-card {
            background: linear-gradient(135deg, #8b5cf6, #6366f1);
            border-radius: 20px;
            padding: 32px 24px;
            text-align: center;
            color: white;
            margin-bottom: 24px;
            box-shadow: 0 10px 40px rgba(99, 102, 241, 0.3);
            max-width: 440px;
            margin-left: auto;
            margin-right: auto;
        }
        
        .preco-valor {
            font-size: 56px;
            font-weight: 800;
            line-height: 1;
            margin-bottom: 4px;
        }
        
        .preco-periodo {
            font-size: 16px;
            opacity: 0.8;
            margin-bottom: 8px;
        }
        
        .preco-descricao {
            font-size: 13px;
            opacity: 0.7;
        }
        
        .beneficios-section {
            max-width: 440px;
            margin: 0 auto 24px;
        }
        
        .beneficios-title {
            font-size: 18px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 16px;
        }
        
        .beneficio-item {
            display: flex;
            align-items: flex-start;
            gap: 12px;
            padding: 14px 16px;
            background: white;
            border-radius: 12px;
            margin-bottom: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }
        
        .beneficio-icone {
            width: 40px;
            height: 40px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
            flex-shrink: 0;
        }
        
        .beneficio-texto h3 {
            font-size: 14px;
            font-weight: 600;
            color: #1e293b;
            margin-bottom: 2px;
        }
        
        .beneficio-texto p {
            font-size: 12px;
            color: #64748b;
            line-height: 1.4;
        }
        
        .comparativo {
            max-width: 440px;
            margin: 0 auto 24px;
            background: white;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }
        
        .comparativo-header {
            display: flex;
            background: #f8fafc;
            font-weight: 600;
            font-size: 12px;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .comparativo-header div {
            padding: 12px 16px;
            text-align: center;
        }
        
        .comparativo-row {
            display: flex;
            border-bottom: 1px solid #f1f5f9;
            font-size: 13px;
        }
        
        .comparativo-row:last-child {
            border-bottom: none;
        }
        
        .comparativo-row div {
            padding: 12px 16px;
            text-align: center;
        }
        
        .comparativo-label {
            text-align: left !important;
            color: #1e293b;
            font-weight: 500;
        }
        
        .check { color: #10b981; font-weight: 600; }
        .uncheck { color: #ef4444; }
        
        .metodos-pagamento {
            max-width: 440px;
            margin: 0 auto 24px;
        }
        
        .metodo-card {
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 16px;
            background: white;
            border: 2px solid #e5e7eb;
            border-radius: 12px;
            margin-bottom: 8px;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .metodo-card:hover {
            border-color: #8b5cf6;
        }
        
        .metodo-card.selecionado {
            border-color: #8b5cf6;
            background: #faf5ff;
            box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1);
        }
        
        .metodo-icone {
            font-size: 28px;
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
        
        .metodo-info h3 {
            font-size: 14px;
            font-weight: 600;
            color: #1e293b;
        }
        
        .metodo-info p {
            font-size: 11px;
            color: #64748b;
        }
        
        .btn-assinar {
            width: 100%;
            max-width: 440px;
            margin: 0 auto;
            display: block;
            padding: 16px;
            border-radius: 14px;
            border: none;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            font-family: 'DM Sans', sans-serif;
            transition: all 0.2s;
        }
        
        .btn-assinar:active {
            transform: scale(0.98);
        }
        
        .btn-voltar {
            display: block;
            text-align: center;
            margin-top: 16px;
            font-size: 14px;
            color: #64748b;
            cursor: pointer;
        }
        
        .btn-voltar:hover {
            color: #1e293b;
        }
        
        .garantia {
            text-align: center;
            margin-top: 16px;
            font-size: 12px;
            color: #94a3b8;
        }
        
        /* Mobile */
        @media (max-width: 480px) {
            .preco-valor { font-size: 44px; }
            .upgrade-title { font-size: 24px; }
        }
    </style>
    """)
    
    metodo_selecionado = {"metodo": "pix"}
    metodos_refs = {}
    
    with ui.element('div').classes('upgrade-page'):
        
        # ============================================================
        # HEADER
        # ============================================================
        with ui.element('div').classes('upgrade-header'):
            ui.image(WORDMARK).classes('upgrade-logo')
            ui.label("Faça Upgrade para Premium").classes('upgrade-title')
            ui.label("Desbloqueie todos os recursos e tenha controle total das suas finanças").classes('upgrade-subtitle')
        
        # ============================================================
        # CARD DE PREÇO
        # ============================================================
        with ui.element('div').classes('preco-card'):
            ui.label("R$").style('font-size:20px;opacity:0.8;')
            ui.label("4,99").classes('preco-valor')
            ui.label("/mês").classes('preco-periodo')
            ui.label("Cancele quando quiser • Sem taxas escondidas").classes('preco-descricao')
        
        # ============================================================
        # BENEFÍCIOS
        # ============================================================
        with ui.element('div').classes('beneficios-section'):
            ui.label("✨ O que você ganha:").classes('beneficios-title')
            
            beneficios = [
                {
                    "icone": "📊",
                    "cor": "#3b82f6",
                    "titulo": "Lançamentos Ilimitados",
                    "descricao": "Registre quantos gastos quiser, sem limite mensal"
                },
                {
                    "icone": "💳",
                    "cor": "#8b5cf6",
                    "titulo": "Múltiplos Cartões",
                    "descricao": "Cadastre vários cartões e controle cada um individualmente"
                },
                {
                    "icone": "🔀",
                    "cor": "#10b981",
                    "titulo": "Modo Individual",
                    "descricao": "Cada cartão com seu próprio limite e data de fechamento"
                },
                {
                    "icone": "🤖",
                    "cor": "#f59e0b",
                    "titulo": "Consultor Premium",
                    "descricao": "30+ alertas inteligentes com análises detalhadas"
                },
                {
                    "icone": "📈",
                    "cor": "#ec4899",
                    "titulo": "Relatórios Avançados",
                    "descricao": "Análise de gastos por categoria, período e tendências"
                },
                {
                    "icone": "⚡",
                    "cor": "#6366f1",
                    "titulo": "Suporte Prioritário",
                    "descricao": "Atendimento rápido e personalizado"
                },
            ]
            
            for b in beneficios:
                with ui.element('div').classes('beneficio-item'):
                    with ui.element('div').classes('beneficio-icone').style(f'background:{b["cor"]}15;'):
                        ui.label(b["icone"]).style('font-size:20px;')
                    with ui.element('div').classes('beneficio-texto'):
                        ui.label(b["titulo"]).style('font-size:14px;font-weight:600;color:#1e293b;margin-bottom:2px;')
                        ui.label(b["descricao"]).style('font-size:12px;color:#64748b;')
        
        # ============================================================
        # COMPARATIVO
        # ============================================================
        with ui.element('div').classes('comparativo'):
            # Header
            with ui.element('div').classes('comparativo-header'):
                ui.label("Funcionalidade").style('flex:2;text-align:left;')
                ui.label("Gratuito").style('flex:1;')
                ui.label("Premium").style('flex:1;color:#8b5cf6;')
            
            comparativos = [
                ("Lançamentos/mês", "20", "Ilimitado", True),
                ("Cartões", "1", "Ilimitado", True),
                ("Modo Individual", "❌", "✅", True),
                ("Consultor Financeiro", "6 alertas", "30+ alertas", True),
                ("Relatórios", "Básico", "Avançado", True),
                ("Suporte", "Normal", "Prioritário", True),
            ]
            
            for label, gratuito, premium, destaque in comparativos:
                with ui.element('div').classes('comparativo-row'):
                    ui.label(label).classes('comparativo-label').style('flex:2;')
                    ui.label(gratuito).classes('uncheck').style('flex:1;')
                    ui.label(premium).classes('check').style('flex:1;')
        
        # ============================================================
        # MÉTODOS DE PAGAMENTO
        # ============================================================
        with ui.element('div').classes('metodos-pagamento'):
            ui.label("💳 Forma de pagamento").classes('beneficios-title')
            
            metodos = [
                {
                    "id": "pix",
                    "icone": "📱",
                    "titulo": "PIX",
                    "descricao": "Aprovação instantânea",
                    "cor": "#10b981"
                },
                {
                    "id": "cartao",
                    "icone": "💳",
                    "titulo": "Cartão de Crédito",
                    "descricao": "Visa, Mastercard, Elo",
                    "cor": "#3b82f6"
                },
                {
                    "id": "boleto",
                    "icone": "📄",
                    "titulo": "Boleto Bancário",
                    "descricao": "Compensação em até 3 dias",
                    "cor": "#f59e0b"
                },
            ]
            
            for m in metodos:
                is_selecionado = m["id"] == metodo_selecionado["metodo"]
                card = ui.element('div').classes(f'metodo-card {"selecionado" if is_selecionado else ""}')
                if is_selecionado:
                    card.style('border-color:#8b5cf6;background:#faf5ff;box-shadow:0 0 0 3px rgba(139,92,246,0.1);')
                
                with card:
                    with ui.element('div').classes('metodo-icone').style(f'background:{m["cor"]}15;'):
                        ui.label(m["icone"]).style('font-size:24px;')
                    with ui.element('div').classes('metodo-info'):
                        ui.label(m["titulo"]).style('font-size:14px;font-weight:600;')
                        ui.label(m["descricao"]).style('font-size:11px;color:#64748b;')
                
                card.on('click', lambda mid=m["id"]: selecionar_metodo(mid))
                metodos_refs[m["id"]] = card
            
            def selecionar_metodo(metodo):
                metodo_selecionado["metodo"] = metodo
                for mid, ref in metodos_refs.items():
                    if mid == metodo:
                        ref.classes('metodo-card selecionado')
                        ref.style('border-color:#8b5cf6;background:#faf5ff;box-shadow:0 0 0 3px rgba(139,92,246,0.1);')
                    else:
                        ref.classes(remove='selecionado')
                        ref.style('border-color:#e5e7eb;background:white;box-shadow:none;')
        
        # ============================================================
        # BOTÃO ASSINAR
        # ============================================================
        def assinar():
            metodo = metodo_selecionado["metodo"]
            nomes = {"pix": "PIX", "cartao": "Cartão de Crédito", "boleto": "Boleto"}
            nome_metodo = nomes.get(metodo, metodo)
            
            from db import get_usuario_logado_email, atualizar_plano_usuario, registrar_pagamento
            
            email = get_usuario_logado_email()
            if email:
                try:
                    atualizar_plano_usuario(email, 'premium')
                    # Registrar pagamento simulado
                    from db import carregar_pagamentos, salvar_pagamentos
                    pagamentos = carregar_pagamentos() if hasattr(carregar_pagamentos, '__call__') else []
                    pagamentos.append({
                        "id": len(pagamentos) + 1,
                        "email": email,
                        "metodo": metodo,
                        "valor": 4.99,
                        "status": "confirmado",
                        "admin": "sistema",
                        "data": datetime.now().isoformat()
                    })
                    # Importar função correta
                    from admin import registrar_pagamento
                    registrar_pagamento(email, metodo, 4.99, "confirmado", "sistema")
                    
                    ui.notify(f"✅ Assinatura Premium ativada via {nome_metodo}!", type="positive", position="top", timeout=3000)
                    ui.timer(1.5, lambda: ui.navigate.to('/app'), once=True)
                except Exception as e:
                    ui.notify(f"❌ Erro: {str(e)}", type="negative", position="top")
            else:
                ui.notify("⚠️ Faça login primeiro", type="warning", position="top")
        
        ui.button(f"🚀 Assinar Premium - R$ 4,99/mês", on_click=assinar).classes('btn-assinar').style(
            'background:linear-gradient(135deg,#8b5cf6,#6366f1);color:white;'
        )
        
        # Voltar
        ui.label("← Voltar para o app").classes('btn-voltar').on('click', lambda: ui.navigate.to('/app'))
        
        # Garantia
        with ui.element('div').classes('garantia'):
            ui.label("🔒 Pagamento seguro • Cancele quando quiser • Satisfação garantida")

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