"""
Camada de acesso a dados - JSON file-based
"""

import json
import os
from datetime import datetime
from constantes import (
    ARQUIVO_DADOS,
    LIMITE_TOTAL_PADRAO,
    LIMITE_PARCELADO_PADRAO,
    DIA_FECHAMENTO_PADRAO,
    CATEGORIAS_PADRAO
)


def _existe_arquivo():
    """Verifica se o arquivo de dados existe"""
    return os.path.exists(ARQUIVO_DADOS)


def _criar_arquivo_inicial():
    """Cria o arquivo de dados com valores padrão"""
    dados = {
        "config": {
            "limite_total": LIMITE_TOTAL_PADRAO,
            "limite_parcelado": LIMITE_PARCELADO_PADRAO,
            "dia_fechamento": DIA_FECHAMENTO_PADRAO,
            "modo_cartao": "Unificado"
        },
        "gastos": [],
        "fixos": [],
        "cartoes": [],
        "categorias": CATEGORIAS_PADRAO
    }
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)
    return dados


def inicializar():
    """Cria o arquivo de dados se não existir"""
    if not _existe_arquivo():
        _criar_arquivo_inicial()


def carregar():
    """Carrega dados do arquivo JSON"""
    if not _existe_arquivo():
        return _criar_arquivo_inicial()
    
    with open(ARQUIVO_DADOS, "r", encoding="utf-8") as f:
        dados = json.load(f)
    
    # Garantir que categorias sempre existam
    if "categorias" not in dados or not dados["categorias"]:
        dados["categorias"] = CATEGORIAS_PADRAO
        _salvar_direto(dados)
    
    # Garantir que config existe
    if "config" not in dados:
        dados["config"] = {
            "limite_total": LIMITE_TOTAL_PADRAO,
            "limite_parcelado": LIMITE_PARCELADO_PADRAO,
            "dia_fechamento": DIA_FECHAMENTO_PADRAO,
            "modo_cartao": "Unificado"
        }
        _salvar_direto(dados)
    
    # Garantir que modo_cartao existe
    if "modo_cartao" not in dados["config"]:
        dados["config"]["modo_cartao"] = "Unificado"
        _salvar_direto(dados)
    
    # Garantir que gastos, fixos e cartoes existem
    if "gastos" not in dados:
        dados["gastos"] = []
    if "fixos" not in dados:
        dados["fixos"] = []
    if "cartoes" not in dados:
        dados["cartoes"] = []
    
    return dados


def _salvar_direto(dados):
    """Salva dados diretamente no arquivo (uso interno)"""
    with open(ARQUIVO_DADOS, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=2, ensure_ascii=False)


def salvar(dados):
    """Salva dados no arquivo JSON"""
    _salvar_direto(dados)


def gerar_id():
    """Gera ID único baseado em timestamp"""
    return str(datetime.now().timestamp())


# =========================
# GASTOS
# =========================
def adicionar_gasto(descricao, valor, tipo, parcelas=1, data=None, categoria=None, subcategoria=None, cartao=None):
    """
    Adiciona um novo gasto
    
    Args:
        descricao: Descrição do gasto
        valor: Valor total
        tipo: Tipo (À Vista, Parcelado, Fixo)
        parcelas: Número de parcelas (padrão 1)
        data: Data no formato YYYY-MM-DD (padrão hoje)
        categoria: Nome da categoria
        subcategoria: Nome da subcategoria (ignorado)
        cartao: Nome do cartão (modo individual)
    """
    dados = carregar()
    
    if data is None:
        data = datetime.now().strftime("%Y-%m-%d")
    
    if not categoria:
        categoria = "Outros"
    
    if tipo == "Fixo":
        gasto = {
            "id": gerar_id(),
            "descricao": descricao,
            "valor": float(valor),
            "tipo": tipo,
            "categoria": categoria,
            "cartao": cartao,
            "data_criacao": datetime.now().strftime("%Y-%m-%d")
        }
        dados["fixos"].append(gasto)
    else:
        valor_float = float(valor)
        
        if tipo == "Parcelado" and parcelas > 1:
            valor_parcela = round(valor_float / parcelas, 2)
            diferenca = round(valor_float - (valor_parcela * parcelas), 2)
            
            data_base = datetime.strptime(data, "%Y-%m-%d") if data else datetime.now()
            
            for i in range(parcelas):
                mes = data_base.month + i
                ano = data_base.year + (mes - 1) // 12
                mes = ((mes - 1) % 12) + 1
                
                try:
                    data_parcela = datetime(ano, mes, data_base.day)
                except ValueError:
                    import calendar
                    ultimo_dia = calendar.monthrange(ano, mes)[1]
                    dia = min(data_base.day, ultimo_dia)
                    data_parcela = datetime(ano, mes, dia)
                
                valor_final = valor_parcela + diferenca if i == parcelas - 1 else valor_parcela
                
                gasto = {
                    "id": gerar_id(),
                    "descricao": f"{descricao} ({i+1}/{parcelas})",
                    "descricao_base": descricao,
                    "valor": valor_final,
                    "valor_total": valor_float,
                    "tipo": tipo,
                    "parcelas": parcelas,
                    "parcela_atual": i + 1,
                    "data": data_parcela.strftime("%Y-%m-%d"),
                    "categoria": categoria,
                    "cartao": cartao
                }
                dados["gastos"].append(gasto)
        else:
            gasto = {
                "id": gerar_id(),
                "descricao": descricao,
                "valor": valor_float,
                "tipo": tipo,
                "parcelas": 1,
                "parcela_atual": 1,
                "data": data,
                "categoria": categoria,
                "cartao": cartao
            }
            dados["gastos"].append(gasto)
    
    salvar(dados)
    return True


def remover_gasto(gasto_id):
    """Remove um gasto pelo ID"""
    dados = carregar()
    dados["gastos"] = [g for g in dados["gastos"] if g.get("id") != gasto_id]
    dados["fixos"] = [g for g in dados["fixos"] if g.get("id") != gasto_id]
    salvar(dados)


def atualizar_gasto(gasto_id, **kwargs):
    """Atualiza campos de um gasto"""
    dados = carregar()
    
    for lista_nome in ["gastos", "fixos"]:
        for g in dados[lista_nome]:
            if g.get("id") == gasto_id:
                for key, value in kwargs.items():
                    if value is not None:
                        g[key] = value
                break
    
    salvar(dados)


# =========================
# CONFIGURAÇÕES
# =========================
def atualizar_config(limite_total=None, limite_parcelado=None, dia_fechamento=None, modo_cartao=None):
    """Atualiza configurações"""
    dados = carregar()
    
    if limite_total is not None:
        dados["config"]["limite_total"] = float(limite_total)
    if limite_parcelado is not None:
        dados["config"]["limite_parcelado"] = float(limite_parcelado)
    if dia_fechamento is not None:
        dados["config"]["dia_fechamento"] = int(dia_fechamento)
    if modo_cartao is not None:
        dados["config"]["modo_cartao"] = str(modo_cartao)
    
    salvar(dados)
    return dados["config"]


# =========================
# CATEGORIAS
# =========================
def adicionar_categoria(nome, icone="category", cor="#6b7280", subcategorias=None):
    """Adiciona nova categoria"""
    dados = carregar()
    
    categoria = {
        "nome": nome,
        "icone": icone,
        "cor": cor,
        "subcategorias": subcategorias or []
    }
    dados["categorias"].append(categoria)
    salvar(dados)
    return categoria


# =========================
# CARTÕES
# =========================
def adicionar_cartao(nome, limite_total, limite_parcelado=None, dia_fechamento=None):
    """Adiciona um novo cartão"""
    dados = carregar()
    
    if "cartoes" not in dados:
        dados["cartoes"] = []
    
    cartao = {
        "id": gerar_id(),
        "nome": nome,
        "limite_total": float(limite_total),
        "limite_parcelado": float(limite_parcelado) if limite_parcelado else float(limite_total),
        "dia_fechamento": int(dia_fechamento) if dia_fechamento else 10,
        "ativo": True
    }
    dados["cartoes"].append(cartao)
    salvar(dados)
    return cartao


def listar_cartoes():
    """Lista todos os cartões"""
    dados = carregar()
    return dados.get("cartoes", [])


def remover_cartao(cartao_id):
    """Remove um cartão"""
    dados = carregar()
    dados["cartoes"] = [c for c in dados.get("cartoes", []) if c.get("id") != cartao_id]
    salvar(dados)


def atualizar_cartao(cartao_id, **kwargs):
    """Atualiza dados de um cartão"""
    dados = carregar()
    for c in dados.get("cartoes", []):
        if c.get("id") == cartao_id:
            for key, value in kwargs.items():
                if value is not None:
                    c[key] = value
            break
    salvar(dados)