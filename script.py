# ============================================================
# CORRECAO HERO - Mais opaco na esquerda + texto preto
# ============================================================

import os
from datetime import datetime
import shutil

PASTA_RAIZ = os.path.dirname(os.path.abspath(__file__))
ARQ = os.path.join(PASTA_RAIZ, 'landing.py')
if not os.path.exists(ARQ):
    ARQ = os.path.join(PASTA_RAIZ, 'telas', 'landing.py')

backup = ARQ.replace('.py', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.py')
shutil.copy(ARQ, backup)
print(f"Backup: {backup}")

with open(ARQ, 'r', encoding='utf-8') as f:
    conteudo = f.read()

# 1. Aumentar opacidade do fade (de 0.85 para 0.95)
css_opacidade = '.lp-hero-bg::after{{content:\'\';position:absolute;top:0;left:0;width:55%;height:100%;background:linear-gradient(90deg,rgba(255,255,255,0.95) 0%,rgba(255,255,255,0.85) 40%,rgba(255,255,255,0.2) 80%,transparent 100%);z-index:1}}'
css_nova = '.lp-hero-bg::after{{content:\'\';position:absolute;top:0;left:0;width:60%;height:100%;background:linear-gradient(90deg,rgba(255,255,255,0.98) 0%,rgba(255,255,255,0.95) 35%,rgba(255,255,255,0.88) 55%,rgba(255,255,255,0.5) 75%,transparent 100%);z-index:1}}'

if css_opacidade in conteudo:
    conteudo = conteudo.replace(css_opacidade, css_nova)
    print("Fade esquerdo: mais opaco (60% largura, 98% opacidade)")
else:
    print("CSS nao encontrado, procurando alternativo...")
    if 'lp-hero-bg::after' in conteudo:
        print("Encontrado lp-hero-bg::after")

# 2. Trocar cor do texto descritivo de cinza (#6b7280) para preto (#111827)
css_texto_cinza = '.lp-hero-p{{font-size:17px;color:#6b7280;line-height:1.7;margin-bottom:32px;max-width:500px}}'
css_texto_preto = '.lp-hero-p{{font-size:17px;color:#1f2937;line-height:1.7;margin-bottom:32px;max-width:500px}}'

if css_texto_cinza in conteudo:
    conteudo = conteudo.replace(css_texto_cinza, css_texto_preto)
    print("Texto descritivo: #1f2937 (quase preto)")
else:
    # Tentar no HTML inline
    conteudo = conteudo.replace(
        "ui.label('Controle total dos seus cartoes de credito, gastos organizados por categoria e alertas personalizados para voce nunca perder o controle.').classes('lp-hero-p')",
        "ui.label('Controle total dos seus cartoes de credito, gastos organizados por categoria e alertas personalizados para voce nunca perder o controle.').classes('lp-hero-p').style('color: #1f2937 !important;')"
    )
    print("Texto descritivo: corrigido via style inline")

# 3. Trust items tambem mais escuros
conteudo = conteudo.replace(
    "font-size:13px;color:#9ca3af",
    "font-size:13px;color:#4b5563"
)
print("Trust items: cor mais escura")

with open(ARQ, 'w', encoding='utf-8') as f:
    f.write(conteudo)

print("\nHero corrigido: texto preto + fade mais opaco")