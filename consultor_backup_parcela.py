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
        self.total_gasto_vista = 0
        self.total_gasto_parcelado = 0
        self.total_fixos = 0
        self.total_mes_passado = 0
        self.percentual = 0
        self.restante = 0
        self.limite_total = 0
        self.limite_vista = 0
        self.limite_parcelado = 0
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
        self.cartoes_detalhe = {}
        self.modo_cartao = "Unificado"
        self.gastos_fim_semana = 0
        self.gastos_inicio_mes = 0
        self.gastos_fim_mes = 0


# ============================================================
# FUNÇÕES DE CICLO
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


# ============================================================
# BUILDER DO CONTEXTO
# ============================================================
def build_context(dados, gastos, fixos, cartoes=None, gastos_mes_passado=None):
    """Constrói contexto baseado nos cartões e seus ciclos individuais"""
    ctx = Context()
    hoje = datetime.now()
    config = dados.get("config", {})
    
    ctx.total_fixos = sum(f.get("valor", 0) for f in fixos)
    ctx.qtd_gastos = len(gastos)
    ctx.dia_atual = hoje.day
    ctx.dia_fechamento = config.get("dia_fechamento", 10)
    ctx.modo_cartao = config.get("modo_cartao", "Unificado")
    
    # ══════════════════════════════════════════════
    # Processar cada cartão no seu próprio ciclo
    # ══════════════════════════════════════════════
    ctx.cartoes_detalhe = {}
    
    if cartoes and ctx.modo_cartao == "Individual":
        for cartao in cartoes:
            nome = cartao.get("nome", "")
            dia_fech = cartao.get("dia_fechamento", 10)
            
            inicio, fim = obter_periodo_ciclo(dia_fech)
            
            vista = 0
            parcelado = 0
            
            for g in gastos:
                if g.get("cartao") != nome:
                    continue
                if not g.get("data"):
                    continue
                
                try:
                    data = datetime.strptime(g["data"], "%Y-%m-%d")
                except:
                    continue
                
                if not (inicio <= data <= fim):
                    continue
                
                if data > hoje:
                    continue
                
                # JSON já traz o valor da parcela (não divide)
                if g.get("tipo") == "Parcelado" or g.get("parcelas", 1) > 1:
                    parcelado += g.get("valor", 0)
                else:
                    vista += g.get("valor", 0)
            
            # Limites do cartão
            limite_vista_cartao = cartao.get("limite_vista", 0) or 0
            limite_parcelado_cartao = cartao.get("limite_parcelado", 0) or 0
            # Fallback: se não tem limite_vista, calcula
            if not limite_vista_cartao and cartao.get("limite_total", 0):
                limite_vista_cartao = (cartao.get("limite_total", 0) or 0) - limite_parcelado_cartao
            
            ctx.cartoes_detalhe[nome] = {
                "vista": vista,
                "parcelado": parcelado,
                "total": vista + parcelado,
                "limite_total": limite_vista_cartao + limite_parcelado_cartao,
                "limite_vista": limite_vista_cartao,
                "limite_parcelado": limite_parcelado_cartao,
            }
        
        # Consolidação global
        ctx.total_gasto_vista = sum(c["vista"] for c in ctx.cartoes_detalhe.values()) + ctx.total_fixos
        ctx.total_gasto_parcelado = sum(c["parcelado"] for c in ctx.cartoes_detalhe.values())
        ctx.total_gasto = ctx.total_gasto_vista + ctx.total_gasto_parcelado
        
        ctx.limite_vista = sum(c["limite_vista"] for c in ctx.cartoes_detalhe.values())
        ctx.limite_parcelado = sum(c["limite_parcelado"] for c in ctx.cartoes_detalhe.values())
        ctx.limite_total = ctx.limite_vista + ctx.limite_parcelado
        
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
    ctx.dias_para_fechamento = max(ctx.dia_fechamento - hoje.day, 0)
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
        ctx.total_mes_passado = sum(g.get("valor", 0) for g in gastos_mes_passado)
    else:
        ctx.total_mes_passado = 0
    
    # Últimos dias
    ctx.gastos_ultimos_3_dias = sum(
        g.get("valor", 0) for g in gastos
        if g.get("data") and (hoje - datetime.strptime(g["data"], "%Y-%m-%d")).days <= 3
    )
    ctx.gastos_ultimos_7_dias = sum(
        g.get("valor", 0) for g in gastos
        if g.get("data") and (hoje - datetime.strptime(g["data"], "%Y-%m-%d")).days <= 7
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
    if ctx.total_gasto > ctx.limite_total:
        return [Notification("crit1", "Limite Total Estourado!",
            f"Você ultrapassou em R$ {ctx.total_gasto - ctx.limite_total:.2f}. Evite novas compras!",
            "🚨 CRÍTICO", 100, "⚠️", "#ef4444", "Agora")]
    return []

def r_percentual_alto(ctx):
    if ctx.percentual > 90:
        return [Notification("crit2", "Uso Elevado do Limite",
            f"{ctx.percentual:.0f}% do limite utilizado. Máximo cuidado!",
            "🚨 CRÍTICO", 95, "🔥", "#f97316", "Urgente")]
    return []

def r_restante_baixo(ctx):
    if 0 < ctx.restante < 100:
        return [Notification("crit3", "Limite Quase Esgotado",
            f"Restam apenas R$ {ctx.restante:.2f}. Cuidado!",
            "🚨 CRÍTICO", 85, "⚠️", "#ef4444", "Agora")]
    return []

def r_cartao_estourado(ctx):
    """Verifica se algum cartão individual estourou"""
    notificacoes = []
    for nome, c in ctx.cartoes_detalhe.items():
        if c["total"] > c["limite_total"] and c["limite_total"] > 0:
            excedeu = c["total"] - c["limite_total"]
            notificacoes.append(Notification(
                f"cart_{nome}",
                f"Cartão {nome} Estourado!",
                f"Excedeu em R$ {excedeu:.2f}. Limite: R$ {c['limite_total']:.2f}.",
                "🚨 CRÍTICO", 100, "💳", "#ef4444", "Agora"
            ))
    return notificacoes

def r_parcelado_excedido(ctx):
    """Verifica se parcelado excedeu por cartão"""
    notificacoes = []
    for nome, c in ctx.cartoes_detalhe.items():
        if c["parcelado"] > c["limite_parcelado"] and c["limite_parcelado"] > 0:
            notificacoes.append(Notification(
                f"parc_{nome}",
                f"Parcelado Excedido - {nome}",
                f"Parcelas R$ {c['parcelado']:.2f} > Limite R$ {c['limite_parcelado']:.2f}",
                "🚨 CRÍTICO", 90, "📦", "#ef4444", "Urgente"
            ))
    return notificacoes

def r_vista_excedido(ctx):
    """Verifica se à vista excedeu por cartão"""
    notificacoes = []
    for nome, c in ctx.cartoes_detalhe.items():
        if c["vista"] > c["limite_vista"] and c["limite_vista"] > 0:
            notificacoes.append(Notification(
                f"vista_{nome}",
                f"À Vista Excedido - {nome}",
                f"Gasto R$ {c['vista']:.2f} > Limite R$ {c['limite_vista']:.2f}",
                "🚨 CRÍTICO", 90, "💰", "#ef4444", "Urgente"
            ))
    return notificacoes


# ============================================================
# ⚠️ REGRAS - ALERTA
# ============================================================
def r_parcelado_domina(ctx):
    if ctx.total_gasto_parcelado > ctx.total_gasto_vista and ctx.total_gasto > 0:
        return [Notification("alt1", "Parcelado Dominante",
            "Você está dependendo muito de parcelamento. Cuidado!",
            "⚠️ ALERTA", 70, "📦", "#f59e0b", "Atenção")]
    return []

def r_fixos_altos(ctx):
    if ctx.limite_total > 0 and ctx.total_fixos > ctx.limite_total * 0.3:
        return [Notification("alt2", "Gastos Fixos Elevados",
            f"Seus custos fixos representam {ctx.total_fixos/ctx.limite_total*100:.0f}% do limite. Revise assinaturas.",
            "⚠️ ALERTA", 70, "📊", "#f59e0b", "Sugestão")]
    return []

def r_percentual_80(ctx):
    if 80 <= ctx.percentual < 90:
        return [Notification("alt3", f"Limite em {ctx.percentual:.0f}%",
            f"Usado R$ {ctx.total_gasto:.2f} de R$ {ctx.limite_total:.2f}. Atenção!",
            "⚠️ ALERTA", 75, "🟡", "#f59e0b", "Atenção")]
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

def r_ticket_alto(ctx):
    if ctx.qtd_gastos > 0:
        ticket_medio = ctx.total_gasto / ctx.qtd_gastos
        if ticket_medio > 200:
            return [Notification("ana2", "Ticket Médio Alto",
                f"Média de R$ {ticket_medio:.2f} por compra.",
                "📊 ANÁLISE", 60, "💰", "#8b5cf6", "Análise")]
    return []


# ============================================================
# 🔮 REGRAS - PREVISÃO
# ============================================================
def r_projecao_estouro(ctx):
    if ctx.projecao > ctx.limite_total and ctx.percentual < 90:
        return [Notification("prev1", "Projeção: Limite Será Estourado!",
            f"Neste ritmo, você gastará R$ {ctx.projecao:.2f}.",
            "🔮 PREVISÃO", 90, "🔮", "#ef4444", "Atenção")]
    return []

def r_projecao_sobra(ctx):
    if ctx.projecao < ctx.limite_total * 0.7 and ctx.percentual < 50:
        return [Notification("prev2", "Vai Sobrar Dinheiro!",
            f"Projeção: R$ {ctx.projecao:.2f}. Considere investir.",
            "🔮 PREVISÃO", 40, "💡", "#10b981", "Oportunidade")]
    return []

def r_ritmo_alto(ctx):
    ritmo_ideal = ctx.limite_total / 30
    if ctx.gasto_diario > ritmo_ideal * 1.5 and ctx.dia_atual > 5:
        return [Notification("prev3", "Ritmo Acima do Ideal",
            f"Gasto diário R$ {ctx.gasto_diario:.2f} (ideal: R$ {ritmo_ideal:.2f}).",
            "🔮 PREVISÃO", 75, "⚡", "#ef4444", "Atenção")]
    return []


# ============================================================
# 💳 REGRAS - CARTÕES
# ============================================================
def r_cartao_sem_uso(ctx):
    if ctx.cartoes_sem_uso:
        nomes = ", ".join(ctx.cartoes_sem_uso[:2])
        return [Notification("cart1", f"Cartão sem Uso: {nomes}",
            "Considere concentrar gastos em um cartão para melhor controle.",
            "💳 CARTÕES", 35, "💳", "#6366f1", "Dica")]
    return []


# ============================================================
# 🎯 REGRAS - METAS
# ============================================================
def r_melhor_mes(ctx):
    if ctx.total_mes_passado > 0 and ctx.total_gasto < ctx.total_mes_passado:
        economia = ctx.total_mes_passado - ctx.total_gasto
        return [Notification("meta1", "Melhor que Mês Passado! 🏆",
            f"Você economizou R$ {economia:.2f} em relação ao mês anterior.",
            "🎯 METAS", 50, "🏆", "#10b981", "Parabéns")]
    return []

def r_dentro_meta(ctx):
    if ctx.percentual < 50 and ctx.total_gasto > 0:
        return [Notification("meta2", "Dentro da Meta! 🎯",
            f"Apenas {ctx.percentual:.0f}% do limite usado. Continue assim!",
            "🎯 METAS", 40, "🎯", "#10b981", "Parabéns")]
    return []


# ============================================================
# CONFIGURAÇÃO DE PLANOS
# ============================================================
REGRAS_GRATUITO = [
    'r_limite_estourado',
    'r_percentual_alto',
    'r_restante_baixo',
    'r_percentual_80',
    'r_fixos_altos',
    'r_melhor_mes',
]

REGRAS_PREMIUM = [
    'r_limite_estourado', 'r_percentual_alto', 'r_restante_baixo',
    'r_cartao_estourado', 'r_parcelado_excedido', 'r_vista_excedido',
    'r_parcelado_domina', 'r_fixos_altos', 'r_percentual_80',
    'r_fim_semana', 'r_inicio_mes',
    'r_categoria_dominante', 'r_ticket_alto',
    'r_projecao_estouro', 'r_projecao_sobra', 'r_ritmo_alto',
    'r_cartao_sem_uso',
    'r_melhor_mes', 'r_dentro_meta',
]

MAPA_REGRAS = {
    # CRÍTICO
    'r_limite_estourado': r_limite_estourado,
    'r_percentual_alto': r_percentual_alto,
    'r_restante_baixo': r_restante_baixo,
    'r_cartao_estourado': r_cartao_estourado,
    'r_parcelado_excedido': r_parcelado_excedido,
    'r_vista_excedido': r_vista_excedido,
    # ALERTA
    'r_parcelado_domina': r_parcelado_domina,
    'r_fixos_altos': r_fixos_altos,
    'r_percentual_80': r_percentual_80,
    # COMPORTAMENTO
    'r_fim_semana': r_fim_semana,
    'r_inicio_mes': r_inicio_mes,
    # ANÁLISE
    'r_categoria_dominante': r_categoria_dominante,
    'r_ticket_alto': r_ticket_alto,
    # PREVISÃO
    'r_projecao_estouro': r_projecao_estouro,
    'r_projecao_sobra': r_projecao_sobra,
    'r_ritmo_alto': r_ritmo_alto,
    # CARTÕES
    'r_cartao_sem_uso': r_cartao_sem_uso,
    # METAS
    'r_melhor_mes': r_melhor_mes,
    'r_dentro_meta': r_dentro_meta,
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
            "Desbloqueie 19 regras inteligentes com o plano Premium!",
            "💎 UPGRADE", 10, "⭐", "#8b5cf6", "Dica"
        ))
    
    notificacoes.sort(key=lambda n: n.prioridade, reverse=True)
    return [n.to_dict() for n in notificacoes]
