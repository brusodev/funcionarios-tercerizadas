import PyPDF2
import re
import json
import csv
from pathlib import Path
from datetime import datetime

def extrair_texto_pdf(pdf_path):
    """Extrai texto de todas as páginas do PDF"""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        texto_completo = []
        for page in reader.pages:
            texto_completo.append(page.extract_text())
    return '\n'.join(texto_completo)

def processar_pdf_v7(pdf_path):
    """
    V7 - VERSÃO FINAL COM LÓGICA CORRETA DE VALORES
    
    LÓGICA:
    1. Encontrar item com quantidade
    2. Primeiro: buscar valor R$ na MESMA linha
    3. Segundo: buscar primeiro valor R$ nas próximas linhas (ignorando Subtotal)
    4. SEMPRE dividir o valor encontrado pela quantidade para obter valor unitário
    """
    texto = extrair_texto_pdf(pdf_path)
    linhas = texto.split('\n')
    
    # Padrão para identificar linhas de itens
    pattern_item = re.compile(
        r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades|kg)\s+((?:SMARTPHONE|TELEFONE\s+CELULAR|APARELHO\s+CELULAR|APARELHO\s+DE\s+TELEFONE\s+CELULAR|IPHONE|(?<!TELEFONE\s)(?<!APARELHO\s)CELULAR|(?:REDMI|NOTE|POCO|POCOPHONE|MI)\s+\d+).*)',
        re.IGNORECASE
    )
    
    # Padrão para encontrar valores em reais
    pattern_valor = re.compile(r'R\$\s*([\d.]+,\d{2})')
    
    resultados = []
    
    for i, linha in enumerate(linhas):
        match = pattern_item.match(linha.strip())
        if match:
            qtd_str = match.group(1).replace(',', '.')
            quantidade = float(qtd_str)
            descricao = match.group(2).strip()
            
            # PRIMEIRO: tentar na mesma linha (alguns itens têm valor inline)
            valor_total_lote = None
            match_valor_inline = pattern_valor.search(linha)
            if match_valor_inline:
                valor_str = match_valor_inline.group(1).replace('.', '').replace(',', '.')
                valor_total_lote = float(valor_str)
            
            # SEGUNDO: se não encontrou na mesma linha, buscar nas próximas 10 linhas
            if not valor_total_lote:
                for j in range(1, 11):
                    if i + j >= len(linhas):
                        break
                    
                    proxima_linha = linhas[i + j]
                    
                    # Ignorar linhas com Subtotal
                    if 'Subtotal:' in proxima_linha or 'subtotal:' in proxima_linha.lower():
                        continue
                    
                    # Buscar primeiro valor R$
                    match_valor = pattern_valor.search(proxima_linha)
                    if match_valor:
                        valor_str = match_valor.group(1).replace('.', '').replace(',', '.')
                        valor_total_lote = float(valor_str)
                        break
            
            # Calcular valor unitário (SEMPRE dividindo pela quantidade)
            if valor_total_lote:
                valor_unitario = valor_total_lote / quantidade
                valor_total_item = valor_total_lote  # Já é o total
            else:
                valor_unitario = 0
                valor_total_item = 0
            
            resultados.append({
                'quantidade': quantidade,
                'descricao': descricao,
                'valor_unitario': round(valor_unitario, 2),
                'valor_total': round(valor_total_item, 2)
            })
    
    return resultados


# Processar todos os PDFs
print("="*80)
print("PROCESSAMENTO FINAL - VERSÃO V7")
print("="*80)
print(f"Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

pdfs = sorted(Path('.').glob('ADM *.PDF'))
todos_resultados = {}
resumo_geral = []

for pdf in pdfs:
    print(f"Processando {pdf.name}...")
    resultados = processar_pdf_v7(pdf)
    
    total_aparelhos = sum(r['quantidade'] for r in resultados)
    total_valor = sum(r['valor_total'] for r in resultados)
    
    todos_resultados[pdf.stem] = {
        'arquivo': pdf.name,
        'total_aparelhos': int(total_aparelhos),
        'total_valor': round(total_valor, 2),
        'itens': resultados
    }
    
    resumo_geral.append({
        'pdf': pdf.name,
        'aparelhos': int(total_aparelhos),
        'valor_total': round(total_valor, 2)
    })

# RELATÓRIO 1: Resumo por PDF (JSON)
print("\n" + "="*80)
print("GERANDO RELATÓRIO 1: Resumo por PDF (resumo_por_pdf.json)")
print("="*80)

with open('resumo_por_pdf.json', 'w', encoding='utf-8') as f:
    json.dump(resumo_geral, f, ensure_ascii=False, indent=2)
print("✓ Arquivo 'resumo_por_pdf.json' criado")

# RELATÓRIO 2: Detalhado com todos os itens (CSV)
print("\n" + "="*80)
print("GERANDO RELATÓRIO 2: Detalhado com todos os itens (itens_detalhados.csv)")
print("="*80)

with open('itens_detalhados.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.writer(f, delimiter=';')
    writer.writerow(['PDF', 'Quantidade', 'Descrição', 'Valor Unitário', 'Valor Total'])
    
    for pdf_nome, dados in sorted(todos_resultados.items()):
        for item in dados['itens']:
            writer.writerow([
                dados['arquivo'],
                int(item['quantidade']),
                item['descricao'],
                f"R$ {item['valor_unitario']:.2f}".replace('.', ','),
                f"R$ {item['valor_total']:.2f}".replace('.', ',')
            ])

print("✓ Arquivo 'itens_detalhados.csv' criado (separador ';' para Excel)")

# RELATÓRIO 3: Consolidado por modelo (JSON)
print("\n" + "="*80)
print("GERANDO RELATÓRIO 3: Consolidado por modelo (consolidado_por_modelo.json)")
print("="*80)

# Extrair marca e modelo da descrição
consolidado = {}
for pdf_nome, dados in todos_resultados.items():
    for item in dados['itens']:
        desc = item['descricao']
        
        # Normalizar descrição para usar como chave
        # Remove detalhes específicos como SN, IMEI, origem
        desc_limpa = re.sub(r'(SN|IMEI|NUMERO DE SERIE)[:\s].*', '', desc, flags=re.IGNORECASE)
        desc_limpa = re.sub(r'(CHINA|INDIA|VIETNAM|BRASIL).*', '', desc_limpa, flags=re.IGNORECASE)
        desc_limpa = desc_limpa.strip().rstrip(',')
        
        if desc_limpa not in consolidado:
            consolidado[desc_limpa] = {
                'modelo': desc_limpa,
                'quantidade_total': 0,
                'valor_medio': 0,
                'valor_total': 0,
                'valores': []
            }
        
        consolidado[desc_limpa]['quantidade_total'] += item['quantidade']
        consolidado[desc_limpa]['valor_total'] += item['valor_total']
        if item['valor_unitario'] > 0:
            consolidado[desc_limpa]['valores'].append(item['valor_unitario'])

# Calcular médias
for modelo in consolidado.values():
    if modelo['valores']:
        modelo['valor_medio'] = round(sum(modelo['valores']) / len(modelo['valores']), 2)
    modelo['quantidade_total'] = int(modelo['quantidade_total'])
    modelo['valor_total'] = round(modelo['valor_total'], 2)
    del modelo['valores']  # Remover lista de valores do JSON final

# Ordenar por quantidade (maior para menor)
consolidado_lista = sorted(consolidado.values(), key=lambda x: x['quantidade_total'], reverse=True)

with open('consolidado_por_modelo.json', 'w', encoding='utf-8') as f:
    json.dump(consolidado_lista, f, ensure_ascii=False, indent=2)
print("✓ Arquivo 'consolidado_por_modelo.json' criado")

# RELATÓRIO 4: JSON completo com tudo
print("\n" + "="*80)
print("GERANDO RELATÓRIO 4: JSON completo (resultado_completo.json)")
print("="*80)

resultado_final = {
    'data_processamento': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'versao': 'V7 - Final',
    'total_geral': {
        'aparelhos': sum(r['aparelhos'] for r in resumo_geral),
        'valor_total': round(sum(r['valor_total'] for r in resumo_geral), 2)
    },
    'resumo_por_pdf': resumo_geral,
    'detalhes_por_pdf': todos_resultados
}

with open('resultado_completo.json', 'w', encoding='utf-8') as f:
    json.dump(resultado_final, f, ensure_ascii=False, indent=2)
print("✓ Arquivo 'resultado_completo.json' criado")

# RESUMO FINAL
print("\n" + "="*80)
print("RESUMO FINAL - TODOS OS 15 PDFs")
print("="*80)

total_geral_aparelhos = sum(r['aparelhos'] for r in resumo_geral)
total_geral_valor = sum(r['valor_total'] for r in resumo_geral)

print(f"\nTOTAL GERAL:")
print(f"   Aparelhos: {total_geral_aparelhos:,}".replace(',', '.'))
print(f"   Valor total: R$ {total_geral_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

print(f"\nPOR PDF:")
print(f"{'PDF':<50} {'Aparelhos':>12} {'Valor Total':>20}")
print("-" * 85)
for item in sorted(resumo_geral, key=lambda x: x['aparelhos'], reverse=True):
    nome_curto = item['pdf'].replace('ADM 0800100_', '').replace('_2025 de 30_09_2025.PDF', '').replace(' de 30092025.PDF', '')
    print(f"{nome_curto:<50} {item['aparelhos']:>12,}".replace(',', '.') + f" R$ {item['valor_total']:>18,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

print(f"\n{'='*85}")
print(f"{'TOTAL':<50} {total_geral_aparelhos:>12,}".replace(',', '.') + f" R$ {total_geral_valor:>18,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

print("\n" + "="*80)
print("ARQUIVOS GERADOS:")
print("="*80)
print("1. resumo_por_pdf.json - Resumo simples de cada PDF")
print("2. itens_detalhados.csv - Todos os itens linha por linha (Excel)")
print("3. consolidado_por_modelo.json - Agrupado por modelo de celular")
print("4. resultado_completo.json - Dados completos em JSON")
print("\n✓ Processamento concluído!")
print(f"Fim: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
