import PyPDF2
import re
import json
import csv
from collections import defaultdict
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

def extrair_linhas_v6_inteligente(texto_pdf):
    """
    Versão 6 - CORREÇÃO CRÍTICA
    Detecta se o valor é TOTAL ou UNITÁRIO baseado no contexto
    """
    linhas = texto_pdf.split('\n')
    itens_encontrados = []
    
    # Padrão V5 para itens
    padrao_item = r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades|kg)\s+((?:SMARTPHONE|TELEFONE\s+CELULAR|APARELHO\s+CELULAR|APARELHO\s+DE\s+TELEFONE\s+CELULAR|IPHONE|(?<!TELEFONE\s)(?<!APARELHO\s)CELULAR|(?:REDMI|NOTE|POCO|POCOPHONE|MI)\s+\d+).*)'
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
            
            # Procura valor nas próximas 10 linhas
            valor_unitario = 0.0
            linha_valor = ""
            
            for j in range(i, min(i + 10, len(linhas))):
                linha_busca = linhas[j]
                
                # Ignora linhas com "Subtotal:" pois são somas de múltiplos itens
                if 'subtotal' in linha_busca.lower():
                    continue
                
                match_valor = re.search(r'R\$\s*([\d.,]+)', linha_busca)
                if match_valor:
                    valor_encontrado = normalizar_valor(match_valor.group(1))
                    
                    if valor_encontrado > 0:
                        # INTELIGÊNCIA: Se o valor é muito maior que esperado para um celular,
                        # provavelmente é o valor TOTAL, não unitário
                        
                        # Hipótese: valor total = valor do processo/lote
                        # Se quantidade > 1 e valor > 50.000, é muito provável que seja valor total
                        
                        if quantidade > 1 and valor_encontrado > 50000:
                            # Este é provavelmente o valor TOTAL
                            valor_unitario = valor_encontrado / quantidade
                            linha_valor = f"{linha_busca[:100]} (TOTAL dividido por {quantidade})"
                        elif quantidade > 1 and valor_encontrado > 20000:
                            # Pode ser total ou unitário muito caro
                            # Vamos verificar se faz sentido como unitário
                            valor_unit_candidato = valor_encontrado / quantidade
                            
                            # Se dividir der um valor razoável (500-15000), provavelmente é total
                            if 500 <= valor_unit_candidato <= 15000:
                                valor_unitario = valor_unit_candidato
                                linha_valor = f"{linha_busca[:100]} (TOTAL dividido)"
                            else:
                                # Senão, usa como unitário
                                valor_unitario = valor_encontrado
                                linha_valor = linha_busca[:100]
                        else:
                            # Valor parece razoável como unitário
                            valor_unitario = valor_encontrado
                            linha_valor = linha_busca[:100]
                        
                        break
            
            valor_total = valor_unitario * quantidade
            
            itens_encontrados.append({
                'quantidade': quantidade,
                'descricao': descricao,
                'valor_unitario': valor_unitario,
                'valor_total': valor_total,
                'linha_original': linha,
                'linha_valor': linha_valor
            })
    
    return itens_encontrados

print("="*80)
print("PROCESSAMENTO V6 - CORREÇÃO INTELIGENTE DE VALORES")
print("="*80)
print("✅ Detecta automaticamente se valor é TOTAL ou UNITÁRIO")
print("✅ Corrige multiplicação indevida de valores totais")
print("="*80)

# Testa primeiro com o PDF 0735
print(f"\n{'='*80}")
print("TESTE COM PDF 0735")
print(f"{'='*80}")

pdf_path = "ADM 0800100_0735_2025 de 30_09_2025.PDF"
texto = extrair_texto_pdf(pdf_path)
itens = extrair_linhas_v6_inteligente(texto)

total_aparelhos = sum(item['quantidade'] for item in itens)
total_valor = sum(item['valor_total'] for item in itens)

print(f"\nRESULTADO:")
print(f"   Aparelhos: {total_aparelhos:,}")
print(f"   Valor total: R$ {total_valor:,.2f}")
print(f"\nESPERADO (segundo você):")
print(f"   Aparelhos: 3,804")
print(f"   Valor total: R$ 2.845.357,66")
print(f"\nDIFERENÇA:")
print(f"   Aparelhos: {total_aparelhos - 3804:+,}")
print(f"   Valor: R$ {total_valor - 2845357.66:+,.2f}")
print(f"   Percentual: {((total_valor / 2845357.66) - 1) * 100:+.1f}%")

# Mostra exemplos de correções
print(f"\n{'='*80}")
print("EXEMPLOS DE VALORES CORRIGIDOS:")
print(f"{'='*80}")

# Pega os 10 itens com maior quantidade
itens_ordenados = sorted(itens, key=lambda x: x['quantidade'], reverse=True)

for i, item in enumerate(itens_ordenados[:10]):
    print(f"\n{i+1}. Qtd: {item['quantidade']} | Valor unit: R$ {item['valor_unitario']:,.2f} | Total: R$ {item['valor_total']:,.2f}")
    print(f"   {item['descricao'][:80]}")
    if 'TOTAL dividido' in item['linha_valor']:
        print(f"   ✅ CORRIGIDO: {item['linha_valor'][:100]}")

print(f"\n{'='*80}")
print("Processando TODOS os 15 PDFs com correção...")
print(f"{'='*80}")

# Processa todos os PDFs
pdf_files = sorted(Path('.').glob('ADM *.PDF'))
todos_itens = []
resumo_por_pdf = {}

for pdf_file in pdf_files:
    nome_pdf = pdf_file.name
    print(f"Processando: {nome_pdf}")
    
    try:
        texto = extrair_texto_pdf(str(pdf_file))
        itens = extrair_linhas_v6_inteligente(texto)
        
        total_aparelhos = sum(item['quantidade'] for item in itens)
        total_valor = sum(item['valor_total'] for item in itens)
        
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

# Salva arquivos
with open('celulares_com_valores_V6_CORRIGIDO.json', 'w', encoding='utf-8') as f:
    json.dump(dados_json, f, ensure_ascii=False, indent=2)

with open('celulares_com_valores_V6_CORRIGIDO.csv', 'w', newline='', encoding='utf-8-sig') as f:
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

resumo_detalhado = {}
for pdf, stats in sorted(resumo_por_pdf.items()):
    resumo_detalhado[pdf] = {
        'total_aparelhos': stats['total_aparelhos'],
        'total_linhas': stats['total_linhas'],
        'total_valor': round(stats['total_valor'], 2)
    }

with open('celulares_por_pdf_com_valores_V6_CORRIGIDO.json', 'w', encoding='utf-8') as f:
    json.dump(resumo_detalhado, f, ensure_ascii=False, indent=2)

# Resumo final
print(f"\n{'='*80}")
print("RESUMO FINAL (VERSÃO 6 - CORRIGIDA)")
print(f"{'='*80}")

total_pdfs = len(resumo_por_pdf)
total_aparelhos = sum(item['quantidade'] for item in todos_itens)
total_linhas = len(todos_itens)
total_valor = sum(item['valor_total'] for item in todos_itens)

print(f"Total de PDFs: {total_pdfs}")
print(f"Total de aparelhos: {total_aparelhos:,}")
print(f"Total de linhas: {total_linhas:,}")
print(f"Total valor: R$ {total_valor:,.2f}")

# Verificação específica do PDF 0735
if 'ADM 0800100_0735_2025 de 30_09_2025.PDF' in resumo_por_pdf:
    pdf_0735 = resumo_por_pdf['ADM 0800100_0735_2025 de 30_09_2025.PDF']
    print(f"\n{'='*80}")
    print("VERIFICAÇÃO PDF 0735:")
    print(f"{'='*80}")
    print(f"   Esperado:   3.804 aparelhos | R$ 2.845.357,66")
    print(f"   Encontrado: {pdf_0735['total_aparelhos']:,} aparelhos | R$ {pdf_0735['total_valor']:,.2f}")
    dif_valor = pdf_0735['total_valor'] - 2845357.66
    print(f"   Diferença:  {pdf_0735['total_aparelhos'] - 3804:+,} aparelhos | R$ {dif_valor:+,.2f}")
    print(f"   Precisão:   {(1 - abs(dif_valor) / 2845357.66) * 100:.1f}%")

print(f"\n{'='*80}")
print("✅ Arquivos gerados:")
print("   - celulares_com_valores_V6_CORRIGIDO.json")
print("   - celulares_com_valores_V6_CORRIGIDO.csv")
print("   - celulares_por_pdf_com_valores_V6_CORRIGIDO.json")
print(f"{'='*80}")
