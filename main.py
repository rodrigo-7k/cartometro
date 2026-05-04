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
    carregar, atualizar_config
)
from config_service import config_service
from auth_service import get_usuario_logado
import admin
import os

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

# Imagens placeholder para prints do app
PRINT_DASHBOARD  = "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=800&q=80"
PRINT_CARTOES    = "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800&q=80"
PRINT_LANCAMENTOS = "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&q=80"
PRINT_RELATORIOS = "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&q=80"

# ============================================================
# VARIÁVEIS GLOBAIS
# ============================================================
usuario_atual = None
container_principal = None


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
    
    body {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background: #ffffff;
        color: #0f172a;
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
    }}
    
    /* ========== NAVBAR ========== */
    .navbar {{
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-bottom: 1px solid rgba(0, 0, 0, 0.06);
    }}
    
    .navbar.scrolled {{
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.08);
    }}
    
    .navbar-container {{
        max-width: 1280px;
        width: 90%;
        margin: 0 auto;
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: 72px;
    }}
    
    .navbar-logo {{
        height: 40px;
        width: auto;
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
    
    .nav-link:hover {{
        color: #7c3aed;
        background: #f5f3ff;
    }}
    
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
    
    .btn-secondary:hover {{
        background: #f5f3ff;
        border-color: #7c3aed;
    }}
    
    .mobile-menu-btn {{
        display: none;
        background: none;
        border: none;
        font-size: 24px;
        cursor: pointer;
        color: #475569;
        padding: 8px;
    }}
    
    /* ========== HERO ========== */
    .hero {{
        padding: 120px 0 80px;
        background: linear-gradient(135deg, #faf5ff 0%, #f0f4ff 50%, #ffffff 100%);
        position: relative;
        overflow: hidden;
    }}
    
    .hero-container {{
        max-width: 1280px;
        width: 90%;
        margin: 0 auto;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 64px;
        align-items: center;
        position: relative;
        z-index: 1;
    }}
    
    .hero-content {{
        max-width: 560px;
    }}
    
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
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
    }}
    
    .hero-badge-dot {{
        width: 6px;
        height: 6px;
        background: #7c3aed;
        border-radius: 50%;
    }}
    
    .hero-title {{
        font-size: clamp(40px, 4.5vw, 60px);
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
    
    .hero-demo:hover {{
        border-color: #c4b5fd;
        color: #7c3aed !important;
    }}
    
    .hero-trust {{
        display: flex;
        align-items: center;
        gap: 16px;
        color: #94a3b8;
        font-size: 13px;
        flex-wrap: wrap;
    }}
    
    .hero-trust-item {{
        display: flex;
        align-items: center;
        gap: 6px;
    }}
    
    .hero-image {{
        position: relative;
        display: flex;
        justify-content: center;
        align-items: center;
    }}
    
    .hero-image-main {{
        width: 100%;
        max-width: 520px;
        border-radius: 16px;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25);
    }}
    
    /* ========== LOGO SECTION AFTER HERO ========== */
    .logo-showcase {{
        padding: 60px 0;
        background: white;
        text-align: center;
    }}
    
    .logo-showcase img {{
        height: 60px;
        width: auto;
        opacity: 0.3;
    }}
    
    /* ========== FEATURES ========== */
    .features {{
        padding: 100px 0;
        background: white;
    }}
    
    .features-container {{
        max-width: 1280px;
        width: 90%;
        margin: 0 auto;
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
    
    .feature-title {{
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 8px;
    }}
    
    .feature-description {{
        font-size: 14px;
        color: #64748b;
        line-height: 1.6;
    }}
    
    /* ========== APP SHOWCASE ========== */
    .app-showcase {{
        padding: 100px 0;
        background: #fafafa;
    }}
    
    .app-showcase-container {{
        max-width: 1280px;
        width: 90%;
        margin: 0 auto;
    }}
    
    .showcase-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 60px;
        margin-top: 64px;
    }}
    
    .showcase-item {{
        display: flex;
        flex-direction: column;
    }}
    
    .showcase-image {{
        width: 100%;
        border-radius: 16px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        margin-bottom: 24px;
    }}
    
    .showcase-title {{
        font-size: 20px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 8px;
    }}
    
    .showcase-description {{
        font-size: 14px;
        color: #64748b;
        line-height: 1.6;
    }}
    
    /* ========== HOW IT WORKS ========== */
    .how-it-works {{
        padding: 100px 0;
        background: white;
    }}
    
    .how-container {{
        max-width: 1280px;
        width: 90%;
        margin: 0 auto;
    }}
    
    .how-grid {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 80px;
        align-items: center;
        margin-top: 64px;
    }}
    
    .how-steps {{
        display: flex;
        flex-direction: column;
        gap: 32px;
    }}
    
    .how-step {{
        display: flex;
        gap: 20px;
    }}
    
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
    
    .step-content h3 {{
        font-size: 18px;
        font-weight: 700;
        color: #0f172a;
        margin-bottom: 4px;
    }}
    
    .step-content p {{
        font-size: 14px;
        color: #64748b;
        line-height: 1.6;
    }}
    
    .how-image img {{
        width: 100%;
        border-radius: 16px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
    }}
    
    /* ========== PRICING ========== */
    .pricing {{
        padding: 100px 0;
        background: #fafafa;
    }}
    
    .pricing-container {{
        max-width: 1280px;
        width: 90%;
        margin: 0 auto;
    }}
    
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
    
    .plan-card:hover {{
        border-color: #c4b5fd;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
    }}
    
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
    
    .plan-header {{
        text-align: center;
        margin-bottom: 32px;
    }}
    
    .plan-name {{
        font-size: 24px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 8px;
    }}
    
    .plan-price {{
        font-size: 56px;
        font-weight: 900;
        color: #7c3aed;
        line-height: 1;
        margin-bottom: 4px;
    }}
    
    .plan-period {{
        font-size: 14px;
        color: #94a3b8;
    }}
    
    .plan-divider {{
        height: 1px;
        background: #f1f5f9;
        margin-bottom: 24px;
    }}
    
    .plan-features {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
        margin-bottom: 32px;
    }}
    
    .plan-feature {{
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 13px;
        color: #475569;
    }}
    
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
    
    .plan-btn.primary:hover {{
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.4);
        transform: translateY(-2px);
    }}
    
    .plan-btn.secondary {{
        background: transparent;
        color: #7c3aed;
        border: 2px solid #e9d5ff;
    }}
    
    .plan-btn.secondary:hover {{
        background: #f5f3ff;
        border-color: #7c3aed;
    }}
    
    /* ========== CTA ========== */
    .cta {{
        padding: 100px 0;
        background: linear-gradient(135deg, #6d28d9, #4f46e5);
        position: relative;
        overflow: hidden;
    }}
    
    .cta-container {{
        max-width: 1280px;
        width: 90%;
        margin: 0 auto;
        text-align: center;
        position: relative;
        z-index: 1;
    }}
    
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
    
    .cta-btn:hover {{
        transform: translateY(-2px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.3);
    }}
    
    /* ========== FOOTER ========== */
    .footer {{
        background: #0f172a;
        padding: 48px 0 32px;
        color: #94a3b8;
    }}
    
    .footer-container {{
        max-width: 1280px;
        width: 90%;
        margin: 0 auto;
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 1fr;
        gap: 48px;
        padding-bottom: 32px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    }}
    
    .footer-brand img {{
        height: 56px;
        width: auto;
        margin-bottom: 12px;
        display: block;
    }}
    
    .footer-brand p {{
        font-size: 13px;
        line-height: 1.7;
        color: #64748b;
        max-width: 260px;
    }}
    
    .footer-col h4 {{
        font-size: 13px;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 16px;
        letter-spacing: 0.3px;
    }}
    
    .footer-col a {{
        display: block;
        font-size: 13px;
        color: #64748b;
        margin-bottom: 10px;
        text-decoration: none;
        transition: color 0.2s;
        cursor: pointer;
    }}
    
    .footer-col a:hover {{
        color: #e2e8f0;
    }}
    
    .footer-bottom {{
        max-width: 1280px;
        width: 90%;
        margin: 24px auto 0;
        text-align: center;
    }}
    
    .footer-copyright {{
        font-size: 13px;
        color: #475569;
    }}
    
    /* ========== RESPONSIVO ========== */
    @media (max-width: 1024px) {{
        .hero-container {{
            grid-template-columns: 1fr;
            gap: 48px;
        }}
        
        .hero-image {{
            order: -1;
            max-width: 500px;
            margin: 0 auto;
        }}
        
        .features-grid {{
            grid-template-columns: repeat(2, 1fr);
        }}
        
        .showcase-grid {{
            grid-template-columns: 1fr;
            gap: 48px;
        }}
        
        .how-grid {{
            grid-template-columns: 1fr;
            gap: 48px;
        }}
        
        .how-image {{
            order: -1;
        }}
        
        .pricing-grid {{
            grid-template-columns: 1fr;
            max-width: 500px;
        }}
        
        .footer-container {{
            grid-template-columns: 1fr 1fr;
            gap: 32px;
        }}
    }}
    
    @media (max-width: 768px) {{
        .navbar-links {{
            display: none;
        }}
        
        .mobile-menu-btn {{
            display: block;
        }}
        
        .navbar-container,
        .hero-container,
        .features-container,
        .app-showcase-container,
        .how-container,
        .pricing-container,
        .cta-container,
        .footer-container,
        .footer-bottom {{
            width: 94%;
        }}
        
        .hero {{
            padding: 100px 0 60px;
        }}
        
        .hero-image {{
            display: block !important;
        }}
        
        .hero-title {{
            font-size: 34px;
        }}
        
        .hero-description {{
            font-size: 16px;
        }}
        
        .features {{
            padding: 60px 0;
        }}
        
        .features-grid {{
            grid-template-columns: 1fr;
        }}
        
        .app-showcase {{
            padding: 60px 0;
        }}
        
        .how-it-works {{
            padding: 60px 0;
        }}
        
        .pricing {{
            padding: 60px 0;
        }}
        
        .cta {{
            padding: 60px 0;
        }}
        
        .plan-features {{
            grid-template-columns: 1fr;
        }}
        
        .footer-container {{
            grid-template-columns: 1fr;
            gap: 28px;
        }}
    }}
    
    @media (max-width: 480px) {{
        .hero-actions {{
            flex-direction: column;
        }}
        
        .plan-card {{
            padding: 32px 24px;
        }}
        
        .hero-title {{
            font-size: 30px;
        }}
    }}
    </style>
    
    <script>
    window.addEventListener('scroll', function() {{
        var nav = document.querySelector('.navbar');
        if(nav) {{
            if(window.scrollY > 20) {{
                nav.classList.add('scrolled');
            }} else {{
                nav.classList.remove('scrolled');
            }}
        }}
    }});
    </script>
    """)
    
    # ========== NAVBAR ==========
    with ui.element('nav').classes('navbar'):
        with ui.element('div').classes('navbar-container'):
            ui.image(LOGO_FULL_COLOR).classes('navbar-logo')
            
            with ui.element('div').classes('navbar-links'):
                ui.button('Funcionalidades', on_click=lambda: ui.run_javascript('document.getElementById("features-section").scrollIntoView({behavior:"smooth"})')).classes('nav-link')
                ui.button('App', on_click=lambda: ui.run_javascript('document.getElementById("app-showcase").scrollIntoView({behavior:"smooth"})')).classes('nav-link')
                ui.button('Como Funciona', on_click=lambda: ui.run_javascript('document.getElementById("how-section").scrollIntoView({behavior:"smooth"})')).classes('nav-link')
                ui.button('Planos', on_click=lambda: ui.run_javascript('document.getElementById("pricing-section").scrollIntoView({behavior:"smooth"})')).classes('nav-link')
                ui.button('Entrar', on_click=lambda: ui.navigate.to('/login')).classes('btn-secondary')
                ui.button('Começar Grátis', on_click=lambda: ui.navigate.to('/criar-conta')).classes('btn-primary')
            
            ui.button('☰').classes('mobile-menu-btn')
    
    # ========== HERO ==========
    with ui.element('section').classes('hero'):
        with ui.element('div').classes('hero-container'):
            with ui.element('div').classes('hero-content'):
                with ui.element('div').classes('hero-badge'):
                    ui.element('div').classes('hero-badge-dot')
                    ui.label('Consultor com 30+ alertas inteligentes')
                
                ui.html('<h1 class="hero-title">Domine suas finanças com <span>inteligência</span></h1>')
                ui.label('Controle total dos seus cartões de crédito, gastos organizados e alertas personalizados para você nunca perder o controle.').classes('hero-description')
                
                with ui.element('div').classes('hero-actions'):
                    ui.button('🚀 Começar Agora', on_click=lambda: ui.navigate.to('/criar-conta')).classes('hero-cta')
                    ui.button('Ver Demonstração →', on_click=lambda: ui.navigate.to('/login')).classes('hero-demo')
                
                with ui.element('div').classes('hero-trust'):
                    with ui.element('div').classes('hero-trust-item'):
                        ui.label('✓ Grátis para sempre')
                    with ui.element('div').classes('hero-trust-item'):
                        ui.label('✓ Sem cartão de crédito')
                    with ui.element('div').classes('hero-trust-item'):
                        ui.label('✓ 2 minutos para começar')
            
            with ui.element('div').classes('hero-image'):
                ui.image(PRINT_DASHBOARD).classes('hero-image-main')
    
    # ========== LOGO SHOWCASE ==========
    with ui.element('div').classes('logo-showcase'):
        ui.image(LOGO_FULL_COLOR).style('height: 60px; width: auto; opacity: 0.3; margin: 0 auto; display: block;')
    
    # ========== FEATURES ==========
    with ui.element('section').classes('features').props('id=features-section'):
        with ui.element('div').classes('features-container'):
            with ui.element('div').classes('section-header'):
                ui.label('Funcionalidades').classes('section-badge')
                ui.label('Tudo que você precisa em um só lugar').classes('section-title')
                ui.label('Ferramentas completas para controle financeiro, do básico ao avançado.').classes('section-description')
            
            with ui.element('div').classes('features-grid'):
                features = [
                    ('📊', '#3b82f6', 'Dashboard Inteligente', 'Visualize KPIs em tempo real: limite usado, gastos por categoria e tendências do mês.'),
                    ('💳', '#7c3aed', 'Múltiplos Cartões', 'Gerencie cada cartão individualmente ou de forma unificada, com limites e ciclos distintos.'),
                    ('🤖', '#10b981', 'Consultor Financeiro', '30+ alertas que analisam seus padrões de consumo antes que problemas aconteçam.'),
                    ('📅', '#f59e0b', 'Ciclo de Fatura', 'Acompanhe gastos pelo ciclo real da fatura ou pelo mês calendário.'),
                    ('🔁', '#ec4899', 'Gastos Recorrentes', 'Cadastre assinaturas e fixos que entram automaticamente todo mês.'),
                    ('🎯', '#6366f1', 'Metas e Limites', 'Defina orçamentos por categoria e receba alertas ao se aproximar do limite.'),
                ]
                
                for icon, color, title, description in features:
                    with ui.element('div').classes('feature-card'):
                        ui.label(icon).classes('feature-icon').style(f'background: {color}15;')
                        ui.label(title).classes('feature-title')
                        ui.label(description).classes('feature-description')
    
    # ========== APP SHOWCASE ==========
    with ui.element('section').classes('app-showcase').props('id=app-showcase'):
        with ui.element('div').classes('app-showcase-container'):
            with ui.element('div').classes('section-header'):
                ui.label('Conheça o App').classes('section-badge')
                ui.label('Veja como funciona na prática').classes('section-title')
                ui.label('Interface intuitiva e fácil de usar para você ter controle total.').classes('section-description')
            
            with ui.element('div').classes('showcase-grid'):
                # Print 1
                with ui.element('div').classes('showcase-item'):
                    ui.image(PRINT_DASHBOARD).classes('showcase-image')
                    ui.label('Dashboard Completo').classes('showcase-title')
                    ui.label('Visão geral de todos os seus cartões e gastos em um único lugar. Acompanhe limites, gastos do mês e tendências.').classes('showcase-description')
                
                # Print 2
                with ui.element('div').classes('showcase-item'):
                    ui.image(PRINT_LANCAMENTOS).classes('showcase-image')
                    ui.label('Lançamentos Simplificados').classes('showcase-title')
                    ui.label('Registre cada compra em segundos. Categorize gastos e acompanhe em tempo real o impacto no seu limite.').classes('showcase-description')
                
                # Print 3
                with ui.element('div').classes('showcase-item'):
                    ui.image(PRINT_CARTOES).classes('showcase-image')
                    ui.label('Gestão de Cartões').classes('showcase-title')
                    ui.label('Cadastre múltiplos cartões, configure limites e ciclos de fatura. Visualize cada um individualmente ou de forma unificada.').classes('showcase-description')
                
                # Print 4
                with ui.element('div').classes('showcase-item'):
                    ui.image(PRINT_RELATORIOS).classes('showcase-image')
                    ui.label('Relatórios e Insights').classes('showcase-title')
                    ui.label('Receba análises inteligentes dos seus gastos. O consultor premium identifica padrões e sugere economias.').classes('showcase-description')
    
    # ========== HOW IT WORKS ==========
    with ui.element('section').classes('how-it-works').props('id=how-section'):
        with ui.element('div').classes('how-container'):
            with ui.element('div').classes('section-header'):
                ui.label('Como Funciona').classes('section-badge')
                ui.label('Comece em minutos, sem complicação').classes('section-title')
                ui.label('Quatro passos simples para transformar sua relação com o dinheiro.').classes('section-description')
            
            with ui.element('div').classes('how-grid'):
                with ui.element('div').classes('how-steps'):
                    steps = [
                        ('01', 'Crie sua conta gratuita', 'Cadastro rápido em menos de 2 minutos, sem necessidade de cartão de crédito.'),
                        ('02', 'Adicione seus cartões', 'Cadastre seus cartões com limites e datas de vencimento da fatura.'),
                        ('03', 'Registre seus gastos', 'Lance compras manualmente ou importe seu extrato. Simples e rápido.'),
                        ('04', 'Receba insights inteligentes', 'O consultor analisa seus dados e envia alertas personalizados.'),
                    ]
                    
                    for number, title, description in steps:
                        with ui.element('div').classes('how-step'):
                            ui.label(number).classes('step-number')
                            with ui.element('div').classes('step-content'):
                                ui.label(title).style('font-size: 18px; font-weight: 700; color: #0f172a; margin-bottom: 4px;')
                                ui.label(description).style('font-size: 14px; color: #64748b; line-height: 1.6;')
                
                with ui.element('div').classes('how-image'):
                    ui.image(PRINT_DASHBOARD)
    
    # ========== PRICING ==========
    with ui.element('section').classes('pricing').props('id=pricing-section'):
        with ui.element('div').classes('pricing-container'):
            with ui.element('div').classes('section-header'):
                ui.label('Planos').classes('section-badge')
                ui.label('Simples e transparente').classes('section-title')
                ui.label('Sem taxas escondidas. Faça upgrade ou downgrade quando quiser.').classes('section-description')
            
            with ui.element('div').classes('pricing-grid'):
                # Free Plan
                with ui.element('div').classes('plan-card'):
                    with ui.element('div').classes('plan-header'):
                        ui.label('🆓 Gratuito').classes('plan-name')
                        ui.label('R$ 0').classes('plan-price')
                        ui.label('para sempre').classes('plan-period')
                    
                    ui.element('div').classes('plan-divider')
                    
                    with ui.element('div').classes('plan-features'):
                        for feature in ['20 lançamentos/mês', '1 cartão', 'Modo Unificado', 'Consultor básico', 'Dashboard completo', 'Exportação de dados']:
                            ui.label(f'✓ {feature}').classes('plan-feature')
                    
                    ui.button('Começar Grátis', on_click=lambda: ui.navigate.to('/criar-conta')).classes('plan-btn secondary')
                
                # Premium Plan
                with ui.element('div').classes('plan-card featured'):
                    ui.label('MAIS POPULAR').classes('plan-badge')
                    
                    with ui.element('div').classes('plan-header'):
                        ui.label('💎 Premium').classes('plan-name')
                        ui.label('R$ 4,99').classes('plan-price')
                        ui.label('/mês').classes('plan-period')
                    
                    ui.element('div').classes('plan-divider')
                    
                    with ui.element('div').classes('plan-features'):
                        for feature in ['Lançamentos ilimitados', 'Múltiplos cartões', 'Modo Individual', 'Consultor Premium (30+)', 'Relatórios avançados', 'Suporte prioritário']:
                            ui.label(f'✓ {feature}').classes('plan-feature')
                    
                    ui.button('Assinar Premium', on_click=lambda: ui.navigate.to('/criar-conta')).classes('plan-btn primary')
    
    # ========== CTA ==========
    with ui.element('section').classes('cta'):
        with ui.element('div').classes('cta-container'):
            ui.label('Pronto para controlar suas finanças?').classes('cta-title')
            ui.label('Junte-se a milhares de pessoas que já transformaram sua relação com o dinheiro usando o Cartometro.').classes('cta-description')
            ui.button('🚀 Criar Conta Gratuita', on_click=lambda: ui.navigate.to('/criar-conta')).classes('cta-btn')
    
    # ========== FOOTER ==========
    with ui.element('footer').classes('footer'):
        with ui.element('div').classes('footer-container'):
            with ui.element('div').classes('footer-brand'):
                ui.image(LOGO_BRANCA)
                ui.label('Controle Inteligente do seu Crédito. Simples, rápido e eficiente.')
            
            with ui.element('div').classes('footer-col'):
                ui.label('Produto')
                for link_text, section_id in [('Funcionalidades', 'features-section'), ('App', 'app-showcase'), ('Como Funciona', 'how-section'), ('Planos', 'pricing-section')]:
                    ui.label(link_text).on('click', lambda sid=section_id: ui.run_javascript(f'document.getElementById("{sid}").scrollIntoView({{behavior:"smooth"}})'))
            
            with ui.element('div').classes('footer-col'):
                ui.label('Suporte')
                for link_text in ['Central de Ajuda', 'suporte@cartometro.app', 'FAQ']:
                    ui.label(link_text)
            
            with ui.element('div').classes('footer-col'):
                ui.label('Legal')
                for link_text in ['Termos de Uso', 'Privacidade']:
                    ui.label(link_text)
        
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
    
    body {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        height: 100vh;
        overflow: hidden;
    }}
    
    .login-page {{
        display: flex;
        height: 100vh;
        width: 100%;
    }}
    
    /* LADO ESQUERDO - BRAND COM LOGO FULL BRANCA */
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
    
    .login-brand::after {{
        content: '';
        position: absolute;
        width: 600px;
        height: 600px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(255, 255, 255, 0.03) 0%, transparent 70%);
        bottom: -200px;
        left: -200px;
    }}
    
    .login-brand-content {{
        position: relative;
        z-index: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        max-width: 500px;
    }}
    
    .login-brand-logo {{
        width: 320px;
        height: auto;
        margin-bottom: 48px;
    }}
    
    .login-brand-benefits {{
        text-align: left;
        width: 100%;
    }}
    
    .login-brand-title {{
        font-size: 26px;
        font-weight: 800;
        color: white;
        margin-bottom: 10px;
        letter-spacing: -0.5px;
        text-align: center;
    }}
    
    .login-brand-subtitle {{
        font-size: 14px;
        color: rgba(255, 255, 255, 0.7);
        margin-bottom: 40px;
        line-height: 1.6;
        text-align: center;
    }}
    
    .benefit-item {{
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 16px;
        color: white;
    }}
    
    .benefit-icon {{
        width: 36px;
        height: 36px;
        background: rgba(255, 255, 255, 0.12);
        border-radius: 10px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        flex-shrink: 0;
    }}
    
    .benefit-text {{
        font-size: 13px;
        font-weight: 500;
        line-height: 1.4;
    }}
    
    /* LADO DIREITO - LOGIN FORM */
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
    
    .login-form-container {{
        width: 100%;
        max-width: 380px;
    }}
    
    .login-logo-icon {{
        width: 100px;
        height: auto;
        margin: 0 auto 16px;
        display: block;
    }}
    
    .login-wordmark {{
        width: 160px;
        height: auto;
        margin: 0 auto 8px;
        display: block;
    }}
    
    .login-title {{
        font-size: 26px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 4px;
        text-align: center;
        letter-spacing: -0.5px;
    }}
    
    .login-subtitle {{
        font-size: 13px;
        color: #94a3b8;
        text-align: center;
        margin-bottom: 32px;
    }}
    
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
    
    .back-button:hover {{
        color: #0f172a;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
    }}
    
    .field-wrapper {{
        margin-bottom: 16px;
    }}
    
    .field-label {{
        font-size: 13px;
        font-weight: 600;
        color: #475569;
        margin-bottom: 6px;
        display: block;
    }}
    
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
    
    .error-message.show {{
        display: block;
    }}
    
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
    
    .login-btn:hover {{
        background: {cor_escura};
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        transform: translateY(-1px);
    }}
    
    .demo-section {{
        margin-top: 28px;
        padding-top: 24px;
        border-top: 1px solid #f1f5f9;
    }}
    
    .demo-label {{
        font-size: 11px;
        font-weight: 700;
        color: #cbd5e1;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 10px;
        text-align: center;
    }}
    
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
    
    .demo-btn:hover {{
        background: #ede9fe;
        border-color: #c4b5fd;
    }}
    
    .register-link {{
        text-align: center;
        margin-top: 24px;
        font-size: 13px;
        color: #94a3b8;
    }}
    
    .register-link span {{
        color: #7c3aed;
        font-weight: 600;
        cursor: pointer;
    }}
    
    .register-link span:hover {{
        text-decoration: underline;
    }}
    
    /* Input styling */
    .q-field--outlined .q-field__control {{
        border-radius: 10px !important;
        height: 48px !important;
        background: #fafafa !important;
    }}
    
    .q-field--outlined.q-field--focused .q-field__control {{
        border-color: {cor} !important;
        box-shadow: 0 0 0 3px {cor}15 !important;
    }}
    
    @media (max-width: 1024px) {{
        .login-brand {{
            display: none;
        }}
        
        .login-form-side {{
            width: 100%;
            padding: 32px 24px;
        }}
        
        /* Mobile: mostrar gradiente no topo */
        .login-form-side::before {{
            display: block;
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 200px;
            background: linear-gradient(160deg, {cor_escura} 0%, {cor} 100%);
            z-index: 0;
        }}
        
        .login-form-container {{
            position: relative;
            z-index: 1;
            margin-top: 40px;
        }}
        
        .login-logo-icon {{
            width: 80px;
            filter: brightness(0) invert(1);
        }}
        
        .back-button {{
            top: 16px;
            left: 16px;
            background: rgba(255, 255, 255, 0.2);
            color: white;
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }}
        
        .back-button:hover {{
            background: rgba(255, 255, 255, 0.3);
            color: white;
        }}
    }}
    
    @media (max-width: 480px) {{
        .login-form-side {{
            padding: 20px 16px;
        }}
        
        .login-title {{
            font-size: 24px;
        }}
        
        .login-logo-icon {{
            width: 70px;
        }}
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
        senha_input.value = 'admin'
    
    # Construir a página
    with ui.element('div').classes('login-page'):
        # LADO ESQUERDO - Marca e Benefícios
        with ui.element('div').classes('login-brand'):
            with ui.element('div').classes('login-brand-content'):
                ui.image(LOGO_FULL_BRANCA).classes('login-brand-logo')
                
                with ui.element('div').classes('login-brand-benefits'):
                    ui.label('Controle inteligente do seu crédito').classes('login-brand-title')
                    ui.label('Tudo que você precisa para dominar suas finanças em um só lugar.').classes('login-brand-subtitle')
                    
                    for icon, text in beneficios:
                        with ui.element('div').classes('benefit-item'):
                            ui.label(icon).classes('benefit-icon')
                            ui.label(text).classes('benefit-text')
        
        # LADO DIREITO - Formulário
        with ui.element('div').classes('login-form-side'):
            # Botão Voltar
            ui.button('← Voltar', on_click=lambda: ui.navigate.to('/')).props('no-caps').classes('back-button')
            
            with ui.element('div').classes('login-form-container'):
                # Logo icon
                ui.image(LOGO).classes('login-logo-icon')
                
                # Wordmark
                ui.image(WORDMARK).classes('login-wordmark')
                
                ui.label('Bem-vindo de volta').classes('login-title')
                ui.label('Entre para continuar').classes('login-subtitle')
                
                # Campos
                with ui.element('div').classes('field-wrapper'):
                    ui.label('Email').classes('field-label')
                    email_input = ui.input(placeholder='seu@email.com').props('outlined dense').classes('w-full')
                
                with ui.element('div').classes('field-wrapper'):
                    ui.label('Senha').classes('field-label')
                    senha_input = ui.input(placeholder='••••••••', password=True, password_toggle_button=True).props('outlined dense').classes('w-full')
                
                # Mensagem de erro
                error_label = ui.label('').classes('error-message')
                
                # Botão de login
                ui.button('Entrar', on_click=fazer_login).props('no-caps').classes('login-btn')
                
                # Demo section
                with ui.element('div').classes('demo-section'):
                    ui.label('Acesso rápido').classes('demo-label')
                    ui.button('👑 Demo: demo / admin', on_click=preencher_demo).classes('demo-btn')
                
                # Register link
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
        body {{ 
            font-family: 'Inter', sans-serif; 
            background: #f8fafc; 
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 24px;
        }}
        .register-container {{
            background: white;
            border-radius: 20px;
            padding: 40px;
            width: 100%;
            max-width: 460px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }}
        .register-logo {{
            width: 140px;
            height: auto;
            margin: 0 auto 24px;
            display: block;
        }}
        .register-title {{
            font-size: 24px;
            font-weight: 800;
            color: #0f172a;
            text-align: center;
            margin-bottom: 4px;
        }}
        .register-subtitle {{
            font-size: 14px;
            color: #94a3b8;
            text-align: center;
            margin-bottom: 32px;
        }}
        .plan-selector {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 12px;
            margin-bottom: 24px;
        }}
        .plan-option {{
            border: 2px solid #e2e8f0;
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
            background: white;
        }}
        .plan-option.selected {{
            border-color: #7c3aed;
            background: #faf5ff;
            box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
        }}
        .plan-option-icon {{
            font-size: 28px;
            margin-bottom: 8px;
        }}
        .plan-option-name {{
            font-size: 14px;
            font-weight: 700;
            color: #0f172a;
            margin-bottom: 4px;
        }}
        .plan-option-price {{
            font-size: 20px;
            font-weight: 800;
            color: #7c3aed;
        }}
        .plan-option-period {{
            font-size: 11px;
            color: #94a3b8;
        }}
        .form-group {{
            margin-bottom: 16px;
        }}
        .form-label {{
            font-size: 13px;
            font-weight: 600;
            color: #475569;
            margin-bottom: 6px;
            display: block;
        }}
        .q-field--outlined .q-field__control {{
            border-radius: 10px !important;
            height: 48px !important;
            background: #fafafa !important;
        }}
        .register-btn {{
            width: 100%;
            height: 48px;
            background: #7c3aed;
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            font-family: inherit;
            transition: all 0.2s;
            margin-top: 8px;
        }}
        .register-btn:hover {{
            background: #6d28d9;
        }}
        .login-link {{
            text-align: center;
            margin-top: 20px;
            font-size: 13px;
            color: #94a3b8;
        }}
        .login-link span {{
            color: #7c3aed;
            font-weight: 600;
            cursor: pointer;
        }}
        .login-link span:hover {{
            text-decoration: underline;
        }}
        .error-msg {{
            background: #fef2f2;
            border-left: 3px solid #ef4444;
            color: #ef4444;
            padding: 12px 16px;
            border-radius: 8px;
            font-size: 13px;
            margin-bottom: 16px;
            display: none;
        }}
        .error-msg.show {{
            display: block;
        }}
    </style>
    """)
    
    plano_selecionado = {"plano": "gratuito"}
    planos_refs = {}
    
    with ui.element('div').classes('register-container'):
        ui.image(WORDMARK).classes('register-logo')
        ui.label('Criar sua Conta').classes('register-title')
        ui.label('Comece grátis, faça upgrade quando quiser').classes('register-subtitle')
        
        # Seletor de plano
        with ui.element('div').classes('plan-selector'):
            # Plano Gratuito
            plano_free = ui.element('div').classes('plan-option selected')
            with plano_free:
                ui.label('🆓').classes('plan-option-icon')
                ui.label('Gratuito').classes('plan-option-name')
                ui.label('R$ 0').classes('plan-option-price')
                ui.label('para sempre').classes('plan-option-period')
            plano_free.on('click', lambda: selecionar_plano('gratuito'))
            planos_refs['gratuito'] = plano_free
            
            # Plano Premium
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
                if nome == plano:
                    ref.classes('plan-option selected')
                else:
                    ref.classes(remove='selected')
        
        # Campos do formulário
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
                erro_label.classes('error-msg show')
                erro_label.set_text('⚠️ Preencha todos os campos')
                return
            
            if senha != confirmar:
                erro_label.classes('error-msg show')
                erro_label.set_text('⚠️ Senhas não conferem')
                return
            
            if len(senha) < 4:
                erro_label.classes('error-msg show')
                erro_label.set_text('⚠️ Senha deve ter pelo menos 4 caracteres')
                return
            
            sucesso, msg, usuario = criar_usuario(nome, email, senha, plano_selecionado["plano"])
            
            if sucesso:
                plano_nome = 'Premium' if plano_selecionado["plano"] == 'premium' else 'Gratuito'
                ui.notify(f'✅ Conta {plano_nome} criada! Redirecionando...', type='positive', position='top', timeout=3000)
                ui.timer(1.5, lambda: ui.navigate.to('/login'), once=True)
            else:
                erro_label.classes('error-msg show')
                erro_label.set_text(f'❌ {msg}')
        
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