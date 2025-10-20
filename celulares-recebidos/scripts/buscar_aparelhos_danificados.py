import PyPDF2
import re
import json

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

# Palavras-chave para buscar danos/defeitos
palavras_dano = [
    'TRINCAD', 'QUEBRAD', 'AVARIAD', 'DANIFICAD',
    'DEFEITO', 'RACHAD', 'FRATURAD', 'PARTIDO',
    'SEM TELA', 'TELA QUEBRADA', 'TELA TRINCADA',
    'DISPLAY QUEBRADO', 'DISPLAY TRINCADO',
    'NAO LIGA', 'NÃO LIGA', 'INOPERANTE',
    'MAU ESTADO', 'MÁU ESTADO', 'SUCATA',
    'INUTILIZAVEL', 'INUTILIZÁVEL', 'DETERIORAD'
]

print("=" * 100)
print("PROCURANDO APARELHOS COM DESCRIÇÃO DE DANOS")
print("=" * 100)
print()
print("Palavras-chave buscadas:")
print(f"  {', '.join(palavras_dano)}")
print()
print("=" * 100)
print()

aparelhos_danificados = []
total_por_tipo_dano = {}
total_por_pdf = {}

for pdf_nome in pdfs:
    try:
        with open(pdf_nome, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            texto_completo = ""
            
            for page in pdf_reader.pages:
                texto_completo += page.extract_text() + "\n"
        
        linhas = texto_completo.split('\n')
        
        # Padrões para procurar aparelhos
        pattern = r'^(\d+,\d+)\s+un\s+(SMARTPHONE|TELEFONE\s+CELULAR|APARELHO|IPHONE|CELULAR)\s+(.+)'
        
        encontrados_neste_pdf = []
        
        for i, linha in enumerate(linhas):
            match = re.match(pattern, linha.strip(), re.IGNORECASE)
            
            if match:
                quantidade_str = match.group(1)
                tipo = match.group(2)
                descricao = match.group(3).strip()
                
                # Acumular descrição de linhas seguintes (até 10 linhas)
                partes_descricao = [descricao]
                
                for j in range(i+1, min(i+10, len(linhas))):
                    proxima_linha = linhas[j].strip()
                    
                    if re.match(r'^\d+,\d+\s+un\s+', proxima_linha, re.IGNORECASE):
                        break
                    if 'Subtotal:' in proxima_linha or 'Total' in proxima_linha:
                        break
                        
                    if proxima_linha:
                        partes_descricao.append(proxima_linha)
                        
                        if 'R$' in proxima_linha:
                            break
                
                descricao_completa = ' '.join(partes_descricao)
                
                # Verificar se contém palavras de dano
                descricao_upper = descricao_completa.upper()
                
                danos_encontrados = []
                for palavra in palavras_dano:
                    if palavra in descricao_upper:
                        danos_encontrados.append(palavra)
                
                if danos_encontrados:
                    # Extrair valor se houver
                    valor_match = re.search(r'R\$\s*([\d.]+,\d{2})', descricao_completa)
                    valor = valor_match.group(1) if valor_match else "Não encontrado"
                    
                    quantidade = float(quantidade_str.replace(',', '.'))
                    
                    item = {
                        'pdf': pdf_nome,
                        'quantidade': quantidade,
                        'tipo': tipo,
                        'descricao': descricao_completa[:200],  # Limitar tamanho
                        'valor': valor,
                        'danos': danos_encontrados
                    }
                    
                    aparelhos_danificados.append(item)
                    encontrados_neste_pdf.append(item)
                    
                    # Contabilizar por tipo de dano
                    for dano in danos_encontrados:
                        if dano not in total_por_tipo_dano:
                            total_por_tipo_dano[dano] = 0
                        total_por_tipo_dano[dano] += quantidade
        
        if encontrados_neste_pdf:
            total_por_pdf[pdf_nome] = len(encontrados_neste_pdf)
            print(f"📄 {pdf_nome}")
            print(f"   Encontrados: {len(encontrados_neste_pdf)} itens com descrição de danos")
            print()
            
            for item in encontrados_neste_pdf[:10]:  # Mostrar até 10 por PDF
                print(f"   • {item['quantidade']:.0f} un {item['tipo']}")
                print(f"     {item['descricao']}")
                print(f"     Valor: R$ {item['valor']}")
                print(f"     Danos detectados: {', '.join(item['danos'])}")
                print()
            
            if len(encontrados_neste_pdf) > 10:
                print(f"   ... e mais {len(encontrados_neste_pdf) - 10} itens")
                print()
    
    except Exception as e:
        print(f"❌ Erro ao processar {pdf_nome}: {e}")
        print()

print("=" * 100)
print("RESUMO GERAL")
print("=" * 100)
print()

if aparelhos_danificados:
    total_aparelhos_danificados = sum(item['quantidade'] for item in aparelhos_danificados)
    
    print(f"✓ Total de itens com descrição de danos: {len(aparelhos_danificados)}")
    print(f"✓ Total de aparelhos danificados: {int(total_aparelhos_danificados)} unidades")
    print()
    
    print("Distribuição por tipo de dano:")
    for dano, qtd in sorted(total_por_tipo_dano.items(), key=lambda x: x[1], reverse=True):
        print(f"  {dano}: {int(qtd)} unidades")
    print()
    
    print("Distribuição por PDF:")
    for pdf, qtd in sorted(total_por_pdf.items(), key=lambda x: x[1], reverse=True):
        print(f"  {pdf}: {qtd} itens")
    print()
    
    # Salvar em JSON
    with open('aparelhos_danificados.json', 'w', encoding='utf-8') as f:
        json.dump({
            'total_itens': len(aparelhos_danificados),
            'total_aparelhos': int(total_aparelhos_danificados),
            'por_tipo_dano': {k: int(v) for k, v in total_por_tipo_dano.items()},
            'por_pdf': total_por_pdf,
            'itens': aparelhos_danificados
        }, f, ensure_ascii=False, indent=2)
    
    print("Arquivo salvo: aparelhos_danificados.json")
    
else:
    print("✗ Nenhum aparelho com descrição de danos foi encontrado.")

print("=" * 100)
