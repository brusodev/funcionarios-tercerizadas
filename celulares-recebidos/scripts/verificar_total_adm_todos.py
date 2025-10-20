import PyPDF2
import re

# PDFs para verificar
pdfs = [
    'ADM 0800100_0733_2025 de 30_09_2025.PDF',
    'ADM 0800100_0734_2025 de 30_09_2025.PDF',
    'ADM 0800100_0740_2025 de 30_09_2025.PDF',
    'ADM 0800100_0741_2025 de 30_09_2025.PDF',
    'ADM 0800100_0742_2025 de 30_09_2025.PDF',
    'ADM 0800100_0743_2025 de 30_09_2025.PDF',
    'ADM 0800100_0744_2025 de 30_09_2025.PDF',
    'ADM 0800100_0735_2025 de 30_09_2025.PDF',
    'ADM 0800100_0736_2025 de 30_09_2025.PDF',
    'ADM 0800100_0737_2025 de 30_09_2025.PDF',
    'ADM 0800100_0738_2025 de 30_09_2025.PDF',
    'ADM 0800100_0739_2025 de 30_09_2025.PDF',
    'ADM 0800100_0745_2025 de 30_09_2025.PDF',
    'ADM 0800100_0746_2025 de 30_09_2025.PDF',
    'ADM 0800100_0747_2025 de 30092025.PDF'
]

valores_usuario = {
    'ADM 0800100_0733_2025 de 30_09_2025.PDF': 7879.62,
    'ADM 0800100_0734_2025 de 30_09_2025.PDF': 5716622.03,
    'ADM 0800100_0740_2025 de 30_09_2025.PDF': 3950.54,
    'ADM 0800100_0741_2025 de 30_09_2025.PDF': 18816.20,
    'ADM 0800100_0742_2025 de 30_09_2025.PDF': 84426.55,
    'ADM 0800100_0743_2025 de 30_09_2025.PDF': 974075.30,
    'ADM 0800100_0744_2025 de 30_09_2025.PDF': 3461458.49,
    'ADM 0800100_0735_2025 de 30_09_2025.PDF': 2839605.26,
    'ADM 0800100_0736_2025 de 30_09_2025.PDF': 1960163.54,
    'ADM 0800100_0737_2025 de 30_09_2025.PDF': 280644.01,
    'ADM 0800100_0738_2025 de 30_09_2025.PDF': 485270.26,
    'ADM 0800100_0739_2025 de 30_09_2025.PDF': 1870406.44,
    'ADM 0800100_0745_2025 de 30_09_2025.PDF': 4644268.78,
    'ADM 0800100_0746_2025 de 30_09_2025.PDF': 3050180.53,
    'ADM 0800100_0747_2025 de 30092025.PDF': 3466230.15
}

print("=" * 100)
print("VERIFICAÇÃO DOS VALORES 'Total do ADM' NOS PDFs")
print("=" * 100)
print()

total_adm_encontrados = {}
discrepancias = []

for pdf_nome in pdfs:
    try:
        with open(pdf_nome, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            texto_completo = ""
            
            for page in pdf_reader.pages:
                texto_completo += page.extract_text() + "\n"
        
        linhas = texto_completo.split('\n')
        
        # Procurar por "Total do ADM"
        total_adm = None
        linha_num = None
        
        for i, linha in enumerate(linhas):
            if 'Total do ADM' in linha or 'Total ADM' in linha:
                # Extrair valor
                valor_match = re.search(r'R\$\s*([\d.]+,\d{2})', linha)
                if valor_match:
                    total_adm = valor_match.group(1)
                    linha_num = i
                    break
        
        if total_adm:
            # Converter para float
            valor_float = float(total_adm.replace('.', '').replace(',', '.'))
            total_adm_encontrados[pdf_nome] = valor_float
            
            # Comparar com valor fornecido pelo usuário
            valor_usuario = valores_usuario.get(pdf_nome, 0)
            diferenca = abs(valor_float - valor_usuario)
            
            status = "✓" if diferenca < 1 else "❌"
            
            print(f"{pdf_nome}")
            print(f"  Total do ADM (PDF): R$ {total_adm}")
            print(f"  Valor informado: R$ {valor_usuario:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
            print(f"  Status: {status}")
            
            if diferenca >= 1:
                print(f"  ⚠ DISCREPÂNCIA: R$ {diferenca:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
                discrepancias.append({
                    'pdf': pdf_nome,
                    'pdf_valor': valor_float,
                    'usuario_valor': valor_usuario,
                    'diferenca': diferenca
                })
            print()
        else:
            print(f"{pdf_nome}")
            print(f"  ⚠ Total do ADM NÃO ENCONTRADO no PDF")
            print()
            
    except Exception as e:
        print(f"{pdf_nome}")
        print(f"  ❌ ERRO: {e}")
        print()

print("=" * 100)
print("RESUMO")
print("=" * 100)
print()

if discrepancias:
    print(f"⚠ ATENÇÃO: {len(discrepancias)} PDF(s) com discrepância entre valor informado e Total do ADM:")
    print()
    for disc in discrepancias:
        print(f"  {disc['pdf']}")
        print(f"    Total do ADM (PDF): R$ {disc['pdf_valor']:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
        print(f"    Valor informado: R$ {disc['usuario_valor']:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
        print(f"    Diferença: R$ {disc['diferenca']:,.2f}".replace(',', '_').replace('.', ',').replace('_', '.'))
        print()
    
    print("RECOMENDAÇÃO: Verificar manualmente esses PDFs para confirmar valores corretos.")
else:
    print("✓ Todos os valores conferem com os PDFs!")

print("=" * 100)
