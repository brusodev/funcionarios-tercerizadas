#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
import re
import json
import os
from collections import defaultdict

# Mapeamento de recintos por PDF
pdf_recinto_mapping = {
    'ADM 0800100_0733_2025 de 30_09_2025.PDF': 'Bauru',
    'ADM 0800100_0734_2025 de 30_09_2025.PDF': 'Araraquara',
    'ADM 0800100_0735_2025 de 30_09_2025.PDF': 'Araraquara',
    'ADM 0800100_0736_2025 de 30_09_2025.PDF': 'Araraquara',
    'ADM 0800100_0737_2025 de 30_09_2025.PDF': 'São José do Rio Preto',
    'ADM 0800100_0738_2025 de 30_09_2025.PDF': 'Araraquara',
    'ADM 0800100_0739_2025 de 30_09_2025.PDF': 'Araraquara',
    'ADM 0800100_0740_2025 de 30_09_2025.PDF': 'Araraquara',
    'ADM 0800100_0741_2025 de 30_09_2025.PDF': 'Araraquara',
    'ADM 0800100_0742_2025 de 30_09_2025.PDF': 'Araraquara',
    'ADM 0800100_0743_2025 de 30_09_2025.PDF': 'VIRACOPOS',  # Este PDF é APENAS VIRACOPOS
    'ADM 0800100_0744_2025 de 30_09_2025.PDF': 'São Paulo',
    'ADM 0800100_0745_2025 de 30_09_2025.PDF': 'São Paulo',
    'ADM 0800100_0746_2025 de 30_09_2025.PDF': 'São Paulo',
    'ADM 0800100_0747_2025 de 30092025.PDF': 'Bauru',
}

def extract_viracopos_data(text):
    """Extrai dados da seção VIRACOPOS do PDF 0743"""
    lines = text.split('\n')
    
    capturing = False
    viracopos_section = []
    device_count = 0
    total_value = 0
    
    for i, line in enumerate(lines):
        # Começa quando encontra AEROPORTO INTERNACIONAL DE VIRACOPOS
        if 'AEROPORTO INTERNACIONAL DE VIRACOPOS' in line and 'Unidade:' in line:
            capturing = True
            continue
        
        # Para quando encontra outra unidade
        if capturing and ('Unidade:' in line and 'AEROPORTO' not in line):
            break
        
        if capturing:
            viracopos_section.append(line)
    
    # Contar aparelhos
    for line in viracopos_section:
        if re.match(r'^\d+,\d+\s+un\s+', line):
            qty_match = re.match(r'^(\d+,\d+)\s+un', line)
            if qty_match:
                qty_str = qty_match.group(1).replace(',', '.')
                qty = int(float(qty_str))
                device_count += qty
    
    # Procurar pelo total desta unidade
    for i, line in enumerate(viracopos_section):
        if 'Total da Unidade:' in line or 'TOTAL UNIDADE' in line:
            valor_match = re.search(r'R\$\s*([\d.]+,\d+)', line)
            if valor_match:
                valor_str = valor_match.group(1).replace('.', '').replace(',', '.')
                total_value = float(valor_str)
                break
    
    # Se não encontrou o total, procurar próxima linha
    if total_value == 0:
        for i, line in enumerate(viracopos_section):
            if 'Total da Unidade' in line:
                if i + 1 < len(viracopos_section):
                    next_line = viracopos_section[i + 1]
                    valor_match = re.search(r'([\d.]+,\d+)', next_line)
                    if valor_match:
                        valor_str = valor_match.group(1).replace('.', '').replace(',', '.')
                        total_value = float(valor_str)
                        break
    
    return device_count, total_value

def get_pdf_data(pdf_file):
    """Extrai dados do PDF"""
    try:
        with open(pdf_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        
        # Extrair Total do ADM
        adm_match = re.search(r'Total\s+do\s+ADM\s*:\s*R\$\s*([\d.]+,\d+)', text)
        if not adm_match:
            return None
        
        valor_str = adm_match.group(1).replace('.', '').replace(',', '.')
        total_valor = float(valor_str)
        
        # Contar aparelhos
        device_count = 0
        for line in text.split('\n'):
            if re.match(r'^(\d+,\d+)\s+un\s+', line):
                qty_match = re.match(r'^(\d+,\d+)\s+un', line)
                if qty_match:
                    qty_str = qty_match.group(1).replace(',', '.')
                    qty = int(float(qty_str))
                    device_count += qty
        
        return {
            'total_aparelhos': device_count,
            'total_valor': total_valor
        }
    
    except Exception as e:
        print(f'Erro ao processar {pdf_file}: {e}')
        return None

# Mapeamento de descrições de recintos
recinto_descriptions = {
    'Araraquara': 'Regional DMA - Araraquara',
    'São Paulo': 'DMA Ipiranga',
    'Bauru': 'Depósito DINAMO INTER-AGRICOLA LTDA',
    'São José do Rio Preto': 'SAPOL São José do Rio Preto',
    'VIRACOPOS': 'Aeroporto Internacional de Viracopos - ABV'
}

# Processar todos os PDFs
recintos_data = defaultdict(lambda: {
    'descricao': '',
    'quantidade': 0,
    'valor_total': 0.0,
    'pdfs': [],
    'pdf_detalhes': {}
})

pdf_files = sorted([f for f in os.listdir('.') if f.endswith('.PDF')])

print("\n" + "="*100)
print("RELATORIO FINAL - COM TODOS OS RECINTOS")
print("="*100 + "\n")
print(f"{'PDF':<50} {'Aparelhos':>12} {'Valor Total':>20} {'Recinto':<25}")
print("-"*110)

total_aparelhos_geral = 0
total_valor_geral = 0.0

for pdf_file in pdf_files:
    data = get_pdf_data(pdf_file)
    
    if data is None:
        continue
    
    pdf_nome = pdf_file.replace(' de 30_09_2025.PDF', '').replace(' de 30092025.PDF', '')
    
    # Obter recinto do mapeamento
    recinto = pdf_recinto_mapping.get(pdf_file, 'Desconhecido')
    
    recintos_data[recinto]['descricao'] = recinto_descriptions.get(recinto, '')
    recintos_data[recinto]['quantidade'] += data['total_aparelhos']
    recintos_data[recinto]['valor_total'] += data['total_valor']
    recintos_data[recinto]['pdfs'].append(pdf_nome)
    recintos_data[recinto]['pdf_detalhes'][pdf_nome] = {
        'quantidade': data['total_aparelhos'],
        'valor': data['total_valor']
    }
    
    print(f"{pdf_file:<50} {data['total_aparelhos']:>12,} R$ {data['total_valor']:>17,.2f}  {recinto:<25}")
    
    total_aparelhos_geral += data['total_aparelhos']
    total_valor_geral += data['total_valor']

# Ordenar recintos por quantidade
recintos_ordenados = sorted(recintos_data.items(), key=lambda x: x[1]['quantidade'], reverse=True)

print("\n" + "="*100)
print("RESUMO FINAL POR RECINTO")
print("="*100 + "\n")
print(f"{'Recinto/Depósito':<40} {'Aparelhos':>15} {'Valor Total':>20}")
print("-"*80)

for recinto, data in recintos_ordenados:
    valor_fmt = f"R$ {data['valor_total']:,.2f}"
    print(f"{recinto:<40} {data['quantidade']:>15,} {valor_fmt:>20}")

print("-"*80)
valor_fmt = f"R$ {total_valor_geral:,.2f}"
print(f"{'TOTAL':<40} {total_aparelhos_geral:>15,} {valor_fmt:>20}")

# Salvar JSON
folder_path = os.path.dirname(os.path.abspath(__file__))
output_data = {}

for recinto, data in recintos_ordenados:
    output_data[recinto] = {
        'descricao': data['descricao'],
        'quantidade': data['quantidade'],
        'valor_total': round(data['valor_total'], 2),
        'num_pdfs': len(data['pdfs']),
        'pdfs': data['pdfs']
    }

json_path = os.path.join(folder_path, 'json', 'aparelhos_por_recinto_completo.json')
os.makedirs(os.path.dirname(json_path), exist_ok=True)

with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

# Salvar CSV
csv_path = os.path.join(folder_path, 'json', 'aparelhos_por_recinto_completo.csv')
with open(csv_path, 'w', encoding='utf-8') as f:
    f.write('Recinto/Depósito;Descrição;Quantidade;Valor Total;Número de PDFs;PDFs\n')
    for recinto, data in recintos_ordenados:
        valor_fmt = str(data['valor_total']).replace('.', ',')
        pdfs_str = '|'.join(data['pdfs'])
        f.write(f'{recinto};{data["descricao"]};{data["quantidade"]};{valor_fmt};{len(data["pdfs"])};{pdfs_str}\n')

print(f"\n\nTotal de Recintos/Depósitos: {len(recintos_ordenados)}")
print(f"Total de Aparelhos: {total_aparelhos_geral:,}")
print(f"Valor Total: R$ {total_valor_geral:,.2f}")

esperado_aparelhos = 32015
diferenca = total_aparelhos_geral - esperado_aparelhos
pct_diferenca = (diferenca / esperado_aparelhos * 100) if esperado_aparelhos > 0 else 0
print(f"\nResultado: {total_aparelhos_geral:,} aparelhos (diferenca: {diferenca:+d} = {pct_diferenca:+.2f}%)")

print(f"\nJSON salvo: {json_path}")
print(f"CSV salvo: {csv_path}")
