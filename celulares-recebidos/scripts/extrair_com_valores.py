import os
import json
import re
from pathlib import Path
from collections import defaultdict

try:
    import PyPDF2
except ImportError:
    print("PyPDF2 não está instalado. Instalando...")
    os.system("pip install PyPDF2")
    import PyPDF2

def extrair_texto_pdf(caminho_pdf):
    """Extrai texto de um arquivo PDF."""
    texto = ""
    try:
        with open(caminho_pdf, 'rb') as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)
            for pagina in leitor.pages:
                texto += pagina.extract_text() + "\n"
    except Exception as e:
        print(f"Erro ao ler {caminho_pdf}: {e}")
    return texto

def extrair_linhas_com_valores(texto):
    """
    Extrai linhas que começam com quantidade + un + SMARTPHONE/TELEFONE CELULAR
    e tenta capturar o valor R$ que pode estar na mesma linha ou nas próximas.
    """
    linhas = []
    texto_linhas = texto.split('\n')
    
    i = 0
    while i < len(texto_linhas):
        linha = texto_linhas[i]
        
        # Procura por linhas que começam com quantidade + un + SMARTPHONE/TELEFONE CELULAR
        match = re.match(
            r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades)\s+((?:SMARTPHONE|TELEFONE\s+CELULAR)\s+.+)',
            linha,
            re.IGNORECASE
        )
        
        if match:
            quantidade_str = match.group(1).replace(',', '.')
            descricao = match.group(2).strip()
            
            try:
                quantidade = int(float(quantidade_str))
                
                # Procura pelo valor R$ na mesma linha ou nas próximas 5 linhas
                valor_encontrado = None
                linha_completa = linha
                
                # Primeiro tenta na própria linha
                valor_match = re.search(r'R\$\s*([\d.,]+)', linha)
                if valor_match:
                    valor_encontrado = valor_match.group(1)
                else:
                    # Procura nas próximas linhas (até 5 linhas à frente)
                    for j in range(1, min(6, len(texto_linhas) - i)):
                        proxima_linha = texto_linhas[i + j]
                        
                        # Para se encontrar outra linha de aparelho (evita pegar valor errado)
                        if re.match(r'^\d+(?:,\d+)?\s+(?:un|unidade)', proxima_linha, re.IGNORECASE):
                            break
                        
                        valor_match = re.search(r'R\$\s*([\d.,]+)', proxima_linha)
                        if valor_match:
                            valor_encontrado = valor_match.group(1)
                            linha_completa += " " + proxima_linha.strip()
                            break
                
                # Converte o valor para float se encontrado
                valor_numerico = None
                if valor_encontrado:
                    try:
                        # Remove pontos de milhar e substitui vírgula por ponto
                        valor_limpo = valor_encontrado.replace('.', '').replace(',', '.')
                        valor_numerico = float(valor_limpo)
                    except:
                        pass
                
                linhas.append((quantidade, descricao, valor_encontrado, valor_numerico, linha_completa))
                
            except ValueError:
                pass
        
        i += 1
    
    return linhas

def processar_pdfs_com_valores(diretorio):
    """Processa todos os PDFs extraindo quantidades, descrições E valores."""
    contador = defaultdict(lambda: {'quantidade': 0, 'valor_total': 0, 'ocorrencias': []})
    todas_linhas = []
    pdfs_processados = 0
    total_aparelhos = 0
    total_valor = 0
    
    # Lista todos os arquivos PDF únicos
    pdfs_encontrados = set()
    for pattern in ["*.PDF", "*.pdf"]:
        for pdf in Path(diretorio).glob(pattern):
            pdfs_encontrados.add(pdf.resolve())
    
    pdfs = sorted(list(pdfs_encontrados))
    
    print(f"Encontrados {len(pdfs)} arquivos PDF únicos para processar...\n")
    
    for pdf_path in pdfs:
        print(f"Processando: {pdf_path.name}")
        texto = extrair_texto_pdf(pdf_path)
        
        if texto:
            linhas = extrair_linhas_com_valores(texto)
            
            smartphones_neste_pdf = 0
            valor_neste_pdf = 0
            
            for quantidade, descricao, valor_str, valor_num, linha_completa in linhas:
                # Remove apenas R$ e o que vem depois da descrição
                descricao_limpa = re.sub(r'\s*R\$.*$', '', descricao)
                descricao_limpa = re.sub(r'///.*$', '', descricao_limpa).strip()
                
                if descricao_limpa:
                    contador[descricao_limpa]['quantidade'] += quantidade
                    if valor_num:
                        contador[descricao_limpa]['valor_total'] += valor_num
                    
                    contador[descricao_limpa]['ocorrencias'].append({
                        'pdf': pdf_path.name,
                        'quantidade': quantidade,
                        'valor_str': valor_str,
                        'valor_numerico': valor_num
                    })
                    
                    total_aparelhos += quantidade
                    smartphones_neste_pdf += quantidade
                    
                    if valor_num:
                        total_valor += valor_num
                        valor_neste_pdf += valor_num
                    
                    todas_linhas.append({
                        'pdf': pdf_path.name,
                        'quantidade': quantidade,
                        'descricao': descricao_limpa,
                        'valor': valor_str,
                        'valor_numerico': valor_num,
                        'linha_original': linha_completa[:250]
                    })
            
            print(f"  → {smartphones_neste_pdf} aparelhos | R$ {valor_neste_pdf:,.2f}")
            pdfs_processados += 1
    
    print(f"\n{pdfs_processados} PDFs processados com sucesso!")
    print(f"Total de aparelhos: {total_aparelhos:,}")
    print(f"Valor total: R$ {total_valor:,.2f}")
    
    return dict(contador), todas_linhas, total_aparelhos, total_valor

def salvar_json_com_valores(dados, todas_linhas, total_aparelhos, total_valor, arquivo_saida):
    """Salva os dados em formato JSON incluindo valores."""
    
    # Prepara modelos ordenados
    modelos_ordenados = {}
    for desc, info in sorted(dados.items(), key=lambda x: x[1]['quantidade'], reverse=True):
        modelos_ordenados[desc] = {
            'quantidade': info['quantidade'],
            'valor_total': round(info['valor_total'], 2) if info['valor_total'] else None,
            'valor_medio_unitario': round(info['valor_total'] / info['quantidade'], 2) if info['valor_total'] and info['quantidade'] > 0 else None,
            'total_ocorrencias': len(info['ocorrencias'])
        }
    
    resultado = {
        "resumo": {
            "total_modelos": len(dados),
            "total_aparelhos": total_aparelhos,
            "valor_total": round(total_valor, 2),
            "valor_medio_por_aparelho": round(total_valor / total_aparelhos, 2) if total_aparelhos > 0 else None,
            "total_linhas_processadas": len(todas_linhas)
        },
        "modelos_com_valores": modelos_ordenados,
        "primeiras_100_linhas": todas_linhas[:100]
    }
    
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    return resultado

def salvar_csv_com_valores(todas_linhas, arquivo_csv):
    """Salva um CSV com todas as linhas incluindo valores."""
    import csv
    
    with open(arquivo_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['PDF', 'Quantidade', 'Descrição', 'Valor (texto)', 'Valor (numérico)', 'Linha Original'])
        
        for linha in todas_linhas:
            writer.writerow([
                linha['pdf'],
                linha['quantidade'],
                linha['descricao'],
                linha['valor'] if linha['valor'] else 'N/A',
                f"R$ {linha['valor_numerico']:.2f}" if linha['valor_numerico'] else 'N/A',
                linha['linha_original']
            ])
    
    print(f"CSV com valores salvo em: {arquivo_csv}")

if __name__ == "__main__":
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 80)
    print("EXTRAÇÃO COM VALORES - QUANTIDADES, MODELOS E VALORES R$")
    print("=" * 80)
    print()
    
    # Processar PDFs
    aparelhos, todas_linhas, total, total_valor = processar_pdfs_com_valores(diretorio_atual)
    
    # Salvar resultado em JSON
    arquivo_json = os.path.join(diretorio_atual, "celulares_com_valores.json")
    resultado = salvar_json_com_valores(aparelhos, todas_linhas, total, total_valor, arquivo_json)
    
    # Salvar CSV detalhado
    arquivo_csv = os.path.join(diretorio_atual, "celulares_com_valores.csv")
    salvar_csv_com_valores(todas_linhas, arquivo_csv)
    
    print()
    print("=" * 80)
    print("RESULTADO FINAL COM VALORES")
    print("=" * 80)
    print(f"Total de aparelhos.........: {resultado['resumo']['total_aparelhos']:,}")
    print(f"Total de modelos...........: {resultado['resumo']['total_modelos']:,}")
    print(f"Valor total................: R$ {resultado['resumo']['valor_total']:,.2f}")
    print(f"Valor médio por aparelho...: R$ {resultado['resumo']['valor_medio_por_aparelho']:,.2f}")
    print()
    print("Top 10 modelos (por quantidade):")
    print("-" * 80)
    
    for i, (modelo, info) in enumerate(list(resultado['modelos_com_valores'].items())[:10], 1):
        valor_info = f"R$ {info['valor_total']:,.2f}" if info['valor_total'] else "N/A"
        print(f"{i:2d}. {modelo[:55]:55s} {info['quantidade']:5d} un | {valor_info:>15s}")
    
    print()
    print(f"✅ JSON salvo em: {arquivo_json}")
    print(f"✅ CSV salvo em: {arquivo_csv}")
    print()
