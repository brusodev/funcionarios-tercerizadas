"""
Lista de Funcionários por Área e Local
=====================================

Script para gerar listagens detalhadas dos funcionários organizadas por área e local.
"""

import pandas as pd
from template_servicos import TemplateServicos
from datetime import datetime
import json

def listar_funcionarios_detalhado():
    """Lista todos os funcionários com área e locais detalhados"""
    template = TemplateServicos()
    template.carregar_todos_dados()
    
    print("👥 LISTA COMPLETA DE FUNCIONÁRIOS")
    print("=" * 80)
    print(f"📅 Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}")
    print()
    
    total_geral = 0
    
    for chave, area in template.areas.items():
        if area.funcionarios:
            print(f"🏢 {area.nome.upper()}")
            print(f"📝 {area.descricao}")
            print("-" * 60)
            
            # Organizar funcionários por local
            funcionarios_por_local = area.get_funcionarios_por_local()
            
            for local, funcionarios in funcionarios_por_local.items():
                print(f"\n📍 LOCAL: {local}")
                print(f"   👥 {len(funcionarios)} funcionário(s)")
                print()
                
                for i, func in enumerate(funcionarios, 1):
                    print(f"   {i:2d}. {func.nome}")
                    print(f"       🔧 {func.tipo_servico}")
                    if len(func.get_locais_lista()) > 1:
                        outros_locais = [l for l in func.get_locais_lista() if l != local]
                        if outros_locais:
                            print(f"       📍 Atua também em: {', '.join(outros_locais)}")
                    print()
            
            total_area = area.get_total_funcionarios()
            total_geral += total_area
            print(f"📊 Subtotal {area.nome}: {total_area} funcionários")
            print("=" * 80)
            print()
    
    print(f"📈 TOTAL GERAL: {total_geral} funcionários")

def listar_por_local():
    """Lista funcionários organizados por local (todos os locais juntos)"""
    template = TemplateServicos()
    template.carregar_todos_dados()
    
    print("📍 FUNCIONÁRIOS POR LOCAL")
    print("=" * 80)
    print(f"📅 Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}")
    print()
    
    # Consolidar todos os funcionários por local
    todos_por_local = {}
    
    for chave, area in template.areas.items():
        if area.funcionarios:
            funcionarios_por_local = area.get_funcionarios_por_local()
            for local, funcionarios in funcionarios_por_local.items():
                if local not in todos_por_local:
                    todos_por_local[local] = []
                
                for func in funcionarios:
                    todos_por_local[local].append({
                        'funcionario': func,
                        'area': area.nome
                    })
    
    # Exibir por local
    for local in sorted(todos_por_local.keys()):
        funcionarios_local = todos_por_local[local]
        print(f"🏢 LOCAL: {local}")
        print(f"   👥 {len(funcionarios_local)} funcionário(s)")
        print("-" * 50)
        
        # Agrupar por área dentro do local
        por_area = {}
        for item in funcionarios_local:
            area_nome = item['area']
            if area_nome not in por_area:
                por_area[area_nome] = []
            por_area[area_nome].append(item['funcionario'])
        
        for area_nome, funcionarios in por_area.items():
            print(f"\n   🔹 {area_nome} ({len(funcionarios)} funcionários)")
            for i, func in enumerate(funcionarios, 1):
                print(f"      {i:2d}. {func.nome}")
                print(f"          🔧 {func.tipo_servico}")
        
        print("\n" + "=" * 80)
        print()

def gerar_lista_excel(arquivo="lista_funcionarios.xlsx"):
    """Gera uma planilha Excel com todos os funcionários organizados"""
    template = TemplateServicos()
    template.carregar_todos_dados()
    
    dados_para_excel = []
    
    for chave, area in template.areas.items():
        if area.funcionarios:
            for func in area.funcionarios:
                # Para cada local que o funcionário atua
                locais_lista = func.get_locais_lista()
                for local in locais_lista:
                    dados_para_excel.append({
                        'Area': area.nome,
                        'Funcionario': func.nome,
                        'Tipo_Servico': func.tipo_servico,
                        'Local': local,
                        'Todos_Locais': func.locais,
                        'Numero': func.numero
                    })
    
    # Criar DataFrame e salvar
    df = pd.DataFrame(dados_para_excel)
    df = df.sort_values(['Area', 'Local', 'Funcionario'])
    
    with pd.ExcelWriter(arquivo, engine='openpyxl') as writer:
        # Planilha principal
        df.to_excel(writer, sheet_name='Lista_Completa', index=False)
        
        # Planilha por área
        for area_nome in df['Area'].unique():
            df_area = df[df['Area'] == area_nome]
            nome_aba = area_nome.replace(' ', '_')[:30]  # Limite do Excel
            df_area.to_excel(writer, sheet_name=nome_aba, index=False)
        
        # Planilha por local
        df_por_local = df.groupby(['Local', 'Area', 'Funcionario']).first().reset_index()
        df_por_local.to_excel(writer, sheet_name='Por_Local', index=False)
    
    print(f"📊 Lista Excel criada: {arquivo}")
    print(f"   📄 {len(dados_para_excel)} registros")
    print(f"   📋 {len(df['Area'].unique())} áreas")
    print(f"   📍 {len(df['Local'].unique())} locais")
    
    return arquivo

def gerar_lista_json(arquivo="lista_funcionarios.json"):
    """Gera arquivo JSON estruturado com a lista de funcionários"""
    template = TemplateServicos()
    template.carregar_todos_dados()
    
    dados_json = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'total_funcionarios': 0,
        'total_areas': 0,
        'total_locais': 0,
        'areas': {},
        'por_local': {},
        'lista_completa': []
    }
    
    todos_locais = set()
    total_funcionarios = 0
    
    # Processar por área
    for chave, area in template.areas.items():
        if area.funcionarios:
            dados_json['areas'][chave] = {
                'nome': area.nome,
                'descricao': area.descricao,
                'funcionarios': []
            }
            
            for func in area.funcionarios:
                funcionario_info = {
                    'numero': func.numero,
                    'nome': func.nome,
                    'tipo_servico': func.tipo_servico,
                    'locais': func.get_locais_lista(),
                    'locais_texto': func.locais
                }
                
                dados_json['areas'][chave]['funcionarios'].append(funcionario_info)
                dados_json['lista_completa'].append({
                    **funcionario_info,
                    'area': area.nome,
                    'area_chave': chave
                })
                
                todos_locais.update(func.get_locais_lista())
                total_funcionarios += 1
    
    # Processar por local
    for local in sorted(todos_locais):
        dados_json['por_local'][local] = []
        
        for chave, area in template.areas.items():
            if area.funcionarios:
                funcionarios_local = []
                for func in area.funcionarios:
                    if local in func.get_locais_lista():
                        funcionarios_local.append({
                            'numero': func.numero,
                            'nome': func.nome,
                            'tipo_servico': func.tipo_servico,
                            'area': area.nome
                        })
                
                if funcionarios_local:
                    dados_json['por_local'][local].extend(funcionarios_local)
    
    # Totais
    dados_json['total_funcionarios'] = total_funcionarios
    dados_json['total_areas'] = len([a for a in template.areas.values() if a.funcionarios])
    dados_json['total_locais'] = len(todos_locais)
    
    # Salvar
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(dados_json, f, ensure_ascii=False, indent=2)
    
    print(f"📄 Lista JSON criada: {arquivo}")
    return arquivo

def buscar_funcionario(nome_busca):
    """Busca funcionário por nome (busca parcial)"""
    template = TemplateServicos()
    template.carregar_todos_dados()
    
    nome_busca = nome_busca.lower()
    encontrados = []
    
    for chave, area in template.areas.items():
        if area.funcionarios:
            for func in area.funcionarios:
                if nome_busca in func.nome.lower():
                    encontrados.append({
                        'funcionario': func,
                        'area': area
                    })
    
    if encontrados:
        print(f"🔍 RESULTADOS DA BUSCA: '{nome_busca}'")
        print(f"📊 {len(encontrados)} funcionário(s) encontrado(s)")
        print("=" * 60)
        
        for i, item in enumerate(encontrados, 1):
            func = item['funcionario']
            area = item['area']
            print(f"\n{i}. {func.nome}")
            print(f"   🏢 Área: {area.nome}")
            print(f"   🔧 Serviço: {func.tipo_servico}")
            print(f"   📍 Locais: {func.locais}")
    else:
        print(f"❌ Nenhum funcionário encontrado com '{nome_busca}'")

def menu_principal():
    """Menu principal para escolher tipo de listagem"""
    print("\n" + "="*60)
    print("👥 LISTAGEM DE FUNCIONÁRIOS - SERVIÇOS TERCEIRIZADOS")
    print("="*60)
    print()
    print("Escolha o tipo de listagem:")
    print("1. 📋 Lista detalhada por área")
    print("2. 📍 Lista organizada por local")
    print("3. 📊 Gerar planilha Excel")
    print("4. 📄 Gerar arquivo JSON")
    print("5. 🔍 Buscar funcionário por nome")
    print("6. 📈 Todas as opções (completo)")
    print("0. ❌ Sair")
    print()
    
    while True:
        try:
            opcao = input("Digite sua opção (0-6): ").strip()
            
            if opcao == "1":
                listar_funcionarios_detalhado()
                break
            elif opcao == "2":
                listar_por_local()
                break
            elif opcao == "3":
                gerar_lista_excel()
                break
            elif opcao == "4":
                gerar_lista_json()
                break
            elif opcao == "5":
                nome = input("Digite o nome ou parte do nome: ").strip()
                if nome:
                    buscar_funcionario(nome)
                else:
                    print("❌ Nome não pode estar vazio")
                break
            elif opcao == "6":
                print("🚀 Gerando todas as listagens...")
                listar_funcionarios_detalhado()
                print("\n" + "="*80 + "\n")
                listar_por_local()
                gerar_lista_excel()
                gerar_lista_json()
                break
            elif opcao == "0":
                print("👋 Até logo!")
                break
            else:
                print("❌ Opção inválida. Digite um número de 0 a 6.")
        except KeyboardInterrupt:
            print("\n👋 Até logo!")
            break

if __name__ == "__main__":
    menu_principal()