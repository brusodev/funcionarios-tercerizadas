import PyPDF2
import re

print("="*120)
print("🔍 INSPETOR DE PDF - VISUALIZAR TODAS AS LINHAS CONTADAS")
print("="*120 + "\n")

# Lista de PDFs
pdfs_disponiveis = {
    '0733': 'ADM 0800100_0733_2025 de 30_09_2025.PDF',
    '0734': 'ADM 0800100_0734_2025 de 30_09_2025.PDF',
    '0740': 'ADM 0800100_0740_2025 de 30_09_2025.PDF',
    '0741': 'ADM 0800100_0741_2025 de 30_09_2025.PDF',
    '0742': 'ADM 0800100_0742_2025 de 30_09_2025.PDF',
    '0743': 'ADM 0800100_0743_2025 de 30_09_2025.PDF',
    '0744': 'ADM 0800100_0744_2025 de 30_09_2025.PDF',
    '0735': 'ADM 0800100_0735_2025 de 30_09_2025.PDF',
    '0736': 'ADM 0800100_0736_2025 de 30_09_2025.PDF',
    '0737': 'ADM 0800100_0737_2025 de 30_09_2025.PDF',
    '0738': 'ADM 0800100_0738_2025 de 30_09_2025.PDF',
    '0739': 'ADM 0800100_0739_2025 de 30_09_2025.PDF',
    '0745': 'ADM 0800100_0745_2025 de 30_09_2025.PDF',
    '0746': 'ADM 0800100_0746_2025 de 30_09_2025.PDF',
    '0747': 'ADM 0800100_0747_2025 de 30092025.PDF',
}

print("PDFs disponíveis:")
for pdf_num in pdfs_disponiveis.keys():
    print(f"  {pdf_num}")

pdf_selecionado = input("\nQual PDF deseja inspecionar? (ex: 0735): ").strip()

if pdf_selecionado not in pdfs_disponiveis:
    print(f"❌ PDF {pdf_selecionado} não encontrado!")
    exit(1)

pdf_nome = pdfs_disponiveis[pdf_selecionado]

print(f"\n{'='*120}")
print(f"📋 INSPECIONANDO: {pdf_nome}")
print(f"{'='*120}\n")

try:
    with open(pdf_nome, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    
    lines = text.split('\n')
    
    contador = 0
    total = 0
    
    print(f"{'Nº':<4} {'Qtd':<8} {'Descrição':<100}\n")
    
    for linha in lines:
        match = re.match(r'^(\d+,\d+)\s+un\s+(.+)$', linha)
        if match:
            qty_str = match.group(1).replace(',', '.')
            qtd = int(float(qty_str))
            description = match.group(2)
            
            contador += 1
            total += qtd
            
            # Destacar linhas com quantidade >= 100
            if qtd >= 100:
                print(f"{contador:<4} {qtd:<8,d} {description:<100} 🔴 GRANDE")
            else:
                print(f"{contador:<4} {qtd:<8,d} {description:<100}")
    
    print(f"\n{'─'*120}")
    print(f"✅ Total de linhas contadas: {contador}")
    print(f"✅ Total de aparelhos: {total:,}\n")
    
except Exception as e:
    print(f"❌ Erro ao processar PDF: {e}\n")
