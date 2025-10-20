import PyPDF2
import re

# Procurar por Araraquara em PDFs que podem conter
pdfs_araraquara = [
    'ADM 0800100_0739_2025 de 30_09_2025.PDF',
    'ADM 0800100_0747_2025 de 30092025.PDF'
]

for pdf_nome in pdfs_araraquara:
    print(f"\n{'='*100}")
    print(f"Buscando ARARAQUARA em: {pdf_nome}")
    print(f"{'='*100}\n")
    
    try:
        with open(pdf_nome, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            texto_completo = ""
            
            for page_num, page in enumerate(pdf_reader.pages):
                texto = page.extract_text()
                texto_completo += texto + "\n"
        
        linhas = texto_completo.split('\n')
        
        # Procurar Araraquara
        for i, linha in enumerate(linhas):
            if 'ARARAQUARA' in linha.upper() or '810900' in linha:
                print(f"Linha {i}: {linha}")
                
                # Contexto detalhado
                print("\nCONTEXTO:")
                for j in range(max(0, i-5), min(len(linhas), i+15)):
                    marker = ">>>" if j == i else "   "
                    print(f"{marker} {j:4d}: {linhas[j][:120]}")
                print()
        
    except Exception as e:
        print(f"Erro: {e}")
