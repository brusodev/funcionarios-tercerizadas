import PyPDF2
import re
from collections import defaultdict

pdf_files = [f'ADM 0800100_073{i}_2025 de 30_09_2025.PDF' for i in range(3, 8)] + \
            [f'ADM 0800100_074{i}_2025 de 30_09_2025.PDF' for i in range(0, 8)] + \
            ['ADM 0800100_0747_2025 de 30092025.PDF']

print("=== PROCURANDO POR APARELHOS EM KG ===\n")

aparelhos_kg_por_pdf = defaultdict(list)
total_kg = 0
total_aparelhos_kg = 0

for pdf_file in pdf_files:
    try:
        with open(pdf_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        
        lines = text.split('\n')
        
        for i, linha in enumerate(lines):
            # Procurar padrão: N,NN kg TELEFONE CELULAR
            if 'kg' in linha.lower() and 'telefone' in linha.lower():
                # Tentar extrair o valor em kg
                match = re.search(r'(\d+,\d+)\s*kg\s+TELEFONE', linha, re.IGNORECASE)
                if match:
                    kg_str = match.group(1).replace(',', '.')
                    kg = float(kg_str)
                    
                    # Estimar número de aparelhos (0,49 kg ≈ 1, 1,00 kg ≈ 2, etc.)
                    # Cada aparelho pesa ~0,5 kg
                    aparelhos_estimado = round(kg / 0.49)  # Mais preciso usar 0,49
                    
                    aparelhos_kg_por_pdf[pdf_file].append({
                        'kg': kg,
                        'aparelhos_estimado': aparelhos_estimado,
                        'descricao': linha[linha.find('TELEFONE'):linha.find('TELEFONE')+50],
                        'linha': i
                    })
                    
                    total_kg += kg
                    total_aparelhos_kg += aparelhos_estimado
        
    except FileNotFoundError:
        pass

print(f"{'PDF':<45} {'KG':>10} {'Aparelhos Est.':>15} {'Linhas':>8}")
print("="*80)

for pdf_file in sorted(aparelhos_kg_por_pdf.keys()):
    items = aparelhos_kg_por_pdf[pdf_file]
    if items:
        total_kg_pdf = sum(item['kg'] for item in items)
        total_aparelhos_pdf = sum(item['aparelhos_estimado'] for item in items)
        print(f"{pdf_file:<45} {total_kg_pdf:>10.2f} {total_aparelhos_pdf:>15} {len(items):>8}")
        
        for item in items[:3]:  # Mostrar apenas os 3 primeiros
            print(f"  └─ {item['kg']:.2f} kg ≈ {item['aparelhos_estimado']} aparelho(s)")
        if len(items) > 3:
            print(f"  └─ ... +{len(items)-3} mais")

if total_aparelhos_kg > 0:
    print("="*80)
    print(f"\n📊 RESUMO GERAL:")
    print(f"   Total de KG: {total_kg:.2f}")
    print(f"   Total de aparelhos em KG: {total_aparelhos_kg:,}")
    print(f"\n   Contagem ATUAL: 32.027 aparelhos (un)")
    print(f"   Contagem EM KG: {total_aparelhos_kg:,} aparelhos")
    print(f"   NOVO TOTAL: {32027 + total_aparelhos_kg:,} aparelhos")
    print(f"\n   Sua contagem: 32.015")
    print(f"   Diferença: {32015 - (32027 + total_aparelhos_kg):,} aparelhos")
else:
    print("\n❌ Nenhum aparelho em KG encontrado!")
