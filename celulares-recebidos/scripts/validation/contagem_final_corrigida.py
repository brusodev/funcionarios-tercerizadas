import PyPDF2
import re
import json
from collections import defaultdict

# Padrões dos recintos
padroes_recinto = {
    'Bauru': r'305\s*-\s*810300.*Bauru',
    'Araraquara': r'16\s*-\s*810900.*Araraquara',
    'São José': r'2\s*-\s*DEPÓSITO SAPOL.*SJR',
    'Viracopos': r'1\s*-\s*AEROPORTOS BRASIL VIRACOPOS',
    'Ipiranga': r'309\s*-\s*817900.*IPIRANGA'
}

# Linhas EXATAS a remover (por índice)
linhas_remover_0735 = {352, 354, 356, 824}

padrao_total = r'Total\s+do\s+ADM\s*:\s*R\$\s*([\d.]+,\d+)'

pdf_files = [f'ADM 0800100_073{i}_2025 de 30_09_2025.PDF' for i in range(3, 8)] + \
            [f'ADM 0800100_074{i}_2025 de 30_09_2025.PDF' for i in range(0, 8)] + \
            ['ADM 0800100_0747_2025 de 30092025.PDF']

resultado_por_recinto = defaultdict(lambda: {'aparelhos': 0, 'valor': 0.0})
resultado_por_pdf = {}

total_geral_aparelhos = 0
total_geral_valor = 0.0

print("=== RECONTAGEM FINAL (REMOVENDO 4 LINHAS DUPLICADAS) ===\n")

for pdf_file in pdf_files:
    try:
        with open(pdf_file, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        
        lines = text.split('\n')
        
        # Extrair total do ADM
        total_match = re.search(padrao_total, text)
        if total_match:
            valor_str = total_match.group(1).replace('.', '').replace(',', '.')
            total_valor = float(valor_str)
        else:
            total_valor = 0.0
        
        # Contar aparelhos por recinto
        recinto_atual = None
        aparelhos_neste_pdf = defaultdict(int)
        linhas_removidas_pdf = 0
        
        for idx, linha in enumerate(lines):
            # REMOVER as 4 linhas específicas DO PDF 0735
            if 'ADM 0800100_0735_2025' in pdf_file and idx in linhas_remover_0735:
                linhas_removidas_pdf += 1
                continue
            
            # Detectar mudança de recinto
            for nome_recinto, padrao in padroes_recinto.items():
                if re.search(padrao, linha):
                    recinto_atual = nome_recinto
                    break
            
            # Procurar linhas de aparelhos
            match = re.match(r'^(\d+,\d+)\s+un\s+(.+)$', linha)
            if match and recinto_atual:
                qty_str = match.group(1).replace(',', '.')
                qtd = int(float(qty_str))
                aparelhos_neste_pdf[recinto_atual] += qtd
        
        # Total deste PDF
        total_aparelhos_pdf = sum(aparelhos_neste_pdf.values())
        
        # Distribuir valor proporcionalmente
        resultado_por_pdf[pdf_file] = {
            'aparelhos': total_aparelhos_pdf,
            'valor': total_valor,
            'linhas_removidas': linhas_removidas_pdf,
            'por_recinto': {}
        }
        
        if total_aparelhos_pdf > 0:
            for nome_recinto, qtd_aparelhos in aparelhos_neste_pdf.items():
                proporcao = qtd_aparelhos / total_aparelhos_pdf
                valor_recinto = total_valor * proporcao
                
                resultado_por_recinto[nome_recinto]['aparelhos'] += qtd_aparelhos
                resultado_por_recinto[nome_recinto]['valor'] += valor_recinto
                
                total_geral_aparelhos += qtd_aparelhos
                total_geral_valor += valor_recinto
        
        # Output
        info = f"📄 {pdf_file}: {total_aparelhos_pdf:,} aparelhos"
        if linhas_removidas_pdf > 0:
            info += f" (removidas {linhas_removidas_pdf} linhas duplicadas)"
        print(info)
        for nome_recinto in sorted(aparelhos_neste_pdf.keys()):
            qtd = aparelhos_neste_pdf[nome_recinto]
            print(f"     - {nome_recinto}: {qtd:,}")
        print()
    
    except FileNotFoundError:
        pass

print("\n" + "="*70)
print("=== TOTAIS FINAIS POR RECINTO ===")
print("="*70 + "\n")

for recinto in sorted(resultado_por_recinto.keys()):
    data = resultado_por_recinto[recinto]
    print(f"📍 {recinto.upper()}")
    print(f"   Aparelhos: {data['aparelhos']:,}")
    print(f"   Valor: R$ {data['valor']:,.2f}")
    print()

print("\n" + "="*70)
print(f"🎯 TOTAL GERAL (CORRIGIDO)")
print(f"   Aparelhos: {total_geral_aparelhos:,}")
print(f"   Valor: R$ {total_geral_valor:,.2f}")
print(f"   SUA CONTAGEM: 32.015")
print(f"   DIFERENÇA: {total_geral_aparelhos - 32015:+,}")
print("="*70)

# Salvar JSON
with open('aparelhos_por_recinto_FINAL_CORRIGIDO.json', 'w', encoding='utf-8') as f:
    json.dump({
        'metadata': {
            'total_aparelhos': total_geral_aparelhos,
            'total_valor': f"R$ {total_geral_valor:,.2f}",
            'observacao': 'Removidas 4 linhas duplicadas do PDF 0735 (692+161+119+206 un)',
            'comparacao_usuario': {
                'usuario_contou': 32015,
                'script_contou': total_geral_aparelhos,
                'diferenca': total_geral_aparelhos - 32015
            }
        },
        'por_recinto': {k: {
            'aparelhos': v['aparelhos'],
            'valor': f"R$ {v['valor']:,.2f}"
        } for k, v in resultado_por_recinto.items()}
    }, f, ensure_ascii=False, indent=2)

print("\n✅ Arquivo salvo: aparelhos_por_recinto_FINAL_CORRIGIDO.json")
