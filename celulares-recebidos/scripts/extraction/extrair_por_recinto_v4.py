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

def count_devices(text):
    """Count devices from extracted text"""
    # Pattern for device lines: 1,00 un SMARTPHONE/CELULAR/IPHONE etc.
    patterns = [
        r'^(\d+,\d+)\s+un\s+(SMARTPHONE|TELEFONE\s+CELULAR|APARELHO)\s+(.+?)(?:\n|$)',
        r'^(\d+,\d+)\s+un\s+(IPHONE)\s+(.+?)(?:\n|$)',
        r'^(\d+,\d+)\s+un\s+(CELULAR)\s+(.+?)(?:\n|$)',
    ]
    
    devices = []
    for pattern in patterns:
        for match in re.finditer(pattern, text, re.MULTILINE):
            qty = float(match.group(1).replace(',', '.'))
            device_type = match.group(2)
            rest = match.group(3)
            
            # Extract model and price
            if '///' in rest:
                parts = rest.split('///')
                modelo = parts[0].strip()
                valor_str = parts[1].strip() if len(parts) > 1 else "0"
            else:
                modelo = rest
                valor_str = "0"
            
            # Clean up valor
            valor_str = valor_str.replace('R$', '').replace('\n', '').strip()
            if not valor_str or valor_str == '':
                valor_str = "0"
            
            try:
                valor = float(valor_str.replace(',', '.'))
            except:
                valor = 0
            
            devices.append({
                'quantidade': qty,
                'tipo': device_type,
                'modelo': modelo,
                'valor': valor,
                'valor_total': qty * valor
            })
    
    return devices

def extract_recintos_and_unidades(text, pdf_name):
    """
    Extract both Unidades (main) and Recintos (nested)
    Structure:
    XXXXX - CITY Unidade:
      ...devices...
      16 - 810900 Regional DMA - ARARAQUARA/SP
      ...devices for araraquara...
    """
    
    result = defaultdict(lambda: {
        'quantidade': 0,
        'valor_total': 0.0,
        'itens': 0,
        'pdfs': set()
    })
    
    # First, find main Unidades
    pattern_unidade = r'(\d{7})\s*-\s*([A-ZÁ-Ú\s/]+?)\s+Unidade:'
    
    lines = text.split('\n')
    
    current_unidade = None
    current_recinto = None
    unidade_start = None
    recinto_start = None
    
    for idx, line in enumerate(lines):
        # Check for Unidade header
        unidade_match = re.match(pattern_unidade, line)
        if unidade_match:
            current_unidade = f"{unidade_match.group(1)} - {unidade_match.group(2).strip()}"
            current_recinto = None
            unidade_start = idx
            continue
        
        # Check for nested Recinto (format: "16 - 810900 Regional DMA - City/SP")
        # This appears as a header within a Unidade section
        recinto_match = re.match(r'(\d+)\s*-\s*(\d{6})\s+Regional DMA\s*-\s*([A-ZÁ-Ú\s/]+)/[A-Z]{2}', line)
        if recinto_match:
            recinto_code = recinto_match.group(2)
            recinto_name = recinto_match.group(3).strip()
            current_recinto = f"{recinto_code} - {recinto_name} (DMA)"
            recinto_start = idx
            continue
        
        # Check for device line
        device_patterns = [
            r'^(\d+,\d+)\s+un\s+(SMARTPHONE|TELEFONE\s+CELULAR|APARELHO|IPHONE|CELULAR)\s',
        ]
        
        is_device = False
        for pattern in device_patterns:
            if re.match(pattern, line):
                is_device = True
                break
        
        if is_device and (current_unidade or current_recinto):
            # Extract device info from this line
            try:
                parts = line.split()
                qty_str = parts[0]
                qty = float(qty_str.replace(',', '.'))
                
                # Extract value from line (usually at the end after ///)
                value_match = re.search(r'R\$\s*([\d.]+,\d+)', line)
                valor = 0
                if value_match:
                    valor_str = value_match.group(1)
                    valor = float(valor_str.replace('.', '').replace(',', '.'))
                
                # Determine key: use recinto if available, else unidade
                key = current_recinto if current_recinto else current_unidade
                
                if key:
                    result[key]['quantidade'] += int(qty)
                    result[key]['valor_total'] += qty * valor
                    result[key]['itens'] += 1
                    result[key]['pdfs'].add(pdf_name)
                    
            except Exception as e:
                pass
    
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
    
    print("=" * 80)
    print("EXTRATOR DE APARELHOS POR RECINTO/UNIDADE - V4")
    print("Incluindo recintos aninhados (nested recintos como Araraquara)")
    print("=" * 80)
    print()
    
    # Extract all recintos
    recintos_data = process_all_pdfs(folder_path)
    
    print()
    print("=" * 80)
    print("RESULTADOS DA EXTRACAOO")
    print("=" * 80)
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
    
    print(f"{'Recinto/Unidade':<55} {'Aparelhos':>10} {'Valor Total':>20}")
    print("-" * 85)
    
    for recinto, data in recintos_ordenados:
        total_aparelhos += data['quantidade']
        total_valor += data['valor_total']
        
        pdfs_list = sorted(list(data['pdfs']))
        valor_fmt = format_currency(data['valor_total'])
        
        print(f"{recinto:<55} {data['quantidade']:>10,} {valor_fmt:>20}")
        
        output_data[recinto] = {
            'quantidade': data['quantidade'],
            'valor_total': data['valor_total'],
            'itens': data['itens'],
            'pdfs': pdfs_list
        }
    
    print("-" * 85)
    total_valor_fmt = format_currency(total_valor)
    print(f"{'TOTAL':<55} {total_aparelhos:>10,} {total_valor_fmt:>20}")
    print()
    
    print(f"Total de Recintos/Unidades: {len(recintos_ordenados)}")
    print(f"Total de Aparelhos: {total_aparelhos:,}")
    print(f"Valor Total: {total_valor_fmt}")
    print()
    
    # Save to JSON
    json_path = os.path.join(folder_path, 'json', 'aparelhos_por_recinto_v4.json')
    os.makedirs(os.path.dirname(json_path), exist_ok=True)
    
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print(f"JSON salvo em: {json_path}")

if __name__ == '__main__':
    main()
