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

def normalizar_nome_celular(nome):
    """
    Normaliza o nome do celular removendo prefixos comuns e informações extras.
    Mantém apenas: MARCA + MODELO + CAPACIDADE (GB/TB)
    Remove: CHINA, INDIA, ROM, números de série, etc.
    """
    # Remove prefixos comuns
    nome = re.sub(r'^(?:smartphone|celular|aparelho)\s+', '', nome, flags=re.IGNORECASE)
    
    # Converte para maiúsculas
    nome = nome.upper()
    
    # Remove informações extras
    remover = [
        r'\s+CHINA.*$',
        r'\s+INDIA.*$',
        r'\s+VIDE\s+EM\s+DESCRI[CÇ][AÃ]O.*$',
        r'\s+NR\s+DE\s+SERIE.*$',
        r'\s+N[RºÚ]\s+DE\s+S[EÉ]RIE.*$',
        r'\s+IMEI.*$',
        r'\s+SEM\s+CAIXA.*$',
        r'\s+SEM\s+ACESS[OÓ]RIOS.*$',
        r'\s+COM\s+CABO.*$',
        r'\s+EMBALAGEM.*$',
        r'\s+S\/N.*$',
        r'\s+SN\s*$',
        r'\s+NS\s*$',
        r'\s+GRAFITE.*$',
        r'\s+GRAY.*$',
        r'\s+BLACK.*$',
        r'\s+WHITE.*$',
        r'\s+BLUE.*$',
        r'\s+GREEN.*$',
        r'\s+RED.*$',
        r'\s+SILVER.*$',
        r'\s+GOLD.*$',
        r'\s+ROSE.*$',
        r'\s+5G\s*$',  # Remove 5G do final se estiver sozinho
    ]
    
    for padrao in remover:
        nome = re.sub(padrao, '', nome, flags=re.IGNORECASE)
    
    # Normaliza espaços e vírgulas
    nome = re.sub(r'\s*,\s*', ' ', nome)  # Remove vírgulas
    nome = re.sub(r'\s+', ' ', nome)  # Normaliza espaços múltiplos
    nome = nome.strip()
    
    # Remove espaços entre letra e número no modelo (C 65 -> C65, A 3 -> A3)
    nome = re.sub(r'([A-Z])\s+(\d)', r'\1\2', nome)
    nome = re.sub(r'([A-Z])\s+(\d)', r'\1\2', nome)  # Aplica duas vezes para casos consecutivos
    
    # Adiciona espaço antes de GB/TB se não tiver (S128GB -> S 128GB)
    nome = re.sub(r'([A-Z])(\d+GB)', r'\1 \2', nome)
    nome = re.sub(r'([A-Z])(\d+TB)', r'\1 \2', nome)
    
    # Remove /// no final
    nome = re.sub(r'\/+$', '', nome).strip()
    
    # Normaliza capacidade: "64 GB" -> "64GB"
    nome = re.sub(r'(\d+)\s+GB', r'\1GB', nome)
    nome = re.sub(r'(\d+)\s+TB', r'\1TB', nome)
    
    # Normaliza RAM: remove se estiver duplicado ou em posição estranha
    # "128GB 8GB RAM" -> "8GB RAM 128GB"
    match_ram = re.search(r'(\d+GB)\s+(\d+GB)\s+RAM', nome)
    if match_ram:
        storage = match_ram.group(1)
        ram = match_ram.group(2)
        nome = re.sub(r'\d+GB\s+\d+GB\s+RAM', f'{ram} RAM {storage}', nome)
    
    return nome.strip()

def identificar_celulares_com_quantidade(texto):
    """
    Identifica modelos de celulares no texto COM suas quantidades.
    Formatos aceitos:
    - "4,00 un SMARTPHONE XIAOMI REDMI NOTE 14 256GB CHINA/// R$ 3.486,72"
    - "7,00 un SMARTPHONE XIAOMI REDMI A1 32GB CHINA VIDE EM DESCRICAO"
    - "2,00 un SMARTPHONE XIAOMI REDMI A1, 32 GB ( 43115;62ZN07722"
    - "1,00 un SMARTPHONE REALME NOTE 50 3GB RAM 64GB ROM"
    """
    celulares = []
    
    # Padrão que captura até encontrar: R$, (, ///, SN:, NS:, IMEI: ou quebra de linha seguida de palavra maiúscula
    # Captura tudo incluindo GB/TB e RAM/ROM
    
    padrao_geral = r'(\d+(?:,\d+)?)\s+(?:un|unidade|unidades)\s+((?:Smartphone\s+)?(?:iPhone|Samsung|Motorola|Xiaomi|LG|Nokia|Asus|OnePlus|Huawei|Realme|OPPO|Vivo|Sony|Positivo|TCL|Multilaser|Poco)[^(\nR]+?(?:\d+\s*(?:GB|TB)(?:\s+RAM)?(?:\s+\d+\s*(?:GB|TB))?(?:\s+ROM)?)?[^(\nR]*?)(?=\s*(?:R\$|\(|///|SN:|NS:|NR\s+DE|IMEI:|CB:|$|\n\d|\n[A-Z][a-z]))'
    
    matches = re.findall(padrao_geral, texto, re.IGNORECASE | re.MULTILINE)
    
    for match in matches:
        quantidade_str = match[0].replace(',', '.')
        try:
            quantidade = float(quantidade_str)
            modelo = match[1].strip()
            # Remove vírgulas e pontos extras no final
            modelo = re.sub(r'[,\s]+$', '', modelo)
            celulares.append((int(quantidade), modelo))
        except ValueError:
            continue
    
    return celulares

def processar_pdfs(diretorio):
    """Processa todos os PDFs no diretório e conta os aparelhos."""
    contador = defaultdict(int)
    pdfs_processados = 0
    
    # Lista todos os arquivos PDF (sem duplicatas)
    pdfs_encontrados = set()
    for pattern in ["*.PDF", "*.pdf"]:
        for pdf in Path(diretorio).glob(pattern):
            # Normaliza o caminho para evitar duplicatas
            pdfs_encontrados.add(pdf.resolve())
    
    pdfs = sorted(list(pdfs_encontrados))
    
    print(f"Encontrados {len(pdfs)} arquivos PDF únicos para processar...\n")
    
    for pdf_path in pdfs:
        print(f"Processando: {pdf_path.name}")
        texto = extrair_texto_pdf(pdf_path)
        
        if texto:
            celulares = identificar_celulares_com_quantidade(texto)
            
            # Normalizar nomes e somar quantidades
            for quantidade, celular in celulares:
                celular_normalizado = normalizar_nome_celular(celular)
                if celular_normalizado:  # Só adiciona se não for vazio
                    contador[celular_normalizado] += quantidade
            
            pdfs_processados += 1
    
    print(f"\n{pdfs_processados} PDFs processados com sucesso!\n")
    
    return dict(contador)

def salvar_json(dados, arquivo_saida):
    """Salva os dados em formato JSON."""
    resultado = {
        "total_modelos": len(dados),
        "total_aparelhos": sum(dados.values()),
        "modelos": dados,
        "modelos_ordenados": dict(sorted(dados.items(), key=lambda x: x[1], reverse=True))
    }
    
    with open(arquivo_saida, 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    return resultado

if __name__ == "__main__":
    # Diretório atual
    diretorio_atual = os.path.dirname(os.path.abspath(__file__))
    
    print("=" * 60)
    print("EXTRATOR DE APARELHOS CELULARES DOS PDFs")
    print("=" * 60)
    print()
    
    # Processar PDFs
    aparelhos = processar_pdfs(diretorio_atual)
    
    if not aparelhos:
        print("⚠️  ATENÇÃO: Nenhum aparelho celular foi identificado nos PDFs.")
        print("Isso pode significar que:")
        print("1. Os PDFs não contêm informações de celulares")
        print("2. Os padrões de busca precisam ser ajustados")
        print("\nPor favor, abra um dos PDFs e me informe como os aparelhos")
        print("estão descritos no documento para ajustar o script.")
    else:
        # Salvar resultado em JSON
        arquivo_saida = os.path.join(diretorio_atual, "celulares_contabilizados.json")
        resultado = salvar_json(aparelhos, arquivo_saida)
        
        print("=" * 60)
        print("RESULTADO")
        print("=" * 60)
        print(f"Total de modelos diferentes: {resultado['total_modelos']}")
        print(f"Total de aparelhos: {resultado['total_aparelhos']}")
        print()
        print("Top 10 modelos mais frequentes:")
        print("-" * 60)
        
        for i, (modelo, qtd) in enumerate(list(resultado['modelos_ordenados'].items())[:10], 1):
            print(f"{i}. {modelo}: {qtd} unidade(s)")
        
        print()
        print(f"✅ Arquivo JSON salvo em: {arquivo_saida}")
        print()
