"""
Consultor Financeiro Inteligente - Cartometro
Motor de regras para análise e recomendações financeiras
"""

from datetime import datetime, timedelta
from collections import defaultdict


# ============================================================
# MODELOS
# ============================================================
class Notification:
    """Notificação gerada por uma regra"""
    def __init__(self, id, titulo, descricao, categoria, prioridade, icone, cor, tempo="Agora"):
        self.id = id
        self.titulo = titulo
        self.descricao = descricao
        self.categoria = categoria
        self.prioridade = prioridade
        self.icone = icone
        self.cor = cor
        self.tempo = tempo
    
    def to_dict(self):
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "categoria": self.categoria,
            "prioridade": self.prioridade,
            "icone": self.icone,
            "cor": self.cor,
            "tempo": self.tempo
        }


class Context:
    """Contexto completo para avaliação das regras"""
    def __init__(self):
        self.total_gasto = 0
        self.total_mes_passado = 0
        self.percentual = 0
        self.restante = 0
        self.limite_total = 0
        self.limite_vista = 0
        self.limite_parcelado = 0
        self.total_gasto_vista = 0
        self.total_gasto_parcelado = 0
        self.total_fixos = 0
        self.gastos_por_categoria = {}
        self.categoria_mes_passado = {}
        self.dia_atual = 1
        self.dias_para_fechamento = 0
        self.dia_fechamento = 10
        self.gasto_diario = 0
        self.projecao = 0
        self.qtd_gastos = 0
        self.gastos_ultimos_3_dias = 0
        self.gastos_ultimos_7_dias = 0
        self.cartoes_uso = {}
        self.cartoes_sem_uso = []
        self.cartoes_detalhe = {}  # NOVO: detalhes por cartão
        self.modo_cartao = "Unificado"
        self.gastos_fim_semana = 0
        self.gastos_inicio_mes = 0
        self.gastos_fim_mes = 0


# ============================================================
# FUNÇÕES DE CICLO (ETAPA 2)
# ============================================================
def obter_periodo_ciclo(dia_fechamento):
    """Calcula início e fim do ciclo baseado no dia de fechamento"""
    hoje = datetime.now()
    
    if hoje.day > dia_fechamento:
        inicio = datetime(hoje.year, hoje.month, dia_fechamento + 1)
        if hoje.month == 12:
            fim = datetime(hoje.year + 1, 1, dia_fechamento)
        else:
            fim = datetime(hoje.year, hoje.month + 1, dia_fechamento)
    else:
        if hoje.month == 1:
            inicio = datetime(hoje.year - 1, 12, dia_fechamento + 1)
        else:
            inicio = datetime(hoje.year, hoje.month - 1, dia_fechamento + 1)
        fim = datetime(hoje.year, hoje.month, dia_fechamento)
    
    return inicio, fim


def filtrar_gastos_ciclo(gastos, inicio, fim, cartao=None):
    """Filtra gastos que estão dentro do período do ciclo"""
    filtrados = []
    
    for g in gastos:
        if not g.get("data"):
            continue
        
        try:
            data = datetime.strptime(g["data"], "%Y-%m-%d")
        except:
            continue
        
        if inicio <= data <= fim:
            if cartao:
                if g.get("cartao") == cartao:
                    filtrados.append(g)
            else:
                filtrados.append(g)
    
    return filtrados


# ============================================================
# BUILDER DO CONTEXTO (ETAPAS 1, 3, 4)
# ============================================================
def build_context(dados, gastos, fixos, cartoes=None, gastos_mes_passado=None):
    ctx = Context()
    hoje = datetime.now()
    config = dados.get("config", {})
    
    ctx.total_fixos = sum(f.get("valor", 0) for f in fixos)
    ctx.qtd_gastos = len(gastos)
    ctx.dia_atual = hoje.day
    ctx.dia_fechamento = config.get("dia_fechamento", 10)
    ctx.dias_para_fechamento = max(ctx.dia_fechamento - hoje.day, 0)
    ctx.modo_cartao = config.get("modo_cartao", "Unificado")
    
    # ══════════════════════════════════════════════
    # ETAPA 3: Processar cada cartão individualmente
    # ══════════════════════════════════════════════
    ctx.cartoes_detalhe = {}
    
    if cartoes and ctx.modo_cartao == "Individual":
        for cartao in cartoes:
            nome = cartao.get("nome", "")
            dia_fech = cartao.get("dia_fechamento", config.get("dia_fechamento", 10))
            
            inicio, fim = obter_periodo_ciclo(dia_fech)
            gastos_filtrados = filtrar_gastos_ciclo(gastos, inicio, fim, nome)
            
            vista = 0
            parcelado = 0
            
            for g in gastos_filtrados:
                # ETAPA 1.1: NÃO divide por parcelas, JSON já traz valor da parcela
                if g.get("tipo") == "Parcelado" or g.get("parcelas", 1) > 1:
                    parcelado += g.get("valor", 0)
                else:
                    vista += g.get("valor", 0)
            
            # ETAPA 1.2: Fixos entram no À Vista
            vista += ctx.total_fixos
            
            ctx.cartoes_detalhe[nome] = {
                "vista": vista,
                "parcelado": parcelado,
                "total": vista + parcelado,
                "limite_vista": cartao.get("limite_vista", 0) or 0,
                "limite_parcelado": cartao.get("limite_parcelado", 0) or 0,
                "limite_total": (cartao.get("limite_vista", 0) or 0) + (cartao.get("limite_parcelado", 0) or 0),
            }
        
        # ETAPA 4: Consolidação global
        ctx.total_gasto_vista = sum(c["vista"] for c in ctx.cartoes_detalhe.values())
        ctx.total_gasto_parcelado = sum(c["parcelado"] for c in ctx.cartoes_detalhe.values())
        ctx.total_gasto = ctx.total_gasto_vista + ctx.total_gasto_parcelado
        
        ctx.limite_vista = sum(c["limite_vista"] for c in ctx.cartoes_detalhe.values())
        ctx.limite_parcelado = sum(c["limite_parcelado"] for c in ctx.cartoes_detalhe.values())
        ctx.limite_total = ctx.limite_vista + ctx.limite_parcelado
        
        ctx.restante = ctx.limite_total - ctx.total_gasto
        ctx.percentual = (ctx.total_gasto / ctx.limite_total * 100) if ctx.limite_total else 0
        
        # Cartões sem uso
        ctx.cartoes_uso = {nome: c["total"] for nome, c in ctx.cartoes_detalhe.items()}
        ctx.cartoes_sem_uso = [nome for nome, c in ctx.cartoes_detalhe.items() if c["total"] == 0]
    else:
        # Modo Unificado
        ctx.limite_vista = config.get("limite_vista", config.get("limite_total", 3000))
        ctx.limite_parcelado = config.get("limite_parcelado", 1500)
        ctx.limite_total = ctx.limite_vista + ctx.limite_parcelado
        
        ctx.total_gasto_vista = 0
        ctx.total_gasto_parcelado = 0
        
        for g in gastos:
            if g.get("tipo") == "Parcelado" or g.get("parcelas", 1) > 1:
                ctx.total_gasto_parcelado += g.get("valor", 0)
            else:
                ctx.total_gasto_vista += g.get("valor", 0)
        
        ctx.total_gasto_vista += ctx.total_fixos
        ctx.total_gasto = ctx.total_gasto_vista + ctx.total_gasto_parcelado
        ctx.restante = ctx.limite_total - ctx.total_gasto
        ctx.percentual = (ctx.total_gasto / ctx.limite_total * 100) if ctx.limite_total else 0
    
    # Projeções
    ctx.gasto_diario = ctx.total_gasto / max(ctx.dia_atual, 1)
    ctx.projecao = ctx.total_gasto + (ctx.gasto_diario * ctx.dias_para_fechamento)
    
    # Categorias
    categorias = defaultdict(float)
    for g in gastos:
        categorias[g.get("categoria", "Outros")] += g.get("valor", 0)
    ctx.gastos_por_categoria = dict(categorias)
    
    if gastos_mes_passado:
        cat_passado = defaultdict(float)
        for g in gastos_mes_passado:
            cat_passado[g.get("categoria", "Outros")] += g.get("valor", 0)
        ctx.categoria_mes_passado = dict(cat_passado)
    
    # Últimos dias
    ctx.gastos_ultimos_3_dias = sum(
        g.get("valor", 0) for g in gastos
        if g.get("data") and (hoje - datetime.strptime(g["data"], "%Y-%m-%d")).days <= 3
    )
    ctx.gastos_ultimos_7_dias = sum(
        g.get("valor", 0) for g in gastos
        if g.get("data") and (hoje - datetime.strptime(g["data"], "%Y-%m-%d")).days <= 7
    )
    
    # Mês passado
    mes_passado = hoje.month - 1 if hoje.month > 1 else 12
    ano_passado = hoje.year if hoje.month > 1 else hoje.year - 1
    
    if gastos_mes_passado is not None:
        ctx.total_mes_passado = sum(g.get("valor", 0) for g in gastos_mes_passado)
    else:
        ctx.total_mes_passado = sum(
            g.get("valor", 0) for g in gastos
            if g.get("data")
            and datetime.strptime(g["data"], "%Y-%m-%d").month == mes_passado
            and datetime.strptime(g["data"], "%Y-%m-%d").year == ano_passado
        )
    
    # Fim de semana e início/fim do mês
    ctx.gastos_fim_semana = sum(
        g.get("valor", 0) for g in gastos
        if g.get("data") and datetime.strptime(g["data"], "%Y-%m-%d").weekday() >= 5
    )
    ctx.gastos_inicio_mes = sum(
        g.get("valor", 0) for g in gastos
        if g.get("data") and datetime.strptime(g["data"], "%Y-%m-%d").day <= 5
    )
    ctx.gastos_fim_mes = sum(
        g.get("valor", 0) for g in gastos
        if g.get("data") and datetime.strptime(g["data"], "%Y-%m-%d").day >= 25
    )
    
    return ctx


# ============================================================
# 🚨 REGRAS - CRÍTICO
# ============================================================
def r_limite_estourado(ctx):
    if ctx.restante < 0:
        return [Notification("crit1", "Limite Estourado!",
            f"Você ultrapassou seu limite em R$ {abs(ctx.restante):.2f}. Evite novas compras!",
            "🚨 CRÍTICO", 100, "⚠️", "#ef4444", "Agora")]
    return []

def r_percentual_95(ctx):
    if ctx.percentual >= 95:
        return [Notification("crit2", "Limite Quase Esgotado (95%+)",
            f"Restam apenas R$ {ctx.restante:.2f}. Cuidado!",
            "🚨 CRÍTICO", 95, "🔴", "#ef4444", "Urgente")]
    return []

def r_vista_excedido(ctx):
    if ctx.limite_vista > 0 and ctx.total_gasto_vista > ctx.limite_vista:
        return [Notification("crit2b", "Limite À Vista Excedido",
            f"À Vista: R$ {ctx.total_gasto_vista:.2f} de R$ {ctx.limite_vista:.2f}.",
            "🚨 CRÍTICO", 91, "💵", "#ef4444", "Urgente")]
    return []

def r_parcelado_excedido(ctx):
    if ctx.limite_parcelado > 0 and ctx.total_gasto_parcelado > ctx.limite_parcelado:
        return [Notification("crit3", "Limite Parcelado Excedido",
            f"Parcelas: R$ {ctx.total_gasto_parcelado:.2f} de R$ {ctx.limite_parcelado:.2f}.",
            "🚨 CRÍTICO", 90, "📦", "#f59e0b", "Urgente")]
    return []

def r_cartao_estourado(ctx):
    """ETAPA 5: Verifica se algum cartão individual estourou"""
    notificacoes = []
    for nome, c in ctx.cartoes_detalhe.items():
        if c["total"] > c["limite_total"] and c["limite_total"] > 0:
            excedeu = c["total"] - c["limite_total"]
            notificacoes.append(Notification(
                f"cart_est_{nome}",
                f"Cartão {nome} Estourou!",
                f"Excedeu em R$ {excedeu:.2f}. Limite: R$ {c['limite_total']:.2f}.",
                "🚨 CRÍTICO", 100, "💳", "#ef4444", "Agora"
            ))
    return notificacoes

def r_projecao_estouro(ctx):
    if ctx.projecao > ctx.limite_total and ctx.percentual < 95:
        return [Notification("crit4", "Projeção: Limite Será Estourado!",
            f"Neste ritmo, você gastará R$ {ctx.projecao:.2f}.",
            "🚨 CRÍTICO", 92, "🔮", "#ef4444", "Atenção")]
    return []

def r_restante_baixo(ctx):
    if 0 < ctx.restante < 100:
        return [Notification("crit5", "Saldo Muito Baixo!",
            f"Restam apenas R$ {ctx.restante:.2f}. Máximo cuidado!",
            "🚨 CRÍTICO", 85, "⚠️", "#ef4444", "Agora")]
    return []

# ============================================================
# ⚠️ REGRAS - ALERTA
# ============================================================
def r_percentual_80(ctx):
    if 80 <= ctx.percentual < 95:
        return [Notification("alt1", f"Limite em {ctx.percentual:.0f}%",
            f"Usado R$ {ctx.total_gasto:.2f} de R$ {ctx.limite_total:.2f}. Atenção!",
            "⚠️ ALERTA", 80, "🟡", "#f59e0b", "Atenção")]
    return []

def r_gasto_diario_alto(ctx):
    limite_diario = ctx.limite_total * 0.05
    if ctx.gasto_diario > limite_diario and ctx.dia_atual > 3:
        return [Notification("alt2", "Gasto Diário Elevado",
            f"Média de R$ {ctx.gasto_diario:.2f}/dia. Ritmo acelerado!",
            "⚠️ ALERTA", 70, "📈", "#f59e0b", "Observação")]
    return []

def r_categoria_cresceu(ctx):
    notificacoes = []
    if ctx.categoria_mes_passado and ctx.gastos_por_categoria:
        for cat, valor_atual in ctx.gastos_por_categoria.items():
            valor_passado = ctx.categoria_mes_passado.get(cat, 0)
            if valor_passado > 0 and valor_atual > valor_passado * 1.4:
                notificacoes.append(Notification(f"alt_cat_{cat}", f"Categoria '{cat}' Cresceu 40%+",
                    f"R$ {valor_atual:.2f} (era R$ {valor_passado:.2f})",
                    "⚠️ ALERTA", 65, "📊", "#f59e0b", "Alerta"))
    return notificacoes[:2]

def r_acima_media(ctx):
    if ctx.total_mes_passado > 0 and ctx.total_gasto > ctx.total_mes_passado * 1.3:
        return [Notification("alt3", "Acima da Média Histórica",
            f"Gasto {((ctx.total_gasto/ctx.total_mes_passado - 1) * 100):.0f}% maior que mês anterior.",
            "⚠️ ALERTA", 70, "📊", "#f59e0b", "Alerta")]
    return []

def r_pico_3dias(ctx):
    limite_3dias = ctx.limite_total * 0.2
    if ctx.gastos_ultimos_3_dias > limite_3dias:
        return [Notification("alt4", "Pico de Gastos Recente",
            f"R$ {ctx.gastos_ultimos_3_dias:.2f} em 3 dias. Desacelere!",
            "⚠️ ALERTA", 75, "🔥", "#f59e0b", "Urgente")]
    return []

# ============================================================
# 🧠 REGRAS - COMPORTAMENTO
# ============================================================
def r_fim_semana(ctx):
    hoje = datetime.now()
    if hoje.weekday() >= 5:
        return [Notification("comp1", "Fim de Semana - Atenção!",
            "Você costuma gastar mais no fim de semana. Planeje-se!",
            "🧠 COMPORTAMENTO", 40, "📅", "#10b981", "Dica")]
    if hoje.weekday() == 4:
        return [Notification("comp1b", "Sexta-feira - Planeje o FDS",
            "Fim de semana chegando. Cuidado com gastos extras!",
            "🧠 COMPORTAMENTO", 35, "📅", "#10b981", "Dica")]
    return []

def r_inicio_mes(ctx):
    if ctx.dia_atual <= 3:
        return [Notification("comp2", "Início do Mês - Planeje!",
            "Defina seu orçamento. Tente gastar menos que no mês passado.",
            "🧠 COMPORTAMENTO", 40, "📋", "#3b82f6", "Planejamento")]
    return []

def r_categoria_recorrente(ctx):
    return []

def r_compra_frequente(ctx):
    return []

def r_mudanca_padrao(ctx):
    return []

# ============================================================
# 📊 REGRAS - ANÁLISE
# ============================================================
def r_categoria_dominante(ctx):
    if not ctx.gastos_por_categoria or ctx.total_gasto == 0:
        return []
    maior_cat = max(ctx.gastos_por_categoria, key=ctx.gastos_por_categoria.get)
    maior_valor = ctx.gastos_por_categoria[maior_cat]
    percentual_cat = (maior_valor / ctx.total_gasto * 100) if ctx.total_gasto > 0 else 0
    if percentual_cat > 30:
        return [Notification("ana1", f"Categoria Dominante: '{maior_cat}'",
            f"Representa {percentual_cat:.0f}% dos gastos (R$ {maior_valor:.2f}).",
            "📊 ANÁLISE", 60, "📊", "#8b5cf6", "Análise")]
    return []

def r_pulverizado(ctx):
    if len(ctx.gastos_por_categoria) >= 5:
        return [Notification("ana2", "Gastos Pulverizados",
            f"{len(ctx.gastos_por_categoria)} categorias diferentes. Concentre compras para negociar.",
            "📊 ANÁLISE", 50, "🛒", "#6366f1", "Observação")]
    return []

def r_ticket_alto(ctx):
    if ctx.qtd_gastos > 0:
        ticket_medio = ctx.total_gasto / ctx.qtd_gastos
        if ticket_medio > 200:
            return [Notification("ana3", "Ticket Médio Alto",
                f"Média de R$ {ticket_medio:.2f} por compra.",
                "📊 ANÁLISE", 60, "💰", "#8b5cf6", "Análise")]
    return []

def r_poucos_gastos(ctx):
    if ctx.qtd_gastos <= 3 and ctx.total_gasto > 0:
        return [Notification("ana4", "Poucas Compras - Bom Sinal!",
            "Poucas compras mostram controle financeiro.",
            "📊 ANÁLISE", 40, "👍", "#10b981", "Elogio")]
    return []

def r_muitos_pequenos(ctx):
    if ctx.qtd_gastos > 15:
        return [Notification("ana5", "Muitos Pequenos Gastos",
            f"{ctx.qtd_gastos} compras. Cuidado com o 'efeito formiguinha'!",
            "📊 ANÁLISE", 55, "🧾", "#f59e0b", "Alerta")]
    return []

# ============================================================
# 🔮 REGRAS - PREVISÃO
# ============================================================
def r_projecao_sobra(ctx):
    if ctx.projecao < ctx.limite_total * 0.7 and ctx.percentual < 50:
        return [Notification("prev1", "Vai Sobrar Dinheiro!",
            f"Projeção: R$ {ctx.projecao:.2f}. Considere investir.",
            "🔮 PREVISÃO", 40, "💡", "#10b981", "Oportunidade")]
    return []

def r_ritmo_alto(ctx):
    ritmo_ideal = ctx.limite_total / 30
    if ctx.gasto_diario > ritmo_ideal * 1.5 and ctx.dia_atual > 5:
        return [Notification("prev2", "Ritmo Acima do Ideal",
            f"Gasto diário R$ {ctx.gasto_diario:.2f} (ideal: R$ {ritmo_ideal:.2f}).",
            "🔮 PREVISÃO", 80, "⚡", "#ef4444", "Atenção")]
    return []

def r_ritmo_baixo(ctx):
    ritmo_ideal = ctx.limite_total / 30
    if ctx.gasto_diario < ritmo_ideal * 0.5 and ctx.dia_atual > 5:
        return [Notification("prev3", "Ritmo Excelente!",
            f"Gasto diário R$ {ctx.gasto_diario:.2f} (média: R$ {ritmo_ideal:.2f}).",
            "🔮 PREVISÃO", 40, "🟢", "#10b981", "Parabéns")]
    return []

# ============================================================
# 💰 REGRAS - ECONOMIA
# ============================================================
def r_fixos_altos(ctx):
    if ctx.limite_total > 0 and ctx.total_fixos > ctx.limite_total * 0.25:
        return [Notification("eco1", "Gastos Fixos Elevados",
            f"R$ {ctx.total_fixos:.2f} ({ctx.total_fixos/ctx.limite_total*100:.0f}% do limite). Revise assinaturas.",
            "💰 ECONOMIA", 70, "🔁", "#8b5cf6", "Sugestão")]
    return []

def r_fixos_dominam(ctx):
    if ctx.total_gasto > 0 and ctx.total_fixos / ctx.total_gasto > 0.5:
        return [Notification("eco2", "Metade dos Gastos São Fixos",
            f"{(ctx.total_fixos/ctx.total_gasto*100):.0f}% são fixos. Reduza assinaturas.",
            "💰 ECONOMIA", 75, "⚖️", "#f59e0b", "Alerta")]
    return []

def r_economia_potencial(ctx):
    if ctx.gastos_por_categoria and ctx.total_gasto > 0:
        maior_cat = max(ctx.gastos_por_categoria, key=ctx.gastos_por_categoria.get)
        maior_valor = ctx.gastos_por_categoria[maior_cat]
        if maior_valor > ctx.total_gasto * 0.2:
            return [Notification("eco3", "Potencial de Economia",
                f"Reduza 10% em '{maior_cat}' e economize R$ {maior_valor*0.1:.2f}.",
                "💰 ECONOMIA", 60, "💡", "#10b981", "Sugestão")]
    return []

def r_corte_gastos(ctx):
    if ctx.percentual > 75:
        return [Notification("eco4", "Hora de Cortar Gastos",
            f"Você já usou {ctx.percentual:.0f}% do limite. Priorize o essencial.",
            "💰 ECONOMIA", 65, "✂️", "#ef4444", "Sugestão")]
    return []

# ============================================================
# 💳 REGRAS - CARTÕES
# ============================================================
def r_cartao_sem_uso(ctx):
    if ctx.cartoes_sem_uso:
        nomes = ", ".join(ctx.cartoes_sem_uso[:2])
        return [Notification("cart1", f"Cartão sem Uso: {nomes}",
            "Considere concentrar gastos em um cartão.",
            "💳 CARTÕES", 35, "💳", "#6366f1", "Dica")]
    return []

def r_cartao_muito_uso(ctx):
    if ctx.cartoes_uso and len(ctx.cartoes_uso) > 1:
        total_geral = sum(ctx.cartoes_uso.values())
        for nome, valor in ctx.cartoes_uso.items():
            if total_geral > 0 and valor / total_geral > 0.7:
                return [Notification(f"cart2_{nome}", f"Dependência do Cartão '{nome}'",
                    f"{(valor/total_geral*100):.0f}% dos gastos neste cartão.",
                    "💳 CARTÕES", 50, "💳", "#6366f1", "Observação")]
    return []

def r_dependencia_cartao(ctx):
    if ctx.cartoes_uso and len(ctx.cartoes_uso) >= 2:
        valores = list(ctx.cartoes_uso.values())
        total_geral = sum(valores)
        if total_geral > 0 and max(valores) / total_geral > 0.8:
            return [Notification("cart3", "Alta Dependência de Um Cartão",
                "Diversifique o uso para melhorar score.",
                "💳 CARTÕES", 45, "💳", "#8b5cf6", "Dica")]
    return []

# ============================================================
# 🎯 REGRAS - METAS
# ============================================================
def r_melhor_mes(ctx):
    if ctx.total_mes_passado > 0 and ctx.total_gasto < ctx.total_mes_passado:
        economia = ctx.total_mes_passado - ctx.total_gasto
        percentual = (economia / ctx.total_mes_passado * 100) if ctx.total_mes_passado > 0 else 0
        return [Notification("meta1", "Melhor que Mês Passado! 🏆",
            f"Você economizou R$ {economia:.2f} ({percentual:.0f}% a menos).",
            "🎯 METAS", 50, "🏆", "#10b981", "Parabéns")]
    return []

def r_pior_mes(ctx):
    if ctx.total_mes_passado > 0 and ctx.total_gasto > ctx.total_mes_passado * 1.2:
        aumento = ctx.total_gasto - ctx.total_mes_passado
        return [Notification("meta2", "Gastos Aumentaram 📉",
            f"R$ {aumento:.2f} a mais que mês passado.",
            "🎯 METAS", 70, "📉", "#ef4444", "Alerta")]
    return []

def r_dentro_meta(ctx):
    if ctx.percentual < 50 and ctx.total_gasto > 0:
        return [Notification("meta3", "Dentro da Meta! 🎯",
            f"Apenas {ctx.percentual:.0f}% do limite usado.",
            "🎯 METAS", 40, "🎯", "#10b981", "Parabéns")]
    return []

def r_fora_meta(ctx):
    if ctx.percentual > 80:
        return [Notification("meta4", "Fora da Meta 🚫",
            f"{ctx.percentual:.0f}% usado. Reduza para voltar ao controle.",
            "🎯 METAS", 80, "🚫", "#ef4444", "Atenção")]
    return []


# ============================================================
# CONFIGURAÇÃO DE PLANOS
# ============================================================
REGRAS_GRATUITO = [
    'r_limite_estourado',
    'r_percentual_95',
    'r_percentual_80',
    'r_projecao_estouro',
    'r_fixos_altos',
    'r_melhor_mes',
]

REGRAS_PREMIUM = [
    'r_limite_estourado', 'r_percentual_95', 'r_vista_excedido',
    'r_parcelado_excedido', 'r_cartao_estourado',
    'r_projecao_estouro', 'r_restante_baixo',
    'r_percentual_80', 'r_gasto_diario_alto', 'r_categoria_cresceu',
    'r_acima_media', 'r_pico_3dias',
    'r_fim_semana', 'r_inicio_mes', 'r_categoria_recorrente',
    'r_compra_frequente', 'r_mudanca_padrao',
    'r_categoria_dominante', 'r_pulverizado', 'r_ticket_alto',
    'r_poucos_gastos', 'r_muitos_pequenos',
    'r_projecao_sobra', 'r_ritmo_alto', 'r_ritmo_baixo',
    'r_fixos_altos', 'r_fixos_dominam', 'r_economia_potencial', 'r_corte_gastos',
    'r_cartao_sem_uso', 'r_cartao_muito_uso', 'r_dependencia_cartao',
    'r_melhor_mes', 'r_pior_mes', 'r_dentro_meta', 'r_fora_meta',
]

MAPA_REGRAS = {
    'r_limite_estourado': r_limite_estourado,
    'r_percentual_95': r_percentual_95,
    'r_vista_excedido': r_vista_excedido,
    'r_parcelado_excedido': r_parcelado_excedido,
    'r_cartao_estourado': r_cartao_estourado,
    'r_projecao_estouro': r_projecao_estouro,
    'r_restante_baixo': r_restante_baixo,
    'r_percentual_80': r_percentual_80,
    'r_gasto_diario_alto': r_gasto_diario_alto,
    'r_categoria_cresceu': r_categoria_cresceu,
    'r_acima_media': r_acima_media,
    'r_pico_3dias': r_pico_3dias,
    'r_fim_semana': r_fim_semana,
    'r_inicio_mes': r_inicio_mes,
    'r_categoria_recorrente': r_categoria_recorrente,
    'r_compra_frequente': r_compra_frequente,
    'r_mudanca_padrao': r_mudanca_padrao,
    'r_categoria_dominante': r_categoria_dominante,
    'r_pulverizado': r_pulverizado,
    'r_ticket_alto': r_ticket_alto,
    'r_poucos_gastos': r_poucos_gastos,
    'r_muitos_pequenos': r_muitos_pequenos,
    'r_projecao_sobra': r_projecao_sobra,
    'r_ritmo_alto': r_ritmo_alto,
    'r_ritmo_baixo': r_ritmo_baixo,
    'r_fixos_altos': r_fixos_altos,
    'r_fixos_dominam': r_fixos_dominam,
    'r_economia_potencial': r_economia_potencial,
    'r_corte_gastos': r_corte_gastos,
    'r_cartao_sem_uso': r_cartao_sem_uso,
    'r_cartao_muito_uso': r_cartao_muito_uso,
    'r_dependencia_cartao': r_dependencia_cartao,
    'r_melhor_mes': r_melhor_mes,
    'r_pior_mes': r_pior_mes,
    'r_dentro_meta': r_dentro_meta,
    'r_fora_meta': r_fora_meta,
}


# ============================================================
# MOTOR PRINCIPAL
# ============================================================
def gerar_notificacoes(dados, gastos, fixos, cartoes=None, gastos_mes_passado=None, plano="gratuito"):
    """
    Gera notificações com base no plano do usuário
    
    Args:
        dados: dicionário completo de dados
        gastos: lista de gastos do período
        fixos: lista de gastos fixos
        cartoes: lista de cartões (opcional)
        gastos_mes_passado: gastos do mês anterior (opcional)
        plano: "gratuito", "premium" ou "demo"
    
    Returns:
        list: lista de dicionários com notificações
    """
    ctx = build_context(dados, gastos, fixos, cartoes, gastos_mes_passado)
    
    # Seleciona regras baseado no plano
    if plano in ["premium", "demo"]:
        regras_ativas = REGRAS_PREMIUM
    else:
        regras_ativas = REGRAS_GRATUITO
    
    notificacoes = []
    for nome_regra in regras_ativas:
        try:
            funcao = MAPA_REGRAS.get(nome_regra)
            if funcao:
                resultado = funcao(ctx)
                notificacoes.extend(resultado)
        except Exception as e:
            print(f"Erro na regra {nome_regra}: {e}")
    
    # Dica de upgrade para gratuito
    if plano == "gratuito":
        notificacoes.append(Notification(
            "upgrade_dica",
            "🔓 Consultor Premium",
            "Desbloqueie 30+ alertas inteligentes com o plano Premium!",
            "💎 UPGRADE", 10, "⭐", "#8b5cf6", "Dica"
        ))
    
    notificacoes.sort(key=lambda n: n.prioridade, reverse=True)
    return [n.to_dict() for n in notificacoes]
