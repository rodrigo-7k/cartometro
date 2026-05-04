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
ADMIN_SENHA_HASH = hash_senha(ADMIN_SENHA)
ADMIN_NOME = "Administrador"


# ============================================================
# INICIALIZAÇÃO
# ============================================================
def inicializar_admin():
    """Cria arquivos necessários"""
    if not os.path.exists(PAGAMENTOS_FILE):
        salvar_json(PAGAMENTOS_FILE, [])
    
    # Garantir que o arquivo de config existe
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
    
    print(f"✅ Admin configurado: {ADMIN_EMAIL}")


def carregar_config_admin():
    """Carrega configuração do admin"""
    config = carregar_json(ADMIN_FILE)
    if config is None:
        config = {
            "admin": {
                "email": ADMIN_EMAIL,
                "senha": ADMIN_SENHA_HASH,
                "nome": ADMIN_NOME,
                "ultimo_acesso": None
            }
        }
        salvar_json(ADMIN_FILE, config)
    return config


def autenticar_admin(email, senha):
    """Autentica acesso ao painel admin"""
    # Verificação rápida primeiro
    if email.strip().lower() != ADMIN_EMAIL:
        return False
    
    if hash_senha(senha) != ADMIN_SENHA_HASH:
        return False
    
    # Atualizar último acesso
    try:
        config = carregar_config_admin()
        if config and "admin" in config:
            config["admin"]["ultimo_acesso"] = datetime.now().isoformat()
            salvar_json(ADMIN_FILE, config)
    except:
        pass
    
    return True


def alterar_senha_admin(nova_senha):
    """Altera a senha do admin"""
    global ADMIN_SENHA_HASH
    ADMIN_SENHA_HASH = hash_senha(nova_senha)
    
    config = carregar_config_admin()
    config["admin"]["senha"] = ADMIN_SENHA_HASH
    salvar_json(ADMIN_FILE, config)
    return True


def carregar_pagamentos():
    """Carrega histórico de pagamentos"""
    pagamentos = carregar_json(PAGAMENTOS_FILE)
    return pagamentos if pagamentos is not None else []


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
        
        .admin-login-card .subtitle {
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
        
        .btn-acessar {
            width: 100%;
            height: 48px;
            border-radius: 10px;
            background: #8b5cf6;
            color: white;
            border: none;
            font-size: 15px;
            font-weight: 600;
            cursor: pointer;
            font-family: 'DM Sans', sans-serif;
        }
        
        .btn-acessar:hover {
            background: #7c3aed;
        }
        
        .credential-info {
            margin-top: 24px;
            text-align: center;
        }
        
        .credential-info span {
            display: block;
            font-size: 11px;
            color: #94a3b8;
        }
    </style>
    """)
    
    with ui.element('div').classes('admin-login-card'):
        ui.label("🔐 Painel Admin").style('font-size:24px;font-weight:700;color:#1e293b;text-align:center;margin-bottom:4px;')
        ui.label("Cartometro - Gerenciamento").style('font-size:14px;color:#94a3b8;text-align:center;margin-bottom:32px;')
        
        with ui.element('div').classes('campo'):
            ui.label("Email")
            email_input = ui.input(placeholder="admin@cartometro.com").props('outlined').classes('w-full')
        
        with ui.element('div').classes('campo'):
            ui.label("Senha")
            senha_input = ui.input(placeholder="••••••••", password=True, password_toggle_button=True).props('outlined').classes('w-full')
        
        erro_label = ui.label('').style('color:#ef4444;font-size:13px;text-align:center;display:none;margin-bottom:16px;')
        
        def fazer_login_admin():
            email = email_input.value.strip().lower() if email_input.value else ''
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
        
        with ui.element('div').classes('credential-info'):
            ui.label(f"🔑 Email: {ADMIN_EMAIL}").style('font-size:11px;color:#94a3b8;text-align:center;margin-top:24px;')
            ui.label(f"🔒 Senha: {ADMIN_SENHA}").style('font-size:11px;color:#94a3b8;text-align:center;')


# ============================================================
# PAINEL ADMIN (APÓS LOGIN)
# ============================================================
@ui.page('/admin/painel')
def admin_painel():
    """Painel de gerenciamento completo"""
    
    ui.add_head_html("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap');
        
        * { box-sizing: border-box; margin: 0; padding: 0; }
        
        body {
            font-family: 'DM Sans', sans-serif;
            background: #f1f5f9;
            overflow-y: auto !important;
            height: auto !important;
        }
        
        .admin-header {
            background: linear-gradient(135deg, #1e293b, #0f172a);
            color: white;
            padding: 16px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 12px;
        }
        
        .admin-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 24px 16px;
        }
        
        .stat-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
            gap: 12px;
            margin-bottom: 24px;
        }
        
        .stat-card {
            background: white;
            border-radius: 12px;
            padding: 20px 16px;
            text-align: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
        }
        
        .stat-value {
            font-size: 28px;
            font-weight: 700;
        }
        
        .stat-label {
            font-size: 12px;
            color: #64748b;
            margin-top: 4px;
        }
        
        .section-card {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.06);
            margin-bottom: 20px;
        }
        
        .section-header {
            padding: 16px 20px;
            border-bottom: 1px solid #f1f5f9;
            font-size: 16px;
            font-weight: 700;
            color: #1e293b;
        }
        
        .user-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 14px 20px;
            border-bottom: 1px solid #f1f5f9;
            flex-wrap: wrap;
            gap: 8px;
        }
        
        .user-row:hover {
            background: #f8fafc;
        }
        
        .user-row:last-child {
            border-bottom: none;
        }
        
        .user-info {
            display: flex;
            align-items: center;
            gap: 12px;
            flex: 2;
            min-width: 200px;
        }
        
        .user-avatar {
            font-size: 28px;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            flex-shrink: 0;
        }
        
        .user-details {
            display: flex;
            flex-direction: column;
            gap: 0;
        }
        
        .user-nome {
            font-size: 14px;
            font-weight: 600;
            color: #1e293b;
        }
        
        .user-email {
            font-size: 12px;
            color: #94a3b8;
        }
        
        .badge-plano {
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            white-space: nowrap;
        }
        
        .acoes-container {
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
        }
        
        .btn-acao {
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 11px;
            font-weight: 500;
            cursor: pointer;
            border: none;
            transition: all 0.15s;
            white-space: nowrap;
        }
        
        .btn-premium {
            background: #8b5cf6;
            color: white;
        }
        
        .btn-premium:hover { background: #7c3aed; }
        
        .btn-cortesia {
            background: #10b981;
            color: white;
        }
        
        .btn-cortesia:hover { background: #059669; }
        
        .btn-remover {
            background: #fee2e2;
            color: #ef4444;
        }
        
        .btn-remover:hover { background: #fecaca; }
        
        .pagamento-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 20px;
            border-bottom: 1px solid #f1f5f9;
            flex-wrap: wrap;
            gap: 8px;
        }
        
        .empty-state {
            padding: 40px;
            text-align: center;
            color: #94a3b8;
        }
        
        .config-section {
            padding: 20px;
        }
        
        @media (max-width: 768px) {
            .admin-header {
                padding: 12px 16px;
            }
            .user-row {
                flex-direction: column;
                align-items: flex-start;
            }
            .acoes-container {
                width: 100%;
                justify-content: flex-end;
            }
        }
    </style>
    """)
    
    # Carregar dados
    usuarios = carregar_usuarios()
    pagamentos = carregar_pagamentos()
    config_admin = carregar_config_admin()
    
    total_usuarios = len(usuarios)
    total_premium = len([u for u in usuarios if u.get('plano') == 'premium'])
    total_gratuito = len([u for u in usuarios if u.get('plano') == 'gratuito'])
    total_demo = len([u for u in usuarios if u.get('plano') == 'demo'])
    receita_total = sum(p.get('valor', 0) for p in pagamentos if p.get('status') == 'confirmado')
    
    # ============================================================
    # HEADER
    # ============================================================
    with ui.element('div').classes('admin-header'):
        with ui.row().classes('items-center gap-3'):
            ui.label("🔐 Painel Admin").style('font-size:20px;font-weight:700;')
            ui.label("Cartometro").style('font-size:14px;color:#94a3b8;')
            ui.label(f"| {datetime.now().strftime('%d/%m/%Y %H:%M')}").style('font-size:12px;color:#64748b;')
        with ui.row().classes('gap-3'):
            ui.button("🔄 Atualizar", on_click=lambda: ui.navigate.to('/admin/painel')).props('flat').style('color:white;')
            ui.button("🚪 Sair", on_click=lambda: ui.navigate.to('/admin')).props('flat').style('color:#ef4444;')
    
    with ui.element('div').classes('admin-container'):
        
        # ============================================================
        # STATS
        # ============================================================
        with ui.element('div').classes('stat-grid'):
            stats = [
                ("Total Usuários", total_usuarios, "#3b82f6", "👥"),
                ("Premium", total_premium, "#8b5cf6", "💎"),
                ("Gratuitos", total_gratuito, "#f59e0b", "🆓"),
                ("Demo", total_demo, "#6366f1", "👑"),
            ]
            for titulo, valor, cor, icone in stats:
                with ui.element('div').classes('stat-card'):
                    ui.label(icone).style('font-size:24px;')
                    ui.label(str(valor)).style(f'font-size:28px;font-weight:700;color:{cor};')
                    ui.label(titulo).classes('stat-label')
            
            # Receita
            with ui.element('div').classes('stat-card'):
                ui.label("💰").style('font-size:24px;')
                ui.label(f"R$ {receita_total:,.2f}").style('font-size:20px;font-weight:700;color:#10b981;')
                ui.label("Receita Total").classes('stat-label')
        
        # ============================================================
        # USUÁRIOS
        # ============================================================
        with ui.element('div').classes('section-card'):
            with ui.element('div').classes('section-header'):
                with ui.row().classes('items-center justify-between w-full'):
                    ui.label("👥 Usuários Cadastrados")
                    ui.label(f"{total_usuarios} encontrados").classes('text-sm text-gray-400')
            
            if not usuarios:
                with ui.element('div').classes('empty-state'):
                    ui.icon('people').classes('text-4xl mb-2')
                    ui.label("Nenhum usuário cadastrado")
            
            for u in usuarios:
                plano = u.get('plano', 'gratuito')
                cor_plano = '#10b981' if plano == 'premium' else '#f59e0b' if plano == 'gratuito' else '#6366f1'
                
                try:
                    data_cad = datetime.fromisoformat(u.get('data_criacao', '')).strftime('%d/%m/%Y')
                except:
                    data_cad = 'N/A'
                
                try:
                    data_exp = datetime.fromisoformat(u.get('data_expiracao', '')).strftime('%d/%m/%Y') if u.get('data_expiracao') else None
                except:
                    data_exp = None
                
                with ui.element('div').classes('user-row'):
                    # Info usuário
                    with ui.element('div').classes('user-info'):
                        with ui.element('div').classes('user-avatar').style(f'background:{cor_plano}15;'):
                            ui.label(u.get('avatar_emoji', '👤'))
                        with ui.element('div').classes('user-details'):
                            ui.label(u.get('nome', '-')).classes('user-nome')
                            ui.label(u.get('email', '-')).classes('user-email')
                            if data_exp:
                                ui.label(f"Expira: {data_exp}").style('font-size:10px;color:#ef4444;')
                    
                    # Plano
                    with ui.row().classes('items-center gap-2'):
                        ui.label(plano.upper()).classes('badge-plano').style(f'background:{cor_plano}20;color:{cor_plano};')
                        ui.label(data_cad).style('font-size:11px;color:#94a3b8;')
                    
                    # Ações
                    with ui.element('div').classes('acoes-container'):
                        if plano != 'premium':
                            ui.button('⭐ Premium', on_click=lambda u=u: ativar_premium(u)).classes('btn-acao btn-premium')
                            ui.button('🎁 7 dias', on_click=lambda u=u: dar_cortesia(u, 7)).classes('btn-acao btn-cortesia')
                            ui.button('🎁 30 dias', on_click=lambda u=u: dar_cortesia(u, 30)).classes('btn-acao btn-cortesia')
                        else:
                            ui.button('❌ Remover', on_click=lambda u=u: remover_premium(u)).classes('btn-acao btn-remover')
                            ui.button('🎁 +30 dias', on_click=lambda u=u: dar_cortesia(u, 30)).classes('btn-acao btn-cortesia')
        
        # ============================================================
        # PAGAMENTOS
        # ============================================================
        with ui.element('div').classes('section-card'):
            with ui.element('div').classes('section-header'):
                with ui.row().classes('items-center justify-between w-full'):
                    ui.label("💰 Histórico de Pagamentos")
                    ui.label(f"{len(pagamentos)} registros").classes('text-sm text-gray-400')
            
            if not pagamentos:
                with ui.element('div').classes('empty-state'):
                    ui.icon('receipt_long').classes('text-4xl mb-2')
                    ui.label("Nenhum pagamento registrado")
            
            for p in reversed(pagamentos[-20:]):
                cor_status = '#10b981' if p.get('status') == 'confirmado' else '#f59e0b'
                try:
                    data_pag = datetime.fromisoformat(p.get('data', '')).strftime('%d/%m/%Y %H:%M')
                except:
                    data_pag = 'N/A'
                
                with ui.element('div').classes('pagamento-row'):
                    with ui.row().classes('items-center gap-3'):
                        ui.label(p.get('email', '-')).style('font-size:13px;font-weight:500;')
                        ui.label(p.get('metodo', '-').upper()).style('font-size:11px;color:#64748b;background:#f1f5f9;padding:2px 8px;border-radius:4px;')
                    
                    with ui.row().classes('items-center gap-3'):
                        ui.label(f"R$ {p.get('valor', 0):,.2f}").style('font-size:13px;font-weight:600;')
                        ui.label(p.get('status', '-').upper()).classes('badge-plano').style(f'background:{cor_status}20;color:{cor_status};')
                        ui.label(data_pag).style('font-size:11px;color:#94a3b8;')
        
        # ============================================================
        # CONFIGURAÇÕES
        # ============================================================
        with ui.element('div').classes('section-card'):
            with ui.element('div').classes('section-header'):
                ui.label("⚙️ Configurações do Admin")
            
            with ui.element('div').classes('config-section'):
                ui.label("Alterar Senha do Painel").style('font-size:14px;font-weight:600;margin-bottom:12px;')
                
                with ui.row().classes('gap-3 items-end').style('flex-wrap:wrap;'):
                    nova_senha = ui.input("Nova Senha", password=True, password_toggle_button=True).props('outlined').style('flex:1;min-width:200px;')
                    confirmar_senha = ui.input("Confirmar Senha", password=True, password_toggle_button=True).props('outlined').style('flex:1;min-width:200px;')
                    
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
                    
                    ui.button("Salvar Senha", on_click=salvar_nova_senha).style(
                        'background:#8b5cf6;color:white;border-radius:8px;padding:12px 20px;font-weight:600;'
                    )
    
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
        ui.timer(0.5, lambda: ui.navigate.to('/admin/painel'), once=True)
    
    def remover_premium(usuario):
        try:
            atualizar_plano_usuario(usuario['email'], 'gratuito')
            ui.notify(f"⬇ Premium removido de {usuario['nome']}", type="warning")
        except Exception as e:
            ui.notify(f"❌ Erro: {str(e)}", type="negative")
        ui.timer(0.5, lambda: ui.navigate.to('/admin/painel'), once=True)
    
    def dar_cortesia(usuario, dias):
        try:
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
        except Exception as e:
            ui.notify(f"❌ Erro: {str(e)}", type="negative")
        ui.timer(0.5, lambda: ui.navigate.to('/admin/painel'), once=True)


# ============================================================
# INICIALIZAR
# ============================================================
inicializar_admin()