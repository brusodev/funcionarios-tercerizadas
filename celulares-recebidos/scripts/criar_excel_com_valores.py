import json
import pandas as pd
from pathlib import Path

def criar_excel_from_json():
    """Cria arquivo Excel a partir do JSON de celulares por PDF com valores"""
    
    # Carrega o JSON
    with open('celulares_por_pdf_com_valores.json', 'r', encoding='utf-8') as f:
        dados = json.load(f)
    
    # Cria o ExcelWriter
    with pd.ExcelWriter('celulares_por_pdf_com_valores.xlsx', engine='openpyxl') as writer:
        
        # ABA 1: Resumo Geral
        resumo_geral = dados['resumo_geral']
        df_resumo = pd.DataFrame([{
            'Total de PDFs': resumo_geral['total_pdfs'],
            'Total de Aparelhos': resumo_geral['total_aparelhos'],
            'Total de Linhas': resumo_geral['total_linhas'],
            'Valor Total (R$)': resumo_geral['total_valor'],
            'Descrições Únicas': resumo_geral['total_descricoes_unicas'],
            'Valor Médio por Aparelho (R$)': resumo_geral['valor_medio_por_aparelho']
        }])
        df_resumo.to_excel(writer, sheet_name='Resumo Geral', index=False)
        
        # ABA 2: Resumo por PDF
        resumos_pdf = []
        for nome_pdf, info in dados['pdfs'].items():
            resumos_pdf.append({
                'PDF': nome_pdf,
                'Total Aparelhos': info['total_aparelhos'],
                'Total Linhas': info['total_linhas'],
                'Descrições Únicas': info['total_descricoes_unicas'],
                'Valor Total (R$)': info['valor_total'],
                'Valor Médio/Aparelho (R$)': info['valor_medio_por_aparelho']
            })
        
        df_resumo_pdf = pd.DataFrame(resumos_pdf)
        df_resumo_pdf = df_resumo_pdf.sort_values('Valor Total (R$)', ascending=False)
        df_resumo_pdf.to_excel(writer, sheet_name='Resumo por PDF', index=False)
        
        # ABA 3: Todos os Modelos (Consolidado)
        todos_modelos = []
        for nome_pdf, info in dados['pdfs'].items():
            for modelo, detalhes in info['todos_modelos'].items():
                todos_modelos.append({
                    'PDF': nome_pdf,
                    'Modelo': modelo,
                    'Quantidade': detalhes['quantidade'],
                    'Valor Total (R$)': detalhes['valor_total'],
                    'Valor Médio Unitário (R$)': detalhes['valor_medio_unitario']
                })
        
        df_todos_modelos = pd.DataFrame(todos_modelos)
        df_todos_modelos = df_todos_modelos.sort_values('Valor Total (R$)', ascending=False)
        df_todos_modelos.to_excel(writer, sheet_name='Todos os Modelos', index=False)
        
        # ABA 4: Top 10 de Cada PDF
        top10_todos = []
        for nome_pdf, info in dados['pdfs'].items():
            for modelo, detalhes in info['top_10_modelos'].items():
                top10_todos.append({
                    'PDF': nome_pdf,
                    'Modelo': modelo,
                    'Quantidade': detalhes['quantidade'],
                    'Valor Total (R$)': detalhes['valor_total'],
                    'Valor Médio Unitário (R$)': detalhes['valor_medio_unitario']
                })
        
        df_top10 = pd.DataFrame(top10_todos)
        df_top10.to_excel(writer, sheet_name='Top 10 por PDF', index=False)
        
        # ABA 5: Ranking Geral por Quantidade
        # Agrupa modelos iguais de diferentes PDFs
        modelos_agrupados = {}
        for nome_pdf, info in dados['pdfs'].items():
            for modelo, detalhes in info['todos_modelos'].items():
                if modelo not in modelos_agrupados:
                    modelos_agrupados[modelo] = {
                        'quantidade': 0,
                        'valor_total': 0.0
                    }
                modelos_agrupados[modelo]['quantidade'] += detalhes['quantidade']
                modelos_agrupados[modelo]['valor_total'] += detalhes['valor_total']
        
        ranking_quantidade = []
        for modelo, dados_modelo in modelos_agrupados.items():
            valor_medio = dados_modelo['valor_total'] / dados_modelo['quantidade'] if dados_modelo['quantidade'] > 0 else 0
            ranking_quantidade.append({
                'Modelo': modelo,
                'Quantidade Total': dados_modelo['quantidade'],
                'Valor Total (R$)': dados_modelo['valor_total'],
                'Valor Médio Unitário (R$)': round(valor_medio, 2)
            })
        
        df_ranking_qtd = pd.DataFrame(ranking_quantidade)
        df_ranking_qtd = df_ranking_qtd.sort_values('Quantidade Total', ascending=False)
        df_ranking_qtd.to_excel(writer, sheet_name='Ranking por Quantidade', index=False)
        
        # ABA 6: Ranking Geral por Valor
        df_ranking_valor = df_ranking_qtd.sort_values('Valor Total (R$)', ascending=False)
        df_ranking_valor.to_excel(writer, sheet_name='Ranking por Valor', index=False)
        
        # ABA 7: Estatísticas por PDF (análise)
        estatisticas = []
        for nome_pdf, info in dados['pdfs'].items():
            # Calcula algumas estatísticas
            valores_unitarios = [d['valor_medio_unitario'] for d in info['todos_modelos'].values()]
            
            estatisticas.append({
                'PDF': nome_pdf,
                'Total Aparelhos': info['total_aparelhos'],
                'Valor Total (R$)': info['valor_total'],
                'Valor Médio/Aparelho (R$)': info['valor_medio_por_aparelho'],
                'Modelos Diferentes': info['total_descricoes_unicas'],
                'Menor Valor Unitário (R$)': min(valores_unitarios) if valores_unitarios else 0,
                'Maior Valor Unitário (R$)': max(valores_unitarios) if valores_unitarios else 0,
                '% do Valor Total': round((info['valor_total'] / resumo_geral['total_valor']) * 100, 2),
                '% dos Aparelhos': round((info['total_aparelhos'] / resumo_geral['total_aparelhos']) * 100, 2)
            })
        
        df_estatisticas = pd.DataFrame(estatisticas)
        df_estatisticas = df_estatisticas.sort_values('Valor Total (R$)', ascending=False)
        df_estatisticas.to_excel(writer, sheet_name='Estatísticas Detalhadas', index=False)
    
    print("="*70)
    print("✅ EXCEL CRIADO COM SUCESSO!")
    print("="*70)
    print(f"Arquivo: celulares_por_pdf_com_valores.xlsx")
    print()
    print("📊 Abas criadas:")
    print("   1. Resumo Geral - Totais consolidados")
    print("   2. Resumo por PDF - Estatísticas de cada PDF")
    print("   3. Todos os Modelos - Lista completa com PDF de origem")
    print("   4. Top 10 por PDF - Melhores modelos de cada PDF")
    print("   5. Ranking por Quantidade - Modelos mais numerosos")
    print("   6. Ranking por Valor - Modelos de maior valor")
    print("   7. Estatísticas Detalhadas - Análise comparativa dos PDFs")
    print()
    print(f"📈 Total de registros:")
    print(f"   - {len(df_resumo_pdf)} PDFs processados")
    print(f"   - {len(df_todos_modelos)} linhas de modelos")
    print(f"   - {len(df_ranking_qtd)} modelos únicos consolidados")
    print("="*70)

if __name__ == "__main__":
    criar_excel_from_json()
