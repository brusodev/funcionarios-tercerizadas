import openpyxl
import PyPDF2
import re

# Ler Excel
wb = openpyxl.load_workbook('ADM_736.xlsx')
ws = wb.active

linhas_excel = []
for i, row in enumerate(ws.iter_rows(values_only=True), 1):
    if i == 1:
        continue
    n = row[0]
    desc = row[1] if len(row) > 1 else ''
    if n and isinstance(n, (int, float)):
        linhas_excel.append({
            'n': int(n),
            'desc': desc,
            'linha': i
        })

# Ler PDF
pdf_nome = 'ADM 0800100_0736_2025 de 30_09_2025.PDF'
with open(pdf_nome, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for page in reader.pages:
        text += page.extract_text()

lines = text.split('\n')

linhas_pdf = []
for linha in lines:
    match = re.match(r'^(\d+,\d+)\s+un\s+(.+)$', linha)
    if match:
        qty_str = match.group(1).replace(',', '.')
        qtd = int(float(qty_str))
        description = match.group(2)
        linhas_pdf.append({
            'n': qtd,
            'desc': description
        })

print("="*150)
print("COMPARACAO: EXCEL vs PDF")
print("="*150 + "\n")

print(f"Excel: {len(linhas_excel)} linhas, {sum(l['n'] for l in linhas_excel):,} aparelhos")
print(f"PDF:   {len(linhas_pdf)} linhas, {sum(l['n'] for l in linhas_pdf):,} aparelhos")
print(f"\nDiferenca: {len(linhas_excel) - len(linhas_pdf)} linhas, {sum(l['n'] for l in linhas_excel) - sum(l['n'] for l in linhas_pdf):,} aparelhos\n")

# Encontrar linhas do Excel que NAO estao no PDF
print("LINHAS NO EXCEL MAS NAO NO PDF:\n")

for excel_linha in linhas_excel:
    encontrada = False
    for pdf_linha in linhas_pdf:
        if excel_linha['n'] == pdf_linha['n'] and excel_linha['desc'][:50] in pdf_linha['desc']:
            encontrada = True
            break
    
    if not encontrada:
        print(f"Linha {excel_linha['linha']}: {excel_linha['n']:>4} un - {excel_linha['desc'][:100]}")

print("\n" + "="*150 + "\n")
