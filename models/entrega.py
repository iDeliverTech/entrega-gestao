from sqlalchemy import Column, String, Integer, DateTime, Float
from datetime import datetime
from typing import Union

from models import Base

class Entrega(Base):
    __tablename__ = 'entrega'

    id = Column("pk_entrega", Integer, primary_key=True)
    numero_entrega = Column(Integer, unique=True)
    valor = Column(Float)
    frete = Column(Float)
    forma_pagamento = Column(String(100))
    status_entrega = Column(String(100))
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, numero_entrega:int, valor:float, frete:float, forma_pagamento:str, status_entrega:str, data_insercao:Union[DateTime, None] = None):
        """
        Cria uma Entrega

        Arguments:
            numero_entrega: numero da entrega.
            valor: valor da entrega
            frete: frete da entrega
            forma_pagamento: forma de pagamento
            status_entrega: status da entrega
            data_insercao: data de quando a entrega foi inserida à base
        """
        self.numero_entrega = numero_entrega
        self.valor = valor
        self.frete = frete
        self.forma_pagamento = forma_pagamento
        self.status_entrega = status_entrega

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao