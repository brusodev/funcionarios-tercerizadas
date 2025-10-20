"""
Exemplo Prático de Uso do Template de Serviços
==============================================

Este arquivo demonstra diferentes formas de usar o template de serviços.
"""

from template_servicos import TemplateServicos, AreaAtuacao, Funcionario
import json

def exemplo_basico():
    """Exemplo básico de uso do template"""
    print("🔸 EXEMPLO BÁSICO")
    print("-" * 50)
    
    # Criar template
    template = TemplateServicos()
    
    # Carregar dados existentes
    template.carregar_todos_dados()
    
    # Exibir relatório resumido
    relatorio = template.gerar_relatorio_completo()
    print(f"Total de funcionários: {relatorio['resumo_geral']['total_funcionarios']}")
    print(f"Áreas com dados: {relatorio['resumo_geral']['areas_com_dados']}")

def exemplo_detalhado():
    """Exemplo com análise detalhada"""
    print("\n🔸 EXEMPLO DETALHADO")
    print("-" * 50)
    
    template = TemplateServicos()
    template.carregar_todos_dados()
    
    # Analisar área específica
    area_manutencao = template.areas['manutencao_predios']
    
    if area_manutencao.funcionarios:
        print(f"📋 Análise: {area_manutencao.nome}")
        print(f"   • Total: {area_manutencao.get_total_funcionarios()} funcionários")
        
        # Funcionários por local
        por_local = area_manutencao.get_funcionarios_por_local()
        print(f"   • Distribuição por local:")
        for local, func_list in por_local.items():
            print(f"     - {local}: {len(func_list)} funcionários")
        
        # Primeiros 3 funcionários
        print(f"   • Primeiros funcionários:")
        for i, func in enumerate(area_manutencao.funcionarios[:3]):
            print(f"     {i+1}. {func.nome}")

def exemplo_criacao_manual():
    """Exemplo criando dados manualmente"""
    print("\n🔸 EXEMPLO CRIAÇÃO MANUAL")
    print("-" * 50)
    
    template = TemplateServicos()
    
    # Criar funcionários manualmente para área de Segurança
    funcionarios_seguranca = [
        Funcionario(1, "JOÃO DA SILVA SANTOS", "Serviço de segurança patrimonial", "Sede/Arouche"),
        Funcionario(2, "MARIA OLIVEIRA COSTA", "Controle de acesso", "Casa Verde/Cape"),
        Funcionario(3, "PEDRO SOUZA LIMA", "Vigilância noturna", "Sede")
    ]
    
    # Atualizar área
    area_seguranca = template.areas['seguranca_acesso']
    area_seguranca.funcionarios = funcionarios_seguranca
    area_seguranca.tipos_servico = list(set(f.tipo_servico for f in funcionarios_seguranca))
    
    # Coletar todos os locais
    locais = set()
    for func in funcionarios_seguranca:
        locais.update(func.get_locais_lista())
    area_seguranca.locais_atendidos = list(locais)
    
    print("✅ Área de Segurança configurada manualmente!")
    print(f"   • {len(funcionarios_seguranca)} funcionários adicionados")
    print(f"   • Locais: {', '.join(area_seguranca.locais_atendidos)}")

def exemplo_exportacao():
    """Exemplo de diferentes formatos de exportação"""
    print("\n🔸 EXEMPLO EXPORTAÇÃO")
    print("-" * 50)
    
    template = TemplateServicos()
    template.carregar_todos_dados()
    
    # Relatório JSON
    template.salvar_relatorio_json("relatorio_exemplo.json")
    
    # Relatório customizado por área
    relatorio = template.gerar_relatorio_completo()
    
    for area_key, area_info in relatorio['areas'].items():
        if area_info['total_funcionarios'] > 0:
            nome_arquivo = f"relatorio_{area_key}.json"
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(area_info, f, ensure_ascii=False, indent=2)
            print(f"📄 Relatório da área salvo: {nome_arquivo}")

def exemplo_analise_comparativa():
    """Exemplo de análise comparativa entre áreas"""
    print("\n🔸 EXEMPLO ANÁLISE COMPARATIVA")
    print("-" * 50)
    
    template = TemplateServicos()
    template.carregar_todos_dados()
    
    print("📊 Comparativo entre áreas:")
    print("="*60)
    
    areas_com_dados = []
    for key, area in template.areas.items():
        if area.funcionarios:
            total_func = area.get_total_funcionarios()
            total_locais = len(area.locais_atendidos)
            areas_com_dados.append({
                'nome': area.nome,
                'funcionarios': total_func,
                'locais': total_locais,
                'media_func_por_local': round(total_func / total_locais if total_locais > 0 else 0, 2)
            })
    
    # Ordenar por número de funcionários
    areas_com_dados.sort(key=lambda x: x['funcionarios'], reverse=True)
    
    for i, area in enumerate(areas_com_dados, 1):
        print(f"{i}º {area['nome']}")
        print(f"   👥 {area['funcionarios']} funcionários")
        print(f"   📍 {area['locais']} locais")
        print(f"   📈 Média: {area['media_func_por_local']} func/local")
        print()

def main():
    """Executa todos os exemplos"""
    print("🚀 EXEMPLOS DE USO DO TEMPLATE DE SERVIÇOS")
    print("="*80)
    
    # Executar exemplos
    exemplo_basico()
    exemplo_detalhado()
    exemplo_criacao_manual()
    exemplo_exportacao()
    exemplo_analise_comparativa()
    
    print("✅ Todos os exemplos executados com sucesso!")
    print("\n💡 Dica: Verifique os arquivos JSON gerados para ver os dados estruturados.")

if __name__ == "__main__":
    main()