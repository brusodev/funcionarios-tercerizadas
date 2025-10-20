import PyPDF2
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

def analisar_todas_linhas_com_numero():
    """Analisa todas as linhas que começam com número no PDF"""
    
    pdf_path = Path('ADM 0800100_0746_2025 de 30_09_2025.PDF')
    
    print("="*80)
    print("ANÁLISE COMPLETA - Todas as linhas que começam com número")
    print("="*80)
    
    texto = extrair_texto_pdf(pdf_path)
    linhas = texto.split('\n')
    
    # Padrão para qualquer linha que começa com número
    padrao_numero = re.compile(r'^(\d+(?:,\d+)?)\s+(.+)', re.IGNORECASE)
    padrao_valor = re.compile(r'R\$\s*([\d.,]+)')
    
    linhas_com_numero = []
    categorias = defaultdict(int)
    
    i = 0
    while i < len(linhas):
        linha_atual = linhas[i].strip()
        match = padrao_numero.match(linha_atual)
        
        if match:
            quantidade_str = match.group(1)
            resto = match.group(2).strip()
            quantidade = float(quantidade_str.replace(',', '.'))
            
            # Classifica a linha
            categoria = "OUTRO"
            tem_smartphone = bool(re.search(r'SMARTPHONE', resto, re.IGNORECASE))
            tem_telefone = bool(re.search(r'TELEFONE\s+CELULAR', resto, re.IGNORECASE))
            tem_un = bool(re.search(r'^(?:un|unidade|unidades)\s+', resto, re.IGNORECASE))
            
            if tem_smartphone and tem_un:
                categoria = "SMARTPHONE com 'un'"
            elif tem_telefone and tem_un:
                categoria = "TELEFONE CELULAR com 'un'"
            elif tem_smartphone and not tem_un:
                categoria = "SMARTPHONE sem 'un'"
            elif tem_telefone and not tem_un:
                categoria = "TELEFONE CELULAR sem 'un'"
            elif tem_un:
                categoria = "Outros com 'un'"
            
            categorias[categoria] += 1
            
            # Procura valor
            valor_numerico = 0.0
            for offset in range(6):
                if i + offset < len(linhas):
                    linha_busca = linhas[i + offset]
                    match_valor = padrao_valor.search(linha_busca)
                    if match_valor:
                        valor_numerico = normalizar_valor(match_valor.group(1))
                        break
                    if offset > 0 and padrao_numero.match(linhas[i + offset].strip()):
                        break
            
            linhas_com_numero.append({
                'linha_num': i + 1,
                'quantidade': quantidade,
                'categoria': categoria,
                'valor': valor_numerico,
                'linha': linha_atual[:150]
            })
        
        i += 1
    
    # Estatísticas por categoria
    print("\n📊 ESTATÍSTICAS POR CATEGORIA:")
    print("-"*80)
    
    for categoria, count in sorted(categorias.items(), key=lambda x: x[1], reverse=True):
        linhas_cat = [l for l in linhas_com_numero if l['categoria'] == categoria]
        total_qtd = sum([l['quantidade'] for l in linhas_cat])
        total_valor = sum([l['valor'] for l in linhas_cat])
        print(f"\n{categoria}:")
        print(f"   Linhas: {count}")
        print(f"   Total aparelhos: {int(total_qtd)}")
        print(f"   Total valor: R$ {total_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    # Total geral
    print("\n" + "="*80)
    print("TOTAL GERAL (todas as linhas com número):")
    total_linhas = len(linhas_com_numero)
    total_qtd_geral = sum([l['quantidade'] for l in linhas_com_numero])
    total_valor_geral = sum([l['valor'] for l in linhas_com_numero])
    
    print(f"   Total de linhas: {total_linhas}")
    print(f"   Total de aparelhos: {int(total_qtd_geral)}")
    print(f"   Total valor: R$ {total_valor_geral:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    # Mostra exemplos de cada categoria
    print("\n" + "="*80)
    print("EXEMPLOS DE CADA CATEGORIA:")
    print("="*80)
    
    for categoria in sorted(categorias.keys()):
        exemplos = [l for l in linhas_com_numero if l['categoria'] == categoria][:5]
        if exemplos:
            print(f"\n{categoria} (mostrando {len(exemplos)} de {categorias[categoria]}):")
            for ex in exemplos:
                print(f"   Linha {ex['linha_num']}: Qtd={ex['quantidade']}, Valor=R$ {ex['valor']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
                print(f"      {ex['linha']}")
    
    # Salva análise completa
    with open('analise_completa_0746.txt', 'w', encoding='utf-8') as f:
        f.write("ANÁLISE COMPLETA - PDF 0746\n")
        f.write("="*80 + "\n\n")
        
        for categoria in sorted(categorias.keys()):
            f.write(f"\n{'='*80}\n")
            f.write(f"CATEGORIA: {categoria}\n")
            f.write(f"{'='*80}\n\n")
            
            linhas_cat = [l for l in linhas_com_numero if l['categoria'] == categoria]
            for linha in linhas_cat:
                f.write(f"Linha {linha['linha_num']}: Qtd={linha['quantidade']}, Valor=R$ {linha['valor']:,.2f}\n")
                f.write(f"   {linha['linha']}\n\n")
    
    print("\n📄 Análise completa salva em: analise_completa_0746.txt")
    
    # Comparação final
    print("\n" + "="*80)
    print("COMPARAÇÃO COM VALORES ESPERADOS:")
    print("="*80)
    print(f"Usuário esperava: 2544 aparelhos | R$ 3.050.180,53")
    print(f"Script atual encontrou: 2536 aparelhos | R$ 3.040.062,23")
    print(f"Todas as linhas com número: {int(total_qtd_geral)} aparelhos | R$ {total_valor_geral:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print()
    print(f"Diferença (esperado vs atual): {2544 - 2536} aparelhos | R$ {3050180.53 - 3040062.23:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

if __name__ == "__main__":
    analisar_todas_linhas_com_numero()
