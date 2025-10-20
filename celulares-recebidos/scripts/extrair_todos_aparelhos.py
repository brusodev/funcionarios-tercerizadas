import PyPDF2
import re
import json

# Abrir o PDF
pdf_path = 'ADM 0800100_0745_2025 de 30_09_2025.PDF'

with open(pdf_path, 'rb') as file:
    pdf_reader = PyPDF2.PdfReader(file)
    texto_completo = ""
    
    # Extrair texto de todas as páginas
    for page in pdf_reader.pages:
        texto_completo += page.extract_text() + "\n"

# Dividir em linhas
linhas = texto_completo.split('\n')

# PADRÃO EXPANDIDO: capturar SMARTPHONE, TELEFONE CELULAR e APARELHO
pattern = r'^(\d+,\d+)\s+un\s+(SMARTPHONE|TELEFONE\s+CELULAR|APARELHO)\s+(.+)'

items = []
linha_anterior = ""

for i, linha in enumerate(linhas):
    match = re.match(pattern, linha.strip(), re.IGNORECASE)
    
    if match:
        quantidade_str = match.group(1)
        tipo = match.group(2)
        descricao = match.group(3).strip()
        
        # Acumular descrição de linhas seguintes
        partes_descricao = [descricao]
        
        # Procurar nas próximas linhas por continuação
        for j in range(i+1, min(i+10, len(linhas))):
            proxima_linha = linhas[j].strip()
            
            # Parar se encontrar próximo item ou subtotal
            if re.match(r'^\d+,\d+\s+un\s+', proxima_linha, re.IGNORECASE):
                break
            if 'Subtotal:' in proxima_linha or 'Total' in proxima_linha:
                break
                
            # Se a linha não está vazia, adicionar à descrição
            if proxima_linha:
                partes_descricao.append(proxima_linha)
                
                # Se encontrou valor, parar
                if 'R$' in proxima_linha:
                    break
        
        # Montar descrição completa
        descricao_completa = ' '.join(partes_descricao)
        
        # Extrair valor
        valor_match = re.search(r'R\$\s*([\d.]+,\d{2})', descricao_completa)
        
        if valor_match:
            quantidade = float(quantidade_str.replace(',', '.'))
            valor_str = valor_match.group(1)
            
            # Limpar descrição (remover valor)
            descricao_limpa = re.sub(r'///.*$', '', descricao_completa).strip()
            
            # Formatar descrição para ficar igual ao padrão
            descricao_formatada = f"{tipo} {descricao_limpa}"
            
            items.append({
                'unidade': quantidade,
                'modelo': descricao_formatada,
                'valor': f'R$ {valor_str}'
            })

# Salvar JSON estruturado
with open('celulares_todos_aparelhos.json', 'w', encoding='utf-8') as f:
    json.dump(items, f, ensure_ascii=False, indent=2)

# Calcular totais
total_unidades = sum(item['unidade'] for item in items)

total_valor = 0
for item in items:
    valor_str = item['valor'].replace('R$', '').strip()
    valor_str = valor_str.replace('.', '').replace(',', '.')
    total_valor += float(valor_str)

print("=" * 80)
print("EXTRAÇÃO COMPLETA - TODOS OS TIPOS DE APARELHOS")
print("=" * 80)
print(f"\nTotal de itens: {len(items)}")
print(f"Total de aparelhos: {int(total_unidades)}")
print(f"Total em valores: R$ {total_valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
print("\nPor tipo:")

# Contar por tipo
tipos = {}
for item in items:
    tipo = item['modelo'].split()[0:2]  # Primeiras 2 palavras
    tipo_key = ' '.join(tipo)
    
    if tipo_key not in tipos:
        tipos[tipo_key] = {'quantidade': 0, 'valor': 0}
    
    tipos[tipo_key]['quantidade'] += item['unidade']
    
    valor_str = item['valor'].replace('R$', '').strip()
    valor_str = valor_str.replace('.', '').replace(',', '.')
    tipos[tipo_key]['valor'] += float(valor_str)

for tipo, dados in sorted(tipos.items()):
    print(f"  {tipo}: {int(dados['quantidade'])} unidades, R$ {dados['valor']:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))

print("\n" + "=" * 80)
print(f"Total do ADM (oficial): R$ 4.644.268,78")
print(f"Total calculado: R$ {total_valor:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))

diferenca = 4644268.78 - total_valor
if abs(diferenca) < 1:
    print("✓ VALORES CONFEREM!")
else:
    print(f"Diferença: R$ {abs(diferenca):,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
    if diferenca > 0:
        print(f"  Ainda faltam R$ {diferenca:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
    else:
        print(f"  Total excede em R$ {abs(diferenca):,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))

print("\nArquivo salvo: celulares_todos_aparelhos.json")
print("=" * 80)
