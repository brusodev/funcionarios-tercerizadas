import pandas as pd
import PyPDF2
import re
from pathlib import Path

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

def analisar_pdf_0743():
    """Analisa o PDF 0743 e compara com a contagem manual"""
    
    print("="*80)
    print("ANÁLISE DETALHADA - PDF 0743")
    print("="*80)
    
    # 1. Analisa a contagem manual do Excel
    print("\n📊 PARTE 1: CONTAGEM MANUAL (Excel - aba 743)")
    print("-"*80)
    
    df = pd.read_excel('analise_detalhada.xlsx', sheet_name='743')
    
    # Coluna A são as quantidades
    coluna_a = df.iloc[:, 0]
    valores = pd.to_numeric(coluna_a, errors='coerce')
    total_manual = valores.dropna().sum()
    
    print(f"Total de aparelhos (soma coluna A): {int(total_manual)}")
    print(f"Total de linhas com quantidade: {valores.notna().sum()}")
    
    # Analisa a coluna B para valores
    coluna_b = df.iloc[:, 1]
    
    # Procura por valores R$
    padrao_valor = re.compile(r'R\$\s*([\d.,]+)')
    valores_encontrados = []
    
    for idx, texto in coluna_b.items():
        if pd.notna(texto):
            match = padrao_valor.search(str(texto))
            if match:
                valor = normalizar_valor(match.group(1))
                if valor > 0:
                    valores_encontrados.append({
                        'linha': idx + 2,
                        'valor': valor,
                        'texto': str(texto)[:100]
                    })
    
    total_valor_manual = sum([v['valor'] for v in valores_encontrados])
    print(f"Total de valores encontrados: {len(valores_encontrados)}")
    print(f"Soma total dos valores: R$ {total_valor_manual:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    # Mostra exemplos de linhas com quantidade
    print(f"\n📋 Primeiras 20 linhas com quantidade:")
    linhas_com_qtd = df[valores.notna()].head(20)
    for idx, row in linhas_com_qtd.iterrows():
        qtd = row.iloc[0]
        desc = str(row.iloc[1])[:80] if pd.notna(row.iloc[1]) else ""
        print(f"   Linha {idx+2}: Qtd={qtd} | {desc}")
    
    # 2. Analisa o PDF diretamente
    print(f"\n📄 PARTE 2: EXTRAÇÃO DO PDF")
    print("-"*80)
    
    pdf_path = Path('ADM 0800100_0743_2025 de 30_09_2025.PDF')
    
    if not pdf_path.exists():
        print(f"❌ PDF não encontrado: {pdf_path}")
        return
    
    # Extrai texto
    texto = ""
    with open(pdf_path, 'rb') as arquivo:
        leitor = PyPDF2.PdfReader(arquivo)
        for pagina in leitor.pages:
            texto += pagina.extract_text() + "\n"
    
    linhas = texto.split('\n')
    
    # Padrão atual
    padrao_linha = re.compile(
        r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades)\s+((?:SMARTPHONE|TELEFONE\s+CELULAR|(?<!TELEFONE\s)CELULAR|APARELHO\s+CELULAR|IPHONE).*)', 
        re.IGNORECASE
    )
    
    padrao_codigo = re.compile(r'^\d+\s*-\s*\d+')
    padrao_valor_pdf = re.compile(r'R\$\s*([\d.,]+)')
    
    linhas_encontradas = []
    i = 0
    while i < len(linhas):
        linha_atual = linhas[i].strip()
        
        if padrao_codigo.match(linha_atual):
            i += 1
            continue
        
        match = padrao_linha.match(linha_atual)
        
        if match:
            quantidade_str = match.group(1)
            descricao = match.group(2).strip()
            quantidade = float(quantidade_str.replace(',', '.'))
            
            # Procura valor
            valor_encontrado = None
            valor_numerico = 0.0
            
            for offset in range(10):
                if i + offset < len(linhas):
                    linha_busca = linhas[i + offset]
                    match_valor = padrao_valor_pdf.search(linha_busca)
                    
                    if match_valor:
                        valor_encontrado = match_valor.group(1)
                        valor_numerico = normalizar_valor(valor_encontrado)
                        break
                    
                    if offset > 0 and padrao_linha.match(linhas[i + offset].strip()) and not padrao_codigo.match(linhas[i + offset].strip()):
                        break
            
            linhas_encontradas.append({
                'linha_num': i + 1,
                'quantidade': quantidade,
                'descricao': descricao[:80],
                'valor': valor_numerico,
                'linha_original': linha_atual[:120]
            })
        
        i += 1
    
    total_pdf = sum([l['quantidade'] for l in linhas_encontradas])
    total_valor_pdf = sum([l['valor'] for l in linhas_encontradas])
    
    print(f"Total de linhas encontradas: {len(linhas_encontradas)}")
    print(f"Total de aparelhos: {int(total_pdf)}")
    print(f"Total valor: R$ {total_valor_pdf:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    # 3. Comparação
    print(f"\n🔍 PARTE 3: COMPARAÇÃO")
    print("-"*80)
    print(f"Manual (Excel):     {int(total_manual)} aparelhos | R$ {total_valor_manual:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print(f"Extração (Script):  {int(total_pdf)} aparelhos | R$ {total_valor_pdf:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print(f"JSON atual:         612 aparelhos | R$ 974.075,37")
    print()
    print(f"Diferença Manual vs Script: {int(total_manual - total_pdf)} aparelhos | R$ {(total_valor_manual - total_valor_pdf):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    # 4. Procura por padrões que podem estar sendo perdidos
    print(f"\n🔎 PARTE 4: PROCURANDO PADRÕES PERDIDOS")
    print("-"*80)
    
    # Verifica se há linhas que começam com número mas não são capturadas
    padrao_numero = re.compile(r'^(\d+(?:,\d+)?)\s+(.+)', re.IGNORECASE)
    
    linhas_com_numero = []
    for i, linha in enumerate(linhas):
        linha_strip = linha.strip()
        if padrao_codigo.match(linha_strip):
            continue
        
        match = padrao_numero.match(linha_strip)
        if match and not padrao_linha.match(linha_strip):
            # Linha com número que NÃO foi capturada
            quantidade_str = match.group(1)
            resto = match.group(2)
            
            # Verifica se tem palavras-chave relacionadas a celular
            palavras_celular = ['celular', 'smartphone', 'iphone', 'telefone', 'aparelho']
            if any(palavra in resto.lower() for palavra in palavras_celular):
                linhas_com_numero.append({
                    'linha': i + 1,
                    'quantidade': float(quantidade_str.replace(',', '.')),
                    'texto': linha_strip[:150]
                })
    
    if linhas_com_numero:
        print(f"❗ Encontradas {len(linhas_com_numero)} linhas com número e palavras-chave que NÃO foram capturadas:")
        total_perdido = sum([l['quantidade'] for l in linhas_com_numero])
        print(f"Total de aparelhos perdidos: {int(total_perdido)}")
        print()
        
        for linha in linhas_com_numero[:30]:
            print(f"   Linha {linha['linha']}: Qtd={linha['quantidade']}")
            print(f"      {linha['texto']}")
            print()
    else:
        print("✓ Nenhuma linha com padrão diferente encontrada")
    
    # Salva relatório detalhado
    with open('analise_0743_detalhada.txt', 'w', encoding='utf-8') as f:
        f.write("ANÁLISE DETALHADA - PDF 0743\n")
        f.write("="*80 + "\n\n")
        
        f.write("CONTAGEM MANUAL (Excel):\n")
        f.write(f"Total aparelhos: {int(total_manual)}\n")
        f.write(f"Total valor: R$ {total_valor_manual:,.2f}\n\n")
        
        f.write("EXTRAÇÃO DO PDF:\n")
        f.write(f"Total aparelhos: {int(total_pdf)}\n")
        f.write(f"Total valor: R$ {total_valor_pdf:,.2f}\n\n")
        
        f.write("LINHAS EXTRAÍDAS:\n")
        f.write("-"*80 + "\n")
        for linha in linhas_encontradas:
            f.write(f"Linha {linha['linha_num']}: Qtd={linha['quantidade']}, Valor=R$ {linha['valor']:,.2f}\n")
            f.write(f"   {linha['linha_original']}\n\n")
        
        if linhas_com_numero:
            f.write("\nLINHAS PERDIDAS (não capturadas):\n")
            f.write("-"*80 + "\n")
            for linha in linhas_com_numero:
                f.write(f"Linha {linha['linha']}: Qtd={linha['quantidade']}\n")
                f.write(f"   {linha['texto']}\n\n")
    
    print(f"\n📄 Relatório completo salvo em: analise_0743_detalhada.txt")

if __name__ == "__main__":
    analisar_pdf_0743()
