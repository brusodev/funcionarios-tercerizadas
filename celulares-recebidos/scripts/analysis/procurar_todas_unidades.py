import PyPDF2
import re
from collections import defaultdict

pdf_files = [f'ADM 0800100_073{i}_2025 de 30_09_2025.PDF' for i in range(3, 8)] + \
            [f'ADM 0800100_074{i}_2025 de 30_09_2025.PDF' for i in range(0, 8)] + \
            ['ADM 0800100_0747_2025 de 30092025.PDF']

print("=== PROCURA COMPLETA POR UNIDADES DIFERENTES (kg, LOTE, etc.) ===\n")

aparelhos_especiais = defaultdict(lambda: {'quantidade': 0, 'itens': []})
total_especial = 0

for pdf_file in pdf_files:
    try:
        with open(pdf_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        
        lines = text.split('\n')
        
        for i, linha in enumerate(lines):
            # Procurar padrões de quantidade que NÃO sejam "un"
            # Pode ser: kg, lote, caixa, lata, pç, etc.
            
            # Padrão: N,NN [UNIDADE] TELEFONE/CELULAR
            match = re.search(r'(\d+,\d+)\s+(kg|lote|LOTE|caixa|CAIXA|pç|Pç|lata|LATA)\s+TELEFONE|(\d+,\d+)\s+(kg|lote|LOTE|caixa|CAIXA|pç|Pç|lata|LATA).*CELULAR', linha, re.IGNORECASE)
            
            if match:
                # Extrair quantidade e unidade
                if match.group(1):
                    qty_str = match.group(1).replace(',', '.')
                    unidade = match.group(2)
                else:
                    qty_str = match.group(3).replace(',', '.')
                    unidade = match.group(4)
                
                qty = float(qty_str)
                
                # Converter para aparelhos
                if unidade.lower() == 'kg':
                    aparelhos = round(qty / 0.49)
                elif unidade.lower() == 'lote':
                    aparelhos = int(qty)
                else:
                    aparelhos = int(qty)
                
                aparelhos_especiais[unidade.lower()]['quantidade'] += aparelhos
                aparelhos_especiais[unidade.lower()]['itens'].append({
                    'pdf': pdf_file,
                    'qty': qty,
                    'aparelhos': aparelhos,
                    'linha': i,
                    'descricao': linha[:60]
                })
                
                total_especial += aparelhos
    
    except FileNotFoundError:
        pass

print(f"{'Unidade':<10} {'Qtd Original':>15} {'Aparelhos':>15} {'PDFs':>8}")
print("="*60)

for unidade in sorted(aparelhos_especiais.keys()):
    data = aparelhos_especiais[unidade]
    pdfs_unicos = len(set(item['pdf'] for item in data['itens']))
    print(f"{unidade:<10} {sum(item['qty'] for item in data['itens']):>15.2f} {data['quantidade']:>15} {pdfs_unicos:>8}")
    
    for item in data['itens'][:2]:
        print(f"  └─ {item['pdf'].split('_')[2]}: {item['qty']:.2f} → {item['aparelhos']} aparelho(s)")
    if len(data['itens']) > 2:
        print(f"  └─ ... +{len(data['itens'])-2} mais")

print("="*60)
print(f"\n📊 TOTAL EM UNIDADES ESPECIAIS: {total_especial:,} aparelhos")
print(f"\n   Contagem ATUAL: 32.027 aparelhos (un)")
print(f"   Contagem ESPECIAL: {total_especial:,} aparelhos (kg, lote, etc.)")
print(f"   NOVO TOTAL: {32027 + total_especial:,} aparelhos")
print(f"\n   Sua contagem: 32.015")
print(f"   Diferença: {32015 - (32027 + total_especial):,}")
