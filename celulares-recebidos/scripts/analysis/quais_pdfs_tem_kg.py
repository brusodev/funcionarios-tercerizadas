import PyPDF2
import re

pdf_files = [f'ADM 0800100_073{i}_2025 de 30_09_2025.PDF' for i in range(3, 8)] + \
            [f'ADM 0800100_074{i}_2025 de 30_09_2025.PDF' for i in range(0, 8)] + \
            ['ADM 0800100_0747_2025 de 30092025.PDF']

print('=== PDFs COM LINHAS CONTENDO kg ===\n')

for pdf_file in pdf_files:
    try:
        with open(pdf_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        
        linhas_kg = [linha for linha in text.split('\n') if 'kg' in linha.lower()]
        
        if linhas_kg:
            print(f'{pdf_file}: {len(linhas_kg)} linhas com kg')
            for linha in linhas_kg[:2]:
                print(f'  └─ {linha[:80]}')
            if len(linhas_kg) > 2:
                print(f'  └─ ... +{len(linhas_kg)-2} mais')
            print()
    except:
        pass
