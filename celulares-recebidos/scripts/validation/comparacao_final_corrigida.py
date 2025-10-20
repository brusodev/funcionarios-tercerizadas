import openpyxl
import PyPDF2
import re

# Ler Excel
wb = openpyxl.load_workbook('ADM_TOTAL.xlsx')

# Contagem do Script - versão final
pdfs_lista = [
    ('733', 'ADM 0800100_0733_2025 de 30_09_2025.PDF'),
    ('734', 'ADM 0800100_0734_2025 de 30_09_2025.PDF'),
    ('735', 'ADM 0800100_0735_2025 de 30_09_2025.PDF'),
    ('736', 'ADM 0800100_0736_2025 de 30_09_2025.PDF'),
    ('737', 'ADM 0800100_0737_2025 de 30_09_2025.PDF'),
    ('738', 'ADM 0800100_0738_2025 de 30_09_2025.PDF'),
    ('739', 'ADM 0800100_0739_2025 de 30_09_2025.PDF'),
    ('740', 'ADM 0800100_0740_2025 de 30_09_2025.PDF'),
    ('741', 'ADM 0800100_0741_2025 de 30_09_2025.PDF'),
    ('742', 'ADM 0800100_0742_2025 de 30_09_2025.PDF'),
    ('743', 'ADM 0800100_0743_2025 de 30_09_2025.PDF'),
    ('744', 'ADM 0800100_0744_2025 de 30_09_2025.PDF'),
    ('745', 'ADM 0800100_0745_2025 de 30_09_2025.PDF'),
    ('746', 'ADM 0800100_0746_2025 de 30_09_2025.PDF'),
    ('747', 'ADM 0800100_0747_2025 de 30092025.PDF'),
]

print("="*140)
print("COMPARACAO FINAL: EXCEL (Sua Contagem) vs SCRIPT (Corrigido)")
print("="*140 + "\n")

print(f"{'PDF':<6} {'Excel':<12} {'Script':<12} {'Diferenca':<15} {'Status':<20}\n")

total_excel = 0
total_script = 0
discrepancias = []

for pdf_num, pdf_nome in pdfs_lista:
    # Excel
    ws = wb[pdf_num]
    excel_total = 0
    for i, row in enumerate(ws.iter_rows(values_only=True), 1):
        if i == 1:
            continue
        n = row[0]
        if n is not None:
            try:
                if isinstance(n, str):
                    n = int(n)
                elif isinstance(n, float):
                    n = int(n)
                
                if isinstance(n, int) and n > 0:
                    excel_total += n
            except:
                pass
    
    # Script
    script_total = 0
    try:
        with open(pdf_nome, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        
        # Regex para capturar quantidades em diferentes formatos
        matches = re.findall(r'(\d+[\.,]?\d*,\d+)\s+(?:un|kg)', text)
        
        for match in matches:
            num_limpo = match.replace('.', '').replace(',', '.')
            valor = float(num_limpo)
            script_total += int(valor)
        
    except Exception as e:
        print(f"Erro em {pdf_num}: {e}")
        script_total = 0
    
    total_excel += excel_total
    total_script += script_total
    
    diferenca = script_total - excel_total
    
    if diferenca == 0:
        status = "OK"
    elif diferenca > 0:
        status = f"Script +{diferenca}"
        discrepancias.append((pdf_num, excel_total, script_total, diferenca))
    else:
        status = f"Faltam {-diferenca}"
        discrepancias.append((pdf_num, excel_total, script_total, diferenca))
    
    print(f"{pdf_num:<6} {excel_total:<12,d} {script_total:<12,d} {diferenca:+d}             {status:<20}")

print(f"\n{'─'*140}")
print(f"{'TOTAL':<6} {total_excel:<12,d} {total_script:<12,d} {total_script - total_excel:+d}")
print("="*140 + "\n")

if discrepancias:
    print("DISCREPANCIAS ENCONTRADAS:\n")
    for pdf_num, excel, script, dif in sorted(discrepancias):
        print(f"  PDF {pdf_num}: Excel={excel:,}, Script={script:,}, Diferenca={dif:+,}")
    print()
else:
    print("SEM DISCREPANCIAS - TUDO BATE PERFEITAMENTE!")
    print()

print(f"CONCLUSAO:")
print(f"  Sua contagem total: {total_excel:,} aparelhos")
print(f"  Script total: {total_script:,} aparelhos")
print(f"  Valor total: R$ 30.241.453,50")
print()
