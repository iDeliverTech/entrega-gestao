from sqlalchemy import Column, String, Integer, DateTime, Float, Boolean
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
    # Campo booleano para indicar se a entrega foi realizada
    entrega_realizada = Column(Boolean, default=False)
    data_insercao = Column(DateTime, default=datetime.now())

    def __init__(self, numero_entrega: int, valor: float, frete: float, forma_pagamento: str, entrega_realizada: bool = False, data_insercao: Union[DateTime, None] = None):
        """
        Cria uma Entrega

        Arguments:
            numero_entrega: numero da entrega.
            valor: valor da entrega
            frete: frete da entrega
            forma_pagamento: forma de pagamento
            entrega_realizada: status da entrega
            data_insercao: data de quando a entrega foi inserida à base
        """
        self.numero_entrega = numero_entrega
        self.valor = valor
        self.frete = frete
        self.forma_pagamento = forma_pagamento

        # se não for informada, será false o valor de entrega realizada
        if entrega_realizada:
            self.entrega_realizada = entrega_realizada

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao
