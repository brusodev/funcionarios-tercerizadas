import PyPDF2
import re

def extrair_texto_pdf(caminho_pdf):
    with open(caminho_pdf, 'rb') as arquivo:
        leitor_pdf = PyPDF2.PdfReader(arquivo)
        texto_completo = []
        for pagina in leitor_pdf.pages:
            texto_completo.append(pagina.extract_text())
        return '\n'.join(texto_completo)

print("="*100)
print("ANÁLISE DETALHADA DA ESTRUTURA DO PDF 0735")
print("="*100)

pdf_path = "ADM 0800100_0735_2025 de 30_09_2025.PDF"
texto = extrair_texto_pdf(pdf_path)
linhas = texto.split('\n')

# Procura por um bloco completo de item
print("\nMostrando primeiros 20 exemplos de itens com contexto completo:\n")

padrao_item = r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades|kg)\s+(SMARTPHONE.*)'
count = 0

for i, linha in enumerate(linhas):
    linha = linha.strip()
    match = re.match(padrao_item, linha, re.IGNORECASE)
    
    if match and count < 20:
        count += 1
        qtd = match.group(1)
        desc = match.group(2)[:80]
        
        print(f"{'='*100}")
        print(f"ITEM {count}: Qtd={qtd}")
        print(f"{'='*100}")
        print(f"Linha {i}: {linha}")
        
        # Mostra as próximas 5 linhas
        print(f"\nPróximas 5 linhas:")
        for j in range(1, 6):
            if i + j < len(linhas):
                print(f"  +{j}: {linhas[i+j]}")
        
        # Procura por "R$" nas próximas linhas
        valores_encontrados = []
        for j in range(1, 11):
            if i + j < len(linhas):
                if 'R$' in linhas[i+j]:
                    valores_encontrados.append(f"+{j}: {linhas[i+j]}")
        
        if valores_encontrados:
            print(f"\nValores encontrados:")
            for v in valores_encontrados:
                print(f"  {v}")
        
        print()

print(f"\n{'='*100}")
print(f"Total de itens SMARTPHONE encontrados: {count}")
print(f"{'='*100}")
