"""
Cartometro - Controle Inteligente do seu Crédito
"""

from nicegui import ui
from db import (
    inicializar, autenticar_usuario, criar_usuario,
    set_usuario_logado, get_usuario_logado_email, resetar_dados_demo,
    buscar_usuario_por_email, get_plano_usuario,
    verificar_limite_lancamentos, tem_consultor_premium,
    carregar, atualizar_config
)
from config_service import config_service
from auth_service import get_usuario_logado
import admin
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
            
            # Resetar dados demo SEMPRE que logar com demo
            if email == 'demo':
                resetar_dados_demo(email)
            
            set_usuario_logado(email)
            ui.notify(f'✅ Bem-vindo, {usuario["nome"]}!', type='positive', position='top')
            ui.navigate.to('/app')
        else:
            error_label.style('display: block')
            error_label.set_text('❌ Email ou senha incorretos.')

    def preencher_demo():
        email_input.value = 'demo'
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
                        email_input = ui.input(placeholder='demo').props('outlined dense').classes('w-full')

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
                        ui.label('👑 demo / admin (Demonstração)').classes('lp-hint-item').on('click', preencher_demo)

                    with ui.element('div').classes('lp-criar-conta'):
                        ui.label('Não tem conta?').classes('text-sm text-gray-400')
                        ui.label('Criar conta gratuita').classes('text-sm font-semibold cursor-pointer').style(f'color: {cor}').on('click', abrir_cadastro)


# =========================
# TELA DE CADASTRO
# =========================
@ui.page('/criar-conta')
def criar_conta():
    WORDMARK = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845635/wordmark_nf3put.png"
    
    ui.add_head_html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'DM Sans', sans-serif; background: #f3f4f6; overflow-y: auto !important; height: auto !important; }
        .cadastro-page { min-height: 100vh; width: 100%; padding: 20px 16px; display: flex; flex-direction: column; }
        .cadastro-card { background: white; border-radius: 20px; padding: 32px 20px; width: 100%; max-width: 440px; margin: 0 auto; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
        .logo-img { width: 140px; height: auto; margin: 0 auto 20px auto; display: block; }
        .planos-container { display: flex; gap: 10px; margin-bottom: 24px; }
        .plano-card { flex: 1; border: 2px solid #e5e7eb; border-radius: 14px; padding: 14px 10px; text-align: center; cursor: pointer; transition: all 0.2s ease; background: white; }
        .plano-card:active { transform: scale(0.97); }
        .plano-card.selecionado { border-color: #8b5cf6; background: #faf5ff; box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.1); }
        .campo { margin-bottom: 14px; }
        .campo label { font-size: 12px; font-weight: 600; color: #374151; margin-bottom: 4px; display: block; }
        .erro-msg { color: #ef4444; font-size: 12px; text-align: center; padding: 8px; background: #fef2f2; border-radius: 8px; margin-bottom: 12px; display: none; }
        .erro-msg.show { display: block; }
    </style>
    """)

    plano_selecionado = {"plano": "gratuito"}
    planos_refs = {}
    
    with ui.element('div').classes('cadastro-page'):
        with ui.element('div').classes('cadastro-card'):
            ui.image(WORDMARK).classes('logo-img')
            
            ui.label('Criar sua Conta').style('font-size:22px;font-weight:700;text-align:center;color:#1e293b;margin-bottom:4px;')
            ui.label('Comece grátis, faça upgrade quando quiser').style('font-size:13px;color:#9ca3af;text-align:center;margin-bottom:20px;')
            
            with ui.element('div').classes('planos-container'):
                plano_gratuito = ui.element('div').classes('plano-card selecionado')
                with plano_gratuito:
                    ui.label('🆓').style('font-size:28px;')
                    ui.label('Gratuito').style('font-size:14px;font-weight:700;')
                    ui.label('R$ 0').style('font-size:22px;font-weight:700;color:#8b5cf6;')
                    ui.label('para sempre').style('font-size:11px;color:#9ca3af;')
                plano_gratuito.on('click', lambda: selecionar_plano('gratuito'))
                planos_refs['gratuito'] = plano_gratuito
                
                plano_premium = ui.element('div').classes('plano-card')
                with plano_premium:
                    ui.label('💎').style('font-size:28px;')
                    ui.label('Premium').style('font-size:14px;font-weight:700;')
                    ui.label('R$ 4,99').style('font-size:22px;font-weight:700;color:#8b5cf6;')
                    ui.label('/mês').style('font-size:11px;color:#9ca3af;')
                plano_premium.on('click', lambda: selecionar_plano('premium'))
                planos_refs['premium'] = plano_premium
            
            def selecionar_plano(plano):
                plano_selecionado["plano"] = plano
                for nome, ref in planos_refs.items():
                    if nome == plano:
                        ref.classes('plano-card selecionado')
                        ref.style('border-color:#8b5cf6;background:#faf5ff;box-shadow:0 0 0 3px rgba(139,92,246,0.1);')
                    else:
                        ref.classes(remove='selecionado')
                        ref.style('border-color:#e5e7eb;background:white;box-shadow:none;')
                if plano == 'premium':
                    btn_criar.style('background:#8b5cf6;')
                    btn_criar.set_text('Criar Conta Premium')
                else:
                    btn_criar.style('background:#3b82f6;')
                    btn_criar.set_text('Criar Conta Gratuita')
            
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
            
            erro_label = ui.label('').classes('erro-msg')
            
            def cadastrar():
                nome = nome_input.value.strip() if nome_input.value else ''
                email = email_input.value.strip() if email_input.value else ''
                senha = senha_input.value or ''
                confirmar = confirmar_input.value or ''
                
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
            
            with ui.element('div').style('text-align:center;margin-top:16px;'):
                ui.label('Já tem conta? ').style('display:inline;font-size:13px;color:#9ca3af;')
                ui.label('Fazer login').style('display:inline;color:#8b5cf6;font-weight:600;cursor:pointer;font-size:13px;').on('click', lambda: ui.navigate.to('/'))


# =========================
# TELA DE UPGRADE
# =========================
@ui.page('/upgrade')
def tela_upgrade():
    WORDMARK = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845635/wordmark_nf3put.png"
    
    ui.add_head_html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { font-family: 'DM Sans', sans-serif; background: #f3f4f6; overflow-y: auto !important; height: auto !important; }
        .upgrade-page { min-height: 100vh; width: 100%; padding: 20px 16px 40px; }
        .preco-card { background: linear-gradient(135deg, #8b5cf6, #6366f1); border-radius: 20px; padding: 32px 24px; text-align: center; color: white; margin-bottom: 24px; box-shadow: 0 10px 40px rgba(99, 102, 241, 0.3); max-width: 440px; margin-left: auto; margin-right: auto; }
        .metodo-card { display: flex; align-items: center; gap: 12px; padding: 16px; background: white; border: 2px solid #e5e7eb; border-radius: 12px; margin-bottom: 8px; cursor: pointer; transition: all 0.2s; }
        .metodo-card.selecionado { border-color: #8b5cf6; background: #faf5ff; }
    </style>
    """)
    
    metodo_selecionado = {"metodo": "pix"}
    metodos_refs = {}
    
    with ui.element('div').classes('upgrade-page'):
        with ui.element('div').style('text-align:center;margin-bottom:24px;'):
            ui.image(WORDMARK).style('width:120px;height:auto;margin:0 auto 16px auto;display:block;')
            ui.label("Faça Upgrade para Premium").style('font-size:24px;font-weight:800;color:#1e293b;')
        
        with ui.element('div').classes('preco-card'):
            ui.label("R$ 4,99").style('font-size:48px;font-weight:800;')
            ui.label("/mês").style('font-size:16px;opacity:0.8;')
            ui.label("Cancele quando quiser").style('font-size:13px;opacity:0.7;')
        
        with ui.element('div').style('max-width:440px;margin:0 auto 24px;'):
            ui.label("💳 Forma de pagamento").style('font-size:16px;font-weight:700;margin-bottom:12px;')
            
            for metodo_id, icone, nome, desc in [
                ("pix", "📱", "PIX", "Aprovação instantânea"),
                ("cartao", "💳", "Cartão", "Crédito/Débito"),
                ("boleto", "📄", "Boleto", "3 dias úteis"),
            ]:
                is_sel = metodo_id == metodo_selecionado["metodo"]
                card = ui.element('div').classes(f'metodo-card {"selecionado" if is_sel else ""}')
                if is_sel:
                    card.style('border-color:#8b5cf6;background:#faf5ff;')
                with card:
                    ui.label(icone).style('font-size:24px;')
                    with ui.column().classes('gap-0'):
                        ui.label(nome).style('font-size:14px;font-weight:600;')
                        ui.label(desc).style('font-size:11px;color:#64748b;')
                card.on('click', lambda mid=metodo_id: selecionar_metodo(mid))
                metodos_refs[metodo_id] = card
            
            def selecionar_metodo(metodo):
                metodo_selecionado["metodo"] = metodo
                for mid, ref in metodos_refs.items():
                    if mid == metodo:
                        ref.classes('metodo-card selecionado')
                        ref.style('border-color:#8b5cf6;background:#faf5ff;')
                    else:
                        ref.classes(remove='selecionado')
                        ref.style('border-color:#e5e7eb;background:white;')
        
        def assinar():
            from db import get_usuario_logado_email, atualizar_plano_usuario
            from admin import registrar_pagamento
            
            email = get_usuario_logado_email()
            if email:
                atualizar_plano_usuario(email, 'premium')
                registrar_pagamento(email, metodo_selecionado["metodo"], 4.99, "confirmado", "sistema")
                ui.notify("✅ Assinatura Premium ativada!", type="positive", position="top", timeout=3000)
                ui.timer(1.5, lambda: ui.navigate.to('/app'), once=True)
            else:
                ui.notify("⚠️ Faça login primeiro", type="warning", position="top")
        
        ui.button("🚀 Assinar Premium - R$ 4,99/mês", on_click=assinar).style(
            'width:100%;max-width:440px;margin:0 auto;display:block;padding:16px;border-radius:14px;'
            'background:linear-gradient(135deg,#8b5cf6,#6366f1);color:white;border:none;'
            'font-size:16px;font-weight:700;cursor:pointer;'
        )
        
        ui.label("← Voltar para o app").style('text-align:center;margin-top:16px;color:#64748b;cursor:pointer;').on('click', lambda: ui.navigate.to('/app'))


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
admin.inicializar_admin()
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