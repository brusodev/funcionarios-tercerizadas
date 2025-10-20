import PyPDF2
import re

pdf_file = 'ADM 0800100_0738_2025 de 30_09_2025.PDF'

with open(pdf_file, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for page in reader.pages:
        text += page.extract_text()

lines = text.split('\n')

print("="*80)
print("🔍 ANÁLISE COMPLETA PDF 0738 - PROCURANDO OS 2 APARELHOS EXTRAS")
print("="*80 + "\n")

# Procurar TODAS as linhas que começam com quantidade
print("TODAS AS LINHAS COM QUANTIDADE NO PDF 0738:\n")

aparelhos = []
for i, linha in enumerate(lines):
    match = re.match(r'^(\d+,\d+)\s+un\s+(.+)$', linha)
    if match:
        qty_str = match.group(1).replace(',', '.')
        qtd = int(float(qty_str))
        description = match.group(2)
        
        aparelhos.append({
            'qtd': qtd,
            'descricao': description,
            'linha': i
        })

print(f"Total de linhas de aparelhos: {len(aparelhos)}")
print(f"Total de aparelhos: {sum(a['qtd'] for a in aparelhos):,}\n")

# Procurar por linhas que possam ser problemáticas
print("LINHAS POSSIVELMENTE DESCARTÁVEIS:\n")

problematicas = []

for item in aparelhos:
    desc = item['descricao'].upper()
    
    # Procurar indicadores de problemas
    if any(keyword in desc for keyword in ['BLOQUEADO', 'DEFEITO', 'DANIFICADO', 'FURTADO', 
                                             'SELADO', 'LACRADO', 'SEM', 'VAZIO', 'VAZIA',
                                             'DUPLICADO', 'CÓPIA', 'FUNDO', 'DISPLAY',
                                             'BATERIA', 'CARREGADOR', 'QUEBRADO', 'TRINCADO',
                                             'NÃO FUNCIONA', 'NÃO LIGANDO', 'N/A', 'INUTILIZADO']):
        problematicas.append(item)
        print(f"⚠️  {item['qtd']} un - {item['descricao'][:80]}")

if not problematicas:
    print("Nenhuma linha com indicadores óbvios de problema\n")
    print("MOSTRANDO TODAS AS LINHAS COM QUANTIDADE BAIXA (1-5 un):\n")
    
    for item in aparelhos:
        if item['qtd'] <= 5:
            print(f"  {item['qtd']} un - {item['descricao'][:80]}")

print(f"\n{'='*80}")
print("Aparelhos identificados como problemáticos: ", sum(a['qtd'] for a in problematicas))
print(f"{'='*80}")

# Se não encontrou, mostrar as últimas 20 linhas de aparelhos
if not problematicas:
    print("\nÚLTIMAS 20 LINHAS DE APARELHOS DO PDF:\n")
    for item in aparelhos[-20:]:
        print(f"  {item['qtd']:3d} un - {item['descricao'][:70]}")
