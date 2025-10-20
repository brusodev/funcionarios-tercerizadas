import os
import json
import re
from pathlib import Path
from collections import defaultdict

try:
    import PyPDF2
except ImportError:
    print("PyPDF2 não está instalado. Instalando...")
    os.system("pip install PyPDF2")
    import PyPDF2

def extrair_texto_pdf(caminho_pdf):
    """Extrai texto de um arquivo PDF."""
    texto = ""
    try:
        with open(caminho_pdf, 'rb') as arquivo:
            leitor = PyPDF2.PdfReader(arquivo)
            for pagina in leitor.pages:
                texto += pagina.extract_text() + "\n"
    except Exception as e:
        print(f"Erro ao ler {caminho_pdf}: {e}")
    return texto

def extrair_todas_linhas_com_quantidade(texto):
    """
    Extrai APENAS as linhas que começam com quantidade + un/unidade + SMARTPHONE ou TELEFONE CELULAR
    Retorna lista de tuplas: (quantidade, linha_completa)
    """
    linhas = []
    
    # Divide o texto em linhas
    for linha in texto.split('\n'):
        # Procura especificamente por: número + un + SMARTPHONE ou TELEFONE CELULAR
        # Padrão: quantidade + un/unidade + (SMARTPHONE ou TELEFONE CELULAR) + resto
        match = re.match(
            r'^(\d+(?:,\d+)?)\s+(?:un|unidade|unidades)\s+((?:SMARTPHONE|TELEFONE\s+CELULAR)\s+.+)',
            linha,
            re.IGNORECASE
        )
        
        if match:
            quantidade_str = match.group(1).replace(',', '.')
            conteudo = match.group(2).strip()
            try:
                quantidade = int(float(quantidade_str))
                linhas.append((quantidade, conteudo, linha))
            except ValueError:
                continue
    
    return linhas

def eh_smartphone(linha):
    """
    Verifica se a linha contém um smartphone.
    Como já filtramos por SMARTPHONE ou TELEFONE CELULAR no regex,
    essa função agora só valida se não é uma linha inválida.
    """
    # Já vem filtrado, então sempre retorna True
    # Mas podemos adicionar filtros extras se necessário
    return True

def normalizar_modelo(texto):
    """
    Normaliza o nome do modelo removendo informações extras.
    Mantém: MARCA + MODELO + CAPACIDADE principal
    Trata formatos:
    - "SMARTPHONE XIAOMI REDMI 13 128GB"
    - "TELEFONE CELULAR/MOTOROLA/moto wx395/"
    - "TELEFONE CELULAR SAMSUNG GT-19192///"
    """
    # Remove "SMARTPHONE" e "TELEFONE CELULAR" do início
    texto = re.sub(r'^SMARTPHONE\s+', '', texto, flags=re.IGNORECASE)
    texto = re.sub(r'^TELEFONE\s+CELULAR\s+', '', texto, flags=re.IGNORECASE)
    
    # Trata formato com barras: "MOTOROLA/moto wx395/" -> "MOTOROLA MOTO WX395"
    # Se tem barras, substitui por espaços e remove barras extras
    if '/' in texto:
        # Remove barras do final primeiro
        texto = re.sub(r'/+$', '', texto)
        # Substitui barras por espaços
        texto = texto.replace('/', ' ')
    
    # Converte para maiúsculas
    texto = texto.upper()
    
    # Lista de padrões a remover
    remover = [
        r'\s+CHINA.*$',
        r'\s+INDIA.*$',
        r'\s+VIDE\s+EM\s+DESCRI[CÇ][AÃ]O.*$',
        r'\s+NR\s+DE\s+SERIE.*$',
        r'\s+NR\s+DE\s+S[EÉ]RIE.*$',
        r'\s+N[RºÚ]\s+DE.*$',
        r'\s+IMEI.*$',
        r'\s+SN:.*$',
        r'\s+NS:.*$',
        r'\s+SEM\s+CAIXA.*$',
        r'\s+SEM\s+ACESS[OÓ]RIOS.*$',
        r'\s+COM\s+CABO.*$',
        r'\s+EMBALAGEM.*$',
        r'\s+CB:.*$',
        r'///.*$',
        r'\s+R\$.*$',
        r'\(.*$',  # Remove tudo após parênteses
    ]
    
    for padrao in remover:
        texto = re.sub(padrao, '', texto, flags=re.IGNORECASE)
    
    # Remove vírgulas
    texto = re.sub(r'\s*,\s*', ' ', texto)
    
    # Normaliza espaços
    texto = re.sub(r'\s+', ' ', texto)
    
    # Remove espaços entre letra e número (C 65 -> C65)
    texto = re.sub(r'([A-Z])\s+(\d)', r'\1\2', texto)
    texto = re.sub(r'([A-Z])\s+(\d)', r'\1\2', texto)
    
    # Adiciona espaço antes de GB/TB se grudado em letra (S128GB -> S 128GB)
    texto = re.sub(r'([A-Z])(\d+GB)', r'\1 \2', texto)
    texto = re.sub(r'([A-Z])(\d+TB)', r'\1 \2', texto)
    
    # Normaliza capacidade: "64 GB" -> "64GB"
    texto = re.sub(r'(\d+)\s+GB', r'\1GB', texto)
    texto = re.sub(r'(\d+)\s+TB', r'\1TB', texto)
    
    return texto.strip()

def extrair_descricao_completa(texto):
    """
    Extrai a descrição completa do aparelho até o valor R$ ou ///
    Mantém o texto original sem normalização.
    """
    # Remove apenas o valor R$ e o que vem depois, e ///
    texto = re.sub(r'\s*R\$.*$', '', texto)
    texto = re.sub(r'///.*$', '', texto)
    
    # Remove apenas espaços extras no início e fim
    texto = texto.strip()
    
    return texto

def processar_pdfs_linha_por_linha(diretorio):
    """Processa todos os PDFs linha por linha."""
    contador = defaultdict(int)
    todas_linhas = []
    pdfs_processados = 0
    total_aparelhos = 0
    
    # Lista todos os arquivos PDF únicos
    pdfs_encontrados = set()
    for pattern in ["*.PDF", "*.pdf"]:
        for pdf in Path(diretorio).glob(pattern):
            pdfs_encontrados.add(pdf.resolve())
    
    pdfs = sorted(list(pdfs_encontrados))
    
    print(f"Encontrados {len(pdfs)} arquivos PDF únicos para processar...\n")
    
    for pdf_path in pdfs:
        print(f"Processando: {pdf_path.name}")
        texto = extrair_texto_pdf(pdf_path)
        
        if texto:
            # Extrai todas as linhas com quantidade
            linhas = extrair_todas_linhas_com_quantidade(texto)
            
            smartphones_neste_pdf = 0
            
            for quantidade, conteudo, linha_completa in linhas:
                # Verifica se é smartphone
                if eh_smartphone(conteudo):
                    # Usa a descrição completa SEM normalização
                    descricao_completa = extrair_descricao_completa(conteudo)
                    
                    if descricao_completa:
                        contador[descricao_completa] += quantidade
                        total_aparelhos += quantidade
                        smartphones_neste_pdf += quantidade
                        todas_linhas.append({
                            'pdf': pdf_path.name,
                            'quantidade': quantidade,
                            'descricao_completa': descricao_completa,
                            'linha_original': linha_completa[:200]  # Aumentado para 200 chars
                        })
            
            print(f"  → {smartphones_neste_pdf} smartphones encontrados")
            pdfs_processados += 1
    
    print(f"\n{pdfs_processados} PDFs processados com sucesso!")
    print(f"Total de aparelhos contados: {total_aparelhos}")
    
    return dict(contador), todas_linhas, total_aparelhos

def salvar_json(dados, todas_linhas, total_aparelhos, arquivo_saida):
    """Salva os dados em formato JSON."""
    resultado = {
        "total_modelos": len(dados),
        "total_aparelhos": total_aparelhos,
        "modelos": dados,
        "modelos_ordenados": dict(sorted(dados.items(), key=lambda x: x[1], reverse=True)),
        "detalhamento_por_linha": todas_linhas[:100]  # Primeiras 100 linhas como exemplo
    }
    
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    return resultado

def salvar_csv_detalhado(todas_linhas, arquivo_csv):
    """Salva um CSV com todas as linhas detalhadas."""
    import csv
    
    with open(arquivo_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['PDF', 'Quantidade', 'Descrição Completa', 'Linha Original'])
        
        for linha in todas_linhas:
            writer.writerow([
                linha['pdf'],
                linha['quantidade'],
                linha['descricao_completa'],
                linha['linha_original']
            ])
    
    print(f"CSV detalhado salvo em: {arquivo_csv}")

if __name__ == "__main__":
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 70)
    print("VERIFICAÇÃO LINHA POR LINHA - CONTAGEM EXATA DE CELULARES")
    print("=" * 70)
    print()
    
    # Processar PDFs
    aparelhos, todas_linhas, total = processar_pdfs_linha_por_linha(diretorio_atual)
    
    # Salvar resultado em JSON
    arquivo_json = os.path.join(diretorio_atual, "celulares_contabilizados.json")
    resultado = salvar_json(aparelhos, todas_linhas, total, arquivo_json)
    
    # Salvar CSV detalhado
    arquivo_csv = os.path.join(diretorio_atual, "celulares_detalhado.csv")
    salvar_csv_detalhado(todas_linhas, arquivo_csv)
    
    print()
    print("=" * 70)
    print("RESULTADO FINAL")
    print("=" * 70)
    print(f"Total de PDFs processados: {len(set([l['pdf'] for l in todas_linhas]))}")
    print(f"Total de linhas com smartphones: {len(todas_linhas)}")
    print(f"Total de modelos diferentes: {resultado['total_modelos']}")
    print(f"Total de aparelhos: {resultado['total_aparelhos']}")
    print()
    print("Top 15 modelos mais frequentes:")
    print("-" * 70)
    
    for i, (modelo, qtd) in enumerate(list(resultado['modelos_ordenados'].items())[:15], 1):
        print(f"{i:2d}. {modelo:50s} {qtd:5d} unidades")
    
    print()
    print(f"✅ Arquivo JSON salvo em: {arquivo_json}")
    print(f"✅ Arquivo CSV detalhado salvo em: {arquivo_csv}")
    print()
    print("O arquivo CSV contém TODAS as linhas encontradas para verificação manual.")
