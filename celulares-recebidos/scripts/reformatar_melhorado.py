import re

# Ler arquivo original
with open('teste_original.json', 'r', encoding='utf-8') as f:
    original = f.read()

linhas = original.split('\n')

# Padrão para identificar início de item SMARTPHONE
pattern_item = re.compile(r'^(\d+,\d+)\s+un\s+SMARTPHONE', re.IGNORECASE)

# Padrão para valores em reais
pattern_valor = re.compile(r'R\$\s*([\d.]+,\d{2})')

# Lista para armazenar linhas formatadas
linhas_formatadas = []

i = 0
while i < len(linhas):
    linha_atual = linhas[i].strip()
    
    # Verificar se é início de um item SMARTPHONE
    match = pattern_item.match(linha_atual)
    if match:
        qtd = match.group(1)
        
        # Acumular todas as linhas até encontrar o valor
        partes_descricao = [linha_atual]
        valor = None
        j = i
        
        # Verificar se já tem valor na mesma linha
        match_valor = pattern_valor.search(linha_atual)
        if match_valor:
            valor = match_valor.group(0)
            # Remover valor da descrição
            texto_sem_valor = linha_atual[:match_valor.start()].strip()
            partes_descricao = [texto_sem_valor]
        else:
            # Continuar buscando nas próximas linhas
            j = i + 1
            while j < len(linhas) and j < i + 10:  # Buscar até 10 linhas à frente
                linha_seguinte = linhas[j].strip()
                
                # Parar se encontrar outro item, Subtotal, Total do ADM, ou cabeçalho
                if (pattern_item.match(linha_seguinte) or 
                    'Subtotal:' in linha_seguinte or 
                    'Total do ADM:' in linha_seguinte or
                    linha_seguinte.startswith('Quantidade Un.') or
                    linha_seguinte.startswith('Recinto:') or
                    'Documento de' in linha_seguinte):
                    break
                
                # Verificar se tem valor
                match_valor = pattern_valor.search(linha_seguinte)
                if match_valor:
                    valor = match_valor.group(0)
                    # Pegar texto antes do valor
                    texto_antes = linha_seguinte[:match_valor.start()].strip()
                    if texto_antes:
                        partes_descricao.append(texto_antes)
                    break
                elif linha_seguinte:  # Linha não vazia
                    # Adicionar como continuação da descrição
                    partes_descricao.append(linha_seguinte)
                
                j += 1
        
        # Se encontrou valor, formatar a linha
        if valor:
            # Juntar todas as partes da descrição
            descricao_completa = ' '.join(partes_descricao)
            
            # Remover a quantidade e "un" do início
            descricao_sem_qtd = re.sub(r'^\d+,\d+\s+un\s+', '', descricao_completa)
            
            # Remover espaços múltiplos
            descricao_limpa = ' '.join(descricao_sem_qtd.split())
            
            # Remover espaço antes de //
            descricao_limpa = descricao_limpa.replace(' //', '//')
            
            # Garantir que termina com /// antes do valor
            if not descricao_limpa.endswith('///'):
                # Se já tem //, adicionar mais /
                if descricao_limpa.endswith('//'):
                    descricao_limpa += '/'
                elif descricao_limpa.endswith('/'):
                    descricao_limpa += '//'
                else:
                    descricao_limpa += '///'
            
            # Formatar linha final
            linha_formatada = f"{qtd} un {descricao_limpa}{valor}"
            linhas_formatadas.append(linha_formatada)
    
    i += 1

# Salvar arquivo formatado
with open('teste.json', 'w', encoding='utf-8') as f:
    f.write('\n'.join(linhas_formatadas))

print("="*80)
print("CONVERSÃO MELHORADA CONCLUÍDA")
print("="*80)
print(f"\nOriginal: {len([l for l in linhas if pattern_item.match(l.strip())]):,} itens SMARTPHONE".replace(',', '.'))
print(f"Convertido: {len(linhas_formatadas):,} linhas formatadas".replace(',', '.'))

print(f"\nPrimeiras 5 linhas:")
print("-" * 80)
for i, linha in enumerate(linhas_formatadas[:5], 1):
    print(f"{i}. {linha}")

print(f"\nÚltimas 5 linhas:")
print("-" * 80)
for i, linha in enumerate(linhas_formatadas[-5:], len(linhas_formatadas)-4):
    print(f"{i}. {linha}")

print(f"\n✓ Arquivo 'teste.json' reformatado com captura completa das descrições!")
