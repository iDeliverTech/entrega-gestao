from enum import Enum


class Region(Enum):
    SP = 'SP'
    RJ = 'RJ'
    MG = 'MG'
    ES = 'ES'
    MT = 'MT'
    MS = 'MS'
    GO = 'GO'
    DF = 'DF'
    AL = 'AL'
    BA = 'BA'
    CE = 'CE'
    MA = 'MA'
    PB = 'PB'
    PE = 'PE'
    PI = 'PI'
    RN = 'RN'
    SE = 'SE'
    PR = 'PR'
    SC = 'SC'
    RS = 'RS'
    AC = 'AC'
    AM = 'AM'
    AP = 'AP'
    PA = 'PA'
    RO = 'RO'
    RR = 'RR'
    TO = 'TO'


# Constantes para as taxas de frete das regiões
SUDESTE = 7.85
CENTRO_OESTE = 12.50
NORDESTE = 15.98
SUL = 17.30
NORTE = 20.83


# Dicionário com as taxas de frete
frete_map = {
    Region.SP: SUDESTE,
    Region.RJ: SUDESTE,
    Region.MG: SUDESTE,
    Region.ES: SUDESTE,
    Region.MT: CENTRO_OESTE,
    Region.MS: CENTRO_OESTE,
    Region.GO: CENTRO_OESTE,
    Region.DF: CENTRO_OESTE,
    Region.AL: NORDESTE,
    Region.BA: NORDESTE,
    Region.CE: NORDESTE,
    Region.MA: NORDESTE,
    Region.PB: NORDESTE,
    Region.PE: NORDESTE,
    Region.PI: NORDESTE,
    Region.RN: NORDESTE,
    Region.SE: NORDESTE,
    Region.PR: SUL,
    Region.SC: SUL,
    Region.RS: SUL,
    Region.AC: NORTE,
    Region.AM: NORTE,
    Region.AP: NORTE,
    Region.PA: NORTE,
    Region.RO: NORTE,
    Region.RR: NORTE,
    Region.TO: NORTE
}


# Função para validar o CEP
def validate_cep(cep):
    # Remove caracteres não numéricos do CEP
    cep_value = ''.join(filter(str.isdigit, cep))

    # CEP deve ter 8 caracteres
    if len(cep_value) < 8 or len(cep_value) > 8:
        raise ValueError("CEP deve conter entre 8 e 9 caracteres.")


# Função para obter a taxa de frete com base na UF (Unidade Federativa)
def get_frete(uf):
    region = Region(uf)  # Converte a UF em uma enumeração Region
    return frete_map.get(region, 0.0)  # Retorna a taxa de frete correspondente
