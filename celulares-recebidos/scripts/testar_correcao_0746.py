import PyPDF2
import re
import json
import csv
from pathlib import Path
from collections import defaultdict

def extrair_texto_pdf(caminho_pdf):
    """Extrai todo o texto de um PDF"""
    texto = ""
    try:
        with open(caminho_pdf, 'rb') as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)
            for pagina in leitor.pages:
                texto += pagina.extract_text() + "\n"
    except Exception as e:
        print(f"Erro ao ler {caminho_pdf}: {e}")
    return texto

def normalizar_valor(valor_str):
    """Converte string de valor brasileiro para float"""
    if not valor_str:
        return 0.0
    valor_str = valor_str.replace("R$", "").strip()
    valor_str = valor_str.replace(".", "").replace(",", ".")
    try:
        return float(valor_str)
    except:
        return 0.0

def extrair_linhas_com_valores_corrigido(texto, nome_pdf):
    """
    Extrai linhas com quantidade, descrição e valor - VERSÃO CORRIGIDA
    Agora aceita: SMARTPHONE, TELEFONE CELULAR, ou apenas CELULAR
    """
    linhas = texto.split('\n')
    resultados = []
    
    # Padrão CORRIGIDO: aceita SMARTPHONE, TELEFONE CELULAR ou CELULAR (sem TELEFONE antes)
    # Mas exclui linhas que parecem ser códigos/números de região
    padrao_linha = re.compile(
        r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades)\s+((?:SMARTPHONE|TELEFONE\s+CELULAR|(?<!TELEFONE\s)CELULAR)\s+.+)', 
        re.IGNORECASE
    )
    
    # Padrão para valores
    padrao_valor = re.compile(r'R\$\s*([\d.,]+)')
    
    # Padrão para detectar linhas que são códigos (ex: "309 - 817900")
    padrao_codigo = re.compile(r'^\d+\s*-\s*\d+')
    
    i = 0
    while i < len(linhas):
        linha_atual = linhas[i].strip()
        
        # Pula se for linha de código
        if padrao_codigo.match(linha_atual):
            i += 1
            continue
        
        match = padrao_linha.match(linha_atual)
        
        if match:
            quantidade_str = match.group(1)
            descricao = match.group(2).strip()
            
            # Converte quantidade (formato brasileiro com vírgula)
            quantidade = float(quantidade_str.replace(',', '.'))
            
            # Procura valor na linha atual e nas próximas 5 linhas
            valor_encontrado = None
            valor_numerico = 0.0
            linhas_busca = 6
            
            for offset in range(linhas_busca):
                if i + offset < len(linhas):
                    linha_busca = linhas[i + offset]
                    match_valor = padrao_valor.search(linha_busca)
                    
                    if match_valor:
                        valor_encontrado = match_valor.group(1)
                        valor_numerico = normalizar_valor(valor_encontrado)
                        break
                    
                    # Para se encontrar uma nova linha de item
                    if offset > 0 and padrao_linha.match(linhas[i + offset].strip()):
                        break
            
            resultados.append({
                'pdf': nome_pdf,
                'quantidade': quantidade,
                'descricao': descricao,
                'valor_texto': valor_encontrado if valor_encontrado else '',
                'valor_numerico': valor_numerico,
                'linha_original': linha_atual
            })
        
        i += 1
    
    return resultados

def testar_correcao_pdf_0746():
    """Testa a correção no PDF 0746"""
    
    pdf_path = Path('ADM 0800100_0746_2025 de 30_09_2025.PDF')
    
    print("="*80)
    print("TESTE DA CORREÇÃO - PDF 0746")
    print("="*80)
    
    texto = extrair_texto_pdf(pdf_path)
    linhas_extraidas = extrair_linhas_com_valores_corrigido(texto, pdf_path.name)
    
    total_aparelhos = sum([l['quantidade'] for l in linhas_extraidas])
    total_valor = sum([l['valor_numerico'] for l in linhas_extraidas])
    
    print(f"\n📊 RESULTADOS COM PADRÃO CORRIGIDO:")
    print(f"   Total de linhas: {len(linhas_extraidas)}")
    print(f"   Total de aparelhos: {int(total_aparelhos)}")
    print(f"   Total valor: R$ {total_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    print(f"\n🎯 COMPARAÇÃO:")
    print(f"   Esperado (usuário): 2544 aparelhos | R$ 3.050.180,53")
    print(f"   Script antigo: 2536 aparelhos | R$ 3.040.062,23")
    print(f"   Script CORRIGIDO: {int(total_aparelhos)} aparelhos | R$ {total_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    print(f"\n✅ DIFERENÇA (corrigido vs esperado):")
    print(f"   Aparelhos: {int(total_aparelhos - 2544)} (diferença de {abs(int(total_aparelhos - 2544))} unidades)")
    print(f"   Valor: R$ {(total_valor - 3050180.53):,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
    
    # Mostra as linhas que foram adicionadas (as que têm apenas "CELULAR")
    linhas_celular = [l for l in linhas_extraidas if 'CELULAR' in l['descricao'].upper() and 'SMARTPHONE' not in l['descricao'].upper() and 'TELEFONE CELULAR' not in l['descricao'].upper()]
    
    if linhas_celular:
        print(f"\n📝 LINHAS ADICIONADAS (apenas 'CELULAR'):")
        for linha in linhas_celular:
            print(f"   Qtd: {int(linha['quantidade'])}, Valor: R$ {linha['valor_numerico']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            print(f"   {linha['linha_original']}")
    
    # Salva resultado detalhado
    with open('teste_correcao_0746.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Quantidade', 'Descrição', 'Valor (texto)', 'Valor (numérico)', 'Linha Original'])
        for linha in linhas_extraidas:
            writer.writerow([
                linha['quantidade'],
                linha['descricao'],
                linha['valor_texto'],
                linha['valor_numerico'],
                linha['linha_original']
            ])
    
    print(f"\n📄 Resultado detalhado salvo em: teste_correcao_0746.csv")
    
    return total_aparelhos, total_valor

if __name__ == "__main__":
    testar_correcao_pdf_0746()
