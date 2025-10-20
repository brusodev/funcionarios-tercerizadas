import PyPDF2
import re

pdf_files_para_verificar = [
    ('ADM 0800100_0735_2025 de 30_09_2025.PDF', 12, 'PDF 0735'),
    ('ADM 0800100_0738_2025 de 30_09_2025.PDF', 2, 'PDF 0738'),
    ('ADM 0800100_0744_2025 de 30_09_2025.PDF', 1, 'PDF 0744'),
]

for pdf_file, diferenca_esperada, pdf_nome in pdf_files_para_verificar:
    print("="*80)
    print(f"🔍 {pdf_nome} (Diferença de +{diferenca_esperada} aparelhos)")
    print("="*80 + "\n")
    
    try:
        with open(pdf_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        
        lines = text.split('\n')
        
        # Procurar palavras-chave que indicariam linhas especiais
        palavras_chave = [
            'DANIFICADO', 'FURTADO', 'ROUBADO', 'PERDA', 'ACIDENTE',
            'DEFEITO', 'NÃO FUNCIONA', 'SEM FUNCIONAMENTO',
            'BLOQUEADO', 'SELADO', 'LACRADO',
            'DUPLICADO', 'DUPLICATA', 'CÓPIA',
            'SUBTOTAL', 'TOTAL', 'RESUMO'
        ]
        
        linhas_especiais = []
        
        for i, linha in enumerate(lines):
            # Se tem quantidade no início
            if re.match(r'^(\d+,\d+)\s+un\s+', linha):
                # E tem alguma palavra-chave
                for palavra in palavras_chave:
                    if palavra in linha.upper():
                        match = re.match(r'^(\d+,\d+)\s+un\s+(.+)$', linha)
                        if match:
                            qty = int(float(match.group(1).replace(',', '.')))
                            linhas_especiais.append({
                                'qtd': qty,
                                'palavra_chave': palavra,
                                'descricao': match.group(2)[:80]
                            })
                        break
        
        if linhas_especiais:
            print(f"Encontradas {len(linhas_especiais)} linhas com status especial:\n")
            total_especial = 0
            for item in linhas_especiais:
                print(f"  {item['qtd']:,} un - {item['palavra_chave']}")
                print(f"  └─ {item['descricao']}\n")
                total_especial += item['qtd']
            print(f"TOTAL: {total_especial:,} aparelhos com status especial")
        else:
            print("❌ Nenhuma linha com status especial encontrada")
            print("\nMostrando as ÚLTIMAS 10 linhas do PDF para contexto:\n")
            for linha in lines[-10:]:
                if linha.strip():
                    print(f"  {linha[:80]}")
    
    except FileNotFoundError:
        print(f"❌ Arquivo não encontrado: {pdf_file}")
    
    print()
