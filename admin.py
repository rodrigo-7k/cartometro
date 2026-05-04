"""
Painel Administrativo - Cartometro
Gerenciamento Completo de Usuários e Assinaturas
"""

from nicegui import ui
from db import (
    carregar_usuarios, salvar_usuarios, buscar_usuario_por_email,
    atualizar_plano_usuario, PLANOS, carregar_json, salvar_json,
    hash_senha, get_plano_usuario
)
from datetime import datetime, timedelta
import os

# ============================================================
# CONFIGURAÇÃO
# ============================================================
ADMIN_FILE = 'admin_config.json'
PAGAMENTOS_FILE = 'pagamentos.json'

ADMIN_EMAIL = "admin@cartometro.com"
ADMIN_SENHA = "Cartometro@2024"
ADMIN_SENHA_HASH = hash_senha(ADMIN_SENHA)
ADMIN_NOME = "Administrador"


# ============================================================
# INICIALIZAÇÃO
# ============================================================
def inicializar_admin():
    if not os.path.exists(PAGAMENTOS_FILE):
        salvar_json(PAGAMENTOS_FILE, [])
    
    if not os.path.exists(ADMIN_FILE):
        config = {
            "admin": {
                "email": ADMIN_EMAIL,
                "senha": ADMIN_SENHA_HASH,
                "nome": ADMIN_NOME,
                "ultimo_acesso": None
            }
        }
        salvar_json(ADMIN_FILE, config)
    
    print(f"✅ Admin: {ADMIN_EMAIL}")


def carregar_config_admin():
    config = carregar_json(ADMIN_FILE)
    if config is None:
        config = {"admin": {"email": ADMIN_EMAIL, "senha": ADMIN_SENHA_HASH, "nome": ADMIN_NOME, "ultimo_acesso": None}}
        salvar_json(ADMIN_FILE, config)
    return config


def autenticar_admin(email, senha):
    if email.strip().lower() != ADMIN_EMAIL:
        return False
    if hash_senha(senha) != ADMIN_SENHA_HASH:
        return False
    try:
        config = carregar_config_admin()
        if config and "admin" in config:
            config["admin"]["ultimo_acesso"] = datetime.now().isoformat()
            salvar_json(ADMIN_FILE, config)
    except:
        pass
    return True


def alterar_senha_admin(nova_senha):
    global ADMIN_SENHA_HASH
    ADMIN_SENHA_HASH = hash_senha(nova_senha)
    config = carregar_config_admin()
    config["admin"]["senha"] = ADMIN_SENHA_HASH
    salvar_json(ADMIN_FILE, config)
    return True


def carregar_pagamentos():
    pagamentos = carregar_json(PAGAMENTOS_FILE)
    return pagamentos if pagamentos is not None else []


def salvar_pagamentos(pagamentos):
    salvar_json(PAGAMENTOS_FILE, pagamentos)


def registrar_pagamento(email, metodo, valor, status="confirmado", admin_responsavel=""):
    pagamentos = carregar_pagamentos()
    pagamentos.append({
        "id": len(pagamentos) + 1,
        "email": email,
        "metodo": metodo,
        "valor": valor,
        "status": status,
        "admin": admin_responsavel,
        "data": datetime.now().isoformat()
    })
    salvar_pagamentos(pagamentos)


# ============================================================
# TELA DE LOGIN
# ============================================================
@ui.page('/admin')
def admin_login():
    ui.add_head_html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'DM Sans', sans-serif;
            background: linear-gradient(135deg, #1e293b, #0f172a);
            height: 100vh; display: flex; align-items: center; justify-content: center;
        }
        .login-card {
            background: white; border-radius: 20px; padding: 48px 40px;
            width: 400px; max-width: 90vw; box-shadow: 0 25px 60px rgba(0,0,0,0.3);
        }
    </style>
    """)
    
    with ui.element('div').classes('login-card'):
        ui.label("🔐 Painel Admin").style('font-size:24px;font-weight:700;text-align:center;color:#1e293b;')
        ui.label("Cartometro").style('font-size:14px;color:#94a3b8;text-align:center;margin-bottom:32px;')
        
        ui.label("Email").style('font-size:13px;font-weight:500;color:#475569;margin-bottom:6px;')
        email_input = ui.input(placeholder="admin@cartometro.com").props('outlined').classes('w-full').style('margin-bottom:20px;')
        
        ui.label("Senha").style('font-size:13px;font-weight:500;color:#475569;margin-bottom:6px;')
        senha_input = ui.input(placeholder="••••••••", password=True, password_toggle_button=True).props('outlined').classes('w-full').style('margin-bottom:20px;')
        
        erro_label = ui.label('').style('color:#ef4444;font-size:13px;text-align:center;display:none;margin-bottom:16px;')
        
        def fazer_login():
            email = email_input.value.strip().lower() if email_input.value else ''
            senha = senha_input.value or ''
            if not email or not senha:
                erro_label.style('display:block'); erro_label.set_text('⚠️ Preencha todos os campos'); return
            if autenticar_admin(email, senha):
                ui.notify("✅ Acesso autorizado!", type="positive", position="top")
                ui.navigate.to('/admin/painel')
            else:
                erro_label.style('display:block'); erro_label.set_text('❌ Acesso negado')
        
        ui.button("Acessar Painel", on_click=fazer_login).props('no-caps').style(
            'width:100%;height:48px;border-radius:10px;background:#8b5cf6;color:white;border:none;font-size:15px;font-weight:600;cursor:pointer;'
        )
        
        with ui.element('div').style('text-align:center;margin-top:24px;'):
            ui.label(f"🔑 {ADMIN_EMAIL}").style('font-size:11px;color:#94a3b8;')
            ui.label(f"🔒 {ADMIN_SENHA}").style('font-size:11px;color:#94a3b8;')


# ============================================================
# PAINEL ADMIN COMPLETO
# ============================================================
@ui.page('/admin/painel')
def admin_painel():
    
    # Carregar dados
    usuarios = carregar_usuarios()
    pagamentos = carregar_pagamentos()
    
    total_usuarios = len(usuarios)
    total_premium = len([u for u in usuarios if u.get('plano') == 'premium'])
    total_gratuito = len([u for u in usuarios if u.get('plano') == 'gratuito'])
    total_demo = len([u for u in usuarios if u.get('plano') == 'demo'])
    total_ativos = len([u for u in usuarios if u.get('ativo', True)])
    total_inativos = total_usuarios - total_ativos
    receita_total = sum(p.get('valor', 0) for p in pagamentos if p.get('status') == 'confirmado')
    
    # ============================================================
    # HEADER
    # ============================================================
    with ui.row().classes('w-full items-center justify-between p-4').style('background:#1e293b;color:white;flex-wrap:wrap;gap:12px;'):
        with ui.row().classes('items-center gap-3'):
            ui.label("🔐 Painel Admin").style('font-size:20px;font-weight:700;')
            ui.label(f"| {datetime.now().strftime('%d/%m/%Y %H:%M')}").style('font-size:12px;color:#94a3b8;')
        with ui.row().classes('gap-2'):
            ui.button("🔄 Atualizar", on_click=lambda: ui.navigate.to('/admin/painel')).props('flat').style('color:white;')
            ui.button("📊 Relatório", on_click=gerar_relatorio).props('flat').style('color:#10b981;')
            ui.button("🚪 Sair", on_click=lambda: ui.navigate.to('/admin')).props('flat').style('color:#ef4444;')
    
    with ui.element('div').style('max-width:1300px;margin:0 auto;padding:24px 16px;'):
        
        # ============================================================
        # STATS
        # ============================================================
        with ui.row().classes('gap-3 mb-6').style('flex-wrap:wrap;'):
            stats_data = [
                ("👥 Total", total_usuarios, "#3b82f6"),
                ("💎 Premium", total_premium, "#8b5cf6"),
                ("🆓 Gratuitos", total_gratuito, "#f59e0b"),
                ("👑 Demo", total_demo, "#6366f1"),
                ("✅ Ativos", total_ativos, "#10b981"),
                ("❌ Inativos", total_inativos, "#ef4444"),
                ("💰 Receita", f"R$ {receita_total:,.2f}", "#10b981"),
            ]
            for titulo, valor, cor in stats_data:
                with ui.card().classes('p-4 text-center').style('flex:1;min-width:120px;'):
                    ui.label(str(valor)).style(f'font-size:24px;font-weight:700;color:{cor};')
                    ui.label(titulo).style('font-size:11px;color:#64748b;margin-top:4px;')
        
        # ============================================================
        # USUÁRIOS
        # ============================================================
        with ui.card().classes('w-full p-0 mb-6'):
            with ui.row().classes('items-center justify-between p-4 border-b'):
                ui.label("👥 Usuários Cadastrados").style('font-size:16px;font-weight:700;')
                with ui.row().classes('gap-2'):
                    ui.button("📧 Exportar CSV", on_click=exportar_csv).props('flat').style('color:#3b82f6;font-size:12px;')
                    ui.button("➕ Novo Usuário", on_click=abrir_form_novo_usuario).style('background:#10b981;color:white;border-radius:8px;font-size:12px;padding:6px 12px;')
            
            if not usuarios:
                with ui.element('div').style('padding:40px;text-align:center;'):
                    ui.label("Nenhum usuário cadastrado").style('color:#94a3b8;')
            else:
                for u in usuarios:
                    plano = u.get('plano', 'gratuito')
                    ativo = u.get('ativo', True)
                    cor_plano = '#10b981' if plano == 'premium' else '#f59e0b' if plano == 'gratuito' else '#6366f1'
                    
                    try:
                        data_cad = datetime.fromisoformat(u.get('data_criacao', '')).strftime('%d/%m/%Y')
                    except:
                        data_cad = 'N/A'
                    
                    try:
                        data_exp = datetime.fromisoformat(u.get('data_expiracao', '')).strftime('%d/%m/%Y') if u.get('data_expiracao') else None
                    except:
                        data_exp = None
                    
                    with ui.row().classes('items-center justify-between p-3 border-b').style('flex-wrap:wrap;gap:8px;border-color:#f1f5f9;'):
                        # Info
                        with ui.row().classes('items-center gap-3').style('flex:2;min-width:200px;'):
                            ui.label(u.get('avatar_emoji', '👤')).style('font-size:24px;')
                            with ui.column().classes('gap-0'):
                                with ui.row().classes('items-center gap-2'):
                                    ui.label(u.get('nome', '-')).style('font-size:14px;font-weight:600;')
                                    if not ativo:
                                        ui.label("INATIVO").style('font-size:9px;background:#fee2e2;color:#ef4444;padding:1px 6px;border-radius:4px;')
                                ui.label(u.get('email', '-')).style('font-size:12px;color:#94a3b8;')
                        
                        # Plano + Datas
                        with ui.row().classes('items-center gap-2'):
                            ui.label(plano.upper()).style(f'padding:2px 10px;border-radius:20px;font-size:10px;font-weight:600;background:{cor_plano}20;color:{cor_plano};')
                            ui.label(data_cad).style('font-size:11px;color:#94a3b8;')
                            if data_exp:
                                ui.label(f"⏰ {data_exp}").style('font-size:10px;color:#ef4444;')
                        
                        # Ações
                        with ui.row().classes('gap-1').style('flex-wrap:wrap;'):
                            if plano != 'premium':
                                ui.button('⭐ Premium', on_click=lambda u=u: ativar_premium(u)).style('font-size:10px;background:#8b5cf6;color:white;border-radius:4px;padding:4px 8px;')
                                ui.button('🎁 7d', on_click=lambda u=u: dar_cortesia(u, 7)).style('font-size:10px;background:#10b981;color:white;border-radius:4px;padding:4px 8px;')
                                ui.button('🎁 30d', on_click=lambda u=u: dar_cortesia(u, 30)).style('font-size:10px;background:#059669;color:white;border-radius:4px;padding:4px 8px;')
                            else:
                                ui.button('❌ Remover', on_click=lambda u=u: remover_premium(u)).style('font-size:10px;background:#fee2e2;color:#ef4444;border-radius:4px;padding:4px 8px;')
                                ui.button('➕ 30d', on_click=lambda u=u: dar_cortesia(u, 30)).style('font-size:10px;background:#10b981;color:white;border-radius:4px;padding:4px 8px;')
                            
                            if ativo:
                                ui.button('🔒 Desativar', on_click=lambda u=u: toggle_ativo(u, False)).style('font-size:10px;background:#fef3c7;color:#d97706;border-radius:4px;padding:4px 8px;')
                            else:
                                ui.button('🔓 Ativar', on_click=lambda u=u: toggle_ativo(u, True)).style('font-size:10px;background:#d1fae5;color:#059669;border-radius:4px;padding:4px 8px;')
                            
                            ui.button('🗑️', on_click=lambda u=u: confirmar_excluir_usuario(u)).style('font-size:10px;background:#fee2e2;color:#ef4444;border-radius:4px;padding:4px 8px;')
        
        # ============================================================
        # PAGAMENTOS
        # ============================================================
        with ui.card().classes('w-full p-0 mb-6'):
            with ui.row().classes('items-center justify-between p-4 border-b'):
                ui.label("💰 Histórico de Pagamentos").style('font-size:16px;font-weight:700;')
                ui.label(f"{len(pagamentos)} registros").style('font-size:12px;color:#94a3b8;')
            
            if not pagamentos:
                with ui.element('div').style('padding:40px;text-align:center;'):
                    ui.label("Nenhum pagamento registrado").style('color:#94a3b8;')
            else:
                for p in reversed(pagamentos[-30:]):
                    cor_status = '#10b981' if p.get('status') == 'confirmado' else '#f59e0b'
                    try:
                        data_pag = datetime.fromisoformat(p.get('data', '')).strftime('%d/%m/%Y %H:%M')
                    except:
                        data_pag = 'N/A'
                    
                    with ui.row().classes('items-center justify-between p-3 border-b').style('border-color:#f1f5f9;flex-wrap:wrap;gap:8px;'):
                        with ui.row().classes('items-center gap-3'):
                            ui.label(p.get('email', '-')).style('font-size:13px;font-weight:500;')
                            ui.label(p.get('metodo', '-').upper()).style('font-size:10px;background:#f1f5f9;padding:2px 8px;border-radius:4px;color:#64748b;')
                        
                        with ui.row().classes('items-center gap-3'):
                            ui.label(f"R$ {p.get('valor', 0):,.2f}").style('font-size:13px;font-weight:600;')
                            ui.label(p.get('status', '-').upper()).style(f'font-size:10px;font-weight:600;padding:2px 10px;border-radius:20px;background:{cor_status}20;color:{cor_status};')
                            ui.label(p.get('admin', '-')).style('font-size:10px;color:#94a3b8;')
                            ui.label(data_pag).style('font-size:11px;color:#94a3b8;')
        
        # ============================================================
        # CONFIGURAÇÕES
        # ============================================================
        with ui.card().classes('w-full p-0'):
            with ui.row().classes('items-center justify-between p-4 border-b'):
                ui.label("⚙️ Configurações").style('font-size:16px;font-weight:700;')
            
            with ui.element('div').style('padding:20px;'):
                ui.label("🔒 Alterar Senha do Painel").style('font-size:14px;font-weight:600;margin-bottom:12px;')
                with ui.row().classes('gap-3 items-end').style('flex-wrap:wrap;'):
                    nova_senha = ui.input("Nova Senha", password=True, password_toggle_button=True).props('outlined').style('flex:1;min-width:180px;')
                    confirmar_senha = ui.input("Confirmar Senha", password=True, password_toggle_button=True).props('outlined').style('flex:1;min-width:180px;')
                    ui.button("Salvar", on_click=lambda: salvar_senha()).style('background:#8b5cf6;color:white;border-radius:8px;padding:12px 20px;')
                    
                    def salvar_senha():
                        if not nova_senha.value or len(nova_senha.value) < 6:
                            ui.notify("⚠️ Mínimo 6 caracteres", type="warning"); return
                        if nova_senha.value != confirmar_senha.value:
                            ui.notify("⚠️ Senhas não conferem", type="warning"); return
                        alterar_senha_admin(nova_senha.value)
                        ui.notify("✅ Senha alterada!", type="positive")
                        nova_senha.value = ''; confirmar_senha.value = ''
                
                ui.separator().style('margin:20px 0;')
                
                ui.label("📊 Informações do Sistema").style('font-size:14px;font-weight:600;margin-bottom:12px;')
                with ui.row().classes('gap-3').style('flex-wrap:wrap;'):
                    ui.label(f"Total de usuários: {total_usuarios}").style('font-size:13px;')
                    ui.label(f"Premium ativos: {total_premium}").style('font-size:13px;')
                    ui.label(f"Gratuitos: {total_gratuito}").style('font-size:13px;')
                    ui.label(f"Receita total: R$ {receita_total:,.2f}").style('font-size:13px;')
    
    # ============================================================
    # FUNÇÕES DE AÇÃO
    # ============================================================
    def ativar_premium(usuario):
        try:
            atualizar_plano_usuario(usuario['email'], 'premium')
            registrar_pagamento(usuario['email'], 'admin', 0, 'confirmado', 'admin')
            ui.notify(f"✅ Premium ativado para {usuario['nome']}!", type="positive")
        except Exception as e:
            ui.notify(f"❌ Erro: {str(e)}", type="negative")
        ui.timer(0.3, lambda: ui.navigate.to('/admin/painel'), once=True)
    
    def remover_premium(usuario):
        try:
            atualizar_plano_usuario(usuario['email'], 'gratuito')
            ui.notify(f"⬇ Premium removido de {usuario['nome']}", type="warning")
        except Exception as e:
            ui.notify(f"❌ Erro: {str(e)}", type="negative")
        ui.timer(0.3, lambda: ui.navigate.to('/admin/painel'), once=True)
    
    def dar_cortesia(usuario, dias):
        try:
            # Recarregar lista fresca
            usuarios_lista = carregar_usuarios()
            encontrado = False
            for u in usuarios_lista:
                if u.get('email', '').lower() == usuario.get('email', '').lower():
                    u['plano'] = 'premium'
                    u['data_expiracao'] = (datetime.now() + timedelta(days=dias)).isoformat()
                    u['ativo'] = True
                    encontrado = True
                    break
            
            if encontrado:
                salvar_usuarios(usuarios_lista)
                registrar_pagamento(usuario['email'], 'cortesia', 0, 'cortesia', 'admin')
                ui.notify(f"🎁 {dias} dias de Premium para {usuario['nome']}!", type="positive")
            else:
                ui.notify(f"❌ Usuário não encontrado", type="negative")
        except Exception as e:
            ui.notify(f"❌ Erro ao dar cortesia: {str(e)}", type="negative")
        ui.timer(0.3, lambda: ui.navigate.to('/admin/painel'), once=True)
    
    def toggle_ativo(usuario, ativo):
        try:
            usuarios_lista = carregar_usuarios()
            for u in usuarios_lista:
                if u.get('email', '').lower() == usuario.get('email', '').lower():
                    u['ativo'] = ativo
                    break
            salvar_usuarios(usuarios_lista)
            status = "ativado" if ativo else "desativado"
            ui.notify(f"🔒 Usuário {status}!", type="info")
        except Exception as e:
            ui.notify(f"❌ Erro: {str(e)}", type="negative")
        ui.timer(0.3, lambda: ui.navigate.to('/admin/painel'), once=True)
    
    def confirmar_excluir_usuario(usuario):
        with ui.dialog() as dialog, ui.card().classes('p-6 rounded-2xl max-w-[400px]'):
            ui.label("🗑️ Excluir Usuário?").style('font-size:18px;font-weight:700;color:#ef4444;margin-bottom:8px;')
            ui.label(f"Nome: {usuario.get('nome', '-')}").style('font-size:14px;')
            ui.label(f"Email: {usuario.get('email', '-')}").style('font-size:14px;color:#64748b;margin-bottom:16px;')
            ui.label("⚠️ Esta ação não pode ser desfeita!").style('font-size:12px;color:#ef4444;margin-bottom:16px;')
            
            with ui.row().classes('justify-end gap-2'):
                ui.button("Cancelar", on_click=dialog.close).props('outline')
                ui.button("Excluir", on_click=lambda: [excluir_usuario(usuario), dialog.close()]).style('background:#ef4444;color:white;')
        dialog.open()
    
    def excluir_usuario(usuario):
        try:
            usuarios_lista = carregar_usuarios()
            usuarios_lista = [u for u in usuarios_lista if u.get('email', '').lower() != usuario.get('email', '').lower()]
            salvar_usuarios(usuarios_lista)
            
            # Remover arquivo de dados
            arquivo = f"data/{usuario['email'].replace('@','_').replace('.','_').lower()}.json"
            if os.path.exists(arquivo):
                os.remove(arquivo)
            
            ui.notify(f"🗑️ Usuário {usuario['nome']} excluído!", type="warning")
        except Exception as e:
            ui.notify(f"❌ Erro: {str(e)}", type="negative")
        ui.timer(0.3, lambda: ui.navigate.to('/admin/painel'), once=True)
    
    def gerar_relatorio():
        texto = f"RELATÓRIO CARTÓMETRO - {datetime.now().strftime('%d/%m/%Y %H:%M')}\n"
        texto += f"{'='*50}\n"
        texto += f"Total Usuários: {total_usuarios}\n"
        texto += f"Premium: {total_premium}\n"
        texto += f"Gratuitos: {total_gratuito}\n"
        texto += f"Demo: {total_demo}\n"
        texto += f"Ativos: {total_ativos}\n"
        texto += f"Receita: R$ {receita_total:,.2f}\n"
        texto += f"{'='*50}\n"
        texto += f"\nUSUÁRIOS:\n"
        for u in usuarios:
            texto += f"  {u.get('nome','-')} | {u.get('email','-')} | {u.get('plano','-')} | {'Ativo' if u.get('ativo',True) else 'Inativo'}\n"
        
        with ui.dialog() as dialog, ui.card().classes('p-6 rounded-2xl max-w-[600px] max-h-[80vh]'):
            ui.label("📊 Relatório").style('font-size:18px;font-weight:700;margin-bottom:12px;')
            ui.textarea(value=texto).props('outlined readonly').style('width:100%;height:400px;font-family:monospace;font-size:11px;')
            ui.button("Fechar", on_click=dialog.close).props('outline').classes('mt-3')
        dialog.open()
    
    def exportar_csv():
        csv = "Nome,Email,Plano,Ativo,Data Cadastro,Expiração\n"
        for u in usuarios:
            csv += f"{u.get('nome','')},{u.get('email','')},{u.get('plano','')},{u.get('ativo',True)},{u.get('data_criacao','')},{u.get('data_expiracao','')}\n"
        
        with ui.dialog() as dialog, ui.card().classes('p-6 rounded-2xl max-w-[600px]'):
            ui.label("📧 Exportar CSV").style('font-size:18px;font-weight:700;margin-bottom:12px;')
            ui.textarea(value=csv).props('outlined readonly').style('width:100%;height:300px;font-family:monospace;font-size:11px;')
            ui.label("Copie o conteúdo acima e salve como .csv").style('font-size:12px;color:#64748b;margin-top:8px;')
            ui.button("Fechar", on_click=dialog.close).props('outline').classes('mt-3')
        dialog.open()
    
    def abrir_form_novo_usuario():
        with ui.dialog() as dialog, ui.card().classes('p-6 rounded-2xl max-w-[450px]'):
            ui.label("➕ Novo Usuário").style('font-size:18px;font-weight:700;margin-bottom:16px;')
            
            nome_inp = ui.input("Nome completo").props('outlined').classes('w-full mb-3')
            email_inp = ui.input("Email").props('outlined').classes('w-full mb-3')
            senha_inp = ui.input("Senha", password=True, password_toggle_button=True).props('outlined').classes('w-full mb-3')
            plano_inp = ui.select(["gratuito", "premium"], value="gratuito", label="Plano").props('outlined').classes('w-full mb-4')
            
            erro = ui.label('').style('color:#ef4444;font-size:12px;display:none;')
            
            def criar():
                nome = nome_inp.value.strip() if nome_inp.value else ''
                email = email_inp.value.strip() if email_inp.value else ''
                senha = senha_inp.value or ''
                
                if not nome or not email or not senha:
                    erro.style('display:block'); erro.set_text('Preencha todos os campos'); return
                
                from db import criar_usuario
                sucesso, msg, _ = criar_usuario(nome, email, senha, plano_inp.value)
                if sucesso:
                    ui.notify(f"✅ Usuário criado!", type="positive")
                    dialog.close()
                    ui.timer(0.3, lambda: ui.navigate.to('/admin/painel'), once=True)
                else:
                    erro.style('display:block'); erro.set_text(msg)
            
            with ui.row().classes('justify-end gap-2'):
                ui.button("Cancelar", on_click=dialog.close).props('outline')
                ui.button("Criar", on_click=criar).style('background:#10b981;color:white;')


# ============================================================
# INICIALIZAR
# ============================================================
inicializar_admin()