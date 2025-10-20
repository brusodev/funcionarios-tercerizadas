import PyPDF2
import re
from collections import defaultdict

# Sua contagem manual (fornecida anteriormente)
sua_contagem = {
    'ADM 0800100_0733_2025 de 30_09_2025.PDF': 13,
    'ADM 0800100_0734_2025 de 30_09_2025.PDF': 6879,
    'ADM 0800100_0735_2025 de 30_09_2025.PDF': 3804,
    'ADM 0800100_0736_2025 de 30_09_2025.PDF': 1873,
    'ADM 0800100_0737_2025 de 30_09_2025.PDF': 616,
    'ADM 0800100_0738_2025 de 30_09_2025.PDF': 442,
    'ADM 0800100_0739_2025 de 30_09_2025.PDF': 3708,
    'ADM 0800100_0740_2025 de 30_09_2025.PDF': 9,
    'ADM 0800100_0741_2025 de 30_09_2025.PDF': 19,
    'ADM 0800100_0742_2025 de 30_09_2025.PDF': 225,
    'ADM 0800100_0743_2025 de 30_09_2025.PDF': 912,
    'ADM 0800100_0744_2025 de 30_09_2025.PDF': 3457,
    'ADM 0800100_0745_2025 de 30_09_2025.PDF': 3390,
    'ADM 0800100_0746_2025 de 30_09_2025.PDF': 2544,
    'ADM 0800100_0747_2025 de 30092025.PDF': 4124,
}

pdf_files = list(sua_contagem.keys())

print("=== COMPARAÇÃO: SUA CONTAGEM vs SCRIPT ===\n")
print(f"{'PDF':<45} {'Você':>10} {'Script':>10} {'Diferença':>12} {'Status':>12}")
print("="*90)

total_sua = 0
total_script = 0
diferenca_total = 0
pdfs_com_diferenca = []

for pdf_file in pdf_files:
    try:
        with open(pdf_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        
        lines = text.split('\n')
        
        # Contar aparelhos (padrão: N,NN un)
        script_count = 0
        for linha in lines:
            match = re.match(r'^(\d+,\d+)\s+un\s+(.+)$', linha)
            if match:
                qty_str = match.group(1).replace(',', '.')
                qtd = int(float(qty_str))
                script_count += qtd
        
        sua_count = sua_contagem[pdf_file]
        diferenca = script_count - sua_count
        
        total_sua += sua_count
        total_script += script_count
        diferenca_total += diferenca
        
        if diferenca != 0:
            pdfs_com_diferenca.append((pdf_file, sua_count, script_count, diferenca))
            status = f"⚠️ +{diferenca}" if diferenca > 0 else f"❌ {diferenca}"
        else:
            status = "✅ OK"
        
        pdf_nome = pdf_file.split('_')[2] + '_' + pdf_file.split('_')[3][:1]
        print(f"{pdf_nome:<45} {sua_count:>10} {script_count:>10} {diferenca:>+12} {status:>12}")
    
    except FileNotFoundError:
        print(f"{pdf_file:<45} {'N/A':>10} {'ERRO':>10}")

print("="*90)
print(f"{'TOTAL':<45} {total_sua:>10} {total_script:>10} {diferenca_total:>+12}")

print("\n" + "="*90)
print("📊 RESUMO DAS DISCREPÂNCIAS:")
print("="*90 + "\n")

if pdfs_com_diferenca:
    for pdf_file, sua_count, script_count, diferenca in pdfs_com_diferenca:
        sinal = "+" if diferenca > 0 else ""
        print(f"🔴 {pdf_file.split('_')[2]}: {sinal}{diferenca} aparelhos (Você: {sua_count}, Script: {script_count})")
    
    print(f"\n📌 TOTAL DE DIFERENÇAS: {sum(abs(d[3]) for d in pdfs_com_diferenca):,} aparelhos")
else:
    print("✅ Todos os PDFs batem perfeitamente!")

print(f"\n🎯 DIFERENÇA FINAL: {diferenca_total:+} aparelhos")
print(f"   Sua contagem: {total_sua:,}")
print(f"   Script contagem: {total_script:,}")
