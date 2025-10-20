"""
Lista Rápida de Funcionários
===========================

Script simples para gerar rapidamente a lista de funcionários por área e local.
"""

from template_servicos import TemplateServicos
from datetime import datetime

def lista_rapida():
    """Gera lista rápida formatada para console"""
    template = TemplateServicos()
    template.carregar_todos_dados()
    
    print("👥 LISTA DE FUNCIONÁRIOS POR ÁREA E LOCAL")
    print("=" * 70)
    print(f"📅 {datetime.now().strftime('%d/%m/%Y às %H:%M')}")
    print()
    
    total_geral = 0
    
    for chave, area in template.areas.items():
        if area.funcionarios:
            print(f"🏢 {area.nome.upper()}")
            print("-" * 50)
            
            for i, func in enumerate(area.funcionarios, 1):
                print(f"{i:2d}. {func.nome}")
                print(f"    🔧 {func.tipo_servico}")
                print(f"    📍 {func.locais}")
                print()
            
            total_geral += len(area.funcionarios)
            print(f"📊 Total da área: {len(area.funcionarios)} funcionários")
            print("=" * 70)
            print()
    
    print(f"📈 TOTAL GERAL: {total_geral} funcionários")

if __name__ == "__main__":
    lista_rapida()