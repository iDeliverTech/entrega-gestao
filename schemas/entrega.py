from pydantic import BaseModel
from typing import List
from models.entrega import Entrega


class EntregaSchema(BaseModel):
    """ Define como uma entrega deve ser representado
    """
    numero_entrega: int = 123
    valor: float = 78.90
    forma_pagamento: str = "Pix"
    cep: str = "99999999"


class EntregaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no numero da entrega.
    """
    numero_entrega: int = 1505


class EntregaStatusSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a atualização do status da entrega, que será
        feita apenas com base no campo booleano e o numero da entrega.
    """
    numero_entrega: int = 1505
    entrega_realizada: bool = False


class EntregaViewSchema(BaseModel):
    """ Define como uma entrega será retornado: entrega.
    """
    id: int = 1
    numero_entrega: int = 123
    valor: float = 78.90
    frete: float = 15.30
    logradouro: str = "Avenida Azevedo"
    forma_pagamento: str = "Pix"
    entrega_realizada: bool = False


class ListagemEntregasSchema(BaseModel):
    """ Define como uma listagem de entregas será retornada.
    """
    entregas: List[EntregaViewSchema]


class EntregaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    numero_entrega: str


def apresenta_entregas(entregas: List[Entrega]):
    """ Retorna uma representação de entregas seguindo o schema definido em
        EntregaViewSchema.
    """
    result = []
    for entrega in entregas:
        result.append({
            "numero_entrega": entrega.numero_entrega,
            "valor": entrega.valor,
            "frete": entrega.frete,
            "logradouro": entrega.logradouro,
            "forma_pagamento": entrega.forma_pagamento,
            "entrega_realizada": entrega.entrega_realizada
        })

    return {"entregas": result}


def apresenta_entrega(entrega: Entrega):
    """ Retorna uma representação de uma entrega seguindo o schema definido em
        EntregaViewSchema.
    """
    return {
        "id": entrega.id,
        "numero_entrega": entrega.numero_entrega,
        "valor": entrega.valor,
        "frete": entrega.frete,
        "logradouro": entrega.logradouro,
        "forma_pagamento": entrega.forma_pagamento,
        "entrega_realizada": entrega.entrega_realizada
    }
