import PyPDF2
import re
from collections import defaultdict

pdf_file = 'ADM 0800100_0735_2025 de 30_09_2025.PDF'

with open(pdf_file, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for page in reader.pages:
        text += page.extract_text()

lines = text.split('\n')

# Procurar modelos dos 4 aparelhos suspeitos
suspicious_models = [
    'XIAOMI REDMI NOTE 13 256GB CHINA',
    'XIAOMI REDMI NOTE 13 5G 256GB CHINA',
    'XIAOMI POCO C65 128GB INDIA',
    'XIAOMI REDMI NOTE 14 256GB CHINA'
]

model_counts = defaultdict(list)

# Procurar TODAS as linhas com esses modelos
for i, line in enumerate(lines):
    match = re.match(r'^(\d+,\d+)\s+un\s+(.+)$', line)
    if match:
        qty_str = match.group(1).replace(',', '.')
        qty = int(float(qty_str))
        description = match.group(2)
        
        for model in suspicious_models:
            if model in description:
                model_counts[model].append({
                    'qty': qty,
                    'line': i,
                    'full': line[:120]
                })

print("=== PROCURA DE DUPLICAÇÃO DOS 4 MODELOS SUSPEITOS ===\n")

for model in suspicious_models:
    if model_counts[model]:
        print(f"\n🔍 MODELO: {model}")
        print(f"   Encontrado {len(model_counts[model])} vez(es):")
        total = 0
        for entry in model_counts[model]:
            print(f"   - {entry['qty']:5d} un (linha {entry['line']})")
            total += entry['qty']
        print(f"   TOTAL: {total} aparelhos")
    else:
        print(f"\n❌ MODELO: {model}")
        print(f"   NÃO encontrado em nenhuma outra linha!")
