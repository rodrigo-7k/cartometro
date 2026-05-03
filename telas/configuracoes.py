"""
Tela de Configurações - Limites, Tema, Gastos Fixos, Cartões, Usuários e Sobre
"""

from nicegui import ui
from db import carregar, atualizar_config, adicionar_gasto, remover_gasto, adicionar_cartao, remover_cartao, atualizar_cartao
from config_service import config_service
from constantes import CATEGORIAS_PADRAO
from datetime import datetime
import json
import os
import hashlib


# ============================================================
# URLS DAS IMAGENS (CLOUDINARY)
# ============================================================
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

USUARIOS_ARQ = 'usuarios.json'

CUSTOM_CSS = """
<style>
* { box-sizing: border-box !important; }

.config-tela {
    width: 100% !important;
    height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
    background: #f3f4f6 !important;
    overflow: hidden !important;
    padding: 0 !important;
    margin: 0 !important;
}

.config-header { flex-shrink: 0 !important; width: 100% !important; }

.config-scroll {
    flex: 1 !important;
    overflow-y: auto !important;
    overflow-x: hidden !important;
    padding: 8px 8px 20px 8px !important;
    width: 100% !important;
}

.config-scroll::-webkit-scrollbar { width: 4px; }
.config-scroll::-webkit-scrollbar-track { background: #e5e7eb; }
.config-scroll::-webkit-scrollbar-thumb { background: #9ca3af; border-radius: 4px; }

.tabs-container {
    background: white !important;
    border-bottom: 1px solid #e5e7eb !important;
    padding: 2px 4px !important;
    display: flex !important;
    gap: 1px !important;
    overflow-x: auto !important;
    flex-shrink: 0 !important;
    scrollbar-width: none !important;
    -webkit-overflow-scrolling: touch !important;
}

.tabs-container::-webkit-scrollbar { display: none !important; }

.tab-btn {
    padding: 8px 10px !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    border-radius: 8px 8px 0 0 !important;
    border: none !important;
    background: transparent !important;
    color: #6b7280 !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
    white-space: nowrap !important;
    flex-shrink: 0 !important;
    min-width: fit-content !important;
    display: flex !important;
    align-items: center !important;
    gap: 3px !important;
}

.tab-btn:hover { color: #374151 !important; background: #f9fafb !important; }

.config-card {
    background: white !important;
    border-radius: 12px !important;
    padding: 16px !important;
    margin: 0 0 12px 0 !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
    width: 100% !important;
}

.campo-label { font-size: 12px; font-weight: 600; color: #374151; margin-bottom: 4px; }

.dica-card {
    border-radius: 8px !important;
    padding: 10px 12px !important;
    margin-bottom: 12px !important;
}

.cores-grid { display: grid !important; grid-template-columns: repeat(4, 1fr) !important; gap: 10px !important; width: 100% !important; }
.cor-item { display: flex !important; flex-direction: column !important; align-items: center !important; gap: 6px !important; cursor: pointer !important; padding: 4px !important; }
.cor-circle {
    width: 48px !important; height: 48px !important;
    border-radius: 50% !important;
    transition: all 0.2s ease !important;
    border: 3px solid transparent !important;
    cursor: pointer !important;
}
.cor-circle:hover { transform: scale(1.12) !important; }

.avatares-grid { display: grid !important; grid-template-columns: repeat(4, 1fr) !important; gap: 8px !important; width: 100% !important; }
.avatar-option {
    aspect-ratio: 1 !important; width: 100% !important;
    border-radius: 14px !important;
    display: flex !important; align-items: center !important; justify-content: center !important;
    font-size: 32px !important; cursor: pointer !important;
    transition: all 0.15s ease !important;
    border: 2px solid #e5e7eb !important; background: white !important;
}
.avatar-option:hover { transform: scale(1.05) !important; }

.fixo-card {
    width: 100% !important; padding: 12px !important;
    background: #faf5ff !important; border-radius: 8px !important;
    margin-bottom: 8px !important; border: 1px solid #e9d5ff !important;
}

.usuario-card, .cartao-card {
    background: #f9fafb !important; border-radius: 10px !important;
    padding: 12px !important; margin-bottom: 8px !important;
    border: 1px solid #f3f4f6 !important;
}

.sobre-logo-container {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    padding: 32px 20px !important;
    background: linear-gradient(135deg, #f8fafc, #f0f5ff) !important;
    border-radius: 16px !important;
    margin-bottom: 16px !important;
}

.sobre-logo {
    width: 200px !important;
    height: auto !important;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1)) !important;
}

.sobre-info-item {
    background: white !important;
    border-radius: 10px !important;
    padding: 14px 16px !important;
    margin-bottom: 10px !important;
    border-left: 3px solid var(--cor-primaria) !important;
}

.sobre-info-label {
    font-size: 10px !important;
    font-weight: 600 !important;
    color: #9ca3af !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    margin-bottom: 4px !important;
}

.sobre-info-value {
    font-size: 14px !important;
    font-weight: 500 !important;
    color: #1f2937 !important;
}

.sobre-badge {
    display: inline-flex !important;
    align-items: center !important;
    gap: 6px !important;
    padding: 4px 12px !important;
    border-radius: 20px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    color: white !important;
}

.sobre-func-item {
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    padding: 4px 0 !important;
}

.btn-sm { padding: 6px 12px !important; font-size: 11px !important; border-radius: 6px !important; min-height: 30px !important; }

.q-field--outlined.q-field--focused .q-field__control:before { border-color: var(--cor-primaria) !important; }
.q-field--outlined.q-field--focused .q-field__control:after { border-color: var(--cor-primaria) !important; }
.q-field--focused .q-field__control { border-color: transparent !important; }
.q-field--focused .q-field__label { color: #374151 !important; }
.q-field--focused .q-field__native { color: #111827 !important; }
.q-item.q-manual-focusable--focused { background: var(--cor-primaria) !important; color: white !important; }
</style>
"""


def tela_configuracoes(container, dialog_pai=None):
    
    container.clear()
    container.classes('p-0 m-0')
    container.style('padding: 0 !important; margin: 0 !important; width: 100% !important; height: 100% !important;')
    
    ui.add_head_html(CUSTOM_CSS)
    
    cor_primaria = config_service.get_primary_color()
    cor_escura = config_service.get_primary_dark()
    
    ui.add_head_html(f'<style>:root {{ --cor-primaria: {cor_primaria}; }}</style>')
    
    aba_ativa = {"atual": "limites"}
    dados = carregar()
    usuarios_ref = {"lista": []}
    tab_content = None
    
    def carregar_dados():
        nonlocal dados
        dados = carregar()
    
    def carregar_usuarios():
        if os.path.exists(USUARIOS_ARQ):
            with open(USUARIOS_ARQ, "r", encoding="utf-8") as f:
                usuarios_ref["lista"] = json.load(f)
        else:
            usuarios_ref["lista"] = []
    
    def hash_senha(senha):
        return hashlib.sha256(senha.encode()).hexdigest()
    
    def salvar_usuarios():
        with open(USUARIOS_ARQ, "w", encoding="utf-8") as f:
            json.dump(usuarios_ref["lista"], f, indent=2, ensure_ascii=False)
    
    def fechar():
        if dialog_pai is not None:
            dialog_pai.close()
        else:
            container.clear()
    
    def recarregar_principal():
        fechar()
        ui.run_javascript('location.reload()')
    
    # =========================
    # RENDER: LIMITES
    # =========================
    def render_limites():
        config = dados.get("config", {})
        modo_atual = config.get("modo_cartao", "Unificado")
        
        with ui.card().classes('config-card'):
            with ui.row().classes('items-center gap-2 mb-3'):
                ui.icon('tune').classes('text-lg').style(f'color: {cor_primaria} !important;')
                ui.label("Configuração do Cartão").classes('text-base font-bold')
            
            # ============================================================
            # DICA INFORMATIVA
            # ============================================================
            with ui.card().classes('dica-card').style(f'background: {cor_primaria}08; border-left: 3px solid {cor_primaria};'):
                with ui.row().classes('items-start gap-2'):
                    ui.icon('info').classes('text-sm mt-0.5').style(f'color: {cor_primaria} !important;')
                    with ui.column().classes('gap-1'):
                        ui.label("💡 Como funciona").classes('text-xs font-semibold').style(f'color: {cor_primaria} !important;')
                        ui.label("Escolha o modo de controle primeiro. No modo Unificado, você define limites gerais. No Individual, cada cartão tem seus próprios limites.").classes('text-[11px] text-gray-600')
            
            # ============================================================
            # MODO DE CONTROLE (PRIMEIRO)
            # ============================================================
            with ui.column().classes('w-full gap-1 mb-4'):
                ui.label("💳 Modo de Controle").classes('campo-label')
                modo_cartao = ui.select(
                    options=["Unificado", "Individual"], 
                    label="Modo", 
                    value=modo_atual
                ).props('outlined dense').classes('w-full')
                
                # Container para campos condicionais
                container_limites = ui.column().classes('w-full')
            
            # ============================================================
            # CAMPOS CONDICIONAIS
            # ============================================================
            campos_limites = {}
            
            def atualizar_campos_limites():
                container_limites.clear()
                campos_limites.clear()
                
                if modo_cartao.value == "Unificado":
                    # MODO UNIFICADO - Mostrar limites gerais
                    with container_limites:
                        with ui.card().classes('dica-card mt-2').style('background: #eff6ff; border-left: 3px solid #3b82f6;'):
                            with ui.row().classes('items-start gap-2'):
                                ui.icon('check_circle').classes('text-sm mt-0.5').style('color: #3b82f6 !important;')
                                with ui.column().classes('gap-1'):
                                    ui.label("🔹 Modo Unificado").classes('text-xs font-semibold text-blue-700')
                                    ui.label("• Um único limite para controlar todos os gastos").classes('text-[11px] text-gray-600')
                                    ui.label("• Perfeito para quem tem apenas um cartão de crédito").classes('text-[11px] text-gray-600')
                                    ui.label("• Os KPIs mostram o limite total consolidado").classes('text-[11px] text-gray-600')
                                    ui.label("✅ Configuração mais simples e direta").classes('text-[11px] text-blue-600 font-medium')
                        
                        with ui.column().classes('w-full gap-1 mb-3 mt-3'):
                            ui.label("💰 Limite Total (R$)").classes('campo-label')
                            lt = ui.number(value=config.get("limite_total", 3000), format="%.2f").props('outlined dense').classes('w-full')
                            ui.label("Valor máximo disponível para todas as compras").classes('text-[10px] text-gray-400')
                            campos_limites['limite_total'] = lt
                        
                        with ui.column().classes('w-full gap-1 mb-3'):
                            ui.label("📦 Limite Parcelado (R$)").classes('campo-label')
                            lp = ui.number(value=config.get("limite_parcelado", 1500), format="%.2f").props('outlined dense').classes('w-full')
                            ui.label("Controle extra para não acumular muitas parcelas").classes('text-[10px] text-gray-400')
                            campos_limites['limite_parcelado'] = lp
                        
                        with ui.column().classes('w-full gap-1 mb-3'):
                            ui.label("📅 Dia de Fechamento").classes('campo-label')
                            df = ui.select(options=list(range(1, 32)), label="Dia", value=config.get("dia_fechamento", 10)).props('outlined dense').classes('w-full')
                            ui.label("📌 Dica: Compras após o fechamento entram na próxima fatura").classes('text-[10px] text-gray-400')
                            campos_limites['dia_fechamento'] = df
                        
                        def salvar_unificado():
                            lt_val = campos_limites.get('limite_total')
                            lp_val = campos_limites.get('limite_parcelado')
                            df_val = campos_limites.get('dia_fechamento')
                            atualizar_config(
                                limite_total=lt_val.value if lt_val else 3000, 
                                limite_parcelado=lp_val.value if lp_val else 1500, 
                                dia_fechamento=df_val.value if df_val else 10, 
                                modo_cartao=modo_cartao.value
                            )
                            ui.notify("✅ Limites salvos! Recarregando...", type="positive", position="top", timeout=1000)
                            recarregar_principal()
                        
                        ui.button("Salvar Limites", on_click=salvar_unificado, icon='save').classes('w-full mt-2').style(
                            f'background: {cor_primaria} !important; color: white !important; border-radius: 8px; font-weight: 600;'
                        )
                
                else:
                    # MODO INDIVIDUAL - Cada cartão tem seus limites
                    with container_limites:
                        with ui.card().classes('dica-card mt-2').style('background: #faf5ff; border-left: 3px solid #8b5cf6;'):
                            with ui.row().classes('items-start gap-2'):
                                ui.icon('account_balance_wallet').classes('text-sm mt-0.5').style('color: #8b5cf6 !important;')
                                with ui.column().classes('gap-1'):
                                    ui.label("🔹 Modo Individual").classes('text-xs font-semibold text-purple-700')
                                    ui.label("• Cada cartão tem seu próprio limite e controle").classes('text-[11px] text-gray-600')
                                    ui.label("• Cadastre seus cartões na aba '💳 Cartões'").classes('text-[11px] text-gray-600')
                                    ui.label("• Filtre gastos por cartão na tela principal").classes('text-[11px] text-gray-600')
                                    ui.label("• Ideal para quem tem múltiplos cartões").classes('text-[11px] text-gray-600')
                                    
                                    cartoes = dados.get("cartoes", [])
                                    if not cartoes:
                                        with ui.card().classes('p-3 mt-2 rounded').style('background: #fef3c7; border: 1px solid #f59e0b;'):
                                            with ui.row().classes('items-start gap-2'):
                                                ui.icon('warning').classes('text-sm mt-0.5').style('color: #f59e0b !important;')
                                                with ui.column().classes('gap-1'):
                                                    ui.label("⚠️ Nenhum cartão cadastrado!").classes('text-xs font-semibold text-yellow-700')
                                                    ui.label("Vá na aba '💳 Cartões' para cadastrar seus cartões com limites individuais.").classes('text-[10px] text-yellow-600')
                                    else:
                                        with ui.card().classes('p-3 mt-2 rounded').style('background: #ecfdf5; border: 1px solid #10b981;'):
                                            with ui.row().classes('items-start gap-2'):
                                                ui.icon('check_circle').classes('text-sm mt-0.5').style('color: #10b981 !important;')
                                                with ui.column().classes('gap-1'):
                                                    ui.label(f"✅ {len(cartoes)} cartão(ões) cadastrado(s)").classes('text-xs font-semibold text-green-700')
                                                    ui.label("Os limites são gerenciados individualmente na aba de cartões.").classes('text-[10px] text-green-600')
                                        
                                        # Mostrar resumo dos cartões
                                        for c in cartoes:
                                            with ui.card().classes('dica-card mt-2').style('background: #f9fafb;'):
                                                with ui.row().classes('items-center justify-between'):
                                                    ui.label(f"💳 {c.get('nome', '')}").classes('text-sm font-semibold')
                                                    with ui.column().classes('gap-0 items-end'):
                                                        ui.label(f"Limite: {config_service.formatar_valor(c.get('limite_total', 0))}").classes('text-xs text-gray-600')
                                                        ui.label(f"Fecha dia {c.get('dia_fechamento', 10)}").classes('text-[10px] text-gray-400')
                        
                        def salvar_individual():
                            atualizar_config(modo_cartao=modo_cartao.value)
                            ui.notify("✅ Modo Individual ativado! Configure os cartões na aba Cartões.", type="positive", position="top", timeout=2000)
                            recarregar_principal()
                        
                        ui.button("Salvar Modo", on_click=salvar_individual, icon='save').classes('w-full mt-2').style(
                            f'background: {cor_primaria} !important; color: white !important; border-radius: 8px; font-weight: 600;'
                        )
            
            # ============================================================
            # EVENTO DE MUDANÇA
            # ============================================================
            modo_cartao.on('update:model-value', lambda e: atualizar_campos_limites())
            
            # Renderizar campos iniciais
            atualizar_campos_limites()
    
    # =========================
    # RENDER: CARTÕES
    # =========================
    def render_cartoes():
        cartoes = dados.get("cartoes", [])
        
        def abrir_form_cartao(cartao=None):
            is_edicao = cartao is not None
            with ui.dialog() as form_dialog, ui.card().classes('w-[400px] max-w-[90vw] p-4 rounded-xl'):
                with ui.row().classes('items-center gap-2 mb-3'):
                    ui.icon('credit_card').classes('text-lg').style(f'color: {cor_primaria} !important;')
                    ui.label("Editar Cartão" if is_edicao else "Novo Cartão").classes('text-lg font-bold')
                
                nome_inp = ui.input("Nome do Cartão", value=cartao.get("nome", "") if is_edicao else "").props('outlined dense').classes('w-full mb-2')
                limite_inp = ui.number("Limite Total (R$)", value=cartao.get("limite_total", 0) if is_edicao else 0, format="%.2f").props('outlined dense prefix=R$').classes('w-full mb-2')
                parc_inp = ui.number("Limite Parcelado (R$)", value=cartao.get("limite_parcelado", 0) if is_edicao else 0, format="%.2f").props('outlined dense prefix=R$').classes('w-full mb-2')
                dia_inp = ui.select(options=list(range(1, 32)), label="Dia Fechamento", value=cartao.get("dia_fechamento", 10) if is_edicao else 10).props('outlined dense').classes('w-full mb-3')
                
                def salvar_cartao():
                    if not nome_inp.value:
                        ui.notify("⚠️ Informe o nome do cartão", type="warning", position="top")
                        return
                    if is_edicao:
                        atualizar_cartao(cartao["id"], nome=nome_inp.value, limite_total=float(limite_inp.value or 0), limite_parcelado=float(parc_inp.value or 0), dia_fechamento=int(dia_inp.value or 10))
                    else:
                        adicionar_cartao(nome_inp.value, limite_inp.value or 0, parc_inp.value, dia_inp.value)
                    carregar_dados()
                    form_dialog.close()
                    ui.notify("✅ Cartão salvo!", type="positive", position="top", timeout=1000)
                    recarregar_principal()
                
                with ui.row().classes('justify-end gap-2 mt-2'):
                    ui.button("Cancelar", on_click=form_dialog.close).props('outline').style(f'color: {cor_primaria} !important; border-color: {cor_primaria} !important; border-radius: 8px;')
                    ui.button("Salvar", on_click=salvar_cartao, icon='save').style(f'background: {cor_primaria} !important; color: white !important; border-radius: 8px; font-weight: 600;')
            form_dialog.open()
        
        def remover_cartao_conf(cartao):
            def confirmar():
                remover_cartao(cartao.get("id"))
                carregar_dados()
                ui.notify("🗑️ Cartão removido!", type="warning", position="top", timeout=1000)
                confirm_dialog.close()
                recarregar_principal()
            
            with ui.dialog() as confirm_dialog, ui.card().classes('w-[320px] p-4 rounded-xl'):
                with ui.row().classes('items-center gap-2 mb-3'):
                    ui.icon('warning').classes('text-lg').style(f'color: {cor_primaria} !important;')
                    ui.label("Excluir cartão?").classes('text-lg font-bold')
                ui.label(f"{cartao.get('nome')}").classes('text-sm text-gray-500')
                with ui.row().classes('justify-end gap-2 mt-4'):
                    ui.button("Cancelar", on_click=confirm_dialog.close).props('outline').style(f'color: {cor_primaria} !important; border-color: {cor_primaria} !important; border-radius: 8px;')
                    ui.button("Excluir", on_click=confirmar).style(f'background: {cor_primaria} !important; color: white !important; border-radius: 8px; font-weight: 600;')
            confirm_dialog.open()
        
        with ui.card().classes('config-card'):
            with ui.card().classes('dica-card').style(f'background: {cor_primaria}08; border-left: 3px solid {cor_primaria};'):
                with ui.row().classes('items-start gap-2'):
                    ui.icon('info').classes('text-sm mt-0.5').style(f'color: {cor_primaria} !important;')
                    with ui.column().classes('gap-1'):
                        ui.label("💡 Controle individual").classes('text-xs font-semibold').style(f'color: {cor_primaria} !important;')
                        ui.label("Cadastre cada cartão com seu limite. No modo Individual, você pode filtrar gastos por cartão na tela principal.").classes('text-[11px] text-gray-600')
            
            with ui.row().classes('items-center justify-between mb-3'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('credit_card').classes('text-lg').style(f'color: {cor_primaria} !important;')
                    ui.label("Cartões").classes('text-base font-bold')
                ui.button("+ Novo Cartão", on_click=lambda: abrir_form_cartao(), icon='add').classes('btn-sm').style(f'background: {cor_primaria} !important; color: white !important;')
            
            if not cartoes:
                ui.label("Nenhum cartão cadastrado").classes('text-sm text-gray-400 text-center p-4')
                return
            
            for c in cartoes:
                with ui.card().classes('cartao-card'):
                    with ui.row().classes('items-center justify-between w-full'):
                        with ui.column().classes('gap-0 flex-1'):
                            ui.label(c.get("nome", "")).classes('text-sm font-semibold text-gray-800')
                            ui.label(f"Limite: {config_service.formatar_valor(c.get('limite_total', 0))}").classes('text-[11px] text-gray-500')
                            ui.label(f"Fecha dia {c.get('dia_fechamento', 10)}").classes('text-[10px] text-gray-400')
                        with ui.row().classes('gap-1'):
                            ui.button(icon='edit', on_click=lambda c=c: abrir_form_cartao(c)).props('flat round size=sm').style(f'color: {cor_primaria} !important;')
                            ui.button(icon='delete', on_click=lambda c=c: remover_cartao_conf(c)).props('flat round size=sm').style(f'color: {cor_primaria} !important;')
    
    # =========================
    # RENDER: TEMA
    # =========================
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
            with ui.card().classes('dica-card').style(f'background: {cor_primaria}08; border-left: 3px solid {cor_primaria};'):
                with ui.row().classes('items-start gap-2'):
                    ui.icon('info').classes('text-sm mt-0.5').style(f'color: {cor_primaria} !important;')
                    with ui.column().classes('gap-1'):
                        ui.label("🎨 Personalização").classes('text-xs font-semibold').style(f'color: {cor_primaria} !important;')
                        ui.label("Escolha a cor principal do sistema. Ela será aplicada em botões, ícones e destaques em todo o aplicativo.").classes('text-[11px] text-gray-600')
            
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
    
    # =========================
    # RENDER: FIXOS
    # =========================
    def render_fixos():
        fixos = dados.get("fixos", [])
        categorias = dados.get("categorias", CATEGORIAS_PADRAO)
        categorias_nomes = [c["nome"] for c in categorias]
        
        def remover_fixo(gid):
            remover_gasto(gid)
            ui.notify("🗑️ Removido!", type="warning", position="top", timeout=1000)
            recarregar_principal()
        
        with ui.card().classes('config-card'):
            with ui.card().classes('dica-card').style(f'background: {cor_primaria}08; border-left: 3px solid {cor_primaria};'):
                with ui.row().classes('items-start gap-2'):
                    ui.icon('info').classes('text-sm mt-0.5').style(f'color: {cor_primaria} !important;')
                    with ui.column().classes('gap-1'):
                        ui.label("💡 Gastos recorrentes").classes('text-xs font-semibold').style(f'color: {cor_primaria} !important;')
                        ui.label("Streaming, academias, assinaturas. Eles sempre aparecem nos lançamentos e são contabilizados nos limites mensais.").classes('text-[11px] text-gray-600')
            
            with ui.row().classes('items-center justify-between mb-3'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('repeat').classes('text-lg').style(f'color: {cor_primaria} !important;')
                    ui.label("Gastos Fixos").classes('text-base font-bold')
                total = sum(g.get("valor", 0) for g in fixos)
                ui.label(config_service.formatar_valor(total)).classes('text-sm font-bold').style(f'color: {cor_primaria} !important;')
            
            if fixos:
                for g in fixos:
                    with ui.card().classes('fixo-card'):
                        with ui.row().classes('justify-between items-center w-full'):
                            with ui.column().classes('gap-0 flex-1'):
                                ui.label(g.get("descricao", "")).classes('text-sm font-semibold text-gray-800')
                                if g.get("categoria"): ui.label(g.get("categoria")).classes('text-[10px] text-purple-500')
                            with ui.row().classes('items-center gap-3'):
                                ui.label(config_service.formatar_valor(g.get("valor", 0))).classes('text-sm font-bold').style(f'color: {cor_primaria} !important;')
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
                        adicionar_gasto(descricao=di.value.strip(), valor=vi.value, tipo="Fixo", categoria=ci.value)
                        ui.notify("✅ Adicionado!", type="positive", position="top", timeout=1000)
                        recarregar_principal()
                    
                    ui.button("Adicionar", on_click=add_fixo, icon='add').classes('w-full').style(f'background: {cor_primaria} !important; color: white !important; border-radius: 8px; font-weight: 600;')
    
    # =========================
    # RENDER: USUÁRIOS
    # =========================
    def render_usuarios():
        carregar_usuarios()
        usuarios = usuarios_ref["lista"]
        
        def confirmar_exclusao(usuario):
            def confirmar():
                usuarios_ref["lista"] = [u for u in usuarios_ref["lista"] if u.get("id") != usuario.get("id")]
                salvar_usuarios()
                ui.notify("🗑️ Usuário removido!", type="warning", position="top", timeout=1000)
                confirm_dialog.close()
                recarregar_principal()
            
            with ui.dialog() as confirm_dialog, ui.card().classes('w-[320px] p-4 rounded-xl'):
                with ui.row().classes('items-center gap-2 mb-3'):
                    ui.icon('warning').classes('text-lg').style(f'color: {cor_primaria} !important;')
                    ui.label("Excluir usuário?").classes('text-lg font-bold')
                ui.label(f"{usuario.get('nome')} - {usuario.get('email')}").classes('text-sm text-gray-500')
                with ui.row().classes('justify-end gap-2 mt-4'):
                    ui.button("Cancelar", on_click=confirm_dialog.close).props('outline').style(f'color: {cor_primaria} !important; border-color: {cor_primaria} !important; border-radius: 8px;')
                    ui.button("Excluir", on_click=confirmar).style(f'background: {cor_primaria} !important; color: white !important; border-radius: 8px; font-weight: 600;')
            confirm_dialog.open()
        
        def abrir_form_usuario(usuario=None):
            is_edicao = usuario is not None
            avatar_selecionado = [usuario.get("avatar_emoji", "🐶") if is_edicao else "🐶"]
            
            with ui.dialog() as form_dialog, ui.card().classes('w-[400px] max-w-[90vw] p-4 rounded-xl'):
                with ui.row().classes('items-center gap-2 mb-4'):
                    ui.icon('person').classes('text-lg').style(f'color: {cor_primaria} !important;')
                    ui.label("Editar Usuário" if is_edicao else "Novo Usuário").classes('text-lg font-bold')
                
                nome_inp = ui.input("Nome completo", value=usuario.get("nome", "") if is_edicao else "").props('outlined dense').classes('w-full mb-3')
                email_inp = ui.input("E-mail", value=usuario.get("email", "") if is_edicao else "").props('outlined dense').classes('w-full mb-3')
                role_inp = ui.select(["admin", "visitante"], label="Função", value=usuario.get("role", "visitante") if is_edicao else "visitante").props('outlined dense').classes('w-full mb-3')
                senha_inp = ui.input("Senha" if not is_edicao else "Nova senha (deixe vazio para manter)", password=True).props('outlined dense').classes('w-full mb-4')
                
                with ui.card().classes('dica-card mb-3').style(f'background: {cor_primaria}08; border-left: 3px solid {cor_primaria};'):
                    ui.label("👤 Escolha um avatar que te represente").classes('text-[11px] text-gray-600')
                
                avatares_refs = []
                with ui.element('div').classes('avatares-grid mb-4'):
                    for av in AVATARES:
                        is_sel = av == avatar_selecionado[0]
                        av_div = ui.element('div').classes(f'avatar-option {"selected" if is_sel else ""}')
                        if is_sel:
                            av_div.style(f'border-color: {cor_primaria} !important; background: {cor_primaria}15 !important; box-shadow: 0 0 0 3px {cor_primaria}30 !important;')
                        with av_div: ui.label(av)
                        av_div.on('click', lambda a=av: selecionar_avatar(a))
                        avatares_refs.append((av_div, av))
                
                def selecionar_avatar(a):
                    avatar_selecionado[0] = a
                    for div, av in avatares_refs:
                        if av == a:
                            div.classes('selected')
                            div.style(f'border-color: {cor_primaria} !important; background: {cor_primaria}15 !important; box-shadow: 0 0 0 3px {cor_primaria}30 !important; transform: scale(1.05) !important;')
                        else:
                            div.classes(remove='selected')
                            div.style('border-color: #e5e7eb !important; background: white !important; box-shadow: none !important; transform: scale(1) !important;')
                
                def salvar():
                    if not nome_inp.value or not email_inp.value:
                        ui.notify("⚠️ Nome e email são obrigatórios", type="warning", position="top")
                        return
                    if not is_edicao and not senha_inp.value:
                        ui.notify("⚠️ Informe uma senha", type="warning", position="top")
                        return
                    
                    if is_edicao:
                        usuario["nome"] = nome_inp.value
                        usuario["email"] = email_inp.value
                        usuario["role"] = role_inp.value
                        usuario["avatar_emoji"] = avatar_selecionado[0]
                        usuario["avatar"] = avatar_selecionado[0]
                        if senha_inp.value: usuario["senha"] = hash_senha(senha_inp.value)
                    else:
                        novo_id = max([u.get("id", 0) for u in usuarios_ref["lista"]]) + 1 if usuarios_ref["lista"] else 1
                        usuarios_ref["lista"].append({
                            "id": novo_id, "nome": nome_inp.value, "email": email_inp.value,
                            "senha": hash_senha(senha_inp.value), "role": role_inp.value,
                            "avatar_emoji": avatar_selecionado[0], "avatar": avatar_selecionado[0],
                            "ativo": True, "data_cadastro": datetime.now().isoformat()
                        })
                    
                    salvar_usuarios()
                    form_dialog.close()
                    ui.notify("✅ Usuário salvo!", type="positive", position="top", timeout=1000)
                    recarregar_principal()
                
                with ui.row().classes('justify-end gap-2 mt-2'):
                    ui.button("Cancelar", on_click=form_dialog.close).props('outline').style(f'color: {cor_primaria} !important; border-color: {cor_primaria} !important; border-radius: 8px;')
                    ui.button("Salvar", on_click=salvar, icon='save').style(f'background: {cor_primaria} !important; color: white !important; border-radius: 8px; font-weight: 600;')
            form_dialog.open()
        
        with ui.card().classes('config-card'):
            with ui.card().classes('dica-card').style(f'background: {cor_primaria}08; border-left: 3px solid {cor_primaria};'):
                with ui.row().classes('items-start gap-2'):
                    ui.icon('info').classes('text-sm mt-0.5').style(f'color: {cor_primaria} !important;')
                    with ui.column().classes('gap-1'):
                        ui.label("👥 Gerenciamento de acesso").classes('text-xs font-semibold').style(f'color: {cor_primaria} !important;')
                        ui.label("Admin tem acesso total. Visitante pode visualizar mas não alterar configurações do sistema.").classes('text-[11px] text-gray-600')
            
            with ui.row().classes('items-center justify-between mb-4'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('people').classes('text-lg').style(f'color: {cor_primaria} !important;')
                    ui.label("Usuários").classes('text-base font-bold')
                ui.button("+ Novo", on_click=lambda: abrir_form_usuario(), icon='person_add').classes('btn-sm').style(f'background: {cor_primaria} !important; color: white !important;')
            
            if not usuarios:
                ui.label("Nenhum usuário cadastrado").classes('text-sm text-gray-400 text-center p-4')
                return
            
            for u in usuarios:
                with ui.card().classes('usuario-card'):
                    with ui.row().classes('items-center justify-between w-full'):
                        with ui.row().classes('items-center gap-3 flex-1'):
                            with ui.element('div').classes('w-10 h-10 rounded-full flex items-center justify-center').style(f'background: {cor_primaria}15 !important;'):
                                ui.label(u.get("avatar_emoji", "👤")).classes('text-xl')
                            with ui.column().classes('gap-0'):
                                ui.label(u.get("nome", "-")).classes('text-sm font-semibold text-gray-800')
                                ui.label(u.get("email", "-")).classes('text-[11px] text-gray-500')
                                role = u.get("role", "visitante")
                                ui.label(role.upper()).classes('text-[10px] font-bold').style(f'color: {cor_primaria} !important;' if role == "admin" else 'color: #6b7280 !important;')
                        with ui.row().classes('gap-1'):
                            ui.button(icon='edit', on_click=lambda u=u: abrir_form_usuario(u)).props('flat round size=sm').style(f'color: {cor_primaria} !important;')
                            ui.button(icon='delete', on_click=lambda u=u: confirmar_exclusao(u)).props('flat round size=sm').style(f'color: {cor_primaria} !important;')
    
    # =========================
    # RENDER: SOBRE
    # =========================
    def render_sobre():
        # Logo em destaque (URL Cloudinary)
        with ui.element('div').classes('sobre-logo-container'):
            ui.image(LOGO_COMPLETA).classes('sobre-logo')
        
        # Informações do App
        with ui.card().classes('config-card'):
            with ui.row().classes('items-center justify-between mb-4'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('info').classes('text-lg').style(f'color: {cor_primaria} !important;')
                    ui.label("Informações do App").classes('text-base font-bold')
                with ui.element('div').classes('sobre-badge').style(f'background: {cor_primaria} !important;'):
                    ui.icon('check_circle').classes('text-xs')
                    ui.label("v2.0.0")
            
            info_items = [
                ("Nome do App", "Cartometro"),
                ("Slogan", "Controle Inteligente do seu Crédito"),
                ("Versão", "2.0.0 - Estável"),
                ("Data de Lançamento", "Janeiro 2025"),
            ]
            
            for label, valor in info_items:
                with ui.element('div').classes('sobre-info-item').style(f'border-left-color: {cor_primaria} !important;'):
                    ui.label(label).classes('sobre-info-label')
                    ui.label(valor).classes('sobre-info-value')
        
        # Desenvolvedor
        with ui.card().classes('config-card'):
            with ui.row().classes('items-center gap-2 mb-4'):
                ui.icon('code').classes('text-lg').style(f'color: {cor_primaria} !important;')
                ui.label("Desenvolvedor").classes('text-base font-bold')
            
            dev_items = [
                ("Desenvolvido por", "Cartometro Tech"),
                ("Contato", "suporte@cartometro.app"),
                ("Website", "www.cartometro.app"),
            ]
            
            for label, valor in dev_items:
                with ui.element('div').classes('sobre-info-item').style(f'border-left-color: {cor_primaria} !important;'):
                    ui.label(label).classes('sobre-info-label')
                    ui.label(valor).classes('sobre-info-value')
        
        # Tecnologias
        with ui.card().classes('config-card'):
            with ui.row().classes('items-center gap-2 mb-4'):
                ui.icon('build').classes('text-lg').style(f'color: {cor_primaria} !important;')
                ui.label("Tecnologias").classes('text-base font-bold')
            
            tech_items = [
                ("Framework", "NiceGUI + Quasar Framework"),
                ("Linguagem", "Python 3.10+"),
                ("Banco de Dados", "JSON (Local)"),
            ]
            
            for label, valor in tech_items:
                with ui.element('div').classes('sobre-info-item').style(f'border-left-color: {cor_primaria} !important;'):
                    ui.label(label).classes('sobre-info-label')
                    ui.label(valor).classes('sobre-info-value')
        
        # Funcionalidades
        with ui.card().classes('config-card'):
            with ui.row().classes('items-center gap-2 mb-4'):
                ui.icon('star').classes('text-lg').style(f'color: {cor_primaria} !important;')
                ui.label("Principais Funcionalidades").classes('text-base font-bold')
            
            funcionalidades = [
                "📊 Dashboard financeiro em tempo real",
                "💳 Controle de cartão de crédito (Unificado/Individual)",
                "📅 Gestão por ciclo de fatura ou mês",
                "🔁 Gastos fixos e parcelados",
                "🎯 Metas e limites personalizados",
                "🤖 Consultor Financeiro Inteligente (30+ regras)",
                "🎨 Temas personalizáveis (8 cores)",
                "👥 Suporte a múltiplos usuários",
                "📱 Interface 100% responsiva (Desktop + Mobile)",
                "🔔 Notificações e alertas inteligentes",
            ]
            
            for func in funcionalidades:
                with ui.element('div').classes('sobre-func-item'):
                    ui.icon('check_circle').classes('text-xs').style(f'color: {cor_primaria} !important;')
                    ui.label(func).classes('text-sm text-gray-700')
        
        # Copyright
        with ui.card().classes('config-card').style('text-align: center;'):
            ui.label("© 2025 Cartometro").classes('text-sm font-semibold text-gray-600')
            ui.label("Todos os direitos reservados.").classes('text-xs text-gray-400 mt-1')
            ui.label("Feito com ❤️ para você controlar suas finanças").classes('text-xs text-gray-400 mt-2')
    
    # =========================
    # ATUALIZAÇÃO
    # =========================
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
            elif aba == "usuarios": render_usuarios()
            elif aba == "sobre": render_sobre()
    
    def mudar_aba(aba, btns):
        aba_ativa["atual"] = aba
        for nome, btn in btns.items():
            btn.classes(remove='active')
            btn.style('color: #6b7280 !important; background: transparent !important; border-bottom: 2px solid transparent !important;')
        if aba in btns:
            btns[aba].classes('active')
            btns[aba].style(f'color: {cor_primaria} !important; font-weight: 600 !important; border-bottom: 2px solid {cor_primaria} !important; background: {cor_primaria}10 !important;')
        atualizar_conteudo()
    
    # =========================
    # MONTAR INTERFACE
    # =========================
    def montar_interface():
        nonlocal tab_content
        config = dados.get("config", {})
        modo = config.get("modo_cartao", "Unificado")
        
        abas_list = [
            ("limites", "⚙️ Limites"),
            ("tema", "🎨 Tema"),
            ("fixos", "🔁 Fixos"),
            ("usuarios", "👥 Users"),
            ("sobre", "ℹ️ Sobre"),
        ]
        if modo == "Individual":
            abas_list.insert(1, ("cartoes", "💳 Cartões"))
        
        with ui.element('div').classes('config-tela'):
            with ui.element('div').classes('config-header'):
                with ui.row().classes('w-full items-center justify-between p-3').style(f'background: linear-gradient(135deg, {cor_escura}, {cor_primaria}) !important;'):
                    with ui.row().classes('items-center gap-2'):
                        ui.button(icon='arrow_back', on_click=recarregar_principal).props('flat round').style('color: white !important;')
                        with ui.element('div').classes('w-8 h-8 rounded-full flex items-center justify-center').style('background: rgba(255,255,255,0.2) !important;'):
                            ui.icon('settings').classes('text-sm text-white')
                        ui.label("Configurações").classes('text-lg font-bold text-white')
            
            ui.element('div').style(f'height: 3px; background: linear-gradient(90deg, {cor_primaria}, {cor_primaria}60, transparent); position: relative; flex-shrink: 0;')
            
            with ui.element('div').classes('tabs-container'):
                tabs = {}
                for nome, label in abas_list:
                    is_active = nome == aba_ativa["atual"]
                    btn = ui.label(label).classes(f'tab-btn {"active" if is_active else ""}')
                    if is_active:
                        btn.style(f'color: {cor_primaria} !important; font-weight: 600 !important; border-bottom: 2px solid {cor_primaria} !important; background: {cor_primaria}10 !important;')
                    btn.on('click', lambda n=nome: mudar_aba(n, tabs))
                    tabs[nome] = btn
            
            with ui.element('div').classes('config-scroll'):
                tab_content = ui.column().classes('w-full')
                atualizar_conteudo()
    
    montar_interface()


__all__ = ['tela_configuracoes']