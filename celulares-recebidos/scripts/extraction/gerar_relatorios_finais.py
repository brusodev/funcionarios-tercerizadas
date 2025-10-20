import PyPDF2
import re
import json
import csv
from collections import defaultdict

# Padrões dos recintos
padroes_recinto = {
    'Bauru': r'305\s*-\s*810300.*Bauru',
    'Araraquara': r'16\s*-\s*810900.*Araraquara',
    'São José do Rio Preto': r'2\s*-\s*DEPÓSITO SAPOL.*SJR',
    'Viracopos': r'1\s*-\s*AEROPORTOS BRASIL VIRACOPOS',
    'Ipiranga': r'309\s*-\s*817900.*IPIRANGA',
}

padrao_total = r'Total\s+do\s+ADM\s*:\s*R\$\s*([\d.]+,\d+)'

# Linhas a REMOVER para gerar relatório com 32.015
linhas_remover = {
    'ADM 0800100_0735_2025 de 30_09_2025.PDF': [352, 354, 356, 824],  # 4 consolidações
    'ADM 0800100_0738_2025 de 30_09_2025.PDF': ['BLOQUEADO', 'SEM EMBALAGEM'],  # BLOQUEADO + SEM EMBALAGEM
    'ADM 0800100_0744_2025 de 30_09_2025.PDF': ['SEM CAPACIDADE'],  # SEM CAPACIDADE
}

pdf_files = [f'ADM 0800100_073{i}_2025 de 30_09_2025.PDF' for i in range(3, 8)] + \
            [f'ADM 0800100_074{i}_2025 de 30_09_2025.PDF' for i in range(0, 8)] + \
            ['ADM 0800100_0747_2025 de 30092025.PDF']

def processar_pdf(pdf_file, remover_problematicos=False):
    """
    Processa um PDF e retorna aparelhos por recinto
    Se remover_problematicos=True, remove aparelhos com problemas
    """
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
        aparelhos_kg_neste_pdf = defaultdict(int)
        
        # Controle de exclusão para linhas específicas
        linhas_excluidas = set()
        
        for idx, linha in enumerate(lines):
            # Verificar se deve remover esta linha (para versão 32.015)
            if remover_problematicos:
                if pdf_file in linhas_remover:
                    # Para PDF 0735: remover por índice
                    if isinstance(linhas_remover[pdf_file][0], int) and idx in linhas_remover[pdf_file]:
                        linhas_excluidas.add(idx)
                        continue
                    
                    # Para PDF 0738 e 0744: remover por palavra-chave
                    for keyword in linhas_remover.get(pdf_file, []):
                        if isinstance(keyword, str) and keyword in linha.upper():
                            linhas_excluidas.add(idx)
                            break
            
            # Detectar mudança de recinto
            for nome_recinto, padrao in padroes_recinto.items():
                if re.search(padrao, linha):
                    recinto_atual = nome_recinto
                    break
            
            # Procurar linhas de aparelhos em UN
            match_un = re.match(r'^(\d+,\d+)\s+un\s+(.+)$', linha)
            if match_un and recinto_atual and idx not in linhas_excluidas:
                qty_str = match_un.group(1).replace(',', '.')
                qtd = int(float(qty_str))
                aparelhos_neste_pdf[recinto_atual] += qtd
            
            # Procurar linhas de aparelhos em KG (especial para PDF 0743)
            if 'ADM 0800100_0743_2025' in pdf_file:
                match_kg = re.search(r'(\d+,\d+)\s*kg\s+TELEFONE', linha, re.IGNORECASE)
                if match_kg and recinto_atual:
                    kg_str = match_kg.group(1).replace(',', '.')
                    kg = float(kg_str)
                    aparelhos_kg = round(kg / 0.49)
                    aparelhos_kg_neste_pdf[recinto_atual] += aparelhos_kg
        
        # Adicionar aparelhos em KG aos totais
        for recinto in aparelhos_kg_neste_pdf:
            aparelhos_neste_pdf[recinto] += aparelhos_kg_neste_pdf[recinto]
        
        return aparelhos_neste_pdf, total_valor
    
    except FileNotFoundError:
        return defaultdict(int), 0.0

# ==================== GERAR RELATÓRIO COM 32.015 ====================
print("="*80)
print("GERANDO RELATÓRIO COM 32.015 APARELHOS (SUA CONTAGEM)")
print("="*80 + "\n")

resultado_32015 = defaultdict(lambda: {'aparelhos': 0, 'valor': 0.0})
total_geral_32015 = 0
total_valor_32015 = 0.0

for pdf_file in pdf_files:
    aparelhos_por_recinto, valor_total = processar_pdf(pdf_file, remover_problematicos=True)
    
    if aparelhos_por_recinto:
        total_aparelhos_pdf = sum(aparelhos_por_recinto.values())
        
        if total_aparelhos_pdf > 0:
            for nome_recinto, qtd_aparelhos in aparelhos_por_recinto.items():
                proporcao = qtd_aparelhos / total_aparelhos_pdf
                valor_recinto = valor_total * proporcao
                
                resultado_32015[nome_recinto]['aparelhos'] += qtd_aparelhos
                resultado_32015[nome_recinto]['valor'] += valor_recinto
                
                total_geral_32015 += qtd_aparelhos
                total_valor_32015 += valor_recinto

print("\n📊 TOTAIS POR RECINTO (32.015 APARELHOS - SUA CONTAGEM):\n")
for recinto in ['Bauru', 'Araraquara', 'Ipiranga', 'Viracopos', 'São José do Rio Preto']:
    if recinto in resultado_32015:
        data = resultado_32015[recinto]
        print(f"  {recinto:<25} {data['aparelhos']:>8,} aparelhos | R$ {data['valor']:>15,.2f}")

print(f"\n  {'TOTAL':<25} {total_geral_32015:>8,} aparelhos | R$ {total_valor_32015:>15,.2f}")

# ==================== GERAR RELATÓRIO COM 32.027 ====================
print("\n" + "="*80)
print("GERANDO RELATÓRIO COM 32.027 APARELHOS (CONTAGEM COMPLETA)")
print("="*80 + "\n")

resultado_32027 = defaultdict(lambda: {'aparelhos': 0, 'valor': 0.0})
total_geral_32027 = 0
total_valor_32027 = 0.0

for pdf_file in pdf_files:
    aparelhos_por_recinto, valor_total = processar_pdf(pdf_file, remover_problematicos=False)
    
    if aparelhos_por_recinto:
        total_aparelhos_pdf = sum(aparelhos_por_recinto.values())
        
        if total_aparelhos_pdf > 0:
            for nome_recinto, qtd_aparelhos in aparelhos_por_recinto.items():
                proporcao = qtd_aparelhos / total_aparelhos_pdf
                valor_recinto = valor_total * proporcao
                
                resultado_32027[nome_recinto]['aparelhos'] += qtd_aparelhos
                resultado_32027[nome_recinto]['valor'] += valor_recinto
                
                total_geral_32027 += qtd_aparelhos
                total_valor_32027 += valor_recinto

print("\n📊 TOTAIS POR RECINTO (32.027 APARELHOS - CONTAGEM COMPLETA):\n")
for recinto in ['Bauru', 'Araraquara', 'Ipiranga', 'Viracopos', 'São José do Rio Preto']:
    if recinto in resultado_32027:
        data = resultado_32027[recinto]
        print(f"  {recinto:<25} {data['aparelhos']:>8,} aparelhos | R$ {data['valor']:>15,.2f}")

print(f"\n  {'TOTAL':<25} {total_geral_32027:>8,} aparelhos | R$ {total_valor_32027:>15,.2f}")

# ==================== SALVAR JSON ====================
print("\n" + "="*80)
print("SALVANDO ARQUIVOS...")
print("="*80 + "\n")

# JSON 32.015
json_32015 = {
    'metadata': {
        'total_aparelhos': total_geral_32015,
        'total_valor': f"R$ {total_valor_32015:,.2f}",
        'versao': 'Contagem do Usuário (32.015)',
        'observacoes': [
            'Removidas 4 linhas de consolidação do PDF 0735',
            'Removido 1 aparelho BLOQUEADO do PDF 0738',
            'Removido 1 aparelho SEM EMBALAGEM do PDF 0738',
            'Removido 1 aparelho SEM CAPACIDADE do PDF 0744',
            'Inclusos 3 aparelhos em KG do PDF 0743'
        ]
    },
    'por_recinto': {}
}

for recinto in ['Bauru', 'Araraquara', 'Ipiranga', 'Viracopos', 'São José do Rio Preto']:
    if recinto in resultado_32015:
        data = resultado_32015[recinto]
        json_32015['por_recinto'][recinto] = {
            'aparelhos': data['aparelhos'],
            'valor': f"R$ {data['valor']:,.2f}",
            'percentual_aparelhos': f"{(data['aparelhos']/total_geral_32015)*100:.1f}%",
            'percentual_valor': f"{(data['valor']/total_valor_32015)*100:.1f}%"
        }

with open('RELATORIO_32015_SUA_CONTAGEM.json', 'w', encoding='utf-8') as f:
    json.dump(json_32015, f, ensure_ascii=False, indent=2)

# JSON 32.027
json_32027 = {
    'metadata': {
        'total_aparelhos': total_geral_32027,
        'total_valor': f"R$ {total_valor_32027:,.2f}",
        'versao': 'Contagem Completa (32.027)',
        'observacoes': [
            'Inclui 4 linhas de consolidação do PDF 0735',
            'Inclui 1 aparelho BLOQUEADO do PDF 0738',
            'Inclui 1 aparelho SEM EMBALAGEM do PDF 0738',
            'Inclui 1 aparelho SEM CAPACIDADE do PDF 0744',
            'Inclui 3 aparelhos em KG do PDF 0743'
        ]
    },
    'por_recinto': {}
}

for recinto in ['Bauru', 'Araraquara', 'Ipiranga', 'Viracopos', 'São José do Rio Preto']:
    if recinto in resultado_32027:
        data = resultado_32027[recinto]
        json_32027['por_recinto'][recinto] = {
            'aparelhos': data['aparelhos'],
            'valor': f"R$ {data['valor']:,.2f}",
            'percentual_aparelhos': f"{(data['aparelhos']/total_geral_32027)*100:.1f}%",
            'percentual_valor': f"{(data['valor']/total_valor_32027)*100:.1f}%"
        }

with open('RELATORIO_32027_CONTAGEM_COMPLETA.json', 'w', encoding='utf-8') as f:
    json.dump(json_32027, f, ensure_ascii=False, indent=2)

print("✅ JSON gerado: RELATORIO_32015_SUA_CONTAGEM.json")
print("✅ JSON gerado: RELATORIO_32027_CONTAGEM_COMPLETA.json")

# ==================== SALVAR CSV ====================
# CSV 32.015
with open('RELATORIO_32015_SUA_CONTAGEM.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(['Recinto', 'Aparelhos', 'Valor R$', '% Aparelhos', '% Valor'])
    
    for recinto in ['Bauru', 'Araraquara', 'Ipiranga', 'Viracopos', 'São José do Rio Preto']:
        if recinto in resultado_32015:
            data = resultado_32015[recinto]
            writer.writerow([
                recinto,
                data['aparelhos'],
                f"{data['valor']:.2f}",
                f"{(data['aparelhos']/total_geral_32015)*100:.1f}%",
                f"{(data['valor']/total_valor_32015)*100:.1f}%"
            ])
    
    writer.writerow(['TOTAL', total_geral_32015, f"{total_valor_32015:.2f}", '100%', '100%'])

print("✅ CSV gerado: RELATORIO_32015_SUA_CONTAGEM.csv")

# CSV 32.027
with open('RELATORIO_32027_CONTAGEM_COMPLETA.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(['Recinto', 'Aparelhos', 'Valor R$', '% Aparelhos', '% Valor'])
    
    for recinto in ['Bauru', 'Araraquara', 'Ipiranga', 'Viracopos', 'São José do Rio Preto']:
        if recinto in resultado_32027:
            data = resultado_32027[recinto]
            writer.writerow([
                recinto,
                data['aparelhos'],
                f"{data['valor']:.2f}",
                f"{(data['aparelhos']/total_geral_32027)*100:.1f}%",
                f"{(data['valor']/total_valor_32027)*100:.1f}%"
            ])
    
    writer.writerow(['TOTAL', total_geral_32027, f"{total_valor_32027:.2f}", '100%', '100%'])

print("✅ CSV gerado: RELATORIO_32027_CONTAGEM_COMPLETA.csv")

print("\n" + "="*80)
print("✅ TODOS OS RELATÓRIOS GERADOS COM SUCESSO!")
print("="*80)
