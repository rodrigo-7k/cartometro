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

# Imagens placeholder (substitua depois)
HERO_IMAGE      = "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&q=80"
DASHBOARD_MOCKUP= "https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=700&q=80"
MOBILE_MOCKUP   = "https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=400&q=80"

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

    ui.add_head_html("""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;0,9..40,800;0,9..40,900;1,9..40,400&display=swap" rel="stylesheet">
    <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    html { scroll-behavior: smooth; }
    body {
        font-family: 'DM Sans', sans-serif;
        overflow-x: hidden;
        background: #fff;
        color: #1e293b;
    }

    /* ── Navbar ─────────────────────────────── */
    .lp-nav {
        position: fixed; top: 0; left: 0; right: 0; z-index: 999;
        display: flex; align-items: center; justify-content: space-between;
        padding: 0 40px; height: 68px;
        background: rgba(255,255,255,0.92);
        backdrop-filter: blur(14px);
        border-bottom: 1px solid rgba(0,0,0,0.06);
        transition: box-shadow 0.3s;
    }
    .lp-nav.scrolled { box-shadow: 0 4px 30px rgba(0,0,0,0.08); }
    .lp-nav-logo { height: 34px; width: auto; display: block; }
    .lp-nav-links { display: flex; align-items: center; gap: 8px; }
    .lp-nav-link {
        font-size: 14px; font-weight: 500; color: #475569;
        padding: 8px 14px; border-radius: 8px;
        cursor: pointer; transition: all 0.2s;
    }
    .lp-nav-link:hover { color: #7c3aed; background: #f5f3ff; }
    .lp-btn-ghost {
        font-size: 14px; font-weight: 600; color: #7c3aed !important;
        padding: 9px 18px; border-radius: 10px;
        border: 1.5px solid #ddd6fe; background: transparent;
        cursor: pointer; transition: all 0.2s;
        font-family: 'DM Sans', sans-serif;
    }
    .lp-btn-ghost:hover { border-color: #7c3aed; background: #f5f3ff; }
    .lp-btn-solid {
        font-size: 14px; font-weight: 600; color: #fff !important;
        padding: 9px 20px; border-radius: 10px;
        background: linear-gradient(135deg, #7c3aed 0%, #6366f1 100%);
        border: none; cursor: pointer;
        font-family: 'DM Sans', sans-serif;
        transition: all 0.25s;
        box-shadow: 0 2px 12px rgba(109,40,217,0.25);
    }
    .lp-btn-solid:hover { transform: translateY(-1px); box-shadow: 0 6px 20px rgba(109,40,217,0.35); }
    .lp-nav-mobile-actions { display: none; }

    /* ── Hero ────────────────────────────────── */
    .lp-hero {
        min-height: 100vh;
        padding: 100px 40px 80px;
        display: flex; align-items: center; justify-content: center;
        background: linear-gradient(155deg, #faf5ff 0%, #f0f4ff 50%, #fff 100%);
        position: relative; overflow: hidden;
    }
    .lp-hero::before {
        content: '';
        position: absolute; inset: 0;
        background:
            radial-gradient(ellipse 700px 500px at 80% 20%, rgba(124,58,237,0.08) 0%, transparent 70%),
            radial-gradient(ellipse 500px 400px at 10% 80%, rgba(99,102,241,0.07) 0%, transparent 70%);
        pointer-events: none;
    }
    .lp-hero-inner {
        max-width: 1160px; width: 100%;
        display: grid; grid-template-columns: 1fr 1fr;
        gap: 64px; align-items: center;
        position: relative; z-index: 1;
    }
    .lp-hero-badge {
        display: inline-flex; align-items: center; gap: 8px;
        background: #f5f3ff; border: 1px solid #ddd6fe;
        color: #7c3aed; font-size: 13px; font-weight: 600;
        padding: 6px 14px; border-radius: 100px;
        margin-bottom: 24px;
    }
    .lp-hero-badge span { width: 6px; height: 6px; background: #7c3aed; border-radius: 50%; }
    .lp-hero-h1 {
        font-size: clamp(36px, 4.5vw, 58px);
        font-weight: 900; line-height: 1.08;
        letter-spacing: -1.5px; color: #1e293b;
        margin-bottom: 22px;
    }
    .lp-hero-h1 em {
        font-style: normal;
        background: linear-gradient(135deg, #7c3aed, #6366f1);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .lp-hero-sub {
        font-size: 17px; color: #64748b; line-height: 1.75;
        max-width: 480px; margin-bottom: 36px;
    }
    .lp-hero-actions { display: flex; gap: 14px; flex-wrap: wrap; }
    .lp-hero-cta {
        font-size: 15px; font-weight: 700; color: #fff !important;
        padding: 14px 28px; border-radius: 12px;
        background: linear-gradient(135deg, #7c3aed, #6366f1);
        border: none; cursor: pointer;
        font-family: 'DM Sans', sans-serif;
        box-shadow: 0 4px 20px rgba(109,40,217,0.3);
        transition: all 0.25s;
    }
    .lp-hero-cta:hover { transform: translateY(-2px); box-shadow: 0 8px 28px rgba(109,40,217,0.4); }
    .lp-hero-demo {
        font-size: 15px; font-weight: 600; color: #475569 !important;
        padding: 14px 28px; border-radius: 12px;
        background: white; border: 1.5px solid #e2e8f0;
        cursor: pointer; font-family: 'DM Sans', sans-serif;
        transition: all 0.2s;
    }
    .lp-hero-demo:hover { border-color: #c4b5fd; color: #7c3aed !important; background: #faf5ff; }
    .lp-hero-trust {
        margin-top: 32px; display: flex; align-items: center; gap: 10px;
        font-size: 13px; color: #94a3b8;
    }
    .lp-hero-trust-dot { width: 5px; height: 5px; background: #cbd5e1; border-radius: 50%; }

    /* Hero image panel */
    .lp-hero-visual {
        position: relative; display: flex; justify-content: center; align-items: center;
    }
    .lp-hero-img-wrap {
        width: 100%; max-width: 520px;
        border-radius: 24px; overflow: hidden;
        box-shadow: 0 32px 80px rgba(0,0,0,0.14), 0 8px 24px rgba(0,0,0,0.08);
        position: relative;
    }
    .lp-hero-img-wrap img { width: 100%; display: block; }
    .lp-hero-float {
        position: absolute;
        background: white;
        border-radius: 16px;
        padding: 12px 18px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.12);
        display: flex; align-items: center; gap: 12px;
        font-size: 13px; font-weight: 600; color: #1e293b;
        white-space: nowrap; z-index: 2;
    }
    .lp-hero-float.f1 { bottom: -20px; left: -20px; }
    .lp-hero-float.f2 { top: -16px; right: -16px; }
    .lp-float-dot { width: 36px; height: 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 18px; flex-shrink: 0; }

    /* ── Logos / Social proof ─────────────────── */
    .lp-social {
        padding: 36px 40px;
        border-top: 1px solid #f1f5f9; border-bottom: 1px solid #f1f5f9;
        text-align: center;
    }
    .lp-social-label { font-size: 12px; font-weight: 600; letter-spacing: 0.08em; color: #cbd5e1; text-transform: uppercase; margin-bottom: 20px; }
    .lp-social-stats { display: flex; justify-content: center; gap: 56px; flex-wrap: wrap; }
    .lp-stat { display: flex; flex-direction: column; align-items: center; gap: 4px; }
    .lp-stat-num { font-size: 28px; font-weight: 900; color: #1e293b; letter-spacing: -1px; }
    .lp-stat-label { font-size: 13px; color: #94a3b8; }

    /* ── Features ─────────────────────────────── */
    .lp-features {
        padding: 100px 40px;
        background: #fff;
    }
    .lp-section-tag {
        display: inline-flex; align-items: center; gap: 8px;
        font-size: 12px; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase;
        color: #7c3aed; background: #f5f3ff; padding: 6px 14px; border-radius: 100px;
        margin-bottom: 20px;
    }
    .lp-section-h { font-size: clamp(28px, 3.5vw, 42px); font-weight: 900; letter-spacing: -1px; color: #1e293b; margin-bottom: 14px; }
    .lp-section-sub { font-size: 17px; color: #64748b; line-height: 1.7; max-width: 560px; }
    .lp-features-inner { max-width: 1160px; margin: 0 auto; }
    .lp-features-header { text-align: center; margin-bottom: 64px; }
    .lp-features-header .lp-section-sub { margin: 0 auto; }
    .lp-feat-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 20px;
    }
    .lp-feat-card {
        background: #fafafa; border: 1px solid #f1f5f9;
        border-radius: 20px; padding: 32px 28px;
        transition: all 0.3s; cursor: default;
        position: relative; overflow: hidden;
    }
    .lp-feat-card::before {
        content: ''; position: absolute; inset: 0;
        background: linear-gradient(135deg, transparent 60%, rgba(124,58,237,0.03) 100%);
        opacity: 0; transition: opacity 0.3s;
    }
    .lp-feat-card:hover { transform: translateY(-4px); box-shadow: 0 16px 48px rgba(0,0,0,0.08); border-color: #e0e7ff; }
    .lp-feat-card:hover::before { opacity: 1; }
    .lp-feat-icon {
        width: 52px; height: 52px; border-radius: 14px;
        display: flex; align-items: center; justify-content: center;
        font-size: 24px; margin-bottom: 20px;
    }
    .lp-feat-title { font-size: 17px; font-weight: 700; color: #1e293b; margin-bottom: 8px; }
    .lp-feat-desc { font-size: 14px; color: #64748b; line-height: 1.65; }

    /* ── How it works ─────────────────────────── */
    .lp-how {
        padding: 100px 40px;
        background: linear-gradient(180deg, #f8fafc 0%, #fff 100%);
    }
    .lp-how-inner { max-width: 1160px; margin: 0 auto; }
    .lp-how-grid {
        display: grid; grid-template-columns: 1fr 1fr;
        gap: 80px; align-items: center; margin-top: 64px;
    }
    .lp-how-steps { display: flex; flex-direction: column; gap: 32px; }
    .lp-step { display: flex; gap: 20px; align-items: flex-start; }
    .lp-step-num {
        width: 40px; height: 40px; border-radius: 12px; flex-shrink: 0;
        background: linear-gradient(135deg, #7c3aed, #6366f1);
        color: white; font-size: 15px; font-weight: 800;
        display: flex; align-items: center; justify-content: center;
        box-shadow: 0 4px 12px rgba(109,40,217,0.3);
    }
    .lp-step-title { font-size: 17px; font-weight: 700; color: #1e293b; margin-bottom: 6px; }
    .lp-step-desc { font-size: 14px; color: #64748b; line-height: 1.65; }
    .lp-how-visual {
        border-radius: 24px; overflow: hidden;
        box-shadow: 0 24px 64px rgba(0,0,0,0.12);
    }
    .lp-how-visual img { width: 100%; display: block; }

    /* ── Pricing ──────────────────────────────── */
    .lp-pricing {
        padding: 100px 40px;
        background: #fff;
    }
    .lp-pricing-inner { max-width: 1160px; margin: 0 auto; }
    .lp-pricing-header { text-align: center; margin-bottom: 64px; }
    .lp-pricing-header .lp-section-sub { margin: 0 auto; }
    .lp-plans {
        display: grid; grid-template-columns: 1fr 1fr;
        gap: 24px; max-width: 780px; margin: 0 auto;
    }
    .lp-plan {
        border: 1.5px solid #e5e7eb; border-radius: 24px;
        padding: 40px 36px; background: #fff;
        transition: all 0.3s; position: relative;
    }
    .lp-plan:hover { box-shadow: 0 16px 48px rgba(0,0,0,0.08); transform: translateY(-2px); }
    .lp-plan.featured {
        border-color: #7c3aed;
        background: linear-gradient(160deg, #faf5ff 0%, #fff 60%);
        box-shadow: 0 20px 60px rgba(124,58,237,0.12);
    }
    .lp-plan-badge {
        position: absolute; top: -13px; left: 50%; transform: translateX(-50%);
        background: linear-gradient(135deg, #7c3aed, #6366f1);
        color: white; font-size: 11px; font-weight: 700; letter-spacing: 0.08em;
        padding: 5px 16px; border-radius: 100px; text-transform: uppercase; white-space: nowrap;
    }
    .lp-plan-name { font-size: 20px; font-weight: 800; color: #1e293b; margin-bottom: 8px; }
    .lp-plan-price { font-size: 48px; font-weight: 900; color: #7c3aed; line-height: 1; margin: 16px 0 4px; }
    .lp-plan-period { font-size: 14px; color: #94a3b8; margin-bottom: 24px; }
    .lp-plan-divider { height: 1px; background: #f1f5f9; margin: 24px 0; }
    .lp-plan-item { display: flex; align-items: flex-start; gap: 10px; padding: 7px 0; font-size: 14px; color: #475569; }
    .lp-plan-check { font-size: 16px; flex-shrink: 0; margin-top: 1px; }
    .lp-plan-btn {
        width: 100%; margin-top: 28px; padding: 14px;
        border-radius: 12px; font-size: 15px; font-weight: 700;
        border: none; cursor: pointer;
        font-family: 'DM Sans', sans-serif; transition: all 0.25s;
    }
    .lp-plan-btn.solid {
        background: linear-gradient(135deg, #7c3aed, #6366f1);
        color: white !important;
        box-shadow: 0 4px 16px rgba(109,40,217,0.28);
    }
    .lp-plan-btn.solid:hover { transform: translateY(-1px); box-shadow: 0 8px 24px rgba(109,40,217,0.38); }
    .lp-plan-btn.outline {
        background: transparent; color: #7c3aed !important;
        border: 1.5px solid #ddd6fe;
    }
    .lp-plan-btn.outline:hover { background: #f5f3ff; border-color: #7c3aed; }

    /* ── CTA ──────────────────────────────────── */
    .lp-cta {
        padding: 100px 40px;
        background: linear-gradient(135deg, #6d28d9 0%, #4f46e5 100%);
        text-align: center; color: white; position: relative; overflow: hidden;
    }
    .lp-cta::before {
        content: ''; position: absolute; inset: 0;
        background:
            radial-gradient(ellipse 600px 400px at 20% 50%, rgba(255,255,255,0.05) 0%, transparent 70%),
            radial-gradient(ellipse 500px 300px at 80% 50%, rgba(255,255,255,0.04) 0%, transparent 70%);
        pointer-events: none;
    }
    .lp-cta-inner { max-width: 680px; margin: 0 auto; position: relative; z-index: 1; }
    .lp-cta h2 { font-size: clamp(28px, 4vw, 48px); font-weight: 900; letter-spacing: -1px; margin-bottom: 18px; }
    .lp-cta p { font-size: 17px; opacity: 0.85; line-height: 1.7; margin-bottom: 40px; }
    .lp-cta-btn {
        display: inline-block;
        background: white; color: #6d28d9 !important;
        font-size: 16px; font-weight: 700;
        padding: 16px 40px; border-radius: 14px;
        border: none; cursor: pointer;
        font-family: 'DM Sans', sans-serif;
        box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        transition: all 0.25s;
    }
    .lp-cta-btn:hover { transform: translateY(-2px); box-shadow: 0 12px 40px rgba(0,0,0,0.28); }

    /* ── Footer ───────────────────────────────── */
    .lp-footer {
        background: #0f172a; color: #94a3b8;
        padding: 64px 40px 32px;
    }
    .lp-footer-inner { max-width: 1160px; margin: 0 auto; }
    .lp-footer-top {
        display: grid; grid-template-columns: 2fr 1fr 1fr 1fr;
        gap: 48px; padding-bottom: 48px;
        border-bottom: 1px solid rgba(255,255,255,0.07);
    }
    .lp-footer-brand-logo { height: 36px; width: auto; display: block; margin-bottom: 16px; }
    .lp-footer-tagline { font-size: 13px; line-height: 1.7; color: #64748b; max-width: 220px; }
    .lp-footer-col-title { font-size: 13px; font-weight: 700; color: #e2e8f0; margin-bottom: 18px; letter-spacing: 0.03em; }
    .lp-footer-link { font-size: 13px; color: #64748b; margin-bottom: 12px; cursor: pointer; transition: color 0.2s; display: block; }
    .lp-footer-link:hover { color: #e2e8f0; }
    .lp-footer-bottom { padding-top: 28px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px; }
    .lp-footer-copy { font-size: 13px; color: #475569; }

    /* ── Responsivo ───────────────────────────── */
    @media (max-width: 1024px) {
        .lp-feat-grid { grid-template-columns: repeat(2, 1fr); }
        .lp-footer-top { grid-template-columns: 1fr 1fr; }
    }
    @media (max-width: 768px) {
        .lp-nav { padding: 0 20px; }
        .lp-nav-links { display: none; }
        .lp-nav-mobile-actions { display: flex; gap: 8px; }
        .lp-hero { padding: 88px 20px 60px; }
        .lp-hero-inner { grid-template-columns: 1fr; gap: 40px; text-align: center; }
        .lp-hero-actions { justify-content: center; }
        .lp-hero-sub { margin: 0 auto 36px; }
        .lp-hero-trust { justify-content: center; }
        .lp-hero-visual { order: -1; }
        .lp-hero-img-wrap { max-width: 100%; }
        .lp-hero-float.f1 { display: none; }
        .lp-hero-float.f2 { display: none; }
        .lp-social { padding: 36px 20px; }
        .lp-social-stats { gap: 28px; }
        .lp-features, .lp-how, .lp-pricing, .lp-cta { padding: 72px 20px; }
        .lp-feat-grid { grid-template-columns: 1fr; }
        .lp-how-grid { grid-template-columns: 1fr; gap: 48px; }
        .lp-plans { grid-template-columns: 1fr; max-width: 420px; }
        .lp-footer { padding: 48px 20px 28px; }
        .lp-footer-top { grid-template-columns: 1fr 1fr; gap: 32px; }
        .lp-footer-bottom { flex-direction: column; text-align: center; }
    }
    @media (max-width: 480px) {
        .lp-footer-top { grid-template-columns: 1fr; }
    }
    </style>
    <script>
    window.addEventListener('scroll', function() {
        var nav = document.querySelector('.lp-nav');
        if(nav) nav.classList.toggle('scrolled', window.scrollY > 20);
    });
    </script>
    """)

    # ── NAVBAR ────────────────────────────────────────────────────
    with ui.element('div').classes('lp-nav'):
        ui.image(LOGO_FULL_COLOR).classes('lp-nav-logo')
        with ui.element('div').classes('lp-nav-links'):
            ui.label('Funcionalidades').classes('lp-nav-link').on('click', lambda: ui.run_javascript('document.getElementById("features").scrollIntoView({behavior:"smooth"})'))
            ui.label('Como funciona').classes('lp-nav-link').on('click', lambda: ui.run_javascript('document.getElementById("how").scrollIntoView({behavior:"smooth"})'))
            ui.label('Planos').classes('lp-nav-link').on('click', lambda: ui.run_javascript('document.getElementById("pricing").scrollIntoView({behavior:"smooth"})'))
            ui.button('Entrar', on_click=lambda: ui.navigate.to('/login')).classes('lp-btn-ghost')
            ui.button('Criar Conta Grátis', on_click=lambda: ui.navigate.to('/criar-conta')).classes('lp-btn-solid')
        with ui.element('div').classes('lp-nav-mobile-actions'):
            ui.button('Entrar', on_click=lambda: ui.navigate.to('/login')).classes('lp-btn-ghost')
            ui.button('Criar Conta', on_click=lambda: ui.navigate.to('/criar-conta')).classes('lp-btn-solid')

    # ── HERO ──────────────────────────────────────────────────────
    with ui.element('div').classes('lp-hero'):
        with ui.element('div').classes('lp-hero-inner'):
            # Texto
            with ui.element('div').classes('lp-hero-text'):
                with ui.element('div').classes('lp-hero-badge'):
                    ui.element('span')
                    ui.label('Novo: Consultor com 30+ alertas inteligentes')
                ui.html('<h1 class="lp-hero-h1">Controle inteligente<br>do seu <em>cartão de crédito</em></h1>')
                ui.label('Gerencie seus gastos, defina limites e tenha total controle das suas finanças em um só lugar.').classes('lp-hero-sub')
                with ui.element('div').classes('lp-hero-actions'):
                    ui.button('🚀 Começar Grátis', on_click=lambda: ui.navigate.to('/criar-conta')).classes('lp-hero-cta')
                    ui.button('Ver demonstração →', on_click=lambda: ui.navigate.to('/login')).classes('lp-hero-demo')
                with ui.element('div').classes('lp-hero-trust'):
                    ui.label('✓ Grátis para sempre')
                    ui.element('div').classes('lp-hero-trust-dot')
                    ui.label('✓ Sem cartão de crédito')
                    ui.element('div').classes('lp-hero-trust-dot')
                    ui.label('✓ Pronto em 2 minutos')

            # Visual
            with ui.element('div').classes('lp-hero-visual'):
                with ui.element('div').classes('lp-hero-img-wrap'):
                    ui.image(HERO_IMAGE)
                with ui.element('div').classes('lp-hero-float f1'):
                    with ui.element('div').classes('lp-float-dot').style('background:#dcfce7;'):
                        ui.label('💳')
                    with ui.element('div'):
                        ui.label('Limite disponível').style('font-size:11px;color:#94a3b8;font-weight:500;')
                        ui.label('R$ 3.240,00').style('font-size:15px;font-weight:800;color:#1e293b;')
                with ui.element('div').classes('lp-hero-float f2'):
                    with ui.element('div').classes('lp-float-dot').style('background:#f0f4ff;'):
                        ui.label('📊')
                    with ui.element('div'):
                        ui.label('Gastos este mês').style('font-size:11px;color:#94a3b8;font-weight:500;')
                        ui.label('↓ 12% vs anterior').style('font-size:14px;font-weight:700;color:#10b981;')

    # ── SOCIAL PROOF ──────────────────────────────────────────────
    with ui.element('div').classes('lp-social'):
        ui.label('Números que falam por si').classes('lp-social-label')
        with ui.element('div').classes('lp-social-stats'):
            for num, label in [('10k+', 'Usuários ativos'), ('R$2M+', 'Gastos controlados'), ('30+', 'Alertas inteligentes'), ('4.9★', 'Avaliação média')]:
                with ui.element('div').classes('lp-stat'):
                    ui.label(num).classes('lp-stat-num')
                    ui.label(label).classes('lp-stat-label')

    # ── FEATURES ──────────────────────────────────────────────────
    with ui.element('div').classes('lp-features').props('id=features'):
        with ui.element('div').classes('lp-features-inner'):
            with ui.element('div').classes('lp-features-header'):
                ui.label('✦ Funcionalidades').classes('lp-section-tag')
                ui.label('Tudo que você precisa').classes('lp-section-h')
                ui.label('Do controle básico ao gerenciamento avançado — uma plataforma completa para dominar suas finanças.').classes('lp-section-sub')

            with ui.element('div').classes('lp-feat-grid'):
                features = [
                    ("📊", "#3b82f6", "Dashboard Inteligente",  "Visualize KPIs em tempo real: limite usado, gastos por categoria, tendência do mês e muito mais."),
                    ("💳", "#7c3aed", "Múltiplos Cartões",       "Gerencie cada cartão individualmente ou de forma unificada, com limites e ciclos distintos."),
                    ("🤖", "#10b981", "Consultor Financeiro",    "30+ alertas que analisam seus padrões de consumo e te avisam antes de problemas acontecerem."),
                    ("📅", "#f59e0b", "Ciclo de Fatura",         "Acompanhe gastos pelo ciclo real da fatura ou pelo mês calendário — como você preferir."),
                    ("🔁", "#ec4899", "Gastos Recorrentes",      "Cadastre assinaturas e fixos que entram automaticamente todo mês, sem trabalho manual."),
                    ("🎯", "#6366f1", "Metas e Limites",         "Defina orçamentos por categoria e receba alertas em tempo real ao se aproximar do limite."),
                ]
                for icone, cor, titulo, desc in features:
                    with ui.element('div').classes('lp-feat-card'):
                        with ui.element('div').classes('lp-feat-icon').style(f'background:{cor}18;'):
                            ui.label(icone)
                        ui.label(titulo).classes('lp-feat-title')
                        ui.label(desc).classes('lp-feat-desc')

    # ── HOW IT WORKS ──────────────────────────────────────────────
    with ui.element('div').classes('lp-how').props('id=how'):
        with ui.element('div').classes('lp-how-inner'):
            ui.label('✦ Como funciona').classes('lp-section-tag')
            ui.label('Comece em minutos').classes('lp-section-h')
            with ui.element('div').classes('lp-how-grid'):
                with ui.element('div').classes('lp-how-steps'):
                    steps = [
                        ("1", "Crie sua conta grátis", "Cadastre-se em menos de 2 minutos, sem precisar de cartão de crédito."),
                        ("2", "Adicione seus cartões", "Cadastre seus cartões com limites e datas de vencimento da fatura."),
                        ("3", "Lance seus gastos", "Registre compras manualmente ou importe via extrato. Simples e rápido."),
                        ("4", "Receba insights", "O consultor financeiro analisa seus dados e envia alertas personalizados."),
                    ]
                    for num, title, desc in steps:
                        with ui.element('div').classes('lp-step'):
                            ui.label(num).classes('lp-step-num')
                            with ui.element('div'):
                                ui.label(title).classes('lp-step-title')
                                ui.label(desc).classes('lp-step-desc')

                with ui.element('div').classes('lp-how-visual'):
                    ui.image(DASHBOARD_MOCKUP)

    # ── PRICING ───────────────────────────────────────────────────
    with ui.element('div').classes('lp-pricing').props('id=pricing'):
        with ui.element('div').classes('lp-pricing-inner'):
            with ui.element('div').classes('lp-pricing-header'):
                ui.label('✦ Planos').classes('lp-section-tag')
                ui.label('Simples e transparente').classes('lp-section-h')
                ui.label('Sem taxas escondidas. Faça upgrade ou downgrade quando quiser.').classes('lp-section-sub')

            with ui.element('div').classes('lp-plans'):
                # Gratuito
                with ui.element('div').classes('lp-plan'):
                    ui.label('🆓 Gratuito').classes('lp-plan-name')
                    ui.label('R$ 0').classes('lp-plan-price')
                    ui.label('para sempre').classes('lp-plan-period')
                    ui.element('div').classes('lp-plan-divider')
                    for item in ['20 lançamentos/mês', '1 cartão', 'Modo Unificado', 'Consultor básico', 'Dashboard completo']:
                        with ui.element('div').classes('lp-plan-item'):
                            ui.label('✅').classes('lp-plan-check')
                            ui.label(item)
                    ui.button('Começar Grátis', on_click=lambda: ui.navigate.to('/criar-conta')).classes('lp-plan-btn outline')

                # Premium
                with ui.element('div').classes('lp-plan featured'):
                    ui.label('MAIS POPULAR').classes('lp-plan-badge')
                    ui.label('💎 Premium').classes('lp-plan-name')
                    ui.label('R$ 4,99').classes('lp-plan-price')
                    ui.label('/mês').classes('lp-plan-period')
                    ui.element('div').classes('lp-plan-divider')
                    for item in ['Lançamentos ilimitados', 'Múltiplos cartões', 'Modo Individual', 'Consultor Premium (30+)', 'Relatórios avançados', 'Suporte prioritário']:
                        with ui.element('div').classes('lp-plan-item'):
                            ui.label('✅').classes('lp-plan-check')
                            ui.label(item)
                    ui.button('Assinar Premium', on_click=lambda: ui.navigate.to('/criar-conta')).classes('lp-plan-btn solid')

    # ── CTA ───────────────────────────────────────────────────────
    with ui.element('div').classes('lp-cta'):
        with ui.element('div').classes('lp-cta-inner'):
            ui.html('<h2>Pronto para controlar suas finanças?</h2>')
            ui.label('Junte-se a milhares de usuários que já transformaram a relação com o dinheiro usando o Cartometro.').classes('lp-cta p')
            ui.button('🚀 Criar Conta Gratuita', on_click=lambda: ui.navigate.to('/criar-conta')).classes('lp-cta-btn')

    # ── FOOTER ────────────────────────────────────────────────────
    with ui.element('div').classes('lp-footer'):
        with ui.element('div').classes('lp-footer-inner'):
            with ui.element('div').classes('lp-footer-top'):
                with ui.element('div'):
                    ui.image(LOGO_BRANCA).classes('lp-footer-brand-logo')
                    ui.label('Controle Inteligente do seu Crédito. Simples, rápido e eficiente.').classes('lp-footer-tagline')
                with ui.element('div'):
                    ui.label('Produto').classes('lp-footer-col-title')
                    for lbl in ['Funcionalidades', 'Planos', 'Ver Demo']:
                        ui.label(lbl).classes('lp-footer-link')
                with ui.element('div'):
                    ui.label('Suporte').classes('lp-footer-col-title')
                    for lbl in ['Central de Ajuda', 'suporte@cartometro.app', 'FAQ']:
                        ui.label(lbl).classes('lp-footer-link')
                with ui.element('div'):
                    ui.label('Legal').classes('lp-footer-col-title')
                    for lbl in ['Termos de Uso', 'Privacidade']:
                        ui.label(lbl).classes('lp-footer-link')
            with ui.element('div').classes('lp-footer-bottom'):
                ui.label('© 2025 Cartometro. Todos os direitos reservados.').classes('lp-footer-copy')


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