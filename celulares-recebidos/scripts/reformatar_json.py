import re

# Ler o arquivo teste.json original
with open('teste.json', 'r', encoding='utf-8') as f:
    conteudo = f.read()

linhas = conteudo.split('\n')

# Padrão para identificar linhas de itens
pattern_item = re.compile(
    r'^(\d+,\d+)\s+un\s+(SMARTPHONE.*?)(?://|$)',
    re.IGNORECASE
)

# Padrão para valores em reais
pattern_valor = re.compile(r'R\$\s*([\d.]+,\d{2})')

# Lista para armazenar linhas formatadas
linhas_formatadas = []

i = 0
while i < len(linhas):
    linha = linhas[i].strip()
    
    # Verificar se é uma linha de item
    match = pattern_item.match(linha)
    if match:
        qtd = match.group(1)
        descricao_bruta = match.group(2).strip()
        
        # Buscar valor e descrição completa nas próximas linhas
        valor = None
        descricao_completa = linha  # Começar com a linha inteira
        
        # Primeiro verificar se valor está na mesma linha
        match_valor = pattern_valor.search(linha)
        if match_valor:
            valor = match_valor.group(0)  # Pega "R$ valor"
            # Remover o valor da descrição completa
            descricao_completa = linha[:match_valor.start()].strip()
        else:
            # Buscar nas próximas linhas e acumular descrição
            linhas_descricao = [linha]
            
            for j in range(i + 1, min(i + 5, len(linhas))):
                linha_busca = linhas[j].strip()
                
                # Ignorar Subtotal e Total do ADM
                if 'Subtotal:' in linha_busca or 'Total do ADM:' in linha_busca:
                    break
                
                # Se encontrou valor, pegar e parar
                match_valor = pattern_valor.search(linha_busca)
                if match_valor:
                    valor = match_valor.group(0)  # Pega "R$ valor"
                    # Adicionar parte antes do valor
                    texto_antes_valor = linha_busca[:match_valor.start()].strip()
                    if texto_antes_valor and not texto_antes_valor.startswith('PROC'):
                        linhas_descricao.append(texto_antes_valor)
                    break
                else:
                    # Linha de continuação da descrição (se não for cabeçalho)
                    if linha_busca and not linha_busca.startswith('PROC') and not linha_busca.startswith('Quantidade'):
                        linhas_descricao.append(linha_busca)
            
            # Juntar todas as linhas de descrição
            descricao_completa = ' '.join(linhas_descricao)
        
        # Se encontrou valor, formatar linha
        if valor:
            # Remover "un" e quantidade do início para reconstruir
            descricao_sem_qtd = re.sub(r'^\d+,\d+\s+un\s+', '', descricao_completa)
            
            # Remover espaços extras
            descricao_limpa = ' '.join(descricao_sem_qtd.split())
            
            # Remover espaço antes de // se existir
            descricao_limpa = descricao_limpa.replace(' //', '//')
            
            # Formatar: quantidade un descrição///valor
            linha_formatada = f"{qtd} un {descricao_limpa}///{valor}"
            linhas_formatadas.append(linha_formatada)
    
    i += 1

# Salvar arquivo formatado
with open('teste.json', 'w', encoding='utf-8') as f:
    f.write('\n'.join(linhas_formatadas))

print("="*80)
print("CONVERSÃO CONCLUÍDA")
print("="*80)
print(f"\nTotal de linhas formatadas: {len(linhas_formatadas):,}".replace(',', '.'))
print(f"\nPrimeiras 10 linhas do novo formato:")
print("-" * 80)
for i, linha in enumerate(linhas_formatadas[:10], 1):
    print(f"{i}. {linha}")

print(f"\n✓ Arquivo 'teste.json' foi reformatado no padrão de 'teste copy.json'")
print(f"  Formato: quantidade un descrição///R$ valor")
