import PyPDF2
import re
from collections import defaultdict

print("="*120)
print("🔍 FERRAMENTA DE VERIFICAÇÃO PDF-POR-PDF")
print("="*120)
print("\nEste script irá contar todos os aparelhos em CADA PDF e comparar com suas contagens manuais.")
print("Insira a contagem manual de cada PDF para validação.\n")
print("="*120 + "\n")

# Lista de PDFs na ordem
pdfs_lista = [
    ('0733', 'ADM 0800100_0733_2025 de 30_09_2025.PDF'),
    ('0734', 'ADM 0800100_0734_2025 de 30_09_2025.PDF'),
    ('0740', 'ADM 0800100_0740_2025 de 30_09_2025.PDF'),
    ('0741', 'ADM 0800100_0741_2025 de 30_09_2025.PDF'),
    ('0742', 'ADM 0800100_0742_2025 de 30_09_2025.PDF'),
    ('0743', 'ADM 0800100_0743_2025 de 30_09_2025.PDF'),
    ('0744', 'ADM 0800100_0744_2025 de 30_09_2025.PDF'),
    ('0735', 'ADM 0800100_0735_2025 de 30_09_2025.PDF'),
    ('0736', 'ADM 0800100_0736_2025 de 30_09_2025.PDF'),
    ('0737', 'ADM 0800100_0737_2025 de 30_09_2025.PDF'),
    ('0738', 'ADM 0800100_0738_2025 de 30_09_2025.PDF'),
    ('0739', 'ADM 0800100_0739_2025 de 30_09_2025.PDF'),
    ('0745', 'ADM 0800100_0745_2025 de 30_09_2025.PDF'),
    ('0746', 'ADM 0800100_0746_2025 de 30_09_2025.PDF'),
    ('0747', 'ADM 0800100_0747_2025 de 30092025.PDF'),
]

# Contagens do usuário (de sua tabela)
contagens_usuario = {
    '0733': 13,
    '0734': 6879,
    '0740': 9,
    '0741': 19,
    '0742': 225,
    '0743': 912,
    '0744': 3457,
    '0735': 3804,
    '0736': 1873,
    '0737': 616,
    '0738': 442,
    '0739': 3708,
    '0745': 3390,
    '0746': 2544,
    '0747': 4124,
}

# Contar aparelhos no script
contagens_script = {}
detalhes_pdf = {}

for pdf_num, pdf_nome in pdfs_lista:
    total = 0
    linhas_contadas = []
    
    try:
        with open(pdf_nome, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        
        lines = text.split('\n')
        
        for linha in lines:
            match = re.match(r'^(\d+,\d+)\s+un\s+(.+)$', linha)
            if match:
                qty_str = match.group(1).replace(',', '.')
                qtd = int(float(qty_str))
                description = match.group(2)
                total += qtd
                linhas_contadas.append({
                    'qtd': qtd,
                    'desc': description[:60]
                })
        
        contagens_script[pdf_num] = total
        detalhes_pdf[pdf_num] = linhas_contadas
        
    except Exception as e:
        print(f"❌ Erro ao processar {pdf_nome}: {e}\n")
        contagens_script[pdf_num] = 0

# Exibir comparação
print(f"{'Nº':<3} {'PDF':<8} {'Seu Count':<12} {'Script':<12} {'Diferença':<15} {'Status':<15}\n")

total_usuario = 0
total_script = 0
erros = []

for pdf_num, pdf_nome in pdfs_lista:
    seu_count = contagens_usuario[pdf_num]
    script_count = contagens_script[pdf_num]
    diferenca = script_count - seu_count
    
    total_usuario += seu_count
    total_script += script_count
    
    if diferenca == 0:
        status = "✅ OK"
    elif diferenca > 0:
        status = f"⚠️ +{diferenca}"
        erros.append((pdf_num, seu_count, script_count, diferenca, "EXTRA no script"))
    else:
        status = f"⚠️ {diferenca}"
        erros.append((pdf_num, seu_count, script_count, diferenca, "FALTAM no script"))
    
    print(f"{pdfs_lista.index((pdf_num, pdf_nome))+1:<3} {pdf_num:<8} {seu_count:<12,d} {script_count:<12,d} {diferenca:+d}              {status:<15}")

print(f"\n{'─'*70}")
print(f"{'TOTAL':<12} {total_usuario:<12,d} {total_script:<12,d} {total_script - total_usuario:+d}")
print(f"{'─'*70}\n")

if erros:
    print("⚠️  DISCREPÂNCIAS ENCONTRADAS:\n")
    for pdf_num, seu, script, dif, tipo in erros:
        print(f"PDF {pdf_num}: {tipo}")
        print(f"  Você contou: {seu:,} aparelhos")
        print(f"  Script contou: {script:,} aparelhos")
        print(f"  Diferença: {dif:+d}\n")
else:
    print("✅ TODAS AS CONTAGENS BATEM PERFEITAMENTE!\n")

# Opção para inspecionar um PDF específico
print("="*120)
print("💡 Para inspecionar um PDF específico e ver TODAS as linhas contadas, execute:")
print("   python inspecionar_pdf.py")
print("="*120 + "\n")
