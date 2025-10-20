import PyPDF2
import re

# Extrair texto do PDF 0745 novamente
pdf_path = "ADM 0800100_0745_2025 de 30_09_2025.PDF"

with open(pdf_path, 'rb') as file:
    reader = PyPDF2.PdfReader(file)
    texto_completo = []
    for page in reader.pages:
        texto_completo.append(page.extract_text())

texto = '\n'.join(texto_completo)

# Salvar como teste.json (restaurar original)
with open('teste_original_backup.json', 'w', encoding='utf-8') as f:
    f.write(texto)

print("✓ Backup do PDF extraído salvo como 'teste_original_backup.json'")
print("\nAgora vou reformatar com o script atualizado...")

# Processar com o script atualizado
linhas = texto.split('\n')

# Padrão para identificar linhas de itens
pattern_item = re.compile(
    r'^(\d+,\d+)\s+un\s+(SMARTPHONE.*?)(?://|$|\s*$)',
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
        
        # Buscar valor e descrição completa nas próximas linhas
        valor = None
        linhas_descricao = [linha]
        
        # Primeiro verificar se valor está na mesma linha
        match_valor = pattern_valor.search(linha)
        if match_valor:
            valor = match_valor.group(0)
        else:
            # Buscar nas próximas linhas e acumular descrição
            for j in range(i + 1, min(i + 5, len(linhas))):
                linha_busca = linhas[j].strip()
                
                # Parar em Subtotal, Total do ADM ou linha vazia significativa
                if 'Subtotal:' in linha_busca or 'Total do ADM:' in linha_busca or linha_busca.startswith('Quantidade Un.'):
                    break
                
                # Se encontrou valor, pegar e parar
                match_valor = pattern_valor.search(linha_busca)
                if match_valor:
                    valor = match_valor.group(0)
                    # Adicionar parte antes do valor
                    texto_antes_valor = linha_busca[:match_valor.start()].strip()
                    if texto_antes_valor:
                        linhas_descricao.append(texto_antes_valor)
                    break
                elif linha_busca:
                    # Linha de continuação da descrição
                    linhas_descricao.append(linha_busca)
        
        # Se encontrou valor, formatar linha
        if valor:
            # Juntar todas as linhas de descrição
            descricao_completa = ' '.join(linhas_descricao)
            
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

print(f"\n{'='*80}")
print("CONVERSÃO CONCLUÍDA")
print("="*80)
print(f"\nTotal de linhas formatadas: {len(linhas_formatadas):,}".replace(',', '.'))
print(f"\nÚltimas 10 linhas do novo formato:")
print("-" * 80)
for i, linha in enumerate(linhas_formatadas[-10:], len(linhas_formatadas) - 9):
    print(f"{i}. {linha[:100]}...")  # Mostrar primeiros 100 chars

print(f"\n✓ Arquivo 'teste.json' foi reformatado")
print(f"  Formato: quantidade un descrição//IMEI-processo///R$ valor")
