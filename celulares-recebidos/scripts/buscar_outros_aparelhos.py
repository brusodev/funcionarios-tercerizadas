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

# Palavras-chave para EXCLUIR (celulares/smartphones)
excluir = ['SMARTPHONE', 'TELEFONE', 'CELULAR', 'IPHONE']

# Categorias de outros aparelhos para buscar
categorias_buscar = [
    'TABLET', 'IPAD', 'GALAXY TAB',
    'NOTEBOOK', 'LAPTOP', 'NETBOOK',
    'SMARTWATCH', 'RELOGIO', 'RELÓGIO', 'WATCH',
    'FONE', 'HEADPHONE', 'EARPHONE', 'EARBUD', 'AIRPOD',
    'CAIXA DE SOM', 'SPEAKER', 'ALTO-FALANTE',
    'CARREGADOR', 'FONTE', 'POWER BANK',
    'CABO', 'ADAPTADOR',
    'CAMERA', 'CÂMERA', 'WEBCAM',
    'MOUSE', 'TECLADO', 'KEYBOARD',
    'HD', 'SSD', 'PENDRIVE', 'CARTAO DE MEMORIA', 'CARTÃO DE MEMÓRIA',
    'MONITOR', 'DISPLAY',
    'ROTEADOR', 'ROUTER', 'MODEM',
    'CONSOLE', 'PLAYSTATION', 'XBOX', 'NINTENDO',
    'DRONE', 'GOPRO',
    'E-READER', 'KINDLE',
    'CHROMEBOOK', 'MACBOOK'
]

print("=" * 100)
print("PROCURANDO OUTROS TIPOS DE APARELHOS (NÃO CELULARES/SMARTPHONES)")
print("=" * 100)
print()

outros_aparelhos = []
categorias_encontradas = {}
total_por_pdf = {}

for pdf_nome in pdfs:
    try:
        with open(pdf_nome, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            texto_completo = ""
            
            for page in pdf_reader.pages:
                texto_completo += page.extract_text() + "\n"
        
        linhas = texto_completo.split('\n')
        
        # Procurar linhas com "un" e valor R$
        pattern = r'^(\d+,?\d*)\s+un\s+(.+)'
        
        encontrados_neste_pdf = []
        
        for i, linha in enumerate(linhas):
            match = re.match(pattern, linha.strip(), re.IGNORECASE)
            
            if match:
                quantidade_str = match.group(1)
                descricao = match.group(2).strip()
                
                # Verificar se NÃO é celular/smartphone
                descricao_upper = descricao.upper()
                
                # Pular se for celular/smartphone
                eh_celular = False
                for palavra_excluir in excluir:
                    if descricao_upper.startswith(palavra_excluir):
                        eh_celular = True
                        break
                
                if eh_celular:
                    continue
                
                # Acumular descrição de linhas seguintes
                partes_descricao = [descricao]
                
                for j in range(i+1, min(i+10, len(linhas))):
                    proxima_linha = linhas[j].strip()
                    
                    if re.match(r'^\d+,?\d*\s+un\s+', proxima_linha, re.IGNORECASE):
                        break
                    if 'Subtotal:' in proxima_linha or 'Total' in proxima_linha:
                        break
                        
                    if proxima_linha:
                        partes_descricao.append(proxima_linha)
                        
                        if 'R$' in proxima_linha:
                            break
                
                descricao_completa = ' '.join(partes_descricao)
                descricao_upper_completa = descricao_completa.upper()
                
                # Verificar se contém alguma categoria de interesse
                categoria_detectada = None
                for categoria in categorias_buscar:
                    if categoria in descricao_upper_completa:
                        categoria_detectada = categoria
                        break
                
                # Se não encontrou categoria específica mas tem valor, pode ser outro tipo
                valor_match = re.search(r'R\$\s*([\d.]+,\d{2})', descricao_completa)
                
                if valor_match or categoria_detectada:
                    try:
                        quantidade = float(quantidade_str.replace(',', '.'))
                    except:
                        quantidade = 1.0
                    
                    valor = valor_match.group(1) if valor_match else "Não encontrado"
                    
                    item = {
                        'pdf': pdf_nome,
                        'quantidade': quantidade,
                        'descricao': descricao_completa[:250],
                        'valor': valor,
                        'categoria': categoria_detectada if categoria_detectada else 'OUTROS'
                    }
                    
                    outros_aparelhos.append(item)
                    encontrados_neste_pdf.append(item)
                    
                    # Contabilizar por categoria
                    cat = categoria_detectada if categoria_detectada else 'OUTROS'
                    if cat not in categorias_encontradas:
                        categorias_encontradas[cat] = {'quantidade': 0, 'itens': 0}
                    categorias_encontradas[cat]['quantidade'] += quantidade
                    categorias_encontradas[cat]['itens'] += 1
        
        if encontrados_neste_pdf:
            total_por_pdf[pdf_nome] = len(encontrados_neste_pdf)
            print(f"📄 {pdf_nome}")
            print(f"   Encontrados: {len(encontrados_neste_pdf)} itens (não celulares)")
            print()
            
            for item in encontrados_neste_pdf[:15]:  # Mostrar até 15 por PDF
                print(f"   • {item['quantidade']:.0f} un - [{item['categoria']}]")
                print(f"     {item['descricao']}")
                print(f"     Valor: R$ {item['valor']}")
                print()
            
            if len(encontrados_neste_pdf) > 15:
                print(f"   ... e mais {len(encontrados_neste_pdf) - 15} itens")
                print()
    
    except Exception as e:
        print(f"❌ Erro ao processar {pdf_nome}: {e}")
        print()

print("=" * 100)
print("RESUMO GERAL")
print("=" * 100)
print()

if outros_aparelhos:
    total_unidades = sum(item['quantidade'] for item in outros_aparelhos)
    
    print(f"✓ Total de tipos diferentes: {len(outros_aparelhos)} itens")
    print(f"✓ Total de unidades: {int(total_unidades)}")
    print()
    
    print("Distribuição por categoria:")
    for cat, dados in sorted(categorias_encontradas.items(), key=lambda x: x[1]['quantidade'], reverse=True):
        print(f"  {cat}: {int(dados['quantidade'])} unidades ({dados['itens']} tipos diferentes)")
    print()
    
    if total_por_pdf:
        print("Distribuição por PDF:")
        for pdf, qtd in sorted(total_por_pdf.items(), key=lambda x: x[1], reverse=True):
            print(f"  {pdf}: {qtd} tipos")
        print()
    
    # Salvar em JSON
    with open('outros_aparelhos.json', 'w', encoding='utf-8') as f:
        json.dump({
            'total_itens': len(outros_aparelhos),
            'total_unidades': int(total_unidades),
            'por_categoria': {k: {'quantidade': int(v['quantidade']), 'itens': v['itens']} 
                             for k, v in categorias_encontradas.items()},
            'por_pdf': total_por_pdf,
            'itens': outros_aparelhos
        }, f, ensure_ascii=False, indent=2)
    
    print("Arquivo salvo: outros_aparelhos.json")
    
else:
    print("✗ Nenhum outro tipo de aparelho foi encontrado.")

print("=" * 100)
