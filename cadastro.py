"""Tela de Cadastro do Cartometro"""

from nicegui import ui
from db import criar_usuario
from config import LOGO_FULL_BRANCA, WORDMARK, FAVICON  # ✅ Importa de config, não de main

@ui.page('/criar-conta')
def cadastro_page():
    ui.add_head_html(f"""
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,600;14..32,700;14..32,800;14..32,900&display=swap" rel="stylesheet">
    <link rel="icon" type="image/x-icon" href="{FAVICON}">
    <style>
    *,*::before,*::after{{margin:0;padding:0;box-sizing:border-box}}
    html,body{{height:100%;font-family:'Inter',sans-serif;overflow-x:hidden}}
    :root{{--blue:#2563eb;--blue-dark:#1d4ed8;--blue-light:#eff6ff;--blue-mid:#bfdbfe}}
    
    .reg-page{{display:flex;min-height:100vh}}
    
    .reg-brand{{flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;background:linear-gradient(155deg,var(--blue-dark) 0%,var(--blue) 100%);padding:60px 52px;position:relative;overflow:hidden}}
    .reg-brand::before{{content:'';position:absolute;width:600px;height:600px;border-radius:50%;border:1px solid rgba(255,255,255,.07);top:-200px;right:-200px;pointer-events:none}}
    .reg-brand-inner{{position:relative;z-index:1;max-width:440px;text-align:center}}
    .reg-brand-logo{{height:200px;width:auto;display:block;margin:0 auto 44px}}
    .reg-brand-title{{font-size:26px;font-weight:800;color:#fff;letter-spacing:-.5px;margin-bottom:10px}}
    .reg-brand-sub{{font-size:14px;color:rgba(255,255,255,.72);line-height:1.6;margin-bottom:40px}}
    .reg-benefit{{display:flex;align-items:center;gap:12px;margin-bottom:14px;text-align:left}}
    .reg-ben-icon{{width:36px;height:36px;border-radius:10px;flex-shrink:0;background:rgba(255,255,255,.13);display:flex;align-items:center;justify-content:center;font-size:17px}}
    .reg-ben-text{{font-size:13px;font-weight:500;color:#fff;line-height:1.4}}
    
    .reg-form-side{{width:520px;flex-shrink:0;display:flex;flex-direction:column;align-items:center;justify-content:center;background:#fff;padding:52px 48px;position:relative;overflow-y:auto}}
    .reg-back{{position:absolute;top:20px;left:20px;background:#fff;border:none;padding:9px 16px;border-radius:8px;font-size:12px;color:#6b7280;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.07);font-family:inherit;z-index:10;transition:all .2s}}
    .reg-back:hover{{color:#111827;box-shadow:0 4px 12px rgba(0,0,0,.11)}}
    .reg-form-inner{{width:100%;max-width:380px}}
    .reg-wordmark{{height:36px;width:auto;display:block;margin:0 auto 28px}}
    .reg-title{{font-size:26px;font-weight:800;color:#111827;text-align:center;margin-bottom:4px}}
    .reg-subtitle{{font-size:13px;color:#9ca3af;text-align:center;margin-bottom:28px}}
    
    .reg-plans{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:24px}}
    .reg-plan-opt{{border:2px solid #e5e7eb;border-radius:12px;padding:16px 12px;text-align:center;cursor:pointer;transition:all .2s;background:#fff;position:relative}}
    .reg-plan-opt.active{{border-color:var(--blue);background:var(--blue-light);box-shadow:0 0 0 3px rgba(37,99,235,.12)}}
    .reg-plan-opt-badge{{position:absolute;top:-10px;left:50%;transform:translateX(-50%);background:var(--blue);color:#fff;font-size:10px;font-weight:700;padding:3px 12px;border-radius:100px;white-space:nowrap;display:none}}
    .reg-plan-opt.active .reg-plan-opt-badge{{display:block}}
    .reg-plan-emoji{{font-size:24px;margin-bottom:6px}}
    .reg-plan-name{{font-size:13px;font-weight:700;color:#111827;margin-bottom:4px}}
    .reg-plan-price{{font-size:19px;font-weight:900;color:var(--blue)}}
    .reg-plan-period{{font-size:11px;color:#9ca3af}}
    
    .reg-field{{margin-bottom:14px}}
    .reg-label{{font-size:13px;font-weight:600;color:#374151;margin-bottom:5px;display:block}}
    .q-field--outlined .q-field__control{{border-radius:9px!important;height:46px!important;background:#fafafa!important}}
    .q-field--outlined.q-field--focused .q-field__control{{border-color:var(--blue)!important;box-shadow:0 0 0 3px rgba(37,99,235,.12)!important}}
    
    .reg-btn{{width:100%;height:48px;background:var(--blue);color:#fff;border:none;border-radius:10px;font-size:16px;font-weight:700;cursor:pointer;font-family:inherit;transition:all .2s;margin-top:8px;box-shadow:0 2px 8px rgba(37,99,235,.3)}}
    .reg-btn:hover{{background:var(--blue-dark);transform:translateY(-1px);box-shadow:0 5px 16px rgba(37,99,235,.38)}}
    
    .reg-error{{background:#fef2f2;border-left:3px solid #ef4444;color:#ef4444;padding:11px 14px;border-radius:8px;font-size:13px;margin-bottom:14px;display:none}}
    .reg-error.show{{display:block}}
    
    .reg-footer-note{{text-align:center;margin-top:20px;font-size:13px;color:#9ca3af}}
    .txt-link{{color:var(--blue);font-weight:600;cursor:pointer;display:inline}}
    .txt-link:hover{{text-decoration:underline}}
    
    @media(max-width:900px){{
        .reg-brand{{display:none}}
        .reg-form-side{{width:100%;padding:0;flex-direction:column;align-items:stretch;justify-content:flex-start}}
        .reg-mobile-header{{display:flex!important;flex-direction:column;align-items:center;justify-content:center;background:linear-gradient(155deg,var(--blue-dark),var(--blue));padding:44px 24px 52px;position:relative}}
        .reg-mobile-header::after{{content:'';position:absolute;bottom:-24px;left:0;right:0;height:48px;background:#fff;border-radius:28px 28px 0 0}}
        .reg-mobile-logo{{height:140px;width:auto}}
        .reg-form-inner{{padding:24px 24px 40px;margin:0 auto}}
        .reg-back{{position:absolute;top:16px;right:16px;left:auto;background:rgba(255,255,255,.18);color:#fff;backdrop-filter:blur(8px);box-shadow:none;border-radius:8px}}
        .reg-back:hover{{background:rgba(255,255,255,.28);color:#fff}}
        .reg-wordmark{{display:none}}
    }}
    </style>
    """)
    
    plano_selecionado = {"plano": "gratuito"}
    planos_refs = {}
    
    with ui.element('div').classes('reg-page'):
        with ui.element('div').classes('reg-brand'):
            with ui.element('div').classes('reg-brand-inner'):
                ui.html(f'<img src="{LOGO_FULL_BRANCA}" alt="Cartometro" class="reg-brand-logo">')
                ui.label('Controle inteligente do seu crédito').classes('reg-brand-title')
                ui.label('Tudo que você precisa para dominar suas finanças em um só lugar.').classes('reg-brand-sub')
                for icon, txt in [
                    ('📊','Dashboard com KPIs em tempo real'),
                    ('🤖','Consultor financeiro com 30+ alertas'),
                    ('💳','Controle total de múltiplos cartões'),
                    ('🎯','Metas e orçamentos personalizados'),
                    ('🔔','Alertas antes de problemas acontecerem'),
                ]:
                    with ui.element('div').classes('reg-benefit'):
                        with ui.element('div').classes('reg-ben-icon'):
                            ui.label(icon)
                        ui.label(txt).classes('reg-ben-text')
        
        with ui.element('div').classes('reg-form-side'):
            ui.html(f'<div class="reg-mobile-header" style="display:none;"><img src="{LOGO_FULL_BRANCA}" alt="Cartometro" class="reg-mobile-logo"></div>')
            ui.button('← Voltar', on_click=lambda: ui.navigate.to('/')).props('no-caps').classes('reg-back')
            
            with ui.element('div').classes('reg-form-inner'):
                ui.html(f'<img src="{WORDMARK}" alt="Cartometro" class="reg-wordmark">')
                ui.label('Criar sua Conta').classes('reg-title')
                ui.label('Comece grátis, faça upgrade quando quiser').classes('reg-subtitle')
                
                with ui.element('div').classes('reg-plans'):
                    plano_free = ui.element('div').classes('reg-plan-opt active')
                    with plano_free:
                        ui.label('SELECIONADO').classes('reg-plan-opt-badge')
                        ui.label('🆓').classes('reg-plan-emoji')
                        ui.label('Gratuito').classes('reg-plan-name')
                        ui.label('R$ 0').classes('reg-plan-price')
                        ui.label('para sempre').classes('reg-plan-period')
                    plano_free.on('click', lambda: selecionar_plano('gratuito'))
                    planos_refs['gratuito'] = plano_free
                    
                    plano_premium = ui.element('div').classes('reg-plan-opt')
                    with plano_premium:
                        ui.label('SELECIONADO').classes('reg-plan-opt-badge')
                        ui.label('💎').classes('reg-plan-emoji')
                        ui.label('Premium').classes('reg-plan-name')
                        ui.label('R$ 4,99').classes('reg-plan-price')
                        ui.label('/mês').classes('reg-plan-period')
                    plano_premium.on('click', lambda: selecionar_plano('premium'))
                    planos_refs['premium'] = plano_premium
                
                def selecionar_plano(plano):
                    plano_selecionado['plano'] = plano
                    for nome, ref in planos_refs.items():
                        ref.classes('reg-plan-opt active') if nome == plano else ref.classes(remove='active')
                
                with ui.element('div').classes('reg-field'):
                    ui.label('Nome completo').classes('reg-label')
                    nome_input = ui.input(placeholder='Seu nome completo').props('outlined dense').classes('w-full')
                with ui.element('div').classes('reg-field'):
                    ui.label('Email').classes('reg-label')
                    email_input = ui.input(placeholder='seu@email.com').props('outlined dense').classes('w-full')
                with ui.element('div').classes('reg-field'):
                    ui.label('Senha').classes('reg-label')
                    senha_input = ui.input(placeholder='Mínimo 4 caracteres', password=True, password_toggle_button=True).props('outlined dense').classes('w-full')
                with ui.element('div').classes('reg-field'):
                    ui.label('Confirmar Senha').classes('reg-label')
                    confirmar_input = ui.input(placeholder='Repita a senha', password=True, password_toggle_button=True).props('outlined dense').classes('w-full')
                
                erro_label = ui.label('').classes('reg-error')
                
                def cadastrar():
                    nome = (nome_input.value or '').strip()
                    email = (email_input.value or '').strip()
                    senha = senha_input.value or ''
                    confirmar = confirmar_input.value or ''
                    erro_label.classes(remove='show')
                    if not nome or not email or not senha:
                        erro_label.classes('reg-error show'); erro_label.set_text('⚠️ Preencha todos os campos'); return
                    if senha != confirmar:
                        erro_label.classes('reg-error show'); erro_label.set_text('⚠️ Senhas não conferem'); return
                    if len(senha) < 4:
                        erro_label.classes('reg-error show'); erro_label.set_text('⚠️ Mínimo 4 caracteres'); return
                    sucesso, msg, _ = criar_usuario(nome, email, senha, plano_selecionado['plano'])
                    if sucesso:
                        plano_nome = 'Premium' if plano_selecionado['plano'] == 'premium' else 'Gratuito'
                        ui.notify(f'✅ Conta {plano_nome} criada!', type='positive', position='top', timeout=3000)
                        ui.timer(1.5, lambda: ui.navigate.to('/login'), once=True)
                    else:
                        erro_label.classes('reg-error show'); erro_label.set_text(f'❌ {msg}')
                
                ui.button('Criar Conta', on_click=cadastrar).props('no-caps').classes('reg-btn')
                
                with ui.element('div').classes('reg-footer-note'):
                    ui.label('Já tem conta? ').style('display:inline;')
                    ui.label('Fazer login').classes('txt-link').on('click', lambda: ui.navigate.to('/login'))