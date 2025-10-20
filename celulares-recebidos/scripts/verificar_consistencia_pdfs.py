import json

print("=" * 80)
print("VERIFICAÇÃO: SOMA DOS PDFs vs TOTAL GERAL")
print("=" * 80)
print()

# 1. Carregar celulares_contabilizados.json
with open('celulares_contabilizados.json', 'r', encoding='utf-8') as f:
    dados_geral = json.load(f)

total_geral = dados_geral['total_aparelhos']
total_modelos_geral = dados_geral['total_modelos']

print("📊 TOTAL GERAL (celulares_contabilizados.json):")
print(f"   Total de aparelhos: {total_geral:,}")
print(f"   Total de modelos únicos: {total_modelos_geral:,}")
print()

# 2. Carregar celulares_por_pdf.json
with open('celulares_por_pdf.json', 'r', encoding='utf-8') as f:
    dados_por_pdf = json.load(f)

print("📊 RESUMO GERAL DO JSON POR PDF:")
print(f"   Total de aparelhos (resumo_geral): {dados_por_pdf['resumo_geral']['total_aparelhos_todos_pdfs']:,}")
print(f"   Total de modelos únicos (resumo_geral): {dados_por_pdf['resumo_geral']['total_descricoes_unicas_todos_pdfs']:,}")
print()

# 3. Somar manualmente todos os PDFs
print("🧮 SOMANDO MANUALMENTE CADA PDF:")
print("-" * 80)

soma_aparelhos = 0
soma_linhas = 0
contador_pdfs = 0

for pdf_nome, pdf_dados in dados_por_pdf['pdfs'].items():
    pdf_simples = pdf_nome.replace('ADM 0800100_', '').replace('_2025 de 30_09_2025.PDF', '').replace('_2025 de 30092025.PDF', '')
    aparelhos = pdf_dados['total_aparelhos']
    linhas = pdf_dados['total_linhas']
    
    soma_aparelhos += aparelhos
    soma_linhas += linhas
    contador_pdfs += 1
    
    print(f"   {contador_pdfs:2d}. {pdf_simples:10s} = {aparelhos:6,} aparelhos ({linhas:5,} linhas)")

print("-" * 80)
print(f"   SOMA TOTAL: {soma_aparelhos:6,} aparelhos ({soma_linhas:5,} linhas)")
print()

# 4. Verificar consistência
print("=" * 80)
print("RESULTADO DA VERIFICAÇÃO")
print("=" * 80)
print()

print("Comparação dos totais de APARELHOS:")
print(f"   1. celulares_contabilizados.json............: {total_geral:,}")
print(f"   2. celulares_por_pdf.json (resumo_geral)....: {dados_por_pdf['resumo_geral']['total_aparelhos_todos_pdfs']:,}")
print(f"   3. Soma manual de todos os PDFs.............: {soma_aparelhos:,}")
print()

if total_geral == dados_por_pdf['resumo_geral']['total_aparelhos_todos_pdfs'] == soma_aparelhos:
    print("   ✅ PERFEITO! Todos os valores batem: {:,} aparelhos".format(total_geral))
    print()
    print("   ✓ celulares_contabilizados.json")
    print("   ✓ celulares_por_pdf.json (resumo_geral)")
    print("   ✓ Soma de todos os 15 PDFs individuais")
    print()
    print("   Os dados estão 100% consistentes! 🎯")
else:
    print("   ⚠️ ATENÇÃO: Divergência encontrada!")
    print()
    if total_geral != soma_aparelhos:
        diff = abs(total_geral - soma_aparelhos)
        print(f"   Diferença: {diff:,} aparelhos")
    
print()
print("=" * 80)
