#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
import re
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

PDF_RECINTO_MAP = {
    '0733': 'Bauru',
    '0734': 'Araraquara',
    '0735': 'Araraquara',
    '0736': 'Araraquara',
    '0737': 'São José do Rio Preto',
    '0738': 'Araraquara',
    '0739': 'Araraquara',
    '0740': 'Araraquara',
    '0741': 'Araraquara',
    '0742': 'Araraquara',
    '0743': 'Araraquara',
    '0744': 'São Paulo',
    '0745': 'São Paulo',
    '0746': 'São Paulo',
    '0747': 'Bauru',
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

def find_duplicates(folder_path):
    """Find devices that appear multiple times"""
    
    all_devices = {}
    
    pdf_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.PDF')])
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        match = re.search(r'_(\d{4})_', pdf_file)
        if not match:
            continue
        
        pdf_num = match.group(1)
        if pdf_num not in PDF_RECINTO_MAP:
            continue
        
        recinto = PDF_RECINTO_MAP[pdf_num]
        text = extract_text_from_pdf(pdf_path)
        if not text:
            continue
        
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            # Match device lines
            device_match = re.match(r'^(\d+,\d+)\s+un\s+(SMARTPHONE|TELEFONE\s+CELULAR|APARELHO|IPHONE|CELULAR|TABLET|NOTE|REDMI|IPTV\s+BOX|RECEPTOR|SMART\s+TV|BOX)\s+(.+)$', line, re.IGNORECASE)
            
            if device_match:
                qty_str = device_match.group(1)
                device_type = device_match.group(2)
                description = device_match.group(3)
                
                # Extract value from line or next lines
                valor = 0.0
                for j in range(i, min(i+4, len(lines))):
                    value_match = re.search(r'R\$\s*([\d.]+,\d+)', lines[j])
                    if value_match:
                        valor_str = value_match.group(1)
                        valor = float(valor_str.replace('.', '').replace(',', '.'))
                        break
                
                # Create a unique key
                key = f"{description[:60]}|{device_type}"
                
                if key not in all_devices:
                    all_devices[key] = []
                
                all_devices[key].append({
                    'pdf': pdf_file,
                    'recinto': recinto,
                    'quantidade': float(qty_str.replace(',', '.')),
                    'tipo': device_type,
                    'descricao': description,
                    'valor': valor,
                    'linha': i
                })
    
    # Find potential duplicates
    duplicates = {k: v for k, v in all_devices.items() if len(v) > 1}
    
    return duplicates, all_devices

def main():
    folder_path = r"c:\Users\bruno.vargas\Desktop\PROJETOS\celulares-recebidos"
    
    print("=" * 100)
    print("INVESTIGACAO DE APARELHOS DUPLICADOS OU EXTRAS")
    print("=" * 100)
    print()
    
    duplicates, all_devices = find_duplicates(folder_path)
    
    if duplicates:
        print(f"Encontrados {len(duplicates)} tipos de dispositivos que aparecem em múltiplos PDFs:\n")
        
        total_duplicatas = 0
        for key, devices in sorted(duplicates.items()):
            if len(devices) > 1:
                print(f"Dispositivo: {key}")
                total_qty = sum(d['quantidade'] for d in devices)
                print(f"  Total: {total_qty} aparelhos em {len(devices)} PDFs diferentes")
                for dev in devices:
                    print(f"    - {dev['pdf']}: {dev['quantidade']} x R$ {dev['valor']}")
                total_duplicatas += total_qty
                print()
        
        print(f"Total de aparelhos em possíveis duplicatas: {total_duplicatas}")
    else:
        print("Nenhuma duplicata óbvia encontrada.")
    
    print()
    print("=" * 100)
    print("BUSCA POR LINHAS DUPLICADAS DENTRO DE MESMO PDF")
    print("=" * 100)
    print()
    
    # Check for exact duplicates within same PDF
    pdf_files = sorted([f for f in os.listdir(folder_path) if f.endswith('.PDF')])
    
    for pdf_file in pdf_files:
        pdf_path = os.path.join(folder_path, pdf_file)
        text = extract_text_from_pdf(pdf_path)
        if not text:
            continue
        
        lines = text.split('\n')
        device_lines = {}
        
        for i, line in enumerate(lines):
            device_match = re.match(r'^(\d+,\d+)\s+un\s+(SMARTPHONE|TELEFONE\s+CELULAR|APARELHO|IPHONE|CELULAR|TABLET|NOTE|REDMI|IPTV\s+BOX|RECEPTOR)\s+(.+)$', line, re.IGNORECASE)
            
            if device_match:
                key = line[:80]  # Use first 80 chars as key
                
                if key not in device_lines:
                    device_lines[key] = []
                
                device_lines[key].append(i)
        
        # Find duplicates
        for key, line_nums in device_lines.items():
            if len(line_nums) > 1:
                print(f"{pdf_file}:")
                print(f"  Linha duplicada encontrada em posições: {line_nums}")
                print(f"  Conteúdo: {key}")
                print()

if __name__ == '__main__':
    main()
