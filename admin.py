"""
Painel Administrativo - Cartometro
Gerenciamento de Usuários e Assinaturas
Acesso restrito com login próprio
"""

from nicegui import ui
from db import (
    carregar_usuarios, salvar_usuarios, buscar_usuario_por_email,
    atualizar_plano_usuario, PLANOS, carregar_json, salvar_json,
    hash_senha
)
from datetime import datetime, timedelta
import os

# ============================================================
# CONFIGURAÇÃO DO ADMIN
# ============================================================
ADMIN_FILE = 'admin_config.json'
PAGAMENTOS_FILE = 'pagamentos.json'

# Credenciais padrão do admin (altere aqui ou pelo painel)
ADMIN_PADRAO = {
    "email": "admin@cartometro.com",
    "senha": "Cartometro@2024",  # Será hasheada na inicialização
    "nome": "Administrador"
}

# ============================================================
# INICIALIZAÇÃO
# ============================================================
def inicializar_admin():
    """Cria configuração inicial do admin"""
    if not os.path.exists(ADMIN_FILE):
        config = {
            "admin": {
                "email": ADMIN_PADRAO["email"],
                "senha": hash_senha(ADMIN_PADRAO["senha"]),
                "nome": ADMIN_PADRAO["nome"],
                "ultimo_acesso": None
            }
        }
        salvar_json(ADMIN_FILE, config)
        print(f"✅ Admin criado: {ADMIN_PADRAO['email']}")
        print(f"🔑 Senha inicial: {ADMIN_PADRAO['senha']}")
    
    if not os.path.exists(PAGAMENTOS_FILE):
        salvar_json(PAGAMENTOS_FILE, [])


def carregar_config_admin():
    """Carrega configuração do admin"""
    return carregar_json(ADMIN_FILE) or {}


def salvar_config_admin(config):
    """Salva configuração do admin"""
    salvar_json(ADMIN_FILE, config)


def autenticar_admin(email, senha):
    """Autentica acesso ao painel admin"""
    config = carregar_config_admin()
    admin = config.get("admin", {})
    
    if admin.get("email") == email and admin.get("senha") == hash_senha(senha):
        # Atualizar último acesso
        config["admin"]["ultimo_acesso"] = datetime.now().isoformat()
        salvar_config_admin(config)
        return True
    
    return False


def alterar_senha_admin(nova_senha):
    """Altera a senha do admin"""
    config = carregar_config_admin()
    config["admin"]["senha"] = hash_senha(nova_senha)
    salvar_config_admin(config)
    return True


def carregar_pagamentos():
    """Carrega histórico de pagamentos"""
    return carregar_json(PAGAMENTOS_FILE) or []


def salvar_pagamentos(pagamentos):
    """Salva histórico de pagamentos"""
    salvar_json(PAGAMENTOS_FILE, pagamentos)


def registrar_pagamento(email, metodo, valor, status="confirmado", admin_responsavel=""):
    """Registra um pagamento no histórico"""
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
# TELA DE LOGIN DO ADMIN
# ============================================================
@ui.page('/admin')
def admin_login():
    """Tela de login do painel admin"""
    
    ui.add_head_html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: 'DM Sans', sans-serif;
            background: linear-gradient(135deg, #1e293b, #0f172a);
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .admin-login-card {
            background: white;
            border-radius: 20px;
            padding: 48px 40px;
            width: 400px;
            max-width: 90vw;
            box-shadow: 0 25px 60px rgba(0,0,0,0.3);
        }
        
        .admin-login-card h1 {
            font-size: 24px;
            font-weight: 700;
            color: #1e293b;
            text-align: center;
            margin-bottom: 4px;
        }
        
        .admin-login-card p {
            font-size: 14px;
            color: #94a3b8;
            text-align: center;
            margin-bottom: 32px;
        }
        
        .campo {
            margin-bottom: 20px;
        }
        
        .campo label {
            font-size: 13px;
            font-weight: 500;
            color: #475569;
            margin-bottom: 6px;
            display: block;
        }
    </style>
    """)
    
    with ui.element('div').classes('admin-login-card'):
        ui.label("🔐 Painel Admin").style('font-size:24px;font-weight:700;color:#1e293b;text-align:center;margin-bottom:4px;')
        ui.label("Cartometro").style('font-size:14px;color:#94a3b8;text-align:center;margin-bottom:32px;')
        
        with ui.element('div').classes('campo'):
            ui.label("Email")
            email_input = ui.input(placeholder="admin@cartometro.com").props('outlined').classes('w-full')
        
        with ui.element('div').classes('campo'):
            ui.label("Senha")
            senha_input = ui.input(placeholder="••••••••", password=True, password_toggle_button=True).props('outlined').classes('w-full')
        
        erro_label = ui.label('').style('color:#ef4444;font-size:13px;text-align:center;display:none;margin-bottom:16px;')
        
        def fazer_login_admin():
            email = email_input.value.strip() if email_input.value else ''
            senha = senha_input.value or ''
            
            if not email or not senha:
                erro_label.style('display:block')
                erro_label.set_text('⚠️ Preencha todos os campos')
                return
            
            if autenticar_admin(email, senha):
                ui.notify("✅ Acesso autorizado!", type="positive", position="top")
                ui.navigate.to('/admin/painel')
            else:
                erro_label.style('display:block')
                erro_label.set_text('❌ Acesso negado')
        
        ui.button("Acessar Painel", on_click=fazer_login_admin).props('no-caps').style(
            'width:100%;height:48px;border-radius:10px;'
            'background:#8b5cf6;color:white;border:none;'
            'font-size:15px;font-weight:600;cursor:pointer;'
            'font-family:"DM Sans",sans-serif;'
        )
        
        ui.label("🔑 Admin: admin@cartometro.com / Cartometro@2024").style(
            'font-size:11px;color:#94a3b8;text-align:center;margin-top:24px;'
        )


# ============================================================
# PAINEL ADMIN (APÓS LOGIN)
# ============================================================
@ui.page('/admin/painel')
def admin_painel():
    """Painel de gerenciamento (acesso restrito)"""
    
    ui.add_head_html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
        
        * { box-sizing: border-box; }
        
        body {
            font-family: 'DM Sans', sans-serif;
            background: #f1f5f9;
            margin: 0;
            padding: 0;
        }
        
        .admin-layout {
            display: flex;
            min-height: 100vh;
        }
        
        .admin-sidebar {
            width: 260px;
            background: linear-gradient(180deg, #1e293b, #0f172a);
            color: white;
            padding: 24px 16px;
            position: fixed;
            top: 0;
            left: 0;
            bottom: 0;
            overflow-y: auto;
        }
        
        .admin-main {
            margin-left: 260px;
            flex: 1;
            padding: 32px;
        }
        
        .admin-header {
            background: white;
            border-radius: 12px;
            padding: 20px 24px;
            margin-bottom: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }
        
        .stat-card {
            background: white;
            border-radius: 12px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            text-align: center;
        }
        
        .stat-card h2 {
            font-size: 36px;
            font-weight: 700;
            margin: 0;
        }
        
        .stat-card p {
            font-size: 13px;
            color: #64748b;
            margin: 4px 0 0 0;
        }
        
        .user-table {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }
        
        .user-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 16px 24px;
            border-bottom: 1px solid #f1f5f9;
            transition: background 0.15s;
        }
        
        .user-row:hover {
            background: #f8fafc;
        }
        
        .user-row:last-child {
            border-bottom: none;
        }
        
        .badge {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }
        
        .btn-acao {
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 12px;
            font-weight: 500;
            cursor: pointer;
            border: none;
            transition: all 0.15s;
        }
        
        .btn-premium {
            background: #8b5cf6;
            color: white;
        }
        
        .btn-premium:hover {
            background: #7c3aed;
        }
        
        .btn-cortesia {
            background: #10b981;
            color: white;
        }
        
        .btn-cortesia:hover {
            background: #059669;
        }
        
        .btn-remover {
            background: #fee2e2;
            color: #ef4444;
        }
        
        .btn-remover:hover {
            background: #fecaca;
        }
        
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }
        
        .modal-overlay.active {
            display: flex;
        }
        
        .modal-card {
            background: white;
            border-radius: 16px;
            padding: 32px;
            width: 500px;
            max-width: 90vw;
            box-shadow: 0 25px 60px rgba(0,0,0,0.3);
        }
    </style>
    """)
    
    # Dados
    usuarios = carregar_usuarios()
    pagamentos = carregar_pagamentos()
    config_admin = carregar_config_admin()
    
    total_usuarios = len(usuarios)
    total_premium = len([u for u in usuarios if u.get('plano') == 'premium'])
    total_gratuito = len([u for u in usuarios if u.get('plano') == 'gratuito'])
    total_pagamentos = len(pagamentos)
    receita_total = sum(p.get('valor', 0) for p in pagamentos if p.get('status') == 'confirmado')
    
    with ui.element('div').classes('admin-layout'):
        # ============================================================
        # SIDEBAR
        # ============================================================
        with ui.element('div').classes('admin-sidebar'):
            ui.label("🔐 Admin").classes('text-lg font-bold mb-1')
            ui.label("Cartometro").classes('text-xs text-gray-400 mb-8')
            
            with ui.column().classes('gap-1'):
                ui.button("📊 Dashboard", on_click=lambda: scroll_to('dashboard')).props('flat').style('color:white;justify-content:flex-start;')
                ui.button("👥 Usuários", on_click=lambda: scroll_to('usuarios')).props('flat').style('color:white;justify-content:flex-start;')
                ui.button("💰 Pagamentos", on_click=lambda: scroll_to('pagamentos')).props('flat').style('color:white;justify-content:flex-start;')
                ui.button("⚙️ Config", on_click=lambda: scroll_to('config')).props('flat').style('color:white;justify-content:flex-start;')
            
            ui.element('div').style('margin-top:auto;')
            ui.button("🚪 Sair", on_click=lambda: ui.navigate.to('/admin')).props('flat').style('color:#ef4444;justify-content:flex-start;')
        
        # ============================================================
        # CONTEÚDO PRINCIPAL
        # ============================================================
        with ui.element('div').classes('admin-main'):
            
            # Header
            with ui.element('div').classes('admin-header'):
                with ui.row().classes('items-center justify-between'):
                    with ui.column().classes('gap-0'):
                        ui.label("Dashboard Administrativo").classes('text-xl font-bold text-gray-800')
                        ui.label(f"Bem-vindo, {config_admin.get('admin', {}).get('nome', 'Admin')}").classes('text-sm text-gray-500')
                    ui.label(datetime.now().strftime("%d/%m/%Y %H:%M")).classes('text-sm text-gray-400')
            
            # ============================================================
            # STATS
            # ============================================================
            ui.element('div').props('id=dashboard')
            with ui.row().classes('gap-4 mb-8'):
                with ui.element('div').classes('stat-card flex-1'):
                    ui.label(str(total_usuarios)).classes('text-3xl font-bold text-blue-600')
                    ui.label("Total de Usuários").classes('text-sm text-gray-500')
                
                with ui.element('div').classes('stat-card flex-1'):
                    ui.label(str(total_premium)).classes('text-3xl font-bold text-purple-600')
                    ui.label("Premium").classes('text-sm text-gray-500')
                
                with ui.element('div').classes('stat-card flex-1'):
                    ui.label(str(total_gratuito)).classes('text-3xl font-bold text-yellow-600')
                    ui.label("Gratuitos").classes('text-sm text-gray-500')
                
                with ui.element('div').classes('stat-card flex-1'):
                    ui.label(f"R$ {receita_total:,.2f}").classes('text-2xl font-bold text-green-600')
                    ui.label("Receita Total").classes('text-sm text-gray-500')
            
            # ============================================================
            # LISTA DE USUÁRIOS
            # ============================================================
            ui.element('div').props('id=usuarios')
            with ui.element('div').classes('user-table mb-8'):
                with ui.element('div').style('padding:20px 24px;border-bottom:1px solid #f1f5f9;'):
                    ui.label("👥 Usuários Cadastrados").classes('text-lg font-bold text-gray-800')
                
                # Cabeçalho
                with ui.element('div').classes('user-row').style('background:#f8fafc;font-weight:600;'):
                    ui.label("Usuário").style('flex:2;')
                    ui.label("Plano").style('flex:1;text-align:center;')
                    ui.label("Cadastro").style('flex:1;text-align:center;')
                    ui.label("Expiração").style('flex:1;text-align:center;')
                    ui.label("Ações").style('flex:2;text-align:center;')
                
                for u in usuarios:
                    plano = u.get('plano', 'gratuito')
                    cor_plano = '#10b981' if plano == 'premium' else '#f59e0b' if plano == 'gratuito' else '#3b82f6'
                    
                    try:
                        data_cad = datetime.fromisoformat(u.get('data_criacao', '')).strftime('%d/%m/%Y')
                    except:
                        data_cad = 'N/A'
                    
                    try:
                        data_exp = datetime.fromisoformat(u.get('data_expiracao', '')).strftime('%d/%m/%Y') if u.get('data_expiracao') else 'N/A'
                    except:
                        data_exp = 'N/A'
                    
                    with ui.element('div').classes('user-row'):
                        # Info usuário
                        with ui.row().classes('items-center gap-3').style('flex:2;'):
                            ui.label(u.get('avatar_emoji', '👤')).classes('text-xl')
                            with ui.column().classes('gap-0'):
                                ui.label(u.get('nome', '-')).classes('font-semibold text-sm')
                                ui.label(u.get('email', '-')).classes('text-xs text-gray-400')
                        
                        # Plano
                        with ui.element('div').style('flex:1;text-align:center;'):
                            ui.label(plano.upper()).classes('badge').style(f'background:{cor_plano}20;color:{cor_plano};')
                        
                        # Data cadastro
                        ui.label(data_cad).style('flex:1;text-align:center;font-size:13px;color:#64748b;')
                        
                        # Expiração
                        ui.label(data_exp).style('flex:1;text-align:center;font-size:13px;color:#64748b;')
                        
                        # Ações
                        with ui.row().classes('gap-2 justify-center').style('flex:2;'):
                            if plano != 'premium':
                                ui.button('⭐ Premium', on_click=lambda u=u: ativar_premium(u)).classes('btn-acao btn-premium')
                                ui.button('🎁 7 dias', on_click=lambda u=u: dar_cortesia(u, 7)).classes('btn-acao btn-cortesia')
                            else:
                                ui.button('❌ Remover', on_click=lambda u=u: remover_premium(u)).classes('btn-acao btn-remover')
                                ui.button('🎁 +30 dias', on_click=lambda u=u: dar_cortesia(u, 30)).classes('btn-acao btn-cortesia')
            
            # ============================================================
            # HISTÓRICO DE PAGAMENTOS
            # ============================================================
            ui.element('div').props('id=pagamentos')
            with ui.element('div').classes('user-table mb-8'):
                with ui.element('div').style('padding:20px 24px;border-bottom:1px solid #f1f5f9;'):
                    with ui.row().classes('items-center justify-between'):
                        ui.label("💰 Histórico de Pagamentos").classes('text-lg font-bold text-gray-800')
                        ui.label(f"{len(pagamentos)} registros").classes('text-sm text-gray-400')
                
                if not pagamentos:
                    with ui.element('div').style('padding:40px;text-align:center;'):
                        ui.label("Nenhum pagamento registrado").classes('text-gray-400')
                else:
                    for p in reversed(pagamentos[-20:]):  # Últimos 20
                        cor_status = '#10b981' if p.get('status') == 'confirmado' else '#f59e0b'
                        try:
                            data_pag = datetime.fromisoformat(p.get('data', '')).strftime('%d/%m/%Y %H:%M')
                        except:
                            data_pag = 'N/A'
                        
                        with ui.element('div').classes('user-row'):
                            ui.label(p.get('email', '-')).style('flex:2;font-size:13px;')
                            ui.label(p.get('metodo', '-').upper()).style('flex:1;text-align:center;font-size:12px;')
                            ui.label(f"R$ {p.get('valor', 0):,.2f}").style('flex:1;text-align:center;font-size:13px;font-weight:600;')
                            ui.label(p.get('status', '-').upper()).classes('badge').style(f'background:{cor_status}20;color:{cor_status};')
                            ui.label(data_pag).style('flex:1;text-align:center;font-size:12px;color:#94a3b8;')
            
            # ============================================================
            # CONFIGURAÇÕES DO ADMIN
            # ============================================================
            ui.element('div').props('id=config')
            with ui.element('div').classes('user-table'):
                with ui.element('div').style('padding:20px 24px;border-bottom:1px solid #f1f5f9;'):
                    ui.label("⚙️ Configurações do Admin").classes('text-lg font-bold text-gray-800')
                
                with ui.element('div').style('padding:24px;'):
                    ui.label("Alterar Senha do Painel Admin").classes('font-semibold mb-4')
                    
                    with ui.row().classes('gap-4 items-end'):
                        nova_senha = ui.input("Nova Senha", password=True, password_toggle_button=True).props('outlined').classes('flex-1')
                        confirmar_senha = ui.input("Confirmar Senha", password=True, password_toggle_button=True).props('outlined').classes('flex-1')
                        
                        def salvar_nova_senha():
                            if not nova_senha.value or len(nova_senha.value) < 6:
                                ui.notify("⚠️ Senha deve ter pelo menos 6 caracteres", type="warning")
                                return
                            if nova_senha.value != confirmar_senha.value:
                                ui.notify("⚠️ Senhas não conferem", type="warning")
                                return
                            
                            alterar_senha_admin(nova_senha.value)
                            ui.notify("✅ Senha alterada com sucesso!", type="positive")
                            nova_senha.value = ''
                            confirmar_senha.value = ''
                        
                        ui.button("Salvar Senha", on_click=salvar_nova_senha).style('background:#8b5cf6;color:white;border-radius:8px;')
    
    # ============================================================
    # FUNÇÕES DE AÇÃO
    # ============================================================
    def ativar_premium(usuario):
        atualizar_plano_usuario(usuario['email'], 'premium')
        registrar_pagamento(usuario['email'], 'admin_manual', 0, 'confirmado', 'admin')
        ui.notify(f"✅ Premium ativado para {usuario['nome']}!", type="positive")
        ui.timer(0.5, lambda: ui.navigate.to('/admin/painel'), once=True)
    
    def remover_premium(usuario):
        atualizar_plano_usuario(usuario['email'], 'gratuito')
        ui.notify(f"⬇ Premium removido de {usuario['nome']}", type="warning")
        ui.timer(0.5, lambda: ui.navigate.to('/admin/painel'), once=True)
    
    def dar_cortesia(usuario, dias):
        from db import carregar_usuarios as cu, salvar_usuarios as su
        usuarios_lista = cu()
        for u in usuarios_lista:
            if u['email'] == usuario['email']:
                u['plano'] = 'premium'
                u['data_expiracao'] = (datetime.now() + timedelta(days=dias)).isoformat()
                u['ativo'] = True
                break
        su(usuarios_lista)
        registrar_pagamento(usuario['email'], 'cortesia', 0, 'cortesia', 'admin')
        ui.notify(f"🎁 {dias} dias de Premium para {usuario['nome']}!", type="positive")
        ui.timer(0.5, lambda: ui.navigate.to('/admin/painel'), once=True)


# ============================================================
# INICIALIZAR
# ============================================================
inicializar_admin()