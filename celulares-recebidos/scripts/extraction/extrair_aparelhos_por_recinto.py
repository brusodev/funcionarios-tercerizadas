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

# Valores de referência por PDF
valores_referencia = {
    'ADM 0800100_0733_2025 de 30_09_2025.PDF': {'aparelhos': 13, 'valor': 7879.62},
    'ADM 0800100_0734_2025 de 30_09_2025.PDF': {'aparelhos': 6879, 'valor': 5716622.03},
    'ADM 0800100_0740_2025 de 30_09_2025.PDF': {'aparelhos': 9, 'valor': 3950.54},
    'ADM 0800100_0741_2025 de 30_09_2025.PDF': {'aparelhos': 19, 'valor': 18816.20},
    'ADM 0800100_0742_2025 de 30_09_2025.PDF': {'aparelhos': 225, 'valor': 84426.55},
    'ADM 0800100_0743_2025 de 30_09_2025.PDF': {'aparelhos': 912, 'valor': 1555781.16},
    'ADM 0800100_0744_2025 de 30_09_2025.PDF': {'aparelhos': 3457, 'valor': 3465958.49},
    'ADM 0800100_0735_2025 de 30_09_2025.PDF': {'aparelhos': 3804, 'valor': 2845357.66},
    'ADM 0800100_0736_2025 de 30_09_2025.PDF': {'aparelhos': 1873, 'valor': 2744064.74},
    'ADM 0800100_0737_2025 de 30_09_2025.PDF': {'aparelhos': 616, 'valor': 280644.01},
    'ADM 0800100_0738_2025 de 30_09_2025.PDF': {'aparelhos': 442, 'valor': 486866.60},
    'ADM 0800100_0739_2025 de 30_09_2025.PDF': {'aparelhos': 3708, 'valor': 1870406.44},
    'ADM 0800100_0745_2025 de 30_09_2025.PDF': {'aparelhos': 3390, 'valor': 4644268.78},
    'ADM 0800100_0746_2025 de 30_09_2025.PDF': {'aparelhos': 2544, 'valor': 3050180.53},
    'ADM 0800100_0747_2025 de 30092025.PDF': {'aparelhos': 4124, 'valor': 3466230.15}
}

def extrair_recinto_pdf(pdf_path):
    """Extrai informações de Recinto do PDF e agrupa aparelhos por Recinto"""
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        texto_completo = ""
        
        for page in pdf_reader.pages:
            texto_completo += page.extract_text() + "\n"
    
    linhas = texto_completo.split('\n')
    
    # Procurar por padrão "Recinto: XXX - XXXXX ..."
    # Exemplo: "Recinto: 305 - 810300 Regional DMA - Bauru/SP"
    pattern_recinto = r'Recinto:\s*(\d+)\s*-\s*(\d+)\s+(.+?)(?:\n|$)'
    
    recintos = {}
    
    for i, linha in enumerate(linhas):
        match = re.search(pattern_recinto, linha)
        if match:
            num_recinto = match.group(1)
            codigo_recinto = match.group(2)
            nome_recinto = match.group(3).strip()
            
            recinto_id = f"{num_recinto} - {codigo_recinto} {nome_recinto}"
            
            if recinto_id not in recintos:
                recintos[recinto_id] = {
                    'numero': num_recinto,
                    'codigo': codigo_recinto,
                    'nome': nome_recinto,
                    'aparelhos': 0,
                    'itens': []
                }
    
    # Se encontrou recintos, procurar aparelhos para cada um
    if recintos:
        # Procurar linhas com aparelhos
        pattern_aparelho = r'^(\d+,\d+)\s+un\s+(SMARTPHONE|TELEFONE\s+CELULAR|APARELHO|IPHONE|CELULAR)\s+(.+)'
        
        recinto_atual = None
        
        for i, linha in enumerate(linhas):
            # Verificar se é linha de recinto
            match_recinto = re.search(pattern_recinto, linha)
            if match_recinto:
                num_recinto = match_recinto.group(1)
                codigo_recinto = match_recinto.group(2)
                nome_recinto = match_recinto.group(3).strip()
                recinto_atual = f"{num_recinto} - {codigo_recinto} {nome_recinto}"
                continue
            
            # Verificar se é linha de aparelho
            match_aparelho = re.match(pattern_aparelho, linha.strip(), re.IGNORECASE)
            
            if match_aparelho and recinto_atual:
                quantidade_str = match_aparelho.group(1)
                quantidade = float(quantidade_str.replace(',', '.'))
                
                tipo = match_aparelho.group(2)
                descricao = match_aparelho.group(3).strip()
                
                # Acumular descrição de linhas seguintes
                partes_descricao = [descricao]
                
                for j in range(i+1, min(i+10, len(linhas))):
                    proxima_linha = linhas[j].strip()
                    
                    if re.match(r'^\d+,\d+\s+un\s+', proxima_linha, re.IGNORECASE):
                        break
                    if 'Subtotal:' in proxima_linha or 'Recinto:' in proxima_linha:
                        break
                        
                    if proxima_linha:
                        partes_descricao.append(proxima_linha)
                        
                        if 'R$' in proxima_linha:
                            break
                
                descricao_completa = ' '.join(partes_descricao)
                
                # Extrair valor
                valor_match = re.search(r'R\$\s*([\d.]+,\d{2})', descricao_completa)
                valor = valor_match.group(1) if valor_match else "N/A"
                
                recintos[recinto_atual]['aparelhos'] += quantidade
                recintos[recinto_atual]['itens'].append({
                    'quantidade': quantidade,
                    'tipo': tipo,
                    'descricao': descricao_completa[:150],
                    'valor': valor
                })
    
    return recintos

print("=" * 120)
print("EXTRAÇÃO DE APARELHOS POR RECINTO")
print("=" * 120)
print()

aparelhos_por_recinto = defaultdict(lambda: {'quantidade': 0, 'pdf': [], 'detalhes': []})
total_geral = 0

for pdf_nome in pdfs:
    print(f"Processando: {pdf_nome}...")
    
    try:
        recintos = extrair_recinto_pdf(pdf_nome)
        
        if recintos:
            for recinto_id, dados in recintos.items():
                aparelhos_por_recinto[recinto_id]['quantidade'] += dados['aparelhos']
                if pdf_nome not in aparelhos_por_recinto[recinto_id]['pdf']:
                    aparelhos_por_recinto[recinto_id]['pdf'].append(pdf_nome)
                
                total_geral += dados['aparelhos']
                
                # Guardar detalhes dos primeiros itens
                for item in dados['itens'][:3]:
                    aparelhos_por_recinto[recinto_id]['detalhes'].append(item)
        else:
            print(f"  ⚠ Nenhum Recinto encontrado neste PDF")
    
    except Exception as e:
        print(f"  ❌ Erro: {e}")
    
    print()

print("=" * 120)
print("RESUMO POR RECINTO")
print("=" * 120)
print()

if aparelhos_por_recinto:
    print(f"Total de Recintos: {len(aparelhos_por_recinto)}")
    print(f"Total de Aparelhos: {int(total_geral)}")
    print()
    print("-" * 120)
    print()
    
    # Ordenar por quantidade decrescente
    recintos_ordenados = sorted(aparelhos_por_recinto.items(), 
                               key=lambda x: x[1]['quantidade'], 
                               reverse=True)
    
    for recinto_id, dados in recintos_ordenados:
        print(f"Recinto: {recinto_id}")
        print(f"  Aparelhos: {int(dados['quantidade'])} unidades")
        print(f"  PDFs: {', '.join(dados['pdf'])}")
        print()
    
    # Salvar em JSON
    resultado_json = {
        'total_recintos': len(aparelhos_por_recinto),
        'total_aparelhos': int(total_geral),
        'recintos': {}
    }
    
    for recinto_id, dados in recintos_ordenados:
        resultado_json['recintos'][recinto_id] = {
            'quantidade': int(dados['quantidade']),
            'pdfs': dados['pdf'],
            'exemplos_itens': dados['detalhes'][:5]
        }
    
    with open('aparelhos_por_recinto.json', 'w', encoding='utf-8') as f:
        json.dump(resultado_json, f, ensure_ascii=False, indent=2)
    
    print("-" * 120)
    print(f"\nArquivo salvo: aparelhos_por_recinto.json")
    
else:
    print("⚠ Nenhum Recinto foi encontrado nos PDFs!")
    print("\nProcurando padrões alternativos de 'Recinto'...")
    
    # Tentar padrão alternativo
    for pdf_nome in pdfs[:3]:  # Verificar primeiros 3 PDFs
        try:
            with open(pdf_nome, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                texto = pdf_reader.pages[0].extract_text()
                
            print(f"\n{pdf_nome}:")
            print("Primeiras linhas:")
            linhas = texto.split('\n')
            for i, linha in enumerate(linhas[:50]):
                if linha.strip():
                    print(f"  {i}: {linha[:100]}")
        except:
            pass

print("\n" + "=" * 120)
