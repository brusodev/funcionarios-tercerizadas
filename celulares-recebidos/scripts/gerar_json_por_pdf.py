import json
import csv
from collections import defaultdict

print("=" * 80)
print("GERANDO JSON COM CONTAGEM DETALHADA POR PDF")
print("=" * 80)
print()

# Estrutura para armazenar dados por PDF
dados_por_pdf = {}

# Ler o CSV detalhado
with open('celulares_detalhado.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    
    for row in reader:
        pdf = row['PDF']
        quantidade = int(row['Quantidade'])
        descricao = row['Descrição Completa']
        
        # Inicializa o PDF se ainda não existe
        if pdf not in dados_por_pdf:
            dados_por_pdf[pdf] = {
                'nome_arquivo': pdf,
                'total_aparelhos': 0,
                'total_linhas': 0,
                'total_descricoes_unicas': 0,
                'modelos': {},
                'linhas_detalhadas': []
            }
        
        # Atualiza totais
        dados_por_pdf[pdf]['total_aparelhos'] += quantidade
        dados_por_pdf[pdf]['total_linhas'] += 1
        
        # Conta por modelo/descrição
        if descricao in dados_por_pdf[pdf]['modelos']:
            dados_por_pdf[pdf]['modelos'][descricao] += quantidade
        else:
            dados_por_pdf[pdf]['modelos'][descricao] = quantidade
        
        # Adiciona linha detalhada
        dados_por_pdf[pdf]['linhas_detalhadas'].append({
            'quantidade': quantidade,
            'descricao': descricao
        })

# Atualiza contagem de descrições únicas
for pdf in dados_por_pdf:
    dados_por_pdf[pdf]['total_descricoes_unicas'] = len(dados_por_pdf[pdf]['modelos'])
    
    # Ordena modelos por quantidade (do maior para o menor)
    dados_por_pdf[pdf]['modelos_ordenados'] = dict(
        sorted(dados_por_pdf[pdf]['modelos'].items(), key=lambda x: x[1], reverse=True)
    )
    
    # Top 10 modelos deste PDF
    dados_por_pdf[pdf]['top_10_modelos'] = dict(
        list(dados_por_pdf[pdf]['modelos_ordenados'].items())[:10]
    )

# Criar JSON final
resultado_final = {
    'resumo_geral': {
        'total_pdfs': len(dados_por_pdf),
        'total_aparelhos_todos_pdfs': sum(p['total_aparelhos'] for p in dados_por_pdf.values()),
        'total_linhas_todos_pdfs': sum(p['total_linhas'] for p in dados_por_pdf.values()),
        'total_descricoes_unicas_todos_pdfs': len(set(
            desc for pdf in dados_por_pdf.values() for desc in pdf['modelos'].keys()
        ))
    },
    'pdfs': {}
}

# Adiciona cada PDF ordenado por total de aparelhos (do maior para o menor)
pdfs_ordenados = sorted(
    dados_por_pdf.items(),
    key=lambda x: x[1]['total_aparelhos'],
    reverse=True
)

for pdf_nome, pdf_dados in pdfs_ordenados:
    # Remove linhas_detalhadas para deixar o JSON menor (opcional)
    # Mantém apenas o essencial
    resultado_final['pdfs'][pdf_nome] = {
        'nome_arquivo': pdf_dados['nome_arquivo'],
        'total_aparelhos': pdf_dados['total_aparelhos'],
        'total_linhas': pdf_dados['total_linhas'],
        'total_descricoes_unicas': pdf_dados['total_descricoes_unicas'],
        'top_10_modelos': pdf_dados['top_10_modelos'],
        'todos_modelos': pdf_dados['modelos_ordenados']
    }

# Salvar JSON
arquivo_saida = 'celulares_por_pdf.json'
with open(arquivo_saida, 'w', encoding='utf-8') as f:
    json.dump(resultado_final, f, ensure_ascii=False, indent=2)

print(f"✅ Arquivo gerado: {arquivo_saida}")
print()

# Mostrar resumo
print("=" * 80)
print("RESUMO POR PDF (ordenado por total de aparelhos)")
print("=" * 80)
print()

for i, (pdf_nome, pdf_dados) in enumerate(pdfs_ordenados, 1):
    pdf_simples = pdf_nome.replace('ADM 0800100_', '').replace('_2025 de 30_09_2025.PDF', '').replace('_2025 de 30092025.PDF', '')
    print(f"{i:2d}. {pdf_simples:30s} | {pdf_dados['total_aparelhos']:6,} aparelhos | {pdf_dados['total_linhas']:5,} linhas | {pdf_dados['total_descricoes_unicas']:4,} modelos únicos")

print()
print("=" * 80)
print("RESUMO GERAL")
print("=" * 80)
print(f"Total de PDFs processados......: {resultado_final['resumo_geral']['total_pdfs']}")
print(f"Total de aparelhos.............: {resultado_final['resumo_geral']['total_aparelhos_todos_pdfs']:,}")
print(f"Total de linhas................: {resultado_final['resumo_geral']['total_linhas_todos_pdfs']:,}")
print(f"Total de descrições únicas.....: {resultado_final['resumo_geral']['total_descricoes_unicas_todos_pdfs']:,}")
print()
print(f"✅ JSON detalhado por PDF salvo em: {arquivo_saida}")
print()
