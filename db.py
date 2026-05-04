"""
Database - Persistência Individual por Usuário
Cartometro - Controle Inteligente do seu Crédito
"""
import json
import os
import hashlib
from datetime import datetime, timedelta

# ============================================================
# CONFIGURAÇÃO
# ============================================================
DADOS_DIR = 'data'
USUARIOS_FILE = 'usuarios.json'

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
    "demo": {
        "nome": "Demonstração",
        "modo_individual": False,
        "max_lancamentos_mes": 3,
        "max_cartoes": 1,
        "consultor_premium": False,
        "duracao_dias": None
    },
    "gratuito": {
        "nome": "Gratuito",
        "modo_individual": False,
        "max_lancamentos_mes": 20,
        "max_cartoes": 1,
        "consultor_premium": False,
        "duracao_dias": None
    },
    "premium": {
        "nome": "Premium",
        "modo_individual": True,
        "max_lancamentos_mes": 9999,
        "max_cartoes": 9999,
        "consultor_premium": True,
        "duracao_dias": 365
    },
}


# ============================================================
# INICIALIZAÇÃO
# ============================================================
def inicializar():
    """Cria estrutura inicial de diretórios e arquivos"""
    if not os.path.exists(DADOS_DIR):
        os.makedirs(DADOS_DIR)
    
    if not os.path.exists(USUARIOS_FILE):
        usuarios = [
            {
                "id": "demo",
                "nome": "Demo",
                "email": "demo",
                "senha": hash_senha("admin"),
                "plano": "demo",
                "ativo": True,
                "avatar_emoji": "👑",
                "data_criacao": datetime.now().isoformat(),
                "data_expiracao": None
            }
        ]
        salvar_json(USUARIOS_FILE, usuarios)
        
        dados_demo = criar_dados_iniciais("Demo")
        dados_demo["perfil"]["avatar_emoji"] = "👑"
        salvar_json(f'{DADOS_DIR}/demo.json', dados_demo)


# ============================================================
# UTILITÁRIOS
# ============================================================
def hash_senha(senha):
    """Gera hash SHA-256 da senha"""
    return hashlib.sha256(senha.encode()).hexdigest()


def carregar_json(arquivo):
    """Carrega arquivo JSON com segurança"""
    try:
        if os.path.exists(arquivo):
            with open(arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar {arquivo}: {e}")
    return None


def salvar_json(arquivo, dados):
    """Salva arquivo JSON com segurança"""
    try:
        os.makedirs(os.path.dirname(arquivo), exist_ok=True)
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"Erro ao salvar {arquivo}: {e}")
        return False


def get_arquivo_usuario(email):
    """Retorna o caminho do arquivo de dados do usuário"""
    nome_arquivo = email.replace('@', '_').replace('.', '_').lower()
    return f'{DADOS_DIR}/{nome_arquivo}.json'


def criar_dados_iniciais(nome="Usuário"):
    """Cria estrutura de dados inicial para novo usuário"""
    return {
        "config": {
            "limite_total": 3000,
            "limite_parcelado": 1500,
            "dia_fechamento": 10,
            "modo_cartao": "Unificado",
            "cor_primaria": "#3b82f6",
            "cor_escura": "#1e40af"
        },
        "gastos": [],
        "fixos": [],
        "cartoes": [],
        "categorias": CATEGORIAS_PADRAO,
        "perfil": {
            "nome": nome,
            "avatar_emoji": "👤"
        }
    }


# ============================================================
# USUÁRIOS (CADASTRO)
# ============================================================
def carregar_usuarios():
    """Carrega lista de todos os usuários cadastrados"""
    return carregar_json(USUARIOS_FILE) or []


def salvar_usuarios(usuarios):
    """Salva lista de usuários"""
    return salvar_json(USUARIOS_FILE, usuarios)


def buscar_usuario_por_email(email):
    """Busca um usuário pelo email"""
    if not email:
        return None
    usuarios = carregar_usuarios()
    for u in usuarios:
        if u.get('email', '').lower() == email.lower():
            return u
    return None


def autenticar_usuario(email, senha):
    """Autentica usuário por email e senha"""
    usuario = buscar_usuario_por_email(email)
    
    if not usuario:
        return None
    
    if not usuario.get('ativo', True):
        return None
    
    if usuario.get('senha') != hash_senha(senha):
        return None
    
    # Verificar expiração do plano premium
    if usuario.get('data_expiracao'):
        try:
            if datetime.fromisoformat(usuario['data_expiracao']) < datetime.now():
                usuario['plano'] = 'gratuito'
                usuario['data_expiracao'] = None
                salvar_usuarios(carregar_usuarios())
        except:
            pass
    
    return usuario


def criar_usuario(nome, email, senha, plano="gratuito"):
    """Cria um novo usuário"""
    if not nome or len(nome.strip()) < 2:
        return False, "Nome deve ter pelo menos 2 caracteres", None
    
    if not email or '@' not in email:
        return False, "Email inválido", None
    
    if not senha or len(senha) < 4:
        return False, "Senha deve ter pelo menos 4 caracteres", None
    
    usuarios = carregar_usuarios()
    if buscar_usuario_por_email(email):
        return False, "Este email já está cadastrado", None
    
    plano_info = PLANOS.get(plano, PLANOS['gratuito'])
    data_expiracao = None
    if plano_info.get('duracao_dias'):
        data_expiracao = (datetime.now() + timedelta(days=plano_info['duracao_dias'])).isoformat()
    
    novo_usuario = {
        "id": email.lower(),
        "nome": nome.strip(),
        "email": email.lower().strip(),
        "senha": hash_senha(senha),
        "plano": plano,
        "ativo": True,
        "avatar_emoji": "👤",
        "data_criacao": datetime.now().isoformat(),
        "data_expiracao": data_expiracao
    }
    
    usuarios.append(novo_usuario)
    
    if not salvar_usuarios(usuarios):
        return False, "Erro ao salvar usuário", None
    
    dados = criar_dados_iniciais(nome.strip())
    if not salvar_json(get_arquivo_usuario(email), dados):
        return False, "Erro ao criar dados do usuário", None
    
    return True, "Conta criada com sucesso!", novo_usuario


def atualizar_plano_usuario(email, novo_plano):
    """Atualiza o plano de um usuário"""
    usuarios = carregar_usuarios()
    for u in usuarios:
        if u['email'].lower() == email.lower():
            u['plano'] = novo_plano
            plano_info = PLANOS.get(novo_plano, PLANOS['gratuito'])
            
            if plano_info.get('duracao_dias'):
                u['data_expiracao'] = (datetime.now() + timedelta(days=plano_info['duracao_dias'])).isoformat()
            else:
                u['data_expiracao'] = None
            
            u['ativo'] = True
            salvar_usuarios(usuarios)
            return True
    return False


def atualizar_perfil_usuario(email, nome=None, avatar_emoji=None, senha=None):
    """Atualiza dados do perfil do usuário"""
    usuarios = carregar_usuarios()
    for u in usuarios:
        if u['email'].lower() == email.lower():
            if nome:
                u['nome'] = nome.strip()
            if avatar_emoji:
                u['avatar_emoji'] = avatar_emoji
            if senha:
                u['senha'] = hash_senha(senha)
            salvar_usuarios(usuarios)
            
            dados = carregar_dados_usuario(email)
            if dados:
                if 'perfil' not in dados:
                    dados['perfil'] = {}
                if nome:
                    dados['perfil']['nome'] = nome.strip()
                if avatar_emoji:
                    dados['perfil']['avatar_emoji'] = avatar_emoji
                salvar_dados_usuario(email, dados)
            
            return True
    return False


# ============================================================
# RESETAR DADOS DEMO
# ============================================================
def resetar_dados_demo(email):
    """Reseta os dados da conta demo"""
    if email == 'demo':
        dados = criar_dados_iniciais("Demo")
        dados["perfil"]["avatar_emoji"] = "👑"
        salvar_dados_usuario(email, dados)
        return True
    return False


# ============================================================
# LIMITES DO PLANO
# ============================================================
def get_plano_usuario(email):
    """Retorna informações do plano do usuário"""
    usuario = buscar_usuario_por_email(email)
    if not usuario:
        return PLANOS['gratuito']
    plano = usuario.get('plano', 'gratuito')
    return PLANOS.get(plano, PLANOS['gratuito'])


def verificar_limite_lancamentos(email):
    """Verifica se usuário pode adicionar mais lançamentos este mês"""
    plano = get_plano_usuario(email)
    max_lanc = plano['max_lancamentos_mes']
    
    if max_lanc >= 9999:
        return True, ""
    
    dados = carregar_dados_usuario(email)
    gastos = dados.get('gastos', [])
    
    hoje = datetime.now()
    lancamentos_mes = 0
    for g in gastos:
        if g.get('data'):
            try:
                dt = datetime.strptime(g['data'], "%Y-%m-%d")
                if dt.month == hoje.month and dt.year == hoje.year:
                    lancamentos_mes += 1
            except:
                pass
    
    if lancamentos_mes >= max_lanc:
        return False, f"⚠️ Limite de {max_lanc} lançamentos/mês atingido! Faça upgrade para Premium."
    
    return True, f"{lancamentos_mes}/{max_lanc} lançamentos este mês"


def verificar_limite_cartoes(email):
    """Verifica se usuário pode adicionar mais cartões"""
    plano = get_plano_usuario(email)
    max_cart = plano['max_cartoes']
    
    if max_cart >= 9999:
        return True, ""
    
    dados = carregar_dados_usuario(email)
    cartoes = dados.get('cartoes', [])
    
    if len(cartoes) >= max_cart:
        return False, f"⚠️ Limite de {max_cart} cartão(ões) atingido! Faça upgrade para Premium."
    
    return True, ""


def pode_usar_modo_individual(email):
    """Verifica se o plano permite modo Individual"""
    plano = get_plano_usuario(email)
    return plano.get('modo_individual', False)


def tem_consultor_premium(email):
    """Verifica se o plano tem consultor completo"""
    plano = get_plano_usuario(email)
    return plano.get('consultor_premium', False)


# ============================================================
# DADOS DO USUÁRIO
# ============================================================
def carregar_dados_usuario(email):
    """Carrega todos os dados de um usuário"""
    if not email:
        return criar_dados_iniciais()
    
    dados = carregar_json(get_arquivo_usuario(email))
    
    if not dados:
        usuario = buscar_usuario_por_email(email)
        nome = usuario.get('nome', 'Usuário') if usuario else 'Usuário'
        dados = criar_dados_iniciais(nome)
        salvar_json(get_arquivo_usuario(email), dados)
    
    return dados


def salvar_dados_usuario(email, dados):
    """Salva todos os dados de um usuário"""
    if not email:
        return False
    return salvar_json(get_arquivo_usuario(email), dados)


def atualizar_config_usuario(email, **kwargs):
    """Atualiza apenas as configurações do usuário"""
    dados = carregar_dados_usuario(email)
    if 'config' not in dados:
        dados['config'] = {}
    dados['config'].update(kwargs)
    return salvar_dados_usuario(email, dados)


# ============================================================
# COMPATIBILIDADE COM CÓDIGO EXISTENTE
# ============================================================
_usuario_logado_email = None


def set_usuario_logado(email):
    """Define o usuário logado atual"""
    global _usuario_logado_email
    _usuario_logado_email = email


def get_usuario_logado_email():
    """Retorna o email do usuário logado"""
    return _usuario_logado_email


def carregar():
    """Compatibilidade - carrega dados do usuário logado"""
    if _usuario_logado_email:
        return carregar_dados_usuario(_usuario_logado_email)
    return criar_dados_iniciais()


def salvar(dados):
    """Compatibilidade - salva dados do usuário logado"""
    if _usuario_logado_email:
        salvar_dados_usuario(_usuario_logado_email, dados)


def atualizar_config(**kwargs):
    """Compatibilidade - atualiza config do usuário logado"""
    if _usuario_logado_email:
        atualizar_config_usuario(_usuario_logado_email, **kwargs)


def adicionar_gasto(descricao="", valor=0, tipo="À Vista", categoria="Outros", data=None, **kwargs):
    """Adiciona um gasto para o usuário logado"""
    if not _usuario_logado_email:
        return
    
    dados = carregar_dados_usuario(_usuario_logado_email)
    if 'gastos' not in dados:
        dados['gastos'] = []
    
    novo_id = max([g.get('id', 0) for g in dados['gastos']], default=0) + 1
    
    gasto = {
        "id": novo_id,
        "descricao": descricao,
        "valor": float(valor),
        "tipo": tipo,
        "categoria": categoria,
        "data": data or datetime.now().strftime("%Y-%m-%d"),
        "data_criacao": datetime.now().isoformat()
    }
    gasto.update(kwargs)
    
    dados['gastos'].append(gasto)
    salvar_dados_usuario(_usuario_logado_email, dados)


def remover_gasto(gasto_id):
    """Remove um gasto do usuário logado"""
    if not _usuario_logado_email:
        return
    
    dados = carregar_dados_usuario(_usuario_logado_email)
    dados['gastos'] = [g for g in dados.get('gastos', []) if g.get('id') != gasto_id]
    salvar_dados_usuario(_usuario_logado_email, dados)


def adicionar_cartao(nome, limite_total=0, limite_parcelado=0, dia_fechamento=10):
    """Adiciona um cartão para o usuário logado"""
    if not _usuario_logado_email:
        return
    
    dados = carregar_dados_usuario(_usuario_logado_email)
    if 'cartoes' not in dados:
        dados['cartoes'] = []
    
    novo_id = max([c.get('id', 0) for c in dados['cartoes']], default=0) + 1
    
    dados['cartoes'].append({
        "id": novo_id,
        "nome": nome,
        "limite_total": float(limite_total or 0),
        "limite_parcelado": float(limite_parcelado or 0),
        "dia_fechamento": int(dia_fechamento or 10)
    })
    
    salvar_dados_usuario(_usuario_logado_email, dados)


def remover_cartao(cartao_id):
    """Remove um cartão do usuário logado"""
    if not _usuario_logado_email:
        return
    
    dados = carregar_dados_usuario(_usuario_logado_email)
    dados['cartoes'] = [c for c in dados.get('cartoes', []) if c.get('id') != cartao_id]
    salvar_dados_usuario(_usuario_logado_email, dados)


def atualizar_cartao(cartao_id, **kwargs):
    """Atualiza um cartão do usuário logado"""
    if not _usuario_logado_email:
        return
    
    dados = carregar_dados_usuario(_usuario_logado_email)
    for c in dados.get('cartoes', []):
        if c.get('id') == cartao_id:
            c.update(kwargs)
            break
    salvar_dados_usuario(_usuario_logado_email, dados)