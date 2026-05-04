"""
Tela de Lançamentos - Cartometro
Versão Mobile com Consultor Financeiro Inteligente
"""

from nicegui import ui, app
from db import (
    carregar, salvar, remover_gasto, adicionar_gasto,
    verificar_limite_lancamentos, get_usuario_logado_email,
    get_plano_usuario, tem_consultor_premium
)
from config_service import config_service
from auth_service import get_usuario_logado
from datetime import datetime, timedelta
from collections import defaultdict
from constantes import (
    GASTO_AVISTA, GASTO_PARCELADO, GASTO_FIXO,
    CORES_TIPOS, ICONES_TIPOS, CATEGORIAS_PADRAO
)

ARQUIVO = "dados.json"

# ============================================================
# URLS DAS IMAGENS (CLOUDINARY)
# ============================================================
LOGO_COMPLETA = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845630/logo_full_branca_wlx97y.png"


CUSTOM_CSS = """
<style>
.q-dialog__inner { padding: 0 !important; margin: 0 !important; }
.mobile-dialog { width: 90vw !important; max-width: 500px !important; height: auto !important; max-height: 85vh !important; margin: 0 auto !important; border-radius: 20px !important; display: flex !important; flex-direction: column !important; }
.q-card { margin: 0 !important; border-radius: 0 !important; box-shadow: none !important; }
.dialog-scroll { flex: 1 !important; overflow-y: auto !important; overflow-x: hidden !important; }
.dialog-scroll::-webkit-scrollbar { width: 4px; }
.dialog-scroll::-webkit-scrollbar-track { background: #e5e7eb; }
.dialog-scroll::-webkit-scrollbar-thumb { background: #9ca3af; border-radius: 4px; }
.botoes-fixos { flex-shrink: 0 !important; background: white !important; border-top: 1px solid #e5e7eb !important; z-index: 10 !important; }

.lancamentos-tela { position: fixed !important; top: 0; left: 0; right: 0; bottom: 0; width: 100% !important; height: 100% !important; display: flex !important; flex-direction: column !important; background: #f3f4f6 !important; overflow: hidden !important; }
.lancamentos-header-fixo { flex-shrink: 0 !important; width: 100% !important; z-index: 10 !important; }
.header-bar { padding: 8px 14px !important; box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important; }
.header-subtitle-text { font-size: 9px !important; opacity: 0.7 !important; line-height: 1 !important; }
.header-icon-btn { width: 28px; height: 28px; min-width: 28px; padding: 0 !important; border-radius: 50% !important; }

.limite-badge {
    display: inline-flex !important;
    align-items: center !important;
    gap: 3px !important;
    padding: 2px 8px !important;
    border-radius: 10px !important;
    font-size: 9px !important;
    font-weight: 600 !important;
    background: rgba(255,255,255,0.2) !important;
    color: white !important;
}

.busca-row { padding: 4px 8px !important; background: white !important; display: flex; align-items: center; gap: 4px; }
.busca-row .q-field__native, .busca-row .q-field__control { min-height: 32px !important; font-size: 13px !important; }

.filtros-compactos { padding: 6px 8px !important; background: white !important; border-top: 1px solid #f3f4f6; display: flex; gap: 6px; align-items: center; flex-wrap: wrap; }
.filtros-compactos .q-field { margin: 0 !important; padding: 0 !important; }
.filtros-compactos .q-field__native, .filtros-compactos .q-field__control { min-height: 30px !important; font-size: 12px !important; }

.lancamentos-rolagem { flex: 1 !important; overflow-y: auto; overflow-x: hidden; padding-bottom: 64px !important; }
.lancamentos-rolagem::-webkit-scrollbar { width: 4px; }
.lancamentos-rolagem::-webkit-scrollbar-track { background: #e5e7eb; }
.lancamentos-rolagem::-webkit-scrollbar-thumb { background: #9ca3af; border-radius: 4px; }

.kpi-grid { display: grid !important; grid-template-columns: repeat(3, 1fr); gap: 6px; padding: 8px 8px 2px 8px; width: 100%; }
.kpi-card { padding: 10px 8px !important; background: white !important; border-radius: 10px !important; border-left: 3px solid #ccc !important; box-shadow: 0 1px 2px rgba(0,0,0,0.04) !important; }
.kpi-icon { font-size: 18px !important; margin-bottom: 2px !important; }
.kpi-label { font-size: 8px !important; color: #6b7280; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 600; margin-bottom: 1px; }
.kpi-valor { font-size: 13px !important; font-weight: 700; color: #1f2937; line-height: 1.2; }

.progresso-container { padding: 2px 8px 6px 8px; width: 100%; }
.progresso-card { width: 100% !important; padding: 10px 12px !important; border-radius: 10px; background: white; box-shadow: 0 1px 2px rgba(0,0,0,0.04); }
.progresso-label { font-size: 11px !important; color: #6b7280; font-weight: 500; }
.progresso-percentual { font-size: 14px !important; font-weight: 700; }
.barra-container { width: 100%; height: 6px; border-radius: 3px; background: #e5e7eb; overflow: hidden; }
.barra-preenchimento { height: 100%; border-radius: 3px; transition: width 0.3s ease; }

.lancamento-card { padding: 12px 14px !important; background: white; cursor: pointer; transition: all 0.15s; border-radius: 8px; margin: 0 8px 4px 8px; width: calc(100% - 16px); box-shadow: 0 1px 2px rgba(0,0,0,0.04); border-left: 4px solid #ccc; }
.lancamento-card:active { background: #f9fafb; transform: scale(0.99); }
.lancamento-card-fixo { padding: 12px 14px !important; background: #faf5ff; cursor: default; border-radius: 8px; margin: 0 8px 4px 8px; width: calc(100% - 16px); box-shadow: 0 1px 2px rgba(0,0,0,0.04); border-left: 4px solid #a855f7; }

.dia-header { padding: 8px 12px 2px 12px; width: 100%; }
.dia-titulo { font-size: 10px !important; font-weight: 600; color: #6b7280; text-transform: uppercase; letter-spacing: 0.3px; }
.dia-total { font-size: 10px !important; font-weight: 700; }
.lancamento-desc { font-size: 14px !important; font-weight: 500; color: #1f2937; line-height: 1.3; }
.lancamento-detalhe { font-size: 11px !important; color: #9ca3af; }
.lancamento-valor { font-size: 14px !important; font-weight: 600; }
.chevron-icon { font-size: 14px !important; color: #d1d5db; }
.estado-vazio { padding: 40px 20px; text-align: center; }

.fab-button { position: fixed !important; bottom: 72px; right: 16px; z-index: 999; width: 50px; height: 50px; border-radius: 25px; box-shadow: 0 4px 16px rgba(0,0,0,0.2); display: flex; align-items: center; justify-content: center; }

.bottom-nav-bar { position: fixed !important; bottom: 0; left: 0; right: 0; height: 56px; background: white; border-top: 1px solid #e5e7eb; display: flex; align-items: center; justify-content: space-around; z-index: 100; padding: 0 4px; box-shadow: 0 -2px 10px rgba(0,0,0,0.05); }
.bottom-nav-item { display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2px; padding: 4px 10px; cursor: pointer; transition: all 0.15s; border-radius: 8px; min-width: 48px; border: none; background: transparent; }
.bottom-nav-item:hover { background: #f3f4f6; }
.bottom-nav-icon { font-size: 20px !important; }
.bottom-nav-label { font-size: 9px !important; font-weight: 500; color: #6b7280; }
.bottom-nav-item.active .bottom-nav-label { color: var(--cor-primaria, #3b82f6) !important; font-weight: 600; }

.toggle-container { display: flex; border-radius: 8px; overflow: hidden; border: 1.5px solid #e5e7eb; height: 32px; }
.toggle-btn { padding: 0 14px; display: flex; align-items: center; justify-content: center; cursor: pointer; font-size: 11px; font-weight: 600; transition: all 0.15s; white-space: nowrap; }

.notificacoes-container { position: relative; }
.notif-badge { position: absolute; top: -2px; right: -2px; width: 16px; height: 16px; border-radius: 50%; background: #ef4444; color: white; font-size: 9px; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.notif-popup { width: 400px; max-width: 92vw; max-height: 75vh; overflow-y: auto; border-radius: 16px; }
.notif-item { padding: 12px 14px; border-bottom: 1px solid #f3f4f6; cursor: pointer; transition: background 0.15s; }
.notif-item:hover { background: #f9fafb; }
.notif-item-lida { opacity: 0.5; }
.notif-icone { font-size: 20px; width: 38px; height: 38px; border-radius: 50%; display: flex; align-items: center; justify-content: center; flex-shrink: 0; }
.notif-titulo { font-size: 12px; font-weight: 600; color: #1f2937; line-height: 1.3; }
.notif-descricao { font-size: 11px; color: #6b7280; line-height: 1.4; }
.notif-tempo { font-size: 10px; color: #9ca3af; }
.notif-categoria { font-size: 9px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 2px; }

.q-field--outlined.q-field--focused .q-field__control:before { border-color: var(--cor-primaria) !important; }
.q-field--outlined.q-field--focused .q-field__control:after { border-color: var(--cor-primaria) !important; }
.q-field--focused .q-field__control { border-color: transparent !important; }
.q-field--focused .q-field__label { color: #374151 !important; }
.q-field--focused .q-field__native { color: #111827 !important; }
.q-item.q-manual-focusable--focused { background: var(--cor-primaria) !important; color: white !important; }
.q-date__today { color: var(--cor-primaria) !important; font-weight: bold !important; }
.q-date__day--selected { background: var(--cor-primaria) !important; color: white !important; }

@media (max-width: 768px) { .mobile-dialog { width: 100vw !important; max-width: 100vw !important; border-radius: 0 !important; } }
</style>
"""


def tela_lancamentos(container):
    
    container.clear()
    container.classes('p-0 m-0')
    container.style('padding: 0 !important; margin: 0 !important; width: 100% !important; height: 100% !important;')
    
    ui.add_head_html(CUSTOM_CSS)
    
    cor_primaria = config_service.get_primary_color()
    cor_escura = config_service.get_primary_dark()
    
    ui.add_head_html(f'<style>:root {{ --cor-primaria: {cor_primaria}; }}</style>')
    
    hoje = datetime.now()
    tipo_filtro = "ciclo"
    filtro_mes = hoje.month
    filtro_ano = hoje.year
    filtro_busca = ""
    filtro_cartao = "Todos"
    botoes_toggle = {}
    
    kpi_container = None
    lista = None
    contador_label = None  # Para atualizar o contador de lançamentos
    
    # Persistência de notificações lidas
    if 'notif_lidas' not in app.storage.user:
        app.storage.user['notif_lidas'] = []
    notificacoes_lidas = set(app.storage.user['notif_lidas'])
    notif_badge = None
    
    # Info do plano
    email_logado = get_usuario_logado_email()
    plano_info = get_plano_usuario(email_logado) if email_logado else {}
    plano_nome = plano_info.get('nome', 'Gratuito')
    max_lanc = plano_info.get('max_lancamentos_mes', 20)
    consultor_premium = tem_consultor_premium(email_logado) if email_logado else False
    
    def carregar_dados():
        dados = carregar()
        categorias = dados.get("categorias", CATEGORIAS_PADRAO)
        gastos = dados.get("gastos", [])
        fixos = dados.get("fixos", [])
        cartoes = dados.get("cartoes", [])
        mapa_icones = {}
        mapa_cores = {}
        for c in categorias:
            nome = c.get("nome", "")
            mapa_icones[nome] = c.get("icone", "category")
            mapa_cores[nome] = c.get("cor", "#6b7280")
        return dados, categorias, gastos, fixos, cartoes, mapa_icones, mapa_cores
    
    dados, categorias, gastos, fixos, cartoes, mapa_icones, mapa_cores = carregar_dados()
    
    modo_cartao = dados.get("config", {}).get("modo_cartao", "Unificado")
    
    def get_cor_icone(categoria):
        return mapa_cores.get(categoria, "#6b7280"), mapa_icones.get(categoria, "category")
    
    def atualizar_dados():
        nonlocal dados, categorias, gastos, fixos, cartoes, mapa_icones, mapa_cores
        dados, categorias, gastos, fixos, cartoes, mapa_icones, mapa_cores = carregar_dados()
        atualizar_lista()
        atualizar_badge()
        atualizar_contador()
    
    def get_ciclo_atual():
        config = dados.get("config", {})
        dia_fechamento = config.get("dia_fechamento", 10)
        fim = datetime(filtro_ano, filtro_mes, dia_fechamento)
        if filtro_mes == 1:
            inicio = datetime(filtro_ano - 1, 12, dia_fechamento + 1)
        else:
            inicio = datetime(filtro_ano, filtro_mes - 1, dia_fechamento + 1)
        return inicio, fim
    
    def calcular_totais():
        config = dados.get("config", {})
        
        if modo_cartao == "Unificado":
            limite_total = config.get("limite_total", 3000)
            limite_parcelado = config.get("limite_parcelado", 1500)
        else:
            if filtro_cartao != "Todos":
                cartoes_filtrados = [c for c in cartoes if c.get("nome") == filtro_cartao]
            else:
                cartoes_filtrados = cartoes
            limite_total = sum(c.get("limite_total", 0) for c in cartoes_filtrados)
            limite_parcelado = sum(c.get("limite_parcelado", 0) for c in cartoes_filtrados)
        
        total_gasto = 0
        total_parcelado = 0
        
        if tipo_filtro == "ciclo":
            inicio, fim = get_ciclo_atual()
            for g in gastos:
                if modo_cartao == "Individual" and filtro_cartao != "Todos":
                    if g.get("cartao") != filtro_cartao: continue
                if g.get("data"):
                    try:
                        dt = datetime.strptime(g["data"], "%Y-%m-%d")
                        if inicio <= dt <= fim:
                            total_gasto += g.get("valor", 0)
                            if g.get("tipo") == GASTO_PARCELADO or g.get("parcelas", 1) > 1:
                                total_parcelado += g.get("valor", 0)
                    except: pass
        else:
            for g in gastos:
                if modo_cartao == "Individual" and filtro_cartao != "Todos":
                    if g.get("cartao") != filtro_cartao: continue
                if g.get("data"):
                    try:
                        dt = datetime.strptime(g["data"], "%Y-%m-%d")
                        if dt.month == filtro_mes and dt.year == filtro_ano:
                            total_gasto += g.get("valor", 0)
                            if g.get("tipo") == GASTO_PARCELADO or g.get("parcelas", 1) > 1:
                                total_parcelado += g.get("valor", 0)
                    except: pass
        
        for f in fixos:
            total_gasto += f.get("valor", 0)
        
        restante = limite_total - total_gasto
        return {
            "total_gasto": total_gasto, "total_parcelado": total_parcelado,
            "limite_total": limite_total, "limite_parcelado": limite_parcelado,
            "restante": restante,
            "percentual": (total_gasto / limite_total * 100) if limite_total > 0 else 0,
        }
    
    # ==========================================
    # CONTADOR DE LANÇAMENTOS
    # ==========================================
    def contar_lancamentos_mes():
        """Conta quantos lançamentos foram feitos este mês"""
        hoje = datetime.now()
        count = 0
        for g in gastos:
            if g.get('data'):
                try:
                    dt = datetime.strptime(g['data'], "%Y-%m-%d")
                    if dt.month == hoje.month and dt.year == hoje.year:
                        count += 1
                except:
                    pass
        return count
    
    def atualizar_contador():
        nonlocal contador_label
        if contador_label is None:
            return
        
        count = contar_lancamentos_mes()
        if max_lanc >= 9999:
            contador_label.set_text(f"📊 {count} lançamentos")
        else:
            contador_label.set_text(f"📊 {count}/{max_lanc} lançamentos")
            if count >= max_lanc:
                contador_label.style('background: rgba(239,68,68,0.3) !important;')
            elif count >= max_lanc * 0.8:
                contador_label.style('background: rgba(245,158,11,0.3) !important;')
            else:
                contador_label.style('background: rgba(255,255,255,0.2) !important;')
    
    # ==========================================
    # CONSULTOR FINANCEIRO
    # ==========================================
    from consultor import gerar_notificacoes
    
    def atualizar_badge():
        if notif_badge is None: return
        
        plano = "premium" if consultor_premium else "gratuito"
        notificacoes = gerar_notificacoes(dados, gastos, fixos, cartoes, plano=plano)
        nao_lidas = [n for n in notificacoes if n["id"] not in notificacoes_lidas]
        total = len(nao_lidas)
        if total > 0:
            notif_badge.style('display: flex')
            notif_badge.set_text(str(total))
        else:
            notif_badge.style('display: none')
    
    def abrir_notificacoes():
        plano = "premium" if consultor_premium else "gratuito"
        notificacoes = gerar_notificacoes(dados, gastos, fixos, cartoes, plano=plano)
        
        with ui.dialog() as notif_dialog, ui.card().classes('notif-popup p-0 gap-0'):
            with ui.row().classes('w-full items-center justify-between p-3').style(f'background: linear-gradient(135deg, {cor_escura}, {cor_primaria}) !important;'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon('notifications').classes('text-xl text-white')
                    
                    if consultor_premium:
                        ui.label("Consultor Premium").classes('text-white font-bold text-sm')
                    else:
                        ui.label("Consultor").classes('text-white font-bold text-sm')
                    
                    nao_lidas = len([n for n in notificacoes if n["id"] not in notificacoes_lidas])
                    ui.label(f"({nao_lidas} novas)").classes('text-white/70 text-xs')
                
                ui.button(icon='close', on_click=lambda: [notif_dialog.close(), atualizar_badge()]).props('flat').style('color: white !important;')
            
            # Banner upgrade para gratuito
            if not consultor_premium:
                with ui.card().classes('m-2 p-3').style('background: linear-gradient(135deg, #8b5cf6, #6366f1); border-radius: 10px;'):
                    with ui.row().classes('items-center justify-between'):
                        with ui.row().classes('items-center gap-2'):
                            ui.icon('star').classes('text-white')
                            ui.label("💎 Consultor Premium").classes('text-white text-sm font-bold')
                        ui.label("30+ alertas").classes('text-white/80 text-xs')
            
            with ui.element('div').style('max-height: 65vh; overflow-y: auto;'):
                if not notificacoes:
                    with ui.card().classes('p-8 text-center m-3'):
                        ui.icon('check_circle').classes('text-5xl text-green-400 mb-2')
                        ui.label("Tudo em ordem! 🎉").classes('text-base font-bold text-gray-600')
                        ui.label("Nenhuma notificação no momento.").classes('text-sm text-gray-400')
                else:
                    for n in notificacoes:
                        is_lida = n["id"] in notificacoes_lidas
                        with ui.card().classes(f'notif-item {"notif-item-lida" if is_lida else ""}').on('click', lambda nid=n["id"]: marcar_lida(nid)):
                            with ui.row().classes('items-start gap-3 w-full'):
                                with ui.element('div').classes('notif-icone').style(f'background: {n["cor"]}15;'):
                                    ui.label(n["icone"])
                                with ui.column().classes('gap-0 flex-1'):
                                    ui.label(n["categoria"]).classes('notif-categoria').style(f'color: {n["cor"]}')
                                    with ui.row().classes('justify-between items-center'):
                                        ui.label(n["titulo"]).classes('notif-titulo')
                                        ui.label(n["tempo"]).classes('notif-tempo')
                                    ui.label(n["descricao"]).classes('notif-descricao')
                                    if is_lida:
                                        ui.label("✓ Lida").classes('text-[9px] text-green-500 mt-1')
        
        def marcar_lida(nid):
            notificacoes_lidas.add(nid)
            app.storage.user['notif_lidas'] = list(notificacoes_lidas)
            atualizar_badge()
            notif_dialog.close()
            abrir_notificacoes()
        
        notif_dialog.open()
    
    # ==========================================
    # DEMAIS FUNÇÕES
    # ==========================================
    def visualizar_gasto(gasto, idx):
        categoria = gasto.get("categoria", "Sem categoria")
        cor_cat, icone_cat = get_cor_icone(categoria)
        
        with ui.dialog() as dialog, ui.card().classes('mobile-dialog w-full p-0 gap-0'):
            with ui.row().classes('w-full items-center justify-between p-4').style(f'background: linear-gradient(135deg, {cor_escura}, {cor_primaria}) !important;'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon(icone_cat).classes('text-2xl text-white')
                    ui.label("Detalhes").classes('text-white text-lg font-bold')
                ui.button(icon='close', on_click=dialog.close).props('flat').style('color: white !important;')
            
            with ui.element('div').classes('dialog-scroll w-full p-4'):
                with ui.column().classes('w-full gap-4'):
                    ui.input(label="Descrição", value=gasto.get("descricao", "")).props('outlined dense readonly').classes('w-full bg-gray-50')
                    ui.input(label="Valor", value=f"R$ {gasto.get('valor', 0):.2f}").props('outlined dense readonly').classes('w-full bg-gray-50')
                    ui.input(label="Categoria", value=categoria).props('outlined dense readonly').classes('w-full bg-gray-50')
                    if gasto.get("cartao"): ui.input(label="Cartão", value=gasto.get("cartao")).props('outlined dense readonly').classes('w-full bg-gray-50')
                    if gasto.get("data"): ui.input(label="Data", value=gasto["data"]).props('outlined dense readonly').classes('w-full bg-gray-50')
                    if gasto.get("parcelas", 1) > 1: ui.input(label="Parcelas", value=f"{gasto.get('parcela_atual', 1)}/{gasto.get('parcelas', 1)}").props('outlined dense readonly').classes('w-full bg-gray-50')
            
            with ui.row().classes('botoes-fixos justify-end gap-2 p-4'):
                ui.button("Fechar", on_click=dialog.close).props('outline').style(f'color: {cor_primaria} !important; border-color: {cor_primaria} !important; border-radius: 8px;')
                ui.button("Editar", on_click=lambda: [dialog.close(), editar_gasto(idx)], icon='edit').style(f'color: {cor_primaria} !important; border: 1px solid {cor_primaria} !important; border-radius: 8px;').props('outline')
                ui.button("Excluir", on_click=lambda: [dialog.close(), confirmar_exclusao(idx)], icon='delete').style(f'background: #ef4444 !important; color: white !important; border-radius: 8px;')
        dialog.open()
    
    def editar_gasto(idx):
        gasto = gastos[idx]
        categorias_dict = {c["nome"]: c for c in categorias}
        lista_categorias = list(categorias_dict.keys())
        
        with ui.dialog() as dialog, ui.card().classes('mobile-dialog w-full p-0 gap-0'):
            with ui.row().classes('w-full items-center justify-between p-4').style(f'background: linear-gradient(135deg, {cor_escura}, {cor_primaria}) !important;'):
                ui.icon('edit').classes('text-2xl text-white')
                ui.label("Editar Gasto").classes('text-white text-lg font-bold')
                ui.button(icon='close', on_click=dialog.close).props('flat').style('color: white !important;')
            
            with ui.element('div').classes('dialog-scroll w-full p-4'):
                with ui.column().classes('w-full gap-4'):
                    desc_input = ui.input(label="Descrição", value=gasto.get("descricao", "")).props('outlined dense').classes('w-full')
                    valor_input = ui.number(label="Valor R$", value=gasto.get("valor", 0), format="%.2f").props('outlined dense prefix=R$').classes('w-full')
                    
                    cat_value = {"valor": gasto.get("categoria", lista_categorias[0] if lista_categorias else "Outros")}
                    cat_display = ui.input(value=cat_value["valor"]).props('outlined dense readonly').classes('w-full')
                    
                    def abrir_selector_cat():
                        with ui.dialog() as sel_dialog, ui.card().classes('p-4 rounded-xl max-w-[350px]'):
                            ui.label("Selecione a categoria").classes('text-sm font-bold mb-3').style(f'color: {cor_primaria} !important;')
                            for nome in lista_categorias:
                                is_sel = nome == cat_value["valor"]
                                with ui.row().classes('items-center gap-2 p-2 rounded-lg cursor-pointer w-full').style(f'background: {cor_primaria}15 !important;' if is_sel else 'background: transparent;').on('click', lambda n=nome: selecionar_cat(n)):
                                    ui.icon(categorias_dict[nome].get("icone", "category")).classes('text-lg').style(f'color: {categorias_dict[nome].get("cor", "#6b7280")} !important;')
                                    ui.label(nome).classes('text-sm font-medium')
                            def selecionar_cat(nome): cat_value["valor"] = nome; cat_display.value = nome; sel_dialog.close()
                            with ui.row().classes('justify-end w-full mt-3'): ui.button("Fechar", on_click=sel_dialog.close).props('outline').style(f'color: {cor_primaria} !important; border-color: {cor_primaria} !important;')
                        sel_dialog.open()
                    cat_display.on('click', abrir_selector_cat)
                    
                    cartao_value = None
                    if modo_cartao == "Individual":
                        nomes_cartoes = [c["nome"] for c in cartoes]
                        if nomes_cartoes:
                            cartao_value = {"valor": gasto.get("cartao", nomes_cartoes[0])}
                            cartao_display = ui.input(value=cartao_value["valor"]).props('outlined dense readonly').classes('w-full')
                            def abrir_selector_cartao():
                                with ui.dialog() as sel_dialog, ui.card().classes('p-4 rounded-xl max-w-[350px]'):
                                    ui.label("Selecione o cartão").classes('text-sm font-bold mb-3').style(f'color: {cor_primaria} !important;')
                                    for nome in nomes_cartoes:
                                        is_sel = nome == cartao_value["valor"]
                                        with ui.row().classes('items-center gap-2 p-2 rounded-lg cursor-pointer w-full').style(f'background: {cor_primaria}15 !important;' if is_sel else 'background: transparent;').on('click', lambda n=nome: selecionar_cartao(n)):
                                            ui.icon('credit_card').classes('text-lg').style(f'color: {cor_primaria} !important;'); ui.label(nome).classes('text-sm font-medium')
                                    def selecionar_cartao(nome): cartao_value["valor"] = nome; cartao_display.value = nome; sel_dialog.close()
                                    with ui.row().classes('justify-end w-full mt-3'): ui.button("Fechar", on_click=sel_dialog.close).props('outline').style(f'color: {cor_primaria} !important; border-color: {cor_primaria} !important;')
                                sel_dialog.open()
                            cartao_display.on('click', abrir_selector_cartao)
                    
                    data_formatada = ""
                    if gasto.get("data"):
                        try: data_formatada = datetime.strptime(gasto["data"], "%Y-%m-%d").strftime("%d/%m/%Y")
                        except: pass
                    data_input = ui.input(value=data_formatada, placeholder="DD/MM/AAAA").props('outlined dense').classes('w-full')
                    
                    def abrir_calendario():
                        with ui.dialog() as cal_dialog, ui.card().classes('p-4 rounded-xl'):
                            cal = ui.date().props('today-btn minimal')
                            def confirmar_data():
                                if cal.value:
                                    try: data_input.value = datetime.strptime(str(cal.value)[:10], "%Y-%m-%d").strftime("%d/%m/%Y")
                                    except: pass
                                cal_dialog.close()
                            with ui.row().classes('justify-end gap-2 mt-3'):
                                ui.button("Cancelar", on_click=cal_dialog.close).props('outline').style(f'color: {cor_primaria} !important; border-color: {cor_primaria} !important;')
                                ui.button("OK", on_click=confirmar_data).style(f'background: {cor_primaria} !important; color: white !important; border-radius: 8px;')
                        cal_dialog.open()
                    data_input.on('click', abrir_calendario)
            
            with ui.row().classes('botoes-fixos justify-end gap-2 p-4'):
                ui.button("Cancelar", on_click=dialog.close).props('outline').style(f'color: {cor_primaria} !important; border-color: {cor_primaria} !important; border-radius: 8px;')
                def salvar_edicao():
                    try:
                        atualizacoes = {"descricao": desc_input.value, "valor": float(valor_input.value or 0), "categoria": cat_value["valor"]}
                        if data_input.value:
                            try: atualizacoes["data"] = datetime.strptime(data_input.value, "%d/%m/%Y").strftime("%Y-%m-%d")
                            except: pass
                        if modo_cartao == "Individual" and cartao_value: atualizacoes["cartao"] = cartao_value["valor"]
                        dados["gastos"][idx].update(atualizacoes); salvar(dados); dialog.close(); atualizar_dados()
                        ui.notify("✅ Gasto atualizado!", type="positive", position="top")
                    except Exception as e: ui.notify(f"❌ Erro: {str(e)}", type="negative", position="top")
                ui.button("Salvar", on_click=salvar_edicao, icon='save').style(f'background: {cor_primaria} !important; color: white !important; border-radius: 8px; font-weight: 600;')
        dialog.open()
    
    def confirmar_exclusao(idx):
        gasto = gastos[idx]
        def excluir():
            try:
                if gasto.get("id"): remover_gasto(gasto["id"])
                else: dados["gastos"].pop(idx); salvar(dados)
                confirm_dialog.close(); atualizar_dados()
                ui.notify("🗑️ Gasto excluído!", type="warning", position="top")
            except Exception as e: ui.notify(f"❌ Erro: {str(e)}", type="negative", position="top")
        with ui.dialog() as confirm_dialog, ui.card().classes('w-[320px] p-4 rounded-xl'):
            ui.icon('warning').classes('text-red-500 text-2xl mb-2')
            ui.label("Excluir gasto?").classes('text-lg font-bold')
            ui.label(f"📝 {gasto.get('descricao', 'Sem descrição')}").classes('text-sm')
            ui.label(f"💰 R$ {gasto.get('valor', 0):.2f}").classes('text-sm font-bold text-red-500')
            with ui.row().classes('justify-end gap-2 mt-4'):
                ui.button("Cancelar", on_click=confirm_dialog.close).props('outline').style(f'color: {cor_primaria} !important; border-color: {cor_primaria} !important;')
                ui.button("Excluir", on_click=excluir).style(f'background: #ef4444 !important; color: white !important; border-radius: 8px;')
        confirm_dialog.open()
    
    def atualizar_lista():
        nonlocal kpi_container, lista
        if lista is None or kpi_container is None: return
        lista.clear(); kpi_container.clear()
        
        totais = calcular_totais()
        
        with kpi_container:
            with ui.element('div').classes('kpi-grid'):
                cor_restante = cor_primaria if totais["restante"] > 0 else "#ef4444"
                for borda_cor, icone_nome, label, valor in [(cor_restante, 'wallet', 'Restante', totais["restante"]), ('#ef4444', 'trending_down', 'Gasto', totais["total_gasto"]), ('#6366f1', 'speed', 'Limite', totais["limite_total"])]:
                    with ui.card().classes('kpi-card').style(f'border-left-color: {borda_cor} !important;'):
                        ui.icon(icone_nome).classes('kpi-icon').style(f'color: {borda_cor} !important;')
                        ui.label(label).classes('kpi-label')
                        ui.label(f"R$ {valor:,.2f}").classes('kpi-valor')
            
            with ui.element('div').classes('progresso-container'):
                with ui.card().classes('progresso-card'):
                    percentual = min(totais["percentual"], 100)
                    cor_barra = "#10b981" if percentual < 50 else "#f59e0b" if percentual < 80 else "#ef4444"
                    with ui.row().classes('justify-between items-center mb-2'):
                        ui.label("Limite utilizado").classes('progresso-label')
                        ui.label(f"{percentual:.0f}%").classes('progresso-percentual').style(f'color: {cor_barra} !important;')
                    with ui.element('div').classes('barra-container'):
                        ui.element('div').classes('barra-preenchimento').style(f'width: {percentual:.0f}%; background: {cor_barra} !important;')
        
        termo = filtro_busca.lower() if filtro_busca else ""
        gastos_filtrados = []
        
        if tipo_filtro == "ciclo":
            inicio, fim = get_ciclo_atual()
            for i, g in enumerate(gastos):
                if termo and termo not in str(g).lower(): continue
                if modo_cartao == "Individual" and filtro_cartao != "Todos":
                    if g.get("cartao") != filtro_cartao: continue
                if g.get("data"):
                    try:
                        if not (inicio <= datetime.strptime(g["data"], "%Y-%m-%d") <= fim): continue
                    except: pass
                gastos_filtrados.append((i, g))
        else:
            for i, g in enumerate(gastos):
                if termo and termo not in str(g).lower(): continue
                if modo_cartao == "Individual" and filtro_cartao != "Todos":
                    if g.get("cartao") != filtro_cartao: continue
                if g.get("data"):
                    try:
                        dt = datetime.strptime(g["data"], "%Y-%m-%d")
                        if dt.month != filtro_mes or dt.year != filtro_ano: continue
                    except: pass
                gastos_filtrados.append((i, g))
        
        for i, f in enumerate(fixos):
            if termo and termo not in str(f).lower(): continue
            gastos_filtrados.append((-1, {**f, "tipo": GASTO_FIXO, "_is_fixo": True}))
        
        por_data = defaultdict(list)
        sem_data = []
        for idx, g in gastos_filtrados:
            if g.get("_is_fixo"): sem_data.append((idx, g))
            elif g.get("data"):
                try: por_data[datetime.strptime(g["data"], "%Y-%m-%d").strftime("%Y-%m-%d")].append((idx, g))
                except: sem_data.append((idx, g))
            else: sem_data.append((idx, g))
        
        with lista:
            if not gastos_filtrados:
                with ui.card().classes('estado-vazio'):
                    ui.icon('receipt_long').classes('text-5xl text-gray-300 mb-2')
                    ui.label("Nenhum gasto encontrado").classes('text-gray-500 text-sm')
                return
            
            for data_str in sorted(por_data.keys(), reverse=True):
                grupo = por_data[data_str]
                with ui.row().classes('dia-header justify-between items-center'):
                    try:
                        data_formatada = datetime.strptime(data_str, "%Y-%m-%d").strftime("%d/%m")
                    except:
                        data_formatada = data_str
                    ui.label(f"📅 {data_formatada}").classes('dia-titulo')
                    ui.label(f"R$ {sum(g[1].get('valor', 0) for g in grupo):,.2f}").classes('dia-total text-red-500')
                
                for idx, g in grupo:
                    categoria = g.get("categoria", "Sem categoria")
                    cor_cat, icone_cat = get_cor_icone(categoria)
                    detalhes = []
                    if g.get("cartao"): detalhes.append(f"💳 {g.get('cartao')}")
                    if g.get("tipo") == GASTO_PARCELADO or g.get("parcelas", 1) > 1:
                        if g.get("parcela_atual") and g.get("parcelas"): detalhes.append(f"{g.get('parcela_atual', 1)}/{g.get('parcelas')}x")
                    
                    with ui.card().classes('lancamento-card').style(f'border-left-color: {cor_cat} !important;').on('click', lambda g=g, i=idx: visualizar_gasto(g, i) if i >= 0 else None):
                        with ui.row().classes('items-center justify-between w-full'):
                            with ui.row().classes('items-center gap-3 flex-1'):
                                ui.icon(icone_cat).classes('text-lg').style(f'color: {cor_cat} !important;')
                                with ui.column().classes('gap-0 flex-1'):
                                    ui.label(g.get("descricao", "Sem descrição")).classes('lancamento-desc')
                                    if detalhes: ui.label(" • ".join(detalhes)).classes('lancamento-detalhe')
                            with ui.row().classes('items-center gap-2'):
                                ui.label(f"R$ {g.get('valor', 0):,.2f}").classes('lancamento-valor text-red-500')
                                ui.icon('chevron_right').classes('chevron-icon')
            
            if sem_data:
                with ui.row().classes('dia-header justify-between items-center'):
                    ui.label("🔁 Fixos").classes('dia-titulo text-purple-600')
                    ui.label(f"R$ {sum(g[1].get('valor', 0) for g in sem_data):,.2f}").classes('dia-total text-purple-600')
                
                for idx, g in sem_data:
                    categoria = g.get("categoria", "Sem categoria")
                    cor_cat, icone_cat = get_cor_icone(categoria)
                    with ui.card().classes('lancamento-card-fixo').style(f'border-left-color: {cor_cat} !important;'):
                        with ui.row().classes('items-center justify-between w-full'):
                            with ui.row().classes('items-center gap-3 flex-1'):
                                ui.icon(icone_cat).classes('text-lg').style(f'color: {cor_cat} !important;')
                                with ui.column().classes('gap-0 flex-1'):
                                    ui.label(g.get("descricao", "Sem descrição")).classes('lancamento-desc')
                                    ui.label("Mensal").classes('lancamento-detalhe text-purple-400')
                            ui.label(f"R$ {g.get('valor', 0):,.2f}").classes('lancamento-valor text-purple-600')
    
    # ==========================================
    # FILTROS
    # ==========================================
    def set_filtro_tipo(valor):
        nonlocal tipo_filtro
        tipo_filtro = str(valor).lower() if valor else "ciclo"
        if tipo_filtro == "ciclo": 
            botoes_toggle['ciclo'].style(f'background: {cor_primaria} !important; color: white !important;')
            botoes_toggle['mes'].style('background: #f3f4f6 !important; color: #6b7280 !important;')
        else: 
            botoes_toggle['ciclo'].style('background: #f3f4f6 !important; color: #6b7280 !important;')
            botoes_toggle['mes'].style(f'background: {cor_primaria} !important; color: white !important;')
        atualizar_lista(); atualizar_badge()
    
    def set_filtro_busca(valor):
        nonlocal filtro_busca
        if isinstance(valor, dict): valor = valor.get('args', valor.get('value', ''))
        filtro_busca = str(valor) if valor else ""
        atualizar_lista()
    
    def set_filtro_cartao(valor):
        nonlocal filtro_cartao
        if isinstance(valor, dict): valor = valor.get('label', valor.get('value', 'Todos'))
        filtro_cartao = str(valor) if valor else "Todos"
        atualizar_lista(); atualizar_badge()
    
    def set_filtro_mes(valor):
        nonlocal filtro_mes
        if isinstance(valor, dict): valor = valor.get('label', valor.get('value', hoje.month))
        try: filtro_mes = int(valor) if valor is not None else hoje.month
        except: filtro_mes = hoje.month
        atualizar_lista(); atualizar_badge()
    
    def set_filtro_ano(valor):
        nonlocal filtro_ano
        if isinstance(valor, dict): valor = valor.get('label', valor.get('value', hoje.year))
        try: filtro_ano = int(valor) if valor is not None else hoje.year
        except: filtro_ano = hoje.year
        atualizar_lista(); atualizar_badge()
    
    def abrir_cadastro():
        # Verificar limite de lançamentos
        pode, msg = verificar_limite_lancamentos(email_logado) if email_logado else (True, "")
        if not pode:
            ui.notify(msg, type="warning", position="top", timeout=4000)
            return
        
        from telas.cadastro import tela_cadastro
        tela_cadastro(callback=atualizar_dados)
    
    def abrir_configuracoes():
        from telas.configuracoes import tela_configuracoes
        dialog_config = ui.dialog()
        with dialog_config, ui.element('div').classes('w-full h-full') as temp_container:
            tela_configuracoes(temp_container, dialog_config)
        dialog_config.open()
    
    def fazer_logout():
        from db import set_usuario_logado
        set_usuario_logado(None)
        ui.notify("👋 Até logo!", type="info", position="top")
        ui.timer(0.5, lambda: ui.navigate.to('/'), once=True)
    
    # ==========================================
    # UI
    # ==========================================
    usuario_avatar = "👤"; usuario_nome = "Admin"
    try:
        u = get_usuario_logado()
        if u:
            _av = u.get('avatar_emoji', u.get('avatar', '👤'))
            if isinstance(_av, str):
                if len(_av) > 2 and ('\u200d' in _av or _av.startswith('👨') or _av.startswith('👩')): _av = _av[:2]
                elif len(_av) > 1: _av = _av[0]
            usuario_avatar = _av; usuario_nome = u.get('nome', 'Admin')
    except: pass
    
    nomes_cartoes = ["Todos"] + [c["nome"] for c in cartoes]
    
    with ui.element('div').classes('lancamentos-tela'):
        with ui.element('div').classes('lancamentos-header-fixo'):
            with ui.row().classes('header-bar items-center justify-between').style(f'background: linear-gradient(135deg, {cor_escura}, {cor_primaria}) !important;'):
                with ui.row().classes('items-center gap-2'):
                    # Logo
                    ui.image(LOGO_COMPLETA).style('width: 100px; height: auto;')
                    with ui.column().classes('gap-0'):
                        inicio, fim = get_ciclo_atual()
                        ui.label(f"Fecha dia {fim.day}").classes('header-subtitle-text text-white')
                        
                        # Contador de lançamentos
                        count = contar_lancamentos_mes()
                        if max_lanc >= 9999:
                            contador_label = ui.label(f"📊 {count} lançamentos").classes('limite-badge')
                        else:
                            cor_badge = 'rgba(239,68,68,0.3)' if count >= max_lanc else 'rgba(245,158,11,0.3)' if count >= max_lanc * 0.8 else 'rgba(255,255,255,0.2)'
                            contador_label = ui.label(f"📊 {count}/{max_lanc}").classes('limite-badge')
                            contador_label.style(f'background: {cor_badge} !important;')
                
                with ui.element('div').classes('notificacoes-container'):
                    notif_badge = ui.label('0').classes('notif-badge')
                    notif_badge.style('display: none')
                    
                    # Ícone diferente para premium
                    icon_notif = 'notifications' if consultor_premium else 'notifications'
                    ui.button(icon=icon_notif, on_click=abrir_notificacoes).props('flat round size=sm').classes('header-icon-btn').style('color: white !important;')
                    
                    if not consultor_premium:
                        ui.element('div').style('position:absolute;top:-1px;right:-1px;width:8px;height:8px;border-radius:50%;background:#f59e0b;')
            
            with ui.element('div').classes('busca-row'):
                busca_input = ui.input(placeholder="🔍 Buscar...").props('dense clearable').classes('flex-1').style('font-size: 13px;')
                busca_input.on('keyup', lambda e: set_filtro_busca(e.args.get('value', '')))
            
            with ui.element('div').classes('filtros-compactos'):
                with ui.element('div').classes('toggle-container'):
                    botoes_toggle['ciclo'] = ui.element('div').classes('toggle-btn').style(f'background: {cor_primaria} !important; color: white !important;').on('click', lambda: set_filtro_tipo('ciclo'))
                    with botoes_toggle['ciclo']: ui.label("📅 Ciclo")
                    botoes_toggle['mes'] = ui.element('div').classes('toggle-btn').style('background: #f3f4f6 !important; color: #6b7280 !important;').on('click', lambda: set_filtro_tipo('mes'))
                    with botoes_toggle['mes']: ui.label("📆 Mês")
                
                select_mes = ui.select(options=list(range(1, 13)), value=filtro_mes, label="Mês").props('dense').style('font-size: 12px; flex: 1;')
                select_mes.on('update:model-value', lambda e: set_filtro_mes(e.args))
                select_ano = ui.select(options=list(range(2020, 2031)), value=filtro_ano, label="Ano").props('dense').style('font-size: 12px; flex: 1;')
                select_ano.on('update:model-value', lambda e: set_filtro_ano(e.args))
                
                if modo_cartao == "Individual":
                    select_cartao = ui.select(options=nomes_cartoes, value="Todos", label="Cartão").props('dense').style('font-size: 12px; flex: 1;')
                    select_cartao.on('update:model-value', lambda e: set_filtro_cartao(e.args))
        
        with ui.element('div').classes('lancamentos-rolagem'):
            kpi_container = ui.column().classes('w-full')
            lista = ui.column().classes('w-full')
        
        with ui.element('div').classes('fab-button').style(f'background-color: {cor_primaria} !important;'):
            ui.button(icon='add', on_click=abrir_cadastro).props('round flat').style('color: white !important; width: 50px; height: 50px; font-size: 22px;')
        
        with ui.element('div').classes('bottom-nav-bar'):
            with ui.element('div').classes('bottom-nav-item'): 
                ui.label(usuario_avatar).classes('bottom-nav-icon').style('font-size: 18px')
                ui.label(usuario_nome[:10]).classes('bottom-nav-label').style(f'color: {cor_primaria} !important;')
            with ui.element('div').classes('bottom-nav-item active'): 
                ui.icon('receipt_long').classes('bottom-nav-icon').style(f'color: {cor_primaria} !important;')
                ui.label("Gastos").classes('bottom-nav-label')
            with ui.element('div').classes('bottom-nav-item').on('click', abrir_configuracoes): 
                ui.icon('settings').classes('bottom-nav-icon')
                ui.label("Config").classes('bottom-nav-label')
            with ui.element('div').classes('bottom-nav-item').on('click', fazer_logout): 
                ui.icon('logout').classes('bottom-nav-icon').style('color: #ef4444 !important;')
                ui.label("Sair").classes('bottom-nav-label').style('color: #ef4444 !important;')
    
    def verificar_mudancas():
        nonlocal dados, categorias, gastos, fixos, cartoes
        novos_dados = carregar()
        if len(novos_dados.get("gastos", [])) != len(gastos) or len(novos_dados.get("fixos", [])) != len(fixos):
            dados, categorias, gastos, fixos, cartoes, mapa_icones, mapa_cores = carregar_dados()
            atualizar_lista()
            atualizar_badge()
            atualizar_contador()
    
    ui.timer(2.0, verificar_mudancas)
    atualizar_lista()
    atualizar_badge()
    atualizar_contador()


__all__ = ['tela_lancamentos']