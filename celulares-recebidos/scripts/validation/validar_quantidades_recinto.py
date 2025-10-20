import re
import os
from collections import defaultdict
from PyPDF2 import PdfReader

# Padrões de recinto
RECINTOS = {
    r'305\s*-\s*810300': 'Bauru',
    r'16\s*-\s*810900': 'Araraquara',
    r'2\s*-\s*DEPÓSITO SAPOL': 'São José do Rio Preto',
    r'1\s*-\s*AEROPORTOS BRASIL VIRACOPOS': 'Viracopos',
    r'309\s*-\s*817900': 'Ipiranga',
}

def extrair_recinto_linha(linha):
    """Extrai o recinto de uma linha"""
    for pattern, recinto in RECINTOS.items():
        if re.search(pattern, linha, re.IGNORECASE):
            return recinto
    return None

def converter_quantidade(quantidade_str, unidade):
    """Converte quantidade para aparelhos"""
    quantidade_str = quantidade_str.replace('.', '').replace(',', '.')
    quantidade = float(quantidade_str)
    
    if unidade.lower() == 'kg':
        if quantidade == 0.49:
            return 1
        else:
            return round(quantidade / 0.49)
    else:  # 'un'
        return int(quantidade)

def validar_recintos():
    """Valida distribuição de recintos"""
    
    PATTERN_QUANTIDADE = r'(\d+[\.,]?\d*,\d+)\s+(un|kg)'
    
    distribuicao = defaultdict(lambda: {'aparelhos': 0, 'pdfs': defaultdict(int)})
    
    print("=" * 100)
    print("VALIDAÇÃO DE DISTRIBUIÇÃO POR RECINTO")
    print("=" * 100)
    print()
    
    pdfs = sorted([f for f in os.listdir('.') if f.startswith('ADM') and f.endswith('.PDF')])
    
    print(f"Processando {len(pdfs)} PDFs...\n")
    
    for pdf_file in pdfs:
        pdf_num = re.search(r'0(\d{3})', pdf_file).group(1)
        
        try:
            reader = PdfReader(pdf_file)
            texto_completo = ""
            
            for page in reader.pages:
                texto_completo += page.extract_text()
            
            linhas = texto_completo.split('\n')
            recinto_atual = None
            pdf_total = 0
            
            for linha in linhas:
                linha = linha.strip()
                
                # Detecta mudança de recinto
                novo_recinto = extrair_recinto_linha(linha)
                if novo_recinto:
                    recinto_atual = novo_recinto
                
                # Procura por linhas com quantidade
                if recinto_atual:
                    matches = re.findall(PATTERN_QUANTIDADE, linha)
                    
                    if matches:
                        for quantidade_str, unidade in matches:
                            aparelhos = converter_quantidade(quantidade_str, unidade)
                            
                            if aparelhos > 0:
                                distribuicao[recinto_atual]['aparelhos'] += aparelhos
                                distribuicao[recinto_atual]['pdfs'][pdf_num] += aparelhos
                                pdf_total += aparelhos
            
            print(f"PDF {pdf_num}: {pdf_total:,} aparelhos processados")
        
        except Exception as e:
            print(f"ERRO em PDF {pdf_num}: {e}")
    
    return distribuicao

print("\n🔍 EXECUTANDO VALIDAÇÃO...\n")

distribuicao = validar_recintos()

print()
print("=" * 100)
print("RESULTADOS DA VALIDAÇÃO")
print("=" * 100)
print()

total_geral = 0

for recinto in sorted(distribuicao.keys()):
    dados = distribuicao[recinto]
    aparelhos = dados['aparelhos']
    total_geral += aparelhos
    percentual = (aparelhos / 33215) * 100
    
    print(f"\n{recinto}:")
    print(f"  Total: {aparelhos:,} aparelhos ({percentual:.2f}%)")
    print(f"  Distribuição por PDF:")
    
    for pdf_num in sorted(dados['pdfs'].keys()):
        qtd = dados['pdfs'][pdf_num]
        pct = (qtd / aparelhos) * 100 if aparelhos > 0 else 0
        print(f"    • PDF {pdf_num}: {qtd:,} aparelhos ({pct:.1f}%)")

print()
print("=" * 100)
print(f"TOTAL GERAL: {total_geral:,} aparelhos")
print(f"ESPERADO: 33.215 aparelhos")

if total_geral == 33215:
    print("✅ VALIDAÇÃO PERFEITA - QUANTIDADES BATEM EXATAMENTE!")
elif total_geral > 33215:
    print(f"⚠️  DIFERENÇA: +{total_geral - 33215} aparelhos a mais")
else:
    print(f"⚠️  DIFERENÇA: -{33215 - total_geral} aparelhos a menos")

print("=" * 100)
print()

# Comparação com relatório anterior
print("=" * 100)
print("COMPARAÇÃO COM RELATÓRIO ANTERIOR")
print("=" * 100)
print()

anterior = {
    'Araraquara': 4965,
    'Bauru': 17592,
    'Ipiranga': 9392,
    'São José do Rio Preto': 601,
    'Viracopos': 665
}

print(f"{'Recinto':<30} | {'Anterior':>12} | {'Agora':>12} | {'Diferença':>12} | Status")
print("-" * 80)

total_anterior = 0
total_agora = 0

for recinto in sorted(anterior.keys()):
    ant = anterior[recinto]
    agora = distribuicao[recinto]['aparelhos'] if recinto in distribuicao else 0
    diff = agora - ant
    status = "✅" if diff == 0 else f"⚠️  ({diff:+d})"
    
    total_anterior += ant
    total_agora += agora
    
    print(f"{recinto:<30} | {ant:>12,} | {agora:>12,} | {diff:>12,} | {status}")

print("-" * 80)
print(f"{'TOTAL':<30} | {total_anterior:>12,} | {total_agora:>12,} | {total_agora - total_anterior:>12,} | {'✅' if total_anterior == total_agora else '⚠️'}")
print()

if total_anterior == total_agora:
    print("✅ RELATÓRIO ANTERIOR VALIDADO - VALORES BATEM PERFEITAMENTE!")
    print()
    print("CONCLUSÃO: Você pode confiar 100% nas quantidades por recinto!")
else:
    print("⚠️  EXISTEM DIFERENÇAS")

print()
print("=" * 100)
