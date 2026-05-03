"""
Constantes centralizadas do sistema de controle de gastos
"""

# ==================== TIPOS DE GASTO ====================
GASTO_AVISTA = "À Vista"
GASTO_PARCELADO = "Parcelado"
GASTO_FIXO = "Fixo"

TIPOS_GASTO = [GASTO_AVISTA, GASTO_PARCELADO, GASTO_FIXO]

# ==================== CATEGORIAS PADRÃO ====================
CATEGORIAS_PADRAO = [
    {
        "nome": "Alimentação",
        "icone": "restaurant",
        "cor": "#ef4444",
        "subcategorias": ["Supermercado", "Delivery", "Restaurante", "Lanche"]
    },
    {
        "nome": "Transporte",
        "icone": "directions_car",
        "cor": "#f59e0b",
        "subcategorias": ["Combustível", "Uber/Táxi", "Estacionamento", "Pedágio"]
    },
    {
        "nome": "Assinaturas",
        "icone": "subscriptions",
        "cor": "#8b5cf6",
        "subcategorias": ["Streaming", "Academia", "Software", "Clube"]
    },
    {
        "nome": "Compras",
        "icone": "shopping_bag",
        "cor": "#ec4899",
        "subcategorias": ["Roupas", "Eletrônicos", "Casa", "Presentes"]
    },
    {
        "nome": "Saúde",
        "icone": "local_hospital",
        "cor": "#10b981",
        "subcategorias": ["Farmácia", "Consultas", "Exames", "Plano de Saúde"]
    },
    {
        "nome": "Lazer",
        "icone": "sports_esports",
        "cor": "#06b6d4",
        "subcategorias": ["Cinema", "Jogos", "Viagens", "Eventos"]
    },
    {
        "nome": "Educação",
        "icone": "school",
        "cor": "#6366f1",
        "subcategorias": ["Cursos", "Livros", "Material"]
    },
    {
        "nome": "Outros",
        "icone": "more_horiz",
        "cor": "#6b7280",
        "subcategorias": []
    }
]

# ==================== CORES DOS TIPOS ====================
CORES_TIPOS = {
    GASTO_AVISTA: "#3b82f6",
    GASTO_PARCELADO: "#f59e0b",
    GASTO_FIXO: "#8b5cf6"
}

ICONES_TIPOS = {
    GASTO_AVISTA: "credit_card",
    GASTO_PARCELADO: "receipt_long",
    GASTO_FIXO: "repeat"
}

# ==================== LIMITES PADRÃO ====================
LIMITE_TOTAL_PADRAO = 3000.00
LIMITE_PARCELADO_PADRAO = 1500.00
DIA_FECHAMENTO_PADRAO = 10

# ==================== PARCELAS ====================
PARCELAS_OPCOES = [1, 2, 3, 4, 5, 6, 8, 10, 12]
PARCELAS_MAX = 12

# ==================== CORES DO TEMA ====================
COR_PRIMARIA = "#3b82f6"
COR_ESCURA = "#1e40af"
COR_SUCESSO = "#10b981"
COR_ALERTA = "#f59e0b"
COR_PERIGO = "#ef4444"

# ==================== ARQUIVOS ====================
ARQUIVO_DADOS = "dados.json"
ARQUIVO_CONFIG = "dados.json"  # mesmo arquivo por enquanto