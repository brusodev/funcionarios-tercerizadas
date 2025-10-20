import PyPDF2
import re

pdf_file = 'ADM 0800100_0735_2025 de 30_09_2025.PDF'

with open(pdf_file, 'rb') as f:
    reader = PyPDF2.PdfReader(f)
    text = ''
    for page in reader.pages:
        text += page.extract_text()

lines = text.split('\n')

print("="*80)
print("🔍 ANÁLISE PRECISA PDF 0735")
print("="*80 + "\n")

# Contar TODAS as linhas com aparelhos
total_sem_filtro = 0
total_com_filtro = 0
linhas_4_grandes = []

for i, linha in enumerate(lines):
    match = re.match(r'^(\d+,\d+)\s+un\s+(.+)$', linha)
    if match:
        qty_str = match.group(1).replace(',', '.')
        qtd = int(float(qty_str))
        description = match.group(2)
        
        total_sem_filtro += qtd
        
        # Verificar se é uma das 4 linhas grandes
        if qtd >= 100:
            linhas_4_grandes.append({
                'linha': i,
                'qtd': qtd,
                'descricao': description[:60]
            })
            print(f"🔴 LINHA GRANDE {len(linhas_4_grandes)}: {qtd:3d} un - {description[:70]}")
        else:
            total_com_filtro += qtd

print(f"\n{'='*80}")
print("📊 CONTAGEM PDF 0735:\n")

print(f"Total DE TODAS as linhas (incluindo as 4 grandes):  {total_sem_filtro:,} aparelhos")
print(f"Total SEM as 4 linhas grandes:                     {total_com_filtro:,} aparelhos")
print(f"Soma das 4 linhas grandes:                         {total_sem_filtro - total_com_filtro:,} aparelhos")

print(f"\nDetalhe das 4 linhas:")
soma_4_linhas = 0
for item in linhas_4_grandes:
    print(f"  • {item['qtd']} un - {item['descricao']}")
    soma_4_linhas += item['qtd']

print(f"  TOTAL das 4: {soma_4_linhas} aparelhos\n")

# Verificação: sua contagem vs script
sua_contagem_0735 = 3804
contagem_script_0735 = 3816

print(f"{'='*80}")
print("✅ VERIFICAÇÃO FINAL:\n")

print(f"Sua contagem PDF 0735:           {sua_contagem_0735:,} aparelhos")
print(f"Script sem as 4 grandes:         {total_com_filtro:,} aparelhos")
print(f"Script com as 4 grandes:         {total_sem_filtro:,} aparelhos")
print(f"\nScript - Sua contagem:           {total_sem_filtro - sua_contagem_0735:+,} aparelhos")
print(f"(Diferença = as 4 linhas grandes)")

print(f"\n{'='*80}")
print("🎯 CONCLUSÃO:\n")

if total_sem_filtro == sua_contagem_0735 + soma_4_linhas:
    print("✅ CONFIRMADO: Os 32.015 NÃO incluem as 4 linhas grandes!")
    print(f"   32.015 = (Total 0735 SEM as 4) + resto dos PDFs")
    print(f"   {total_com_filtro} + (outros PDFs) = 32.015")
else:
    print("❌ Não bate exatamente. Verificando...")
    print(f"   Diferença: {sua_contagem_0735 - total_com_filtro:+,} aparelhos")
