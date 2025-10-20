#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
import re
import os
import sys
from collections import defaultdict

sys.stdout.reconfigure(encoding='utf-8')

# Mapeamento de PDFs para Recintos
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

def find_missing_devices(folder_path):
    """Find all devices with zero or missing values"""
    
    missing_devices = []
    
    pdf_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.PDF')])
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        
        # Extract PDF number
        match = re.search(r'_(\d{4})_', pdf_file)
        if not match:
            continue
        
        pdf_num = match.group(1)
        if pdf_num not in PDF_RECINTO_MAP:
            continue
        
        recinto_name, _ = PDF_RECINTO_MAP[pdf_num]
        
        # Extract text
        text = extract_text_from_pdf(pdf_path)
        if not text:
            continue
        
        lines = text.split('\n')
        
        # Look for patterns that might be devices without values
        # Pattern 1: Lines with "un SMARTPHONE/CELULAR" but NO "R$" value
        for i, line in enumerate(lines):
            # Match device lines
            device_match = re.match(r'^(\d+,\d+)\s+un\s+(SMARTPHONE|TELEFONE\s+CELULAR|APARELHO|IPHONE|CELULAR|TABLET|SET[\s-]?TOP)\s+(.+)$', line)
            
            if device_match:
                qty_str = device_match.group(1)
                device_type = device_match.group(2)
                description = device_match.group(3)
                
                # Check if this line or next lines have value
                value_found = False
                valor = 0.0
                value_line_idx = i
                
                # Check current line and next 3 lines for value
                for j in range(i, min(i+4, len(lines))):
                    value_match = re.search(r'R\$\s*([\d.]+,\d+)', lines[j])
                    if value_match:
                        valor_str = value_match.group(1)
                        valor = float(valor_str.replace('.', '').replace(',', '.'))
                        value_found = True
                        value_line_idx = j
                        break
                
                # If no value found, it's a missing device
                if not value_found or valor == 0:
                    qty = float(qty_str.replace(',', '.'))
                    missing_devices.append({
                        'pdf': pdf_file,
                        'recinto': recinto_name,
                        'quantidade': int(qty),
                        'tipo': device_type,
                        'descricao': description[:100],
                        'valor': valor,
                        'linha': i,
                        'linha_texto': line[:100]
                    })
    
    return missing_devices

def find_zero_value_devices(folder_path):
    """Find all device lines and check for missing R$ values"""
    
    zero_devices = []
    total_devices_parsed = 0
    devices_with_zero_value = 0
    
    pdf_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.PDF')])
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        
        # Extract PDF number
        match = re.search(r'_(\d{4})_', pdf_file)
        if not match:
            continue
        
        pdf_num = match.group(1)
        if pdf_num not in PDF_RECINTO_MAP:
            continue
        
        recinto_name, _ = PDF_RECINTO_MAP[pdf_num]
        
        # Extract text
        text = extract_text_from_pdf(pdf_path)
        if not text:
            continue
        
        lines = text.split('\n')
        
        # Find all device lines
        for i, line in enumerate(lines):
            device_match = re.match(r'^(\d+,\d+)\s+un\s+(SMARTPHONE|TELEFONE\s+CELULAR|APARELHO|IPHONE|CELULAR|TABLET|SET[\s-]?TOP)\s+(.+)$', line)
            
            if device_match:
                total_devices_parsed += 1
                qty_str = device_match.group(1)
                device_type = device_match.group(2)
                description = device_match.group(3)
                qty = float(qty_str.replace(',', '.'))
                
                # Look for R$ value in this line
                value_match = re.search(r'R\$\s*([\d.]+,\d+)', line)
                
                if not value_match:
                    # Value not on this line, check next lines
                    valor = 0.0
                    found_in_next = False
                    
                    for j in range(i+1, min(i+5, len(lines))):
                        next_value = re.search(r'R\$\s*([\d.]+,\d+)', lines[j])
                        if next_value:
                            valor_str = next_value.group(1)
                            valor = float(valor_str.replace('.', '').replace(',', '.'))
                            found_in_next = True
                            break
                    
                    if not found_in_next or valor == 0:
                        devices_with_zero_value += int(qty)
                        zero_devices.append({
                            'pdf': pdf_file,
                            'pdf_num': pdf_num,
                            'recinto': recinto_name,
                            'quantidade': int(qty),
                            'tipo': device_type,
                            'descricao': description[:80],
                            'valor': valor,
                            'linha': i
                        })
    
    return zero_devices, total_devices_parsed, devices_with_zero_value

def main():
    folder_path = r"c:\Users\bruno.vargas\Desktop\PROJETOS\celulares-recebidos"
    
    print("=" * 100)
    print("INVESTIGACAO DOS 32 APARELHOS FALTANTES")
    print("=" * 100)
    print()
    
    # Find zero value devices
    print("Buscando dispositivos com valores zerados ou ausentes...\n")
    zero_devices, total_parsed, devices_with_zero = find_zero_value_devices(folder_path)
    
    print(f"Total de linhas de dispositivos analisadas: {total_parsed}")
    print(f"Total de aparelhos com valor ZERO/AUSENTE: {devices_with_zero}")
    print()
    
    if zero_devices:
        print("=" * 100)
        print("DETALHES DOS APARELHOS COM VALOR ZERO/AUSENTE:")
        print("=" * 100)
        print()
        
        # Group by PDF
        by_pdf = defaultdict(list)
        for dev in zero_devices:
            by_pdf[dev['pdf_num']].append(dev)
        
        total_faltantes = 0
        
        for pdf_num in sorted(by_pdf.keys()):
            devices = by_pdf[pdf_num]
            pdf_file = devices[0]['pdf']
            recinto = devices[0]['recinto']
            qty_in_pdf = sum(d['quantidade'] for d in devices)
            
            print(f"PDF {pdf_num} ({os.path.basename(pdf_file)})")
            print(f"  Recinto: {recinto}")
            print(f"  Aparelhos com valor zero: {qty_in_pdf}")
            print(f"  Detalhes:")
            
            for dev in devices[:10]:  # Show first 10
                print(f"    - {dev['quantidade']} x {dev['tipo']}: {dev['descricao'][:60]}")
            
            if len(devices) > 10:
                print(f"    ... e mais {len(devices) - 10} linhas")
            
            print()
            total_faltantes += qty_in_pdf
        
        print(f"Total de aparelhos encontrados com valor ZERO: {total_faltantes}")
    else:
        print("Nenhum dispositivo com valor zero encontrado.")
    
    print()
    print("=" * 100)
    print("BUSCANDO OUTROS FORMATOS DE DISPOSITIVOS")
    print("=" * 100)
    print()
    
    # Search for other patterns that might be devices
    folder_path = r"c:\Users\bruno.vargas\Desktop\PROJETOS\celulares-recebidos"
    pdf_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.PDF')])
    
    other_patterns_found = []
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        match = re.search(r'_(\d{4})_', pdf_file)
        if not match:
            continue
        
        pdf_num = match.group(1)
        if pdf_num not in PDF_RECINTO_MAP:
            continue
        
        text = extract_text_from_pdf(pdf_path)
        if not text:
            continue
        
        lines = text.split('\n')
        
        # Search for lines with "un " but maybe not standard devices
        for i, line in enumerate(lines):
            # Look for quantity patterns even if not standard device type
            if re.match(r'^\d+,\d+\s+un\s+', line) and 'SMARTPHONE' not in line and 'CELULAR' not in line and 'IPHONE' not in line and 'APARELHO' not in line:
                other_patterns_found.append({
                    'pdf': pdf_file,
                    'linha': i,
                    'texto': line[:100]
                })
    
    if other_patterns_found:
        print(f"Encontrados {len(other_patterns_found)} padrões alternativos:")
        for item in other_patterns_found[:20]:
            print(f"  {item['pdf']}: {item['texto']}")
        if len(other_patterns_found) > 20:
            print(f"  ... e mais {len(other_patterns_found) - 20}")
    else:
        print("Nenhum padrão alternativo encontrado.")

if __name__ == '__main__':
    main()
