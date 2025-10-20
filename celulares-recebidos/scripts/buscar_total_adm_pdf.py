import PyPDF2
import re

# Ler o PDF 0745 original
pdf_path = "ADM 0800100_0745_2025 de 30_09_2025.PDF"

with open(pdf_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    texto_completo = []
    for page in reader.pages:
        texto_completo.append(page.extract_text())

texto = '\n'.join(texto_completo)

# Buscar "Total do ADM"
pattern_total_adm = re.compile(r'Total do ADM:\s*R\$\s*([\d.]+,\d{2})')
match = pattern_total_adm.search(texto)

print("="*80)
print("BUSCANDO 'Total do ADM' NO PDF ORIGINAL")
print("="*80)

if match:
    total_adm_str = match.group(1).replace('.', '').replace(',', '.')
    total_adm = float(total_adm_str)
    print(f"\n✓ ENCONTRADO!")
    print(f"Total do ADM: R$ {total_adm:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    # Buscar contexto (linhas antes e depois)
    linhas = texto.split('\n')
    for i, linha in enumerate(linhas):
        if 'Total do ADM:' in linha:
            print(f"\nContexto (linhas {max(0, i-2)} a {min(len(linhas), i+3)}):")
            for j in range(max(0, i-2), min(len(linhas), i+3)):
                marcador = ">>>" if j == i else "   "
                print(f"{marcador} Linha {j}: {linhas[j].strip()}")
else:
    print("\n⚠️ 'Total do ADM' NÃO encontrado no PDF")
    
    # Buscar variações
    print("\nBuscando variações...")
    variações = ['Total do ADM', 'TOTAL DO ADM', 'Total ADM', 'Total Geral', 'TOTAL GERAL']
    for var in variações:
        if var.lower() in texto.lower():
            print(f"  ✓ Encontrado: '{var}'")
            # Mostrar contexto
            idx = texto.lower().find(var.lower())
            print(f"    Contexto: ...{texto[max(0, idx-50):idx+100]}...")

# Buscar todos os Subtotais
print(f"\n{'='*80}")
print("SUBTOTAIS ENCONTRADOS:")
print("="*80)

pattern_subtotal = re.compile(r'Subtotal:\s*R\$\s*([\d.]+,\d{2})')
subtotais = pattern_subtotal.findall(texto)

print(f"\nTotal de Subtotais: {len(subtotais)}")
if subtotais:
    soma_subtotais = sum(float(s.replace('.', '').replace(',', '.')) for s in subtotais)
    print(f"Soma dos Subtotais: R$ {soma_subtotais:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    print(f"\nPrimeiros 5 Subtotais:")
    for i, sub in enumerate(subtotais[:5], 1):
        valor = float(sub.replace('.', '').replace(',', '.'))
        print(f"  {i}. R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    print(f"\nÚltimos 5 Subtotais:")
    for i, sub in enumerate(subtotais[-5:], len(subtotais)-4):
        valor = float(sub.replace('.', '').replace(',', '.'))
        print(f"  {i}. R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
