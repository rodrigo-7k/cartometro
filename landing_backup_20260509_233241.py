"""
Landing Page do Cartometro
Estilo Landingi - Azul #2563eb
"""

from nicegui import ui

HERO_IMG = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778379580/hero_qatkv9.png"
from config import (
    LOGO_BRANCA, LOGO_FULL_COLOR,
    PRINT_DASHBOARD, PRINT_CARTOES, PRINT_LANCAMENTOS, PRINT_RELATORIOS,
    FAVICON
)

@ui.page('/')
def landing_page():
    """Landing Page completa"""
    
    ui.add_head_html(f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700;14..32,800;14..32,900&display=swap" rel="stylesheet">
    <link rel="icon" type="image/x-icon" href="{FAVICON}">
    <style>
    *,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
    html,body{{font-family:'Inter',-apple-system,BlinkMacSystemFont,sans-serif;background:#fff;color:#111827;-webkit-font-smoothing:antialiased;overflow-x:hidden}}
    
    .cl{{width:90%;max-width:1280px;margin:0 auto}}
    
    /* ═══ NAVBAR ═══ */
    .lp-nav{{position:fixed;top:0;left:0;right:0;z-index:1000;background:rgba(255,255,255,.98);border-bottom:1px solid #e5e7eb;transition:box-shadow .25s}}
    .lp-nav.scrolled{{box-shadow:0 2px 12px rgba(0,0,0,.07)}}
    .lp-nav-inner{{width:90%;max-width:1280px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;height:72px}}
    .lp-nav-left{{display:flex;align-items:center;gap:32px}}
    .lp-nav-logo{{height:110px;width:auto;display:block}}
    .lp-nav-links{{display:flex;align-items:center;gap:4px}}
    .lp-nav-links button{{margin:0 2px!important}}
    .lp-nav-right{{display:flex;align-items:center;gap:12px}}
    .lp-nav-mob{{display:none!important;font-size:26px;background:none;border:none;cursor:pointer;color:#374151;padding:4px 8px}}
    
    /* ═══ HERO ═══ */
    .lp-hero{{width:100%;padding:0;position:relative;min-height:100vh;display:flex;align-items:center;overflow:hidden}}
    .lp-hero-bg{{position:absolute;top:0;left:0;width:100%;height:100%;z-index:0;background-size:cover;background-position:center right;background-repeat:no-repeat}}
    .lp-hero-bg::after{{content:'';position:absolute;top:0;left:0;width:55%;height:100%;background:linear-gradient(90deg,rgba(255,255,255,0.95) 0%,rgba(255,255,255,0.85) 40%,rgba(255,255,255,0.2) 80%,transparent 100%);z-index:1}}
    .lp-hero-content{{position:relative;z-index:2;width:100%;padding:120px 0 90px}}
    .lp-hero-grid{{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:center}}
    .lp-hero-tag{{display:inline-flex;align-items:center;gap:8px;background:#fff;border:1px solid #bfdbfe;color:#2563eb;font-size:13px;font-weight:600;padding:6px 16px;border-radius:100px;margin-bottom:24px}}
    .lp-hero-tag-dot{{width:6px;height:6px;background:#2563eb;border-radius:50%}}
    .lp-hero-h1{{font-size:clamp(36px,5vw,60px);font-weight:900;line-height:1.08;letter-spacing:-1.5px;color:#111827;margin-bottom:20px}}
    .lp-hero-h1 span{{color:#2563eb}}
    .lp-hero-p{{font-size:17px;color:#6b7280;line-height:1.7;margin-bottom:32px;max-width:500px}}
    .lp-hero-btns{{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:36px}}
    .lp-hero-trust{{display:flex;align-items:center;gap:20px;flex-wrap:wrap;font-size:13px;color:#9ca3af}}
    .lp-hero-trust span{{display:flex;align-items:center;gap:6px}}
    .lp-hero-img-wrap{{width:100%;border-radius:20px;overflow:hidden;box-shadow:0 28px 64px rgba(0,0,0,.18)}}
    .lp-hero-img-wrap img{{width:100%;display:block}}
    
    /* ═══ SECTIONS ═══ */
    .lp-showcase{{width:100%;padding:64px 0;background:#f8fafc;border-top:1px solid #e5e7eb;border-bottom:1px solid #e5e7eb;text-align:center}}
    .lp-showcase-label{{font-size:12px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#9ca3af;margin-bottom:24px}}
    .lp-showcase-img{{max-width:520px;height:auto;margin:0 auto;display:block}}
    
    .lp-features{{width:100%;padding:90px 0;background:#fff}}
    .lp-sec-tag{{display:inline-flex;align-items:center;background:#eff6ff;color:#2563eb;font-size:12px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;padding:5px 14px;border-radius:100px;margin-bottom:14px}}
    .lp-sec-h{{font-size:clamp(28px,3.5vw,42px);font-weight:900;letter-spacing:-.8px;color:#111827;margin-bottom:12px}}
    .lp-sec-p{{font-size:17px;color:#6b7280;line-height:1.65;max-width:560px;margin:0 auto}}
    .lp-sec-hdr{{text-align:center;margin-bottom:56px}}
    
    .lp-feat-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}}
    .lp-feat-card{{padding:30px 26px;background:#f9fafb;border:1px solid #e5e7eb;border-radius:16px;transition:all .28s}}
    .lp-feat-card:hover{{background:#fff;border-color:#bfdbfe;box-shadow:0 12px 32px rgba(37,99,235,.09);transform:translateY(-4px)}}
    .lp-feat-icon{{width:48px;height:48px;border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px;margin-bottom:18px}}
    .lp-feat-title{{font-size:17px;font-weight:700;color:#111827;margin-bottom:7px}}
    .lp-feat-desc{{font-size:14px;color:#6b7280;line-height:1.65}}
    
    .lp-prints{{width:100%;padding:90px 0;background:#f9fafb}}
    .lp-prints-grid{{display:grid;grid-template-columns:1fr 1fr;gap:36px;margin-top:56px}}
    .lp-print-img{{width:100%;height:220px;object-fit:cover;border-radius:14px;display:block;margin-bottom:18px;box-shadow:0 12px 32px rgba(0,0,0,.1)}}
    .lp-print-title{{font-size:18px;font-weight:700;color:#111827;margin-bottom:6px}}
    .lp-print-desc{{font-size:14px;color:#6b7280;line-height:1.6}}
    
    .lp-how{{width:100%;padding:90px 0;background:#fff}}
    .lp-how-grid{{display:grid;grid-template-columns:1fr 1fr;gap:72px;align-items:center;margin-top:56px}}
    .lp-steps{{display:flex;flex-direction:column;gap:28px}}
    .lp-step{{display:flex;gap:18px;align-items:flex-start}}
    .lp-step-num{{width:44px;height:44px;flex-shrink:0;border-radius:12px;background:#2563eb;color:#fff;font-size:16px;font-weight:800;display:flex;align-items:center;justify-content:center;box-shadow:0 4px 12px rgba(37,99,235,.3)}}
    .lp-step-title{{font-size:17px;font-weight:700;color:#111827;margin-bottom:4px}}
    .lp-step-desc{{font-size:14px;color:#6b7280;line-height:1.6}}
    .lp-how-img{{width:100%;border-radius:18px;box-shadow:0 20px 48px rgba(0,0,0,.12);display:block}}
    
    .lp-pricing{{width:100%;padding:90px 0;background:#f9fafb}}
    .lp-plans{{display:grid;grid-template-columns:1fr 1fr;gap:28px;max-width:860px;margin:56px auto 0}}
    .lp-plan{{border:2px solid #e5e7eb;border-radius:20px;padding:40px 36px;background:#fff;position:relative;transition:all .28s}}
    .lp-plan:hover{{box-shadow:0 12px 36px rgba(0,0,0,.08);transform:translateY(-2px)}}
    .lp-plan.feat{{border-color:#2563eb;background:linear-gradient(155deg,#eff6ff 0%,#fff 60%);box-shadow:0 16px 48px rgba(37,99,235,.12)}}
    .lp-plan-badge{{position:absolute;top:-14px;left:50%;transform:translateX(-50%);background:#2563eb;color:#fff;font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;padding:5px 20px;border-radius:100px;white-space:nowrap}}
    .lp-plan-name{{font-size:22px;font-weight:800;color:#111827;text-align:center;margin-bottom:6px}}
    .lp-plan-desc{{font-size:13px;color:#6b7280;text-align:center;margin-bottom:20px}}
    .lp-plan-price{{font-size:54px;font-weight:900;color:#2563eb;line-height:1;text-align:center}}
    .lp-plan-period{{font-size:13px;color:#9ca3af;text-align:center;margin-bottom:24px}}
    .lp-plan-divider{{height:1px;background:#e5e7eb;margin:20px 0}}
    .lp-plan-items{{display:flex;flex-direction:column;gap:11px;margin-bottom:28px}}
    .lp-plan-item{{display:flex;align-items:flex-start;gap:10px;font-size:14px;color:#374151}}
    .lp-plan-check{{color:#2563eb;font-size:16px;flex-shrink:0;margin-top:1px}}
    
    /* ═══ FAQ ═══ */
    .lp-faq{{width:100%;padding:90px 0;background:#fff}}
    .lp-faq-list{{max-width:760px;margin:56px auto 0}}
    .lp-faq-item{{border-top:1px solid #e5e7eb;padding:20px 0;cursor:pointer}}
    .lp-faq-item:last-child{{border-bottom:1px solid #e5e7eb}}
    .lp-faq-q{{display:flex;justify-content:space-between;align-items:center;gap:16px;user-select:none}}
    .lp-faq-q-text{{font-size:16px;font-weight:600;color:#111827;flex:1}}
    .lp-faq-icon{{width:28px;height:28px;border-radius:8px;flex-shrink:0;background:#eff6ff;color:#2563eb;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:700;transition:transform .3s ease;line-height:1}}
    .lp-faq-a{{font-size:14px;color:#6b7280;line-height:1.7;max-height:0;overflow:hidden;transition:max-height .4s ease,padding .3s ease}}
    .lp-faq-item.active .lp-faq-a{{max-height:500px;padding-top:14px}}
    .lp-faq-item.active .lp-faq-icon{{transform:rotate(45deg)}}
    
    .lp-cta{{width:100%;padding:90px 0;background:linear-gradient(135deg,#1d4ed8 0%,#2563eb 100%);text-align:center}}
    .lp-cta h2{{font-size:clamp(28px,4vw,42px);font-weight:900;color:#fff;letter-spacing:-.8px;margin-bottom:16px}}
    .lp-cta p{{font-size:17px;color:rgba(255,255,255,.88);line-height:1.7;margin-bottom:36px;max-width:560px;margin-left:auto;margin-right:auto}}
    
    .lp-footer{{width:100%;background:#0a0f1e;padding:56px 0 0}}
    .lp-footer-top{{display:grid;grid-template-columns:2.2fr 1fr 1fr 1fr;gap:40px;padding-bottom:40px;border-bottom:1px solid rgba(255,255,255,.07)}}
    .lp-footer-logo{{height:72px;width:auto;display:block;margin-bottom:14px}}
    .lp-footer-tagline{{font-size:13px;color:#6b7280;line-height:1.7;max-width:240px}}
    .lp-footer-col-title{{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:#d1d5db;margin-bottom:16px}}
    .lp-footer-col-link{{display:block;font-size:13px;color:#6b7280;margin-bottom:10px;cursor:pointer;transition:color .2s;text-decoration:none}}
    .lp-footer-col-link:hover{{color:#f9fafb}}
    .lp-footer-bottom{{display:flex;align-items:center;justify-content:space-between;padding:18px 0;flex-wrap:wrap;gap:12px}}
    .lp-footer-copy{{font-size:12px;color:#4b5563}}
    
    @media(max-width:1024px){{.lp-hero-grid{{grid-template-columns:1fr;gap:40px}}.lp-hero-img-wrap{{order:-1;max-width:550px;margin:0 auto}}.lp-feat-grid{{grid-template-columns:repeat(2,1fr)}}.lp-prints-grid{{grid-template-columns:1fr 1fr}}.lp-how-grid{{grid-template-columns:1fr;gap:40px}}.lp-footer-top{{grid-template-columns:1fr 1fr;gap:28px}}}}
    @media(max-width:768px){{.lp-nav-links{{display:none!important}}.lp-nav-right{{display:none!important}}.lp-nav-mob{{display:block!important}}.lp-hero{{padding:120px 0 60px}}.lp-hero-grid{{grid-template-columns:1fr;gap:32px}}.lp-hero-h1{{font-size:32px}}.lp-hero-p{{font-size:15px}}.lp-hero-btns{{flex-direction:column;align-items:stretch}}.lp-feat-grid{{grid-template-columns:1fr}}.lp-prints-grid{{grid-template-columns:1fr}}.lp-how-grid{{grid-template-columns:1fr;gap:32px}}.lp-plans{{grid-template-columns:1fr;max-width:420px}}.lp-footer-top{{grid-template-columns:1fr 1fr;gap:24px}}.lp-footer-bottom{{flex-direction:column;text-align:center}}.cl{{width:94%}}}}
    @media(max-width:480px){{.lp-footer-top{{grid-template-columns:1fr}}.lp-plans{{max-width:100%}}}}
    </style>
    
    <script>
    window.addEventListener('scroll',function(){{var n=document.querySelector('.lp-nav');if(n)n.classList.toggle('scrolled',window.scrollY>24)}});
    
    // FAQ Toggle - Versão corrigida
    document.addEventListener('DOMContentLoaded',function(){{
        setTimeout(function(){{
            document.querySelectorAll('.lp-faq-q').forEach(function(q){{
                q.addEventListener('click',function(){{
                    var item=this.closest('.lp-faq-item');
                    var wasActive=item.classList.contains('active');
                    // Fecha todos
                    document.querySelectorAll('.lp-faq-item').forEach(function(i){{i.classList.remove('active')}});
                    // Abre o clicado (se não estava ativo)
                    if(!wasActive){{item.classList.add('active')}}
                }});
            }});
        }},500);
    }});
    
    function scrollTo(id){{document.getElementById(id).scrollIntoView({{behavior:'smooth'}})}}
    </script>
    """)
    
    # ═══ NAVBAR ═══
    with ui.element('nav').classes('lp-nav'):
        with ui.element('div').classes('lp-nav-inner'):
            with ui.element('div').classes('lp-nav-left'):
                ui.html(f'<a href="/"><img src="{LOGO_FULL_COLOR}" alt="Cartometro" class="lp-nav-logo"></a>')
                with ui.element('div').classes('lp-nav-links'):
                    links = [('Funcionalidades','features-section'),('App','app-showcase'),('Como funciona','how-section'),('Planos','pricing-section'),('FAQ','faq-section')]
                    for i, (label, anchor) in enumerate(links):
                        ui.button(label, on_click=lambda a=anchor: ui.run_javascript(f'scrollTo("{a}")')).props('flat dense no-caps').style('color:#2563eb!important;font-weight:500;font-size:13.5px;background:transparent!important;box-shadow:none!important;margin:0 4px!important;padding:8px 12px!important')
            
            with ui.element('div').classes('lp-nav-right'):
                ui.button('Entrar', on_click=lambda: ui.navigate.to('/login')).props('flat dense no-caps').style('color:#2563eb!important;font-weight:600;font-size:13.5px;background:transparent!important;box-shadow:none!important')
                ui.button('Iniciar teste grátis', on_click=lambda: ui.navigate.to('/criar-conta')).props('dense no-caps').style('background:#2563eb!important;color:#fff!important;font-weight:600;font-size:13.5px;padding:9px 20px!important;border-radius:7px;box-shadow:0 1px 3px rgba(37,99,235,.3)')
            
            ui.button('☰').props('flat dense').style('font-size:24px;color:#374151').classes('lp-nav-mob')
    
    # ═══ HERO ═══
    with ui.element('div').classes('lp-hero'):
        # Imagem de fundo ocupando toda area
        ui.html(f'<div class="lp-hero-bg" style="background-image:url({HERO_IMG})"></div>')
        
        with ui.element('div').classes('lp-hero-content'):
            with ui.element('div').classes('cl'):
                with ui.element('div').classes('lp-hero-grid'):
                    with ui.element('div'):
                        with ui.element('div').classes('lp-hero-tag'):
                            ui.element('div').classes('lp-hero-tag-dot')
                            ui.label('30+ alertas inteligentes no Consultor')
                        ui.html('<h1 class="lp-hero-h1">Domine suas finanças com <span>inteligencia</span></h1>')
                        ui.label('Controle total dos seus cartoes de credito, gastos organizados por categoria e alertas personalizados para voce nunca perder o controle.').classes('lp-hero-p')
                        with ui.element('div').classes('lp-hero-btns'):
                            ui.button('Comecar Agora — Gratis', on_click=lambda: ui.navigate.to('/criar-conta')).props('no-caps').style('background:#2563eb!important;color:#fff!important;font-weight:600;font-size:15px;padding:14px 28px!important;border-radius:10px;box-shadow:0 4px 14px rgba(37,99,235,.32)')
                            ui.button('Fazer Login', on_click=lambda: ui.navigate.to('/login')).props('no-caps').style('background:#2563eb!important;color:#fff!important;font-weight:600;font-size:15px;padding:14px 28px!important;border-radius:10px;box-shadow:0 4px 14px rgba(37,99,235,.32)')
                        with ui.element('div').classes('lp-hero-trust'):
                            for txt in ['Gratis para sempre', 'Sem cartao de credito', '2 minutos para comecar']:
                                with ui.element('span'):
                                    ui.label('✓').style('color:#2563eb!important;font-size:15px')
                                    ui.label(txt)
                    # Lado direito vazio (a imagem de fundo aparece)
                    with ui.element('div'):
                        pass
    
    # ═══ LOGO SHOWCASE ═══
    with ui.element('div').classes('lp-showcase'):
        ui.label('Uma plataforma, controle total').classes('lp-showcase-label')
        ui.html(f'<img src="{LOGO_FULL_COLOR}" alt="Cartometro" class="lp-showcase-img" style="max-width:520px;height:auto;margin:0 auto;display:block">')
    
    # ═══ FEATURES ═══
    with ui.element('div').classes('lp-features').props('id=features-section'):
        with ui.element('div').classes('cl'):
            with ui.element('div').classes('lp-sec-hdr'):
                ui.label('Funcionalidades').classes('lp-sec-tag')
                ui.label('Tudo que você precisa').classes('lp-sec-h')
                ui.label('Ferramentas completas para controle financeiro, do básico ao avançado.').classes('lp-sec-p')
            with ui.element('div').classes('lp-feat-grid'):
                for icon, color, title, desc in [
                    ('📊','#2563eb','Dashboard Inteligente','Visualize KPIs em tempo real: limite usado, gastos por categoria e tendências mensais.'),
                    ('💳','#7c3aed','Múltiplos Cartões','Gerencie cada cartão individualmente ou de forma unificada, com limites e ciclos distintos.'),
                    ('🤖','#10b981','Consultor Financeiro','30+ alertas que analisam seus padrões de consumo antes que problemas aconteçam.'),
                    ('📅','#f59e0b','Ciclo de Fatura','Acompanhe gastos pelo ciclo real da fatura ou pelo mês calendário, como preferir.'),
                    ('🔁','#ec4899','Gastos Recorrentes','Cadastre assinaturas e fixos que entram automaticamente todo mês.'),
                    ('🎯','#6366f1','Metas e Limites','Defina orçamentos por categoria e receba alertas ao se aproximar do limite.'),
                ]:
                    with ui.element('div').classes('lp-feat-card'):
                        with ui.element('div').classes('lp-feat-icon').style(f'background:{color}18;'):
                            ui.label(icon)
                        ui.label(title).classes('lp-feat-title')
                        ui.label(desc).classes('lp-feat-desc')
    
    # ═══ APP PRINTS ═══
    with ui.element('div').classes('lp-prints').props('id=app-showcase'):
        with ui.element('div').classes('cl'):
            with ui.element('div').classes('lp-sec-hdr'):
                ui.label('Conheça o App').classes('lp-sec-tag')
                ui.label('Veja como funciona na prática').classes('lp-sec-h')
                ui.label('Interface limpa e intuitiva para você ter controle total.').classes('lp-sec-p')
            with ui.element('div').classes('lp-prints-grid'):
                for img, title, desc in [
                    (PRINT_DASHBOARD if 'PRINT_DASHBOARD' in locals() else HERO_IMG,'Dashboard Completo','Visão geral de todos os seus cartões e gastos em um único lugar.'),
                    (PRINT_LANCAMENTOS,'Lançamentos','Registre cada compra em segundos. Categorize e acompanhe em tempo real.'),
                    (PRINT_CARTOES,'Gestão de Cartões','Múltiplos cartões com limites e ciclos. Visão individual ou unificada.'),
                    (PRINT_RELATORIOS,'Relatórios e Insights','Análises inteligentes. O consultor identifica padrões e sugere economias.'),
                ]:
                    with ui.element('div'):
                        ui.html(f'<img src="{img}" alt="{title}" class="lp-print-img" style="width:100%;height:220px;object-fit:cover;border-radius:14px;display:block;margin-bottom:18px;box-shadow:0 12px 32px rgba(0,0,0,.1)">')
                        ui.label(title).classes('lp-print-title')
                        ui.label(desc).classes('lp-print-desc')
    
    # ═══ HOW IT WORKS ═══
    with ui.element('div').classes('lp-how').props('id=how-section'):
        with ui.element('div').classes('cl'):
            with ui.element('div').classes('lp-sec-hdr'):
                ui.label('Como Funciona').classes('lp-sec-tag')
                ui.label('Comece em menos de 2 minutos').classes('lp-sec-h')
                ui.label('Quatro passos simples para transformar sua relação com o dinheiro.').classes('lp-sec-p')
            with ui.element('div').classes('lp-how-grid'):
                with ui.element('div').classes('lp-steps'):
                    for num, title, desc in [
                        ('1','Crie sua conta gratuita','Cadastro rápido, sem necessidade de cartão de crédito.'),
                        ('2','Adicione seus cartões','Com limites, bandeiras e datas de vencimento.'),
                        ('3','Registre seus gastos','Manual ou via importação de extrato. Simples e rápido.'),
                        ('4','Receba insights','O consultor analisa seus dados e envia alertas.'),
                    ]:
                        with ui.element('div').classes('lp-step'):
                            ui.label(num).classes('lp-step-num')
                            with ui.element('div'):
                                ui.label(title).classes('lp-step-title')
                                ui.label(desc).classes('lp-step-desc')
                ui.html(f'<img src="{PRINT_RELATORIOS}" alt="Como funciona" class="lp-how-img" style="width:100%;border-radius:18px;box-shadow:0 20px 48px rgba(0,0,0,.12);display:block">')
    
    # ═══ PRICING ═══
    with ui.element('div').classes('lp-pricing').props('id=pricing-section'):
        with ui.element('div').classes('cl'):
            with ui.element('div').classes('lp-sec-hdr'):
                ui.label('Planos').classes('lp-sec-tag')
                ui.label('Simples e transparente').classes('lp-sec-h')
                ui.label('Sem taxas escondidas. Faça upgrade ou downgrade quando quiser.').classes('lp-sec-p')
            with ui.element('div').classes('lp-plans'):
                with ui.element('div').classes('lp-plan'):
                    ui.label('🆓 Gratuito').classes('lp-plan-name')
                    ui.label('Para quem está começando').classes('lp-plan-desc')
                    ui.label('R$ 0').classes('lp-plan-price')
                    ui.label('para sempre').classes('lp-plan-period')
                    ui.element('div').classes('lp-plan-divider')
                    with ui.element('div').classes('lp-plan-items'):
                        for f in ['20 lançamentos por mês','1 cartão de crédito','Modo Unificado','Consultor básico','Dashboard completo','Exportação de dados']:
                            with ui.element('div').classes('lp-plan-item'):
                                ui.label('✓').classes('lp-plan-check')
                                ui.label(f)
                    ui.button('Criar conta gratuita', on_click=lambda: ui.navigate.to('/criar-conta')).props('no-caps').style('width:100%;padding:14px;border-radius:10px;font-size:15px;font-weight:700;background:#2563eb!important;color:#fff!important;box-shadow:0 4px 14px rgba(37,99,235,.32)')
                
                with ui.element('div').classes('lp-plan feat'):
                    ui.label('MAIS POPULAR').classes('lp-plan-badge')
                    ui.label('💎 Premium').classes('lp-plan-name')
                    ui.label('Para quem quer controle total').classes('lp-plan-desc')
                    ui.label('R$ 4,99').classes('lp-plan-price')
                    ui.label('/mês').classes('lp-plan-period')
                    ui.element('div').classes('lp-plan-divider')
                    with ui.element('div').classes('lp-plan-items'):
                        for f in ['Lançamentos ilimitados','Múltiplos cartões','Modo Individual','Consultor Premium (30+)','Relatórios avançados','Suporte prioritário']:
                            with ui.element('div').classes('lp-plan-item'):
                                ui.label('✓').classes('lp-plan-check')
                                ui.label(f)
                    ui.button('Assinar Premium', on_click=lambda: ui.navigate.to('/criar-conta')).props('no-caps').style('width:100%;padding:14px;border-radius:10px;font-size:15px;font-weight:700;background:#2563eb!important;color:#fff!important;box-shadow:0 4px 14px rgba(37,99,235,.32)')
    
    # ═══ FAQ ═══
    with ui.element('div').classes('lp-faq').props('id=faq-section'):
        with ui.element('div').classes('cl'):
            with ui.element('div').classes('lp-sec-hdr'):
                ui.label('Dúvidas Frequentes').classes('lp-sec-tag')
                ui.label('Perguntas Frequentes').classes('lp-sec-h')
                ui.label('Tudo que você precisa saber antes de começar.').classes('lp-sec-p')
            
            with ui.element('div').classes('lp-faq-list'):
                faqs = [
                    ('O plano gratuito tem limite de tempo?','Não. O plano gratuito é para sempre. Você pode usar o Cartometro gratuitamente sem prazo de expiração. O upgrade para o Premium é opcional e pode ser feito a qualquer momento nas configurações da sua conta.'),
                    ('Posso cancelar o Premium quando quiser?','Sim, sem burocracia. Você pode cancelar a qualquer momento diretamente nas configurações. Não há fidelidade, multa ou taxa de cancelamento. Seu plano volta para o Gratuito imediatamente.'),
                    ('Meus dados financeiros são seguros?','Sim, totalmente. Seus dados são armazenados com criptografia e nunca são compartilhados com terceiros. Você tem controle total sobre suas informações e pode excluí-las a qualquer momento.'),
                    ('O Cartometro conecta direto ao banco?','Ainda não. Os lançamentos são registrados manualmente ou via importação de extrato. Isso garante mais privacidade e controle sobre seus dados.'),
                    ('Posso usar em mais de um dispositivo?','Sim. O Cartometro é 100% web, acessível em qualquer navegador: computador, tablet ou celular. Seus dados sincronizam automaticamente.'),
                    ('O que é o Modo Unificado e Individual?','No Modo Unificado, todos os cartões são vistos como um só, com limite combinado. No Modo Individual (Premium), cada cartão tem controle separado com limites e ciclos de fatura independentes.'),
                ]
                for q, a in faqs:
                    ui.html(f'''
                    <div class="lp-faq-item">
                        <div class="lp-faq-q">
                            <span class="lp-faq-q-text">{q}</span>
                            <span class="lp-faq-icon">+</span>
                        </div>
                        <div class="lp-faq-a">{a}</div>
                    </div>
                    ''')
    
    # ═══ CTA ═══
    with ui.element('div').classes('lp-cta'):
        with ui.element('div').classes('cl'):
            ui.html('<h2>Pronto para controlar suas finanças?</h2>')
            ui.html('<p>Junte-se a milhares de pessoas que já transformaram sua relação com o dinheiro usando o Cartometro. Grátis para começar.</p>')
            ui.button('🚀 Criar Conta Gratuita', on_click=lambda: ui.navigate.to('/criar-conta')).props('no-caps').style('background:#fff!important;color:#2563eb!important;font-weight:700;font-size:16px;padding:17px 40px;border-radius:12px;box-shadow:0 8px 28px rgba(0,0,0,.2)')
    
    # ═══ FOOTER ═══
    with ui.element('div').classes('lp-footer'):
        with ui.element('div').classes('cl'):
            with ui.element('div').classes('lp-footer-top'):
                with ui.element('div'):
                    ui.html(f'<img src="{LOGO_BRANCA}" alt="Cartometro" class="lp-footer-logo" style="height:72px;width:auto;display:block;margin-bottom:14px">')
                    ui.label('Controle Inteligente do seu Crédito.').classes('lp-footer-tagline')
                for col_title, col_links in [
                    ('Produto',['Funcionalidades','App','Como Funciona','Planos']),
                    ('Suporte',['Central de Ajuda','suporte@cartometro.app','FAQ']),
                    ('Legal',['Termos de Uso','Privacidade']),
                ]:
                    with ui.element('div'):
                        ui.label(col_title).classes('lp-footer-col-title')
                        for link in col_links:
                            ui.label(link).classes('lp-footer-col-link')
            with ui.element('div').classes('lp-footer-bottom'):
                ui.label('© 2025 Cartometro. Todos os direitos reservados.').classes('lp-footer-copy')