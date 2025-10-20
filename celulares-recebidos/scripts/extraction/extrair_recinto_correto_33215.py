import os
import re
from collections import defaultdict
from PyPDF2 import PdfReader

# Padrões de recinto
RECINTOS = {
    r'305\s*-\s*810300': 'Bauru',
    r'16\s*-\s*810900': 'Araraquara',
    r'2\s*-\s*DEPÓSITO SAPOL': 'São José do Rio Preto',
    r'1\s*-\s*AEROPORTOS BRASIL VIRACOPOS': 'Viracopos',
    r'309\s*-\s*817900': 'Ipiranga',
}

# Padrão para extrair quantidade e unidade
PATTERN_QUANTIDADE = r'(\d+[\.,]?\d*,\d+)\s+(un|kg)'

def extrair_recinto_linha(linha):
    """Extrai o recinto de uma linha de texto"""
    for pattern, recinto in RECINTOS.items():
        if re.search(pattern, linha, re.IGNORECASE):
            return recinto
    return None

def extrair_valor_linha(linha):
    """Extrai o valor de uma linha de texto"""
    match = re.search(r'R\$\s*([\d.]+,\d+)', linha)
    if match:
        valor_str = match.group(1)
        # Remove o ponto de milhar e substitui vírgula por ponto
        valor_float = float(valor_str.replace('.', '').replace(',', '.'))
        return valor_float
    return 0.0

def converter_quantidade(quantidade_str, unidade):
    """Converte quantidade para aparelhos"""
    # Remove separador de milhares se houver
    quantidade_str = quantidade_str.replace('.', '').replace(',', '.')
    quantidade = float(quantidade_str)
    
    if unidade.lower() == 'kg':
        # KG conversion: 0.49 kg = 1 device; 1 kg = 2 devices
        if quantidade == 0.49:
            return 1
        else:
            return round(quantidade / 0.49)
    else:  # 'un'
        return int(quantidade)

def processar_pdfs():
    """Processa todos os PDFs e extrai distribuição por recinto"""
    
    distribuicao = defaultdict(lambda: {'aparelhos': 0, 'valor': 0.0})
    recinto_atual = None
    total_aparelhos = 0
    total_valor = 0.0
    
    # Lista de PDFs em ordem
    pdfs = sorted([f for f in os.listdir('.') if f.startswith('ADM') and f.endswith('.PDF')])
    
    print(f"Processando {len(pdfs)} PDFs...\n")
    
    for pdf_file in pdfs:
        print(f"Processando: {pdf_file}")
        
        try:
            reader = PdfReader(pdf_file)
            texto_completo = ""
            
            for page in reader.pages:
                texto_completo += page.extract_text()
            
            linhas = texto_completo.split('\n')
            pdf_aparelhos = 0
            pdf_valor = 0.0
            
            for linha in linhas:
                linha = linha.strip()
                
                # Detecta mudança de recinto
                novo_recinto = extrair_recinto_linha(linha)
                if novo_recinto:
                    recinto_atual = novo_recinto
                    print(f"  -> Recinto: {recinto_atual}")
                
                # Procura por linhas com quantidade
                if recinto_atual:
                    matches = re.findall(PATTERN_QUANTIDADE, linha)
                    
                    if matches:
                        for quantidade_str, unidade in matches:
                            aparelhos = converter_quantidade(quantidade_str, unidade)
                            valor = extrair_valor_linha(linha)
                            
                            if aparelhos > 0:
                                distribuicao[recinto_atual]['aparelhos'] += aparelhos
                                distribuicao[recinto_atual]['valor'] += valor
                                pdf_aparelhos += aparelhos
                                pdf_valor += valor
                                total_aparelhos += aparelhos
                                total_valor += valor
            
            print(f"  Total PDF: {pdf_aparelhos} aparelhos | R$ {pdf_valor:,.2f}\n")
        
        except Exception as e:
            print(f"  ERRO: {e}\n")
    
    return distribuicao, total_aparelhos, total_valor

def main():
    print("=" * 70)
    print("EXTRAÇÃO DE APARELHOS POR RECINTO (VERSÃO CORRIGIDA - 33.215)")
    print("=" * 70)
    print()
    
    distribuicao, total_aparelhos, total_valor = processar_pdfs()
    
    print("\n" + "=" * 70)
    print("DISTRIBUIÇÃO POR RECINTO")
    print("=" * 70)
    print()
    
    # Calcula percentuais
    with open('RELATORIO_POR_RECINTO_CORRIGIDO.csv', 'w', encoding='utf-8') as f:
        f.write("Recinto;Aparelhos;Percentual;Valor R$\n")
        
        for recinto in sorted(distribuicao.keys()):
            dados = distribuicao[recinto]
            aparelhos = dados['aparelhos']
            valor = dados['valor']
            percentual = (aparelhos / total_aparelhos * 100) if total_aparelhos > 0 else 0
            
            linha = f"{recinto};{aparelhos:,};{percentual:.2f}%;{valor:,.2f}"
            print(linha)
            f.write(linha.replace(',', '.').replace('.', ',') + "\n")
    
    print()
    print("-" * 70)
    print(f"Total de Aparelhos: {total_aparelhos:,}")
    print(f"Valor Total: R$ {total_valor:,.2f}")
    print("-" * 70)
    print()
    
    # Salva em JSON também
    import json
    
    resultado = {
        'total_aparelhos': total_aparelhos,
        'total_valor': total_valor,
        'distribuicao': {}
    }
    
    for recinto in distribuicao:
        resultado['distribuicao'][recinto] = {
            'aparelhos': distribuicao[recinto]['aparelhos'],
            'valor': distribuicao[recinto]['valor'],
            'percentual': (distribuicao[recinto]['aparelhos'] / total_aparelhos * 100) if total_aparelhos > 0 else 0
        }
    
    with open('RELATORIO_POR_RECINTO_CORRIGIDO.json', 'w', encoding='utf-8') as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)
    
    print("✓ Relatórios salvos:")
    print("  - RELATORIO_POR_RECINTO_CORRIGIDO.csv")
    print("  - RELATORIO_POR_RECINTO_CORRIGIDO.json")

if __name__ == '__main__':
    main()
