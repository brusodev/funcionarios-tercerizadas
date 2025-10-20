import PyPDF2
import re
from collections import defaultdict, Counter
from pathlib import Path

def normalizar_quantidade(qtd_str):
    """Converte quantidade com vírgula para inteiro"""
    try:
        return int(float(str(qtd_str).replace(',', '.')))
    except:
        return 0

def normalizar_valor(valor_str):
    """Converte string de valor brasileiro para float"""
    try:
        valor_limpo = valor_str.replace('.', '').replace(',', '.')
        return float(valor_limpo)
    except:
        return 0.0

def extrair_texto_pdf(caminho_pdf):
    """Extrai todo o texto de um arquivo PDF"""
    with open(caminho_pdf, 'rb') as arquivo:
        leitor_pdf = PyPDF2.PdfReader(arquivo)
        texto_completo = []
        for pagina in leitor_pdf.pages:
            texto_completo.append(pagina.extract_text())
        return '\n'.join(texto_completo)

def analisar_pdf_profundamente(caminho_pdf, numero_pdf):
    """Análise profunda de um PDF"""
    
    print(f"\n{'='*100}")
    print(f"ANÁLISE PROFUNDA: PDF {numero_pdf}")
    print(f"Arquivo: {caminho_pdf}")
    print(f"{'='*100}")
    
    # Extrai texto
    texto = extrair_texto_pdf(str(caminho_pdf))
    linhas = texto.split('\n')
    
    print(f"\n📊 ESTATÍSTICAS GERAIS:")
    print(f"   Total de linhas no PDF: {len(linhas):,}")
    
    # Padrões que vamos testar
    padroes_teste = {
        'V5_COMPLETO': r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades|kg)\s+((?:SMARTPHONE|TELEFONE\s+CELULAR|APARELHO\s+CELULAR|IPHONE|(?<!TELEFONE\s)(?<!APARELHO\s)CELULAR|(?:REDMI|NOTE|POCO|POCOPHONE|MI)\s+\d+).*)',
        'SMARTPHONE': r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades|kg)\s+SMARTPHONE',
        'TELEFONE_CELULAR': r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades|kg)\s+TELEFONE\s+CELULAR',
        'IPHONE': r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades|kg)\s+IPHONE',
        'APARELHO_CELULAR': r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades|kg)\s+APARELHO\s+CELULAR',
        'CELULAR_STANDALONE': r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades|kg)\s+(?<!TELEFONE\s)(?<!APARELHO\s)CELULAR',
        'XIAOMI_SEM_PREFIXO': r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades|kg)\s+(?:REDMI|NOTE|POCO|MI)\s+\d+'
    }
    
    # Testa cada padrão
    resultados_padroes = {}
    itens_por_padrao = {}
    
    padrao_codigo = r'^\d+\s*-\s*\d+'
    
    for nome_padrao, regex in padroes_teste.items():
        count = 0
        total_qtd = 0
        exemplos = []
        
        for linha in linhas:
            linha = linha.strip()
            if not linha or re.match(padrao_codigo, linha):
                continue
            
            match = re.match(regex, linha, re.IGNORECASE)
            if match:
                qtd = normalizar_quantidade(match.group(1))
                count += 1
                total_qtd += qtd
                
                if len(exemplos) < 5:  # Guarda até 5 exemplos
                    exemplos.append({
                        'linha': linha[:120],
                        'qtd': qtd
                    })
        
        resultados_padroes[nome_padrao] = {
            'linhas': count,
            'aparelhos': total_qtd,
            'exemplos': exemplos
        }
        
        if nome_padrao == 'V5_COMPLETO':
            # Guarda todos os itens do padrão V5 para análise detalhada
            itens_v5 = []
            for linha in linhas:
                linha = linha.strip()
                if not linha or re.match(padrao_codigo, linha):
                    continue
                
                match = re.match(regex, linha, re.IGNORECASE)
                if match:
                    qtd_str = match.group(1)
                    desc = match.group(2)
                    qtd = normalizar_quantidade(qtd_str)
                    itens_v5.append({
                        'qtd': qtd,
                        'desc': desc,
                        'linha_completa': linha
                    })
            
            itens_por_padrao['V5_COMPLETO'] = itens_v5
    
    # Mostra resultados dos padrões
    print(f"\n📋 RESULTADOS POR PADRÃO:")
    print(f"{'Padrão':<25} {'Linhas':<10} {'Aparelhos':<12}")
    print("-" * 50)
    
    for nome, dados in resultados_padroes.items():
        print(f"{nome:<25} {dados['linhas']:<10} {dados['aparelhos']:<12}")
    
    # Análise detalhada do padrão V5
    itens_v5 = itens_por_padrao.get('V5_COMPLETO', [])
    
    print(f"\n{'='*100}")
    print(f"ANÁLISE DETALHADA - PADRÃO V5")
    print(f"{'='*100}")
    
    # Estatísticas de quantidades
    quantidades = [item['qtd'] for item in itens_v5]
    total_aparelhos = sum(quantidades)
    total_linhas = len(quantidades)
    
    print(f"\n📊 ESTATÍSTICAS:")
    print(f"   Total de linhas encontradas: {total_linhas:,}")
    print(f"   Total de aparelhos: {total_aparelhos:,}")
    print(f"   Média por linha: {total_aparelhos/total_linhas:.1f}" if total_linhas > 0 else "N/A")
    print(f"   Quantidade mínima: {min(quantidades) if quantidades else 0}")
    print(f"   Quantidade máxima: {max(quantidades) if quantidades else 0}")
    
    # Distribuição de quantidades
    counter_qtd = Counter(quantidades)
    print(f"\n📈 TOP 10 QUANTIDADES MAIS COMUNS:")
    for qtd, count in counter_qtd.most_common(10):
        print(f"   {qtd} aparelho(s): {count} linhas ({count * qtd} aparelhos no total)")
    
    # Análise de palavras-chave nas descrições
    print(f"\n🔍 ANÁLISE DE PALAVRAS-CHAVE NAS DESCRIÇÕES:")
    
    palavras_chave = {
        'SMARTPHONE': 0,
        'IPHONE': 0,
        'TELEFONE CELULAR': 0,
        'APARELHO CELULAR': 0,
        'XIAOMI': 0,
        'REDMI': 0,
        'SAMSUNG': 0,
        'MOTOROLA': 0,
        'APPLE': 0,
        'NOTE': 0,
        'POCO': 0,
        'GALAXY': 0
    }
    
    for item in itens_v5:
        desc_upper = item['desc'].upper()
        for palavra in palavras_chave.keys():
            if palavra in desc_upper:
                palavras_chave[palavra] += item['qtd']
    
    print(f"   {'Palavra-chave':<20} {'Aparelhos':<10}")
    print("   " + "-" * 35)
    for palavra, count in sorted(palavras_chave.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"   {palavra:<20} {count:>10,}")
    
    # Análise de valores (R$)
    print(f"\n💰 ANÁLISE DE VALORES:")
    
    itens_com_valor = []
    itens_sem_valor = []
    
    for i, item in enumerate(itens_v5):
        # Procura valor nas próximas 10 linhas do PDF
        linha_idx = -1
        for j, linha in enumerate(linhas):
            if item['linha_completa'] in linha:
                linha_idx = j
                break
        
        valor_encontrado = 0.0
        if linha_idx >= 0:
            for j in range(linha_idx, min(linha_idx + 10, len(linhas))):
                match_valor = re.search(r'R\$\s*([\d.,]+)', linhas[j])
                if match_valor:
                    valor_encontrado = normalizar_valor(match_valor.group(1))
                    break
        
        if valor_encontrado > 0:
            itens_com_valor.append({
                **item,
                'valor_unitario': valor_encontrado,
                'valor_total': valor_encontrado * item['qtd']
            })
        else:
            itens_sem_valor.append(item)
    
    total_valor = sum(i['valor_total'] for i in itens_com_valor)
    
    print(f"   Linhas COM valor: {len(itens_com_valor)} ({sum(i['qtd'] for i in itens_com_valor):,} aparelhos)")
    print(f"   Linhas SEM valor: {len(itens_sem_valor)} ({sum(i['qtd'] for i in itens_sem_valor):,} aparelhos)")
    print(f"   Valor total encontrado: R$ {total_valor:,.2f}")
    
    if itens_com_valor:
        valores = [i['valor_unitario'] for i in itens_com_valor]
        print(f"   Valor unitário médio: R$ {sum(valores)/len(valores):,.2f}")
        print(f"   Valor unitário mínimo: R$ {min(valores):,.2f}")
        print(f"   Valor unitário máximo: R$ {max(valores):,.2f}")
    
    # Procura por padrões que podem estar sendo perdidos
    print(f"\n{'='*100}")
    print(f"🔎 PROCURANDO PADRÕES NÃO CAPTURADOS")
    print(f"{'='*100}")
    
    # Linhas que começam com quantidade mas não foram capturadas
    linhas_com_qtd_nao_capturadas = []
    padrao_qtd_generica = r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades|kg)\s+(.+)'
    
    linhas_capturadas_set = set(item['linha_completa'] for item in itens_v5)
    
    for linha in linhas:
        linha = linha.strip()
        if not linha or re.match(padrao_codigo, linha):
            continue
        
        if linha in linhas_capturadas_set:
            continue
        
        match = re.match(padrao_qtd_generica, linha, re.IGNORECASE)
        if match:
            qtd = normalizar_quantidade(match.group(1))
            desc = match.group(2)
            
            # Verifica se pode ser um celular
            desc_upper = desc.upper()
            palavras_suspeitas = ['CELULAR', 'SMARTPHONE', 'TELEFONE', 'IPHONE', 'APPLE', 
                                 'SAMSUNG', 'XIAOMI', 'MOTOROLA', 'GALAXY', 'REDMI', 'NOTE',
                                 'POCO', 'MI ', 'A0', 'A1', 'A2', 'A3', 'S2', 'G6']
            
            eh_suspeito = any(palavra in desc_upper for palavra in palavras_suspeitas)
            
            if eh_suspeito:
                linhas_com_qtd_nao_capturadas.append({
                    'qtd': qtd,
                    'desc': desc[:100],
                    'linha': linha[:120]
                })
    
    if linhas_com_qtd_nao_capturadas:
        print(f"\n⚠️ ATENÇÃO: {len(linhas_com_qtd_nao_capturadas)} linhas suspeitas NÃO capturadas!")
        print(f"   Total de aparelhos: {sum(i['qtd'] for i in linhas_com_qtd_nao_capturadas):,}")
        print(f"\n   Primeiras 20 linhas:")
        for i, item in enumerate(linhas_com_qtd_nao_capturadas[:20]):
            print(f"\n   {i+1}. Qtd: {item['qtd']}")
            print(f"      {item['linha']}")
    else:
        print(f"\n✅ Nenhuma linha suspeita não capturada encontrada!")
    
    # Retorna resumo
    return {
        'numero_pdf': numero_pdf,
        'total_linhas_pdf': len(linhas),
        'linhas_v5': total_linhas,
        'aparelhos_v5': total_aparelhos,
        'valor_total': total_valor,
        'itens_com_valor': len(itens_com_valor),
        'itens_sem_valor': len(itens_sem_valor),
        'suspeitas_nao_capturadas': len(linhas_com_qtd_nao_capturadas),
        'aparelhos_suspeitos': sum(i['qtd'] for i in linhas_com_qtd_nao_capturadas) if linhas_com_qtd_nao_capturadas else 0
    }

# Lista PDFs para análise detalhada
print("="*100)
print("ANÁLISE MINUCIOSA DOS PDFs PRINCIPAIS")
print("="*100)

# PDFs prioritários para análise
pdfs_prioridade = [
    '0735',  # O MAIOR
    '0734',  # Segundo maior
    '0739',  # Terceiro maior
    '0745',  # Quarto maior
    '0747',  # Temos Excel deste
    '0744',  # Grande também
]

resultados_analise = []

for numero in pdfs_prioridade:
    # Padrão: ADM 0800100_0735_2025 de 30_09_2025.PDF
    pdf_pattern = f"ADM*_{numero}_*.PDF"
    pdf_files = list(Path('.').glob(pdf_pattern))
    
    if pdf_files:
        resultado = analisar_pdf_profundamente(pdf_files[0], numero)
        resultados_analise.append(resultado)
    else:
        print(f"\n⚠️ PDF {numero} não encontrado (padrão: {pdf_pattern})")

# Relatório consolidado
print(f"\n{'='*100}")
print(f"RELATÓRIO CONSOLIDADO DA ANÁLISE")
print(f"{'='*100}")

print(f"\n{'PDF':<6} {'Linhas PDF':<12} {'Linhas V5':<12} {'Aparelhos':<12} {'Valor Total':<18} {'Suspeitas':<10}")
print("-" * 100)

for r in resultados_analise:
    print(f"{r['numero_pdf']:<6} {r['total_linhas_pdf']:<12,} {r['linhas_v5']:<12,} {r['aparelhos_v5']:<12,} R$ {r['valor_total']:<15,.2f} {r['aparelhos_suspeitos']:<10,}")

print(f"\n{'='*100}")
print(f"TOTAIS:")
print(f"{'='*100}")
print(f"Total de aparelhos (V5): {sum(r['aparelhos_v5'] for r in resultados_analise):,}")
print(f"Total de suspeitas não capturadas: {sum(r['aparelhos_suspeitos'] for r in resultados_analise):,}")
print(f"Valor total: R$ {sum(r['valor_total'] for r in resultados_analise):,.2f}")
