#!/usr/bin/env python
# -*- coding: utf-8 -*-

import PyPDF2
import re

pdf_path = r'c:\Users\bruno.vargas\Desktop\PROJETOS\celulares-recebidos\ADM 0800100_0739_2025 de 30_09_2025.PDF'

with open(pdf_path, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for page in reader.pages:
        text += page.extract_text() or ''

lines = text.split('\n')

current_unidade = None
current_recinto = None
araraquara_count = 0
sorocaba_count = 0

for i, line in enumerate(lines):
    # Pattern 1: Main Unidade
    unidade_match = re.match(r'(\d{7})\s*-\s*([A-ZÁ-Ú\s/]+?)\s+Unidade:', line)
    if unidade_match:
        current_unidade = f"{unidade_match.group(1)} - {unidade_match.group(2).strip()}"
        current_recinto = None
        print(f"Linha {i}: UNIDADE: {current_unidade}")
        continue
    
    # Pattern 2: Nested Recinto
    recinto_match = re.search(r'(\d+)\s*-\s*(\d{6})\s+Regional\s+DMA\s*-\s*([A-ZÁ-Ú\s/]+)/[A-Z]{2}', line)
    if recinto_match:
        recinto_code = recinto_match.group(2)
        recinto_name = recinto_match.group(3).strip()
        current_recinto = f"{recinto_code} - {recinto_name} (DMA)"
        print(f"Linha {i}: RECINTO: {current_recinto}")
        continue
    
    # Check for device line
    device_match = re.match(r'^(\d+,\d+)\s+un\s+(SMARTPHONE|TELEFONE\s+CELULAR|APARELHO|IPHONE|CELULAR)\s', line)
    
    if device_match and (current_unidade or current_recinto):
        try:
            qty_str = device_match.group(1)
            qty = float(qty_str.replace(',', '.'))
            
            # Find the value on this line or next lines
            value_match = re.search(r'R\$\s*([\d.]+,\d+)', line)
            valor = 0.0
            if value_match:
                valor_str = value_match.group(1)
                valor = float(valor_str.replace('.', '').replace(',', '.'))
            
            key = current_recinto if current_recinto else current_unidade
            
            if key and "Araraquara" in key:
                araraquara_count += int(qty)
                print(f"  Linha {i} ARARAQUARA: {qty} x {valor} = {qty * valor}")
            elif key and "SOROCABA" in key and "DMA" not in key:
                sorocaba_count += int(qty)
                if i < 6100:  # Only print first few to avoid spam
                    pass
                    
        except Exception as e:
            pass

print()
print(f"Total de aparelhos em ARARAQUARA (DMA): {araraquara_count}")
print(f"Total de aparelhos em SOROCABA (sem DMA): {sorocaba_count}")
