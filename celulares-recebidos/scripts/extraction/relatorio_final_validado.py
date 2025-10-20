#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
import re
import json
import os
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

PDF_RECINTO_MAP = {
    '0733': ('Bauru', 'Depósito DINAMO INTER-AGRICOLA LTDA'),
    '0734': ('Araraquara', 'Regional DMA - Araraquara'),
    '0735': ('Araraquara', 'Regional DMA - Araraquara'),
    '0736': ('Araraquara', 'Regional DMA - Araraquara'),
    '0737': ('São José do Rio Preto', 'SAPOL São José do Rio Preto'),
    '0738': ('Araraquara', 'Regional DMA - Araraquara'),
    '0739': ('Araraquara', 'Regional DMA - Araraquara'),
    '0740': ('Araraquara', 'Regional DMA - Araraquara'),
    '0741': ('Araraquara', 'Regional DMA - Araraquara'),
    '0742': ('Araraquara', 'Regional DMA - Araraquara'),
    '0743': ('Araraquara', 'Regional DMA - Araraquara'),
    '0744': ('São Paulo', 'DMA Ipiranga'),
    '0745': ('São Paulo', 'DMA Ipiranga'),
    '0746': ('São Paulo', 'DMA Ipiranga'),
    '0747': ('Bauru', 'Depósito DINAMO INTER-AGRICOLA LTDA'),
}

def extract_text_from_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
    except:
        return ""

def get_pdf_total_from_adm(text):
    """Extract the 'Total do ADM' value from PDF text"""
    match = re.search(r'Total\s+do\s+ADM\s*:\s*R\$\s*([\d.]+,\d+)', text, re.IGNORECASE)
    if match:
        valor_str = match.group(1)
        return float(valor_str.replace('.', '').replace(',', '.'))
    return None

def count_devices_in_pdf_complete(text):
    """Count ALL devices with better accuracy"""
    
    patterns = [
        r'^(\d+,\d+)\s+un\s+(SMARTPHONE|TELEFONE\s+CELULAR|APARELHO|IPHONE|CELULAR|TABLET|NOTE|REDMI|IPTV\s+BOX|RECEPTOR|SMART\s+TV|BOX)\s+(.+)$',
    ]
    
    devices = {
        'quantidade': 0,
        'valor_total': 0.0,
        'itens': 0,
        'detalhes': []
    }
    
    lines = text.split('\n')
    
    # Track line indices we've already processed to avoid double-counting
    processed_lines = set()
    
    for i, line in enumerate(lines):
        if i in processed_lines:
            continue
        
        for pattern in patterns:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                try:
                    qty_str = match.group(1)
                    qty = float(qty_str.replace(',', '.'))
                    device_type = match.group(2)
                    description = match.group(3) if len(match.groups()) >= 3 else ""
                    
                    valor = 0.0
                    found_value = False
                    value_line_idx = -1
                    
                    # Check current line for value
                    value_match = re.search(r'R\$\s*([\d.]+,\d+)', line)
                    if value_match:
                        valor_str = value_match.group(1)
                        valor = float(valor_str.replace('.', '').replace(',', '.'))
                        found_value = True
                        value_line_idx = i
                    
                    # Check next lines if not found
                    if not found_value:
                        for j in range(i+1, min(i+4, len(lines))):
                            next_match = re.search(r'R\$\s*([\d.]+,\d+)', lines[j])
                            if next_match:
                                valor_str = next_match.group(1)
                                valor = float(valor_str.replace('.', '').replace(',', '.'))
                                found_value = True
                                value_line_idx = j
                                break
                    
                    # Add to count
                    devices['quantidade'] += int(qty)
                    devices['valor_total'] += qty * valor
                    devices['itens'] += 1
                    
                    # Mark lines as processed
                    processed_lines.add(i)
                    if value_line_idx >= 0 and value_line_idx != i:
                        processed_lines.add(value_line_idx)
                    
                    devices['detalhes'].append({
                        'quantidade': int(qty),
                        'tipo': device_type,
                        'descricao': description[:80],
                        'valor': valor,
                        'valor_total': qty * valor
                    })
                    
                    break  # Only match first pattern that succeeds
                    
                except Exception as e:
                    pass
    
    return devices

def process_all_pdfs_com_validacao(folder_path):
    """Process all PDFs with validation against Total do ADM"""
    
    recintos_data = defaultdict(lambda: {
        'quantidade': 0,
        'valor_total': 0.0,
        'itens': 0,
        'pdfs': [],
        'descricao': '',
        'detalhes_por_pdf': {},
        'validacao': []
    })
    
    pdf_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.PDF')])
    
    print(f"Processando {len(pdf_files)} arquivos PDF...\n")
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        
        match = re.search(r'_(\d{4})_', pdf_file)
        if match:
            pdf_num = match.group(1)
        else:
            continue
        
        if pdf_num not in PDF_RECINTO_MAP:
            continue
        
        recinto_name, recinto_desc = PDF_RECINTO_MAP[pdf_num]
        
        text = extract_text_from_pdf(pdf_path)
        if not text:
            continue
        
        devices = count_devices_in_pdf_complete(text)
        adm_total = get_pdf_total_from_adm(text)
        
        print(f"{pdf_file}:")
        print(f"  Aparelhos contados: {devices['quantidade']}")
        print(f"  Valor contado:      R$ {devices['valor_total']:,.2f}")
        
        if adm_total:
            print(f"  Total do ADM:       R$ {adm_total:,.2f}")
            diferenca_pct = abs(devices['valor_total'] - adm_total) / adm_total * 100 if adm_total > 0 else 0
            print(f"  Diferenca:          {diferenca_pct:.2f}%")
        
        print()
        
        if devices['quantidade'] > 0:
            key = recinto_name
            recintos_data[key]['quantidade'] += devices['quantidade']
            recintos_data[key]['valor_total'] += devices['valor_total']
            recintos_data[key]['itens'] += devices['itens']
            recintos_data[key]['pdfs'].append(pdf_file)
            recintos_data[key]['descricao'] = recinto_desc
            recintos_data[key]['detalhes_por_pdf'][pdf_file] = devices['detalhes']
            recintos_data[key]['validacao'].append({
                'pdf': pdf_file,
                'aparelhos_contados': devices['quantidade'],
                'valor_contado': devices['valor_total'],
                'valor_adm': adm_total
            })
    
    return recintos_data

def format_currency(value):
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def main():
    folder_path = r"c:\Users\bruno.vargas\Desktop\PROJETOS\celulares-recebidos"
    
    print("=" * 100)
    print("RELATORIO FINAL COM VALIDACAO CONTRA TOTAL DO ADM")
    print("=" * 100)
    print()
    
    recintos_data = process_all_pdfs_com_validacao(folder_path)
    
    print()
    print("=" * 100)
    print("RESUMO FINAL POR RECINTO")
    print("=" * 100)
    print()
    
    recintos_ordenados = sorted(
        recintos_data.items(),
        key=lambda x: x[1]['quantidade'],
        reverse=True
    )
    
    total_aparelhos = 0
    total_valor = 0.0
    
    output_data = {}
    
    print(f"{'Recinto/Depósito':<40} {'Aparelhos':>12} {'Valor Total':>20}")
    print("-" * 100)
    
    for recinto, data in recintos_ordenados:
        total_aparelhos += data['quantidade']
        total_valor += data['valor_total']
        
        valor_fmt = format_currency(data['valor_total'])
        print(f"{recinto:<40} {data['quantidade']:>12,} {valor_fmt:>20}")
        
        output_data[recinto] = {
            'descricao': data['descricao'],
            'quantidade': data['quantidade'],
            'valor_total': data['valor_total'],
            'itens': data['itens'],
            'pdfs': data['pdfs']
        }
    
    print("-" * 100)
    total_valor_fmt = format_currency(total_valor)
    print(f"{'TOTAL':<40} {total_aparelhos:>12,} {total_valor_fmt:>20}")
    print()
    
    print(f"Total de Aparelhos: {total_aparelhos:,}")
    print(f"Valor Total: {total_valor_fmt}")
    print()
    
    if total_aparelhos == 32015:
        print("SUCESSO: Total = 32.015 aparelhos!")
    else:
        diferenca = total_aparelhos - 32015
        print(f"Diferenca: {diferenca:+,} aparelhos (total: {total_aparelhos})")
    
    # Save JSON
    json_path = os.path.join(folder_path, 'json', 'aparelhos_por_recinto_FINAL.json')
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print()
    print(f"JSON salvo: {json_path}")
    
    # Save CSV
    csv_path = os.path.join(folder_path, 'json', 'aparelhos_por_recinto_FINAL.csv')
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write('Recinto/Depósito;Descrição;Quantidade;Valor Total;PDFs\n')
        for recinto, data in recintos_ordenados:
            valor_fmt = str(data['valor_total']).replace('.', ',')
            pdfs_str = '|'.join(data['pdfs'])
            f.write(f'{recinto};{data["descricao"]};{data["quantidade"]};{valor_fmt};{pdfs_str}\n')
    
    print(f"CSV salvo: {csv_path}")

if __name__ == '__main__':
    main()
