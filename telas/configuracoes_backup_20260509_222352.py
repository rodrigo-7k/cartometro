"""
Tela de Configurações - Limites, Tema, Gastos Fixos, Cartões, Perfil e Sobre
"""

from nicegui import ui
from config import CARTOES_POPULARES, BANDEIRAS
from db import (
    get_usuario_logado_email,
    carregar,
    salvar_json,
    buscar_usuario_por_email,
    salvar_usuarios,
    carregar_usuarios,
    get_plano_usuario,
    PLANOS
)
from config_service import config_service
from constantes import CATEGORIAS_PADRAO
from datetime import datetime
import json
import os
import hashlib


LOGO_COMPLETA = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845630/logo_full_branca_wlx97y.png"


AVATARES = [
    "🐶", "🐱", "🐷", "🦆",
    "🐻", "🦁", "👩🏻‍💻", "👨🏻‍💻",
    "👩🏻", "👨🏻", "👩🏻‍🦳", "👨🏻‍🦳",
]

CORES_TEMA = [
    {"nome": "Azul", "cor": "#3b82f6", "escura": "#1e40af"},
    {"nome": "Verde", "cor": "#10b981", "escura": "#065f46"},
    {"nome": "Roxo", "cor": "#8b5cf6", "escura": "#5b21b6"},
    {"nome": "Rosa", "cor": "#ec4899", "escura": "#be185d"},
    {"nome": "Laranja", "cor": "#f97316", "escura": "#c2410c"},
    {"nome": "Ciano", "cor": "#06b6d4", "escura": "#0e7490"},
    {"nome": "Vermelho", "cor": "#ef4444", "escura": "#b91c1c"},
    {"nome": "Âmbar", "cor": "#d97706", "escura": "#92400e"},
]


CARTOES_POPULARES = [
    {"nome": "Nubank",         "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101451/01_NUBANK_qckg36.png",        "bandeira": "Mastercard", "cor": "#8b5cf6"},
    {"nome": "Banco do Brasil","img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101452/02_BANCO_DO_BRASIL_in4yxr.png", "bandeira": "Visa",       "cor": "#f59e0b"},
    {"nome": "Caixa",          "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101452/03_CAIXA_zhrs2q.png",          "bandeira": "Visa",       "cor": "#1d4ed8"},
    {"nome": "Itaú",           "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101453/04_ITAU_bcc9sw.png",           "bandeira": "Mastercard", "cor": "#f59e0b"},
    {"nome": "Bradesco",       "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101453/05_BRADESCO_he7iod.png",       "bandeira": "Visa",       "cor": "#ef4444"},
    {"nome": "Santander",      "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101454/06_SANTANDER_ew1ogg.png",      "bandeira": "Visa",       "cor": "#dc2626"},
    {"nome": "Mercado Pago",   "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101447/07_MERCADO_PAGO_o7w6vl.png",   "bandeira": "Mastercard", "cor": "#3b82f6"},
    {"nome": "Inter",          "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101447/08_INTER_a1dcn6.png",          "bandeira": "Mastercard", "cor": "#f97316"},
    {"nome": "Banco PAN",      "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101447/09_BANCO_PAN_hnrkff.png",      "bandeira": "Mastercard", "cor": "#2563eb"},
    {"nome": "PicPay",         "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101447/10_PICPAY_qibpgs.png",         "bandeira": "Mastercard", "cor": "#10b981"},
    {"nome": "Sicoob",         "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101447/11_SICOOB_madwy1.png",         "bandeira": "Mastercard", "cor": "#22c55e"},
    {"nome": "Banco Original", "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101447/12_BANCO_ORIGINAL_zxgynu.png", "bandeira": "Mastercard", "cor": "#16a34a"},
    {"nome": "Neon",           "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101449/15_NEON_lc38mq.png",           "bandeira": "Visa",       "cor": "#ea580c"},
    {"nome": "Digio",          "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101449/16_DIGIO_yvcjic.png",          "bandeira": "Visa",       "cor": "#a855f7"},
    {"nome": "XP Investimentos","img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101450/17_XP_INVESTIMENTOS_paxuws.png","bandeira": "Visa",    "cor": "#374151"},
    {"nome": "BTG Pactual",    "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101451/20_BTG_PACTUAL_q7gcub.png",    "bandeira": "Mastercard", "cor": "#2563eb"},
    {"nome": "C6 Bank",        "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111545/08_C6_BANK_uhcgrc.png",        "bandeira": "Mastercard", "cor": "#1f2937"},
    {"nome": "Next",           "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111545/09_NEXT_hroswa.png",           "bandeira": "Visa",       "cor": "#22c55e"},
    {"nome": "Porto Seguro",   "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111545/10_PORTO_SEGURO_enw885.png",   "bandeira": "Visa",       "cor": "#1e40af"},
    {"nome": "Azul",           "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111545/11_AZUL_uodkke.png",           "bandeira": "Visa",       "cor": "#3b82f6"},
    {"nome": "LATAM Pass",     "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111546/12_LATAM_PASS_x8isgn.png",     "bandeira": "Mastercard", "cor": "#dc2626"},
]

BANDEIRAS = [
    {"nome": "Visa",            "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111544/01_VISA_r0gbp1.png"},
    {"nome": "Mastercard",      "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111544/02_MASTERCARD_ofek0k.png"},
    {"nome": "Elo",             "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111544/03_ELO_d0gn8c.png"},
    {"nome": "American Express","img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111544/04_AMERICAN_EXPRESS_yn7ffw.png"},
    {"nome": "Hipercard",       "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111544/05_HIPERCARD_y0kuh1.png"},
    {"nome": "Diners",          "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111544/06_DINERS_CLUB_iewgua.png"},
    {"nome": "Discover",        "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111545/07_DISCOVER_g1xoiv.png"},
]

CUSTOM_CSS = """
<style>
* { box-sizing: border-box !important; }
.config-tela { width: 100% !important; height: 100vh !important; display: flex !important; flex-direction: column !important; background: #f3f4f6 !important; overflow: hidden !important; padding: 0 !important; margin: 0 !important; }
.config-header { flex-shrink: 0 !important; width: 100% !important; }
.config-scroll { flex: 1 !important; overflow-y: auto !important; overflow-x: hidden !important; padding: 8px 8px 20px 8px !important; width: 100% !important; }
.config-scroll::-webkit-scrollbar { width: 4px; }
.config-scroll::-webkit-scrollbar-track { background: #e5e7eb; }
.config-scroll::-webkit-scrollbar-thumb { background: #9ca3af; border-radius: 4px; }
.tabs-container { background: white !important; border-bottom: 1px solid #e5e7eb !important; padding: 2px 4px !important; display: flex !important; gap: 1px !important; overflow-x: auto !important; flex-shrink: 0 !important; scrollbar-width: none !important; -webkit-overflow-scrolling: touch !important; }
.tabs-container::-webkit-scrollbar { display: none !important; }
.tab-btn { padding: 8px 10px !important; font-size: 11px !important; font-weight: 500 !important; border-radius: 8px 8px 0 0 !important; border: none !important; background: transparent !important; color: #6b7280 !important; cursor: pointer !important; transition: all 0.15s ease !important; white-space: nowrap !important; flex-shrink: 0 !important; min-width: fit-content !important; display: flex !important; align-items: center !important; gap: 3px !important; }
.tab-btn:hover { color: #374151 !important; background: #f9fafb !important; }
.config-card { background: white !important; border-radius: 12px !important; padding: 16px !important; margin: 0 0 12px 0 !important; box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important; width: 100% !important; }
.campo-label { font-size: 12px; font-weight: 600; color: #374151; margin-bottom: 4px; }
.dica-card { border-radius: 8px !important; padding: 10px 12px !important; margin-bottom: 12px !important; }
.plano-badge { display: inline-flex !important; align-items: center !important; gap: 4px !important; padding: 3px 10px !important; border-radius: 12px !important; font-size: 10px !important; font-weight: 600 !important; }
.cores-grid { display: grid !important; grid-template-columns: repeat(4, 1fr) !important; gap: 10px !important; width: 100% !important; }
.cor-item { display: flex !important; flex-direction: column !important; align-items: center !important; gap: 6px !important; cursor: pointer !important; padding: 4px !important; }
.cor-circle { width: 48px !important; height: 48px !important; border-radius: 50% !important; transition: all 0.2s ease !important; border: 3px solid transparent !important; cursor: pointer !important; }
.cor-circle:hover { transform: scale(1.12) !important; }
.fixo-card { width: 100% !important; padding: 12px !important; background: #faf5ff !important; border-radius: 8px !important; margin-bottom: 8px !important; border: 1px solid #e9d5ff !important; }
.cartao-card { background: #f9fafb !important; border-radius: 10px !important; padding: 12px !important; margin-bottom: 8px !important; border: 1px solid #f3f4f6 !important; width: 100% !important; }
.sobre-logo-container { display: flex !important; justify-content: center !important; align-items: center !important; padding: 32px 20px !important; background: linear-gradient(135deg, #f8fafc, #f0f5ff) !important; border-radius: 16px !important; margin-bottom: 16px !important; }
.sobre-logo { width: 200px !important; height: auto !important; filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1)) !important; }
.sobre-info-item { background: white !important; border-radius: 10px !important; padding: 14px 16px !important; margin-bottom: 10px !important; border-left: 3px solid var(--cor-primaria) !important; }
.sobre-info-label { font-size: 10px !important; font-weight: 600 !important; color: #9ca3af !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; margin-bottom: 4px !important; }
.sobre-info-value { font-size: 14px !important; font-weight: 500 !important; color: #1f2937 !important; }
.sobre-badge { display: inline-flex !important; align-items: center !important; gap: 6px !important; padding: 4px 12px !important; border-radius: 20px !important; font-size: 12px !important; font-weight: 600 !important; color: white !important; }
.sobre-func-item { display: flex !important; align-items: center !important; gap: 8px !important; padding: 4px 0 !important; }
.perfil-avatar { width: 80px !important; height: 80px !important; border-radius: 50% !important; display: flex !important; align-items: center !important; justify-content: center !important; font-size: 40px !important; margin: 0 auto 16px auto !important; }
.btn-sm { padding: 6px 12px !important; font-size: 11px !important; border-radius: 6px !important; min-height: 30px !important; }
.q-field--outlined.q-field--focused .q-field__control:before { border-color: var(--cor-primaria) !important; }
.q-field--outlined.q-field--focused .q-field__control:after { border-color: var(--cor-primaria) !important; }
.q-field--focused .q-field__control { border-color: transparent !important; }
.q-field--focused .q-field__label { color: #374151 !important; }
.q-field--focused .q-field__native { color: #111827 !important; }
.q-item.q-manual-focusable--focused { background: var(--cor-primaria) !important; color: white !important; }
.banco-img { width: 30% !important; max-width: 72px !important; height: 44px !important; object-fit: contain !important; border-radius: 6px !important; border: 1px solid #e5e7eb !important; padding: 3px !important; flex-shrink: 0 !important; }
.banco-select { flex: 1 !important; min-width: 0 !important; width: 100% !important; }
.banco-row { width: 100% !important; display: flex !important; align-items: center !important; gap: 12px !important; }
.bandeira-img { width: 44px !important; height: 26px !important; object-fit: fill !important; background: white !important; padding: 2px !important; border-radius: 4px !important; flex-shrink: 0 !important; }
.bandeira-select { flex: 1 !important; min-width: 0 !important; width: 100% !important; }
.bandeira-row { width: 100% !important; display: flex !important; align-items: center !important; gap: 12px !important; }
</style>
"""


def pode_usar_modo_individual(email):
    plano = get_plano_usuario(email) if email else 'gratuito'
    return plano in ('premium', 'admin')


def atualizar_config_local(**kwargs):
    email = get_usuario_logado_email()
    if not email:
        return
    arquivo = os.path.join('data', f"{email.replace('@','_').replace('.','_').lower()}.json")
    dados_usuario = carregar(email) if email else {}
    if 'config' not in dados_usuario:
        dados_usuario['config'] = {}
    dados_usuario['config'].update(kwargs)
    salvar_json(arquivo, dados_usuario)


def tela_configuracoes(container, dialog_pai=None):
    
    container.clear()
    container.classes('p-0 m-0')
    container.style('padding: 0 !important; margin: 0 !important; width: 100% !important; height: 100% !important;')
    
    ui.add_head_html(CUSTOM_CSS)
    
    cor_primaria = config_service.get_primary_color()
    cor_escura = config_service.get_primary_dark()
    
    ui.add_head_html(f'<style>:root {{ --cor-primaria: {cor_primaria}; }}</style>')
    
    aba_ativa = {"atual": "limites"}
    email = get_usuario_logado_email()
    dados = carregar(email) if email else {}
    tab_content = None
    
    email_logado = get_usuario_logado_email()
    usuario_info = buscar_usuario_por_email(email_logado) if email_logado else None
    plano_atual = usuario_info.get('plano', 'gratuito') if usuario_info else 'gratuito'
    plano_nome = PLANOS.get(plano_atual, {}).get('nome', 'Gratuito')
    
    def carregar_dados():
        nonlocal dados
        email = get_usuario_logado_email()
        dados = carregar(email) if email else {}
    
    def recarregar_principal():
        if dialog_pai is not None:
            dialog_pai.close()
        else:
            container.clear()
        ui.run_javascript('location.reload()')
    
    def render_limites():
        config = dados.get("config", {})
        modo_atual = config.get("modo_cartao", "Unificado")
        pode_individual = pode_usar_modo_individual(get_usuario_logado_email()) if get_usuario_logado_email() else False
        
        with ui.card().classes('config-card'):
            with ui.row().classes('items-center gap-2 mb-3'):
                ui.icon('tune').classes('text-lg').style(f'color: {cor_primaria} !important;')
                ui.label("Configuração do Cartão").classes('text-base font-bold')
            
            with ui.card().classes('dica-card').style(f'background: {cor_primaria}08; border-left: 3px solid {cor_primaria};'):
                with ui.row().classes('items-start gap-2'):
                    ui.icon('info').classes('text-sm mt-0.5').style(f'color: {cor_primaria} !important;')
                    with ui.column().classes('gap-1'):
                        ui.label("💡 Como funciona").classes('text-xs font-semibold').style(f'color: {cor_primaria} !important;')
                        if not pode_individual:
                            ui.label("No plano Gratuito você usa o modo Unificado. Para usar múltiplos cartões, faça upgrade para Premium!").classes('text-[11px] text-gray-600')
                        else:
                            ui.label("Escolha o modo de controle. No Unificado, limites gerais. No Individual, cada cartão tem seus limites.").classes('text-[11px] text-gray-600')
            
            with ui.column().classes('w-full gap-1 mb-4'):
                ui.label("💳 Modo de Controle").classes('campo-label')
                
                if not pode_individual:
                    modo_cartao = ui.select(options=["Unificado"], label="Modo (Premium para Individual)", value="Unificado").props('outlined dense').classes('w-full')
                    with ui.card().classes('dica-card mt-2').style('background: #fef3c7; border: 1px solid #f59e0b;'):
                        with ui.row().classes('items-start gap-2'):
                            ui.icon('lock').classes('text-sm mt-0.5').style('color: #f59e0b !important;')
                            with ui.column().classes('gap-1'):
                                ui.label("🔒 Modo Individual é Premium").classes('text-xs font-semibold text-yellow-700')
                                ui.label("Faça upgrade para gerenciar múltiplos cartões.").classes('text-[10px] text-yellow-600')
                else:
                    modo_cartao = ui.select(options=["Unificado", "Individual"], label="Modo", value=modo_atual).props('outlined dense').classes('w-full')
                
                container_limites = ui.column().classes('w-full')
            
            campos_limites = {}
            
            def atualizar_campos_limites():
                container_limites.clear()
                campos_limites.clear()
                
                if modo_cartao.value == "Unificado":
                    with container_limites:
                        with ui.column().classes('w-full gap-1 mb-3 mt-3'):
                            ui.label("💵 Limite À Vista (R$)").classes('campo-label')
                            lt = ui.number(value=config.get("limite_total", 3000), format="%.2f").props('outlined dense').classes('w-full')
                            campos_limites['limite_total'] = lt
                        with ui.column().classes('w-full gap-1 mb-3'):
                            ui.label("📦 Limite Parcelado (R$)").classes('campo-label')
                            lp = ui.number(value=config.get("limite_parcelado", 1500), format="%.2f").props('outlined dense').classes('w-full')
                            campos_limites['limite_parcelado'] = lp
                        with ui.column().classes('w-full gap-1 mb-3'):
                            ui.label("📅 Dia de Fechamento").classes('campo-label')
                            df = ui.select(options=list(range(1, 32)), label="Dia", value=config.get("dia_fechamento", 10)).props('outlined dense').classes('w-full')
                            campos_limites['dia_fechamento'] = df
                        
                        def salvar_unificado():
                            lt_val = campos_limites.get('limite_total')
                            lp_val = campos_limites.get('limite_parcelado')
                            df_val = campos_limites.get('dia_fechamento')
                            atualizar_config_local(
                                limite_total=lt_val.value if lt_val else 3000,
                                limite_parcelado=lp_val.value if lp_val else 1500,
                                dia_fechamento=df_val.value if df_val else 10,
                                modo_cartao="Unificado"
                            )
                            ui.notify("✅ Limites salvos!", type="positive", position="top", timeout=1000)
                            recarregar_principal()
                        
                        ui.button("Salvar Limites", on_click=salvar_unificado, icon='save').classes('w-full mt-2').style(f'background: {cor_primaria} !important; color: white !important; border-radius: 8px; font-weight: 600;')
                else:
                    with container_limites:
                        with ui.card().classes('dica-card mt-2').style('background: #faf5ff; border-left: 3px solid #8b5cf6;'):
                            ui.label("🔹 Modo Individual").classes('text-xs font-semibold text-purple-700')
                            ui.label("Cadastre seus cartões na aba '💳 Cartões' com limites individuais.").classes('text-[11px] text-gray-600')
                        cartoes = dados.get("cartoes", [])
                        if cartoes:
                            for c in cartoes:
                                with ui.card().classes('dica-card mt-2').style('background: #f9fafb;'):
                                    with ui.row().classes('items-center justify-between'):
                                        ui.label(f"💳 {c.get('nome', '')}").classes('text-sm font-semibold')
                                        ui.label(f"Limite Total: R$ {c.get('limite_total', 0):.2f}").classes('text-xs text-gray-600')
                        def salvar_individual():
                            atualizar_config_local(modo_cartao="Individual")
                            ui.notify("✅ Modo Individual ativado!", type="positive", position="top", timeout=1000)
                            recarregar_principal()
                        ui.button("Salvar Modo", on_click=salvar_individual, icon='save').classes('w-full mt-2').style(f'background: {cor_primaria} !important; color: white !important; border-radius: 8px; font-weight: 600;')
            
            modo_cartao.on('update:model-value', lambda e: atualizar_campos_limites())
            atualizar_campos_limites()
    
    def render_cartoes():
        cartoes = dados.get("cartoes", [])
        
        def abrir_form_cartao(cartao=None):
            is_edicao = cartao is not None
            with ui.dialog() as form_dialog, ui.card().classes('w-full max-w-[500px] p-0 gap-0 rounded-2xl'):
                with ui.row().classes('w-full items-center justify-between p-4').style(f'background: linear-gradient(135deg, {cor_escura}, {cor_primaria}) !important;'):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('credit_card').classes('text-xl text-white')
                        ui.label("Editar Cartão" if is_edicao else "Novo Cartão").classes('text-white text-base font-bold')
                    ui.button(icon='close', on_click=form_dialog.close).props('flat').style('color: white !important;')
                
                with ui.column().classes('p-4 w-full'):
                    with ui.card().classes('dica-card mb-3').style(f'background: {cor_primaria}08; border-left: 3px solid {cor_primaria};'):
                        ui.label("💳 Selecione seu banco e configure os limites").classes('text-xs').style(f'color: {cor_primaria} !important;')
                    
                    ui.label("🏦 Banco / Instituição").classes('campo-label')
                    nomes_bancos = [c["nome"] for c in CARTOES_POPULARES]
                    valor_padrao = cartao.get("nome", "") if is_edicao and cartao.get("nome", "") in nomes_bancos else nomes_bancos[0]
                    
                    with ui.row().style('display:flex!important;align-items:center!important;gap:12px!important;width:100%!important').classes('mb-3'):
                        banco_img = ui.image(CARTOES_POPULARES[0]["img"]).style('width:64px!important;height:40px!important;object-fit:contain!important;border-radius:6px!important;border:1px solid #e5e7eb!important;padding:3px!important;flex-shrink:0!important')
                        banco_select = ui.select(options=nomes_bancos, value=valor_padrao, label="Banco").props('outlined dense').style('flex:1!important;min-width:0!important')
                    
                    if is_edicao and cartao.get("nome"):
                        for card in CARTOES_POPULARES:
                            if card["nome"] == cartao.get("nome"):
                                banco_img.source = card["img"]
                                break
                    
                    def atualizar_banco():
                        nome = banco_select.value
                        for card in CARTOES_POPULARES:
                            if card["nome"] == nome:
                                banco_img.source = card["img"]
                                bandeira_value["valor"] = card["bandeira"]
                                bandeira_select.value = card["bandeira"]
                                for b in BANDEIRAS:
                                    if b["nome"] == card["bandeira"]:
                                        bandeira_img.source = b["img"]
                                        break
                                break
                    
                    banco_select.on('update:model-value', lambda: atualizar_banco())
                    
                    ui.label("🏷️ Nome personalizado (opcional)").classes('campo-label')
                    nome_inp = ui.input(placeholder="Ou use o nome do banco", value=cartao.get("nome", "") if is_edicao else "").props('outlined dense').classes('w-full mb-3').style('width:100%!important')
                    
                    ui.label("🏁 Bandeira").classes('campo-label')
                    bandeira_padrao = cartao.get("bandeira", CARTOES_POPULARES[0]["bandeira"]) if is_edicao else CARTOES_POPULARES[0]["bandeira"]
                    bandeira_value = {"valor": bandeira_padrao}
                    nomes_bandeiras = [b["nome"] for b in BANDEIRAS]
                    
                    with ui.row().style('display:flex!important;align-items:center!important;gap:12px!important;width:100%!important').classes('mb-3'):
                        bandeira_img = ui.image().style('width:44px!important;height:26px!important;object-fit:scale-down!important;background:white!important;padding:2px!important;border-radius:4px!important;flex-shrink:0!important')
                        for b in BANDEIRAS:
                            if b["nome"] == bandeira_padrao:
                                bandeira_img.source = b["img"]
                                break
                        bandeira_select = ui.select(options=nomes_bandeiras, value=bandeira_padrao, label="Bandeira").props('outlined dense').style('flex:1!important;min-width:0!important')
                    
                    def atualizar_bandeira():
                        for b in BANDEIRAS:
                            if b["nome"] == bandeira_select.value:
                                bandeira_value["valor"] = b["nome"]
                                bandeira_img.source = b["img"]
                                break
                    
                    bandeira_select.on('update:model-value', lambda: atualizar_bandeira())
                    
                    ui.label("💵 Limite À Vista (R$)").classes('campo-label')
                    limite_inp = ui.number(value=cartao.get("limite_vista", 0) if is_edicao else 0, format="%.2f").props('outlined dense prefix=R$').classes('w-full mb-1')
                    with ui.card().classes('dica-card mb-3').style('background: #f0fdf4; border-left: 3px solid #10b981;'):
                        ui.label("💡 Disponível para compras à vista.").classes('text-[10px] text-gray-600')
                    
                    ui.label("📦 Limite Parcelado (R$)").classes('campo-label')
                    parc_inp = ui.number(value=cartao.get("limite_parcelado", 0) if is_edicao else 0, format="%.2f").props('outlined dense prefix=R$').classes('w-full mb-1')
                    with ui.card().classes('dica-card mb-3').style('background: #eff6ff; border-left: 3px solid #3b82f6;'):
                        ui.label("💡 Disponível para compras parceladas.").classes('text-[10px] text-gray-600')
                    
                    ui.label("📅 Dia de Fechamento").classes('campo-label')
                    dia_inp = ui.select(options=list(range(1, 32)), value=cartao.get("dia_fechamento", 10) if is_edicao else 10).props('outlined dense').classes('w-full mb-1')
                    with ui.card().classes('dica-card mb-4').style('background: #fef3c7; border-left: 3px solid #f59e0b;'):
                        ui.label("💡 Dia em que a fatura fecha.").classes('text-[10px] text-gray-600')
                    
                    def salvar_cartao():
                        nome_final = nome_inp.value.strip() if nome_inp.value.strip() else banco_select.value
                        if not nome_final:
                            ui.notify("⚠️ Selecione um banco ou digite um nome", type="warning", position="top")
                            return
                        if not is_edicao:
                            from db import verificar_limite_cartoes
                            pode, msg = verificar_limite_cartoes(get_usuario_logado_email())
                            if not pode:
                                ui.notify(f"⚠️ {msg}", type="warning", position="top", timeout=3000)
                                return
                        novo = {
                            "id": len(dados.get("cartoes", [])) + 1 if not is_edicao else cartao["id"],
                            "nome": nome_final,
                            "bandeira": bandeira_value.get("valor", "Mastercard"),
                            "limite_vista": float(limite_inp.value or 0),
                            "limite_parcelado": float(parc_inp.value or 0),
                            "limite_total": float(limite_inp.value or 0) + float(parc_inp.value or 0),
                            "dia_fechamento": int(dia_inp.value or 10),
                        }
                        if "cartoes" not in dados:
                            dados["cartoes"] = []
                        if is_edicao:
                            for i, c in enumerate(dados["cartoes"]):
                                if c.get("id") == cartao["id"]:
                                    dados["cartoes"][i] = novo
                                    break
                        else:
                            dados["cartoes"].append(novo)
                        arquivo = os.path.join('data', f"{email.replace('@','_').replace('.','_').lower()}.json")
                        salvar_json(arquivo, dados)
                        form_dialog.close()
                        ui.notify("✅ Cartão salvo!", type="positive", position="top", timeout=1000)
                        recarregar_principal()
                    
                    with ui.row().classes('w-full gap-2'):
                        ui.button("Cancelar", on_click=form_dialog.close).props('outline').classes('w-1/2').style(f'color: {cor_primaria} !important; border-color: {cor_primaria} !important; border-radius: 8px;')
                        ui.button("Salvar Cartão", on_click=salvar_cartao, icon='save').classes('w-1/2').style(f'background: {cor_primaria} !important; color: white !important; border-radius: 8px; font-weight: 600;')
            form_dialog.open()
        
        def remover_cartao_conf(cartao):
            def confirmar():
                if "cartoes" in dados:
                    dados["cartoes"] = [c for c in dados["cartoes"] if c.get("id") != cartao.get("id")]
                    arquivo = os.path.join('data', f"{email.replace('@','_').replace('.','_').lower()}.json")
                    salvar_json(arquivo, dados)
                carregar_dados()
                ui.notify("🗑️ Cartão removido!", type="warning", position="top", timeout=1000)
                confirm_dialog.close()
                recarregar_principal()
            with ui.dialog() as confirm_dialog, ui.card().classes('w-[320px] p-4 rounded-xl'):
                ui.icon('warning').classes('text-red-500 text-2xl mb-2')
                ui.label("Excluir cartão?").classes('text-lg font-bold')
                ui.label(f"{cartao.get('nome')}").classes('text-sm text-gray-500')
                with ui.row().classes('justify-end gap-2 mt-4'):
                    ui.button("Cancelar", on_click=confirm_dialog.close).props('outline').style(f'color: {cor_primaria} !important; border-color: {cor_primaria} !important;')
                    ui.button("Excluir", on_click=confirmar).style(f'background: #ef4444 !important; color: white !important; border-radius: 8px;')
            confirm_dialog.open()
        
        with ui.card().classes('config-card'):
            with ui.card().classes('dica-card').style(f'background: {cor_primaria}08; border-left: 3px solid {cor_primaria};'):
                with ui.row().classes('items-start gap-2'):
                    ui.icon('info').classes('text-sm mt-0.5').style(f'color: {cor_primaria} !important;')
                    with ui.column().classes('gap-1'):
                        ui.label("💳 Seus Cartões").classes('text-xs font-semibold').style(f'color: {cor_primaria} !important;')
                        ui.label("Limite Total = Limite À Vista + Limite Parcelado").classes('text-[11px] text-gray-600')
            
            with ui.row().classes('items-center justify-between mb-3'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('credit_card').classes('text-lg').style(f'color: {cor_primaria} !important;')
                    ui.label("Cartões").classes('text-base font-bold')
                ui.button("+ Novo Cartão", on_click=lambda: abrir_form_cartao(), icon='add').classes('btn-sm').style(f'background: {cor_primaria} !important; color: white !important;')
            
            if not cartoes:
                ui.label("Nenhum cartão cadastrado").classes('text-sm text-gray-400 text-center p-4')
                return
            
            for c in cartoes:
                # Calcular valores (SEMPRE recalcula o Total)
                limite_vista_val = c.get("limite_vista", 0) or 0
                limite_parcelado_val = c.get("limite_parcelado", 0) or 0
                limite_total_val = limite_vista_val + limite_parcelado_val
                
                with ui.card().classes('cartao-card'):
                    with ui.row().classes('w-full items-center no-wrap').style('gap: 12px;'):
                        # ESQUERDA (30%) - IMAGEM
                        with ui.element('div').style('flex: 0 0 30%; display: flex; justify-content: center;'):
                            img_cartao = None
                            for card in CARTOES_POPULARES:
                                if card["nome"] == c.get("nome", ""):
                                    img_cartao = card["img"]
                                    break
                            if img_cartao:
                                ui.image(img_cartao).style('width: 100%; max-width: 100px; height: 60px; object-fit: contain;')
                        
                        # DIREITA (70%) - DADOS
                        with ui.element('div').style('flex: 1; display: flex; flex-direction: column; gap: 2px;'):
                            with ui.row().classes('items-center gap-2'):
                                ui.label(c.get("nome", "")).classes('text-sm font-semibold text-gray-800')
                                if c.get("bandeira"):
                                    ui.label(c.get("bandeira", "")).classes('text-[9px] text-gray-400 bg-gray-100 px-2 py-0.5 rounded')
                            
                            ui.label(
                                f"Limite Total: R$ {limite_total_val:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
                            ).classes('text-[12px] font-bold').style(f'color: {cor_primaria} !important;')
                            
                            ui.label(
                                f"À Vista: R$ {limite_vista_val:,.2f} | Parcelado: R$ {limite_parcelado_val:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.')
                            ).classes('text-[9px] text-gray-500')
                            
                            ui.label(f"Fecha dia {c.get('dia_fechamento', 10)}").classes('text-[10px] text-gray-400')
                        
                        # BOTÕES
                        with ui.element('div').style('display: flex; flex-direction: column; gap: 4px;'):
                            ui.button(icon='edit', on_click=lambda c=c: abrir_form_cartao(c)).props('flat round size=sm').style(f'color: {cor_primaria} !important;')
                            ui.button(icon='delete', on_click=lambda c=c: remover_cartao_conf(c)).props('flat round size=sm').style(f'color: {cor_primaria} !important;')
    
    def render_tema():
        cor_atual = config_service.get_primary_color()
        tema_selecionado = {"tema": None}
        botoes_tema = []
        
        def atualizar_destaque():
            for btn, tema in botoes_tema:
                if tema_selecionado["tema"] and tema["cor"].upper() == tema_selecionado["tema"]["cor"].upper():
                    btn.style(f'border-color: #1f2937 !important; box-shadow: 0 0 0 3px white, 0 0 0 5px {cor_primaria} !important;')
                else:
                    btn.style('border-color: transparent !important; box-shadow: none !important;')
        
        def selecionar_tema(tema):
            tema_selecionado["tema"] = tema
            atualizar_destaque()
        
        def aplicar_tema():
            if tema_selecionado["tema"] is None:
                ui.notify("⚠️ Selecione um tema primeiro", type="warning", position="top")
                return
            tema = tema_selecionado["tema"]
            config_service.set_primary_color(tema["cor"])
            config_service.set_primary_dark(tema["escura"])
            ui.notify(f"🎨 Tema {tema['nome']} aplicado!", type="positive", position="top", timeout=1000)
            recarregar_principal()
        
        with ui.card().classes('config-card'):
            with ui.row().classes('items-center gap-2 mb-3'):
                ui.icon('palette').classes('text-lg').style(f'color: {cor_primaria} !important;')
                ui.label("Tema").classes('text-base font-bold')
            ui.label("Selecione uma cor e clique em Aplicar").classes('text-xs text-gray-400 mb-3')
            with ui.element('div').classes('cores-grid mb-4'):
                for tema in CORES_TEMA:
                    is_atual = cor_atual.upper() == tema["cor"].upper()
                    with ui.element('div').classes('cor-item'):
                        btn_cor = ui.element('div').classes('cor-circle').style(f'background: {tema["cor"]};' + (f'border-color: {cor_primaria}; box-shadow: 0 0 0 3px white, 0 0 0 5px {cor_primaria}80;' if is_atual else '')).on('click', lambda t=tema: selecionar_tema(t))
                        ui.label(tema["nome"]).classes('text-[10px] text-gray-600')
                        botoes_tema.append((btn_cor, tema))
            ui.button("Aplicar Tema", on_click=aplicar_tema, icon='check').classes('w-full').style(f'background: {cor_primaria} !important; color: white !important; border-radius: 8px; font-weight: 600;')
    
    def render_fixos():
        fixos = dados.get("fixos", [])
        categorias = dados.get("categorias", CATEGORIAS_PADRAO)
        categorias_nomes = [c["nome"] for c in categorias]
        
        def remover_fixo(gid):
            if 'fixos' in dados:
                dados['fixos'] = [f for f in dados['fixos'] if f.get('id') != gid]
                arquivo = os.path.join('data', f"{email.replace('@','_').replace('.','_').lower()}.json")
                salvar_json(arquivo, dados)
            ui.notify("🗑️ Removido!", type="warning", position="top", timeout=1000)
            recarregar_principal()
        
        with ui.card().classes('config-card'):
            with ui.card().classes('dica-card').style(f'background: {cor_primaria}08; border-left: 3px solid {cor_primaria};'):
                with ui.row().classes('items-start gap-2'):
                    ui.icon('info').classes('text-sm mt-0.5').style(f'color: {cor_primaria} !important;')
                    with ui.column().classes('gap-1'):
                        ui.label("💡 Gastos recorrentes").classes('text-xs font-semibold').style(f'color: {cor_primaria} !important;')
                        ui.label("Streaming, academias, assinaturas. Eles sempre aparecem nos lançamentos.").classes('text-[11px] text-gray-600')
            
            with ui.row().classes('items-center justify-between mb-3'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('repeat').classes('text-lg').style(f'color: {cor_primaria} !important;')
                    ui.label("Gastos Fixos").classes('text-base font-bold')
                total = sum(g.get("valor", 0) for g in fixos)
                ui.label(f"R$ {total:.2f}").classes('text-sm font-bold').style(f'color: {cor_primaria} !important;')
            
            if fixos:
                for g in fixos:
                    with ui.card().classes('fixo-card'):
                        with ui.row().classes('justify-between items-center w-full'):
                            with ui.column().classes('gap-0 flex-1'):
                                ui.label(g.get("descricao", "")).classes('text-sm font-semibold text-gray-800')
                                if g.get("categoria"): ui.label(g.get("categoria")).classes('text-[10px] text-purple-500')
                            with ui.row().classes('items-center gap-3'):
                                ui.label(f"R$ {g.get('valor', 0):.2f}").classes('text-sm font-bold').style(f'color: {cor_primaria} !important;')
                                ui.button(icon='delete', on_click=lambda gid=g["id"]: remover_fixo(gid)).props('flat round size=sm').style(f'color: {cor_primaria} !important;')
            else:
                ui.label("Nenhum gasto fixo").classes('text-sm text-gray-400 text-center p-4')
            
            with ui.expansion("+ Adicionar", icon='add').classes('w-full mt-3').style(f'color: {cor_primaria} !important;'):
                with ui.column().classes('gap-3 p-2'):
                    di = ui.input(label="Descrição", placeholder="Netflix, Spotify...").props('outlined dense').classes('w-full')
                    vi = ui.number(label="Valor R$", format="%.2f", value=0).props('outlined dense prefix=R$').classes('w-full')
                    ci = ui.select(options=categorias_nomes, label="Categoria", value="Assinaturas" if "Assinaturas" in categorias_nomes else categorias_nomes[-1]).props('outlined dense').classes('w-full')
                    
                    def add_fixo():
                        if not di.value or not vi.value or vi.value <= 0:
                            ui.notify("⚠️ Preencha todos os campos", type="warning", position="top")
                            return
                        if 'fixos' not in dados:
                            dados['fixos'] = []
                        dados['fixos'].append({'id': len(dados['fixos']) + 1, 'descricao': di.value.strip(), 'valor': float(vi.value), 'categoria': ci.value})
                        arquivo = os.path.join('data', f"{email.replace('@','_').replace('.','_').lower()}.json")
                        salvar_json(arquivo, dados)
                        ui.notify("✅ Adicionado!", type="positive", position="top", timeout=1000)
                        recarregar_principal()
                    
                    ui.button("Adicionar", on_click=add_fixo, icon='add').classes('w-full').style(f'background: {cor_primaria} !important; color: white !important; border-radius: 8px; font-weight: 600;')
    

    def abrir_gerenciar_assinatura():
        """Popup para gerenciar assinatura Premium"""
        with ui.dialog() as d, ui.card().classes('w-[400px] max-w-[92vw] p-0 gap-0 rounded-2xl'):
            # Header
            with ui.row().classes('w-full items-center justify-between p-4').style(f'background: linear-gradient(135deg, {cor_escura}, {cor_primaria}) !important;'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('credit_card').classes('text-xl text-white')
                    ui.label("Gerenciar Assinatura").classes('text-white text-base font-bold')
                ui.button(icon='close', on_click=d.close).props('flat').style('color: white !important;')
            
            with ui.element('div').classes('p-4'):
                ui.label("💎 Plano Premium Atual").classes('text-sm font-bold mb-3')
                ui.label("R$ 4,99/mês — Lançamentos ilimitados, múltiplos cartões e mais.").classes('text-xs text-gray-500 mb-4')
                
                ui.separator().style('margin:8px 0')
                
                # Opção 1: Cancelar assinatura
                with ui.card().classes('w-full p-3 mb-2').style('background:#fef2f2;border:1px solid #fecaca;border-radius:10px;cursor:pointer').on('click', lambda: confirmar_cancelar()):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('cancel').classes('text-red-500')
                        with ui.column().classes('gap-0'):
                            ui.label("❌ Cancelar Assinatura").classes('text-sm font-semibold text-red-600')
                            ui.label("Volta para o plano Gratuito").classes('text-[10px] text-red-400')
                
                # Opção 2: Mudar para Gratuito
                with ui.card().classes('w-full p-3').style('background:#fef3c7;border:1px solid #fde68a;border-radius:10px;cursor:pointer').on('click', lambda: confirmar_downgrade()):
                    with ui.row().classes('items-center gap-2'):
                        ui.icon('swap_horiz').classes('text-yellow-600')
                        with ui.column().classes('gap-0'):
                            ui.label("⬇️ Mudar para Gratuito").classes('text-sm font-semibold text-yellow-700')
                            ui.label("Seus dados serão mantidos por 30 dias").classes('text-[10px] text-yellow-500')
            
            def confirmar_cancelar():
                d.close()
                with ui.dialog() as d2, ui.card().classes('w-[380px] max-w-[90vw] p-4 rounded-xl text-center'):
                    ui.icon('warning').classes('text-red-500 text-3xl mb-2')
                    ui.label("Cancelar Premium?").classes('text-lg font-bold mb-2')
                    ui.label("⚠️ Ao cancelar:").classes('text-xs font-semibold text-red-500')
                    ui.label("• Seus dados ficarão salvos por 30 dias").classes('text-[11px] text-gray-600')
                    ui.label("• Após 30 dias, tudo será excluído").classes('text-[11px] text-gray-600')
                    ui.label("• Você será deslogado automaticamente").classes('text-[11px] text-gray-600')
                    ui.label("• Poderá reativar o Premium a qualquer momento").classes('text-[11px] text-gray-600 mb-3')
                    
                    with ui.row().classes('justify-center gap-2'):
                        ui.button("Voltar", on_click=d2.close).props('outline').style(f'color:{cor_primaria};border-color:{cor_primaria};border-radius:8px')
                        def cancelar():
                            from db import atualizar_plano_usuario, set_usuario_logado
                            atualizar_plano_usuario(email, 'gratuito')
                            d2.close()
                            ui.notify("✅ Premium cancelado. Voltando para Gratuito.", type="warning", position="top", timeout=3000)
                            ui.timer(2.0, lambda: [set_usuario_logado(None), ui.navigate.to('/login')], once=True)
                        ui.button("Cancelar Premium", on_click=cancelar).style('background:#ef4444;color:white;border-radius:8px;font-weight:600')
                d2.open()
            
            def confirmar_downgrade():
                d.close()
                with ui.dialog() as d2, ui.card().classes('w-[380px] max-w-[90vw] p-4 rounded-xl text-center'):
                    ui.icon('info').classes('text-yellow-500 text-3xl mb-2')
                    ui.label("Mudar para Gratuito?").classes('text-lg font-bold mb-2')
                    ui.label("📋 Resumo:").classes('text-xs font-semibold')
                    ui.label("• Dados mantidos por 30 dias").classes('text-[11px] text-gray-600')
                    ui.label("• Perde acesso a múltiplos cartões").classes('text-[11px] text-gray-600')
                    ui.label("• Limite de 20 lançamentos/mês").classes('text-[11px] text-gray-600')
                    ui.label("• Pode voltar ao Premium quando quiser").classes('text-[11px] text-gray-600 mb-3')
                    
                    with ui.row().classes('justify-center gap-2'):
                        ui.button("Voltar", on_click=d2.close).props('outline').style(f'color:{cor_primaria};border-color:{cor_primaria};border-radius:8px')
                        def downgrade():
                            from db import atualizar_plano_usuario
                            atualizar_plano_usuario(email, 'gratuito')
                            d2.close()
                            ui.notify("⬇️ Plano alterado para Gratuito. Recarregue a página.", type="warning", position="top", timeout=3000)
                            ui.timer(1.5, lambda: recarregar_principal(), once=True)
                        ui.button("Mudar para Gratuito", on_click=downgrade).style('background:#f59e0b;color:white;border-radius:8px;font-weight:600')
                d2.open()
        
        d.open()

    def render_perfil():
        email = get_usuario_logado_email()
        if not email:
            with ui.card().classes('config-card text-center'):
                ui.label("Nenhum usuário logado").classes('text-gray-500')
            return
        
        usuario = buscar_usuario_por_email(email)
        if not usuario:
            with ui.card().classes('config-card text-center'):
                ui.label("Usuário não encontrado").classes('text-gray-500')
            return
        
        avatar_emoji = usuario.get('avatar_emoji', '👤')
        plano = usuario.get('plano', 'gratuito')
        plano_nome = PLANOS.get(plano, {}).get('nome', 'Gratuito')
        
        # ═══ CARD: AVATAR + INFOS EM 2 COLUNAS ═══
        with ui.card().classes('config-card'):
            with ui.row().classes('w-full gap-4'):
                # Coluna esquerda: Avatar + Plano (sem nome/email)
                with ui.column().classes('items-center').style('flex:1;min-width:100px'):
                    avatar_display = ui.element('div').style(f'width:80px;height:80px;border-radius:50%;background:linear-gradient(135deg,{cor_primaria}30,{cor_primaria}10);display:flex;align-items:center;justify-content:center;font-size:40px;cursor:pointer;transition:all 0.2s;border:3px solid {cor_primaria}40;box-shadow:0 4px 12px {cor_primaria}20')
                    with avatar_display:
                        avatar_label = ui.label(avatar_emoji)
                    
                    ui.label("Clique para alterar").classes('text-[9px] text-gray-400 mt-1 mb-2')
                    
                    cor_badge = '#10b981' if plano == 'premium' else '#f59e0b' if plano == 'gratuito' else '#3b82f6'
                    icone_badge = '💎' if plano == 'premium' else '🆓' if plano == 'gratuito' else '👑'
                    with ui.element('div').style(f'display:inline-flex;align-items:center;gap:4px;padding:4px 12px;border-radius:20px;font-size:10px;font-weight:600;background:{cor_badge}15;color:{cor_badge};border:1px solid {cor_badge}30'):
                        ui.label(f"{icone_badge} {plano_nome}")
                    
                    def abrir_selector_avatar():
                        with ui.dialog() as d, ui.card().classes('w-[360px] max-w-[90vw] p-4 rounded-2xl'):
                            ui.label("Escolha seu Avatar").classes('text-lg font-bold mb-3 text-center')
                            with ui.row().classes('flex-wrap justify-center gap-2'):
                                for av in AVATARES:
                                    is_sel = av == avatar_emoji
                                    av_div = ui.element('div').style(f'font-size:28px;padding:6px;cursor:pointer;border-radius:10px;{"border:2px solid "+cor_primaria+";background:"+cor_primaria+"15" if is_sel else "border:2px solid transparent"}')
                                    with av_div:
                                        ui.label(av)
                                    av_div.on('click', lambda a=av: sel_avatar(a))
                            def sel_avatar(a):
                                from db import atualizar_perfil_usuario
                                atualizar_perfil_usuario(email, avatar_emoji=a)
                                avatar_label.set_text(a)
                                d.close()
                                ui.notify("✅ Avatar atualizado!", type="positive", position="top", timeout=1000)
                            ui.button("Fechar", on_click=d.close).props('outline').classes('w-full mt-3').style(f'color:{cor_primaria};border-color:{cor_primaria};border-radius:8px;')
                        d.open()
                    
                    avatar_display.on('click', abrir_selector_avatar)
                
                # Coluna direita: Informações da conta
                with ui.column().classes('gap-1').style('flex:2'):
                    ui.label("📋 Informações da Conta").classes('text-sm font-bold mb-2')
                    
                    try:
                        data_criacao = datetime.fromisoformat(usuario.get('data_criacao', '')).strftime('%d/%m/%Y')
                    except:
                        data_criacao = 'N/A'
                    
                    infos = [
                        ("Nome", usuario.get('nome', '-')),
                        ("Email", usuario.get('email', '-')),
                        ("Membro desde", data_criacao),
                    ]
                    if usuario.get('data_expiracao'):
                        try:
                            data_exp = datetime.fromisoformat(usuario['data_expiracao']).strftime('%d/%m/%Y')
                        except:
                            data_exp = 'N/A'
                        infos.append(("Premium expira", data_exp))
                    
                    for label, valor in infos:
                        with ui.element('div').style(f'background:{cor_primaria}05;border-radius:6px;padding:8px 10px;display:flex;justify-content:space-between;align-items:center'):
                            ui.label(label).style('font-size:10px;color:#9ca3af;font-weight:500')
                            ui.label(valor).style('font-size:11px;color:#1f2937;font-weight:500')
            
            # Trocar senha
            ui.separator().style('margin:10px 0')
            with ui.expansion("🔒 Alterar Senha", icon='lock').classes('w-full').style(f'color:{cor_primaria};font-weight:500'):
                with ui.column().classes('gap-2 p-2'):
                    ns = ui.input("Nova senha", password=True, password_toggle_button=True).props('outlined dense').classes('w-full')
                    cs = ui.input("Confirmar senha", password=True, password_toggle_button=True).props('outlined dense').classes('w-full')
                    def trocar():
                        if not ns.value or len(ns.value) < 4:
                            ui.notify("⚠️ Mínimo 4 caracteres", type="warning", position="top"); return
                        if ns.value != cs.value:
                            ui.notify("⚠️ Senhas não conferem", type="warning", position="top"); return
                        from db import hash_senha, carregar_usuarios, salvar_usuarios
                        usuarios = carregar_usuarios()
                        for u in usuarios:
                            if u.get('email','').lower() == email.lower():
                                u['senha'] = hash_senha(ns.value)
                                salvar_usuarios(usuarios)
                                ui.notify("✅ Senha alterada!", type="positive", position="top"); return
                    ui.button("Salvar Senha", on_click=trocar).style(f'background:{cor_primaria};color:white;border-radius:8px;font-weight:600').classes('w-full')
        
        # ═══ PLANO ═══
        with ui.card().classes('config-card'):
            ui.label("📊 Seu Plano").classes('text-base font-bold mb-3')
            
            if plano == 'gratuito':
                limites = [("Lançamentos por mês", "20"), ("Cartões", "1"), ("Modo Individual", "❌"), ("Consultor Financeiro", "Básico")]
            elif plano == 'premium':
                limites = [("Lançamentos por mês", "Ilimitado"), ("Cartões", "Ilimitado"), ("Modo Individual", "✅"), ("Consultor Financeiro", "Premium (30+)")]
            else:
                limites = [("Lançamentos por mês", "3 (teste)"), ("Cartões", "1"), ("Modo Individual", "❌"), ("Consultor Financeiro", "Básico"), ("Persistência", "❌")]
            
            for label, valor in limites:
                with ui.row().classes('items-center justify-between py-2'):
                    ui.label(label).classes('text-sm text-gray-600')
                    ui.label(valor).classes('text-sm font-semibold')
            
            ui.separator().style('margin:8px 0')
            
            if plano == 'gratuito':
                with ui.card().classes('w-full p-3').style('background:linear-gradient(135deg,#8b5cf6,#6366f1);border-radius:10px'):
                    ui.label("💎 Premium por R$ 4,99/mês").style('font-size:14px;font-weight:600;color:white;margin-bottom:6px')
                    ui.label("Ilimitado, múltiplos cartões e mais!").style('font-size:11px;color:rgba(255,255,255,0.8);margin-bottom:8px')
                    ui.button("Fazer Upgrade", icon='star', on_click=lambda: ui.navigate.to('/admin')).classes('w-full').style('background:white;color:#6366f1;border-radius:8px;font-weight:600')
            elif plano == 'premium':
                with ui.card().classes('w-full p-3').style('background:#f0fdf4;border:1px solid #10b981;border-radius:10px'):
                    ui.label("💎 Você é Premium!").style('font-size:14px;font-weight:600;color:#065f46;margin-bottom:4px')
                    ui.label("Todos os recursos liberados. Aproveite!").style('font-size:11px;color:#047857;margin-bottom:8px')
                    ui.button("Gerenciar Assinatura", icon='settings', on_click=lambda: abrir_gerenciar_assinatura()).classes('w-full').style(f'color:{cor_primaria};border-color:{cor_primaria};border-radius:8px;font-weight:600').props('outline')
            else:
                with ui.card().classes('w-full p-3').style('background:#eff6ff;border:1px solid #3b82f6;border-radius:10px'):
                    ui.label("👑 Conta Demo").style('font-size:14px;font-weight:600;color:#1e40af;margin-bottom:4px')
                    ui.label("Crie sua conta gratuita!").style('font-size:11px;color:#475569;margin-bottom:6px')
                    ui.button("Criar Conta Grátis", on_click=lambda: ui.navigate.to('/criar-conta')).classes('w-full').style('background:#3b82f6;color:white;border-radius:8px')


    def render_sobre():
        with ui.element('div').classes('sobre-logo-container'):
            ui.image(LOGO_COMPLETA).classes('sobre-logo')
        with ui.card().classes('config-card'):
            with ui.row().classes('items-center justify-between mb-4'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('info').classes('text-lg').style(f'color: {cor_primaria} !important;')
                    ui.label("Informações do App").classes('text-base font-bold')
                with ui.element('div').classes('sobre-badge').style(f'background: {cor_primaria} !important;'):
                    ui.icon('check_circle').classes('text-xs')
                    ui.label("v2.0.0")
            for label, valor in [("Nome do App", "Cartometro"), ("Slogan", "Controle Inteligente do seu Crédito"), ("Versão", "2.0.0 - Estável"), ("Data de Lançamento", "Janeiro 2025")]:
                with ui.element('div').classes('sobre-info-item').style(f'border-left-color: {cor_primaria} !important;'):
                    ui.label(label).classes('sobre-info-label')
                    ui.label(valor).classes('sobre-info-value')
        with ui.card().classes('config-card'):
            with ui.row().classes('items-center gap-2 mb-4'):
                ui.icon('star').classes('text-lg').style(f'color: {cor_primaria} !important;')
                ui.label("Funcionalidades").classes('text-base font-bold')
            for func in ["📊 Dashboard financeiro em tempo real", "💳 Controle de cartão de crédito", "📅 Gestão por ciclo de fatura ou mês", "🔁 Gastos fixos e parcelados", "🤖 Consultor Financeiro Inteligente", "🎨 Temas personalizáveis", "📱 Interface 100% responsiva"]:
                with ui.element('div').classes('sobre-func-item'):
                    ui.icon('check_circle').classes('text-xs').style(f'color: {cor_primaria} !important;')
                    ui.label(func).classes('text-sm text-gray-700')
        with ui.card().classes('config-card').style('text-align: center;'):
            ui.label("© 2025 Cartometro").classes('text-sm font-semibold text-gray-600')
            ui.label("Todos os direitos reservados.").classes('text-xs text-gray-400 mt-1')
            ui.label("Feito com ❤️ para você controlar suas finanças").classes('text-xs text-gray-400 mt-2')
    
    def atualizar_conteudo():
        nonlocal tab_content
        if tab_content is None: return
        tab_content.clear()
        aba = aba_ativa["atual"]
        with tab_content:
            if aba == "limites": render_limites()
            elif aba == "cartoes": render_cartoes()
            elif aba == "tema": render_tema()
            elif aba == "fixos": render_fixos()
            elif aba == "perfil": render_perfil()
            elif aba == "sobre": render_sobre()
    
    def mudar_aba(aba, btns):
        aba_ativa["atual"] = aba
        for nome, btn in btns.items():
            btn.classes(remove='active')
            btn.style('color: #6b7280 !important; background: transparent !important;')
        if aba in btns:
            btns[aba].classes('active')
            btns[aba].style(f'color: {cor_primaria} !important; font-weight: 600 !important; background: {cor_primaria}10 !important;')
        atualizar_conteudo()
    
    def montar_interface():
        nonlocal tab_content
        config = dados.get("config", {})
        modo = config.get("modo_cartao", "Unificado")
        pode_individual = pode_usar_modo_individual(get_usuario_logado_email()) if get_usuario_logado_email() else False
        
        abas_list = [("limites", "⚙️ Limites"), ("tema", "🎨 Tema"), ("fixos", "🔁 Fixos"), ("perfil", "👤 Perfil"), ("sobre", "ℹ️ Sobre")]
        if modo == "Individual" and pode_individual:
            abas_list.insert(1, ("cartoes", "💳 Cartões"))
        
        with ui.element('div').classes('config-tela'):
            with ui.element('div').classes('config-header'):
                with ui.row().classes('w-full items-center justify-between p-3').style(f'background: linear-gradient(135deg, {cor_escura}, {cor_primaria}) !important;'):
                    with ui.row().classes('items-center gap-2'):
                        ui.button(icon='arrow_back', on_click=recarregar_principal).props('flat round').style('color: white !important;')
                        with ui.element('div').classes('w-8 h-8 rounded-full flex items-center justify-center').style('background: rgba(255,255,255,0.2) !important;'):
                            ui.icon('settings').classes('text-sm text-white')
                        ui.label("Configurações").classes('text-lg font-bold text-white')
                    cor_badge = '#10b981' if plano_atual == 'premium' else '#f59e0b' if plano_atual == 'gratuito' else '#3b82f6'
                    with ui.element('div').classes('plano-badge').style(f'background: rgba(255,255,255,0.2); color: white;'):
                        ui.label(f"{'💎' if plano_atual == 'premium' else '🆓'} {plano_nome}")
            
            ui.element('div').style(f'height: 3px; background: linear-gradient(90deg, {cor_primaria}, {cor_primaria}60, transparent); position: relative; flex-shrink: 0;')
            
            with ui.element('div').classes('tabs-container'):
                tabs = {}
                for nome, label in abas_list:
                    is_active = nome == aba_ativa["atual"]
                    btn = ui.label(label).classes(f'tab-btn {"active" if is_active else ""}')
                    if is_active:
                        btn.style(f'color: {cor_primaria} !important; font-weight: 600 !important; background: {cor_primaria}10 !important;')
                    btn.on('click', lambda n=nome: mudar_aba(n, tabs))
                    tabs[nome] = btn
            
            with ui.element('div').classes('config-scroll'):
                tab_content = ui.column().classes('w-full')
                atualizar_conteudo()
    
    montar_interface()


__all__ = ['tela_configuracoes']