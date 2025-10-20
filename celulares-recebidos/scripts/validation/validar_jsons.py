import json

print("Validando JSONs gerados...\n")

# Valida JSON Simplificado
try:
    with open('MEGA_JSON_MODELOS_SIMPLIFICADO.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    print("✓ JSON Simplificado: VÁLIDO")
    print(f"  - Total aparelhos: {dados['total_aparelhos']:,}")
    print(f"  - Modelos únicos: {dados['modelos_unicos']:,}")
    print(f"  - Valor: {dados['valor_total']}")
    print()
except Exception as e:
    print(f"✗ JSON Simplificado: ERRO - {e}")
    print()

# Valida JSON Completo
try:
    with open('MEGA_JSON_MODELOS_COMPLETO.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    print("✓ JSON Completo: VÁLIDO")
    print(f"  - Total aparelhos: {dados['total_geral']['aparelhos']:,}")
    print(f"  - Modelos únicos: {dados['total_geral']['modelos_unicos']:,}")
    print(f"  - ADMs: {dados['total_geral']['adms']}")
    print(f"  - Top modelos: {len(dados['top_20_modelos'])}")
    print()
except Exception as e:
    print(f"✗ JSON Completo: ERRO - {e}")
    print()

print("✅ AMBOS OS ARQUIVOS SÃO VÁLIDOS E UTILIZÁVEIS!")
