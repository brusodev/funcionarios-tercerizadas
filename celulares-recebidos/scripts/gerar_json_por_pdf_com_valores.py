import PyPDF2
import json
import re
from pathlib import Path
from collections import defaultdict

def extrair_texto_pdf(caminho_pdf):
    """Extrai todo o texto de um PDF"""
    texto = ""
    try:
        with open(caminho_pdf, 'rb') as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)
            for pagina in leitor.pages:
                texto += pagina.extract_text() + "\n"
    except Exception as e:
        print(f"Erro ao ler {caminho_pdf}: {e}")
    return texto

def normalizar_valor(valor_str):
    """Converte string de valor brasileiro para float"""
    if not valor_str:
        return 0.0
    # Remove "R$" e espaços
    valor_str = valor_str.replace("R$", "").strip()
    # Remove pontos de milhar e substitui vírgula por ponto
    valor_str = valor_str.replace(".", "").replace(",", ".")
    try:
        return float(valor_str)
    except:
        return 0.0

def extrair_linhas_com_valores(texto, nome_pdf):
    """Extrai linhas com quantidade, descrição e valor"""
    linhas = texto.split('\n')
    resultados = []
    
    # Padrão para linhas com quantidade e descrição
    padrao_linha = re.compile(r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades)\s+((?:SMARTPHONE|TELEFONE\s+CELULAR)\s+.+)', re.IGNORECASE)
    
    # Padrão para valores
    padrao_valor = re.compile(r'R\$\s*([\d.,]+)')
    
    i = 0
    while i < len(linhas):
        linha_atual = linhas[i].strip()
        match = padrao_linha.match(linha_atual)
        
        if match:
            quantidade_str = match.group(1)
            descricao = match.group(2).strip()
            
            # Converte quantidade (formato brasileiro com vírgula)
            quantidade = float(quantidade_str.replace(',', '.'))
            
            # Procura valor na linha atual e nas próximas 5 linhas
            valor_encontrado = None
            valor_numerico = 0.0
            linhas_busca = 6  # linha atual + 5 próximas
            
            for offset in range(linhas_busca):
                if i + offset < len(linhas):
                    linha_busca = linhas[i + offset]
                    match_valor = padrao_valor.search(linha_busca)
                    
                    if match_valor:
                        valor_encontrado = match_valor.group(1)
                        valor_numerico = normalizar_valor(valor_encontrado)
                        break
                    
                    # Para se encontrar uma nova linha de item
                    if offset > 0 and padrao_linha.match(linhas[i + offset].strip()):
                        break
            
            resultados.append({
                'pdf': nome_pdf,
                'quantidade': quantidade,
                'descricao': descricao,
                'valor_texto': valor_encontrado if valor_encontrado else '',
                'valor_numerico': valor_numerico,
                'linha_original': linha_atual
            })
        
        i += 1
    
    return resultados

def processar_pdfs_com_valores():
    """Processa todos os PDFs e gera JSON detalhado por PDF com valores"""
    pasta_atual = Path('.')
    pdfs = sorted(list(pasta_atual.glob('ADM *.PDF')))
    
    # Remove duplicatas (mesmo arquivo com caminhos diferentes)
    pdfs_unicos = {}
    for pdf in pdfs:
        caminho_resolvido = pdf.resolve()
        pdfs_unicos[caminho_resolvido] = pdf
    
    pdfs = list(pdfs_unicos.values())
    
    print(f"Encontrados {len(pdfs)} PDFs únicos")
    
    # Estrutura para armazenar dados por PDF
    dados_por_pdf = {}
    totais_gerais = {
        'total_pdfs': 0,
        'total_aparelhos': 0,
        'total_linhas': 0,
        'total_valor': 0.0,
        'total_descricoes_unicas': 0
    }
    
    todas_descricoes_unicas = set()
    
    for pdf in pdfs:
        print(f"Processando: {pdf.name}")
        
        texto = extrair_texto_pdf(pdf)
        linhas_extraidas = extrair_linhas_com_valores(texto, pdf.name)
        
        # Agrupa por descrição para este PDF
        modelos_dict = defaultdict(lambda: {'quantidade': 0, 'valor_total': 0.0})
        
        total_aparelhos_pdf = 0
        total_valor_pdf = 0.0
        
        for linha in linhas_extraidas:
            descricao = linha['descricao']
            quantidade = linha['quantidade']
            valor = linha['valor_numerico']
            
            modelos_dict[descricao]['quantidade'] += quantidade
            modelos_dict[descricao]['valor_total'] += valor
            
            total_aparelhos_pdf += quantidade
            total_valor_pdf += valor
            
            todas_descricoes_unicas.add(descricao)
        
        # Calcula valor médio por unidade para cada modelo
        for modelo, dados in modelos_dict.items():
            if dados['quantidade'] > 0:
                dados['valor_medio_unitario'] = dados['valor_total'] / dados['quantidade']
            else:
                dados['valor_medio_unitario'] = 0.0
        
        # Ordena modelos por quantidade (decrescente)
        modelos_ordenados = dict(sorted(
            modelos_dict.items(),
            key=lambda x: x[1]['quantidade'],
            reverse=True
        ))
        
        # Top 10 para este PDF
        top_10 = dict(list(modelos_ordenados.items())[:10])
        
        # Calcula valor médio por aparelho neste PDF
        valor_medio_aparelho = total_valor_pdf / total_aparelhos_pdf if total_aparelhos_pdf > 0 else 0.0
        
        dados_por_pdf[pdf.name] = {
            'nome_arquivo': pdf.name,
            'total_aparelhos': int(total_aparelhos_pdf),
            'total_linhas': len(linhas_extraidas),
            'total_descricoes_unicas': len(modelos_dict),
            'valor_total': round(total_valor_pdf, 2),
            'valor_medio_por_aparelho': round(valor_medio_aparelho, 2),
            'top_10_modelos': {
                modelo: {
                    'quantidade': int(dados['quantidade']),
                    'valor_total': round(dados['valor_total'], 2),
                    'valor_medio_unitario': round(dados['valor_medio_unitario'], 2)
                }
                for modelo, dados in top_10.items()
            },
            'todos_modelos': {
                modelo: {
                    'quantidade': int(dados['quantidade']),
                    'valor_total': round(dados['valor_total'], 2),
                    'valor_medio_unitario': round(dados['valor_medio_unitario'], 2)
                }
                for modelo, dados in modelos_ordenados.items()
            }
        }
        
        # Atualiza totais gerais
        totais_gerais['total_aparelhos'] += total_aparelhos_pdf
        totais_gerais['total_linhas'] += len(linhas_extraidas)
        totais_gerais['total_valor'] += total_valor_pdf
    
    totais_gerais['total_pdfs'] = len(pdfs)
    totais_gerais['total_descricoes_unicas'] = len(todas_descricoes_unicas)
    totais_gerais['total_aparelhos'] = int(totais_gerais['total_aparelhos'])
    totais_gerais['total_valor'] = round(totais_gerais['total_valor'], 2)
    
    # Calcula valor médio geral
    if totais_gerais['total_aparelhos'] > 0:
        totais_gerais['valor_medio_por_aparelho'] = round(
            totais_gerais['total_valor'] / totais_gerais['total_aparelhos'], 2
        )
    else:
        totais_gerais['valor_medio_por_aparelho'] = 0.0
    
    # Monta estrutura final
    resultado_final = {
        'resumo_geral': totais_gerais,
        'pdfs': dados_por_pdf
    }
    
    # Salva JSON
    with open('celulares_por_pdf_com_valores.json', 'w', encoding='utf-8') as f:
        json.dump(resultado_final, f, ensure_ascii=False, indent=2)
    
    # Exibe resumo
    print("\n" + "="*70)
    print("RESUMO GERAL")
    print("="*70)
    print(f"Total de PDFs processados: {totais_gerais['total_pdfs']}")
    print(f"Total de aparelhos: {totais_gerais['total_aparelhos']:,}".replace(',', '.'))
    print(f"Total de linhas: {totais_gerais['total_linhas']:,}".replace(',', '.'))
    print(f"Descrições únicas: {totais_gerais['total_descricoes_unicas']:,}".replace(',', '.'))
    print(f"Valor total: R$ {totais_gerais['total_valor']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print(f"Valor médio por aparelho: R$ {totais_gerais['valor_medio_por_aparelho']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print()
    
    # Exibe resumo por PDF
    print("="*70)
    print("RESUMO POR PDF")
    print("="*70)
    for nome_pdf, dados in dados_por_pdf.items():
        print(f"\n📄 {nome_pdf}")
        print(f"   Aparelhos: {dados['total_aparelhos']:,}".replace(',', '.'))
        print(f"   Linhas: {dados['total_linhas']:,}".replace(',', '.'))
        print(f"   Valor total: R$ {dados['valor_total']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        print(f"   Valor médio: R$ {dados['valor_medio_por_aparelho']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        
        # Mostra top 3 deste PDF
        print(f"   Top 3 modelos:")
        for i, (modelo, info) in enumerate(list(dados['top_10_modelos'].items())[:3], 1):
            print(f"     {i}. {modelo[:60]}... - {info['quantidade']} un | R$ {info['valor_total']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    print("\n" + "="*70)
    print(f"✅ JSON salvo em: celulares_por_pdf_com_valores.json")
    print("="*70)

if __name__ == "__main__":
    processar_pdfs_com_valores()
