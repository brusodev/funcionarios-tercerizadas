import PyPDF2
import re
from collections import defaultdict
import sys

# Configurar encoding
sys.stdout.reconfigure(encoding='utf-8')

# PDFs para analisar
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

print("=" * 130)
print("INVESTIGACAO: PROCURANDO TODOS OS RECINTOS E ARARAQUARA")
print("=" * 130)
print()

# Padrões para procurar recintos
pattern_unidade = r'(\d{7})\s*-\s*([A-ZÁ-Ú\s/]+?)\s+Unidade:'
pattern_recinto = r'Recinto:\s*(\d+)\s*-\s*(\d+)\s+(.+?)(?:\n|$)'

todos_recintos = defaultdict(list)
todos_recintos_numero = defaultdict(list)

for pdf_nome in pdfs:
    print("\n" + "=" * 130)
    print(f"PDF: {pdf_nome}")
    print("=" * 130)
    
    try:
        with open(pdf_nome, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            texto_completo = ""
            
            for page in pdf_reader.pages:
                texto_completo += page.extract_text() + "\n"
        
        linhas = texto_completo.split('\n')
        
        # Procurar padrão "XXXX - NOMECIDADE Unidade:"
        print("\n📍 Procurando padrão 'XXXXX - CIDADE Unidade:':")
        unidades_encontradas = set()
        
        for linha in linhas:
            match = re.search(pattern_unidade, linha)
            if match:
                codigo = match.group(1)
                nome = match.group(2).strip()
                recinto_id = f"{codigo} - {nome}"
                
                if recinto_id not in unidades_encontradas:
                    unidades_encontradas.add(recinto_id)
                    todos_recintos[recinto_id].append(pdf_nome)
                    print(f"  ✓ {recinto_id}")
        
        if not unidades_encontradas:
            print("  ⚠ Nenhum padrão encontrado")
        
        # Procurar padrão "Recinto: 305 - 810300 Regional DMA - Bauru/SP"
        print("\n📍 Procurando padrão 'Recinto: XXX - XXXXX ...':")
        recintos_numero_encontrados = set()
        
        for linha in linhas:
            match = re.search(pattern_recinto, linha)
            if match:
                num = match.group(1)
                codigo = match.group(2)
                nome = match.group(3).strip()
                recinto_id = f"{num} - {codigo} {nome}"
                
                if recinto_id not in recintos_numero_encontrados:
                    recintos_numero_encontrados.add(recinto_id)
                    todos_recintos_numero[recinto_id].append(pdf_nome)
                    print(f"  ✓ {recinto_id}")
        
        if not recintos_numero_encontrados:
            print("  ⚠ Nenhum padrão encontrado")
        
        # Procurar especificamente por "ARARAQUARA"
        print("\n🔍 Procurando 'ARARAQUARA':")
        araraquara_encontrado = False
        
        for i, linha in enumerate(linhas):
            if 'ARARAQUARA' in linha.upper():
                araraquara_encontrado = True
                print(f"  ✓ Linha {i}: {linha.strip()[:100]}")
                
                # Mostrar contexto (5 linhas antes e depois)
                print(f"\n     Contexto:")
                for j in range(max(0, i-3), min(len(linhas), i+4)):
                    marker = " >>> " if j == i else "     "
                    print(f"{marker}{linhas[j][:120]}")
                print()
        
        if not araraquara_encontrado:
            print("  ⚠ ARARAQUARA não encontrado neste PDF")
    
    except Exception as e:
        print(f"❌ Erro: {e}")


print("\n" + "=" * 130)
print("RESUMO GERAL - TODOS OS RECINTOS ENCONTRADOS")
print("=" * 130)
print()

print(f"\nPADRAO 'XXXXX - CIDADE Unidade:' ({len(todos_recintos)} recintos):\n")
for recinto in sorted(todos_recintos.keys()):
    pdfs_str = ', '.join([p.split('ADM ')[1].split(' de')[0] if 'ADM' in p else p for p in todos_recintos[recinto]])
    print(f"  {recinto} ({len(todos_recintos[recinto])} PDF(s))")

print(f"\nPADRAO 'Recinto: XXX - XXXXX ...' ({len(todos_recintos_numero)} recintos):\n")
for recinto in sorted(todos_recintos_numero.keys()):
    pdfs_str = ', '.join([p.split('ADM ')[1].split(' de')[0] if 'ADM' in p else p for p in todos_recintos_numero[recinto]])
    print(f"  {recinto} ({len(todos_recintos_numero[recinto])} PDF(s))")

print("\n" + "=" * 130)
