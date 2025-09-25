import pandas as pd
import os
from pathlib import Path

def clean_name(name):
    """Limpa e formata o nome do funcionário"""
    if pd.isna(name):
        return ""
    return str(name).strip().upper()

def clean_location(location):
    """Limpa e formata a localização"""
    if pd.isna(location):
        return ""
    return str(location).strip()

def process_excel_file(file_path, area_title):
    """Processa um arquivo Excel e retorna os dados formatados"""
    try:
        # Ler o arquivo Excel
        df = pd.read_excel(file_path)
        
        # Tentar encontrar colunas de nome (várias possibilidades)
        name_columns = ['Nome', 'NOME', 'nome', 'Funcionário', 'FUNCIONÁRIO', 'funcionario', 'Employee']
        location_columns = ['Local', 'LOCAL', 'Localização', 'LOCALIZAÇÃO', 'Locais', 'LOCAIS', 'Location']
        
        name_col = None
        location_col = None
        
        # Encontrar coluna de nomes
        for col in df.columns:
            if any(name_variant.lower() in col.lower() for name_variant in name_columns):
                name_col = col
                break
        
        # Encontrar coluna de locais
        for col in df.columns:
            if any(loc_variant.lower() in col.lower() for loc_variant in location_columns):
                location_col = col
                break
        
        if name_col is None:
            print(f"Coluna de nome não encontrada em {file_path}")
            return None, None
        
        # Extrair nomes dos funcionários
        employees = []
        for idx, row in df.iterrows():
            name = clean_name(row[name_col])
            if name and name not in ['NOME', 'Nome', 'nome']:  # Filtrar cabeçalhos
                employees.append(name)
        
        # Extrair locais (usar o primeiro valor não nulo se existir)
        locations = "Diversos locais"  # Padrão
        if location_col:
            unique_locations = []
            for idx, row in df.iterrows():
                loc = clean_location(row[location_col])
                if loc and loc not in ['LOCAL', 'Local', 'local', 'LOCALIZAÇÃO']:
                    unique_locations.append(loc)
            
            if unique_locations:
                # Remover duplicatas mantendo ordem
                seen = set()
                unique_locs = []
                for loc in unique_locations:
                    if loc not in seen:
                        seen.add(loc)
                        unique_locs.append(loc)
                locations = '/'.join(unique_locs[:10])  # Limitar a 10 locais
        
        return employees, locations
        
    except Exception as e:
        print(f"Erro ao processar {file_path}: {e}")
        return None, None

def generate_html_section(area_title, employees, locations):
    """Gera a seção HTML para uma área"""
    html = f'''
            <div class="area-section">
                <h2 class="area-title">{area_title}</h2>
                <div class="service-description">Serviços de {area_title.lower()}</div>
                <div class="locations-line">{locations}</div>
                <div class="employees-section">
                    <div class="employees-grid">
'''
    
    for idx, employee in enumerate(employees, 1):
        html += f'''                        
                        <div class="employee-item">
                            <div class="employee-number">#{idx}</div>
                            <div class="employee-name">{employee}</div>
                        </div>'''
    
    html += '''
                    </div>
                </div>
            </div>
'''
    return html

def main():
    # Mapeamento dos arquivos para títulos das áreas
    file_mapping = {
        'Bombeiro Civil.xlsx': 'Bombeiro Civil',
        'Serviço de copa.xlsx': 'Serviços de Copa',
        'Serviço de Limpeza nos prédios.xlsx': 'Serviços de Limpeza nos Prédios',
        'Serviço de locação de veículos.xlsx': 'Serviços de Locação de Veículos',
        'Serviço de recepção.xlsx': 'Serviços de Recepção',
        'Serviço de transporte do Gabinete.xlsx': 'Serviços de Transporte do Gabinete',
        'Serviço de vigilância eletrônica.xlsx': 'Serviços de Vigilância Eletrônica',
        'Serviço de vigilância patrimonial.xlsx': 'Serviços de Vigilância Patrimonial',
        'Serviços de manutenção de ar-condicionado.xlsx': 'Serviços de Manutenção de Ar-Condicionado'
    }
    
    current_dir = Path(__file__).parent
    all_html = ""
    
    print("Processando planilhas...")
    
    for filename, area_title in file_mapping.items():
        file_path = current_dir / filename
        
        if file_path.exists():
            print(f"Processando: {filename}")
            employees, locations = process_excel_file(file_path, area_title)
            
            if employees:
                html_section = generate_html_section(area_title, employees, locations)
                all_html += html_section
                print(f"  - {len(employees)} funcionários encontrados")
                print(f"  - Locais: {locations}")
            else:
                print(f"  - Nenhum funcionário encontrado")
        else:
            print(f"Arquivo não encontrado: {filename}")
    
    # Salvar o HTML gerado
    output_file = current_dir / "sections_generated.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(all_html)
    
    print(f"\nHTML gerado salvo em: {output_file}")
    print("Você pode copiar o conteúdo e colar no seu index.html")

if __name__ == "__main__":
    main()