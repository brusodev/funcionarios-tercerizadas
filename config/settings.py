# Configuração do Sistema de Funcionários Terceirizados

# Caminhos dos arquivos
DATA_DIR = "data"
SRC_DIR = "src"
SCRIPTS_DIR = "scripts"
BACKUP_DIR = "backup"

# Configurações da aplicação
APP_TITLE = "Sistema de Gerenciamento de Funcionários Terceirizados"
APP_VERSION = "1.0.0"
LAST_UPDATE = "16/12/2024"

# Configurações de processamento
EXCEL_FILES = [
    "Bombeiro Civil.xlsx",
    "manutencao_predios.xlsx",
    "Serviço de copa.xlsx",
    "Serviço de Limpeza nos prédios.xlsx",
    "Serviço de locação de veículos.xlsx",
    "Serviço de recepção.xlsx",
    "Serviço de transporte do Gabinete.xlsx",
    "Serviço de vigilância eletrônica.xlsx",
    "Serviço de vigilância patrimonial.xlsx",
    "Serviços de manutenção de ar-condicionado.xlsx"
]

# Mapeamento de serviços
SERVICE_MAPPING = {
    "Bombeiro Civil.xlsx": {
        "title": "Bombeiro Civil",
        "description": "Serviços de prevenção e combate a incêndios",
        "locations": "Sede/Arouche e Efape/EE.São Paulo /EE.Raul Brasil/EE. Zuleika De Barros/EE.Geografa Emiko Matsumoto/EE.Paulo Kobayashi/EE. Cidade Julia/URE. Ribeirão Preto/URE. Bauru"
    },
    "Serviço de copa.xlsx": {
        "title": "Serviços de Copa",
        "description": "Serviços de copa e cozinha",
        "locations": "Sede/Arouche"
    },
    "Serviço de Limpeza nos prédios.xlsx": {
        "title": "Serviços de Limpeza nos Prédios",
        "description": "Serviços de limpeza e conservação predial",
        "locations": "Sede/Arouche/ Efape/Casa Verde/Cape/Rio Branco/São Domingos/Armênia/Cajamar"
    },
    "Serviço de locação de veículos.xlsx": {
        "title": "Serviços de Locação de Veículos",
        "description": "Serviços de locação e gestão de frota de veículos",
        "locations": "Armênia/U.R.E-Leste 1, 2,3,4 e 5/U.R.E-Centro/U.R.E-SUL 1,2 e 3/SEDUC-CEE/U.R.E-ITAPECERICA DA SERRA/U.R.E-CENTRO OESTE/U.R.E-NORTE 1 e 2/U.R.E-Centro Sul/U.R.E-Efape/U.R.E-Conviva"
    },
    "Serviço de recepção.xlsx": {
        "title": "Serviços de Recepção",
        "description": "Serviços de recepção e atendimento ao público",
        "locations": "Sede/Arouche/ Efape/EE.São Paulo /EE.Raul Brasil/EE. Zuleika De Barros/EE.Geografa Emiko Matsumoto/EE.Paulo Kobayashi/EE. Cidade Julia/URE. Ribeirão Preto/URE. Bauru"
    },
    "Serviço de transporte do Gabinete.xlsx": {
        "title": "Serviços de Transporte do Gabinete",
        "description": "Serviços de transporte executivo e motoristas",
        "locations": "Sede/EE.São Paulo /EE.Raul Brasil/EE. Zuleika De Barros/EE.Geografa Emiko Matsumoto/EE.Paulo Kobayashi/EE. Cidade Julia/URE. Ribeirão Preto/URE. Bauru"
    },
    "Serviço de vigilância eletrônica.xlsx": {
        "title": "Serviços de Vigilância Eletrônica",
        "description": "Serviços de monitoramento eletrônico e CCTV",
        "locations": "Sede/Arouche/Efape/Armênica/Casa Verde/São Domingos/Tenente Pena/EE.São Paulo /EE.Raul Brasil/EE. Zuleika De Barros/EE.Geografa Emiko Matsumoto/EE.Paulo Kobayashi/EE. Cidade Julia/URE. Ribeirão Preto/URE. Bauru"
    },
    "Serviço de vigilância patrimonial.xlsx": {
        "title": "Serviços de Vigilância Patrimonial",
        "description": "Serviços de vigilância e segurança patrimonial",
        "locations": "Sede/Arouche/Armênia/Casa Verde/São Domingos/Tenente Pena/Rio Branco/Efape/Cape/EE.São Paulo /EE.Raul Brasil/EE. Zuleika De Barros/EE.Geografa Emiko Matsumoto/EE.Paulo Kobayashi/EE. Cidade Julia/URE. Ribeirão Preto/URE. Bauru"
    },
    "Serviços de manutenção de ar-condicionado.xlsx": {
        "title": "Serviços de Manutenção de Ar-Condicionado",
        "description": "Serviços de manutenção preventiva e corretiva de sistemas de climatização",
        "locations": "Sede/Arouche/ Efape e Armênia"
    },
    "manutencao_predios.xlsx": {
        "title": "Manutenção de Prédios",
        "description": "Serviços de manutenção predial corretiva e preventiva nos prédios",
        "locations": "Armênia/Arouche/Cape/Casa Verde/Efape/Rio Branco/Sede/São Domingos"
    }
}