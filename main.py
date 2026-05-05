"""
Cartometro - Controle Inteligente do seu Crédito
Landing Page + App
"""

from nicegui import ui
from db import (
    inicializar, autenticar_usuario, criar_usuario,
    set_usuario_logado, get_usuario_logado_email, resetar_dados_demo,
    buscar_usuario_por_email, get_plano_usuario,
    verificar_limite_lancamentos, tem_consultor_premium,
    carregar, atualizar_config, carregar_usuarios
)
from config_service import config_service
from auth_service import get_usuario_logado
import admin
import os
import sys

# ============================================================
# DETECÇÃO DE AMBIENTE
# ============================================================
IS_PRODUCTION = os.environ.get('RENDER', False) or os.environ.get('PRODUCTION', False)
IS_DEVELOPMENT = not IS_PRODUCTION

print(f"🌍 Ambiente: {'PRODUÇÃO (Render)' if IS_PRODUCTION else 'DESENVOLVIMENTO (Local)'}")
print(f"📁 Diretório atual: {os.getcwd()}")
print(f"🐍 Python: {sys.version}")

# ============================================================
# URLS DAS IMAGENS (CLOUDINARY)
# ============================================================
LOGO_BRANCA      = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845617/logo_branca_mmgwof.png"
LOGO_FULL_BRANCA = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845630/logo_full_branca_wlx97y.png"
LOGO             = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845521/logo_bvchvv.png"
WORDMARK         = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845635/wordmark_nf3put.png"
LOGO_FULL_COLOR  = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845644/logo_full_b6tse3.png"
LOGO_COMPLETA    = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845648/logo_completa_nbtgcz.png"
FAVICON          = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845656/favicon_crsq9e.ico"

# Imagens placeholder
PRINT_DASHBOARD   = "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80"
PRINT_CARTOES     = "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800&q=80"
PRINT_LANCAMENTOS = "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&q=80"
PRINT_RELATORIOS  = "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&q=80"

# ============================================================
# VARIÁVEIS GLOBAIS
# ============================================================
usuario_atual = None
container_principal = None


# ============================================================
# CRIAÇÃO DE USUÁRIOS PADRÃO
# ============================================================
def criar_usuarios_padrao():
    """Cria usuários padrão para desenvolvimento e produção"""
    usuarios = carregar_usuarios()
    emails_existentes = [u.get('email', '').lower() for u in usuarios]
    
    # Usuário Demo (sempre criar se não existir)
    if 'demo' not in emails_existentes:
        print("👤 Criando usuário Demo...")
        sucesso, msg, _ = criar_usuario('Usuário Demo', 'demo', 'demo', 'premium')
        if sucesso:
            print("✅ Usuário Demo criado com sucesso!")
            # Garantir que o demo tenha dados de exemplo
            resetar_dados_demo('demo')
        else:
            print(f"❌ Erro ao criar Demo: {msg}")
    else:
        print("👤 Usuário Demo já existe")
    
    # Usuário Teste Local (apenas em desenvolvimento)
    if IS_DEVELOPMENT and 'teste@local.com' not in emails_existentes:
        print("👤 Criando usuário de teste local...")
        sucesso, msg, _ = criar_usuario('Teste Local', 'teste@local.com', 'teste123', 'premium')
        if sucesso:
            print("✅ Usuário de teste local criado!")
        else:
            print(f"❌ Erro ao criar teste local: {msg}")
    
    # Usuário Admin App (para testes)
    if 'admin@app.com' not in emails_existentes:
        print("👤 Criando usuário admin do app...")
        sucesso, msg, _ = criar_usuario('Admin App', 'admin@app.com', 'admin123', 'premium')
        if sucesso:
            print("✅ Usuário admin do app criado!")
        else:
            print(f"❌ Erro ao criar admin app: {msg}")


# ============================================================
# LANDING PAGE
# ============================================================
@ui.page('/')
def landing_page():
    """Landing Page Profissional do Cartometro"""
    
    ui.add_head_html(f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="icon" type="image/x-icon" href="{FAVICON}">
    <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    
    html, body, #app, .q-page-container, .q-page, .nicegui-content {{
        margin: 0 !important;
        padding: 0 !important;
        max-width: 100% !important;
        width: 100% !important;
        overflow-x: hidden;
    }}
    
    body {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: #ffffff;
        color: #0f172a;
        -webkit-font-smoothing: antialiased;
    }}
    
    .container-lg {{
        width: 90% !important;
        max-width: 1600px !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }}
    
    @media (min-width: 1920px) {{
        .container-lg {{
            width: 92% !important;
            max-width: 1800px !important;
        }}
    }}
    
    /* ========== NAVBAR ========== */
    .navbar {{
        position: fixed;
        top: 0; left: 0; right: 0;
        z-index: 1000;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(0, 0, 0, 0.06);
    }}
    
    .navbar.scrolled {{ box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08); }}
    
    .navbar-inner {{
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 72px;
        width: 90%;
        max-width: 1600px;
        margin: 0 auto;
    }}
    
    @media (min-width: 1920px) {{
        .navbar-inner {{ width: 92%; max-width: 1800px; }}
    }}
    
    .navbar-logo-img {{
        height: 120px;
        width: auto;
        display: block;
    }}
    
    .navbar-links {{
        display: flex;
        align-items: center;
        gap: 8px;
    }}
    
    .nav-link {{
        color: #475569;
        font-size: 14px;
        font-weight: 500;
        padding: 8px 16px;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.2s;
        border: none;
        background: none;
        font-family: inherit;
    }}
    
    .nav-link:hover {{ color: #7c3aed; background: #f5f3ff; }}
    
    .btn-primary {{
        background: #7c3aed;
        color: white !important;
        font-weight: 600;
        padding: 10px 20px;
        border-radius: 10px;
        border: none;
        cursor: pointer;
        font-size: 14px;
        font-family: inherit;
        transition: all 0.2s;
        box-shadow: 0 1px 2px rgba(124, 58, 237, 0.3);
    }}
    
    .btn-primary:hover {{
        background: #6d28d9;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.4);
        transform: translateY(-1px);
    }}
    
    .btn-secondary {{
        background: transparent;
        color: #7c3aed !important;
        font-weight: 600;
        padding: 10px 20px;
        border-radius: 10px;
        border: 2px solid #e9d5ff;
        cursor: pointer;
        font-size: 14px;
        font-family: inherit;
        transition: all 0.2s;
    }}
    
    .btn-secondary:hover {{ background: #f5f3ff; border-color: #7c3aed; }}
    
    .mobile-menu-btn {{
        display: none;
        background: none;
        border: none;
        font-size: 28px;
        cursor: pointer;
        color: #475569;
        padding: 4px 8px;
    }}
    
    /* ========== HERO ========== */
    .hero {{
        width: 100%;
        padding: 140px 0 100px;
        background: linear-gradient(135deg, #faf5ff 0%, #f0f4ff 50%, #ffffff 100%);
    }}
    
    .hero-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 80px;
        align-items: center;
    }}
    
    .hero-content {{ max-width: 600px; }}
    
    .hero-badge {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: white;
        border: 1px solid #e9d5ff;
        color: #7c3aed;
        font-size: 13px;
        font-weight: 600;
        padding: 6px 16px;
        border-radius: 100px;
        margin-bottom: 24px;
    }}
    
    .hero-badge-dot {{
        width: 6px;
        height: 6px;
        background: #7c3aed;
        border-radius: 50%;
    }}
    
    .hero-title {{
        font-size: clamp(36px, 5vw, 64px);
        font-weight: 900;
        line-height: 1.08;
        letter-spacing: -1.5px;
        color: #0f172a;
        margin-bottom: 20px;
    }}
    
    .hero-title span {{
        background: linear-gradient(135deg, #7c3aed, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }}
    
    .hero-description {{
        font-size: 18px;
        color: #64748b;
        line-height: 1.7;
        margin-bottom: 32px;
    }}
    
    .hero-actions {{
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        margin-bottom: 40px;
    }}
    
    .hero-cta {{
        background: #7c3aed;
        color: white !important;
        font-weight: 600;
        font-size: 16px;
        padding: 16px 32px;
        border-radius: 12px;
        border: none;
        cursor: pointer;
        font-family: inherit;
        transition: all 0.2s;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
    }}
    
    .hero-cta:hover {{
        background: #6d28d9;
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
        transform: translateY(-2px);
    }}
    
    .hero-demo {{
        background: white;
        color: #475569 !important;
        font-weight: 600;
        font-size: 16px;
        padding: 16px 32px;
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        cursor: pointer;
        font-family: inherit;
        transition: all 0.2s;
    }}
    
    .hero-demo:hover {{ border-color: #c4b5fd; color: #7c3aed !important; }}
    
    .hero-trust {{
        display: flex;
        align-items: center;
        gap: 16px;
        color: #94a3b8;
        font-size: 13px;
        flex-wrap: wrap;
    }}
    
    .hero-image-wrapper {{
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    
    .hero-image {{
        width: 100%;
        border-radius: 20px;
        box-shadow: 0 30px 60px -12px rgba(0, 0, 0, 0.25);
        display: block;
    }}
    
    /* ========== LOGO SHOWCASE ========== */
    .logo-showcase {{
        width: 100%;
        padding: 80px 0;
        background: #f8fafc;
        text-align: center;
        border-top: 1px solid #f1f5f9;
        border-bottom: 1px solid #f1f5f9;
    }}
    
    .logo-showcase-label {{
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 0.12em;
        color: #94a3b8;
        text-transform: uppercase;
        margin-bottom: 32px;
    }}
    
    .logo-showcase-img {{
        width: 100%;
        max-width: 600px;
        height: auto;
        margin: 0 auto;
        display: block;
    }}
    
    /* ========== FEATURES ========== */
    .features {{
        width: 100%;
        padding: 100px 0;
        background: white;
    }}
    
    .section-header {{
        text-align: center;
        margin-bottom: 64px;
    }}
    
    .section-badge {{
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: #f5f3ff;
        color: #7c3aed;
        font-size: 13px;
        font-weight: 700;
        padding: 6px 16px;
        border-radius: 100px;
        margin-bottom: 16px;
    }}
    
    .section-title {{
        font-size: clamp(32px, 4vw, 48px);
        font-weight: 900;
        color: #0f172a;
        margin-bottom: 16px;
        letter-spacing: -1px;
    }}
    
    .section-description {{
        font-size: 18px;
        color: #64748b;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.6;
    }}
    
    .features-grid {{
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 24px;
    }}
    
    .feature-card {{
        padding: 32px;
        background: #fafafa;
        border: 1px solid #f1f5f9;
        border-radius: 16px;
        transition: all 0.3s;
    }}
    
    .feature-card:hover {{
        background: white;
        border-color: #e9d5ff;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        transform: translateY(-4px);
    }}
    
    .feature-icon {{
        width: 48px;
        height: 48px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 24px;
        margin-bottom: 20px;
    }}
    
    .feature-title {{ font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 8px; }}
    .feature-description {{ font-size: 14px; color: #64748b; line-height: 1.6; }}
    
    /* ========== APP SHOWCASE ========== */
    .app-showcase {{ width: 100%; padding: 100px 0; background: #fafafa; }}
    
    .showcase-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 48px;
        margin-top: 64px;
    }}
    
    .showcase-image {{
        width: 100%;
        height: 260px;
        object-fit: cover;
        border-radius: 16px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        margin-bottom: 24px;
        display: block;
    }}
    
    .showcase-title {{ font-size: 20px; font-weight: 700; color: #0f172a; margin-bottom: 8px; }}
    .showcase-description {{ font-size: 14px; color: #64748b; line-height: 1.6; }}
    
    /* ========== HOW IT WORKS ========== */
    .how-it-works {{ width: 100%; padding: 100px 0; background: white; }}
    
    .how-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 80px;
        align-items: center;
        margin-top: 64px;
    }}
    
    .how-steps {{ display: flex; flex-direction: column; gap: 32px; }}
    .how-step {{ display: flex; gap: 20px; }}
    
    .step-number {{
        width: 48px;
        height: 48px;
        background: linear-gradient(135deg, #7c3aed, #6366f1);
        color: white;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        font-weight: 800;
        flex-shrink: 0;
    }}
    
    .step-content h3 {{ font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 4px; }}
    .step-content p {{ font-size: 14px; color: #64748b; line-height: 1.6; }}
    
    .how-image {{
        width: 100%;
        border-radius: 16px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        display: block;
    }}
    
    /* ========== PRICING ========== */
    .pricing {{ width: 100%; padding: 100px 0; background: #fafafa; }}
    
    .pricing-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 32px;
        max-width: 900px;
        margin: 64px auto 0;
    }}
    
    .plan-card {{
        border: 2px solid #e2e8f0;
        border-radius: 20px;
        padding: 40px 32px;
        background: white;
        transition: all 0.3s;
        position: relative;
    }}
    
    .plan-card:hover {{ border-color: #c4b5fd; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08); }}
    
    .plan-card.featured {{
        border-color: #7c3aed;
        background: linear-gradient(135deg, #faf5ff, #ffffff);
        box-shadow: 0 20px 40px rgba(124, 58, 237, 0.1);
    }}
    
    .plan-badge {{
        position: absolute;
        top: -14px;
        left: 50%;
        transform: translateX(-50%);
        background: linear-gradient(135deg, #7c3aed, #6366f1);
        color: white;
        font-size: 12px;
        font-weight: 700;
        padding: 6px 24px;
        border-radius: 100px;
        white-space: nowrap;
    }}
    
    .plan-header {{ text-align: center; margin-bottom: 28px; }}
    .plan-name {{ font-size: 22px; font-weight: 800; color: #0f172a; margin-bottom: 8px; }}
    .plan-price {{ font-size: 52px; font-weight: 900; color: #7c3aed; line-height: 1; margin-bottom: 4px; }}
    .plan-period {{ font-size: 14px; color: #94a3b8; }}
    .plan-divider {{ height: 1px; background: #f1f5f9; margin-bottom: 24px; }}
    
    .plan-features {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-bottom: 32px;
    }}
    
    .plan-feature {{ display: flex; align-items: center; gap: 8px; font-size: 13px; color: #475569; }}
    
    .plan-btn {{
        width: 100%;
        padding: 16px;
        border-radius: 12px;
        font-size: 16px;
        font-weight: 700;
        font-family: inherit;
        cursor: pointer;
        transition: all 0.2s;
        border: none;
        text-align: center;
        display: block;
    }}
    
    .plan-btn.primary {{
        background: linear-gradient(135deg, #7c3aed, #6366f1);
        color: white;
        box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3);
    }}
    
    .plan-btn.primary:hover {{ box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4); transform: translateY(-2px); }}
    .plan-btn.secondary {{ background: transparent; color: #7c3aed; border: 2px solid #e9d5ff; }}
    .plan-btn.secondary:hover {{ background: #f5f3ff; border-color: #7c3aed; }}
    
    /* ========== CTA ========== */
    .cta {{ width: 100%; padding: 100px 0; background: linear-gradient(135deg, #6d28d9, #4f46e5); }}
    .cta-content {{ text-align: center; }}
    
    .cta-title {{
        font-size: clamp(32px, 4vw, 48px);
        font-weight: 900;
        color: white;
        margin-bottom: 20px;
        letter-spacing: -1px;
    }}
    
    .cta-description {{
        font-size: 18px;
        color: rgba(255, 255, 255, 0.9);
        line-height: 1.7;
        margin-bottom: 40px;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }}
    
    .cta-btn {{
        background: white;
        color: #6d28d9 !important;
        font-weight: 700;
        font-size: 16px;
        padding: 18px 40px;
        border-radius: 14px;
        border: none;
        cursor: pointer;
        font-family: inherit;
        transition: all 0.2s;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    }}
    
    .cta-btn:hover {{ transform: translateY(-2px); box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3); }}
    
    /* ========== FOOTER ========== */
    .footer {{ width: 100%; background: #0f172a; padding: 48px 0 32px; color: #94a3b8; }}
    
    .footer-grid {{
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 1fr;
        gap: 48px;
        padding-bottom: 32px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }}
    
    .footer-brand-img {{ height: 48px; width: auto; margin-bottom: 12px; display: block; }}
    .footer-brand p {{ font-size: 13px; line-height: 1.7; color: #64748b; max-width: 260px; }}
    .footer-col h4 {{ font-size: 13px; font-weight: 700; color: #e2e8f0; margin-bottom: 16px; }}
    .footer-col a {{ display: block; font-size: 13px; color: #64748b; margin-bottom: 10px; text-decoration: none; transition: color 0.2s; cursor: pointer; }}
    .footer-col a:hover {{ color: #e2e8f0; }}
    .footer-bottom {{ text-align: center; margin-top: 24px; }}
    .footer-copyright {{ font-size: 13px; color: #475569; }}
    
    /* ========== RESPONSIVO ========== */
    @media (max-width: 1024px) {{
        .hero-grid {{ grid-template-columns: 1fr; gap: 48px; }}
        .features-grid {{ grid-template-columns: repeat(2, 1fr); }}
        .showcase-grid {{ grid-template-columns: 1fr 1fr; }}
        .how-grid {{ grid-template-columns: 1fr; gap: 48px; }}
        .footer-grid {{ grid-template-columns: 1fr 1fr; gap: 32px; }}
    }}
    
    @media (max-width: 768px) {{
        .navbar-links {{ display: none; }}
        .mobile-menu-btn {{ display: block; }}
        .hero {{ padding: 110px 0 60px; }}
        .hero-grid {{ grid-template-columns: 1fr; gap: 32px; }}
        .features-grid {{ grid-template-columns: 1fr; }}
        .showcase-grid {{ grid-template-columns: 1fr; }}
        .pricing-grid {{ display: flex; flex-direction: row; gap: 16px; overflow-x: auto; scroll-snap-type: x mandatory; padding: 20px 0 24px; scrollbar-width: none; }}
        .pricing-grid::-webkit-scrollbar {{ display: none; }}
        .plan-card {{ min-width: 280px; flex-shrink: 0; scroll-snap-align: start; }}
        .footer-grid {{ grid-template-columns: 1fr; gap: 28px; }}
        .container-lg {{ width: 94% !important; }}
        .logo-showcase-img {{ max-width: 400px; }}
    }}
    </style>
    
    <script>
    window.addEventListener('scroll', function() {{
        var nav = document.querySelector('.navbar');
        if(nav) {{
            if(window.scrollY > 20) {{ nav.classList.add('scrolled'); }}
            else {{ nav.classList.remove('scrolled'); }}
        }}
    }});
    </script>
    """)
    
    # ========== NAVBAR ==========
    with ui.element('nav').classes('navbar'):
        with ui.element('div').classes('navbar-inner'):
            ui.html(f'<a href="/"><img src="{LOGO_FULL_COLOR}" alt="Cartometro" class="navbar-logo-img"></a>')
            with ui.element('div').classes('navbar-links'):
                ui.button('Funcionalidades', on_click=lambda: ui.run_javascript('document.getElementById("features-section").scrollIntoView({behavior:"smooth"})')).classes('nav-link')
                ui.button('App', on_click=lambda: ui.run_javascript('document.getElementById("app-showcase").scrollIntoView({behavior:"smooth"})')).classes('nav-link')
                ui.button('Como Funciona', on_click=lambda: ui.run_javascript('document.getElementById("how-section").scrollIntoView({behavior:"smooth"})')).classes('nav-link')
                ui.button('Planos', on_click=lambda: ui.run_javascript('document.getElementById("pricing-section").scrollIntoView({behavior:"smooth"})')).classes('nav-link')
                ui.button('Entrar', on_click=lambda: ui.navigate.to('/login')).classes('btn-secondary')
                ui.button('Começar Grátis', on_click=lambda: ui.navigate.to('/criar-conta')).classes('btn-primary')
            ui.button('☰').classes('mobile-menu-btn')
    
    # ========== HERO ==========
    with ui.element('div').classes('hero'):
        with ui.element('div').classes('container-lg'):
            with ui.element('div').classes('hero-grid'):
                with ui.element('div').classes('hero-content'):
                    with ui.element('div').classes('hero-badge'):
                        ui.element('div').classes('hero-badge-dot')
                        ui.label('Consultor com 30+ alertas inteligentes')
                    ui.html('<h1 class="hero-title">Domine suas finanças com <span>inteligência</span></h1>')
                    ui.label('Controle total dos seus cartões de crédito, gastos organizados e alertas personalizados.').classes('hero-description')
                    with ui.element('div').classes('hero-actions'):
                        ui.button('🚀 Começar Agora', on_click=lambda: ui.navigate.to('/criar-conta')).classes('hero-cta')
                        ui.button('Ver Demonstração →', on_click=lambda: ui.navigate.to('/login')).classes('hero-demo')
                    with ui.element('div').classes('hero-trust'):
                        ui.label('✓ Grátis para sempre')
                        ui.label('✓ Sem cartão de crédito')
                        ui.label('✓ 2 minutos para começar')
                with ui.element('div').classes('hero-image-wrapper'):
                    ui.html(f'<img src="{PRINT_DASHBOARD}" alt="Dashboard" class="hero-image">')
    
    # ========== LOGO SHOWCASE ==========
    with ui.element('div').classes('logo-showcase'):
        ui.label('Conheça o Cartometro').classes('logo-showcase-label')
        ui.html(f'<img src="{LOGO_FULL_COLOR}" alt="Cartometro" class="logo-showcase-img">')
    
    # ========== FEATURES ==========
    with ui.element('div').classes('features').props('id=features-section'):
        with ui.element('div').classes('container-lg'):
            with ui.element('div').classes('section-header'):
                ui.label('Funcionalidades').classes('section-badge')
                ui.label('Tudo que você precisa').classes('section-title')
                ui.label('Ferramentas completas para controle financeiro.').classes('section-description')
            with ui.element('div').classes('features-grid'):
                for icon, color, title, desc in [
                    ('📊', '#3b82f6', 'Dashboard Inteligente', 'KPIs em tempo real'),
                    ('💳', '#7c3aed', 'Múltiplos Cartões', 'Gestão individual'),
                    ('🤖', '#10b981', 'Consultor Financeiro', '30+ alertas'),
                    ('📅', '#f59e0b', 'Ciclo de Fatura', 'Acompanhamento real'),
                    ('🔁', '#ec4899', 'Gastos Recorrentes', 'Assinaturas automáticas'),
                    ('🎯', '#6366f1', 'Metas e Limites', 'Orçamentos por categoria'),
                ]:
                    with ui.element('div').classes('feature-card'):
                        ui.label(icon).classes('feature-icon').style(f'background: {color}15;')
                        ui.label(title).classes('feature-title')
                        ui.label(desc).classes('feature-description')
    
    # ========== APP SHOWCASE ==========
    with ui.element('div').classes('app-showcase').props('id=app-showcase'):
        with ui.element('div').classes('container-lg'):
            with ui.element('div').classes('section-header'):
                ui.label('Conheça o App').classes('section-badge')
                ui.label('Veja como funciona').classes('section-title')
            with ui.element('div').classes('showcase-grid'):
                for img, title, desc in [
                    (PRINT_DASHBOARD, 'Dashboard Completo', 'Visão geral dos seus cartões e gastos.'),
                    (PRINT_LANCAMENTOS, 'Lançamentos', 'Registre compras em segundos.'),
                    (PRINT_CARTOES, 'Gestão de Cartões', 'Múltiplos cartões com limites.'),
                    (PRINT_RELATORIOS, 'Relatórios', 'Análises inteligentes.'),
                ]:
                    with ui.element('div').classes('showcase-item'):
                        ui.html(f'<img src="{img}" alt="{title}" class="showcase-image">')
                        ui.label(title).classes('showcase-title')
                        ui.label(desc).classes('showcase-description')
    
    # ========== HOW IT WORKS ==========
    with ui.element('div').classes('how-it-works').props('id=how-section'):
        with ui.element('div').classes('container-lg'):
            with ui.element('div').classes('section-header'):
                ui.label('Como Funciona').classes('section-badge')
                ui.label('Comece em minutos').classes('section-title')
            with ui.element('div').classes('how-grid'):
                with ui.element('div').classes('how-steps'):
                    for num, title, desc in [
                        ('01', 'Crie sua conta', 'Cadastro rápido, sem cartão.'),
                        ('02', 'Adicione cartões', 'Com limites e vencimentos.'),
                        ('03', 'Registre gastos', 'Manual ou importação.'),
                        ('04', 'Receba insights', 'Alertas personalizados.'),
                    ]:
                        with ui.element('div').classes('how-step'):
                            ui.label(num).classes('step-number')
                            with ui.element('div').classes('step-content'):
                                ui.label(title).style('font-size:18px;font-weight:700;color:#0f172a;margin-bottom:4px;')
                                ui.label(desc).style('font-size:14px;color:#64748b;line-height:1.6;')
                with ui.element('div'):
                    ui.html(f'<img src="{PRINT_DASHBOARD}" alt="Como funciona" class="how-image">')
    
    # ========== PRICING ==========
    with ui.element('div').classes('pricing').props('id=pricing-section'):
        with ui.element('div').classes('container-lg'):
            with ui.element('div').classes('section-header'):
                ui.label('Planos').classes('section-badge')
                ui.label('Simples e transparente').classes('section-title')
            with ui.element('div').classes('pricing-grid'):
                with ui.element('div').classes('plan-card'):
                    with ui.element('div').classes('plan-header'):
                        ui.label('🆓 Gratuito').classes('plan-name')
                        ui.label('R$ 0').classes('plan-price')
                        ui.label('para sempre').classes('plan-period')
                    ui.element('div').classes('plan-divider')
                    with ui.element('div').classes('plan-features'):
                        for f in ['20 lançamentos/mês', '1 cartão', 'Modo Unificado', 'Consultor básico', 'Dashboard', 'Exportação']:
                            ui.label(f'✓ {f}').classes('plan-feature')
                    ui.button('Começar Grátis', on_click=lambda: ui.navigate.to('/criar-conta')).classes('plan-btn secondary')
                
                with ui.element('div').classes('plan-card featured'):
                    ui.label('MAIS POPULAR').classes('plan-badge')
                    with ui.element('div').classes('plan-header'):
                        ui.label('💎 Premium').classes('plan-name')
                        ui.label('R$ 4,99').classes('plan-price')
                        ui.label('/mês').classes('plan-period')
                    ui.element('div').classes('plan-divider')
                    with ui.element('div').classes('plan-features'):
                        for f in ['Lançamentos ilimitados', 'Múltiplos cartões', 'Modo Individual', 'Consultor Premium', 'Relatórios avançados', 'Suporte prioritário']:
                            ui.label(f'✓ {f}').classes('plan-feature')
                    ui.button('Assinar Premium', on_click=lambda: ui.navigate.to('/criar-conta')).classes('plan-btn primary')
    
    # ========== CTA ==========
    with ui.element('div').classes('cta'):
        with ui.element('div').classes('container-lg'):
            with ui.element('div').classes('cta-content'):
                ui.label('Pronto para controlar suas finanças?').classes('cta-title')
                ui.label('Junte-se a milhares de pessoas que já transformaram sua relação com o dinheiro.').classes('cta-description')
                ui.button('🚀 Criar Conta Gratuita', on_click=lambda: ui.navigate.to('/criar-conta')).classes('cta-btn')
    
    # ========== FOOTER ==========
    with ui.element('div').classes('footer'):
        with ui.element('div').classes('container-lg'):
            with ui.element('div').classes('footer-grid'):
                with ui.element('div').classes('footer-brand'):
                    ui.html(f'<img src="{LOGO_BRANCA}" alt="Cartometro" class="footer-brand-img">')
                    ui.label('Controle Inteligente do seu Crédito.')
                for title, links in [
                    ('Produto', [('Funcionalidades', 'features-section'), ('App', 'app-showcase'), ('Como Funciona', 'how-section'), ('Planos', 'pricing-section')]),
                    ('Suporte', ['Central de Ajuda', 'suporte@cartometro.app', 'FAQ']),
                    ('Legal', ['Termos de Uso', 'Privacidade']),
                ]:
                    with ui.element('div').classes('footer-col'):
                        ui.label(title)
                        for link in links:
                            if isinstance(link, tuple):
                                ui.label(link[0]).on('click', lambda sid=link[1]: ui.run_javascript(f'document.getElementById("{sid}").scrollIntoView({{behavior:"smooth"}})'))
                            else:
                                ui.label(link)
            with ui.element('div').classes('footer-bottom'):
                ui.label('© 2025 Cartometro. Todos os direitos reservados.').classes('footer-copyright')


# ============================================================
# TELA DE LOGIN
# ============================================================
@ui.page('/login')
def login():
    cor = config_service.get_primary_color()
    cor_escura = config_service.get_primary_dark()
    
    beneficios = [
        ("📊", "Dashboard inteligente com KPIs em tempo real"),
        ("🤖", "Consultor financeiro com 30+ alertas"),
        ("💳", "Controle total de múltiplos cartões"),
        ("🎯", "Metas e orçamentos personalizados"),
        ("🔔", "Alertas antes de problemas acontecerem"),
    ]
    
    ui.add_head_html(f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
    <link rel="icon" type="image/x-icon" href="{FAVICON}">
    <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    html, body {{ height: 100%; width: 100%; overflow: hidden; }}
    body {{ font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }}
    .login-page {{ display: flex; height: 100vh; width: 100vw; }}
    
    .login-brand {{
        flex: 1;
        background: linear-gradient(160deg, {cor_escura} 0%, {cor} 60%, {cor}cc 100%);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        padding: 60px;
        position: relative;
        overflow: hidden;
    }}
    
    .login-brand::before {{
        content: '';
        position: absolute;
        width: 800px;
        height: 800px;
        border-radius: 50%;
        border: 2px solid rgba(255, 255, 255, 0.05);
        top: -250px;
        right: -250px;
    }}
    
    .login-brand-content {{
        position: relative;
        z-index: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        max-width: 500px;
    }}
    
    .login-brand-logo {{ width: 640px; height: auto; margin-bottom: 48px; }}
    .login-brand-benefits {{ text-align: left; width: 100%; }}
    .login-brand-title {{ font-size: 26px; font-weight: 800; color: white; margin-bottom: 10px; text-align: center; }}
    .login-brand-subtitle {{ font-size: 14px; color: rgba(255, 255, 255, 0.7); margin-bottom: 40px; line-height: 1.6; text-align: center; }}
    
    .benefit-item {{ display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }}
    .benefit-icon {{ width: 36px; height: 36px; background: rgba(255, 255, 255, 0.12); border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0; }}
    .benefit-text {{ font-size: 13px; font-weight: 500; color: white; }}
    
    .login-form-side {{
        width: 520px;
        flex-shrink: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        background: white;
        padding: 48px;
        position: relative;
    }}
    
    .login-form-container {{ width: 100%; max-width: 380px; }}
    .login-logo-icon {{ width: 180px; height: auto; margin: 0 auto 20px; display: block; }}
    .login-wordmark {{ width: 160px; height: auto; margin: 0 auto 8px; display: block; }}
    .login-title {{ font-size: 26px; font-weight: 800; color: #0f172a; margin-bottom: 4px; text-align: center; }}
    .login-subtitle {{ font-size: 13px; color: #94a3b8; text-align: center; margin-bottom: 32px; }}
    
    .back-button {{
        position: absolute;
        top: 20px;
        left: 20px;
        background: white;
        border: none;
        padding: 10px 16px;
        border-radius: 8px;
        font-size: 12px;
        color: #64748b;
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        transition: all 0.2s;
        font-family: inherit;
        z-index: 10;
    }}
    
    .back-button:hover {{ color: #0f172a; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12); }}
    .field-wrapper {{ margin-bottom: 16px; }}
    .field-label {{ font-size: 13px; font-weight: 600; color: #475569; margin-bottom: 6px; display: block; }}
    
    .error-message {{
        display: none;
        font-size: 13px;
        color: #ef4444;
        background: #fef2f2;
        border-left: 3px solid #ef4444;
        padding: 12px 16px;
        border-radius: 8px;
        margin-bottom: 16px;
    }}
    
    .error-message.show {{ display: block; }}
    
    .login-btn {{
        width: 100%;
        height: 48px;
        background: {cor};
        color: white;
        border: none;
        border-radius: 12px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        font-family: inherit;
        transition: all 0.2s;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
        margin-top: 8px;
    }}
    
    .login-btn:hover {{ background: {cor_escura}; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15); transform: translateY(-1px); }}
    
    .demo-section {{ margin-top: 28px; padding-top: 24px; border-top: 1px solid #f1f5f9; }}
    .demo-label {{ font-size: 11px; font-weight: 700; color: #cbd5e1; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; text-align: center; }}
    
    .demo-btn {{
        width: 100%;
        padding: 12px;
        background: #f5f3ff;
        color: #7c3aed;
        border: 1px solid #e9d5ff;
        border-radius: 10px;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
        font-family: inherit;
        transition: all 0.2s;
        text-align: center;
    }}
    
    .demo-btn:hover {{ background: #ede9fe; border-color: #c4b5fd; }}
    
    .register-link {{ text-align: center; margin-top: 24px; font-size: 13px; color: #94a3b8; }}
    .register-link span {{ color: #7c3aed; font-weight: 600; cursor: pointer; }}
    .register-link span:hover {{ text-decoration: underline; }}
    
    .q-field--outlined .q-field__control {{ border-radius: 10px !important; height: 48px !important; background: #fafafa !important; }}
    .q-field--outlined.q-field--focused .q-field__control {{ border-color: {cor} !important; box-shadow: 0 0 0 3px {cor}15 !important; }}
    
    @media (max-width: 1024px) {{
        .login-brand {{ display: none; }}
        .login-form-side {{ width: 100%; padding: 0; display: flex; flex-direction: column; align-items: stretch; justify-content: flex-start; overflow-y: auto; }}
        .login-mobile-header {{ display: flex !important; flex-direction: column; align-items: center; justify-content: center; background: linear-gradient(160deg, {cor_escura} 0%, {cor} 100%); padding: 48px 24px 56px; position: relative; }}
        .login-mobile-header::after {{ content: ''; position: absolute; bottom: -24px; left: 0; right: 0; height: 48px; background: white; border-radius: 28px 28px 0 0; }}
        .login-mobile-logo {{ width: 120px; height: auto; margin-bottom: 8px; }}
        .login-form-container {{ position: relative; z-index: 1; padding: 20px 24px 40px; width: 100%; max-width: 420px; margin: 0 auto; }}
        .login-logo-icon {{ display: none !important; }}
        .back-button {{ position: absolute; top: 16px; right: 16px; left: auto; background: rgba(255, 255, 255, 0.2); color: white; backdrop-filter: blur(10px); box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1); border-radius: 8px; padding: 8px 14px; font-size: 12px; font-weight: 600; z-index: 10; }}
        .back-button:hover {{ background: rgba(255, 255, 255, 0.3); color: white; }}
    }}
    </style>
    """)
    
    def fazer_login():
        email = email_input.value.strip() if email_input.value else ''
        senha = senha_input.value or ''
        
        if not email or not senha:
            error_label.classes('error-message show')
            error_label.set_text('⚠️ Preencha todos os campos.')
            return
        
        usuario = autenticar_usuario(email, senha)
        
        if usuario:
            global usuario_atual
            usuario_atual = usuario
            if email == 'demo':
                resetar_dados_demo(email)
            set_usuario_logado(email)
            ui.notify(f'✅ Bem-vindo, {usuario["nome"]}!', type='positive', position='top')
            ui.navigate.to('/app')
        else:
            error_label.classes('error-message show')
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
            ui.button('← Voltar', on_click=lambda: ui.navigate.to('/')).props('no-caps').classes('back-button')
            
            with ui.element('div').classes('login-form-container'):
                ui.html(f'<img src="{LOGO}" alt="Cartometro" class="login-logo-icon">')
                ui.html(f'<img src="{WORDMARK}" alt="Cartometro" class="login-wordmark">')
                ui.label('Bem-vindo de volta').classes('login-title')
                ui.label('Entre para continuar').classes('login-subtitle')
                
                with ui.element('div').classes('field-wrapper'):
                    ui.label('Email').classes('field-label')
                    email_input = ui.input(placeholder='seu@email.com').props('outlined dense').classes('w-full')
                with ui.element('div').classes('field-wrapper'):
                    ui.label('Senha').classes('field-label')
                    senha_input = ui.input(placeholder='••••••••', password=True, password_toggle_button=True).props('outlined dense').classes('w-full')
                
                error_label = ui.label('').classes('error-message')
                ui.button('Entrar', on_click=fazer_login).props('no-caps').classes('login-btn')
                
                with ui.element('div').classes('demo-section'):
                    ui.label('Acesso rápido').classes('demo-label')
                    ui.button('👑 Demo: demo / demo', on_click=preencher_demo).classes('demo-btn')
                
                with ui.element('div').classes('register-link'):
                    ui.label('Não tem conta? ').style('display: inline;')
                    ui.label('Criar conta gratuita').style('display: inline;').on('click', lambda: ui.navigate.to('/criar-conta'))


# ============================================================
# TELA DE CADASTRO
# ============================================================
@ui.page('/criar-conta')
def criar_conta():
    ui.add_head_html(f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="icon" type="image/x-icon" href="{FAVICON}">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f8fafc; min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 24px; }}
        .register-container {{ background: white; border-radius: 20px; padding: 40px; width: 100%; max-width: 460px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }}
        .register-logo {{ width: 140px; height: auto; margin: 0 auto 24px; display: block; }}
        .register-title {{ font-size: 24px; font-weight: 800; color: #0f172a; text-align: center; margin-bottom: 4px; }}
        .register-subtitle {{ font-size: 14px; color: #94a3b8; text-align: center; margin-bottom: 32px; }}
        .plan-selector {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 24px; }}
        .plan-option {{ border: 2px solid #e2e8f0; border-radius: 12px; padding: 16px; text-align: center; cursor: pointer; transition: all 0.2s; background: white; }}
        .plan-option.selected {{ border-color: #7c3aed; background: #faf5ff; box-shadow: 0 0 0 3px rgba(124,58,237,0.1); }}
        .plan-option-icon {{ font-size: 28px; margin-bottom: 8px; }}
        .plan-option-name {{ font-size: 14px; font-weight: 700; color: #0f172a; margin-bottom: 4px; }}
        .plan-option-price {{ font-size: 20px; font-weight: 800; color: #7c3aed; }}
        .plan-option-period {{ font-size: 11px; color: #94a3b8; }}
        .form-group {{ margin-bottom: 16px; }}
        .form-label {{ font-size: 13px; font-weight: 600; color: #475569; margin-bottom: 6px; display: block; }}
        .q-field--outlined .q-field__control {{ border-radius: 10px !important; height: 48px !important; background: #fafafa !important; }}
        .register-btn {{ width: 100%; height: 48px; background: #7c3aed; color: white; border: none; border-radius: 12px; font-size: 16px; font-weight: 600; cursor: pointer; font-family: inherit; transition: all 0.2s; margin-top: 8px; }}
        .register-btn:hover {{ background: #6d28d9; }}
        .login-link {{ text-align: center; margin-top: 20px; font-size: 13px; color: #94a3b8; }}
        .login-link span {{ color: #7c3aed; font-weight: 600; cursor: pointer; }}
        .login-link span:hover {{ text-decoration: underline; }}
        .error-msg {{ background: #fef2f2; border-left: 3px solid #ef4444; color: #ef4444; padding: 12px 16px; border-radius: 8px; font-size: 13px; margin-bottom: 16px; display: none; }}
        .error-msg.show {{ display: block; }}
    </style>
    """)
    
    plano_selecionado = {"plano": "gratuito"}
    planos_refs = {}
    
    with ui.element('div').classes('register-container'):
        ui.html(f'<img src="{WORDMARK}" alt="Cartometro" class="register-logo">')
        ui.label('Criar sua Conta').classes('register-title')
        ui.label('Comece grátis, faça upgrade quando quiser').classes('register-subtitle')
        
        with ui.element('div').classes('plan-selector'):
            plano_free = ui.element('div').classes('plan-option selected')
            with plano_free:
                ui.label('🆓').classes('plan-option-icon')
                ui.label('Gratuito').classes('plan-option-name')
                ui.label('R$ 0').classes('plan-option-price')
                ui.label('para sempre').classes('plan-option-period')
            plano_free.on('click', lambda: selecionar_plano('gratuito'))
            planos_refs['gratuito'] = plano_free
            
            plano_premium = ui.element('div').classes('plan-option')
            with plano_premium:
                ui.label('💎').classes('plan-option-icon')
                ui.label('Premium').classes('plan-option-name')
                ui.label('R$ 4,99').classes('plan-option-price')
                ui.label('/mês').classes('plan-option-period')
            plano_premium.on('click', lambda: selecionar_plano('premium'))
            planos_refs['premium'] = plano_premium
        
        def selecionar_plano(plano):
            plano_selecionado["plano"] = plano
            for nome, ref in planos_refs.items():
                ref.classes('plan-option selected') if nome == plano else ref.classes(remove='selected')
        
        with ui.element('div').classes('form-group'):
            ui.label('Nome completo').classes('form-label')
            nome_input = ui.input(placeholder='Seu nome completo').props('outlined dense').classes('w-full')
        with ui.element('div').classes('form-group'):
            ui.label('Email').classes('form-label')
            email_input = ui.input(placeholder='seu@email.com').props('outlined dense').classes('w-full')
        with ui.element('div').classes('form-group'):
            ui.label('Senha').classes('form-label')
            senha_input = ui.input(placeholder='Mínimo 4 caracteres', password=True, password_toggle_button=True).props('outlined dense').classes('w-full')
        with ui.element('div').classes('form-group'):
            ui.label('Confirmar Senha').classes('form-label')
            confirmar_input = ui.input(placeholder='Repita a senha', password=True, password_toggle_button=True).props('outlined dense').classes('w-full')
        
        erro_label = ui.label('').classes('error-msg')
        
        def cadastrar():
            nome = nome_input.value.strip() if nome_input.value else ''
            email = email_input.value.strip() if email_input.value else ''
            senha = senha_input.value or ''
            confirmar = confirmar_input.value or ''
            erro_label.classes(remove='show')
            
            if not nome or not email or not senha:
                erro_label.classes('error-msg show'); erro_label.set_text('⚠️ Preencha todos os campos'); return
            if senha != confirmar:
                erro_label.classes('error-msg show'); erro_label.set_text('⚠️ Senhas não conferem'); return
            if len(senha) < 4:
                erro_label.classes('error-msg show'); erro_label.set_text('⚠️ Senha deve ter pelo menos 4 caracteres'); return
            
            sucesso, msg, usuario = criar_usuario(nome, email, senha, plano_selecionado["plano"])
            if sucesso:
                plano_nome = 'Premium' if plano_selecionado["plano"] == 'premium' else 'Gratuito'
                ui.notify(f'✅ Conta {plano_nome} criada! Redirecionando...', type='positive', position='top', timeout=3000)
                ui.timer(1.5, lambda: ui.navigate.to('/login'), once=True)
            else:
                erro_label.classes('error-msg show'); erro_label.set_text(f'❌ {msg}')
        
        ui.button('Criar Conta', on_click=cadastrar).props('no-caps').classes('register-btn')
        with ui.element('div').classes('login-link'):
            ui.label('Já tem conta? ').style('display: inline;')
            ui.label('Fazer login').style('display: inline;').on('click', lambda: ui.navigate.to('/login'))


# ============================================================
# TELA PRINCIPAL (PÓS-LOGIN)
# ============================================================
@ui.page('/app')
def app():
    global usuario_atual, container_principal
    if not usuario_atual:
        ui.navigate.to('/login')
        return
    from telas.lancamentos import tela_lancamentos
    container_principal = ui.element('div').classes('w-full h-screen')
    tela_lancamentos(container_principal)


# ============================================================
# INICIALIZAÇÃO
# ============================================================
inicializar()
admin.inicializar_admin()
criar_usuarios_padrao()
set_usuario_logado(None)

PORT = int(os.environ.get('PORT', 8080))

if IS_PRODUCTION:
    print(f"🚀 Iniciando em PRODUÇÃO na porta {PORT}")
    ui.run(
        title="Cartometro",
        favicon=FAVICON,
        reload=False,
        show=False,
        host='0.0.0.0',
        port=PORT,
        storage_secret='cartometro-2024-secret'
    )
else:
    print(f"💻 Iniciando em DESENVOLVIMENTO na porta {PORT}")
    print("👤 APP: demo / demo")
    print("👤 APP: admin@app.com / admin123")
    print("👤 APP: teste@local.com / teste123")
    print("🔐 ADMIN: admin@cartometro.com / Cartometro@2024")
    ui.run(
        title="Cartometro [DEV]",
        favicon=FAVICON,
        reload=True,
        show=True,
        host='127.0.0.1',
        port=PORT,
        storage_secret='cartometro-2024-secret'
    )