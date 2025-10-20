import pandas as pd
import PyPDF2
import re
from pathlib import Path

def normalizar_quantidade(qtd_str):
    """Converte quantidade com vírgula para inteiro"""
    try:
        return int(float(str(qtd_str).replace(',', '.')))
    except:
        return 0

def extrair_texto_pdf(caminho_pdf):
    """Extrai todo o texto de um arquivo PDF"""
    with open(caminho_pdf, 'rb') as arquivo:
        leitor_pdf = PyPDF2.PdfReader(arquivo)
        texto_completo = []
        for pagina in leitor_pdf.pages:
            texto_completo.append(pagina.extract_text())
        return '\n'.join(texto_completo)

def extrair_linhas_v5(texto_pdf):
    """Versão 5 - FINAL com todos os padrões"""
    linhas = texto_pdf.split('\n')
    itens_encontrados = []
    
    # Padrão V5 completo
    padrao_item = r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades|kg)\s+((?:SMARTPHONE|TELEFONE\s+CELULAR|APARELHO\s+CELULAR|IPHONE|(?<!TELEFONE\s)(?<!APARELHO\s)CELULAR|(?:REDMI|NOTE|POCO|POCOPHONE|MI)\s+\d+).*)'
    padrao_codigo = r'^\d+\s*-\s*\d+'
    
    for i, linha in enumerate(linhas):
        linha = linha.strip()
        
        if not linha or re.match(padrao_codigo, linha):
            continue
        
        match = re.match(padrao_item, linha, re.IGNORECASE)
        if match:
            qtd_str = match.group(1)
            descricao = match.group(2)
            quantidade = normalizar_quantidade(qtd_str)
            
            itens_encontrados.append({
                'quantidade': quantidade,
                'descricao': descricao
            })
    
    return itens_encontrados

print("="*80)
print("VALIDAÇÃO DOS 4 PDFs COM EXCEL")
print("="*80)

# Abas disponíveis no Excel
abas_excel = ['743', '737', '747', '746']

resultados = []

for aba in abas_excel:
    print(f"\n{'='*80}")
    print(f"📊 VALIDANDO PDF {aba}")
    print(f"{'='*80}")
    
    # Encontra o PDF correspondente (padrão: ADM 0800100_0743_2025...)
    pdf_pattern = f"ADM*0{aba}*.PDF"
    pdf_files = list(Path('.').glob(pdf_pattern))
    
    if not pdf_files:
        print(f"⚠️ PDF não encontrado para aba {aba} (padrão: {pdf_pattern})")
        # Lista PDFs disponíveis para debug
        all_pdfs = list(Path('.').glob("ADM*.PDF"))
        print(f"   PDFs disponíveis: {[p.name for p in all_pdfs[:3]]}...")
        continue
    
    pdf_file = pdf_files[0]
    nome_pdf = pdf_file.name
    print(f"📄 PDF: {nome_pdf}")
    
    # 1. LÊ O EXCEL
    try:
        df = pd.read_excel('analise_detalhada.xlsx', sheet_name=aba)
        coluna_a = df.iloc[:, 0]
        coluna_b = df.iloc[:, 1]
        
        # Total de linhas com quantidade
        valores_a = pd.to_numeric(coluna_a, errors='coerce')
        excel_todas_linhas = valores_a.notna().sum()
        excel_todas_qtd = valores_a.sum()
        
        print(f"\n📊 EXCEL (aba '{aba}'):")
        print(f"   Total de linhas com quantidade: {int(excel_todas_linhas)}")
        print(f"   Soma de TODAS as quantidades: {int(excel_todas_qtd)}")
        
        # Identifica quantas têm valor R$ na descrição
        linhas_com_valor = coluna_b.astype(str).str.contains(r'R\$', na=False, regex=True)
        df_com_valor = df[valores_a.notna() & linhas_com_valor].copy()
        df_com_valor['qtd'] = pd.to_numeric(df_com_valor.iloc[:, 0], errors='coerce')
        
        excel_com_valor_linhas = len(df_com_valor)
        excel_com_valor_qtd = df_com_valor['qtd'].sum()
        
        print(f"\n   Linhas COM valor R$ na descrição: {excel_com_valor_linhas}")
        print(f"   Soma das quantidades COM valor: {int(excel_com_valor_qtd)}")
        
    except Exception as e:
        print(f"   ✗ Erro ao ler Excel: {e}")
        continue
    
    # 2. PROCESSA O PDF
    try:
        texto = extrair_texto_pdf(str(pdf_file))
        itens_pdf = extrair_linhas_v5(texto)
        script_linhas = len(itens_pdf)
        script_qtd = sum(item['quantidade'] for item in itens_pdf)
        
        print(f"\n🔍 SCRIPT V5:")
        print(f"   Linhas encontradas: {script_linhas}")
        print(f"   Total de aparelhos: {script_qtd}")
        
    except Exception as e:
        print(f"   ✗ Erro ao processar PDF: {e}")
        continue
    
    # 3. COMPARA
    print(f"\n{'='*80}")
    print(f"COMPARAÇÃO:")
    print(f"{'='*80}")
    
    # Compara com TODAS as linhas do Excel
    dif_todas = script_qtd - excel_todas_qtd
    print(f"\nScript vs Excel TOTAL:")
    print(f"   Script:  {script_qtd} aparelhos ({script_linhas} linhas)")
    print(f"   Excel:   {int(excel_todas_qtd)} aparelhos ({int(excel_todas_linhas)} linhas)")
    print(f"   Diferença: {dif_todas:+} aparelhos")
    
    # Compara com linhas COM valor R$
    dif_com_valor = script_qtd - excel_com_valor_qtd
    print(f"\nScript vs Excel COM VALOR R$:")
    print(f"   Script:  {script_qtd} aparelhos ({script_linhas} linhas)")
    print(f"   Excel:   {int(excel_com_valor_qtd)} aparelhos ({excel_com_valor_linhas} linhas)")
    print(f"   Diferença: {dif_com_valor:+} aparelhos")
    
    # Determina status
    if abs(dif_todas) == 0:
        status = "✅ EXATO (total)"
    elif abs(dif_com_valor) <= 5:
        status = f"⚠️ Pequena diferença: {dif_com_valor:+} (vs com valor R$)"
    elif abs(dif_todas) <= 5:
        status = f"⚠️ Pequena diferença: {dif_todas:+} (vs total)"
    else:
        status = f"❌ Grande diferença"
    
    print(f"\nStatus: {status}")
    
    resultados.append({
        'pdf': aba,
        'excel_total': int(excel_todas_qtd),
        'excel_com_valor': int(excel_com_valor_qtd),
        'script': script_qtd,
        'dif_total': dif_todas,
        'dif_com_valor': dif_com_valor,
        'status': status
    })

# Relatório final
print(f"\n{'='*80}")
print("RELATÓRIO RESUMIDO")
print(f"{'='*80}")

print(f"\n{'PDF':<6} {'Excel Total':<13} {'Excel c/Valor':<15} {'Script V5':<12} {'Status':<30}")
print("-" * 90)

for r in resultados:
    print(f"{r['pdf']:<6} {r['excel_total']:<13} {r['excel_com_valor']:<15} {r['script']:<12} {r['status']:<30}")

print(f"\n{'='*80}")
print("OBSERVAÇÕES:")
print(f"{'='*80}")
print("""
1. 'Excel Total' = Soma de TODAS as linhas com quantidade no Excel
2. 'Excel c/Valor' = Soma apenas das linhas que têm 'R$' na descrição
3. 'Script V5' = O que o script automatizado encontra no PDF

Se você está fazendo validação manual e encontrando valores diferentes,
isso pode indicar que:
- Você está aplicando algum filtro ou critério específico
- Há linhas duplicadas ou subtotais no Excel
- Há itens que não são celulares mas têm quantidade

Sugiro que você me informe para CADA PDF (743, 737, 747, 746):
- Qual o número CORRETO de aparelhos que você validou manualmente
- Se possível, compartilhe o critério que você usou para validação
""")
