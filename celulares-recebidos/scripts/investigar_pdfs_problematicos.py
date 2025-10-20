import PyPDF2
import re

# PDFs problemáticos
pdfs_investigar = [
    ('ADM 0800100_0740_2025 de 30_09_2025.PDF', 9, 3950.54),
    ('ADM 0800100_0743_2025 de 30_09_2025.PDF', 912, 974075.30),
    ('ADM 0800100_0746_2025 de 30_09_2025.PDF', 2544, 3050180.53)
]

for pdf_nome, aparelhos_esperados, valor_esperado in pdfs_investigar:
    print("=" * 100)
    print(f"INVESTIGANDO: {pdf_nome}")
    print(f"Esperado: {aparelhos_esperados} aparelhos, R$ {valor_esperado:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
    print("=" * 100)
    print()
    
    with open(pdf_nome, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        texto_completo = ""
        
        for page in pdf_reader.pages:
            texto_completo += page.extract_text() + "\n"
    
    linhas = texto_completo.split('\n')
    
    # Procurar por "Total do ADM"
    total_adm = None
    for i, linha in enumerate(linhas):
        if 'Total do ADM' in linha:
            # Extrair valor
            valor_match = re.search(r'R\$\s*([\d.]+,\d{2})', linha)
            if valor_match:
                total_adm = valor_match.group(1)
                print(f"✓ Total do ADM encontrado no PDF: R$ {total_adm}")
                print(f"  Linha {i}: {linha.strip()}")
                break
    
    if not total_adm:
        print("⚠ Total do ADM NÃO encontrado no PDF")
    print()
    
    # Procurar padrões que podem ter sido perdidos
    print("Procurando padrões alternativos...")
    print()
    
    # Padrão 1: Linhas com "un" que NÃO começam com número
    print("1. Linhas com 'un' que NÃO começam com número decimal:")
    linhas_sem_numero = []
    for i, linha in enumerate(linhas):
        if ' un ' in linha.lower() and not re.match(r'^\d+,\d+\s+un', linha.strip(), re.IGNORECASE):
            if any(palavra in linha.upper() for palavra in ['SMARTPHONE', 'TELEFONE', 'CELULAR', 'APARELHO', 'IPHONE']):
                linhas_sem_numero.append((i, linha.strip()))
    
    if linhas_sem_numero:
        print(f"  Encontradas {len(linhas_sem_numero)} linhas:")
        for i, linha in linhas_sem_numero[:20]:  # Mostrar até 20
            print(f"    Linha {i}: {linha[:100]}")
    else:
        print("  Nenhuma encontrada")
    print()
    
    # Padrão 2: Linhas que começam com número inteiro (sem vírgula)
    print("2. Linhas com número INTEIRO + 'un' (sem vírgula decimal):")
    linhas_inteiro = []
    for i, linha in enumerate(linhas):
        match = re.match(r'^(\d+)\s+un\s+(SMARTPHONE|TELEFONE|CELULAR|APARELHO)', linha.strip(), re.IGNORECASE)
        if match:
            linhas_inteiro.append((i, linha.strip()))
    
    if linhas_inteiro:
        print(f"  Encontradas {len(linhas_inteiro)} linhas:")
        for i, linha in linhas_inteiro[:20]:
            print(f"    Linha {i}: {linha[:100]}")
    else:
        print("  Nenhuma encontrada")
    print()
    
    # Padrão 3: Procurar por palavras-chave sem "un"
    print("3. Linhas com SMARTPHONE/TELEFONE/CELULAR sem 'un':")
    linhas_sem_un = []
    for i, linha in enumerate(linhas):
        if any(palavra in linha.upper() for palavra in ['SMARTPHONE', 'TELEFONE CELULAR', 'APARELHO CELULAR']):
            if ' un ' not in linha.lower() and re.search(r'R\$\s*[\d.]+,\d{2}', linha):
                linhas_sem_un.append((i, linha.strip()))
    
    if linhas_sem_un:
        print(f"  Encontradas {len(linhas_sem_un)} linhas:")
        for i, linha in linhas_sem_un[:20]:
            print(f"    Linha {i}: {linha[:100]}")
    else:
        print("  Nenhuma encontrada")
    print()
    
    # Padrão 4: Procurar todos os padrões genéricos com valor
    print("4. TODOS os padrões com 'R$' (genérico):")
    pattern_generico = r'^(.+?)(R\$\s*[\d.]+,\d{2})'
    linhas_com_valor = []
    
    for i, linha in enumerate(linhas):
        if 'R$' in linha and any(palavra in linha.upper() for palavra in ['SMARTPHONE', 'TELEFONE', 'CELULAR', 'APARELHO', 'IPHONE']):
            if not re.match(r'^\d+,\d+\s+un\s+(SMARTPHONE|TELEFONE\s+CELULAR|APARELHO)', linha.strip(), re.IGNORECASE):
                linhas_com_valor.append((i, linha.strip()))
    
    if linhas_com_valor:
        print(f"  Encontradas {len(linhas_com_valor)} linhas que têm R$ mas NÃO foram capturadas:")
        for i, linha in linhas_com_valor[:30]:
            print(f"    Linha {i}: {linha[:150]}")
    else:
        print("  Todas as linhas com R$ foram capturadas!")
    print()
    
    print()

print("=" * 100)
print("INVESTIGAÇÃO CONCLUÍDA")
print("=" * 100)
