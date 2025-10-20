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

def get_pdf_totals(text):
    """Extract Total do ADM and count of devices"""
    
    # Get Total do ADM
    adm_match = re.search(r'Total\s+do\s+ADM\s*:\s*R\$\s*([\d.]+,\d+)', text, re.IGNORECASE)
    adm_total = 0
    if adm_match:
        valor_str = adm_match.group(1)
        adm_total = float(valor_str.replace('.', '').replace(',', '.'))
    
    # Count device lines by pattern
    device_count = 0
    patterns = [
        r'^(\d+,\d+)\s+un\s+(SMARTPHONE|TELEFONE\s+CELULAR|APARELHO|IPHONE|CELULAR|TABLET|NOTE|REDMI|IPTV\s+BOX|RECEPTOR|SMART\s+TV|BOX)\s',
    ]
    
    lines = text.split('\n')
    for line in lines:
        for pattern in patterns:
            if re.match(pattern, line, re.IGNORECASE):
                # Extract quantity
                qty_match = re.match(r'^(\d+,\d+)\s+un', line)
                if qty_match:
                    qty_str = qty_match.group(1)
                    qty = int(float(qty_str.replace(',', '.')))
                    device_count += qty
                break
    
    return {
        'total_valor': adm_total,
        'total_aparelhos': device_count
    }

def process_all_pdfs_usando_adm_total(folder_path):
    """Process all PDFs using ADM Total as source of truth"""
    
    recintos_data = defaultdict(lambda: {
        'quantidade': 0,
        'valor_total': 0.0,
        'pdfs': [],
        'descricao': ''
    })
    
    pdf_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.PDF')])
    
    print(f"Processando {len(pdf_files)} arquivos PDF...\n")
    print(f"{'PDF':<50} {'Aparelhos':>12} {'Valor Total':>20} {'Recinto':<20}")
    print("-" * 110)
    
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
        
        totals = get_pdf_totals(text)
        
        print(f"{pdf_file:<50} {totals['total_aparelhos']:>12,} R$ {totals['total_valor']:>17,.2f}  {recinto_name:<20}")
        
        if totals['total_aparelhos'] > 0:
            key = recinto_name
            recintos_data[key]['quantidade'] += totals['total_aparelhos']
            recintos_data[key]['valor_total'] += totals['total_valor']
            recintos_data[key]['pdfs'].append(pdf_file)
            recintos_data[key]['descricao'] = recinto_desc
    
    return recintos_data

def format_currency(value):
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def main():
    folder_path = r"c:\Users\bruno.vargas\Desktop\PROJETOS\celulares-recebidos"
    
    print("=" * 110)
    print("RELATORIO FINAL - USANDO TOTAL DO ADM COMO FONTE DA VERDADE")
    print("=" * 110)
    print()
    
    recintos_data = process_all_pdfs_usando_adm_total(folder_path)
    
    print()
    print("=" * 110)
    print("RESUMO FINAL POR RECINTO")
    print("=" * 110)
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
            'pdfs': data['pdfs']
        }
    
    print("-" * 100)
    total_valor_fmt = format_currency(total_valor)
    print(f"{'TOTAL':<40} {total_aparelhos:>12,} {total_valor_fmt:>20}")
    print()
    
    print(f"Total de Recintos/Depósitos: {len(recintos_ordenados)}")
    print(f"Total de Aparelhos: {total_aparelhos:,}")
    print(f"Valor Total: {total_valor_fmt}")
    print()
    
    if total_aparelhos == 32015:
        print("SUCESSO EXATO: Total = 32.015 aparelhos!")
    else:
        diferenca = total_aparelhos - 32015
        pct = (total_aparelhos / 32015 - 1) * 100
        print(f"Resultado: {total_aparelhos:,} aparelhos (diferenca: {diferenca:+,} = {pct:+.2f}%)")
    
    # Save JSON
    json_path = os.path.join(folder_path, 'json', 'aparelhos_por_recinto_exato.json')
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print()
    print(f"JSON salvo: {json_path}")
    
    # Save CSV
    csv_path = os.path.join(folder_path, 'json', 'aparelhos_por_recinto_exato.csv')
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write('Recinto/Depósito;Descrição;Quantidade;Valor Total;Número de PDFs;PDFs\n')
        for recinto, data in recintos_ordenados:
            valor_fmt = str(data['valor_total']).replace('.', ',')
            pdfs_str = '|'.join(data['pdfs'])
            f.write(f'{recinto};{data["descricao"]};{data["quantidade"]};{valor_fmt};{len(data["pdfs"])};{pdfs_str}\n')
    
    print(f"CSV salvo: {csv_path}")

if __name__ == '__main__':
    main()
