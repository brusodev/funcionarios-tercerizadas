#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
import re
import json
import os
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

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

def extract_recintos_and_unidades(text, pdf_name):
    """
    Extract both Unidades (main) and Recintos (nested including Araraquara)
    """
    
    result = defaultdict(lambda: {
        'quantidade': 0,
        'valor_total': 0.0,
        'itens': 0,
        'pdfs': set()
    })
    
    lines = text.split('\n')
    
    current_unidade = None
    current_recinto = None
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Pattern 1: Main Unidade (XXXXX - CITY Unidade:)
        unidade_match = re.match(r'(\d{7})\s*-\s*([A-ZÁ-Ú\s/]+?)\s+Unidade:', line)
        if unidade_match:
            current_unidade = f"{unidade_match.group(1)} - {unidade_match.group(2).strip()}"
            current_recinto = None
            i += 1
            continue
        
        # Pattern 2: Nested Recinto - Araraquara and similar
        # This uses a more flexible pattern that matches the actual PDF format
        recinto_match = re.search(r'(\d+)\s*-\s*(\d{6})\s+Regional\s+DMA\s*-\s*([A-ZÁ-Ú\s/]+)/[A-Z]{2}', line)
        if recinto_match:
            recinto_code = recinto_match.group(2)
            recinto_name = recinto_match.group(3).strip()
            current_recinto = f"{recinto_code} - {recinto_name} (DMA)"
            i += 1
            continue
        
        # Check for device line (quantity un DEVICE_TYPE ...)
        device_match = re.match(r'^(\d+,\d+)\s+un\s+(SMARTPHONE|TELEFONE\s+CELULAR|APARELHO|IPHONE|CELULAR)\s', line)
        
        if device_match and (current_unidade or current_recinto):
            try:
                # Parse quantity
                qty_str = device_match.group(1)
                qty = float(qty_str.replace(',', '.'))
                
                # Extract value from line
                value_match = re.search(r'R\$\s*([\d.]+,\d+)', line)
                valor = 0.0
                if value_match:
                    valor_str = value_match.group(1)
                    valor = float(valor_str.replace('.', '').replace(',', '.'))
                
                # Determine target: nested recinto takes priority
                key = current_recinto if current_recinto else current_unidade
                
                if key:
                    result[key]['quantidade'] += int(qty)
                    result[key]['valor_total'] += qty * valor
                    result[key]['itens'] += 1
                    result[key]['pdfs'].add(pdf_name)
                    
            except Exception as e:
                pass
        
        i += 1
    
    return result

def process_all_pdfs(folder_path):
    """Process all PDFs in the folder"""
    
    all_devices = defaultdict(lambda: {
        'quantidade': 0,
        'valor_total': 0.0,
        'itens': 0,
        'pdfs': set()
    })
    
    # Get all PDF files
    pdf_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.PDF')])
    
    print(f"Processando {len(pdf_files)} arquivos PDF...\n")
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        print(f"Processando: {pdf_file}...", end=" ", flush=True)
        
        text = extract_text_from_pdf(pdf_path)
        
        if text:
            recintos = extract_recintos_and_unidades(text, pdf_file)
            
            for recinto_key, data in recintos.items():
                all_devices[recinto_key]['quantidade'] += data['quantidade']
                all_devices[recinto_key]['valor_total'] += data['valor_total']
                all_devices[recinto_key]['itens'] += data['itens']
                all_devices[recinto_key]['pdfs'].update(data['pdfs'])
            
            print(f"OK")
        else:
            print("ERRO")
    
    return all_devices

def format_currency(value):
    """Format value as Brazilian currency"""
    return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

def main():
    folder_path = r"c:\Users\bruno.vargas\Desktop\PROJETOS\celulares-recebidos"
    
    print("=" * 90)
    print("EXTRATOR DE APARELHOS POR RECINTO/UNIDADE - V6")
    print("Pattern melhorado para capturar Araraquara e outros recintos aninhados")
    print("=" * 90)
    print()
    
    # Extract all recintos
    recintos_data = process_all_pdfs(folder_path)
    
    print()
    print("=" * 90)
    print("RESULTADOS")
    print("=" * 90)
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
    
    print(f"{'Recinto/Unidade':<60} {'Aparelhos':>10} {'Valor Total':>20}")
    print("-" * 90)
    
    for recinto, data in recintos_ordenados:
        total_aparelhos += data['quantidade']
        total_valor += data['valor_total']
        
        pdfs_list = sorted(list(data['pdfs']))
        valor_fmt = format_currency(data['valor_total'])
        
        print(f"{recinto:<60} {data['quantidade']:>10,} {valor_fmt:>20}")
        
        output_data[recinto] = {
            'quantidade': data['quantidade'],
            'valor_total': data['valor_total'],
            'itens': data['itens'],
            'pdfs': pdfs_list
        }
    
    print("-" * 90)
    total_valor_fmt = format_currency(total_valor)
    print(f"{'TOTAL':<60} {total_aparelhos:>10,} {total_valor_fmt:>20}")
    print()
    
    print(f"Total de Recintos/Unidades: {len(recintos_ordenados)}")
    print(f"Total de Aparelhos: {total_aparelhos:,}")
    print(f"Valor Total: {total_valor_fmt}")
    print()
    
    # Save to JSON
    json_path = os.path.join(folder_path, 'json', 'aparelhos_por_recinto_v6.json')
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"JSON salvo em: {json_path}")

if __name__ == '__main__':
    main()
