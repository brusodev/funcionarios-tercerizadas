import PyPDF2
import re
import json

# Ler o PDF 0745 completo
pdf_path = "ADM 0800100_0745_2025 de 30_09_2025.PDF"

with open(pdf_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    texto_completo = []
    for page in reader.pages:
        texto_completo.append(page.extract_text())

texto = '\n'.join(texto_completo)
linhas = texto.split('\n')

print("="*80)
print("REPROCESSANDO PDF COMPLETO")
print("="*80)

# Padrão para identificar início de item SMARTPHONE
pattern_item = re.compile(r'^(\d+,\d+)\s+un\s+SMARTPHONE', re.IGNORECASE)
pattern_valor = re.compile(r'R\$\s*([\d.]+,\d{2})')

# Lista para armazenar itens
itens_encontrados = []

i = 0
while i < len(linhas):
    linha_atual = linhas[i].strip()
    
    match = pattern_item.match(linha_atual)
    if match:
        qtd = match.group(1)
        
        # Acumular descrição e buscar valor
        partes_descricao = [linha_atual]
        valor = None
        
        # Verificar se tem valor na mesma linha
        match_valor = pattern_valor.search(linha_atual)
        if match_valor:
            valor = match_valor.group(0)
            texto_sem_valor = linha_atual[:match_valor.start()].strip()
            partes_descricao = [texto_sem_valor]
        else:
            # Buscar nas próximas linhas
            j = i + 1
            while j < len(linhas) and j < i + 10:
                linha_seguinte = linhas[j].strip()
                
                # Parar em próximo item, Subtotal, Total do ADM, cabeçalhos
                if (pattern_item.match(linha_seguinte) or 
                    'Subtotal:' in linha_seguinte or 
                    'Total do ADM:' in linha_seguinte or
                    linha_seguinte.startswith('Quantidade Un.') or
                    linha_seguinte.startswith('Recinto:') or
                    'Documento de' in linha_seguinte or
                    'Original' in linha_seguinte):
                    break
                
                # Verificar se tem valor
                match_valor = pattern_valor.search(linha_seguinte)
                if match_valor:
                    valor = match_valor.group(0)
                    texto_antes = linha_seguinte[:match_valor.start()].strip()
                    if texto_antes:
                        partes_descricao.append(texto_antes)
                    break
                elif linha_seguinte:
                    partes_descricao.append(linha_seguinte)
                
                j += 1
        
        # Se encontrou valor, adicionar
        if valor:
            descricao_completa = ' '.join(partes_descricao)
            descricao_sem_qtd = re.sub(r'^\d+,\d+\s+un\s+', '', descricao_completa)
            descricao_limpa = ' '.join(descricao_sem_qtd.split()).replace(' //', '//')
            
            itens_encontrados.append({
                'quantidade': qtd,
                'descricao': descricao_limpa,
                'valor': valor
            })
    
    i += 1

print(f"\nTotal de itens encontrados: {len(itens_encontrados):,}".replace(',', '.'))

# Calcular total
total_valor = 0
total_aparelhos = 0

for item in itens_encontrados:
    qtd = float(item['quantidade'].replace(',', '.'))
    valor_str = item['valor'].replace('R$ ', '').replace('.', '').replace(',', '.')
    valor = float(valor_str)
    
    total_aparelhos += qtd
    total_valor += valor

print(f"Total de aparelhos: {int(total_aparelhos):,}".replace(',', '.'))
print(f"Total de valores: R$ {total_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Comparar com Total do ADM
pattern_total_adm = re.compile(r'Total do ADM:\s*R\$\s*([\d.]+,\d{2})')
match = pattern_total_adm.search(texto)
if match:
    total_adm_str = match.group(1).replace('.', '').replace(',', '.')
    total_adm = float(total_adm_str)
    diferenca = total_adm - total_valor
    
    print(f"\n{'='*80}")
    print("COMPARAÇÃO COM TOTAL DO ADM:")
    print("="*80)
    print(f"Total do ADM (oficial): R$ {total_adm:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print(f"Total calculado: R$ {total_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print(f"Diferença: R$ {diferenca:+,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    if abs(diferenca) < 1000:
        print("\n✓ Diferença aceitável! (< R$ 1.000)")
    else:
        print(f"\n⚠️ Diferença significativa! Faltam R$ {diferenca:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

# Criar JSON estruturado correto
celulares_completo = []
for item in itens_encontrados:
    qtd = float(item['quantidade'].replace(',', '.'))
    
    celular = {
        "unidade": qtd,
        "modelo": item['descricao'],
        "valor": item['valor']
    }
    celulares_completo.append(celular)

# Salvar JSON completo
with open('celulares_estruturado_completo.json', 'w', encoding='utf-8') as f:
    json.dump(celulares_completo, f, ensure_ascii=False, indent=2)

print(f"\n{'='*80}")
print("✓ Arquivo 'celulares_estruturado_completo.json' criado!")
print("="*80)
