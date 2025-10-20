"""
Template para Organização de Serviços Terceirizados
===================================================

Este template organiza as informações de diferentes áreas de atuação:
- Manutenção de Prédios
- Serviço de Copa
- Segurança e Controle de Acesso
- Transporte

Estrutura de dados baseada nas colunas: nome, tipo_manutencao, locais
"""

import pandas as pd
import json
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from pathlib import Path
import os

@dataclass
class Funcionario:
    """Representa um funcionário terceirizado"""
    numero: int
    nome: str
    tipo_servico: str
    locais: str
    
    def get_locais_lista(self) -> List[str]:
        """Retorna os locais como uma lista"""
        return [local.strip() for local in self.locais.split('/') if local.strip()]

@dataclass
class AreaAtuacao:
    """Representa uma área de atuação de serviços"""
    nome: str
    descricao: str
    funcionarios: List[Funcionario]
    tipos_servico: List[str]
    locais_atendidos: List[str]
    
    def get_total_funcionarios(self) -> int:
        """Retorna o total de funcionários na área"""
        return len(self.funcionarios)
    
    def get_funcionarios_por_local(self) -> Dict[str, List[Funcionario]]:
        """Agrupa funcionários por local de atuação"""
        por_local = {}
        for funcionario in self.funcionarios:
            locais = funcionario.get_locais_lista()
            for local in locais:
                if local not in por_local:
                    por_local[local] = []
                por_local[local].append(funcionario)
        return por_local

class TemplateServicos:
    """Template principal para organização de serviços terceirizados"""
    
    def __init__(self):
        self.areas: Dict[str, AreaAtuacao] = {}
        self.configurar_areas_base()
    
    def configurar_areas_base(self):
        """Configura as áreas de atuação base"""
        areas_config = {
            'manutencao_predios': {
                'nome': 'Manutenção de Prédios',
                'descricao': 'Serviços de manutenção predial corretiva e preventiva',
                'arquivo_dados': 'manutencao_predios.xlsx'
            },
            'servico_copa': {
                'nome': 'Serviço de Copa',
                'descricao': 'Serviços de copa e cozinha nos prédios',
                'arquivo_dados': 'servicos_copas.xlsx'
            },
            'seguranca_acesso': {
                'nome': 'Segurança e Controle de Acesso',
                'descricao': 'Serviços de segurança patrimonial e controle de acesso',
                'arquivo_dados': 'seguranca.xlsx'
            },
            'transporte': {
                'nome': 'Transporte',
                'descricao': 'Serviços de transporte e motoristas',
                'arquivo_dados': 'transporte.xlsx'
            }
        }
        
        for chave, config in areas_config.items():
            self.areas[chave] = AreaAtuacao(
                nome=config['nome'],
                descricao=config['descricao'],
                funcionarios=[],
                tipos_servico=[],
                locais_atendidos=[]
            )
    
    def carregar_dados_planilha(self, arquivo: str, area_chave: str):
        """Carrega dados de uma planilha Excel para uma área específica"""
        try:
            if not os.path.exists(arquivo):
                print(f"Arquivo {arquivo} não encontrado!")
                return False
            
            df = pd.read_excel(arquivo)
            
            # Mapear colunas (considerando variações nos nomes)
            col_mapping = {}
            for col in df.columns:
                col_lower = col.lower().strip()
                if 'nome' in col_lower:
                    col_mapping['nome'] = col
                elif 'tipo' in col_lower and ('manut' in col_lower or 'servico' in col_lower):
                    col_mapping['tipo_servico'] = col
                elif 'locais' in col_lower:
                    col_mapping['locais'] = col
                elif 'nº' in col_lower or 'numero' in col_lower:
                    col_mapping['numero'] = col
            
            print(f"Colunas encontradas: {list(df.columns)}")
            print(f"Mapeamento: {col_mapping}")
            
            funcionarios = []
            tipos_servico = set()
            locais_atendidos = set()
            
            for _, row in df.iterrows():
                funcionario = Funcionario(
                    numero=int(row[col_mapping.get('numero', df.columns[0])]),
                    nome=str(row[col_mapping['nome']]),
                    tipo_servico=str(row[col_mapping['tipo_servico']]),
                    locais=str(row[col_mapping['locais']])
                )
                
                funcionarios.append(funcionario)
                tipos_servico.add(funcionario.tipo_servico)
                locais_atendidos.update(funcionario.get_locais_lista())
            
            # Atualizar área
            area = self.areas[area_chave]
            area.funcionarios = funcionarios
            area.tipos_servico = list(tipos_servico)
            area.locais_atendidos = list(locais_atendidos)
            
            print(f"✅ Carregados {len(funcionarios)} funcionários para {area.nome}")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao carregar {arquivo}: {e}")
            return False
    
    def carregar_todos_dados(self):
        """Carrega dados de todas as planilhas disponíveis"""
        mapeamento_arquivos = {
            'manutencao_predios.xlsx': 'manutencao_predios',
            'servicos_copas.xlsx': 'servico_copa',
            'seguranca.xlsx': 'seguranca_acesso',
            'transporte.xlsx': 'transporte'
        }
        
        for arquivo, area_chave in mapeamento_arquivos.items():
            if os.path.exists(arquivo):
                print(f"\n📁 Carregando {arquivo}...")
                self.carregar_dados_planilha(arquivo, area_chave)
            else:
                print(f"⚠️  Arquivo {arquivo} não encontrado")
    
    def gerar_relatorio_completo(self) -> Dict[str, Any]:
        """Gera relatório completo de todas as áreas"""
        relatorio = {
            'resumo_geral': {
                'total_areas': len(self.areas),
                'total_funcionarios': sum(area.get_total_funcionarios() for area in self.areas.values()),
                'areas_com_dados': sum(1 for area in self.areas.values() if area.funcionarios)
            },
            'areas': {}
        }
        
        for chave, area in self.areas.items():
            relatorio['areas'][chave] = {
                'nome': area.nome,
                'descricao': area.descricao,
                'total_funcionarios': area.get_total_funcionarios(),
                'tipos_servico': area.tipos_servico,
                'locais_atendidos': area.locais_atendidos,
                'funcionarios_por_local': {
                    local: len(funcionarios) 
                    for local, funcionarios in area.get_funcionarios_por_local().items()
                }
            }
        
        return relatorio
    
    def exibir_relatorio(self):
        """Exibe relatório formatado no console"""
        relatorio = self.gerar_relatorio_completo()
        
        print("\n" + "="*80)
        print("🏢 RELATÓRIO DE SERVIÇOS TERCEIRIZADOS")
        print("="*80)
        
        print(f"\n📊 RESUMO GERAL:")
        print(f"   • Total de áreas: {relatorio['resumo_geral']['total_areas']}")
        print(f"   • Total de funcionários: {relatorio['resumo_geral']['total_funcionarios']}")
        print(f"   • Áreas com dados: {relatorio['resumo_geral']['areas_com_dados']}")
        
        for chave, area_info in relatorio['areas'].items():
            print(f"\n🔹 {area_info['nome'].upper()}")
            print(f"   📝 {area_info['descricao']}")
            print(f"   👥 Funcionários: {area_info['total_funcionarios']}")
            
            if area_info['tipos_servico']:
                print(f"   🔧 Tipos de serviço:")
                for tipo in area_info['tipos_servico']:
                    print(f"      • {tipo}")
            
            if area_info['locais_atendidos']:
                print(f"   📍 Locais atendidos:")
                for local in area_info['locais_atendidos']:
                    count = area_info['funcionarios_por_local'].get(local, 0)
                    print(f"      • {local} ({count} funcionários)")
        
        print("\n" + "="*80)
    
    def get_todos_locais_unicos(self) -> List[str]:
        """Retorna lista de todos os locais únicos de todas as áreas"""
        todos_locais = set()
        
        for area in self.areas.values():
            if area.funcionarios:  # Só incluir áreas com dados
                for funcionario in area.funcionarios:
                    locais_lista = funcionario.get_locais_lista()
                    todos_locais.update(locais_lista)
        
        # Ordenar os locais para apresentação consistente
        return sorted(list(todos_locais))
    
    def get_funcionarios_por_local_global(self) -> Dict[str, List[tuple]]:
        """Agrupa todos os funcionários por local, independente da área"""
        por_local = {}
        
        for area_chave, area in self.areas.items():
            if area.funcionarios:  # Só processar áreas com dados
                for funcionario in area.funcionarios:
                    locais_lista = funcionario.get_locais_lista()
                    for local in locais_lista:
                        if local not in por_local:
                            por_local[local] = []
                        # Incluir informação da área junto com o funcionário
                        por_local[local].append((funcionario, area.nome))
        
        return por_local
    
    def salvar_relatorio_json(self, arquivo: str = "relatorio_servicos.json"):
        """Salva relatório em arquivo JSON"""
        relatorio = self.gerar_relatorio_completo()
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(relatorio, f, ensure_ascii=False, indent=2)
        print(f"📄 Relatório salvo em: {arquivo}")
    
    def criar_template_nova_area(self, nome_area: str, arquivo_excel: str):
        """Cria template de planilha Excel para nova área"""
        dados_template = {
            'nº': [1, 2, 3],
            'nome': ['FUNCIONÁRIO EXEMPLO 1', 'FUNCIONÁRIO EXEMPLO 2', 'FUNCIONÁRIO EXEMPLO 3'],
            'tipo_manutencao': [f'Serviço de {nome_area.lower()}'] * 3,
            'locais': ['Sede', 'Sede/Filial A', 'Filial B']
        }
        
        df = pd.DataFrame(dados_template)
        df.to_excel(arquivo_excel, index=False)
        print(f"📋 Template criado: {arquivo_excel}")

def main():
    """Função principal para demonstrar o uso do template"""
    print("🚀 Iniciando Template de Serviços Terceirizados...")
    
    # Criar instância do template
    template = TemplateServicos()
    
    # Carregar dados das planilhas existentes
    template.carregar_todos_dados()
    
    # Exibir relatório
    template.exibir_relatorio()
    
    # Salvar relatório em JSON
    template.salvar_relatorio_json()
    
    # Criar templates para áreas sem dados
    print("\n📋 Criando templates para novas áreas...")
    template.criar_template_nova_area("Segurança e Controle de Acesso", "template_seguranca_acesso.xlsx")
    template.criar_template_nova_area("Transporte", "template_transporte.xlsx")

if __name__ == "__main__":
    main()