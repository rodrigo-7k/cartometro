"""
Cartometro - Controle Inteligente do seu Crédito
Arquivo Principal - Inicialização
"""

from nicegui import ui
from db import inicializar, set_usuario_logado, carregar_usuarios, criar_usuario, resetar_dados_demo, hash_senha, salvar_usuarios
import admin
import config
import os
import sys

# ============================================================
# DETECÇÃO DE AMBIENTE
# ============================================================
IS_PRODUCTION = os.environ.get('RENDER', False) or os.environ.get('PRODUCTION', False)
IS_DEVELOPMENT = not IS_PRODUCTION

print(f"🌍 Ambiente: {'PRODUÇÃO' if IS_PRODUCTION else 'DESENVOLVIMENTO'}")

# ============================================================
# CRIAÇÃO DE USUÁRIOS PADRÃO
# ============================================================
def criar_usuarios_padrao():
    """Cria usuários padrão se não existirem"""
    usuarios = carregar_usuarios()
    emails_existentes = [u.get('email', '').strip().lower() for u in usuarios]
    
    print(f"📊 Usuários existentes: {len(usuarios)} - {emails_existentes}")
    
    # Lista de usuários para criar
    usuarios_para_criar = [
        ("Usuário Demo", "demo", "demo", "premium"),
        ("Admin App", "admin@app.com", "admin123", "premium"),
    ]
    
    if IS_DEVELOPMENT:
        usuarios_para_criar.append(("Teste Local", "teste@local.com", "teste123", "premium"))
    
    for nome, email, senha, plano in usuarios_para_criar:
        if email not in emails_existentes:
            print(f"👤 Criando: {email}...")
            sucesso, msg, usuario = criar_usuario(nome, email, senha, plano)
            if sucesso:
                print(f"✅ {email} criado!")
                if email == 'demo':
                    resetar_dados_demo('demo')
            else:
                print(f"❌ Erro ao criar {email}: {msg}")
                # Tentar criar diretamente
                print(f"🔧 Tentando criar {email} diretamente...")
                usuarios = carregar_usuarios()
                usuarios.append({
                    "nome": nome,
                    "email": email,
                    "senha": hash_senha(senha),
                    "plano": plano,
                    "ativo": True,
                    "data_criacao": "2025-01-01T00:00:00",
                    "avatar_emoji": "👤",
                    "config": {"cor_primaria": "#2563eb", "cor_escura": "#1d4ed8", "tema": "light", "modo_unificado": True}
                })
                salvar_usuarios(usuarios)
                print(f"✅ {email} criado diretamente!")
        else:
            print(f"👤 {email} já existe")

# ============================================================
# INICIALIZAÇÃO
# ============================================================
inicializar()
admin.inicializar_admin()
criar_usuarios_padrao()
set_usuario_logado(None)

# Importa as páginas
import landing
import login
import cadastro
import app_page

PORT = int(os.environ.get('PORT', 8080))

if IS_PRODUCTION:
    print(f"🚀 PRODUÇÃO na porta {PORT}")
    ui.run(
        title="Cartometro",
        favicon=config.FAVICON,
        reload=False,
        show=False,
        host='0.0.0.0',
        port=PORT,
        storage_secret='cartometro-2024-secret'
    )
else:
    print(f"💻 DEV na porta {PORT}")
    print("👑 demo / demo")
    print("🔐 admin@app.com / admin123")
    print("🧪 teste@local.com / teste123")
    ui.run(
        title="Cartometro [DEV]",
        favicon=config.FAVICON,
        reload=True,
        show=True,
        host='127.0.0.1',
        port=PORT,
        storage_secret='cartometro-2024-secret'
    )