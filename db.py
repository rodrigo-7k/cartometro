"""
Database - PostgreSQL para Render
"""
import os
import hashlib
import json
from datetime import datetime, timedelta

# Tentar importar psycopg2
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    POSTGRES = True
except ImportError:
    POSTGRES = False
    print("⚠️ psycopg2 não instalado, usando JSON local")

# ============================================================
# CONFIGURAÇÃO
# ============================================================
DATABASE_URL = os.environ.get('DATABASE_URL', '')

CATEGORIAS_PADRAO = [
    {"nome": "Alimentação", "icone": "restaurant", "cor": "#ef4444"},
    {"nome": "Transporte", "icone": "directions_car", "cor": "#f97316"},
    {"nome": "Moradia", "icone": "home", "cor": "#8b5cf6"},
    {"nome": "Saúde", "icone": "local_hospital", "cor": "#10b981"},
    {"nome": "Educação", "icone": "school", "cor": "#3b82f6"},
    {"nome": "Lazer", "icone": "sports_esports", "cor": "#ec4899"},
    {"nome": "Assinaturas", "icone": "subscriptions", "cor": "#6366f1"},
    {"nome": "Compras", "icone": "shopping_cart", "cor": "#14b8a6"},
    {"nome": "Outros", "icone": "category", "cor": "#6b7280"},
]

PLANOS = {
    "demo": {"nome": "Demonstração", "modo_individual": True, "max_lancamentos_mes": 999, "max_cartoes": 999, "consultor_premium": True, "duracao_dias": None},
    "gratuito": {"nome": "Gratuito", "modo_individual": False, "max_lancamentos_mes": 20, "max_cartoes": 1, "consultor_premium": False, "duracao_dias": None},
    "premium": {"nome": "Premium", "modo_individual": True, "max_lancamentos_mes": 9999, "max_cartoes": 9999, "consultor_premium": True, "duracao_dias": 365},
}

# ============================================================
# CONEXÃO POSTGRES
# ============================================================
def get_conn():
    """Retorna conexão com o banco"""
    if not POSTGRES or not DATABASE_URL:
        return None
    try:
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        print(f"Erro conexão DB: {e}")
        return None


def init_db():
    """Cria tabelas se não existirem"""
    if not POSTGRES or not DATABASE_URL:
        return
    
    conn = get_conn()
    if not conn:
        return
    
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                email TEXT PRIMARY KEY,
                nome TEXT NOT NULL,
                senha TEXT NOT NULL,
                plano TEXT DEFAULT 'gratuito',
                ativo BOOLEAN DEFAULT TRUE,
                avatar_emoji TEXT DEFAULT '👤',
                data_criacao TIMESTAMP DEFAULT NOW(),
                data_expiracao TIMESTAMP
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS dados_usuario (
                email TEXT PRIMARY KEY REFERENCES usuarios(email),
                dados JSONB DEFAULT '{}'
            )
        """)
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pagamentos (
                id SERIAL PRIMARY KEY,
                email TEXT,
                metodo TEXT,
                valor NUMERIC(10,2),
                status TEXT DEFAULT 'confirmado',
                admin TEXT,
                data TIMESTAMP DEFAULT NOW()
            )
        """)
        
        # Criar admin demo se não existir
        cur.execute("SELECT email FROM usuarios WHERE email = 'admin'")
        if not cur.fetchone():
            cur.execute(
                "INSERT INTO usuarios (email, nome, senha, plano, avatar_emoji) VALUES (%s, %s, %s, %s, %s)",
                ('admin', 'Admin Demo', hash_senha('admin'), 'demo', '👑')
            )
            cur.execute(
                "INSERT INTO dados_usuario (email, dados) VALUES (%s, %s)",
                ('admin', json.dumps(criar_dados_iniciais('Admin Demo')))
            )
        
        conn.commit()
        print("✅ Banco PostgreSQL inicializado!")
    except Exception as e:
        print(f"Erro init DB: {e}")
        conn.rollback()
    finally:
        conn.close()


# ============================================================
# MODO LOCAL (FALLBACK)
# ============================================================
import os as _os
DADOS_DIR = 'data'
USUARIOS_FILE = 'usuarios.json'

def _init_local():
    if not _os.path.exists(DADOS_DIR):
        _os.makedirs(DADOS_DIR)
    if not _os.path.exists(USUARIOS_FILE):
        usuarios = [{"id": "admin", "nome": "Admin Demo", "email": "admin", "senha": hash_senha("admin"), "plano": "demo", "ativo": True, "avatar_emoji": "👑", "data_criacao": datetime.now().isoformat(), "data_expiracao": None}]
        _salvar_json(USUARIOS_FILE, usuarios)
        dados = criar_dados_iniciais("Admin Demo")
        dados["perfil"]["avatar_emoji"] = "👑"
        _salvar_json(f'{DADOS_DIR}/admin.json', dados)

def _carregar_json(arquivo):
    try:
        if _os.path.exists(arquivo):
            with open(arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
    except: pass
    return None

def _salvar_json(arquivo, dados):
    try:
        _os.makedirs(_os.path.dirname(arquivo), exist_ok=True)
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        return True
    except: return False

# ============================================================
# FUNÇÕES UNIFICADAS
# ============================================================
def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def criar_dados_iniciais(nome="Usuário"):
    return {
        "config": {"limite_total": 3000, "limite_parcelado": 1500, "dia_fechamento": 10, "modo_cartao": "Unificado", "cor_primaria": "#3b82f6", "cor_escura": "#1e40af"},
        "gastos": [], "fixos": [], "cartoes": [], "categorias": CATEGORIAS_PADRAO,
        "perfil": {"nome": nome, "avatar_emoji": "👤"}
    }

def carregar_json(arquivo):
    if POSTGRES and DATABASE_URL:
        return None  # PostgreSQL não usa arquivos
    return _carregar_json(arquivo)

def salvar_json(arquivo, dados):
    if POSTGRES and DATABASE_URL:
        return True  # PostgreSQL gerencia
    return _salvar_json(arquivo, dados)

# ============================================================
# USUÁRIOS (UNIFICADO)
# ============================================================
def carregar_usuarios():
    if POSTGRES and DATABASE_URL:
        conn = get_conn()
        if conn:
            try:
                cur = conn.cursor(cursor_factory=RealDictCursor)
                cur.execute("SELECT * FROM usuarios ORDER BY data_criacao DESC")
                return [dict(r) for r in cur.fetchall()]
            except: pass
            finally: conn.close()
    return _carregar_json(USUARIOS_FILE) or []

def salvar_usuarios(usuarios):
    if POSTGRES and DATABASE_URL:
        return True
    return _salvar_json(USUARIOS_FILE, usuarios)

def buscar_usuario_por_email(email):
    if POSTGRES and DATABASE_URL:
        conn = get_conn()
        if conn:
            try:
                cur = conn.cursor(cursor_factory=RealDictCursor)
                cur.execute("SELECT * FROM usuarios WHERE LOWER(email) = LOWER(%s)", (email,))
                r = cur.fetchone()
                return dict(r) if r else None
            except: pass
            finally: conn.close()
    usuarios = _carregar_json(USUARIOS_FILE) or []
    for u in usuarios:
        if u.get('email', '').lower() == email.lower():
            return u
    return None

def autenticar_usuario(email, senha):
    usuario = buscar_usuario_por_email(email)
    if not usuario or not usuario.get('ativo', True): return None
    if usuario.get('senha') != hash_senha(senha): return None
    if usuario.get('data_expiracao'):
        try:
            exp = usuario['data_expiracao']
            if isinstance(exp, str): exp = datetime.fromisoformat(exp)
            if exp < datetime.now():
                if POSTGRES and DATABASE_URL:
                    conn = get_conn()
                    if conn:
                        try:
                            cur = conn.cursor()
                            cur.execute("UPDATE usuarios SET plano = 'gratuito', data_expiracao = NULL WHERE email = %s", (email,))
                            conn.commit()
                        except: conn.rollback()
                        finally: conn.close()
                usuario['plano'] = 'gratuito'
                usuario['data_expiracao'] = None
        except: pass
    return usuario

def criar_usuario(nome, email, senha, plano="gratuito"):
    if not nome or len(nome.strip()) < 2: return False, "Nome inválido", None
    if not email or '@' not in email: return False, "Email inválido", None
    if not senha or len(senha) < 4: return False, "Senha deve ter pelo menos 4 caracteres", None
    
    if buscar_usuario_por_email(email):
        return False, "Este email já está cadastrado", None
    
    plano_info = PLANOS.get(plano, PLANOS['gratuito'])
    data_expiracao = None
    if plano_info.get('duracao_dias'):
        data_expiracao = (datetime.now() + timedelta(days=plano_info['duracao_dias'])).isoformat()
    
    if POSTGRES and DATABASE_URL:
        conn = get_conn()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO usuarios (email, nome, senha, plano, data_expiracao) VALUES (%s, %s, %s, %s, %s)",
                    (email.lower().strip(), nome.strip(), hash_senha(senha), plano, data_expiracao)
                )
                cur.execute(
                    "INSERT INTO dados_usuario (email, dados) VALUES (%s, %s)",
                    (email.lower().strip(), json.dumps(criar_dados_iniciais(nome.strip())))
                )
                conn.commit()
                return True, "Conta criada com sucesso!", {"email": email, "nome": nome, "plano": plano}
            except Exception as e:
                conn.rollback()
                return False, f"Erro: {str(e)}", None
            finally: conn.close()
    
    # Fallback local
    usuarios = _carregar_json(USUARIOS_FILE) or []
    usuarios.append({"id": email.lower(), "nome": nome.strip(), "email": email.lower().strip(), "senha": hash_senha(senha), "plano": plano, "ativo": True, "avatar_emoji": "👤", "data_criacao": datetime.now().isoformat(), "data_expiracao": data_expiracao})
    _salvar_json(USUARIOS_FILE, usuarios)
    _salvar_json(f'{DADOS_DIR}/{email.lower().replace("@","_").replace(".","_")}.json', criar_dados_iniciais(nome.strip()))
    return True, "Conta criada com sucesso!", {"email": email, "nome": nome, "plano": plano}

def atualizar_plano_usuario(email, novo_plano):
    plano_info = PLANOS.get(novo_plano, PLANOS['gratuito'])
    data_expiracao = None
    if plano_info.get('duracao_dias'):
        data_expiracao = (datetime.now() + timedelta(days=plano_info['duracao_dias'])).isoformat()
    
    if POSTGRES and DATABASE_URL:
        conn = get_conn()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute("UPDATE usuarios SET plano = %s, data_expiracao = %s, ativo = TRUE WHERE LOWER(email) = LOWER(%s)", (novo_plano, data_expiracao, email))
                conn.commit()
                return True
            except: conn.rollback()
            finally: conn.close()
    
    usuarios = _carregar_json(USUARIOS_FILE) or []
    for u in usuarios:
        if u['email'].lower() == email.lower():
            u['plano'] = novo_plano
            u['data_expiracao'] = data_expiracao
            u['ativo'] = True
            break
    _salvar_json(USUARIOS_FILE, usuarios)
    return True

def atualizar_perfil_usuario(email, nome=None, avatar_emoji=None, senha=None):
    if POSTGRES and DATABASE_URL:
        conn = get_conn()
        if conn:
            try:
                cur = conn.cursor()
                if nome: cur.execute("UPDATE usuarios SET nome = %s WHERE LOWER(email) = LOWER(%s)", (nome, email))
                if avatar_emoji: cur.execute("UPDATE usuarios SET avatar_emoji = %s WHERE LOWER(email) = LOWER(%s)", (avatar_emoji, email))
                if senha: cur.execute("UPDATE usuarios SET senha = %s WHERE LOWER(email) = LOWER(%s)", (hash_senha(senha), email))
                conn.commit()
                return True
            except: conn.rollback()
            finally: conn.close()
    
    usuarios = _carregar_json(USUARIOS_FILE) or []
    for u in usuarios:
        if u['email'].lower() == email.lower():
            if nome: u['nome'] = nome
            if avatar_emoji: u['avatar_emoji'] = avatar_emoji
            if senha: u['senha'] = hash_senha(senha)
            break
    _salvar_json(USUARIOS_FILE, usuarios)
    return True

# ============================================================
# DADOS DO USUÁRIO
# ============================================================
def carregar_dados_usuario(email):
    if POSTGRES and DATABASE_URL:
        conn = get_conn()
        if conn:
            try:
                cur = conn.cursor(cursor_factory=RealDictCursor)
                cur.execute("SELECT dados FROM dados_usuario WHERE LOWER(email) = LOWER(%s)", (email,))
                r = cur.fetchone()
                if r and r['dados']:
                    return r['dados'] if isinstance(r['dados'], dict) else json.loads(r['dados'])
            except: pass
            finally: conn.close()
    
    dados = _carregar_json(f'{DADOS_DIR}/{email.lower().replace("@","_").replace(".","_")}.json')
    return dados if dados else criar_dados_iniciais()

def salvar_dados_usuario(email, dados):
    if POSTGRES and DATABASE_URL:
        conn = get_conn()
        if conn:
            try:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO dados_usuario (email, dados) VALUES (%s, %s) ON CONFLICT (email) DO UPDATE SET dados = %s",
                    (email.lower(), json.dumps(dados), json.dumps(dados))
                )
                conn.commit()
                return True
            except: conn.rollback()
            finally: conn.close()
    
    return _salvar_json(f'{DADOS_DIR}/{email.lower().replace("@","_").replace(".","_")}.json', dados)

def atualizar_config_usuario(email, **kwargs):
    dados = carregar_dados_usuario(email)
    if 'config' not in dados: dados['config'] = {}
    dados['config'].update(kwargs)
    return salvar_dados_usuario(email, dados)

# ============================================================
# LIMITES
# ============================================================
def get_plano_usuario(email):
    usuario = buscar_usuario_por_email(email)
    if not usuario: return PLANOS['gratuito']
    return PLANOS.get(usuario.get('plano', 'gratuito'), PLANOS['gratuito'])

def verificar_limite_lancamentos(email):
    plano = get_plano_usuario(email)
    max_lanc = plano['max_lancamentos_mes']
    if max_lanc >= 9999: return True, ""
    
    dados = carregar_dados_usuario(email)
    gastos = dados.get('gastos', [])
    hoje = datetime.now()
    count = sum(1 for g in gastos if g.get('data') and _mes_ano(g['data']) == (hoje.month, hoje.year))
    
    if count >= max_lanc:
        return False, f"⚠️ Limite de {max_lanc} lançamentos/mês atingido!"
    return True, f"{count}/{max_lanc} lançamentos este mês"

def verificar_limite_cartoes(email):
    plano = get_plano_usuario(email)
    max_cart = plano['max_cartoes']
    if max_cart >= 9999: return True, ""
    
    dados = carregar_dados_usuario(email)
    if len(dados.get('cartoes', [])) >= max_cart:
        return False, f"⚠️ Limite de {max_cart} cartão(ões)!"
    return True, ""

def pode_usar_modo_individual(email):
    return get_plano_usuario(email).get('modo_individual', False)

def tem_consultor_premium(email):
    return get_plano_usuario(email).get('consultor_premium', False)

def _mes_ano(data_str):
    try:
        dt = datetime.strptime(data_str, "%Y-%m-%d")
        return (dt.month, dt.year)
    except: return (0, 0)

# ============================================================
# COMPATIBILIDADE
# ============================================================
_usuario_logado_email = None

def set_usuario_logado(email):
    global _usuario_logado_email
    _usuario_logado_email = email

def get_usuario_logado_email():
    return _usuario_logado_email

def carregar():
    if _usuario_logado_email: return carregar_dados_usuario(_usuario_logado_email)
    return criar_dados_iniciais()

def salvar(dados):
    if _usuario_logado_email: salvar_dados_usuario(_usuario_logado_email, dados)

def atualizar_config(**kwargs):
    if _usuario_logado_email: atualizar_config_usuario(_usuario_logado_email, **kwargs)

def adicionar_gasto(descricao="", valor=0, tipo="À Vista", categoria="Outros", data=None, **kwargs):
    if not _usuario_logado_email: return
    dados = carregar()
    gasto = {"id": len(dados.get('gastos', [])) + 1, "descricao": descricao, "valor": float(valor), "tipo": tipo, "categoria": categoria, "data": data or datetime.now().strftime("%Y-%m-%d")}
    gasto.update(kwargs)
    dados.setdefault('gastos', []).append(gasto)
    salvar(dados)

def remover_gasto(gasto_id):
    if not _usuario_logado_email: return
    dados = carregar()
    dados['gastos'] = [g for g in dados.get('gastos', []) if g.get('id') != gasto_id]
    salvar(dados)

def adicionar_cartao(nome, limite_total=0, limite_parcelado=0, dia_fechamento=10):
    if not _usuario_logado_email: return
    dados = carregar()
    novo = {"id": len(dados.get('cartoes', [])) + 1, "nome": nome, "limite_total": float(limite_total or 0), "limite_parcelado": float(limite_parcelado or 0), "dia_fechamento": int(dia_fechamento or 10)}
    dados.setdefault('cartoes', []).append(novo)
    salvar(dados)

def remover_cartao(cartao_id):
    if not _usuario_logado_email: return
    dados = carregar()
    dados['cartoes'] = [c for c in dados.get('cartoes', []) if c.get('id') != cartao_id]
    salvar(dados)

def atualizar_cartao(cartao_id, **kwargs):
    if not _usuario_logado_email: return
    dados = carregar()
    for c in dados.get('cartoes', []):
        if c.get('id') == cartao_id: c.update(kwargs); break
    salvar(dados)

# ============================================================
# INICIALIZAR
# ============================================================
def inicializar():
    if POSTGRES and DATABASE_URL:
        init_db()
    else:
        _init_local()