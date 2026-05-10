"""
Configurações e constantes compartilhadas
"""

import os

# ============================================================
# URLS DAS IMAGENS (CLOUDINARY)
# ============================================================
LOGO_BRANCA      = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845617/logo_branca_mmgwof.png"
LOGO_FULL_BRANCA = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845630/logo_full_branca_wlx97y.png"
LOGO             = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845521/logo_bvchvv.png"
WORDMARK         = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845635/wordmark_nf3put.png"
LOGO_FULL_COLOR  = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845644/logo_full_b6tse3.png"
LOGO_COMPLETA    = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845648/logo_completa_nbtgcz.png"
FAVICON          = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1777845656/favicon_crsq9e.ico"

# Imagens placeholder
PRINT_DASHBOARD   = "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778165224/hero_section_c2s8nw.jpg"
PRINT_CARTOES     = "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800&q=80"
PRINT_LANCAMENTOS = "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&q=80"
PRINT_RELATORIOS  = "https://images.unsplash.com/photo-1460925895917-afdab827c52f?w=800&q=80"

# ============================================================
# CORES PADRÃO DO SISTEMA (usadas na Landing Page e Login)
# ============================================================
COR_PRIMARIA_PADRAO = "#2563eb"
COR_ESCURA_PADRAO   = "#1d4ed8"
COR_CLARA_PADRAO    = "#eff6ff"
COR_MEDIA_PADRAO    = "#bfdbfe"

# Alias para compatibilidade com código existente
COR_PRIMARIA = COR_PRIMARIA_PADRAO
COR_ESCURA   = COR_ESCURA_PADRAO
COR_CLARA    = COR_CLARA_PADRAO
COR_MEDIA    = COR_MEDIA_PADRAO

# ============================================================


# ═══════════════════════════════════════════════════════════════
# CATÁLOGO DE CARTÕES E BANDEIRAS
# ═══════════════════════════════════════════════════════════════
CARTOES_POPULARES = [
    {"nome": "Nubank",         "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101451/01_NUBANK_qckg36.png",        "bandeira": "Mastercard", "cor": "#8b5cf6"},
    {"nome": "Banco do Brasil","img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101452/02_BANCO_DO_BRASIL_in4yxr.png", "bandeira": "Visa",       "cor": "#f59e0b"},
    {"nome": "Caixa",          "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101452/03_CAIXA_zhrs2q.png",          "bandeira": "Visa",       "cor": "#1d4ed8"},
    {"nome": "Itaú",           "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101453/04_ITAU_bcc9sw.png",           "bandeira": "Mastercard", "cor": "#f59e0b"},
    {"nome": "Bradesco",       "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101453/05_BRADESCO_he7iod.png",       "bandeira": "Visa",       "cor": "#ef4444"},
    {"nome": "Santander",      "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101454/06_SANTANDER_ew1ogg.png",      "bandeira": "Visa",       "cor": "#dc2626"},
    {"nome": "Mercado Pago",   "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101447/07_MERCADO_PAGO_o7w6vl.png",   "bandeira": "Mastercard", "cor": "#3b82f6"},
    {"nome": "Inter",          "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101447/08_INTER_a1dcn6.png",          "bandeira": "Mastercard", "cor": "#f97316"},
    {"nome": "Banco PAN",      "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101447/09_BANCO_PAN_hnrkff.png",      "bandeira": "Mastercard", "cor": "#2563eb"},
    {"nome": "PicPay",         "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101447/10_PICPAY_qibpgs.png",         "bandeira": "Mastercard", "cor": "#10b981"},
    {"nome": "Sicoob",         "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101447/11_SICOOB_madwy1.png",         "bandeira": "Mastercard", "cor": "#22c55e"},
    {"nome": "Banco Original", "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101447/12_BANCO_ORIGINAL_zxgynu.png", "bandeira": "Mastercard", "cor": "#16a34a"},
    {"nome": "Neon",           "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101449/15_NEON_lc38mq.png",           "bandeira": "Visa",       "cor": "#ea580c"},
    {"nome": "Digio",          "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101449/16_DIGIO_yvcjic.png",          "bandeira": "Visa",       "cor": "#a855f7"},
    {"nome": "XP Investimentos","img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101450/17_XP_INVESTIMENTOS_paxuws.png","bandeira": "Visa",    "cor": "#374151"},
    {"nome": "BTG Pactual",    "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778101451/20_BTG_PACTUAL_q7gcub.png",    "bandeira": "Mastercard", "cor": "#2563eb"},
    {"nome": "C6 Bank",        "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111545/08_C6_BANK_uhcgrc.png",        "bandeira": "Mastercard", "cor": "#1f2937"},
    {"nome": "Next",           "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111545/09_NEXT_hroswa.png",           "bandeira": "Visa",       "cor": "#22c55e"},
    {"nome": "Porto Seguro",   "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111545/10_PORTO_SEGURO_enw885.png",   "bandeira": "Visa",       "cor": "#1e40af"},
    {"nome": "Azul",           "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111545/11_AZUL_uodkke.png",           "bandeira": "Visa",       "cor": "#3b82f6"},
    {"nome": "LATAM Pass",     "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111546/12_LATAM_PASS_x8isgn.png",     "bandeira": "Mastercard", "cor": "#dc2626"},
]

BANDEIRAS = [
    {"nome": "Visa",            "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111544/01_VISA_r0gbp1.png"},
    {"nome": "Mastercard",      "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111544/02_MASTERCARD_ofek0k.png"},
    {"nome": "Elo",             "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111544/03_ELO_d0gn8c.png"},
    {"nome": "American Express","img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111544/04_AMERICAN_EXPRESS_yn7ffw.png"},
    {"nome": "Hipercard",       "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111544/05_HIPERCARD_y0kuh1.png"},
    {"nome": "Diners",          "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111544/06_DINERS_CLUB_iewgua.png"},
    {"nome": "Discover",        "img": "https://res.cloudinary.com/dxgyzvs8p/image/upload/v1778111545/07_DISCOVER_g1xoiv.png"},
]

def get_img_cartao(nome):
    """Retorna a URL da imagem do cartão pelo nome"""
    for c in CARTOES_POPULARES:
        if c["nome"] == nome:
            return c["img"]
    return None

def get_img_bandeira(nome):
    """Retorna a URL da imagem da bandeira pelo nome"""
    for b in BANDEIRAS:
        if b["nome"] == nome:
            return b["img"]
    return None

# VARIÁVEIS GLOBAIS
# ============================================================
usuario_atual = None

# ============================================================
# FUNÇÕES PARA CORES DINÂMICAS (usadas no App pós-login)
# ============================================================
def get_cores_usuario():
    """
    Retorna as cores configuradas pelo usuário logado.
    Se não houver usuário logado, retorna as cores padrão.
    """
    if usuario_atual and isinstance(usuario_atual, dict):
        config = usuario_atual.get('config', {})
        return {
            'primaria': config.get('cor_primaria', COR_PRIMARIA_PADRAO),
            'escura': config.get('cor_escura', COR_ESCURA_PADRAO),
            'clara': f"{config.get('cor_primaria', COR_PRIMARIA_PADRAO)}15",  # com transparência
            'media': f"{config.get('cor_primaria', COR_PRIMARIA_PADRAO)}40",  # com transparência
        }
    return {
        'primaria': COR_PRIMARIA_PADRAO,
        'escura': COR_ESCURA_PADRAO,
        'clara': COR_CLARA_PADRAO,
        'media': COR_MEDIA_PADRAO,
    }