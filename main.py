"""
Cartometro - Controle Inteligente do seu Crédito
"""

from nicegui import ui
from db import inicializar
from config_service import config_service
from auth_service import get_usuario_logado
import hashlib
import os
import json

# ============================================================
# URLs DAS IMAGENS (CLOUDINARY)
# ============================================================
LOGO_BRANCA = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845617/logo_branca_mmgwof.png"
LOGO_FULL_BRANCA = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845630/logo_full_branca_wlx97y.png"
LOGO = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845521/logo_bvchvv.png"
WORDMARK = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845635/wordmark_nf3put.png"
FAVICON = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845656/favicon_crsq9e.ico"

USUARIOS_ARQ = 'usuarios.json'

usuario_atual = None
container_principal = None


# =========================
# USUÁRIOS
# =========================
def hash_senha(senha):
    """Gera hash SHA-256 da senha"""
    return hashlib.sha256(senha.encode()).hexdigest()


def carregar_usuarios():
    """Carrega usuários do arquivo JSON"""
    if not os.path.exists(USUARIOS_ARQ):
        usuarios = [{
            "id": 1,
            "nome": "Admin",
            "email": "admin",
            "senha": hash_senha("admin"),
            "avatar_emoji": "👤",
            "avatar": "👤"
        }]
        with open(USUARIOS_ARQ, "w", encoding="utf-8") as f:
            json.dump(usuarios, f, indent=2, ensure_ascii=False)
        return usuarios

    with open(USUARIOS_ARQ, "r", encoding="utf-8") as f:
        return json.load(f)


def autenticar(email, senha):
    """Autentica usuário por email e senha"""
    usuarios = carregar_usuarios()
    senha_hash = hash_senha(senha)
    
    for u in usuarios:
        if u.get("email") == email and u.get("senha") == senha_hash:
            return u
    return None


# =========================
# TELA DE LOGIN
# =========================
@ui.page('/')
def login():
    cor        = config_service.get_primary_color()
    cor_escura = config_service.get_primary_dark()

    # ============================================================
    # CSS GLOBAL - ESTILOS GERAIS
    # ============================================================
    ui.add_head_html(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
    
    <!-- FAVICONS -->
    <link rel="icon" type="image/x-icon" href="{FAVICON}">
    <link rel="icon" type="image/png" sizes="16x16" href="{LOGO}">
    <link rel="icon" type="image/png" sizes="32x32" href="{LOGO}">

    /* ============================================================
       RESET E BASE
       ============================================================ */
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

    /* ============================================================
       SEÇÃO 1: DESKTOP - LADO ESQUERDO (BRAND COM LOGO)
       ============================================================ */
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

    /* Círculos decorativos no fundo */
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

    /* Logo grande no centro do brand */
    .lp-brand-logo {{
        width: 420px;
        height: auto;
        position: relative;
        z-index: 1;
        filter: drop-shadow(0 20px 40px rgba(0,0,0,0.25));
    }}

    /* ============================================================
       SEÇÃO 2: DESKTOP - LADO DIREITO (FORMULÁRIO)
       ============================================================ */
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

    /* Logo no topo do formulário */
    .lp-form-logo {{
        width: 220px;
        height: auto;
        margin-bottom: 32px;
        align-self: center;
    }}

    /* Texto descritivo */
    .lp-form-desc {{
        font-size: 14px;
        color: #9ca3af;
        margin-bottom: 36px;
        text-align: center;
        line-height: 1.5;
    }}

    /* Título "Entrar na conta" */
    .lp-form-box h2 {{
        font-size: 26px; 
        font-weight: 700; 
        letter-spacing: -0.8px;
        color: #0f0f0f; 
        margin-bottom: 32px; 
        line-height: 1.15;
    }}

    /* ============================================================
       SEÇÃO 3: CAMPOS DO FORMULÁRIO (COMUM AOS DOIS)
       ============================================================ */
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

    /* ============================================================
       SEÇÃO 3.1: ACESSO RÁPIDO
       ============================================================ */
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

    /* ============================================================
       SEÇÃO 4: MOBILE - ESCONDER LADO BRAND
       ============================================================ */
    @media (max-width: 768px) {{
        body {{ background: #fff; }}
        
        /* Muda layout para coluna */
        .lp-root {{ flex-direction: column; height: 100dvh; }}
        
        /* Esconde o brand do desktop */
        .lp-brand {{ display: none; }}
        
        /* Formulário ocupa tudo */
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

    /* ============================================================
       SEÇÃO 5: MOBILE - HEADER COLORIDO COM LOGO
       ============================================================ */
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

        /* Círculos decorativos mobile */
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
        
        /* Logo no header colorido */
        .lp-mobile-header-logo {{
            width: 250px;
            height: auto;
            position: relative;
            z-index: 1;
            filter: drop-shadow(0 10px 20px rgba(0,0,0,0.25));
        }}

    /* ============================================================
       SEÇÃO 6: MOBILE - CARD BRANCO COM FORMULÁRIO
       ============================================================ */
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
        
        /* Logo dentro do card branco */
        .lp-form-logo {{ 
            width: 200px; 
            margin-bottom: 24px;
            align-self: center;
        }}
        
        /* Texto descritivo mobile */
        .lp-form-desc {{
            font-size: 13px;
            margin-bottom: 28px;
        }}
        
        /* Título menor no mobile */
        .lp-form-box h2 {{ 
            font-size: 22px; 
            margin-bottom: 28px; 
        }}
    }}
    </style>
    """)

    # ============================================================
    # FUNÇÕES DE LOGIN
    # ============================================================
    def fazer_login():
        email = email_input.value or ''
        senha = senha_input.value or ''

        if not email or not senha:
            error_label.style('display: block')
            error_label.set_text('⚠️ Preencha todos os campos.')
            return

        usuario = autenticar(email, senha)
        if usuario:
            global usuario_atual
            usuario_atual = usuario
            ui.notify(f'✅ Bem-vindo, {usuario["nome"]}!', type='positive', position='top')
            ui.navigate.to('/app')
        else:
            error_label.style('display: block')
            error_label.set_text('❌ E-mail ou senha incorretos.')

    def preencher_admin():
        email_input.value = 'admin'
        senha_input.value = 'admin'

    # ============================================================
    # ESTRUTURA HTML
    # ============================================================
    with ui.element('div').classes('lp-root'):

        # ============================================================
        # DESKTOP: LADO ESQUERDO - APENAS LOGO NO FUNDO COLORIDO
        # ============================================================
        with ui.element('div').classes('lp-brand'):
            ui.image(LOGO_BRANCA).classes('lp-brand-logo')

        # ============================================================
        # DESKTOP: LADO DIREITO - FORMULÁRIO BRANCO
        # ============================================================
        with ui.element('div').classes('lp-form-side'):
            with ui.element('div').classes('lp-form-box'):
                
                # ============================================================
                # MOBILE: HEADER COLORIDO (só aparece no mobile)
                # ============================================================
                with ui.element('div').classes('lp-mobile-header'):
                    ui.image(LOGO).classes('lp-mobile-header-logo')

                # ============================================================
                # MOBILE: CARD BRANCO (wrapper no mobile, normal no desktop)
                # ============================================================
                with ui.element('div').classes('lp-mobile-form-card'):
                    
                    # ============================================================
                    # LOGO NO TOPO DO FORMULÁRIO (desktop e mobile)
                    # ============================================================
                    with ui.element('div').classes('flex justify-center'):
                        ui.image(WORDMARK).classes('lp-form-logo')

                    # ============================================================
                    # TEXTO EXPLICATIVO
                    # ============================================================
                    ui.label('Acompanhe gastos do cartão, defina limites e organize suas finanças com simplicidade.').classes('lp-form-desc')

                    # ============================================================
                    # TÍTULO DO FORMULÁRIO
                    # ============================================================
                    ui.label('Entrar na conta').style(
                        'font-size:26px;font-weight:700;letter-spacing:-0.8px;'
                        'color:#0f0f0f;line-height:1.15;')

                    # ============================================================
                    # CAMPO: E-MAIL
                    # ============================================================
                    with ui.element('div').classes('lp-field-wrap'):
                        ui.label('E-mail').classes('lp-field-label')
                        email_input = ui.input(placeholder='admin').props('outlined dense').classes('w-full')

                    # ============================================================
                    # CAMPO: SENHA
                    # ============================================================
                    with ui.element('div').classes('lp-field-wrap'):
                        ui.label('Senha').classes('lp-field-label')
                        senha_input = ui.input(placeholder='••••••••', password=True, password_toggle_button=True).props('outlined dense').classes('w-full')

                    # ============================================================
                    # MENSAGEM DE ERRO
                    # ============================================================
                    error_label = ui.label('').classes('lp-error')

                    # ============================================================
                    # BOTÃO ENTRAR
                    # ============================================================
                    ui.button('Entrar', on_click=fazer_login).props('no-caps').style(
                        f'width: 100%; height: 48px; border-radius: 11px; '
                        f'background: {cor} !important; color: white !important; '
                        f'border: none; font-size: 15px; font-weight: 600; cursor: pointer; '
                        f'margin-top: 10px; letter-spacing: 0.01em; font-family: "DM Sans", sans-serif;'
                    )

                    # ============================================================
                    # ACESSO RÁPIDO - INFORMAÇÃO DE DEMONSTRAÇÃO
                    # ============================================================
                    with ui.element('div').classes('lp-hint'):
                        ui.label('Acesso rápido').classes('lp-hint-label')
                        ui.label('👤 admin / admin').classes('lp-hint-item').on('click', preencher_admin)


# =========================
# TELA PRINCIPAL (PÓS-LOGIN)
# =========================
@ui.page('/app')
def app():
    global usuario_atual, container_principal
    
    if not usuario_atual:
        usuario_atual = get_usuario_logado()
    
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
carregar_usuarios()

# ============================================================
# CONFIGURAÇÃO PARA DEPLOY (RENDER)
# ============================================================
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