from pydantic import BaseModel
from typing import List
from models.entrega import Entrega

class EntregaSchema(BaseModel):
    """ Define como um novo livro deve ser representado
    """
    numero_entrega: int = 123
    valor: float = 78.90
    frete: float = 15.30
    forma_pagamento: str = "Pix"
    status_entrega: str = "Em processamento"

class EntregaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no numero da entrega.
    """
    numero_entrega: int = 1505

class ListagemEntregasSchema(BaseModel):
    """ Define como uma listagem de entregas será retornada.
    """
    entregas:List[EntregaSchema]

class EntregaViewSchema(BaseModel):
    """ Define como uma entrega será retornado: entrega.
    """
    id: int = 1
    numero_entrega: int = 123
    valor: float = 78.90
    frete: float = 15.30
    forma_pagamento: str = "Pix"
    status_entrega: str = "Entregue"

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
            "forma_pagamento": entrega.forma_pagamento,
            "status_entrega": entrega.status_entrega
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
        "forma_pagamento": entrega.forma_pagamento,
        "status_entrega": entrega.status_entrega
    }