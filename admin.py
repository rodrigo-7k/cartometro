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
# CONFIGURAÇÃO
# ============================================================
ADMIN_FILE = 'admin_config.json'
PAGAMENTOS_FILE = 'pagamentos.json'

ADMIN_EMAIL = "admin@cartometro.com"
ADMIN_SENHA = "Cartometro@2024"
ADMIN_NOME = "Administrador"


# ============================================================
# INICIALIZAÇÃO
# ============================================================
def inicializar_admin():
    """Cria configuração inicial do admin SEMPRE"""
    config = {
        "admin": {
            "email": ADMIN_EMAIL,
            "senha": hash_senha(ADMIN_SENHA),
            "nome": ADMIN_NOME,
            "ultimo_acesso": None
        }
    }
    salvar_json(ADMIN_FILE, config)
    print(f"✅ Admin criado: {ADMIN_EMAIL}")
    print(f"🔑 Senha: {ADMIN_SENHA}")
    
    if not os.path.exists(PAGAMENTOS_FILE):
        salvar_json(PAGAMENTOS_FILE, [])


def carregar_config_admin():
    """Carrega configuração do admin"""
    config = carregar_json(ADMIN_FILE)
    if not config:
        # Recriar se não existir
        inicializar_admin()
        config = carregar_json(ADMIN_FILE)
    return config


def autenticar_admin(email, senha):
    """Autentica acesso ao painel admin"""
    config = carregar_config_admin()
    admin = config.get("admin", {})
    
    email_correto = admin.get("email") == email.strip().lower()
    senha_correta = admin.get("senha") == hash_senha(senha)
    
    if email_correto and senha_correta:
        config["admin"]["ultimo_acesso"] = datetime.now().isoformat()
        salvar_json(ADMIN_FILE, config)
        return True
    
    return False


def alterar_senha_admin(nova_senha):
    """Altera a senha do admin"""
    config = carregar_config_admin()
    config["admin"]["senha"] = hash_senha(nova_senha)
    salvar_json(ADMIN_FILE, config)
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
    </style>
    """)
    
    with ui.element('div').classes('admin-login-card'):
        ui.label("🔐 Painel Admin").style('font-size:24px;font-weight:700;color:#1e293b;text-align:center;margin-bottom:4px;')
        ui.label("Cartometro").style('font-size:14px;color:#94a3b8;text-align:center;margin-bottom:32px;')
        
        ui.label("Email").style('font-size:13px;font-weight:500;color:#475569;margin-bottom:6px;')
        email_input = ui.input(placeholder="admin@cartometro.com").props('outlined').classes('w-full').style('margin-bottom:20px;')
        
        ui.label("Senha").style('font-size:13px;font-weight:500;color:#475569;margin-bottom:6px;')
        senha_input = ui.input(placeholder="••••••••", password=True, password_toggle_button=True).props('outlined').classes('w-full').style('margin-bottom:20px;')
        
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
                erro_label.set_text('❌ Acesso negado. Verifique email e senha.')
        
        ui.button("Acessar Painel", on_click=fazer_login_admin).props('no-caps').style(
            'width:100%;height:48px;border-radius:10px;'
            'background:#8b5cf6;color:white;border:none;'
            'font-size:15px;font-weight:600;cursor:pointer;'
            'font-family:"DM Sans",sans-serif;'
        )
        
        ui.label(f"🔑 Email: {ADMIN_EMAIL}").style('font-size:11px;color:#94a3b8;text-align:center;margin-top:24px;')
        ui.label(f"🔒 Senha: {ADMIN_SENHA}").style('font-size:11px;color:#94a3b8;text-align:center;')


# ============================================================
# PAINEL ADMIN (APÓS LOGIN)
# ============================================================
@ui.page('/admin/painel')
def admin_painel():
    """Painel de gerenciamento"""
    
    ui.add_head_html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
        * { box-sizing: border-box; }
        body { font-family: 'DM Sans', sans-serif; background: #f1f5f9; margin: 0; padding: 0; }
    </style>
    """)
    
    usuarios = carregar_usuarios()
    pagamentos = carregar_pagamentos()
    
    total_usuarios = len(usuarios)
    total_premium = len([u for u in usuarios if u.get('plano') == 'premium'])
    total_gratuito = len([u for u in usuarios if u.get('plano') == 'gratuito'])
    receita_total = sum(p.get('valor', 0) for p in pagamentos if p.get('status') == 'confirmado')
    
    # Header
    with ui.row().classes('w-full items-center justify-between p-4').style('background:linear-gradient(135deg,#1e293b,#0f172a);color:white;'):
        with ui.row().classes('items-center gap-3'):
            ui.label("🔐 Painel Admin - Cartometro").classes('text-xl font-bold')
            ui.label(f"| {datetime.now().strftime('%d/%m/%Y %H:%M')}").classes('text-sm text-gray-400')
        with ui.row().classes('gap-3'):
            ui.button("🔄 Atualizar", on_click=lambda: ui.navigate.to('/admin/painel')).props('flat').style('color:white;')
            ui.button("🚪 Sair", on_click=lambda: ui.navigate.to('/admin')).props('flat').style('color:#ef4444;')
    
    with ui.element('div').style('max-width:1200px;margin:0 auto;padding:24px;'):
        
        # Stats
        with ui.row().classes('gap-4 mb-6'):
            for titulo, valor, cor in [
                ("Total Usuários", total_usuarios, "#3b82f6"),
                ("Premium", total_premium, "#8b5cf6"),
                ("Gratuitos", total_gratuito, "#f59e0b"),
                ("Receita", f"R$ {receita_total:,.2f}", "#10b981"),
            ]:
                with ui.card().classes('flex-1 p-4 text-center'):
                    ui.label(str(valor)).style(f'font-size:32px;font-weight:700;color:{cor};')
                    ui.label(titulo).classes('text-sm text-gray-500')
        
        # Lista de usuários
        ui.label("👥 Usuários Cadastrados").classes('text-lg font-bold mb-3')
        
        with ui.card().classes('w-full p-0'):
            for u in usuarios:
                plano = u.get('plano', 'gratuito')
                cor_plano = '#10b981' if plano == 'premium' else '#f59e0b'
                
                try:
                    data_cad = datetime.fromisoformat(u.get('data_criacao', '')).strftime('%d/%m/%Y')
                except:
                    data_cad = 'N/A'
                
                try:
                    data_exp = datetime.fromisoformat(u.get('data_expiracao', '')).strftime('%d/%m/%Y') if u.get('data_expiracao') else 'N/A'
                except:
                    data_exp = 'N/A'
                
                with ui.row().classes('items-center justify-between p-3 border-b').style('border-color:#f1f5f9;'):
                    with ui.row().classes('items-center gap-3 flex-1'):
                        ui.label(u.get('avatar_emoji', '👤')).classes('text-xl')
                        with ui.column().classes('gap-0'):
                            ui.label(u.get('nome', '-')).classes('font-semibold text-sm')
                            ui.label(u.get('email', '-')).classes('text-xs text-gray-400')
                    
                    with ui.row().classes('items-center gap-2'):
                        ui.label(plano.upper()).style(f'padding:2px 12px;border-radius:20px;font-size:11px;font-weight:600;background:{cor_plano}20;color:{cor_plano};')
                        ui.label(data_cad).classes('text-xs text-gray-400')
                        
                        if plano != 'premium':
                            ui.button('⭐ Premium', on_click=lambda u=u: ativar_premium(u)).style('font-size:11px;background:#8b5cf6;color:white;border-radius:6px;padding:4px 10px;')
                            ui.button('🎁 7 dias', on_click=lambda u=u: dar_cortesia(u, 7)).style('font-size:11px;background:#10b981;color:white;border-radius:6px;padding:4px 10px;')
                        else:
                            ui.button('❌ Remover', on_click=lambda u=u: remover_premium(u)).style('font-size:11px;background:#fee2e2;color:#ef4444;border-radius:6px;padding:4px 10px;')
                            ui.button('🎁 +30 dias', on_click=lambda u=u: dar_cortesia(u, 30)).style('font-size:11px;background:#10b981;color:white;border-radius:6px;padding:4px 10px;')
        
        # Pagamentos
        if pagamentos:
            ui.label("💰 Últimos Pagamentos").classes('text-lg font-bold mb-3 mt-6')
            with ui.card().classes('w-full p-0'):
                for p in reversed(pagamentos[-10:]):
                    try:
                        data_pag = datetime.fromisoformat(p.get('data', '')).strftime('%d/%m/%Y %H:%M')
                    except:
                        data_pag = 'N/A'
                    
                    with ui.row().classes('items-center justify-between p-3 border-b').style('border-color:#f1f5f9;'):
                        ui.label(p.get('email', '-')).classes('text-sm')
                        ui.label(p.get('metodo', '-').upper()).classes('text-xs text-gray-400')
                        ui.label(f"R$ {p.get('valor', 0):,.2f}").classes('text-sm font-semibold')
                        ui.label(data_pag).classes('text-xs text-gray-400')
    
    # Funções
    def ativar_premium(usuario):
        atualizar_plano_usuario(usuario['email'], 'premium')
        registrar_pagamento(usuario['email'], 'admin', 0, 'confirmado', 'admin')
        ui.notify(f"✅ Premium ativado para {usuario['nome']}!", type="positive")
        ui.timer(0.5, lambda: ui.navigate.to('/admin/painel'), once=True)
    
    def remover_premium(usuario):
        atualizar_plano_usuario(usuario['email'], 'gratuito')
        ui.notify(f"⬇ Premium removido de {usuario['nome']}", type="warning")
        ui.timer(0.5, lambda: ui.navigate.to('/admin/painel'), once=True)
    
    def dar_cortesia(usuario, dias):
        usuarios_lista = carregar_usuarios()
        for u in usuarios_lista:
            if u['email'] == usuario['email']:
                u['plano'] = 'premium'
                u['data_expiracao'] = (datetime.now() + timedelta(days=dias)).isoformat()
                u['ativo'] = True
                break
        salvar_usuarios(usuarios_lista)
        registrar_pagamento(usuario['email'], 'cortesia', 0, 'cortesia', 'admin')
        ui.notify(f"🎁 {dias} dias de Premium para {usuario['nome']}!", type="positive")
        ui.timer(0.5, lambda: ui.navigate.to('/admin/painel'), once=True)


# ============================================================
# INICIALIZAR
# ============================================================
inicializar_admin()