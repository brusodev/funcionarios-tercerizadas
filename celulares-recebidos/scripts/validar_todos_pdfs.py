import pandas as pd
import PyPDF2
import re
import json
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
print("VALIDAÇÃO COMPLETA: EXCEL vs SCRIPT V5")
print("="*80)

# Verifica quais abas existem no Excel
try:
    excel_file = pd.ExcelFile('analise_detalhada.xlsx')
    abas_disponiveis = excel_file.sheet_names
    print(f"\n📊 Abas encontradas no Excel: {abas_disponiveis}")
except Exception as e:
    print(f"⚠️ Erro ao abrir Excel: {e}")
    abas_disponiveis = []

# Mapeia número do PDF para aba do Excel
# Exemplo: PDF 0743 -> aba '743'
mapeamento_abas = {}
for aba in abas_disponiveis:
    # Tenta extrair número da aba (743, 746, etc)
    match = re.search(r'\d+', aba)
    if match:
        numero = match.group()
        mapeamento_abas[numero] = aba

print(f"Mapeamento encontrado: {mapeamento_abas}")

# Processa todos os PDFs
pdf_files = sorted(Path('.').glob('ADM *.PDF'))
print(f"\n📄 {len(pdf_files)} PDFs encontrados\n")

resultados_validacao = []

for pdf_file in pdf_files:
    nome_pdf = pdf_file.name
    
    # Extrai o número do PDF (ex: "0743" de "ADM 0800100_0743_2025...")
    match_numero = re.search(r'_(\d{4})_', nome_pdf)
    if not match_numero:
        print(f"⚠️ Não consegui extrair número de: {nome_pdf}")
        continue
    
    numero_pdf = match_numero.group(1)
    
    print(f"\n{'='*80}")
    print(f"📄 PDF {numero_pdf}: {nome_pdf}")
    print(f"{'='*80}")
    
    # Processa o PDF com V5
    try:
        texto = extrair_texto_pdf(str(pdf_file))
        itens_pdf = extrair_linhas_v5(texto)
        total_script = sum(item['quantidade'] for item in itens_pdf)
        linhas_script = len(itens_pdf)
        
        print(f"SCRIPT V5:")
        print(f"   Linhas: {linhas_script}")
        print(f"   Aparelhos: {total_script}")
        
    except Exception as e:
        print(f"   ✗ Erro ao processar PDF: {e}")
        total_script = 0
        linhas_script = 0
    
    # Verifica se existe aba correspondente no Excel
    aba_excel = mapeamento_abas.get(numero_pdf)
    
    if aba_excel:
        try:
            df = pd.read_excel('analise_detalhada.xlsx', sheet_name=aba_excel)
            coluna_a = df.iloc[:, 0]
            
            # Conta linhas com quantidade
            valores_a = pd.to_numeric(coluna_a, errors='coerce')
            linhas_excel = valores_a.notna().sum()
            total_excel = valores_a.sum()
            
            print(f"\nEXCEL (aba '{aba_excel}'):")
            print(f"   Linhas: {int(linhas_excel)}")
            print(f"   Aparelhos: {int(total_excel)}")
            
            # Calcula diferenças
            dif_aparelhos = total_script - total_excel
            dif_linhas = linhas_script - linhas_excel
            
            print(f"\nDIFERENÇA:")
            
            if dif_aparelhos == 0:
                print(f"   Aparelhos: ✅ EXATO (0)")
                status = "✅ EXATO"
            elif abs(dif_aparelhos) <= 5:
                print(f"   Aparelhos: ⚠️ {dif_aparelhos:+} (pequena diferença)")
                status = f"⚠️ {dif_aparelhos:+}"
            else:
                print(f"   Aparelhos: ❌ {dif_aparelhos:+} (ATENÇÃO!)")
                status = f"❌ {dif_aparelhos:+}"
            
            print(f"   Linhas: {dif_linhas:+}")
            
            resultados_validacao.append({
                'numero_pdf': numero_pdf,
                'nome_pdf': nome_pdf,
                'excel_aparelhos': int(total_excel),
                'excel_linhas': int(linhas_excel),
                'script_aparelhos': total_script,
                'script_linhas': linhas_script,
                'dif_aparelhos': dif_aparelhos,
                'dif_linhas': dif_linhas,
                'status': status,
                'tem_excel': True
            })
            
        except Exception as e:
            print(f"\n⚠️ Erro ao ler aba '{aba_excel}': {e}")
            resultados_validacao.append({
                'numero_pdf': numero_pdf,
                'nome_pdf': nome_pdf,
                'script_aparelhos': total_script,
                'script_linhas': linhas_script,
                'status': "📋 Sem Excel",
                'tem_excel': False
            })
    else:
        print(f"\n📋 Sem aba correspondente no Excel")
        resultados_validacao.append({
            'numero_pdf': numero_pdf,
            'nome_pdf': nome_pdf,
            'script_aparelhos': total_script,
            'script_linhas': linhas_script,
            'status': "📋 Sem Excel",
            'tem_excel': False
        })

# Relatório final
print(f"\n{'='*80}")
print("RELATÓRIO FINAL DE VALIDAÇÃO")
print(f"{'='*80}")

print(f"\n{'Nº PDF':<8} {'Excel':<10} {'Script':<10} {'Diferença':<12} {'Status':<15}")
print("-" * 80)

for r in resultados_validacao:
    if r['tem_excel']:
        print(f"{r['numero_pdf']:<8} {r['excel_aparelhos']:<10} {r['script_aparelhos']:<10} {r['dif_aparelhos']:+11}  {r['status']:<15}")
    else:
        print(f"{r['numero_pdf']:<8} {'N/A':<10} {r['script_aparelhos']:<10} {'N/A':<12} {r['status']:<15}")

# Estatísticas
print(f"\n{'='*80}")
print("ESTATÍSTICAS:")
print(f"{'='*80}")

com_excel = [r for r in resultados_validacao if r['tem_excel']]
exatos = [r for r in com_excel if r['dif_aparelhos'] == 0]
pequenas_dif = [r for r in com_excel if 0 < abs(r['dif_aparelhos']) <= 5]
grandes_dif = [r for r in com_excel if abs(r['dif_aparelhos']) > 5]
sem_excel = [r for r in resultados_validacao if not r['tem_excel']]

print(f"PDFs com Excel de validação: {len(com_excel)}")
print(f"   ✅ Exatos (diferença = 0): {len(exatos)}")
print(f"   ⚠️ Pequenas diferenças (1-5): {len(pequenas_dif)}")
print(f"   ❌ Grandes diferenças (>5): {len(grandes_dif)}")
print(f"📋 PDFs sem Excel: {len(sem_excel)}")

if grandes_dif:
    print(f"\n{'='*80}")
    print("⚠️ PDFs COM GRANDES DIFERENÇAS (necessitam investigação):")
    print(f"{'='*80}")
    for r in grandes_dif:
        print(f"\n📄 PDF {r['numero_pdf']}:")
        print(f"   Excel: {r['excel_aparelhos']} aparelhos")
        print(f"   Script: {r['script_aparelhos']} aparelhos")
        print(f"   Diferença: {r['dif_aparelhos']:+} aparelhos")

if pequenas_dif:
    print(f"\n{'='*80}")
    print("ℹ️ PDFs COM PEQUENAS DIFERENÇAS:")
    print(f"{'='*80}")
    for r in pequenas_dif:
        print(f"   PDF {r['numero_pdf']}: {r['dif_aparelhos']:+} aparelhos")

# Salva relatório em JSON
with open('validacao_completa.json', 'w', encoding='utf-8') as f:
    json.dump(resultados_validacao, f, ensure_ascii=False, indent=2)

print(f"\n{'='*80}")
print("✅ Relatório salvo em: validacao_completa.json")
print(f"{'='*80}")
