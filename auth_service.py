"""
Serviço de Autenticação - Fonte única de verdade para usuário logado
"""

import json
import os

ARQUIVO = 'usuarios.json'


def get_usuario_logado():
    """Retorna o primeiro usuário ativo do arquivo JSON"""
    if not os.path.exists(ARQUIVO):
        return None
    
    with open(ARQUIVO, 'r', encoding='utf-8') as f:
        usuarios = json.load(f)
    
    # Retorna o primeiro usuário ativo
    for u in usuarios:
        if u.get("ativo", True):
            return u
    
    # Fallback: retorna o primeiro usuário
    return usuarios[0] if usuarios else None


def atualizar_usuario(usuario_id, **kwargs):
    """Atualiza dados de um usuário no arquivo JSON"""
    if not os.path.exists(ARQUIVO):
        return False
    
    with open(ARQUIVO, 'r', encoding='utf-8') as f:
        usuarios = json.load(f)
    
    for u in usuarios:
        if u.get("id") == usuario_id:
            for key, value in kwargs.items():
                if value is not None:
                    u[key] = value
            
            with open(ARQUIVO, 'w', encoding='utf-8') as f:
                json.dump(usuarios, f, indent=2, ensure_ascii=False)
            return True
    
    return False