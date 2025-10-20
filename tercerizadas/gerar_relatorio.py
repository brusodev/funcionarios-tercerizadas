"""
Utilitário para Geração Rápida de Relatórios
============================================

Script para gerar relatórios rápidos sem precisar programar.
Uso: python gerar_relatorio.py [opções]
"""

import argparse
import sys
from pathlib import Path
from template_servicos import TemplateServicos

def gerar_relatorio_simples():
    """Gera relatório simples no console"""
    template = TemplateServicos()
    template.carregar_todos_dados()
    template.exibir_relatorio()

def gerar_relatorio_json(arquivo="relatorio_completo.json"):
    """Gera relatório em JSON"""
    template = TemplateServicos()
    template.carregar_todos_dados()
    template.salvar_relatorio_json(arquivo)
    print(f"✅ Relatório JSON salvo em: {arquivo}")

def gerar_templates_areas():
    """Gera templates para áreas sem dados"""
    template = TemplateServicos()
    
    areas_sem_dados = {
        'seguranca_acesso': 'Segurança e Controle de Acesso',
        'transporte': 'Transporte'
    }
    
    for chave, nome in areas_sem_dados.items():
        arquivo = f"template_{chave}.xlsx"
        template.criar_template_nova_area(nome, arquivo)

def listar_funcionarios(area=None):
    """Lista funcionários de uma área específica ou todas"""
    template = TemplateServicos()
    template.carregar_todos_dados()
    
    if area:
        # Área específica
        area_obj = template.areas.get(area)
        if not area_obj or not area_obj.funcionarios:
            print(f"❌ Área '{area}' não encontrada ou sem dados")
            return
        
        print(f"\n👥 FUNCIONÁRIOS - {area_obj.nome.upper()}")
        print("="*60)
        for i, func in enumerate(area_obj.funcionarios, 1):
            print(f"{i:2d}. {func.nome}")
            print(f"     📋 {func.tipo_servico}")
            print(f"     📍 {func.locais}")
            print()
    else:
        # Todas as áreas
        print("\n👥 TODOS OS FUNCIONÁRIOS")
        print("="*60)
        total = 0
        
        for key, area_obj in template.areas.items():
            if area_obj.funcionarios:
                print(f"\n🔹 {area_obj.nome} ({len(area_obj.funcionarios)} funcionários)")
                for func in area_obj.funcionarios:
                    print(f"   • {func.nome}")
                total += len(area_obj.funcionarios)
        
        print(f"\n📊 Total geral: {total} funcionários")

def listar_locais():
    """Lista todos os locais de atuação"""
    template = TemplateServicos()
    template.carregar_todos_dados()
    
    todos_locais = set()
    locais_por_area = {}
    
    for key, area in template.areas.items():
        if area.funcionarios:
            locais_area = set()
            for func in area.funcionarios:
                locais_func = func.get_locais_lista()
                locais_area.update(locais_func)
                todos_locais.update(locais_func)
            locais_por_area[area.nome] = locais_area
    
    print("\n📍 LOCAIS DE ATUAÇÃO")
    print("="*60)
    
    print(f"\n🌐 Todos os locais ({len(todos_locais)} únicos):")
    for local in sorted(todos_locais):
        print(f"   • {local}")
    
    print(f"\n📋 Por área:")
    for area_nome, locais in locais_por_area.items():
        print(f"\n🔹 {area_nome}:")
        for local in sorted(locais):
            print(f"   • {local}")

def main():
    parser = argparse.ArgumentParser(
        description="Gerador de Relatórios de Serviços Terceirizados",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  python gerar_relatorio.py --simples                    # Relatório no console
  python gerar_relatorio.py --json relatorio.json       # Relatório JSON
  python gerar_relatorio.py --templates                  # Gerar templates
  python gerar_relatorio.py --funcionarios               # Listar funcionários
  python gerar_relatorio.py --funcionarios manutencao_predios  # Área específica
  python gerar_relatorio.py --locais                     # Listar locais
        """
    )
    
    parser.add_argument('--simples', action='store_true',
                       help='Gerar relatório simples no console')
    
    parser.add_argument('--json', metavar='ARQUIVO',
                       help='Gerar relatório em JSON (especificar nome do arquivo)')
    
    parser.add_argument('--templates', action='store_true',
                       help='Gerar templates Excel para áreas sem dados')
    
    parser.add_argument('--funcionarios', nargs='?', const=True, metavar='AREA',
                       help='Listar funcionários (opcionalmente de uma área específica)')
    
    parser.add_argument('--locais', action='store_true',
                       help='Listar todos os locais de atuação')
    
    args = parser.parse_args()
    
    # Se nenhum argumento, mostrar ajuda
    if len(sys.argv) == 1:
        parser.print_help()
        return
    
    try:
        if args.simples:
            gerar_relatorio_simples()
        
        if args.json:
            gerar_relatorio_json(args.json)
        
        if args.templates:
            gerar_templates_areas()
        
        if args.funcionarios is not False:
            if args.funcionarios is True:
                listar_funcionarios()
            else:
                listar_funcionarios(args.funcionarios)
        
        if args.locais:
            listar_locais()
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()