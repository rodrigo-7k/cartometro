"""
Consultor Financeiro Inteligente - Cartometro
44 Regras em 6 Blocos
"""

from datetime import datetime, timedelta
from collections import defaultdict


# ============================================================
# MODELOS
# ============================================================
class Notification:
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
            "id": self.id, "titulo": self.titulo, "descricao": self.descricao,
            "categoria": self.categoria, "prioridade": self.prioridade,
            "icone": self.icone, "cor": self.cor, "tempo": self.tempo
        }


class Context:
    def __init__(self):
        self.total_gasto = 0
        self.total_gasto_vista = 0
        self.total_gasto_parcelado = 0
        self.total_fixos = 0
        self.total_mes_passado = 0
        self.total_fixos_passado = 0
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
        self.historico_3_ciclos = []
        self.gastos = []
        self.fixos = []


# ============================================================
# FUNÇÕES DE CICLO
# ============================================================
def obter_periodo_ciclo(dia_fechamento):
    hoje = datetime.now()
    if hoje.day > dia_fechamento:
        inicio = datetime(hoje.year, hoje.month, dia_fechamento + 1)
        fim = datetime(hoje.year, hoje.month + 1 if hoje.month < 12 else 1, dia_fechamento)
        if hoje.month == 12:
            fim = datetime(hoje.year + 1, 1, dia_fechamento)
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
    ctx = Context()
    hoje = datetime.now()
    config = dados.get("config", {})
    
    ctx.gastos = gastos
    ctx.fixos = fixos
    ctx.total_fixos = sum(f.get("valor", 0) for f in fixos)
    ctx.qtd_gastos = len(gastos)
    ctx.dia_atual = hoje.day
    ctx.dia_fechamento = config.get("dia_fechamento", 10)
    ctx.dias_para_fechamento = max(ctx.dia_fechamento - hoje.day, 0)
    ctx.modo_cartao = config.get("modo_cartao", "Unificado")
    
    # Processar cartões individuais
    ctx.cartoes_detalhe = {}
    if cartoes and ctx.modo_cartao == "Individual":
        for cartao in cartoes:
            nome = cartao.get("nome", "")
            dia_fech = cartao.get("dia_fechamento", 10)
            inicio, fim = obter_periodo_ciclo(dia_fech)
            
            vista = 0; parcelado = 0
            for g in gastos:
                if g.get("cartao") != nome: continue
                if not g.get("data"): continue
                try: data = datetime.strptime(g["data"], "%Y-%m-%d")
                except: continue
                if not (inicio <= data <= fim): continue
                if data > hoje: continue
                
                valor = g.get("valor", 0)
                is_parcelado = (g.get("tipo") == "Parcelado" or g.get("parcelas", 1) > 1)
                if is_parcelado: parcelado += valor
                else: vista += valor
            
            limite_v = cartao.get("limite_vista", 0) or 0
            limite_p = cartao.get("limite_parcelado", 0) or 0
            if not limite_v and cartao.get("limite_total", 0):
                limite_v = (cartao.get("limite_total", 0) or 0) - limite_p
            
            ctx.cartoes_detalhe[nome] = {
                "vista": vista, "parcelado": parcelado, "total": vista + parcelado,
                "limite_total": limite_v + limite_p, "limite_vista": limite_v, "limite_parcelado": limite_p,
            }
        
        ctx.total_gasto_vista = sum(c["vista"] for c in ctx.cartoes_detalhe.values()) + ctx.total_fixos
        ctx.total_gasto_parcelado = sum(c["parcelado"] for c in ctx.cartoes_detalhe.values())
        ctx.total_gasto = ctx.total_gasto_vista + ctx.total_gasto_parcelado
        ctx.limite_vista = sum(c["limite_vista"] for c in ctx.cartoes_detalhe.values())
        ctx.limite_parcelado = sum(c["limite_parcelado"] for c in ctx.cartoes_detalhe.values())
        ctx.limite_total = ctx.limite_vista + ctx.limite_parcelado
        ctx.cartoes_uso = {nome: c["total"] for nome, c in ctx.cartoes_detalhe.items()}
        ctx.cartoes_sem_uso = [nome for nome, c in ctx.cartoes_detalhe.items() if c["total"] == 0]
    else:
        ctx.limite_vista = config.get("limite_vista", config.get("limite_total", 3000))
        ctx.limite_parcelado = config.get("limite_parcelado", 1500)
        ctx.limite_total = ctx.limite_vista + ctx.limite_parcelado
        ctx.total_gasto_vista = 0; ctx.total_gasto_parcelado = 0
        for g in gastos:
            valor = g.get("valor", 0)
            is_parcelado = (g.get("tipo") == "Parcelado" or g.get("parcelas", 1) > 1)
            if is_parcelado: ctx.total_gasto_parcelado += valor
            else: ctx.total_gasto_vista += valor
        ctx.total_gasto_vista += ctx.total_fixos
        ctx.total_gasto = ctx.total_gasto_vista + ctx.total_gasto_parcelado
    
    ctx.restante = ctx.limite_total - ctx.total_gasto
    ctx.percentual = (ctx.total_gasto / ctx.limite_total * 100) if ctx.limite_total else 0
    ctx.gasto_diario = ctx.total_gasto / max(ctx.dia_atual, 1)
    ctx.projecao = ctx.total_gasto + (ctx.gasto_diario * ctx.dias_para_fechamento)
    
    # Categorias
    categorias = defaultdict(float)
    for g in gastos:
        categorias[g.get("categoria", "Outros")] += g.get("valor", 0)
    ctx.gastos_por_categoria = dict(categorias)
    
    if gastos_mes_passado:
        cat_passado = defaultdict(float)
        total_fixos_passado = 0
        for g in gastos_mes_passado:
            cat_passado[g.get("categoria", "Outros")] += g.get("valor", 0)
        ctx.categoria_mes_passado = dict(cat_passado)
        ctx.total_mes_passado = sum(g.get("valor", 0) for g in gastos_mes_passado)
        ctx.total_fixos_passado = total_fixos_passado
    
    # Últimos dias
    ctx.gastos_ultimos_3_dias = sum(g.get("valor", 0) for g in gastos if g.get("data") and (hoje - datetime.strptime(g["data"], "%Y-%m-%d")).days <= 3)
    ctx.gastos_ultimos_7_dias = sum(g.get("valor", 0) for g in gastos if g.get("data") and (hoje - datetime.strptime(g["data"], "%Y-%m-%d")).days <= 7)
    
    # FDS, início/fim mês
    ctx.gastos_fim_semana = sum(g.get("valor", 0) for g in gastos if g.get("data") and datetime.strptime(g["data"], "%Y-%m-%d").weekday() >= 5)
    ctx.gastos_inicio_mes = sum(g.get("valor", 0) for g in gastos if g.get("data") and datetime.strptime(g["data"], "%Y-%m-%d").day <= 3)
    ctx.gastos_fim_mes = sum(g.get("valor", 0) for g in gastos if g.get("data") and datetime.strptime(g["data"], "%Y-%m-%d").day >= 25)
    
    return ctx


# ============================================================
# 🚨 BLOCO 1 — CRÍTICO (10 regras)
# ============================================================
def r01_limite_total_estourado(ctx):
    if ctx.total_gasto > ctx.limite_total:
        return [Notification("r01", "Limite Total Estourado!", f"Gasto R$ {ctx.total_gasto:.2f} > Limite R$ {ctx.limite_total:.2f}", "🚨 CRÍTICO", 100, "⛔", "#ef4444")]
    return []

def r02_limite_vista_estourado(ctx):
    if ctx.total_gasto_vista > ctx.limite_vista:
        return [Notification("r02", "Limite À Vista Estourado!", f"À Vista R$ {ctx.total_gasto_vista:.2f} > Limite R$ {ctx.limite_vista:.2f}", "🚨 CRÍTICO", 98, "💵", "#ef4444")]
    return []

def r03_limite_parcelado_estourado(ctx):
    if ctx.total_gasto_parcelado > ctx.limite_parcelado:
        return [Notification("r03", "Limite Parcelado Estourado!", f"Parcelado R$ {ctx.total_gasto_parcelado:.2f} > Limite R$ {ctx.limite_parcelado:.2f}", "🚨 CRÍTICO", 98, "📦", "#ef4444")]
    return []

def r04_cartao_individual_estourado(ctx):
    notifs = []
    for nome, c in ctx.cartoes_detalhe.items():
        if c["total"] > c["limite_total"] and c["limite_total"] > 0:
            notifs.append(Notification(f"r04_{nome}", f"Cartão {nome} Estourado!", f"Gasto R$ {c['total']:.2f} > Limite R$ {c['limite_total']:.2f}", "🚨 CRÍTICO", 100, "💳", "#ef4444"))
    return notifs

def r05_percentual_95(ctx):
    if ctx.percentual >= 95:
        return [Notification("r05", "95% do Limite Usado!", f"{ctx.percentual:.0f}% utilizado. Risco iminente!", "🚨 CRÍTICO", 95, "🔥", "#ef4444")]
    return []

def r06_percentual_85(ctx):
    if 85 <= ctx.percentual < 95:
        return [Notification("r06", f"{ctx.percentual:.0f}% do Limite", f"Pré-crítico. Restam R$ {ctx.restante:.2f}", "🚨 CRÍTICO", 85, "⚠️", "#f97316")]
    return []

def r07_restante_negativo(ctx):
    if ctx.restante < 0:
        return [Notification("r07", "Saldo Negativo!", f"Você deve R$ {abs(ctx.restante):.2f}", "🚨 CRÍTICO", 100, "🚫", "#ef4444")]
    return []

def r08_restante_baixo(ctx):
    if 0 < ctx.restante < 100:
        return [Notification("r08", "Saldo Muito Baixo!", f"Restam apenas R$ {ctx.restante:.2f}", "🚨 CRÍTICO", 88, "⚠️", "#ef4444")]
    return []

def r09_projecao_estouro(ctx):
    if ctx.projecao > ctx.limite_total and ctx.percentual < 90:
        return [Notification("r09", "Projeção: Vai Estourar!", f"Neste ritmo, gastará R$ {ctx.projecao:.2f}", "🚨 CRÍTICO", 92, "🔮", "#ef4444")]
    return []

def r10_ritmo_fora_ideal(ctx):
    ideal = ctx.limite_total / max(ctx.dias_para_fechamento + ctx.dia_atual, 1)
    if ctx.gasto_diario > ideal * 1.3 and ctx.dia_atual > 3:
        return [Notification("r10", "Ritmo Acima do Ideal", f"Gasto diário R$ {ctx.gasto_diario:.2f} (ideal R$ {ideal:.2f})", "🚨 CRÍTICO", 80, "⚡", "#f97316")]
    return []


# ============================================================
# ⚠️ BLOCO 2 — ALERTAS (10 regras)
# ============================================================
def r11_crescimento_vs_anterior(ctx):
    if ctx.total_mes_passado > 0 and ctx.total_gasto > ctx.total_mes_passado * 1.2:
        return [Notification("r11", "Gasto Cresceu 20%+", f"R$ {ctx.total_gasto:.2f} vs R$ {ctx.total_mes_passado:.2f} anterior", "⚠️ ALERTA", 70, "📈", "#f59e0b")]
    return []

def r12_pico_3dias(ctx):
    if ctx.gastos_ultimos_3_dias > ctx.limite_total * 0.2:
        return [Notification("r12", "Pico nos Últimos 3 Dias", f"R$ {ctx.gastos_ultimos_3_dias:.2f} em 3 dias", "⚠️ ALERTA", 75, "🔥", "#f59e0b")]
    return []

def r13_pico_semanal(ctx):
    if ctx.gastos_ultimos_7_dias > ctx.limite_total * 0.4:
        return [Notification("r13", "Pico Semanal", f"R$ {ctx.gastos_ultimos_7_dias:.2f} em 7 dias", "⚠️ ALERTA", 70, "📊", "#f59e0b")]
    return []

def r14_categoria_explodiu(ctx):
    notifs = []
    for cat, val in ctx.gastos_por_categoria.items():
        val_passado = ctx.categoria_mes_passado.get(cat, 0)
        if val_passado > 0 and val > val_passado * 1.5:
            notifs.append(Notification(f"r14_{cat}", f"Categoria '{cat}' Disparou!", f"R$ {val:.2f} (era R$ {val_passado:.2f})", "⚠️ ALERTA", 65, "📊", "#f59e0b"))
    return notifs[:2]

def r15_categoria_concentrada(ctx):
    if ctx.gastos_por_categoria and ctx.total_gasto > 0:
        maior = max(ctx.gastos_por_categoria, key=ctx.gastos_por_categoria.get)
        pct = ctx.gastos_por_categoria[maior] / ctx.total_gasto * 100
        if pct > 40:
            return [Notification("r15", f"Gasto Concentrado em '{maior}'", f"{pct:.0f}% dos gastos nesta categoria", "⚠️ ALERTA", 60, "🎯", "#f59e0b")]
    return []

def r16_muitos_pequenos(ctx):
    if ctx.qtd_gastos > 20:
        return [Notification("r16", "Efeito Formiguinha", f"{ctx.qtd_gastos} gastos. Cuidado com pequenos valores!", "⚠️ ALERTA", 55, "🐜", "#f59e0b")]
    return []

def r17_ticket_medio_alto(ctx):
    if ctx.qtd_gastos > 0:
        ticket = ctx.total_gasto / ctx.qtd_gastos
        if ticket > 200:
            return [Notification("r17", "Ticket Médio Alto", f"Média R$ {ticket:.2f} por compra", "⚠️ ALERTA", 55, "💰", "#f59e0b")]
    return []

def r18_parcelado_dominando(ctx):
    if ctx.total_gasto_parcelado > ctx.total_gasto_vista and ctx.total_gasto > 0:
        return [Notification("r18", "Parcelado Dominante", "Gasto parcelado maior que à vista", "⚠️ ALERTA", 65, "📦", "#f59e0b")]
    return []

def r19_fixos_altos(ctx):
    if ctx.limite_total > 0 and ctx.total_fixos > ctx.limite_total * 0.3:
        return [Notification("r19", "Fixos Elevados", f"{ctx.total_fixos/ctx.limite_total*100:.0f}% do limite", "⚠️ ALERTA", 60, "🔁", "#f59e0b")]
    return []

def r20_crescimento_fixos(ctx):
    if ctx.total_fixos_passado > 0 and ctx.total_fixos > ctx.total_fixos_passado * 1.2:
        return [Notification("r20", "Fixos Cresceram 20%+", f"R$ {ctx.total_fixos:.2f} vs R$ {ctx.total_fixos_passado:.2f}", "⚠️ ALERTA", 60, "🔁", "#f59e0b")]
    return []


# ============================================================
# 🧠 BLOCO 3 — COMPORTAMENTO (10 regras)
# ============================================================
def r21_gasto_fds_alto(ctx):
    if ctx.gastos_fim_semana > (ctx.total_gasto / 4) * 1.5 and ctx.total_gasto > 0:
        return [Notification("r21", "Gasto Alto no Fim de Semana", f"R$ {ctx.gastos_fim_semana:.2f} no FDS", "🧠 COMPORTAMENTO", 45, "📅", "#8b5cf6")]
    return []

def r22_gasto_inicio_ciclo(ctx):
    if ctx.gastos_inicio_mes > ctx.limite_total * 0.25 and ctx.dia_atual <= 5:
        return [Notification("r22", "Gasto Forte no Início", f"R$ {ctx.gastos_inicio_mes:.2f} nos primeiros dias", "🧠 COMPORTAMENTO", 45, "🏁", "#8b5cf6")]
    return []

def r23_gasto_fim_ciclo(ctx):
    if ctx.gastos_fim_mes > ctx.limite_total * 0.3 and ctx.dia_atual >= 25:
        return [Notification("r23", "Descontrole no Fim do Ciclo", f"R$ {ctx.gastos_fim_mes:.2f} no final", "🧠 COMPORTAMENTO", 45, "🏁", "#8b5cf6")]
    return []

def r24_intervalo_curto(ctx):
    datas = []
    for g in ctx.gastos:
        if g.get("data"):
            try: datas.append(datetime.strptime(g["data"], "%Y-%m-%d"))
            except: pass
    datas.sort()
    for i in range(len(datas)-2):
        if (datas[i+1] - datas[i]).total_seconds() < 7200:
            return [Notification("r24", "Compras em Sequência", "Intervalo menor que 2h entre compras", "🧠 COMPORTAMENTO", 40, "⏱️", "#8b5cf6")]
    return []

def r25_categoria_recorrente(ctx):
    return []

def r26_padrao_crescente(ctx):
    return []

def r27_uso_concentrado_cartao(ctx):
    if ctx.cartoes_uso and len(ctx.cartoes_uso) > 1:
        total = sum(ctx.cartoes_uso.values())
        for nome, val in ctx.cartoes_uso.items():
            if total > 0 and val / total > 0.7:
                return [Notification("r27", f"Uso Concentrado: {nome}", f"{val/total*100:.0f}% dos gastos", "🧠 COMPORTAMENTO", 40, "💳", "#8b5cf6")]
    return []

def r28_cartao_parado(ctx):
    if ctx.cartoes_sem_uso:
        return [Notification("r28", f"Cartão Parado: {', '.join(ctx.cartoes_sem_uso[:2])}", "Sem uso no ciclo atual", "🧠 COMPORTAMENTO", 30, "💤", "#8b5cf6")]
    return []

def r29_alternancia_ruim(ctx):
    return []

def r30_gasto_emocional(ctx):
    if ctx.qtd_gastos > 5 and ctx.gastos_ultimos_3_dias > ctx.total_gasto * 0.4:
        return [Notification("r30", "Possível Gasto Emocional", "Muitos gastos em pouco tempo", "🧠 COMPORTAMENTO", 50, "🧠", "#8b5cf6")]
    return []


# ============================================================
# 🔮 BLOCO 4 — PREVISÃO (5 regras)
# ============================================================
def r31_vai_sobrar(ctx):
    if ctx.projecao < ctx.limite_total * 0.7 and ctx.percentual < 50:
        return [Notification("r31", "Vai Sobrar Dinheiro!", f"Projeção: R$ {ctx.projecao:.2f}", "🔮 PREVISÃO", 35, "💡", "#10b981")]
    return []

def r32_vai_estourar(ctx):
    if ctx.projecao > ctx.limite_total and ctx.percentual > 50:
        return [Notification("r32", "Vai Estourar Antes do Fechamento!", f"Projeção: R$ {ctx.projecao:.2f} > R$ {ctx.limite_total:.2f}", "🔮 PREVISÃO", 85, "🔮", "#ef4444")]
    return []

def r33_melhor_cartao(ctx):
    if ctx.cartoes_detalhe:
        melhor = min(ctx.cartoes_detalhe.items(), key=lambda x: x[1]["total"] / max(x[1]["limite_total"], 1))
        return [Notification("r33", f"Melhor Cartão: {melhor[0]}", f"Menor utilização: {melhor[1]['total']/max(melhor[1]['limite_total'],1)*100:.0f}%", "🔮 PREVISÃO", 30, "💳", "#10b981")]
    return []

def r34_melhor_dia(ctx):
    return []

def r35_sugestao_corte(ctx):
    if ctx.gastos_por_categoria and ctx.total_gasto > 0:
        maior = max(ctx.gastos_por_categoria, key=ctx.gastos_por_categoria.get)
        pct = ctx.gastos_por_categoria[maior] / ctx.total_gasto * 100
        if pct > 25:
            economia = ctx.gastos_por_categoria[maior] * 0.1
            return [Notification("r35", f"Corte 10% em '{maior}'", f"Economia potencial: R$ {economia:.2f}", "🔮 PREVISÃO", 40, "✂️", "#10b981")]
    return []


# ============================================================
# 💰 BLOCO 5 — ECONOMIA (5 regras)
# ============================================================
def r36_reducao_potencial(ctx):
    if ctx.gastos_por_categoria and ctx.total_gasto > 0:
        maior = max(ctx.gastos_por_categoria, key=ctx.gastos_por_categoria.get)
        economia = ctx.gastos_por_categoria[maior] * 0.1
        return [Notification("r36", "Potencial de Economia", f"Reduza 10% em '{maior}': R$ {economia:.2f}", "💰 ECONOMIA", 40, "💡", "#10b981")]
    return []

def r37_fixos_dominam(ctx):
    if ctx.total_gasto > 0 and ctx.total_fixos / ctx.total_gasto > 0.5:
        return [Notification("r37", "Fixos Dominam", f"{ctx.total_fixos/ctx.total_gasto*100:.0f}% dos gastos são fixos", "💰 ECONOMIA", 65, "🔁", "#f59e0b")]
    return []

def r38_assinaturas_suspeitas(ctx):
    return []

def r39_gasto_invisivel(ctx):
    if ctx.qtd_gastos > 15 and ctx.total_gasto / ctx.qtd_gastos < 50:
        return [Notification("r39", "Gasto Invisível (Formiguinha)", f"{ctx.qtd_gastos} pequenos gastos", "💰 ECONOMIA", 50, "🐜", "#f59e0b")]
    return []

def r40_otimizacao_parcelamento(ctx):
    if ctx.total_gasto_parcelado > ctx.total_gasto_vista * 2:
        return [Notification("r40", "Excesso de Parcelamento", "Considere comprar à vista quando possível", "💰 ECONOMIA", 55, "📦", "#f59e0b")]
    return []


# ============================================================
# 💳 BLOCO 6 — CARTÕES (4 regras extras)
# ============================================================
def r41_melhor_distribuicao(ctx):
    return []

def r42_cartao_saudavel(ctx):
    if ctx.cartoes_detalhe:
        saudavel = min(ctx.cartoes_detalhe.items(), key=lambda x: x[1]["total"] / max(x[1]["limite_total"], 1))
        return [Notification("r42", f"Cartão Mais Saudável: {saudavel[0]}", f"Apenas {saudavel[1]['total']/max(saudavel[1]['limite_total'],1)*100:.0f}% usado", "💳 CARTÕES", 25, "💚", "#10b981")]
    return []

def r43_cartao_critico(ctx):
    notifs = []
    for nome, c in ctx.cartoes_detalhe.items():
        pct = c["total"] / max(c["limite_total"], 1) * 100
        if pct > 85:
            notifs.append(Notification(f"r43_{nome}", f"Cartão Crítico: {nome}", f"{pct:.0f}% utilizado", "💳 CARTÕES", 80, "🚨", "#ef4444"))
    return notifs

def r44_cartao_subutilizado(ctx):
    notifs = []
    for nome, c in ctx.cartoes_detalhe.items():
        pct = c["total"] / max(c["limite_total"], 1) * 100
        if pct < 10 and c["limite_total"] > 0:
            notifs.append(Notification(f"r44_{nome}", f"Cartão Subutilizado: {nome}", f"Apenas {pct:.0f}% usado", "💳 CARTÕES", 20, "💤", "#6366f1"))
    return notifs


# ============================================================
# CONFIGURAÇÃO DE PLANOS
# ============================================================
REGRAS_GRATUITO = [
    'r01', 'r05', 'r07', 'r08', 'r09', 'r19'
]

REGRAS_PREMIUM = [
    'r01','r02','r03','r04','r05','r06','r07','r08','r09','r10',
    'r11','r12','r13','r14','r15','r16','r17','r18','r19','r20',
    'r21','r22','r23','r24','r25','r26','r27','r28','r29','r30',
    'r31','r32','r33','r34','r35',
    'r36','r37','r38','r39','r40',
    'r41','r42','r43','r44',
]

MAPA_REGRAS = {
    'r01': r01_limite_total_estourado, 'r02': r02_limite_vista_estourado,
    'r03': r03_limite_parcelado_estourado, 'r04': r04_cartao_individual_estourado,
    'r05': r05_percentual_95, 'r06': r06_percentual_85,
    'r07': r07_restante_negativo, 'r08': r08_restante_baixo,
    'r09': r09_projecao_estouro, 'r10': r10_ritmo_fora_ideal,
    'r11': r11_crescimento_vs_anterior, 'r12': r12_pico_3dias,
    'r13': r13_pico_semanal, 'r14': r14_categoria_explodiu,
    'r15': r15_categoria_concentrada, 'r16': r16_muitos_pequenos,
    'r17': r17_ticket_medio_alto, 'r18': r18_parcelado_dominando,
    'r19': r19_fixos_altos, 'r20': r20_crescimento_fixos,
    'r21': r21_gasto_fds_alto, 'r22': r22_gasto_inicio_ciclo,
    'r23': r23_gasto_fim_ciclo, 'r24': r24_intervalo_curto,
    'r25': r25_categoria_recorrente, 'r26': r26_padrao_crescente,
    'r27': r27_uso_concentrado_cartao, 'r28': r28_cartao_parado,
    'r29': r29_alternancia_ruim, 'r30': r30_gasto_emocional,
    'r31': r31_vai_sobrar, 'r32': r32_vai_estourar,
    'r33': r33_melhor_cartao, 'r34': r34_melhor_dia,
    'r35': r35_sugestao_corte,
    'r36': r36_reducao_potencial, 'r37': r37_fixos_dominam,
    'r38': r38_assinaturas_suspeitas, 'r39': r39_gasto_invisivel,
    'r40': r40_otimizacao_parcelamento,
    'r41': r41_melhor_distribuicao, 'r42': r42_cartao_saudavel,
    'r43': r43_cartao_critico, 'r44': r44_cartao_subutilizado,
}


# ============================================================
# MOTOR PRINCIPAL
# ============================================================
def gerar_notificacoes(dados, gastos, fixos, cartoes=None, gastos_mes_passado=None, plano="gratuito"):
    ctx = build_context(dados, gastos, fixos, cartoes, gastos_mes_passado)
    
    if plano in ["premium", "demo"]:
        regras_ativas = REGRAS_PREMIUM
    else:
        regras_ativas = REGRAS_GRATUITO
    
    notificacoes = []
    for nome_regra in regras_ativas:
        try:
            funcao = MAPA_REGRAS.get(nome_regra)
            if funcao:
                notificacoes.extend(funcao(ctx))
        except Exception as e:
            print(f"Erro na regra {nome_regra}: {e}")
    
    if plano == "gratuito":
        notificacoes.append(Notification("upgrade", "🔓 Consultor Premium", "Desbloqueie 44 regras inteligentes!", "💎 UPGRADE", 10, "⭐", "#8b5cf6"))
    
    notificacoes.sort(key=lambda n: n.prioridade, reverse=True)
    return [n.to_dict() for n in notificacoes]
