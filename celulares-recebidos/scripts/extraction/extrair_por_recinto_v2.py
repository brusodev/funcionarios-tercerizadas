import PyPDF2
import re
import json
from collections import defaultdict

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

def extrair_aparelhos_por_recinto(pdf_path):
    """Extrai aparelhos agrupados por Recinto/Unidade"""
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        texto_completo = ""
        
        for page in pdf_reader.pages:
            texto_completo += page.extract_text() + "\n"
    
    linhas = texto_completo.split('\n')
    
    # Procurar por padrão "XXXX - NOMECIDADE Unidade:"
    # Exemplo: "0810200 - ARAÇATUBA Unidade:"
    pattern_unidade = r'(\d{7})\s*-\s*([A-ZÁ-Ú\s]+?)\s+Unidade:'
    
    recintos_encontrados = {}
    recinto_atual = None
    
    for i, linha in enumerate(linhas):
        match = re.search(pattern_unidade, linha)
        if match:
            codigo = match.group(1)
            nome = match.group(2).strip()
            recinto_atual = f"{codigo} - {nome}"
            
            if recinto_atual not in recintos_encontrados:
                recintos_encontrados[recinto_atual] = {
                    'codigo': codigo,
                    'nome': nome,
                    'aparelhos': 0,
                    'itens': 0
                }
    
    # Procurar aparelhos
    pattern_aparelho = r'^(\d+,\d+)\s+un\s+(SMARTPHONE|TELEFONE\s+CELULAR|APARELHO|IPHONE|CELULAR|TABLET|RECEPTOR|BOX|IPTV)\s+(.+)'
    
    recinto_atual = None
    
    for i, linha in enumerate(linhas):
        # Atualizar recinto atual
        match_unidade = re.search(pattern_unidade, linha)
        if match_unidade:
            codigo = match_unidade.group(1)
            nome = match_unidade.group(2).strip()
            recinto_atual = f"{codigo} - {nome}"
            continue
        
        # Procurar aparelhos
        match_aparelho = re.match(pattern_aparelho, linha.strip(), re.IGNORECASE)
        
        if match_aparelho and recinto_atual:
            quantidade_str = match_aparelho.group(1)
            quantidade = float(quantidade_str.replace(',', '.'))
            
            if recinto_atual in recintos_encontrados:
                recintos_encontrados[recinto_atual]['aparelhos'] += quantidade
                recintos_encontrados[recinto_atual]['itens'] += 1
    
    return recintos_encontrados

print("=" * 130)
print("EXTRAÇÃO DE APARELHOS POR RECINTO/UNIDADE")
print("=" * 130)
print()

aparelhos_por_recinto = defaultdict(lambda: {'quantidade': 0, 'pdfs': [], 'itens': 0})
total_geral = 0
recintos_encontrados_total = set()

for pdf_nome in pdfs:
    print(f"Processando: {pdf_nome}...")
    
    try:
        recintos = extrair_aparelhos_por_recinto(pdf_nome)
        
        if recintos:
            for recinto_id, dados in recintos.items():
                if dados['aparelhos'] > 0:
                    aparelhos_por_recinto[recinto_id]['quantidade'] += dados['aparelhos']
                    if pdf_nome not in aparelhos_por_recinto[recinto_id]['pdfs']:
                        aparelhos_por_recinto[recinto_id]['pdfs'].append(pdf_nome)
                    aparelhos_por_recinto[recinto_id]['itens'] += dados['itens']
                    
                    recintos_encontrados_total.add(recinto_id)
                    total_geral += dados['aparelhos']
                    
                    print(f"  ✓ {recinto_id}: {int(dados['aparelhos'])} aparelhos ({dados['itens']} itens)")
        else:
            print(f"  ⚠ Nenhum Recinto encontrado")
    
    except Exception as e:
        print(f"  ❌ Erro: {e}")
    
    print()

print("=" * 130)
print("RESUMO POR RECINTO")
print("=" * 130)
print()

if aparelhos_por_recinto:
    print(f"Total de Recintos: {len(aparelhos_por_recinto)}")
    print(f"Total de Aparelhos: {int(total_geral)}")
    print()
    print("-" * 130)
    print()
    
    # Ordenar por quantidade decrescente
    recintos_ordenados = sorted(aparelhos_por_recinto.items(), 
                               key=lambda x: x[1]['quantidade'], 
                               reverse=True)
    
    print(f"{'Recinto':<50} {'Aparelhos':>15} {'Itens':>10} {'PDFs':>30}")
    print("-" * 130)
    
    for recinto_id, dados in recintos_ordenados:
        pdfs_str = ', '.join([p.split('_')[2] for p in dados['pdfs']]) if len(dados['pdfs']) <= 3 else f"{len(dados['pdfs'])} PDFs"
        print(f"{recinto_id:<50} {int(dados['quantidade']):>15,} {dados['itens']:>10} {pdfs_str:>30}")
    
    # Salvar em JSON
    resultado_json = {
        'total_recintos': len(aparelhos_por_recinto),
        'total_aparelhos': int(total_geral),
        'recintos': {}
    }
    
    for recinto_id, dados in recintos_ordenados:
        resultado_json['recintos'][recinto_id] = {
            'quantidade': int(dados['quantidade']),
            'itens': dados['itens'],
            'pdfs': dados['pdfs']
        }
    
    with open('json/aparelhos_por_recinto.json', 'w', encoding='utf-8') as f:
        json.dump(resultado_json, f, ensure_ascii=False, indent=2)
    
    print()
    print("-" * 130)
    print(f"\nArquivo salvo: json/aparelhos_por_recinto.json")
    
else:
    print("⚠ Nenhum Recinto foi encontrado nos PDFs!")

print("\n" + "=" * 130)
