with open('teste.json', 'r', encoding='utf-8') as f:
    content = f.read()

# Substituir ////// por ///
content_corrigido = content.replace('//////', '///')

with open('teste.json', 'w', encoding='utf-8') as f:
    f.write(content_corrigido)

print("✓ Substituição concluída: ////// → ///")

# Mostrar última linha
linhas = content_corrigido.split('\n')
print(f"\nÚltima linha:")
print(linhas[-1])
