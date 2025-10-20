import PyPDF2
import re
from pathlib import Path

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

def diagnosticar_pdf():
    """Diagnostica problemas na extração do PDF 0746"""
    
    pdf_path = Path('ADM 0800100_0746_2025 de 30_09_2025.PDF')
    
    if not pdf_path.exists():
        print(f"❌ Arquivo não encontrado: {pdf_path}")
        return
    
    print("="*80)
    print(f"DIAGNÓSTICO: {pdf_path.name}")
    print("="*80)
    
    texto = extrair_texto_pdf(pdf_path)
    linhas = texto.split('\n')
    
    # Padrão atual (mais restrito)
    padrao_atual = re.compile(r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades)\s+((?:SMARTPHONE|TELEFONE\s+CELULAR)\s+.+)', re.IGNORECASE)
    
    # Padrões alternativos para testar
    # Aceita linhas que começam com quantidade mesmo sem "un"
    padrao_alternativo1 = re.compile(r'^(\d+(?:,\d+)?)\s+((?:SMARTPHONE|TELEFONE\s+CELULAR)\s+.+)', re.IGNORECASE)
    
    # Padrão para valores
    padrao_valor = re.compile(r'R\$\s*([\d.,]+)')
    
    print("\n🔍 ANÁLISE COM PADRÃO ATUAL (requer 'un'):")
    linhas_encontradas_atual = []
    total_qtd_atual = 0
    total_valor_atual = 0.0
    
    i = 0
    while i < len(linhas):
        linha_atual = linhas[i].strip()
        match = padrao_atual.match(linha_atual)
        
        if match:
            quantidade_str = match.group(1)
            descricao = match.group(2).strip()
            quantidade = float(quantidade_str.replace(',', '.'))
            
            # Procura valor
            valor_encontrado = None
            valor_numerico = 0.0
            
            for offset in range(6):
                if i + offset < len(linhas):
                    linha_busca = linhas[i + offset]
                    match_valor = padrao_valor.search(linha_busca)
                    
                    if match_valor:
                        valor_encontrado = match_valor.group(1)
                        valor_numerico = normalizar_valor(valor_encontrado)
                        break
                    
                    if offset > 0 and padrao_atual.match(linhas[i + offset].strip()):
                        break
            
            linhas_encontradas_atual.append({
                'linha_num': i + 1,
                'quantidade': quantidade,
                'descricao': descricao,
                'valor': valor_numerico,
                'linha': linha_atual
            })
            
            total_qtd_atual += quantidade
            total_valor_atual += valor_numerico
        
        i += 1
    
    print(f"   Linhas encontradas: {len(linhas_encontradas_atual)}")
    print(f"   Total de aparelhos: {int(total_qtd_atual)}")
    print(f"   Total valor: R$ {total_valor_atual:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    print("\n🔍 ANÁLISE COM PADRÃO ALTERNATIVO (sem exigir 'un'):")
    linhas_encontradas_alt1 = []
    total_qtd_alt1 = 0
    total_valor_alt1 = 0.0
    
    i = 0
    while i < len(linhas):
        linha_atual = linhas[i].strip()
        match = padrao_alternativo1.match(linha_atual)
        
        if match:
            quantidade_str = match.group(1)
            descricao = match.group(2).strip()
            quantidade = float(quantidade_str.replace(',', '.'))
            
            # Procura valor
            valor_encontrado = None
            valor_numerico = 0.0
            
            for offset in range(6):
                if i + offset < len(linhas):
                    linha_busca = linhas[i + offset]
                    match_valor = padrao_valor.search(linha_busca)
                    
                    if match_valor:
                        valor_encontrado = match_valor.group(1)
                        valor_numerico = normalizar_valor(valor_encontrado)
                        break
                    
                    if offset > 0 and padrao_alternativo1.match(linhas[i + offset].strip()):
                        break
            
            linhas_encontradas_alt1.append({
                'linha_num': i + 1,
                'quantidade': quantidade,
                'descricao': descricao,
                'valor': valor_numerico,
                'linha': linha_atual
            })
            
            total_qtd_alt1 += quantidade
            total_valor_alt1 += valor_numerico
        
        i += 1
    
    print(f"   Linhas encontradas: {len(linhas_encontradas_alt1)}")
    print(f"   Total de aparelhos: {int(total_qtd_alt1)}")
    print(f"   Total valor: R$ {total_valor_alt1:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    # Mostra diferenças
    print("\n📊 DIFERENÇAS ENCONTRADAS:")
    print(f"   Diferença em linhas: {len(linhas_encontradas_alt1) - len(linhas_encontradas_atual)}")
    print(f"   Diferença em aparelhos: {int(total_qtd_alt1 - total_qtd_atual)}")
    print(f"   Diferença em valor: R$ {(total_valor_alt1 - total_valor_atual):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    # Mostra linhas que foram perdidas no padrão atual
    if len(linhas_encontradas_alt1) > len(linhas_encontradas_atual):
        print("\n⚠️ LINHAS PERDIDAS COM PADRÃO ATUAL (primeiras 20):")
        linhas_atuais_set = set([l['linha'] for l in linhas_encontradas_atual])
        linhas_perdidas = [l for l in linhas_encontradas_alt1 if l['linha'] not in linhas_atuais_set]
        
        for i, linha in enumerate(linhas_perdidas[:20], 1):
            print(f"\n   {i}. Linha {linha['linha_num']}: Qtd={linha['quantidade']}, Valor=R$ {linha['valor']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            print(f"      {linha['linha'][:100]}...")
    
    # Comparação com valores informados pelo usuário
    print("\n" + "="*80)
    print("COMPARAÇÃO COM VALORES DO USUÁRIO:")
    print("="*80)
    print(f"Usuário informou:")
    print(f"   Total de aparelhos: 2544")
    print(f"   Total valor: R$ 3.050.180,53")
    print()
    print(f"Padrão ATUAL encontrou:")
    print(f"   Total de aparelhos: {int(total_qtd_atual)} (diferença: {int(total_qtd_atual - 2544)})")
    print(f"   Total valor: R$ {total_valor_atual:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') + f" (diferença: R$ {(total_valor_atual - 3050180.53):,.2f})".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print()
    print(f"Padrão ALTERNATIVO encontrou:")
    print(f"   Total de aparelhos: {int(total_qtd_alt1)} (diferença: {int(total_qtd_alt1 - 2544)})")
    print(f"   Total valor: R$ {total_valor_alt1:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.') + f" (diferença: R$ {(total_valor_alt1 - 3050180.53):,.2f})".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    print("\n" + "="*80)
    
    # Salva relatório detalhado
    with open('diagnostico_pdf_0746.txt', 'w', encoding='utf-8') as f:
        f.write("DIAGNÓSTICO DETALHADO - PDF 0746\n")
        f.write("="*80 + "\n\n")
        f.write(f"Total linhas encontradas (padrão atual): {len(linhas_encontradas_atual)}\n")
        f.write(f"Total linhas encontradas (padrão alternativo): {len(linhas_encontradas_alt1)}\n\n")
        
        f.write("TODAS AS LINHAS (padrão alternativo):\n")
        f.write("-"*80 + "\n")
        for linha in linhas_encontradas_alt1:
            f.write(f"Linha {linha['linha_num']}: Qtd={linha['quantidade']}, Valor=R$ {linha['valor']:,.2f}\n")
            f.write(f"   {linha['linha']}\n\n")
    
    print("📄 Relatório detalhado salvo em: diagnostico_pdf_0746.txt")

if __name__ == "__main__":
    diagnosticar_pdf()
