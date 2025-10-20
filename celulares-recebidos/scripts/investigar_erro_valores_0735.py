import PyPDF2
import re
from collections import defaultdict

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

print("="*100)
print("INVESTIGAÇÃO DO ERRO DE VALORES - PDF 0735")
print("="*100)

pdf_path = "ADM 0800100_0735_2025 de 30_09_2025.PDF"
texto = extrair_texto_pdf(pdf_path)
linhas = texto.split('\n')

print(f"\nTotal de linhas no PDF: {len(linhas):,}")

# Padrão V5
padrao_item = r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades|kg)\s+((?:SMARTPHONE|TELEFONE\s+CELULAR|APARELHO\s+CELULAR|IPHONE|(?<!TELEFONE\s)(?<!APARELHO\s)CELULAR|(?:REDMI|NOTE|POCO|POCOPHONE|MI)\s+\d+).*)'
padrao_codigo = r'^\d+\s*-\s*\d+'

itens_encontrados = []

print(f"\n{'='*100}")
print("EXTRAINDO ITENS E VALORES...")
print(f"{'='*100}")

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
        valores_encontrados = []
        for j in range(i, min(i + 10, len(linhas))):
            linha_busca = linhas[j]
            # Encontra TODOS os valores R$ na linha
            matches_valor = re.findall(r'R\$\s*([\d.,]+)', linha_busca)
            for match_val in matches_valor:
                valor = normalizar_valor(match_val)
                if valor > 0:
                    valores_encontrados.append({
                        'valor': valor,
                        'linha': linha_busca[:100],
                        'distancia': j - i
                    })
        
        # Pega o primeiro valor encontrado (como o script V5 faz)
        valor_usado = valores_encontrados[0]['valor'] if valores_encontrados else 0.0
        
        itens_encontrados.append({
            'qtd': quantidade,
            'desc': descricao[:80],
            'linha_item': linha[:120],
            'valor_unitario': valor_usado,
            'valor_total': valor_usado * quantidade,
            'todos_valores': valores_encontrados,
            'num_valores_encontrados': len(valores_encontrados)
        })

print(f"Itens encontrados: {len(itens_encontrados)}")

# Calcula total
total_aparelhos = sum(item['qtd'] for item in itens_encontrados)
total_valor = sum(item['valor_total'] for item in itens_encontrados)

print(f"\n{'='*100}")
print(f"RESULTADO DO SCRIPT:")
print(f"{'='*100}")
print(f"Total de aparelhos: {total_aparelhos:,}")
print(f"Total de valor: R$ {total_valor:,.2f}")

print(f"\n{'='*100}")
print(f"COMPARAÇÃO:")
print(f"{'='*100}")
print(f"Valor esperado (você informou):  R$ 2.845.357,66")
print(f"Valor encontrado pelo script:    R$ {total_valor:,.2f}")
print(f"Diferença:                        R$ {total_valor - 2845357.66:,.2f}")
print(f"Fator de erro:                    {total_valor / 2845357.66:.1f}x")

# Analisa problemas
print(f"\n{'='*100}")
print(f"ANÁLISE DE PROBLEMAS:")
print(f"{'='*100}")

# Verifica se há itens com múltiplos valores
itens_multiplos_valores = [item for item in itens_encontrados if item['num_valores_encontrados'] > 1]

print(f"\nItens com MÚLTIPLOS valores R$ encontrados: {len(itens_multiplos_valores)}")

if itens_multiplos_valores:
    print(f"\nPrimeiros 20 exemplos de itens com múltiplos valores:")
    for i, item in enumerate(itens_multiplos_valores[:20]):
        print(f"\n{i+1}. Qtd: {item['qtd']} | Valor usado: R$ {item['valor_unitario']:,.2f}")
        print(f"   Item: {item['linha_item']}")
        print(f"   Valores encontrados nas próximas linhas:")
        for v in item['todos_valores'][:5]:
            print(f"      - R$ {v['valor']:,.2f} (distância: {v['distancia']} linhas)")
            print(f"        {v['linha']}")

# Verifica valores muito altos
valores_altos = [item for item in itens_encontrados if item['valor_unitario'] > 100000]

print(f"\n{'='*100}")
print(f"VALORES UNITÁRIOS MUITO ALTOS (> R$ 100.000):")
print(f"{'='*100}")
print(f"Total de itens: {len(valores_altos)}")

if valores_altos:
    print(f"\nTodos os itens com valores > R$ 100.000:")
    for i, item in enumerate(valores_altos):
        print(f"\n{i+1}. Qtd: {item['qtd']} | Valor unitário: R$ {item['valor_unitario']:,.2f} | Total: R$ {item['valor_total']:,.2f}")
        print(f"   Item: {item['linha_item']}")
        if item['todos_valores']:
            print(f"   Valores encontrados:")
            for v in item['todos_valores'][:3]:
                print(f"      - R$ {v['valor']:,.2f} | {v['linha']}")

# Calcula sem os valores muito altos
total_sem_altos = sum(item['valor_total'] for item in itens_encontrados if item['valor_unitario'] <= 100000)
print(f"\n{'='*100}")
print(f"RECALCULANDO SEM VALORES ABSURDOS (> R$ 100.000):")
print(f"{'='*100}")
print(f"Total de valor (sem valores > 100k): R$ {total_sem_altos:,.2f}")
print(f"Diferença com o esperado: R$ {total_sem_altos - 2845357.66:,.2f}")

# Tenta diferentes limiares
for limite in [50000, 30000, 20000, 10000, 5000]:
    total_com_limite = sum(item['valor_total'] for item in itens_encontrados if item['valor_unitario'] <= limite)
    dif = abs(total_com_limite - 2845357.66)
    print(f"Com limite R$ {limite:>6,}: R$ {total_com_limite:>15,.2f} (dif: R$ {dif:>12,.2f})")
