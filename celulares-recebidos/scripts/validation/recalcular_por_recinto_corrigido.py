import PyPDF2
import re
import json
from collections import defaultdict

# Padrões dos recintos (fornecidos pelo usuário)
padroes_recinto = {
    'Bauru': r'305\s*-\s*810300.*Bauru',
    'Araraquara': r'16\s*-\s*810900.*Araraquara',
    'São José': r'2\s*-\s*DEPÓSITO SAPOL.*SJR',
    'Viracopos': r'1\s*-\s*AEROPORTOS BRASIL VIRACOPOS',
    'Ipiranga': r'309\s*-\s*817900.*IPIRANGA'
}

# Lines a REMOVER (duplicatas)
linhas_remover = {
    '692,00 un SMARTPHONE XIAOMI REDMI NOTE 13 256GB CHINA',
    '161,00 un SMARTPHONE XIAOMI REDMI NOTE 13 5G 256GB CHINA',
    '119,00 un SMARTPHONE XIAOMI POCO C65 128GB INDIA',
    '206,00 un SMARTPHONE XIAOMI REDMI NOTE 14 256GB CHINA'
}

# Padrão para encontrar "Total do ADM"
padrao_total = r'Total\s+do\s+ADM\s*:\s*R\$\s*([\d.]+,\d+)'

pdf_files = [f'ADM 0800100_073{i}_2025 de 30_09_2025.PDF' for i in range(3, 8)] + \
            [f'ADM 0800100_074{i}_2025 de 30_09_2025.PDF' for i in range(0, 8)] + \
            ['ADM 0800100_0747_2025 de 30092025.PDF']

resultado_por_recinto = defaultdict(lambda: {'aparelhos': 0, 'valor': 0.0})
resultado_por_pdf = {}
aparelhos_por_recinto_pdf = defaultdict(lambda: defaultdict(int))
valores_por_recinto_pdf = defaultdict(lambda: defaultdict(float))

total_geral_aparelhos = 0
total_geral_valor = 0.0

print("=== RECONTAGEM COM REMOÇÃO DE DUPLICATAS ===\n")

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
        
        for linha in lines:
            # Verificar se é mudança de recinto
            for nome_recinto, padrao in padroes_recinto.items():
                if re.search(padrao, linha):
                    recinto_atual = nome_recinto
                    break
            
            # Verificar se é linha de aparelho
            match = re.match(r'^(\d+,\d+)\s+un\s+(.+)$', linha)
            if match and recinto_atual:
                # Verificar se deve remover (é uma das 4 duplicatas)
                linha_completa = linha.strip()
                
                # Checar se é uma das linhas a remover (aproximado)
                eh_duplicata = False
                for padrao_remover in linhas_remover:
                    if padrao_remover in linha_completa:
                        eh_duplicata = True
                        break
                
                if not eh_duplicata:
                    qty_str = match.group(1).replace(',', '.')
                    qtd = int(float(qty_str))
                    aparelhos_neste_pdf[recinto_atual] += qtd
        
        # Calcular total de aparelhos DESTE PDF (sem as 4 duplicatas)
        total_aparelhos_pdf = sum(aparelhos_neste_pdf.values())
        
        # Distribuir valor proporcionalmente por recinto
        resultado_por_pdf[pdf_file] = {
            'aparelhos': total_aparelhos_pdf,
            'valor': total_valor,
            'por_recinto': {}
        }
        
        if total_aparelhos_pdf > 0:
            for nome_recinto, qtd_aparelhos in aparelhos_neste_pdf.items():
                proporcao = qtd_aparelhos / total_aparelhos_pdf
                valor_recinto = total_valor * proporcao
                
                resultado_por_recinto[nome_recinto]['aparelhos'] += qtd_aparelhos
                resultado_por_recinto[nome_recinto]['valor'] += valor_recinto
                resultado_por_pdf[pdf_file]['por_recinto'][nome_recinto] = {
                    'aparelhos': qtd_aparelhos,
                    'valor': valor_recinto
                }
                
                total_geral_aparelhos += qtd_aparelhos
                total_geral_valor += valor_recinto
        
        print(f"📄 {pdf_file}")
        print(f"   Total: {total_aparelhos_pdf:,} aparelhos | R$ {total_valor:,.2f}")
        for nome_recinto in sorted(aparelhos_neste_pdf.keys()):
            qtd = aparelhos_neste_pdf[nome_recinto]
            print(f"     - {nome_recinto}: {qtd:,} aparelhos")
        print()
    
    except FileNotFoundError:
        pass

print("\n" + "="*60)
print("=== TOTAIS POR RECINTO (COM CORREÇÃO) ===")
print("="*60 + "\n")

for recinto in sorted(resultado_por_recinto.keys()):
    data = resultado_por_recinto[recinto]
    print(f"📍 {recinto.upper()}")
    print(f"   Aparelhos: {data['aparelhos']:,}")
    print(f"   Valor: R$ {data['valor']:,.2f}")
    print()

print("\n" + "="*60)
print(f"🎯 TOTAL GERAL")
print(f"   Aparelhos: {total_geral_aparelhos:,}")
print(f"   Valor: R$ {total_geral_valor:,.2f}")
print("="*60)

# Salvar JSON
with open('aparelhos_por_recinto_CORRIGIDO_SEM_DUPLICATAS.json', 'w', encoding='utf-8') as f:
    json.dump({
        'total': {
            'aparelhos': total_geral_aparelhos,
            'valor': total_geral_valor
        },
        'por_recinto': {k: v for k, v in resultado_por_recinto.items()}
    }, f, ensure_ascii=False, indent=2)

print("\n✅ Arquivo salvo: aparelhos_por_recinto_CORRIGIDO_SEM_DUPLICATAS.json")
