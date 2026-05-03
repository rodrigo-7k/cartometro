"""
Serviço de configuração - Temas, formatação e utilitários
"""

from constantes import COR_PRIMARIA, COR_ESCURA
import json
import os

ARQUIVO_CONFIG = "dados.json"


class ConfigService:
    """Gerencia configurações visuais e formatação"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._cor_primaria = COR_PRIMARIA
            cls._instance._cor_escura = COR_ESCURA
            cls._instance._carregar_cores()
        return cls._instance
    
    def _carregar_cores(self):
        """Carrega cores do arquivo de configuração"""
        try:
            if os.path.exists(ARQUIVO_CONFIG):
                with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
                    dados = json.load(f)
                
                config = dados.get("config", {})
                if "cor_primaria" in config:
                    self._cor_primaria = config["cor_primaria"]
                if "cor_escura" in config:
                    self._cor_escura = config["cor_escura"]
        except:
            pass
    
    def _salvar_cores(self):
        """Salva cores no arquivo de configuração"""
        try:
            # Carregar dados existentes
            if os.path.exists(ARQUIVO_CONFIG):
                with open(ARQUIVO_CONFIG, "r", encoding="utf-8") as f:
                    dados = json.load(f)
            else:
                dados = {}
            
            # Garantir estrutura
            if "config" not in dados:
                dados["config"] = {}
            
            # Atualizar cores
            dados["config"]["cor_primaria"] = self._cor_primaria
            dados["config"]["cor_escura"] = self._cor_escura
            
            # Salvar
            with open(ARQUIVO_CONFIG, "w", encoding="utf-8") as f:
                json.dump(dados, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Erro ao salvar cores: {e}")
    
    def get_primary_color(self):
        return self._cor_primaria
    
    def get_primary_dark(self):
        return self._cor_escura
    
    def set_primary_color(self, cor):
        self._cor_primaria = cor
        self._salvar_cores()
    
    def set_primary_dark(self, cor):
        self._cor_escura = cor
        self._salvar_cores()
    
    @staticmethod
    def formatar_valor(valor):
        """Formata valor monetário"""
        if valor is None:
            return "R$ 0,00"
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    @staticmethod
    def formatar_data(data):
        """Formata data para DD/MM/AAAA"""
        from datetime import datetime
        if isinstance(data, str):
            try:
                data = datetime.strptime(data, "%Y-%m-%d")
            except:
                return data
        return data.strftime("%d/%m/%Y")
    
    @staticmethod
    def cor_com_opacidade(hex_color, opacidade=0.1):
        """Converte cor hex para rgba com opacidade"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"rgba({r}, {g}, {b}, {opacidade})"


# Singleton global
config_service = ConfigService()