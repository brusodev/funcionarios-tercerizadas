import PyPDF2
import re
from pathlib import Path

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

def procurar_linhas_sem_valor():
    """Procura linhas de celular que não têm valor associado nas próximas 5 linhas"""
    
    pdf_path = Path('ADM 0800100_0746_2025 de 30_09_2025.PDF')
    
    texto = extrair_texto_pdf(pdf_path)
    linhas = texto.split('\n')
    
    padrao_linha = re.compile(
        r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades)\s+((?:SMARTPHONE|TELEFONE\s+CELULAR|(?<!TELEFONE\s)CELULAR)\s+.+)', 
        re.IGNORECASE
    )
    padrao_valor = re.compile(r'R\$\s*([\d.,]+)')
    padrao_codigo = re.compile(r'^\d+\s*-\s*\d+')
    
    linhas_sem_valor = []
    linhas_com_valor_distante = []
    
    i = 0
    while i < len(linhas):
        linha_atual = linhas[i].strip()
        
        if padrao_codigo.match(linha_atual):
            i += 1
            continue
        
        match = padrao_linha.match(linha_atual)
        
        if match:
            quantidade_str = match.group(1)
            descricao = match.group(2).strip()
            quantidade = float(quantidade_str.replace(',', '.'))
            
            # Procura valor em diferentes distâncias
            valor_encontrado_5 = None
            valor_encontrado_10 = None
            posicao_valor = None
            
            for offset in range(15):  # Aumenta busca para 15 linhas
                if i + offset < len(linhas):
                    linha_busca = linhas[i + offset]
                    match_valor = padrao_valor.search(linha_busca)
                    
                    if match_valor:
                        if offset <= 5:
                            valor_encontrado_5 = match_valor.group(1)
                        valor_encontrado_10 = match_valor.group(1)
                        posicao_valor = offset
                        break
                    
                    if offset > 0 and padrao_linha.match(linhas[i + offset].strip()):
                        break
            
            # Linha sem valor nas primeiras 5 linhas
            if not valor_encontrado_5:
                info = {
                    'linha_num': i + 1,
                    'quantidade': quantidade,
                    'descricao': descricao[:80],
                    'valor_10_linhas': normalizar_valor(valor_encontrado_10) if valor_encontrado_10 else 0,
                    'posicao_valor': posicao_valor,
                    'linha': linha_atual[:120]
                }
                
                if valor_encontrado_10:
                    linhas_com_valor_distante.append(info)
                else:
                    linhas_sem_valor.append(info)
        
        i += 1
    
    print("="*80)
    print("ANÁLISE DE LINHAS COM PROBLEMAS DE VALOR")
    print("="*80)
    
    if linhas_com_valor_distante:
        print(f"\n🔍 LINHAS COM VALOR DISTANTE (entre 6 e 15 linhas):")
        print(f"   Total: {len(linhas_com_valor_distante)}")
        total_qtd = sum([l['quantidade'] for l in linhas_com_valor_distante])
        total_valor = sum([l['valor_10_linhas'] for l in linhas_com_valor_distante])
        print(f"   Total aparelhos: {int(total_qtd)}")
        print(f"   Total valor: R$ {total_valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
        print()
        
        for linha in linhas_com_valor_distante[:20]:
            print(f"   Linha {linha['linha_num']} (valor na linha +{linha['posicao_valor']}): Qtd={int(linha['quantidade'])}, Valor=R$ {linha['valor_10_linhas']:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))
            print(f"      {linha['linha']}")
            print()
    
    if linhas_sem_valor:
        print(f"\n❌ LINHAS SEM VALOR (até 15 linhas depois):")
        print(f"   Total: {len(linhas_sem_valor)}")
        total_qtd_sem = sum([l['quantidade'] for l in linhas_sem_valor])
        print(f"   Total aparelhos: {int(total_qtd_sem)}")
        print()
        
        for linha in linhas_sem_valor[:20]:
            print(f"   Linha {linha['linha_num']}: Qtd={int(linha['quantidade'])}")
            print(f"      {linha['linha']}")
            print()
    
    # Estatísticas finais
    print("="*80)
    print("RESUMO:")
    print(f"   Linhas com valor distante: {len(linhas_com_valor_distante)}")
    print(f"   Linhas sem valor: {len(linhas_sem_valor)}")
    
    if linhas_com_valor_distante:
        total_qtd_distante = sum([l['quantidade'] for l in linhas_com_valor_distante])
        total_valor_distante = sum([l['valor_10_linhas'] for l in linhas_com_valor_distante])
        print(f"\n   Se incluir valores distantes:")
        print(f"      + {int(total_qtd_distante)} aparelhos")
        print(f"      + R$ {total_valor_distante:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.'))

if __name__ == "__main__":
    procurar_linhas_sem_valor()
