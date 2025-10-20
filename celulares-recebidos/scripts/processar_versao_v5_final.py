import PyPDF2
import re
import json
import csv
from collections import defaultdict
from pathlib import Path

print("="*80)
print("PROCESSAMENTO COM PADRÃO V5 - FINAL ABSOLUTO")
print("="*80)
print("✅ Agora aceita: SMARTPHONE, TELEFONE CELULAR, CELULAR, IPHONE, APARELHO CELULAR")
print("✅ NOVO: Modelos Xiaomi sem prefixo (NOTE, REDMI, POCO, MI)")
print("="*80)

def extrair_texto_pdf(caminho_pdf):
    """Extrai todo o texto de um arquivo PDF"""
    with open(caminho_pdf, 'rb') as arquivo:
        leitor_pdf = PyPDF2.PdfReader(arquivo)
        texto_completo = []
        for pagina in leitor_pdf.pages:
            texto_completo.append(pagina.extract_text())
        return '\n'.join(texto_completo)

def normalizar_valor(valor_str):
    """Converte string de valor brasileiro para float"""
    try:
        valor_limpo = valor_str.replace('.', '').replace(',', '.')
        return float(valor_limpo)
    except:
        return 0.0

def normalizar_quantidade(qtd_str):
    """Converte quantidade com vírgula para inteiro"""
    try:
        return int(float(qtd_str.replace(',', '.')))
    except:
        return 0

def extrair_linhas_com_valores_v5(texto_pdf):
    """
    Versão 5 - FINAL ABSOLUTA
    Captura:
    - SMARTPHONE, TELEFONE CELULAR, APARELHO CELULAR, IPHONE, CELULAR
    - Modelos Xiaomi sem prefixo: NOTE, REDMI, POCO, MI, POCOPHONE
    """
    linhas = texto_pdf.split('\n')
    itens_encontrados = []
    
    # Padrão V5: Adiciona modelos Xiaomi sem prefixo
    # (?:un|unidade|unidades|kg) = aceita "un", "unidade", "unidades" ou "kg"
    # (?:...) = grupo de captura dos padrões aceitos
    padrao_item = r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades|kg)\s+((?:SMARTPHONE|TELEFONE\s+CELULAR|APARELHO\s+CELULAR|IPHONE|(?<!TELEFONE\s)(?<!APARELHO\s)CELULAR|(?:REDMI|NOTE|POCO|POCOPHONE|MI)\s+\d+).*)'
    
    # Padrão para ignorar linhas de código de região
    padrao_codigo = r'^\d+\s*-\s*\d+'
    
    for i, linha in enumerate(linhas):
        linha = linha.strip()
        
        # Ignora linhas vazias e códigos
        if not linha or re.match(padrao_codigo, linha):
            continue
        
        match = re.match(padrao_item, linha, re.IGNORECASE)
        if match:
            qtd_str = match.group(1)
            descricao = match.group(2)
            quantidade = normalizar_quantidade(qtd_str)
            
            # Procura valor nas próximas 10 linhas
            valor = 0.0
            for j in range(i, min(i + 10, len(linhas))):
                linha_busca = linhas[j]
                match_valor = re.search(r'R\$\s*([\d.,]+)', linha_busca)
                if match_valor:
                    valor = normalizar_valor(match_valor.group(1))
                    break
            
            itens_encontrados.append({
                'quantidade': quantidade,
                'descricao': descricao,
                'valor_unitario': valor,
                'valor_total': valor * quantidade,
                'linha_original': linha
            })
    
    return itens_encontrados

# Processa todos os PDFs
pdf_files = sorted(Path('.').glob('ADM *.PDF'))
print(f"📄 {len(pdf_files)} PDFs encontrados\n")

todos_itens = []
resumo_por_pdf = {}

for pdf_file in pdf_files:
    nome_pdf = pdf_file.name
    print(f"Processando: {nome_pdf}")
    
    try:
        texto = extrair_texto_pdf(str(pdf_file))
        itens = extrair_linhas_com_valores_v5(texto)
        
        # Estatísticas do PDF
        total_aparelhos = sum(item['quantidade'] for item in itens)
        total_valor = sum(item['valor_total'] for item in itens)
        
        # Adiciona informação do PDF a cada item
        for item in itens:
            item['pdf'] = nome_pdf
            todos_itens.append(item)
        
        resumo_por_pdf[nome_pdf] = {
            'total_aparelhos': total_aparelhos,
            'total_linhas': len(itens),
            'total_valor': total_valor
        }
        
        print(f"   ✓ {total_aparelhos} aparelhos | R$ {total_valor:,.2f}")
        
    except Exception as e:
        print(f"   ✗ Erro: {e}")

# Consolida por modelo
print(f"\n{'='*80}")
print("CONSOLIDANDO POR MODELO...")
print(f"{'='*80}")

dados_consolidados = defaultdict(lambda: {'quantidade': 0, 'valor_total': 0.0})

for item in todos_itens:
    modelo = item['descricao']
    dados_consolidados[modelo]['quantidade'] += item['quantidade']
    dados_consolidados[modelo]['valor_total'] += item['valor_total']

# Converte para lista ordenada
dados_json = []
for modelo, dados in sorted(dados_consolidados.items()):
    dados_json.append({
        'modelo': modelo,
        'quantidade_total': dados['quantidade'],
        'valor_total': round(dados['valor_total'], 2)
    })

# Salva JSON consolidado
with open('celulares_com_valores_V5_FINAL.json', 'w', encoding='utf-8') as f:
    json.dump(dados_json, f, ensure_ascii=False, indent=2)

# Salva CSV detalhado
with open('celulares_com_valores_V5_FINAL.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=['pdf', 'quantidade', 'descricao', 'valor_unitario', 'valor_total'])
    writer.writeheader()
    for item in todos_itens:
        writer.writerow({
            'pdf': item['pdf'],
            'quantidade': item['quantidade'],
            'descricao': item['descricao'],
            'valor_unitario': round(item['valor_unitario'], 2),
            'valor_total': round(item['valor_total'], 2)
        })

# Salva resumo por PDF
resumo_detalhado = {}
for pdf, stats in sorted(resumo_por_pdf.items()):
    resumo_detalhado[pdf] = {
        'total_aparelhos': stats['total_aparelhos'],
        'total_linhas': stats['total_linhas'],
        'total_valor': round(stats['total_valor'], 2)
    }

with open('celulares_por_pdf_com_valores_V5_FINAL.json', 'w', encoding='utf-8') as f:
    json.dump(resumo_detalhado, f, ensure_ascii=False, indent=2)

# Mostra resumo final
print(f"\n{'='*80}")
print("RESUMO FINAL (VERSÃO 5 - FINAL ABSOLUTA)")
print(f"{'='*80}")

total_pdfs = len(resumo_por_pdf)
total_aparelhos = sum(item['quantidade'] for item in todos_itens)
total_linhas = len(todos_itens)
total_valor = sum(item['valor_total'] for item in todos_itens)

print(f"Total de PDFs: {total_pdfs}")
print(f"Total de aparelhos: {total_aparelhos:,}")
print(f"Total de linhas: {total_linhas:,}")
print(f"Total valor: R$ {total_valor:,.2f}")

# Verificações específicas
print(f"\n{'='*80}")
print("VERIFICAÇÕES ESPECÍFICAS:")
print(f"{'='*80}")

verificacoes = {
    'ADM 0800100_0746_2025 de 30_09_2025.PDF': {'aparelhos': 2544, 'valor': 3050180.53},
    'ADM 0800100_0743_2025 de 30_09_2025.PDF': {'aparelhos': 912, 'valor': 1555781.16}
}

for pdf_name, esperado in verificacoes.items():
    if pdf_name in resumo_por_pdf:
        encontrado = resumo_por_pdf[pdf_name]
        dif_aparelhos = encontrado['total_aparelhos'] - esperado['aparelhos']
        dif_valor = encontrado['total_valor'] - esperado['valor']
        
        print(f"\n📄 {pdf_name}:")
        print(f"   Esperado:   {esperado['aparelhos']} aparelhos | R$ {esperado['valor']:,.2f}")
        print(f"   Encontrado: {encontrado['total_aparelhos']} aparelhos | R$ {encontrado['total_valor']:,.2f}")
        
        sinal_ap = "✅" if dif_aparelhos == 0 else "⚠️"
        sinal_vl = "✅" if abs(dif_valor) < 1 else "⚠️"
        
        print(f"   Diferença:  {sinal_ap} {dif_aparelhos:+} aparelhos | {sinal_vl} R$ {dif_valor:+,.2f}")

print(f"\n{'='*80}")
print("✅ Arquivos gerados:")
print("   - celulares_com_valores_V5_FINAL.json (consolidado por modelo)")
print("   - celulares_com_valores_V5_FINAL.csv (detalhado por linha)")
print("   - celulares_por_pdf_com_valores_V5_FINAL.json (estatísticas por PDF)")
print(f"{'='*80}")
