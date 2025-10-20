import re
import json

# Ler arquivo teste.json
with open('teste.json', 'r', encoding='utf-8') as f:
    linhas = f.readlines()

# Padrão para extrair: quantidade un descrição///valor
pattern = re.compile(r'^(\d+,\d+)\s+un\s+(.+?)///R\$\s*([\d.]+,\d{2})')

# Lista para armazenar os objetos JSON
celulares = []

for linha in linhas:
    linha = linha.strip()
    match = pattern.match(linha)
    
    if match:
        unidade_str = match.group(1)
        modelo = match.group(2).strip()
        valor_str = match.group(3)
        
        # Converter unidade para número
        unidade = float(unidade_str.replace(',', '.'))
        
        # Criar objeto
        celular = {
            "unidade": unidade,
            "modelo": modelo,
            "valor": f"R$ {valor_str}"
        }
        
        celulares.append(celular)

# Salvar como JSON estruturado
with open('celulares_estruturado.json', 'w', encoding='utf-8') as f:
    json.dump(celulares, f, ensure_ascii=False, indent=2)

print("="*80)
print("CONVERSÃO PARA JSON ESTRUTURADO")
print("="*80)
print(f"\nTotal de itens convertidos: {len(celulares):,}".replace(',', '.'))

print(f"\nPrimeiros 3 itens:")
print("-" * 80)
for i, item in enumerate(celulares[:3], 1):
    print(f"\n{i}. {json.dumps(item, ensure_ascii=False, indent=2)}")

print(f"\nÚltimos 3 itens:")
print("-" * 80)
for i, item in enumerate(celulares[-3:], len(celulares)-2):
    print(f"\n{i}. {json.dumps(item, ensure_ascii=False, indent=2)}")

print(f"\n{'='*80}")
print("✓ Arquivo 'celulares_estruturado.json' criado com sucesso!")
print("="*80)
print("\nEstrutura de cada objeto:")
print("""{
  "unidade": número,
  "modelo": "descrição completa",
  "valor": "R$ valor"
}""")
