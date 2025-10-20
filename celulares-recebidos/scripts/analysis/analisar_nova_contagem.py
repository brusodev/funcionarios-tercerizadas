import PyPDF2
import re

print("="*130)
print("🔍 COMPARAÇÃO: SUA CONTAGEM ATUALIZADA vs SCRIPT")
print("="*130 + "\n")

# Sua nova contagem (mais aprofundada)
sua_contagem_novo = {
    '0733': 13,
    '0734': 6879,
    '0740': 9,
    '0741': 19,
    '0742': 225,
    '0743': 911,      # Mudou de 912 para 911
    '0744': 3458,     # Mudou de 3457 para 3458 ✅
    '0735': 3816,     # Mudou de 3804 para 3816 ✅
    '0736': 3058,     # Mudou de 1873 para 3058 ⚠️ GRANDE MUDANÇA
    '0737': 616,
    '0738': 444,      # Mudou de 442 para 444 ✅
    '0739': 3708,
    '0745': 3390,
    '0746': 2544,
    '0747': 4124,
}

# Sua contagem anterior
sua_contagem_anterior = {
    '0733': 13,
    '0734': 6879,
    '0740': 9,
    '0741': 19,
    '0742': 225,
    '0743': 912,
    '0744': 3457,
    '0735': 3804,
    '0736': 1873,
    '0737': 616,
    '0738': 442,
    '0739': 3708,
    '0745': 3390,
    '0746': 2544,
    '0747': 4124,
}

# Contagem do script
contagens_script = {
    '0733': 13,
    '0734': 6879,
    '0740': 9,
    '0741': 19,
    '0742': 225,
    '0743': 909,
    '0744': 3458,
    '0735': 3816,
    '0736': 1873,
    '0737': 616,
    '0738': 444,
    '0739': 3708,
    '0745': 3390,
    '0746': 2544,
    '0747': 4124,
}

pdfs_lista = ['0733', '0734', '0740', '0741', '0742', '0743', '0744', '0735', '0736', '0737', '0738', '0739', '0745', '0746', '0747']

print(f"{'PDF':<6} {'Anterior':<12} {'Novo':<12} {'Script':<12} {'Mudança':<12} {'vs Script':<12} {'Status':<20}\n")

total_anterior = 0
total_novo = 0
total_script = 0

for pdf in pdfs_lista:
    anterior = sua_contagem_anterior[pdf]
    novo = sua_contagem_novo[pdf]
    script = contagens_script[pdf]
    
    total_anterior += anterior
    total_novo += novo
    total_script += script
    
    mudanca = novo - anterior
    vs_script = novo - script
    
    # Determinar status
    if novo == script:
        status = "✅ BATE COM SCRIPT"
    elif vs_script > 0:
        status = f"⚠️ +{vs_script}"
    else:
        status = f"⚠️ {vs_script}"
    
    # Destacar mudanças
    mudanca_str = f"{mudanca:+d}"
    if mudanca != 0:
        if abs(mudanca) > 100:
            mudanca_str += " 🔴 GRANDE"
        else:
            mudanca_str += " 🟡"
    
    print(f"{pdf:<6} {anterior:<12,d} {novo:<12,d} {script:<12,d} {mudanca_str:<15} {vs_script:+d}           {status:<20}")

print(f"\n{'─'*130}")
print(f"{'TOTAL':<6} {total_anterior:<12,d} {total_novo:<12,d} {total_script:<12,d}")
print(f"{'─'*130}\n")

print(f"📊 RESUMO DAS MUDANÇAS:\n")
print(f"Sua contagem ANTERIOR: {total_anterior:,} aparelhos")
print(f"Sua contagem NOVA:     {total_novo:,} aparelhos (+{total_novo - total_anterior:,})")
print(f"Script:                {total_script:,} aparelhos")
print(f"\nDiferença (Novo vs Script): {total_novo - total_script:+,} aparelhos\n")

print("="*130)
print("⚠️  MUDANÇAS SIGNIFICATIVAS ENCONTRADAS:\n")

for pdf in pdfs_lista:
    anterior = sua_contagem_anterior[pdf]
    novo = sua_contagem_novo[pdf]
    script = contagens_script[pdf]
    mudanca = novo - anterior
    
    if mudanca != 0:
        print(f"PDF {pdf}:")
        print(f"  Anterior: {anterior:,} → Novo: {novo:,} (Mudança: {mudanca:+,})")
        print(f"  Script: {script:,} → Diferença agora: {novo - script:+,}")
        if abs(mudanca) > 100:
            print(f"  🔴 MUDANÇA MUITO GRANDE - VERIFICAR ESTE PDF COM ATENÇÃO!")
        print()

print("="*130 + "\n")
