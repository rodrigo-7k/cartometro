"""
Tela de Cadastro de Gastos - Versão Mobile (Popup Otimizado)
"""

from nicegui import ui
from db import carregar, salvar_json, get_usuario_logado_email
from config_service import config_service
from datetime import datetime, timedelta
from constantes import (
    GASTO_AVISTA, GASTO_PARCELADO, GASTO_FIXO,
    TIPOS_GASTO, CATEGORIAS_PADRAO, CORES_TIPOS, ICONES_TIPOS,
    PARCELAS_OPCOES
)
import os as _os  # ✅ Adicionado


CUSTOM_CSS = """
<style>
.q-dialog__inner { padding: 0 !important; margin: 0 !important; }
.mobile-cadastro-dialog { width: 90vw !important; max-width: 500px !important; height: auto !important; max-height: 85vh !important; margin: 0 auto !important; border-radius: 20px !important; display: flex !important; flex-direction: column !important; position: relative !important; }
.q-card { margin: 0 !important; border-radius: 0 !important; box-shadow: none !important; }
.cadastro-scroll { flex: 1 !important; overflow-y: auto !important; overflow-x: hidden !important; padding-bottom: 80px !important; }
.cadastro-scroll::-webkit-scrollbar { width: 4px; }
.cadastro-scroll::-webkit-scrollbar-track { background: #e5e7eb; }
.cadastro-scroll::-webkit-scrollbar-thumb { background: #9ca3af; border-radius: 4px; }
.botoes-fixos { position: sticky !important; bottom: 0 !important; background: white !important; border-top: 1px solid #e5e7eb !important; z-index: 10 !important; margin-top: auto !important; }
.tipos-grid { display: grid !important; grid-template-columns: repeat(3, 1fr) !important; gap: 8px !important; width: 100% !important; }
.parcelas-grid { display: grid !important; grid-template-columns: repeat(4, 1fr) !important; gap: 8px !important; width: 100% !important; }
.campo-mobile { width: 100% !important; margin-bottom: 12px !important; }
.campo-label { font-size: 12px; font-weight: 600; color: #374151; margin-bottom: 4px; }
.gradient-line { height: 3px; width: 100%; }

.tipo-btn {
    border-radius: 10px !important;
    height: 44px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    font-size: 13px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 6px !important;
    border: 1px solid #d1d5db !important;
    color: #374151 !important;
    background: transparent !important;
}
.tipo-btn:active { transform: scale(0.97) !important; }

.dica-card {
    border-radius: 8px !important;
    padding: 10px 12px !important;
    margin-bottom: 8px !important;
}

/* BORDAS NA COR PRIMÁRIA */
.q-field--outlined.q-field--focused .q-field__control:before { border-color: var(--cor-primaria) !important; }
.q-field--outlined.q-field--focused .q-field__control:after { border-color: var(--cor-primaria) !important; }
.q-field--focused .q-field__control { border-color: transparent !important; }

/* TEXTO SEMPRE PRETO */
.q-field--focused .q-field__label { color: #374151 !important; }
.q-field--focused .q-field__native { color: #111827 !important; }
.q-field--focused .q-select__label { color: #374151 !important; }

/* DROPDOWN */
.q-item.q-manual-focusable--focused { background: var(--cor-primaria) !important; color: white !important; }

/* CALENDÁRIO */
.q-date__today { color: var(--cor-primaria) !important; font-weight: bold !important; }
.q-date__day--selected { background: var(--cor-primaria) !important; color: white !important; }
.q-date__day--today { border-color: var(--cor-primaria) !important; }

@media (max-width: 768px) { .mobile-cadastro-dialog { width: 100vw !important; max-width: 100vw !important; border-radius: 0 !important; max-height: 85vh !important; } }
</style>
"""


def tela_cadastro(callback=None):
    
    ui.add_head_html(CUSTOM_CSS)
    
    email = get_usuario_logado_email()
    dados = carregar(email) if email else {}
    categorias = dados.get("categorias", CATEGORIAS_PADRAO)
    cartoes = dados.get("cartoes", [])
    modo_cartao = dados.get("config", {}).get("modo_cartao", "Unificado")
    
    # ✅ Arquivo para salvar
    arquivo = _os.path.join('data', f"{email.replace('@','_').replace('.','_').lower()}.json") if email else None
    
    estado = {"tipo": None, "parcelas": 2}
    campos = {}
    botoes_tipos = []
    dialog = None
    campos_container = None
    parcelas_container = None
    
    cor_primaria = config_service.get_primary_color()
    cor_escura = config_service.get_primary_dark()
    
    ui.add_head_html(f'<style>:root {{ --cor-primaria: {cor_primaria}; }}</style>')
    
    LABELS_TIPOS = {
        GASTO_AVISTA: "À Vista",
        GASTO_PARCELADO: "Parcelado",
        GASTO_FIXO: "Fixo"
    }
    
    # =========================
    # CAMPO CATEGORIA (DIALOG CENTRALIZADO)
    # =========================
    def campo_categoria():
        categorias_dict = {c["nome"]: c for c in categorias}
        lista_categorias = list(categorias_dict.keys())
        
        if not lista_categorias:
            for c in CATEGORIAS_PADRAO:
                categorias_dict[c["nome"]] = c
            lista_categorias = list(categorias_dict.keys())
        
        with ui.column().classes('w-full gap-1 campo-mobile'):
            ui.label("📂 Categoria").classes('campo-label')
            cat_display = ui.input(label="Categoria", value=lista_categorias[0] if lista_categorias else "Outros").props('outlined dense readonly').classes('w-full')
            cat_value = {"valor": lista_categorias[0] if lista_categorias else "Outros"}
            
            def abrir_selector():
                with ui.dialog() as sel_dialog, ui.card().classes('p-4 rounded-xl max-w-[350px]'):
                    ui.label("Selecione a categoria").classes('text-sm font-bold mb-3').style(f'color: {cor_primaria} !important;')
                    
                    for nome in lista_categorias:
                        is_sel = nome == cat_value["valor"]
                        with ui.row().classes('items-center gap-2 p-2 rounded-lg cursor-pointer w-full').style(
                            f'background: {cor_primaria}15 !important;' if is_sel else 'background: transparent;'
                        ).on('click', lambda n=nome: selecionar(n)):
                            ui.icon(categorias_dict[nome].get("icone", "category")).classes('text-lg').style(f'color: {categorias_dict[nome].get("cor", "#6b7280")} !important;')
                            ui.label(nome).classes('text-sm font-medium')
                    
                    def selecionar(nome):
                        cat_value["valor"] = nome
                        cat_display.value = nome
                        sel_dialog.close()
                    
                    with ui.row().classes('justify-end w-full mt-3'):
                        ui.button("Fechar", on_click=sel_dialog.close).props('outline').style(f'color: {cor_primaria} !important; border-color: {cor_primaria} !important;')
                sel_dialog.open()
            
            cat_display.on('click', abrir_selector)
        
        return cat_value
    
    # =========================
    # CAMPO CARTÃO (MODO INDIVIDUAL)
    # =========================
    def campo_cartao():
        nomes_cartoes = [c["nome"] for c in cartoes]
        if not nomes_cartoes:
            return {"valor": None}
        
        with ui.column().classes('w-full gap-1 campo-mobile'):
            ui.label("💳 Cartão (obrigatório)").classes('campo-label')
            
            # Preview da imagem do cartão
            cartao_preview = ui.element('div').style('display:none;align-items:center;gap:8px;padding:8px;background:#f9fafb;border-radius:8px;margin-bottom:4px;')
            with cartao_preview:
                cartao_img = ui.image().style('width:48px;height:30px;object-fit:contain;border-radius:4px;flex-shrink:0;')
                cartao_nome_label = ui.label("").classes('text-sm font-semibold text-gray-800')
            
            cartao_display = ui.input(label="Selecione o cartão", value="").props('outlined dense readonly').classes('w-full')
            cartao_value = {"valor": None}
            
            def abrir_selector_cartao():
                with ui.dialog() as sel_dialog, ui.card().classes('p-4 rounded-xl max-w-[400px]'):
                    ui.label("💳 Selecione o cartão").classes('text-sm font-bold mb-3').style(f'color: {cor_primaria} !important;')
                    
                    for nome in nomes_cartoes:
                        is_sel = nome == cartao_value["valor"]
                        # Buscar imagem do cartão nos dados do usuário
                        img_cartao = None
                        for c in cartoes:
                            if c["nome"] == nome:
                                img_cartao = c.get("img")
                                break
                        # Se não achou, tentar CARTOES_POPULARES
                        if not img_cartao:
                            try:
                                from config import get_img_cartao
                                img_cartao = get_img_cartao(nome)
                            except:
                                pass
                        
                        with ui.row().classes('items-center gap-3 p-2 rounded-lg cursor-pointer w-full').style(
                            f'background: {cor_primaria}15 !important;' if is_sel else 'background: transparent;'
                        ).on('click', lambda n=nome: selecionar(n)):
                            if img_cartao:
                                ui.image(img_cartao).style('width:44px;height:28px;object-fit:contain;border-radius:4px;flex-shrink:0;')
                            else:
                                ui.icon('credit_card').classes('text-lg').style(f'color: {cor_primaria} !important;')
                            ui.label(nome).classes('text-sm font-medium')
                    
                    def selecionar(nome):
                        cartao_value["valor"] = nome
                        cartao_display.value = nome
                        # Mostrar preview
                        img_preview = None
                        for c in cartoes:
                            if c["nome"] == nome:
                                img_preview = c.get("img")
                                break
                        if not img_preview:
                            try:
                                from config import get_img_cartao
                                for c in CARTOES_POPULARES:
                                    if c["nome"] == nome:
                                        img_preview = c["img"]
                                        break
                            except:
                                pass
                        if img_preview:
                            cartao_img.source = img_preview
                        cartao_nome_label.set_text(nome)
                        cartao_preview.style('display:flex')
                        sel_dialog.close()
                    
                    with ui.row().classes('justify-end w-full mt-3'):
                        ui.button("Fechar", on_click=sel_dialog.close).props('outline').style(f'color: {cor_primaria} !important; border-color: {cor_primaria} !important;')
                sel_dialog.open()
            
            cartao_display.on('click', abrir_selector_cartao)
        
        return cartao_value
    # =========================
    # CAMPO DATA (DIALOG CENTRALIZADO)
    # =========================
    def campo_data():
        with ui.column().classes('w-full gap-1 campo-mobile'):
            ui.label("📅 Data da Compra").classes('campo-label')
            inp = ui.input(placeholder="DD/MM/AAAA", value=datetime.now().strftime("%d/%m/%Y")).props('outlined dense').classes('w-full')
            
            def abrir_calendario():
                with ui.dialog() as cal_dialog, ui.card().classes('p-4 rounded-xl'):
                    ui.label("Selecione a data").classes('text-sm font-bold mb-2').style(f'color: {cor_primaria} !important;')
                    cal = ui.date().props('today-btn minimal')
                    
                    def confirmar_data():
                        if cal.value:
                            try:
                                dt = datetime.strptime(str(cal.value)[:10], "%Y-%m-%d")
                                inp.value = dt.strftime("%d/%m/%Y")
                            except: pass
                        cal_dialog.close()
                    
                    with ui.row().classes('justify-end gap-2 mt-3'):
                        ui.button("Cancelar", on_click=cal_dialog.close).props('outline').style(f'color: {cor_primaria} !important; border-color: {cor_primaria} !important;')
                        ui.button("OK", on_click=confirmar_data).style(f'background: {cor_primaria} !important; color: white !important; border-radius: 8px;')
                cal_dialog.open()
            
            inp.on('click', abrir_calendario)
        
        return inp
    
    # =========================
    # CAMPO PARCELAS (2 a 12)
    # =========================
    def campo_parcelas():
        nonlocal parcelas_container
        parcelas_container.clear()
        
        with parcelas_container:
            with ui.column().classes('w-full gap-2 campo-mobile'):
                ui.label("📦 Número de Parcelas").classes('campo-label')
                
                with ui.element('div').classes('parcelas-grid'):
                    botoes_parcela = {}
                    
                    def atualizar_botoes(valor_selecionado):
                        for parcela, btn in botoes_parcela.items():
                            if parcela == valor_selecionado:
                                btn.style(f'background-color: {cor_primaria} !important; color: white !important; border-color: {cor_primaria} !important;')
                            else:
                                btn.style('background-color: transparent !important; color: #374151 !important; border-color: #d1d5db !important;')
                    
                    def atualizar_preview():
                        if campos.get("valor") and campos["valor"].value:
                            try:
                                valor_total = float(campos["valor"].value)
                                num_parcelas = estado["parcelas"]
                                if num_parcelas > 1:
                                    valor_parcela = valor_total / num_parcelas
                                    preview_parcela.set_text(f"💡 {num_parcelas}x de {config_service.formatar_valor(valor_parcela)}")
                                else:
                                    preview_parcela.set_text("")
                            except:
                                preview_parcela.set_text("")
                        else:
                            preview_parcela.set_text("")
                    
                    def selecionar_parcela(parcela):
                        estado["parcelas"] = parcela
                        atualizar_botoes(parcela)
                        atualizar_preview()
                    
                    for parcela in range(2, 13):
                        btn = ui.button(str(parcela), on_click=lambda p=parcela: selecionar_parcela(p)).props('flat').style('border: 1px solid #d1d5db; border-radius: 8px; height: 36px; font-size: 12px;')
                        botoes_parcela[parcela] = btn
                
                preview_parcela = ui.label("").classes('text-xs font-semibold mt-1').style(f'color: {cor_primaria} !important;')
                
                selecionar_parcela(2)
        
        def atualizar_preview_externo():
            if campos.get("valor") and campos["valor"].value:
                try:
                    valor_total = float(campos["valor"].value)
                    num_parcelas = estado["parcelas"]
                    if num_parcelas > 1:
                        valor_parcela = valor_total / num_parcelas
                        preview_parcela.set_text(f"💡 {num_parcelas}x de {config_service.formatar_valor(valor_parcela)}")
                    else:
                        preview_parcela.set_text("")
                except:
                    preview_parcela.set_text("")
            else:
                preview_parcela.set_text("")
        
        return atualizar_preview_externo
    
    # =========================
    # RENDER CAMPOS
    # =========================
    def render_campos():
        campos_container.clear()
        parcelas_container.clear()
        campos.clear()
        
        if not estado["tipo"]: return
        
        tipo = estado["tipo"]
        cor_tipo = CORES_TIPOS.get(tipo, cor_primaria)
        
        with campos_container:
            # Card informativo do tipo com dica
            with ui.card().classes('w-full p-3 rounded-xl mb-3').style(f'background: {config_service.cor_com_opacidade(cor_tipo, 0.1)} !important; border-left: 3px solid {cor_tipo} !important;'):
                with ui.row().classes('items-center gap-2'):
                    ui.icon(ICONES_TIPOS.get(tipo, "receipt")).classes('text-lg').style(f'color: {cor_tipo} !important;')
                    with ui.column().classes('gap-0'):
                        ui.label(LABELS_TIPOS.get(tipo, tipo)).classes('text-sm font-semibold').style(f'color: {cor_tipo} !important;')
                        if tipo == GASTO_PARCELADO:
                            ui.label("O valor será dividido em parcelas mensais").classes('text-[10px] text-gray-500')
                        elif tipo == GASTO_AVISTA:
                            ui.label("Compra paga integralmente na fatura").classes('text-[10px] text-gray-500')
                        elif tipo == GASTO_FIXO:
                            ui.label("Cobrança recorrente todo mês").classes('text-[10px] text-gray-500')
            
            # Dica específica por tipo
            if tipo == GASTO_PARCELADO:
                with ui.card().classes('dica-card mb-3').style(f'background: {cor_primaria}08; border-left: 3px solid {cor_primaria};'):
                    with ui.row().classes('items-start gap-2'):
                        ui.icon('info').classes('text-sm mt-0.5').style(f'color: {cor_primaria} !important;')
                        with ui.column().classes('gap-1'):
                            ui.label("💡 Como funciona o parcelamento").classes('text-xs font-semibold').style(f'color: {cor_primaria} !important;')
                            ui.label("O valor total será dividido igualmente. Cada parcela aparecerá em um mês diferente nos seus lançamentos.").classes('text-[11px] text-gray-600')
            
            elif tipo == GASTO_AVISTA:
                with ui.card().classes('dica-card mb-3').style(f'background: {cor_primaria}08; border-left: 3px solid {cor_primaria};'):
                    with ui.row().classes('items-start gap-2'):
                        ui.icon('info').classes('text-sm mt-0.5').style(f'color: {cor_primaria} !important;')
                        with ui.column().classes('gap-1'):
                            ui.label("💡 Pagamento à vista").classes('text-xs font-semibold').style(f'color: {cor_primaria} !important;')
                            ui.label("O valor total será lançado na fatura atual. Ideal para compras menores ou quando você tem limite disponível.").classes('text-[11px] text-gray-600')
            
            elif tipo == GASTO_FIXO:
                with ui.card().classes('dica-card mb-3').style(f'background: {cor_primaria}08; border-left: 3px solid {cor_primaria};'):
                    with ui.row().classes('items-start gap-2'):
                        ui.icon('info').classes('text-sm mt-0.5').style(f'color: {cor_primaria} !important;')
                        with ui.column().classes('gap-1'):
                            ui.label("💡 Gasto fixo mensal").classes('text-xs font-semibold').style(f'color: {cor_primaria} !important;')
                            ui.label("Este valor será contabilizado todo mês automaticamente. Use para streaming, assinaturas, academia, etc.").classes('text-[11px] text-gray-600')
            
            with ui.column().classes('w-full gap-1 campo-mobile'):
                ui.label("📝 Descrição").classes('campo-label')
                campos["descricao"] = ui.input(label="Descrição", placeholder="Ex: Supermercado, Uber...").props('outlined dense').classes('w-full')
            
            with ui.column().classes('w-full gap-1 campo-mobile'):
                ui.label("💰 Valor (R$)").classes('campo-label')
                campos["valor"] = ui.number(label="Valor", format="%.2f", value=None).props('outlined dense prefix=R$').classes('w-full')
            
            campos["cat"] = campo_categoria()
            
            # Dica da categoria
            with ui.card().classes('dica-card').style(f'background: #f0fdf4; border-left: 3px solid #10b981;'):
                ui.label("📂 Dica: Escolha a categoria correta para organizar melhor seus gastos nos relatórios.").classes('text-[10px] text-gray-600')
            
            # Cartão (modo Individual)
            if modo_cartao == "Individual" and cartoes:
                campos["cartao"] = campo_cartao()
                
                with ui.card().classes('dica-card').style(f'background: #fef3c7; border-left: 3px solid #f59e0b;'):
                    ui.label("💳 Este gasto será atribuído ao cartão selecionado e controle será feito separadamente.").classes('text-[10px] text-gray-600')
            else:
                campos["cartao"] = {"valor": None}
            
            if tipo != GASTO_FIXO:
                campos["data"] = campo_data()
                
                if tipo == GASTO_PARCELADO:
                    with ui.card().classes('dica-card').style(f'background: #eff6ff; border-left: 3px solid #3b82f6;'):
                        ui.label("📅 A data escolhida será a data da primeira parcela. As demais serão nos meses seguintes.").classes('text-[10px] text-gray-600')
            
            if tipo == GASTO_PARCELADO:
                preview_updater = campo_parcelas()
                if campos.get("valor"): campos["valor"].on('change', lambda e: preview_updater())
    
    # =========================
    # SALVAR - ✅ CORRIGIDO
    # =========================
    def salvar():
        if not estado["tipo"]:
            ui.notify("⚠️ Selecione um tipo de gasto", type="warning", position="top")
            return
        
        descricao = campos.get("descricao")
        valor = campos.get("valor")
        
        if not descricao or not descricao.value or not descricao.value.strip():
            ui.notify("⚠️ Informe a descrição", type="warning", position="top")
            return
        
        if not valor or not valor.value or valor.value <= 0:
            ui.notify("⚠️ Informe um valor válido", type="warning", position="top")
            return
        
        data_valor = None
        if campos.get("data") and campos["data"].value:
            try:
                data_obj = datetime.strptime(campos["data"].value, "%d/%m/%Y")
                data_valor = data_obj.strftime("%Y-%m-%d")
            except:
                data_valor = datetime.now().strftime("%Y-%m-%d")
        
        tipo = estado["tipo"]
        parcelas = estado["parcelas"] if tipo == GASTO_PARCELADO else 1
        categoria_valor = campos["cat"]["valor"] if campos.get("cat") else "Outros"
        cartao_valor = campos["cartao"]["valor"] if campos.get("cartao") and campos["cartao"]["valor"] else None
        
        try:
            # ✅ CORRIGIDO: adicionar ao array e salvar com 2 argumentos
            novo_gasto = {
                "id": len(dados.get("gastos", [])) + 1,
                "descricao": descricao.value.strip(),
                "valor": float(valor.value),
                "tipo": tipo,
                "parcelas": parcelas,
                "data": data_valor,
                "categoria": categoria_valor,
                "cartao": cartao_valor
            }
            
            if "gastos" not in dados:
                dados["gastos"] = []
            
            # Se for parcelado, criar um lançamento por parcela
            if tipo == GASTO_PARCELADO and parcelas > 1:
                valor_parcela = round(float(valor.value) / parcelas, 2)
                # Ajustar última parcela para evitar diferença de centavos
                soma_parcelas = valor_parcela * (parcelas - 1)
                ultima_parcela = round(float(valor.value) - soma_parcelas, 2)
                
                for p in range(parcelas):
                    data_parcela = data_obj + timedelta(days=30 * p) if data_obj else None
                    valor_desta_parcela = ultima_parcela if p == parcelas - 1 else valor_parcela
                    
                    dados["gastos"].append({
                        "id": len(dados["gastos"]) + 1,
                        "descricao": f"{descricao.value.strip()} ({p+1}/{parcelas})",
                        "valor": valor_desta_parcela,
                        "valor_total": float(valor.value),
                        "tipo": tipo,
                        "parcelas": parcelas,
                        "parcela_atual": p + 1,
                        "data": data_parcela.strftime("%Y-%m-%d") if data_parcela else None,
                        "categoria": categoria_valor,
                        "cartao": cartao_valor
                    })
            else:
                dados["gastos"].append(novo_gasto)
            
            if arquivo:
                salvar_json(arquivo, dados)
            
            dialog.close()
            
            if tipo == GASTO_PARCELADO and parcelas > 1:
                ui.notify(f"✅ {parcelas}x de {config_service.formatar_valor(float(valor.value)/parcelas)}", type="positive", position="top")
            else:
                ui.notify(f"✅ Gasto de {config_service.formatar_valor(float(valor.value))} salvo!", type="positive", position="top")
            
            if callback: callback()
        except Exception as e:
            ui.notify(f"❌ Erro ao salvar: {str(e)}", type="negative", position="top")
    
    # =========================
    # SELEÇÃO DE TIPO
    # =========================
    def selecionar_tipo(t):
        estado["tipo"] = t
        estado["parcelas"] = 2
        
        for btn, nome in botoes_tipos:
            if nome == t:
                btn.style(f'background-color: {cor_primaria} !important; color: white !important; border-color: {cor_primaria} !important; font-weight: 600;')
            else:
                btn.style(f'color: {cor_primaria} !important; border-color: {cor_primaria} !important; background-color: transparent !important; font-weight: 400;')
        
        render_campos()
    
    # =========================
    # DIALOG
    # =========================
    dialog = ui.dialog()
    
    with dialog, ui.card().classes('mobile-cadastro-dialog w-full p-0 gap-0'):
        
        with ui.row().classes('w-full items-center justify-between p-4').style(f'background: linear-gradient(135deg, {cor_escura}, {cor_primaria}) !important;'):
            with ui.row().classes('items-center gap-2'):
                ui.icon('add_circle_outline').classes('text-2xl text-white')
                with ui.column().classes('gap-0'):
                    ui.label("Novo Gasto").classes('text-white text-lg font-bold')
                    ui.label("Registre sua compra no cartão").classes('text-white/70 text-xs')
            ui.button(icon='close', on_click=dialog.close).props('flat').style('color: white !important;')
        
        ui.element('div').classes('gradient-line').style(f'background: linear-gradient(90deg, {cor_primaria}, {cor_primaria}40, transparent) !important;')
        
        with ui.element('div').classes('cadastro-scroll w-full p-4'):
            with ui.column().classes('w-full gap-4'):
                
                with ui.column().classes('w-full gap-2'):
                    ui.label("📌 Tipo de Gasto").classes('campo-label')
                    
                    with ui.card().classes('dica-card').style(f'background: {cor_primaria}08; border-left: 3px solid {cor_primaria};'):
                        with ui.row().classes('items-start gap-2'):
                            ui.icon('info').classes('text-sm mt-0.5').style(f'color: {cor_primaria} !important;')
                            with ui.column().classes('gap-1'):
                                ui.label("💡 Escolha o tipo").classes('text-xs font-semibold').style(f'color: {cor_primaria} !important;')
                                ui.label("À Vista: pagamento único | Parcelado: divide em vezes | Fixo: cobrança recorrente").classes('text-[11px] text-gray-600')
                    
                    with ui.element('div').classes('tipos-grid'):
                        for t in TIPOS_GASTO:
                            icone_tipo = ICONES_TIPOS.get(t, "receipt")
                            label = LABELS_TIPOS.get(t, t)
                            
                            btn = ui.button(on_click=lambda tipo=t: selecionar_tipo(tipo)).props('flat').classes('tipo-btn')
                            with btn:
                                ui.icon(icone_tipo).classes('text-sm')
                                ui.label(label)
                            btn.style(f'color: {cor_primaria} !important; border-color: {cor_primaria} !important; background-color: transparent !important;')
                            botoes_tipos.append((btn, t))
                
                campos_container = ui.column().classes('w-full')
                parcelas_container = ui.column().classes('w-full')
        
        with ui.row().classes('botoes-fixos justify-end gap-3 p-4'):
            ui.button("Cancelar", on_click=dialog.close).props('outline').classes('px-6 py-2 text-sm').style(f'color: {cor_primaria} !important; border-color: {cor_primaria} !important;')
            ui.button("Salvar", on_click=salvar, icon='save').classes('px-6 py-2 text-sm').style(f'background-color: {cor_primaria} !important; color: white !important; border-radius: 8px;')
    
    dialog.open()


__all__ = ['tela_cadastro']