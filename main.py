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
LOGO_BRANCA = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845617/logo_branca_mmgwof.png"
LOGO_FULL_BRANCA = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845630/logo_full_branca_wlx97y.png"
LOGO = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845521/logo_bvchvv.png"
WORDMARK = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845635/wordmark_nf3put.png"
FAVICON = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845656/favicon_crsq9e.ico"

# Imagens placeholder (substitua depois)
HERO_IMAGE = "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800"
DASHBOARD_MOCKUP = "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=600"
MOBILE_MOCKUP = "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=400"
FEATURES_BG = "https://images.unsplash.com/photo-1551434678-e076c223a692?w=1200"

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
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,400&display=swap');
        
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        
        html, body {{
            font-family: 'DM Sans', sans-serif;
            scroll-behavior: smooth;
            overflow-x: hidden;
            background: #fff;
        }}
        
        /* Navbar */
        .navbar {{
            position: fixed;
            top: 0; left: 0; right: 0;
            z-index: 1000;
            padding: 16px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            transition: all 0.3s;
            background: rgba(255,255,255,0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(0,0,0,0.05);
        }}
        
        .navbar-logo {{
            height: 32px;
            width: auto;
        }}
        
        .navbar-links {{
            display: flex;
            gap: 24px;
            align-items: center;
        }}
        
        .navbar-links a {{
            text-decoration: none;
            color: #475569;
            font-size: 14px;
            font-weight: 500;
            transition: color 0.2s;
        }}
        
        .navbar-links a:hover {{
            color: #8b5cf6;
        }}
        
        .btn-primary {{
            background: linear-gradient(135deg, #8b5cf6, #6366f1);
            color: white !important;
            padding: 10px 20px;
            border-radius: 10px;
            font-weight: 600 !important;
            transition: all 0.3s !important;
            border: none;
            cursor: pointer;
            font-size: 14px;
            font-family: 'DM Sans', sans-serif;
        }}
        
        .btn-primary:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
        }}
        
        .btn-outline {{
            background: transparent;
            color: #8b5cf6 !important;
            padding: 10px 20px;
            border-radius: 10px;
            font-weight: 600 !important;
            border: 2px solid #8b5cf6;
            cursor: pointer;
            font-size: 14px;
            font-family: 'DM Sans', sans-serif;
            transition: all 0.3s;
        }}
        
        .btn-outline:hover {{
            background: #8b5cf6;
            color: white !important;
        }}
        
        /* Hero */
        .hero {{
            padding: 120px 24px 80px;
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
            background: linear-gradient(180deg, #faf5ff 0%, #fff 100%);
            position: relative;
            overflow: hidden;
        }}
        
        .hero::before {{
            content: '';
            position: absolute;
            width: 600px; height: 600px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(139,92,246,0.1) 0%, transparent 70%);
            top: -200px; right: -200px;
        }}
        
        .hero::after {{
            content: '';
            position: absolute;
            width: 400px; height: 400px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(99,102,241,0.08) 0%, transparent 70%);
            bottom: -100px; left: -100px;
        }}
        
        .hero-content {{
            max-width: 1200px;
            width: 100%;
            display: flex;
            align-items: center;
            gap: 60px;
            position: relative;
            z-index: 1;
        }}
        
        .hero-text {{
            flex: 1;
        }}
        
        .hero-text h1 {{
            font-size: 56px;
            font-weight: 900;
            line-height: 1.1;
            color: #1e293b;
            margin-bottom: 20px;
        }}
        
        .hero-text h1 span {{
            background: linear-gradient(135deg, #8b5cf6, #6366f1);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .hero-text p {{
            font-size: 18px;
            color: #64748b;
            line-height: 1.7;
            margin-bottom: 32px;
            max-width: 500px;
        }}
        
        .hero-image {{
            flex: 1;
            display: flex;
            justify-content: center;
        }}
        
        .hero-image img {{
            max-width: 100%;
            border-radius: 20px;
            box-shadow: 0 30px 80px rgba(0,0,0,0.15);
        }}
        
        .hero-buttons {{
            display: flex;
            gap: 16px;
        }}
        
        /* Seções */
        .section {{
            padding: 80px 24px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        
        .section-title {{
            text-align: center;
            margin-bottom: 60px;
        }}
        
        .section-title h2 {{
            font-size: 40px;
            font-weight: 800;
            color: #1e293b;
            margin-bottom: 16px;
        }}
        
        .section-title p {{
            font-size: 18px;
            color: #64748b;
            max-width: 600px;
            margin: 0 auto;
        }}
        
        /* Features */
        .features-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 24px;
        }}
        
        .feature-card {{
            background: white;
            border: 1px solid #f1f5f9;
            border-radius: 20px;
            padding: 32px 28px;
            transition: all 0.3s;
            cursor: default;
        }}
        
        .feature-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 20px 50px rgba(0,0,0,0.08);
            border-color: #e2e8f0;
        }}
        
        .feature-icon {{
            width: 56px;
            height: 56px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            margin-bottom: 20px;
        }}
        
        .feature-card h3 {{
            font-size: 18px;
            font-weight: 700;
            color: #1e293b;
            margin-bottom: 8px;
        }}
        
        .feature-card p {{
            font-size: 14px;
            color: #64748b;
            line-height: 1.6;
        }}
        
        /* Pricing */
        .pricing-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 24px;
            max-width: 800px;
            margin: 0 auto;
        }}
        
        .pricing-card {{
            background: white;
            border: 2px solid #e5e7eb;
            border-radius: 24px;
            padding: 40px 32px;
            text-align: center;
            transition: all 0.3s;
        }}
        
        .pricing-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 20px 50px rgba(0,0,0,0.08);
        }}
        
        .pricing-card.premium {{
            border-color: #8b5cf6;
            background: linear-gradient(180deg, #faf5ff 0%, #fff 100%);
            box-shadow: 0 20px 60px rgba(139, 92, 246, 0.15);
        }}
        
        .pricing-card h3 {{
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 8px;
        }}
        
        .pricing-card .price {{
            font-size: 48px;
            font-weight: 900;
            color: #8b5cf6;
            margin: 16px 0;
        }}
        
        .pricing-card .price span {{
            font-size: 16px;
            font-weight: 400;
            color: #94a3b8;
        }}
        
        .pricing-card ul {{
            list-style: none;
            margin: 24px 0;
            text-align: left;
        }}
        
        .pricing-card ul li {{
            padding: 8px 0;
            font-size: 14px;
            color: #475569;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        /* CTA */
        .cta {{
            background: linear-gradient(135deg, #8b5cf6, #6366f1);
            padding: 80px 24px;
            text-align: center;
            color: white;
        }}
        
        .cta h2 {{
            font-size: 40px;
            font-weight: 800;
            margin-bottom: 16px;
        }}
        
        .cta p {{
            font-size: 18px;
            opacity: 0.9;
            margin-bottom: 32px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }}
        
        .cta .btn-white {{
            background: white;
            color: #6366f1;
            padding: 16px 40px;
            border-radius: 14px;
            font-size: 16px;
            font-weight: 700;
            border: none;
            cursor: pointer;
            font-family: 'DM Sans', sans-serif;
            transition: all 0.3s;
        }}
        
        .cta .btn-white:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }}
        
        /* Footer */
        .footer {{
            background: #1e293b;
            color: white;
            padding: 60px 24px 30px;
        }}
        
        .footer-content {{
            max-width: 1200px;
            margin: 0 auto;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 40px;
        }}
        
        .footer h4 {{
            font-size: 16px;
            font-weight: 700;
            margin-bottom: 16px;
        }}
        
        .footer p, .footer a {{
            font-size: 13px;
            color: #94a3b8;
            line-height: 1.8;
            text-decoration: none;
            display: block;
        }}
        
        .footer a:hover {{
            color: white;
        }}
        
        .footer-bottom {{
            max-width: 1200px;
            margin: 40px auto 0;
            padding-top: 24px;
            border-top: 1px solid rgba(255,255,255,0.1);
            text-align: center;
            font-size: 13px;
            color: #64748b;
        }}
        
        /* Mobile */
        @media (max-width: 768px) {{
            .hero-content {{
                flex-direction: column;
                text-align: center;
            }}
            .hero-text h1 {{
                font-size: 36px;
            }}
            .hero-text p {{
                max-width: 100%;
            }}
            .hero-buttons {{
                justify-content: center;
            }}
            .hero-image {{
                display: none;
            }}
            .navbar-links a {{
                display: none;
            }}
            .section-title h2 {{
                font-size: 28px;
            }}
            .pricing-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
    """)
    
    # ============================================================
    # NAVBAR
    # ============================================================
    with ui.element('div').classes('navbar'):
        ui.image(WORDMARK).classes('navbar-logo')
        with ui.element('div').classes('navbar-links'):
            ui.label('Funcionalidades').on('click', lambda: ui.run_javascript('document.getElementById("features").scrollIntoView({behavior:"smooth"})'))
            ui.label('Planos').on('click', lambda: ui.run_javascript('document.getElementById("pricing").scrollIntoView({behavior:"smooth"})'))
            ui.button('Entrar', on_click=lambda: ui.navigate.to('/login')).classes('btn-outline')
            ui.button('Criar Conta', on_click=lambda: ui.navigate.to('/criar-conta')).classes('btn-primary')
    
    # ============================================================
    # HERO
    # ============================================================
    with ui.element('div').classes('hero'):
        with ui.element('div').classes('hero-content'):
            with ui.element('div').classes('hero-text'):
                ui.label('Controle Inteligente do seu ').style('font-size:56px;font-weight:900;color:#1e293b;line-height:1.1;')
                ui.label('Cartão de Crédito').style('font-size:56px;font-weight:900;background:linear-gradient(135deg,#8b5cf6,#6366f1);-webkit-background-clip:text;-webkit-text-fill-color:transparent;')
                ui.label('Gerencie seus gastos, defina limites e tenha total controle das suas finanças em um só lugar.').style('font-size:18px;color:#64748b;line-height:1.7;margin-top:20px;max-width:500px;')
                with ui.element('div').classes('hero-buttons').style('margin-top:32px;'):
                    ui.button('🚀 Começar Grátis', on_click=lambda: ui.navigate.to('/criar-conta')).classes('btn-primary').style('padding:16px 32px;font-size:16px;')
                    ui.button('📱 Ver Demo', on_click=lambda: ui.navigate.to('/login')).classes('btn-outline').style('padding:16px 32px;font-size:16px;')
            with ui.element('div').classes('hero-image'):
                ui.image(HERO_IMAGE).style('max-width:100%;border-radius:20px;box-shadow:0 30px 80px rgba(0,0,0,0.15);')
    
    # ============================================================
    # FEATURES
    # ============================================================
    with ui.element('div').props('id=features').classes('section'):
        with ui.element('div').classes('section-title'):
            ui.label('✨ Funcionalidades').style('font-size:40px;font-weight:800;color:#1e293b;')
            ui.label('Tudo que você precisa para dominar suas finanças').style('font-size:18px;color:#64748b;')
        
        with ui.element('div').classes('features-grid'):
            features = [
                ("📊", "#3b82f6", "Dashboard Inteligente", "Visualize seus gastos em tempo real com KPIs claros e objetivos."),
                ("💳", "#8b5cf6", "Controle de Cartões", "Gerencie múltiplos cartões com limites individuais ou unificados."),
                ("🤖", "#10b981", "Consultor Financeiro", "30+ alertas inteligentes que analisam seus hábitos de consumo."),
                ("📅", "#f59e0b", "Ciclo de Fatura", "Acompanhe gastos por ciclo de fatura ou mês, como preferir."),
                ("🔁", "#ec4899", "Gastos Recorrentes", "Cadastre assinaturas e gastos fixos que entram automaticamente."),
                ("🎯", "#6366f1", "Metas e Limites", "Defina orçamentos e receba alertas antes de estourar o limite."),
            ]
            for icone, cor, titulo, desc in features:
                with ui.element('div').classes('feature-card'):
                    with ui.element('div').classes('feature-icon').style(f'background:{cor}15;'):
                        ui.label(icone).style('font-size:28px;')
                    ui.label(titulo).style('font-size:18px;font-weight:700;color:#1e293b;margin-bottom:8px;')
                    ui.label(desc).style('font-size:14px;color:#64748b;line-height:1.6;')
    
    # ============================================================
    # PRICING
    # ============================================================
    with ui.element('div').props('id=pricing').classes('section').style('background:#f8fafc;max-width:100%;padding:80px 24px;'):
        with ui.element('div').style('max-width:1200px;margin:0 auto;'):
            with ui.element('div').classes('section-title'):
                ui.label('💎 Planos').style('font-size:40px;font-weight:800;color:#1e293b;')
                ui.label('Escolha o plano ideal para você').style('font-size:18px;color:#64748b;')
            
            with ui.element('div').classes('pricing-grid'):
                # Gratuito
                with ui.element('div').classes('pricing-card'):
                    ui.label('🆓 Gratuito').style('font-size:24px;font-weight:700;')
                    with ui.element('div').classes('price'):
                        ui.label('R$ 0').style('font-size:48px;font-weight:900;color:#8b5cf6;display:inline;')
                        ui.label('/mês').style('font-size:16px;color:#94a3b8;display:inline;')
                    ui.label('Perfeito para começar').style('font-size:14px;color:#64748b;')
                    with ui.element('ul'):
                        for item in ['✅ 20 lançamentos/mês', '✅ 1 cartão', '✅ Modo Unificado', '✅ Consultor básico', '✅ Dashboard completo']:
                            ui.label(item).style('padding:8px 0;font-size:14px;color:#475569;')
                    ui.button('Começar Grátis', on_click=lambda: ui.navigate.to('/criar-conta')).classes('btn-primary').style('width:100%;')
                
                # Premium
                with ui.element('div').classes('pricing-card premium'):
                    with ui.element('div').style('background:#8b5cf6;color:white;padding:4px 16px;border-radius:20px;display:inline-block;font-size:12px;font-weight:600;margin-bottom:12px;'):
                        ui.label('MAIS POPULAR')
                    ui.label('💎 Premium').style('font-size:24px;font-weight:700;')
                    with ui.element('div').classes('price'):
                        ui.label('R$ 4,99').style('font-size:48px;font-weight:900;color:#8b5cf6;display:inline;')
                        ui.label('/mês').style('font-size:16px;color:#94a3b8;display:inline;')
                    ui.label('Para quem quer tudo').style('font-size:14px;color:#64748b;')
                    with ui.element('ul'):
                        for item in ['✅ Lançamentos ilimitados', '✅ Múltiplos cartões', '✅ Modo Individual', '✅ Consultor Premium (30+)', '✅ Relatórios avançados', '✅ Suporte prioritário']:
                            ui.label(item).style('padding:8px 0;font-size:14px;color:#475569;')
                    ui.button('Assinar Premium', on_click=lambda: ui.navigate.to('/criar-conta')).classes('btn-primary').style('width:100%;')
    
    # ============================================================
    # CTA
    # ============================================================
    with ui.element('div').classes('cta'):
        ui.label('Pronto para controlar suas finanças?').style('font-size:40px;font-weight:800;margin-bottom:16px;')
        ui.label('Junte-se a milhares de usuários que já transformaram sua relação com o dinheiro.').style('font-size:18px;opacity:0.9;margin-bottom:32px;max-width:600px;margin-left:auto;margin-right:auto;')
        ui.button('🚀 Criar Conta Gratuita', on_click=lambda: ui.navigate.to('/criar-conta')).classes('btn-white')
    
    # ============================================================
    # FOOTER
    # ============================================================
    with ui.element('div').classes('footer'):
        with ui.element('div').classes('footer-content'):
            with ui.column():
                ui.image(WORDMARK).style('height:28px;width:auto;margin-bottom:16px;filter:brightness(0) invert(1);')
                ui.label('Controle Inteligente do seu Crédito').style('font-size:13px;color:#94a3b8;')
            
            with ui.column():
                ui.label('Produto').style('font-size:16px;font-weight:700;margin-bottom:16px;')
                ui.label('Funcionalidades').style('font-size:13px;color:#94a3b8;')
                ui.label('Planos').style('font-size:13px;color:#94a3b8;')
                ui.label('Demo').style('font-size:13px;color:#94a3b8;')
            
            with ui.column():
                ui.label('Suporte').style('font-size:16px;font-weight:700;margin-bottom:16px;')
                ui.label('Central de Ajuda').style('font-size:13px;color:#94a3b8;')
                ui.label('Email: suporte@cartometro.app').style('font-size:13px;color:#94a3b8;')
                ui.label('FAQ').style('font-size:13px;color:#94a3b8;')
            
            with ui.column():
                ui.label('Legal').style('font-size:16px;font-weight:700;margin-bottom:16px;')
                ui.label('Termos de Uso').style('font-size:13px;color:#94a3b8;')
                ui.label('Privacidade').style('font-size:13px;color:#94a3b8;')
        
        with ui.element('div').classes('footer-bottom'):
            ui.label('© 2025 Cartometro. Todos os direitos reservados.')


# =========================
# TELA DE LOGIN (separada da landing)
# =========================
@ui.page('/login')
def login():
    cor = config_service.get_primary_color()
    cor_escura = config_service.get_primary_dark()

    ui.add_head_html(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&display=swap');
    <link rel="icon" type="image/x-icon" href="{FAVICON}">
    *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
    html, body {{ height: 100%; width: 100%; overflow: hidden; font-family: 'DM Sans', sans-serif; }}
    .lp-root {{ display: flex; height: 100vh; width: 100%; }}
    .lp-brand {{ flex: 1; background: linear-gradient(160deg, {cor_escura} 0%, {cor} 60%, {cor}bb 100%); display: flex; justify-content: center; align-items: center; position: relative; overflow: hidden; }}
    .lp-brand::before {{ content: ''; position: absolute; width: 500px; height: 500px; border-radius: 50%; border: 80px solid rgba(255,255,255,0.04); top: -150px; right: -150px; }}
    .lp-brand::after {{ content: ''; position: absolute; width: 350px; height: 350px; border-radius: 50%; border: 50px solid rgba(255,255,255,0.04); bottom: -80px; left: -80px; }}
    .lp-brand-logo {{ width: 300px; height: auto; position: relative; z-index: 1; }}
    .lp-form-side {{ width: 480px; height: 100%; flex-shrink: 0; display: flex; align-items: center; justify-content: center; background: #fff; padding: 48px 44px; }}
    .lp-form-box {{ width: 100%; max-width: 380px; }}
    .lp-form-logo {{ width: 180px; height: auto; margin-bottom: 32px; align-self: center; display: block; margin-left: auto; margin-right: auto; }}
    .lp-field-wrap {{ margin-bottom: 16px; }}
    .lp-field-label {{ font-size: 13px; font-weight: 500; color: #4b5563; margin-bottom: 6px; display: block; }}
    .lp-field-wrap .q-field--outlined .q-field__control {{ border-radius: 10px !important; height: 48px !important; background: #fafafa !important; font-size: 14px !important; }}
    .lp-field-wrap .q-field--outlined.q-field--focused .q-field__control {{ border-color: {cor} !important; box-shadow: 0 0 0 3px {cor}22 !important; }}
    .lp-error {{ font-size: 13px; color: #ef4444; background: #fef2f2; border-radius: 8px; padding: 10px 14px; margin-top: 12px; display: none; border-left: 3px solid #ef4444; }}
    .lp-hint {{ margin-top: 28px; padding-top: 20px; border-top: 1px solid #f3f4f6; }}
    .lp-hint-label {{ font-size: 11px; font-weight: 600; color: #d1d5db; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; }}
    .lp-hint-item {{ font-size: 12.5px; color: #9ca3af; cursor: pointer; transition: color 0.15s; padding: 3px 0; }}
    .lp-hint-item:hover {{ color: #374151; }}
    .lp-criar-conta {{ margin-top: 20px; text-align: center; }}
    .lp-criar-conta span {{ font-size: 13px; color: #9ca3af; }}
    .lp-criar-conta a {{ color: {cor}; font-weight: 600; cursor: pointer; text-decoration: none; }}
    .lp-criar-conta a:hover {{ text-decoration: underline; }}
    .back-link {{ text-align: center; margin-bottom: 24px; }}
    .back-link a {{ color: #64748b; font-size: 13px; cursor: pointer; text-decoration: none; }}
    .back-link a:hover {{ color: #1e293b; }}
    @media (max-width: 768px) {{ .lp-brand {{ display: none; }} .lp-form-side {{ width: 100%; padding: 24px; }} }}
    </style>
    """)

    def fazer_login():
        email = email_input.value.strip() if email_input.value else ''
        senha = senha_input.value or ''
        if not email or not senha:
            error_label.style('display: block'); error_label.set_text('⚠️ Preencha todos os campos.'); return
        usuario = autenticar_usuario(email, senha)
        if usuario:
            global usuario_atual; usuario_atual = usuario
            if email == 'demo': resetar_dados_demo(email)
            set_usuario_logado(email)
            ui.notify(f'✅ Bem-vindo, {usuario["nome"]}!', type='positive', position='top')
            ui.navigate.to('/app')
        else:
            error_label.style('display: block'); error_label.set_text('❌ Email ou senha incorretos.')

    def preencher_demo():
        email_input.value = 'demo'; senha_input.value = 'admin'

    with ui.element('div').classes('lp-root'):
        with ui.element('div').classes('lp-brand'):
            ui.image(LOGO_BRANCA).classes('lp-brand-logo')
        with ui.element('div').classes('lp-form-side'):
            with ui.element('div').classes('lp-form-box'):
                with ui.element('div').classes('back-link'):
                    ui.label('← Voltar para o site').on('click', lambda: ui.navigate.to('/'))
                ui.image(WORDMARK).classes('lp-form-logo')
                ui.label('Entrar na conta').style('font-size:26px;font-weight:700;letter-spacing:-0.8px;color:#0f0f0f;margin-bottom:6px;')
                ui.label('Bem-vindo de volta!').style('font-size:14px;color:#9ca3af;margin-bottom:32px;')
                with ui.element('div').classes('lp-field-wrap'):
                    ui.label('E-mail').classes('lp-field-label')
                    email_input = ui.input(placeholder='demo').props('outlined dense').classes('w-full')
                with ui.element('div').classes('lp-field-wrap'):
                    ui.label('Senha').classes('lp-field-label')
                    senha_input = ui.input(placeholder='••••••••', password=True, password_toggle_button=True).props('outlined dense').classes('w-full')
                error_label = ui.label('').classes('lp-error')
                ui.button('Entrar', on_click=fazer_login).props('no-caps').style(f'width:100%;height:48px;border-radius:11px;background:{cor};color:white;border:none;font-size:15px;font-weight:600;cursor:pointer;margin-top:10px;')
                with ui.element('div').classes('lp-hint'):
                    ui.label('Acesso rápido').classes('lp-hint-label')
                    ui.label('👑 demo / admin (Demonstração)').classes('lp-hint-item').on('click', preencher_demo)
                with ui.element('div').classes('lp-criar-conta'):
                    ui.label('Não tem conta? ').style('display:inline;font-size:13px;color:#9ca3af;')
                    ui.label('Criar conta gratuita').style('display:inline;color:#8b5cf6;font-weight:600;cursor:pointer;font-size:13px;').on('click', lambda: ui.navigate.to('/criar-conta'))


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
        .plano-card { flex: 1; border: 2px solid #e5e7eb; border-radius: 14px; padding: 14px 10px; text-align: center; cursor: pointer; transition: all 0.2s; background: white; }
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
                    ui.label('🆓').style('font-size:28px;'); ui.label('Gratuito').style('font-size:14px;font-weight:700;')
                    ui.label('R$ 0').style('font-size:22px;font-weight:700;color:#8b5cf6;'); ui.label('para sempre').style('font-size:11px;color:#9ca3af;')
                plano_gratuito.on('click', lambda: selecionar_plano('gratuito')); planos_refs['gratuito'] = plano_gratuito
                
                plano_premium = ui.element('div').classes('plano-card')
                with plano_premium:
                    ui.label('💎').style('font-size:28px;'); ui.label('Premium').style('font-size:14px;font-weight:700;')
                    ui.label('R$ 4,99').style('font-size:22px;font-weight:700;color:#8b5cf6;'); ui.label('/mês').style('font-size:11px;color:#9ca3af;')
                plano_premium.on('click', lambda: selecionar_plano('premium')); planos_refs['premium'] = plano_premium
            
            def selecionar_plano(plano):
                plano_selecionado["plano"] = plano
                for nome, ref in planos_refs.items():
                    if nome == plano: ref.classes('plano-card selecionado'); ref.style('border-color:#8b5cf6;background:#faf5ff;box-shadow:0 0 0 3px rgba(139,92,246,0.1);')
                    else: ref.classes(remove='selecionado'); ref.style('border-color:#e5e7eb;background:white;box-shadow:none;')
                btn_criar.style('background:#8b5cf6;' if plano == 'premium' else 'background:#3b82f6;')
                btn_criar.set_text('Criar Conta Premium' if plano == 'premium' else 'Criar Conta Gratuita')
            
            with ui.element('div').classes('campo'):
                ui.label('Nome completo'); nome_input = ui.input(placeholder='Seu nome completo').props('outlined dense').classes('w-full')
            with ui.element('div').classes('campo'):
                ui.label('E-mail'); email_input = ui.input(placeholder='seu@email.com').props('outlined dense').classes('w-full')
            with ui.element('div').classes('campo'):
                ui.label('Senha'); senha_input = ui.input(placeholder='Mínimo 4 caracteres', password=True, password_toggle_button=True).props('outlined dense').classes('w-full')
            with ui.element('div').classes('campo'):
                ui.label('Confirmar Senha'); confirmar_input = ui.input(placeholder='Repita a senha', password=True, password_toggle_button=True).props('outlined dense').classes('w-full')
            
            erro_label = ui.label('').classes('erro-msg')
            
            def cadastrar():
                nome = nome_input.value.strip() if nome_input.value else ''; email = email_input.value.strip() if email_input.value else ''
                senha = senha_input.value or ''; confirmar = confirmar_input.value or ''
                erro_label.classes(remove='show'); erro_label.style('display:none;')
                if not nome or not email or not senha: erro_label.classes('erro-msg show'); erro_label.style('display:block;'); erro_label.set_text('⚠️ Preencha todos os campos'); return
                if senha != confirmar: erro_label.classes('erro-msg show'); erro_label.style('display:block;'); erro_label.set_text('⚠️ Senhas não conferem'); return
                if len(senha) < 4: erro_label.classes('erro-msg show'); erro_label.style('display:block;'); erro_label.set_text('⚠️ Senha deve ter pelo menos 4 caracteres'); return
                sucesso, msg, usuario = criar_usuario(nome, email, senha, plano_selecionado["plano"])
                if sucesso:
                    plano_nome = 'Premium' if plano_selecionado["plano"] == 'premium' else 'Gratuito'
                    ui.notify(f'✅ Conta {plano_nome} criada! Faça login.', type='positive', position='top', timeout=3000)
                    ui.timer(1.5, lambda: ui.navigate.to('/login'), once=True)
                else: erro_label.classes('erro-msg show'); erro_label.style('display:block;'); erro_label.set_text(f'❌ {msg}')
            
            btn_criar = ui.button('Criar Conta Gratuita', on_click=cadastrar).props('no-caps')
            btn_criar.style('width:100%;padding:14px;border-radius:12px;background:#3b82f6;color:white;border:none;font-size:15px;font-weight:600;cursor:pointer;')
            with ui.element('div').style('text-align:center;margin-top:16px;'):
                ui.label('Já tem conta? ').style('display:inline;font-size:13px;color:#9ca3af;')
                ui.label('Fazer login').style('display:inline;color:#8b5cf6;font-weight:600;cursor:pointer;font-size:13px;').on('click', lambda: ui.navigate.to('/login'))


# =========================
# TELA PRINCIPAL (PÓS-LOGIN)
# =========================
@ui.page('/app')
def app():
    global usuario_atual, container_principal
    if not usuario_atual: ui.navigate.to('/login'); return
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