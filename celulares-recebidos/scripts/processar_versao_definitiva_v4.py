import PyPDF2
import json
import csv
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
    valor_str = valor_str.replace("R$", "").strip()
    valor_str = valor_str.replace(".", "").replace(",", ".")
    try:
        return float(valor_str)
    except:
        return 0.0

def extrair_linhas_com_valores_v4(texto, nome_pdf):
    """
    VERSÃO 4 - DEFINITIVA
    Aceita todos os padrões encontrados:
    - SMARTPHONE
    - TELEFONE CELULAR
    - CELULAR (sem TELEFONE antes)
    - IPHONE
    - APARELHO CELULAR
    """
    linhas = texto.split('\n')
    resultados = []
    
    # Padrão DEFINITIVO: aceita todos os tipos de celular
    padrao_linha = re.compile(
        r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades|kg)\s+((?:SMARTPHONE|TELEFONE\s+CELULAR|APARELHO\s+CELULAR|IPHONE|(?<!TELEFONE\s)(?<!APARELHO\s)CELULAR).*)', 
        re.IGNORECASE
    )
    
    # Padrão para valores
    padrao_valor = re.compile(r'R\$\s*([\d.,]+)')
    
    # Padrão para detectar linhas que são códigos
    padrao_codigo = re.compile(r'^\d+\s*-\s*\d+')
    
    i = 0
    while i < len(linhas):
        linha_atual = linhas[i].strip()
        
        # Pula linhas de código
        if padrao_codigo.match(linha_atual):
            i += 1
            continue
        
        match = padrao_linha.match(linha_atual)
        
        if match:
            quantidade_str = match.group(1)
            descricao = match.group(2).strip()
            
            # Se descrição estiver vazia, usa um texto padrão
            if not descricao or descricao in ['///', '//']:
                descricao = "SMARTPHONE (SEM MODELO ESPECIFICADO)"
            
            quantidade = float(quantidade_str.replace(',', '.'))
            
            # Procura valor nas próximas 10 linhas
            valor_encontrado = None
            valor_numerico = 0.0
            linhas_busca = 10
            
            for offset in range(linhas_busca):
                if i + offset < len(linhas):
                    linha_busca = linhas[i + offset]
                    match_valor = padrao_valor.search(linha_busca)
                    
                    if match_valor:
                        valor_encontrado = match_valor.group(1)
                        valor_numerico = normalizar_valor(valor_encontrado)
                        break
                    
                    # Para se encontrar uma nova linha de item
                    if offset > 0 and padrao_linha.match(linhas[i + offset].strip()) and not padrao_codigo.match(linhas[i + offset].strip()):
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

def processar_pdfs_versao_definitiva():
    """Processa todos os PDFs com o padrão DEFINITIVO"""
    pasta_atual = Path('.')
    pdfs = sorted(list(pasta_atual.glob('ADM *.PDF')))
    
    # Remove duplicatas
    pdfs_unicos = {}
    for pdf in pdfs:
        caminho_resolvido = pdf.resolve()
        pdfs_unicos[caminho_resolvido] = pdf
    
    pdfs = list(pdfs_unicos.values())
    
    print("="*80)
    print("PROCESSAMENTO COM PADRÃO DEFINITIVO V4")
    print("="*80)
    print("✅ Agora aceita: SMARTPHONE, TELEFONE CELULAR, CELULAR, IPHONE, APARELHO CELULAR")
    print(f"📄 {len(pdfs)} PDFs encontrados\n")
    
    # Estruturas de dados
    todas_linhas = []
    dados_por_pdf = {}
    totais_gerais = {
        'total_pdfs': 0,
        'total_aparelhos': 0,
        'total_linhas': 0,
        'total_valor': 0.0,
        'total_descricoes_unicas': 0
    }
    
    todas_descricoes_unicas = set()
    modelos_consolidados = defaultdict(lambda: {'quantidade': 0, 'valor_total': 0.0})
    
    for pdf in pdfs:
        print(f"Processando: {pdf.name}")
        
        texto = extrair_texto_pdf(pdf)
        linhas_extraidas = extrair_linhas_com_valores_v4(texto, pdf.name)
        
        todas_linhas.extend(linhas_extraidas)
        
        # Estatísticas por PDF
        modelos_pdf = defaultdict(lambda: {'quantidade': 0, 'valor_total': 0.0})
        total_aparelhos_pdf = 0
        total_valor_pdf = 0.0
        
        for linha in linhas_extraidas:
            descricao = linha['descricao']
            quantidade = linha['quantidade']
            valor = linha['valor_numerico']
            
            modelos_pdf[descricao]['quantidade'] += quantidade
            modelos_pdf[descricao]['valor_total'] += valor
            
            modelos_consolidados[descricao]['quantidade'] += quantidade
            modelos_consolidados[descricao]['valor_total'] += valor
            
            total_aparelhos_pdf += quantidade
            total_valor_pdf += valor
            
            todas_descricoes_unicas.add(descricao)
        
        # Calcula valor médio por unidade
        for modelo, dados in modelos_pdf.items():
            if dados['quantidade'] > 0:
                dados['valor_medio_unitario'] = dados['valor_total'] / dados['quantidade']
            else:
                dados['valor_medio_unitario'] = 0.0
        
        # Ordena por quantidade
        modelos_ordenados = dict(sorted(
            modelos_pdf.items(),
            key=lambda x: x[1]['quantidade'],
            reverse=True
        ))
        
        top_10 = dict(list(modelos_ordenados.items())[:10])
        valor_medio_aparelho = total_valor_pdf / total_aparelhos_pdf if total_aparelhos_pdf > 0 else 0.0
        
        dados_por_pdf[pdf.name] = {
            'nome_arquivo': pdf.name,
            'total_aparelhos': int(total_aparelhos_pdf),
            'total_linhas': len(linhas_extraidas),
            'total_descricoes_unicas': len(modelos_pdf),
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
        
        totais_gerais['total_aparelhos'] += total_aparelhos_pdf
        totais_gerais['total_linhas'] += len(linhas_extraidas)
        totais_gerais['total_valor'] += total_valor_pdf
        
        print(f"   ✓ {int(total_aparelhos_pdf)} aparelhos | R$ {total_valor_pdf:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    totais_gerais['total_pdfs'] = len(pdfs)
    totais_gerais['total_descricoes_unicas'] = len(todas_descricoes_unicas)
    totais_gerais['total_aparelhos'] = int(totais_gerais['total_aparelhos'])
    totais_gerais['total_valor'] = round(totais_gerais['total_valor'], 2)
    
    if totais_gerais['total_aparelhos'] > 0:
        totais_gerais['valor_medio_por_aparelho'] = round(
            totais_gerais['total_valor'] / totais_gerais['total_aparelhos'], 2
        )
    else:
        totais_gerais['valor_medio_por_aparelho'] = 0.0
    
    # Salva JSON consolidado por modelo
    for modelo, dados in modelos_consolidados.items():
        if dados['quantidade'] > 0:
            dados['valor_medio_unitario'] = dados['valor_total'] / dados['quantidade']
        else:
            dados['valor_medio_unitario'] = 0.0
    
    modelos_final = {
        modelo: {
            'quantidade': int(dados['quantidade']),
            'valor_total': round(dados['valor_total'], 2),
            'valor_medio_unitario': round(dados['valor_medio_unitario'], 2)
        }
        for modelo, dados in sorted(modelos_consolidados.items(), key=lambda x: x[1]['quantidade'], reverse=True)
    }
    
    resultado_modelos = {
        'resumo': totais_gerais,
        'modelos_com_valores': modelos_final
    }
    
    with open('celulares_com_valores_DEFINITIVO.json', 'w', encoding='utf-8') as f:
        json.dump(resultado_modelos, f, ensure_ascii=False, indent=2)
    
    # Salva JSON por PDF
    resultado_por_pdf = {
        'resumo_geral': totais_gerais,
        'pdfs': dados_por_pdf
    }
    
    with open('celulares_por_pdf_com_valores_DEFINITIVO.json', 'w', encoding='utf-8') as f:
        json.dump(resultado_por_pdf, f, ensure_ascii=False, indent=2)
    
    # Salva CSV detalhado
    with open('celulares_com_valores_DEFINITIVO.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['PDF', 'Quantidade', 'Descrição', 'Valor (texto)', 'Valor (numérico)', 'Linha Original'])
        for linha in todas_linhas:
            writer.writerow([
                linha['pdf'],
                linha['quantidade'],
                linha['descricao'],
                linha['valor_texto'],
                linha['valor_numerico'],
                linha['linha_original']
            ])
    
    # Resumo final
    print("\n" + "="*80)
    print("RESUMO FINAL (VERSÃO 4 - DEFINITIVA)")
    print("="*80)
    print(f"Total de PDFs: {totais_gerais['total_pdfs']}")
    print(f"Total de aparelhos: {totais_gerais['total_aparelhos']:,}".replace(',', '.'))
    print(f"Total de linhas: {totais_gerais['total_linhas']:,}".replace(',', '.'))
    print(f"Descrições únicas: {totais_gerais['total_descricoes_unicas']:,}".replace(',', '.'))
    print(f"Valor total: R$ {totais_gerais['total_valor']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print(f"Valor médio/aparelho: R$ {totais_gerais['valor_medio_por_aparelho']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    # Comparação com versões anteriores
    print("\n" + "="*80)
    print("EVOLUÇÃO DAS VERSÕES:")
    print("="*80)
    print("V1: 31,703 aparelhos | R$ 28,851,564.47")
    print("V2: 31,706 aparelhos | R$ 28,858,472.77")
    print("V3: 31,714 aparelhos | R$ 28,861,997.77")
    print(f"V4 DEFINITIVO: {totais_gerais['total_aparelhos']:,}".replace(',', '.') + f" aparelhos | R$ {totais_gerais['total_valor']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    # Verificações específicas
    pdfs_verificar = {
        'ADM 0800100_0746_2025 de 30_09_2025.PDF': {'esperado_qtd': 2544, 'esperado_valor': 3050180.53},
        'ADM 0800100_0743_2025 de 30_09_2025.PDF': {'esperado_qtd': 912, 'esperado_valor': 1555781.16}
    }
    
    print("\n" + "="*80)
    print("VERIFICAÇÕES ESPECÍFICAS:")
    print("="*80)
    
    for pdf_nome, esperado in pdfs_verificar.items():
        if pdf_nome in dados_por_pdf:
            pdf_data = dados_por_pdf[pdf_nome]
            diff_qtd = pdf_data['total_aparelhos'] - esperado['esperado_qtd']
            diff_valor = pdf_data['valor_total'] - esperado['esperado_valor']
            
            print(f"\n📄 {pdf_nome}:")
            print(f"   Esperado:   {esperado['esperado_qtd']} aparelhos | R$ {esperado['esperado_valor']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            print(f"   Encontrado: {pdf_data['total_aparelhos']} aparelhos | R$ {pdf_data['valor_total']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            
            status_qtd = "✅" if abs(diff_qtd) == 0 else "⚠️"
            status_valor = "✅" if abs(diff_valor) < 1.0 else "⚠️"
            
            print(f"   Diferença:  {status_qtd} {diff_qtd:+d} aparelhos | {status_valor} R$ {diff_valor:+,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    print("\n" + "="*80)
    print("✅ Arquivos gerados (versão DEFINITIVA):")
    print("   - celulares_com_valores_DEFINITIVO.json")
    print("   - celulares_por_pdf_com_valores_DEFINITIVO.json")
    print("   - celulares_com_valores_DEFINITIVO.csv")
    print("="*80)

if __name__ == "__main__":
    processar_pdfs_versao_definitiva()
