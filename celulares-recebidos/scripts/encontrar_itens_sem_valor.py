import re

# Ler arquivo original
with open('teste_original.json', 'r', encoding='utf-8') as f:
    original = f.read()

# Ler arquivo convertido
with open('teste.json', 'r', encoding='utf-8') as f:
    convertido = f.read()

linhas_original = original.split('\n')
linhas_convertido = convertido.split('\n')

# Padrão para identificar início de item SMARTPHONE
pattern_item = re.compile(r'^(\d+,\d+)\s+un\s+SMARTPHONE', re.IGNORECASE)
pattern_valor = re.compile(r'R\$\s*([\d.]+,\d{2})')

# Encontrar todos os itens no original e verificar se têm valor
print("="*80)
print("ITENS SEM VALOR NO ORIGINAL")
print("="*80)

itens_sem_valor = []
itens_com_valor = []

i = 0
while i < len(linhas_original):
    linha = linhas_original[i].strip()
    
    if pattern_item.match(linha):
        # Buscar valor nas próximas 5 linhas
        tem_valor = False
        for j in range(i, min(i + 10, len(linhas_original))):
            if pattern_valor.search(linhas_original[j]):
                tem_valor = True
                break
            # Parar se encontrar outro item
            if j > i and pattern_item.match(linhas_original[j].strip()):
                break
        
        if tem_valor:
            itens_com_valor.append(linha)
        else:
            itens_sem_valor.append((i+1, linha))
    
    i += 1

print(f"\nItens COM valor: {len(itens_com_valor)}")
print(f"Itens SEM valor: {len(itens_sem_valor)}")
print(f"Total: {len(itens_com_valor) + len(itens_sem_valor)}")

if itens_sem_valor:
    print(f"\n{'='*80}")
    print("ITENS SEM VALOR ENCONTRADO:")
    print("="*80)
    for linha_num, item in itens_sem_valor:
        print(f"\nLinha {linha_num}: {item}")
        # Mostrar próximas 5 linhas
        for j in range(1, 6):
            if linha_num - 1 + j < len(linhas_original):
                print(f"  +{j}: {linhas_original[linha_num - 1 + j].strip()}")

# Comparar com convertido
print(f"\n{'='*80}")
print("RESUMO")
print("="*80)
print(f"Total de itens no original: {len(itens_com_valor) + len(itens_sem_valor)}")
print(f"Itens com valor (deveriam ser convertidos): {len(itens_com_valor)}")
print(f"Itens sem valor (não podem ser convertidos): {len(itens_sem_valor)}")
print(f"Linhas no arquivo convertido: {len(linhas_convertido)}")
print(f"\nDiferença: {len(itens_com_valor) - len(linhas_convertido)} itens ainda faltando")
