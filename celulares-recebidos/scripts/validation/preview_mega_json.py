import json

# Abre arquivo simplificado para preview
with open('MEGA_JSON_MODELOS_SIMPLIFICADO.json', 'r', encoding='utf-8') as f:
    dados = json.load(f)

print('=' * 90)
print('PREVIEW - MEGA JSON SIMPLIFICADO')
print('=' * 90)
print()
print(f"Total de Aparelhos: {dados['total_aparelhos']:,}")
print(f"Modelos Únicos: {dados['modelos_unicos']:,}")
print(f"Valor Total: {dados['valor_total']}")
print()

print('=' * 90)
print('TOP 10 MODELOS NO JSON')
print('=' * 90)
print()

modelos_list = list(dados['modelos'].items())
for i, (modelo, info) in enumerate(modelos_list[:10], 1):
    modelo_display = modelo[:65] if len(modelo) > 65 else modelo
    print(f"{i:2}. {modelo_display:65} | {info['quantidade_total']:6,} un")
    # Mostra ADMs onde este modelo aparece
    adms = ', '.join(sorted(info['adms'].keys()))
    print(f"    ADMs: {adms}")
    print()

print('=' * 90)
print('ESTRUTURA DO JSON SIMPLIFICADO')
print('=' * 90)
print()
print("Cada modelo tem a seguinte estrutura:")
print("""
{
  "modelo_name": {
    "quantidade_total": 1185,
    "adms": {
      "744": 500,
      "745": 685
    }
  }
}
""")

# Abre arquivo completo para show
print('=' * 90)
print('PREVIEW - MEGA JSON COMPLETO')
print('=' * 90)
print()

with open('MEGA_JSON_MODELOS_COMPLETO.json', 'r', encoding='utf-8') as f:
    dados_completo = json.load(f)

print(f"Chaves principais: {', '.join(dados_completo.keys())}")
print()
print(f"ADMs inclusos: {', '.join(sorted(dados_completo['adms'].keys()))}")
print()

print("Estrutura do JSON completo:")
print(f"- total_geral: totalizações gerais")
print(f"- adms: dicionário com cada ADM")
print(f"  - 733: 13 aparelhos em 2 modelos")
print(f"  - 734: 6.879 aparelhos em 412 modelos")
print(f"  - ... (todos os 15 ADMs)")
print(f"- top_20_modelos: ranking dos 20 mais comuns")
print()

print('=' * 90)
print('TAMANHO DOS ARQUIVOS')
print('=' * 90)
print()

import os

completo_size = os.path.getsize('MEGA_JSON_MODELOS_COMPLETO.json')
simplificado_size = os.path.getsize('MEGA_JSON_MODELOS_SIMPLIFICADO.json')

print(f"MEGA_JSON_MODELOS_COMPLETO.json: {completo_size:,} bytes ({completo_size/1024:.1f} KB)")
print(f"MEGA_JSON_MODELOS_SIMPLIFICADO.json: {simplificado_size:,} bytes ({simplificado_size/1024:.1f} KB)")
print()

print('✅ ARQUIVOS PRONTOS PARA USO!')
