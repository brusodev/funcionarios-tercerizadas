#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
import re
import json
import os
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

# Mapeamento de PDFs para Recintos/Depósitos baseado na informação do usuário
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
    '0743': ('Araraquara', 'Regional DMA - Araraquara'),  # Também tem Viracopos, mas Araraquara é principal
    '0744': ('São Paulo', 'DMA Ipiranga'),
    '0745': ('São Paulo', 'DMA Ipiranga'),
    '0746': ('São Paulo', 'DMA Ipiranga'),
    '0747': ('Bauru', 'Depósito DINAMO INTER-AGRICOLA LTDA'),
}

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
    except Exception as e:
        print(f"Erro ao processar {pdf_path}: {e}")
        return ""

def count_devices_in_pdf(text):
    """Count all devices in PDF text"""
    patterns = [
        r'^(\d+,\d+)\s+un\s+(SMARTPHONE|TELEFONE\s+CELULAR|APARELHO|IPHONE|CELULAR)\s',
    ]
    
    devices = {
        'quantidade': 0,
        'valor_total': 0.0,
        'itens': 0
    }
    
    lines = text.split('\n')
    for line in lines:
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                try:
                    qty_str = match.group(1)
                    qty = float(qty_str.replace(',', '.'))
                    
                    # Extract value from line
                    value_match = re.search(r'R\$\s*([\d.]+,\d+)', line)
                    valor = 0.0
                    if value_match:
                        valor_str = value_match.group(1)
                        valor = float(valor_str.replace('.', '').replace(',', '.'))
                    
                    devices['quantidade'] += int(qty)
                    devices['valor_total'] += qty * valor
                    devices['itens'] += 1
                except:
                    pass
    
    return devices

def process_all_pdfs(folder_path):
    """Process all PDFs in the folder"""
    
    recintos_data = defaultdict(lambda: {
        'quantidade': 0,
        'valor_total': 0.0,
        'itens': 0,
        'pdfs': [],
        'descricao': ''
    })
    
    # Get all PDF files
    pdf_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.PDF')])
    
    print(f"Processando {len(pdf_files)} arquivos PDF...\n")
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        print(f"Processando: {pdf_file}...", end=" ", flush=True)
        
        # Extract PDF number from filename (e.g., "0733" from "ADM 0800100_0733_2025...")
        match = re.search(r'_(\d{4})_', pdf_file)
        if match:
            pdf_num = match.group(1)
        else:
            print(f"ERRO (não consegui extrair número)")
            continue
        
        # Get recinto mapping
        if pdf_num in PDF_RECINTO_MAP:
            recinto_name, recinto_desc = PDF_RECINTO_MAP[pdf_num]
        else:
            recinto_name = "Desconhecido"
            recinto_desc = "Não mapeado"
        
        # Extract devices from PDF
        text = extract_text_from_pdf(pdf_path)
        
        if text:
            devices = count_devices_in_pdf(text)
            
            if devices['quantidade'] > 0:
                # Add to recinto total
                key = recinto_name
                recintos_data[key]['quantidade'] += devices['quantidade']
                recintos_data[key]['valor_total'] += devices['valor_total']
                recintos_data[key]['itens'] += devices['itens']
                recintos_data[key]['pdfs'].append(pdf_file)
                recintos_data[key]['descricao'] = recinto_desc
                
                print(f"OK ({devices['quantidade']} aparelhos)")
            else:
                print(f"OK (0 aparelhos - possível erro na extração)")
        else:
            print("ERRO (não consegui extrair texto)")
    
    return recintos_data

def format_currency(value):
    """Format value as Brazilian currency"""
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def main():
    folder_path = r"c:\Users\bruno.vargas\Desktop\PROJETOS\celulares-recebidos"
    
    print("=" * 100)
    print("RELATORIO DE APARELHOS POR RECINTO/DEPOSITO")
    print("Baseado no mapeamento oficial de PDFs")
    print("=" * 100)
    print()
    
    # Extract all recintos
    recintos_data = process_all_pdfs(folder_path)
    
    print()
    print("=" * 100)
    print("RESUMO POR RECINTO")
    print("=" * 100)
    print()
    
    # Sort by quantidade (descending)
    recintos_ordenados = sorted(
        recintos_data.items(),
        key=lambda x: x[1]['quantidade'],
        reverse=True
    )
    
    total_aparelhos = 0
    total_valor = 0.0
    
    # Create output JSON
    output_data = {}
    
    print(f"{'Recinto/Depósito':<40} {'Aparelhos':>12} {'Valor Total':>20} {'PDFs':>3}")
    print("-" * 100)
    
    for recinto, data in recintos_ordenados:
        total_aparelhos += data['quantidade']
        total_valor += data['valor_total']
        
        valor_fmt = format_currency(data['valor_total'])
        num_pdfs = len(data['pdfs'])
        
        print(f"{recinto:<40} {data['quantidade']:>12,} {valor_fmt:>20} {num_pdfs:>3}")
        print(f"  Depósito: {data['descricao']}")
        print(f"  PDFs: {', '.join([os.path.basename(p) for p in data['pdfs']])}")
        print()
        
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
    
    print(f"Total de Recintos/Depósitos: {len(recintos_ordenados)}")
    print(f"Total de Aparelhos: {total_aparelhos:,}")
    print(f"Valor Total: {total_valor_fmt}")
    print()
    
    # Check if we got all expected devices
    if total_aparelhos == 32015:
        print("SUCESSO: Total confere com 32.015 aparelhos esperados!")
    else:
        print(f"Total de {total_aparelhos} aparelhos (esperado 32.015, diferenca de {32015 - total_aparelhos})")
    print()
    
    # Save to JSON
    json_path = os.path.join(folder_path, 'json', 'aparelhos_por_recinto_mapeado.json')
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"JSON salvo em: {json_path}")
    
    # Also create a simple CSV report
    csv_path = os.path.join(folder_path, 'json', 'aparelhos_por_recinto_mapeado.csv')
    with open(csv_path, 'w', encoding='utf-8') as f:
        f.write('Recinto/Depósito;Descrição;Quantidade;Valor Total;PDFs\n')
        for recinto, data in recintos_ordenados:
            valor_fmt = str(data['valor_total']).replace('.', ',')
            pdfs_str = '|'.join(data['pdfs'])
            f.write(f'{recinto};{data["descricao"]};{data["quantidade"]};{valor_fmt};{pdfs_str}\n')
    
    print(f"CSV salvo em: {csv_path}")

if __name__ == '__main__':
    main()
