import PyPDF2
import re
import json
from pathlib import Path

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
    
    DESCOBERTA CRÍTICA:
    - O PDF tem estrutura: linha com quantidade, próxima linha tem VALOR TOTAL
    - Exemplo: "10,00 un SMARTPHONE..." seguido de "PROC...///R$ 3.832,10"
    - O R$ 3.832,10 é o TOTAL para as 10 unidades, não o preço unitário
    - Portanto: valor unitário = R$ 3.832,10 ÷ 10 = R$ 383,21
    
    LÓGICA V7:
    1. Encontrar item com quantidade
    2. Buscar primeiro valor R$ nas próximas linhas
    3. Ignorar linhas com "Subtotal:"
    4. SEMPRE dividir o valor encontrado pela quantidade
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
    total_valor = 0
    
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
            
            total_valor += valor_total_item
    
    return {
        'total_aparelhos': sum(r['quantidade'] for r in resultados),
        'total_valor': round(total_valor, 2),
        'itens': resultados
    }


# Processar PDF 0735 para validação
print("="*80)
print("TESTE VERSÃO V7 - LÓGICA FINAL CORRIGIDA")
print("="*80)

pdf_0735 = Path("ADM 0800100_0735_2025 de 30_09_2025.PDF")
resultado = processar_pdf_v7(pdf_0735)

print(f"\nRESULTADO PDF 0735:")
print(f"   Aparelhos: {int(resultado['total_aparelhos']):,}".replace(',', '.'))
print(f"   Valor total: R$ {resultado['total_valor']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

print(f"\nESPERADO (segundo você):")
print(f"   Aparelhos: 3.804")
print(f"   Valor total: R$ 2.845.357,66")

diferenca_valor = resultado['total_valor'] - 2845357.66
percentual = (diferenca_valor / 2845357.66) * 100

print(f"\nDIFERENÇA:")
print(f"   Aparelhos: {int(resultado['total_aparelhos']) - 3804:+d}")
print(f"   Valor: R$ {diferenca_valor:+,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
print(f"   Percentual: {percentual:+.1f}%")

# Mostrar primeiros 10 itens como exemplo
print(f"\nPRIMEIROS 10 ITENS COM VALORES CORRIGIDOS:")
for i, item in enumerate(resultado['itens'][:10], 1):
    print(f"\n{i}. Qtd: {int(item['quantidade'])} | Valor unit: R$ {item['valor_unitario']:,.2f} | Total: R$ {item['valor_total']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    print(f"   {item['descricao'][:80]}")

# Verificar se há itens sem valor
sem_valor = [item for item in resultado['itens'] if item['valor_total'] == 0]
print(f"\n{'='*80}")
print(f"Itens SEM valor encontrado: {len(sem_valor)} de {len(resultado['itens'])}")
if sem_valor:
    print("\nPrimeiros 5 itens sem valor:")
    for item in sem_valor[:5]:
        print(f"  - {int(item['quantidade'])}× {item['descricao'][:60]}")
