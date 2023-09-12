from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from models import Session, Entrega
from logger import logger
from schemas import *
from flask_cors import CORS

from enums import validate_cep, get_frete

import requests

info = Info(title="API destinada para o projeto iDeliverTech, Microsserviço responsável pelo gerenciamento de entregas ", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação",
               description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
entrega_tag = Tag(
    name="Entrega", description="Adição, alteração, visualização e remoção de entregas da base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/criar_entrega', tags=[entrega_tag],
          responses={"200": EntregaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def criar_entrega(form: EntregaSchema):
    """Adiciona uma nova entrega à base de dados

    Retorna uma representação das entregas.
    """

    # Validação do CEP
    # Caso ocorra algum erro, verifique os logs.
    validate_cep(form.cep)

    # requisição para a API externa de CEP para obter informações detalhadas do CEP
    api_cep_url = f'https://viacep.com.br/ws/{form.cep}/json/'
    response = requests.get(api_cep_url)

    if response.status_code == 200:
        cep_data = response.json()
        uf = cep_data.get('uf')

        # Obtenha a taxa de frete com base na UF
        frete = get_frete(uf)
    else:
        # Trate o caso em que a API de CEP retornou um status de erro
        return {"message": "Erro ao obter informações do CEP"}, 500

    entrega = Entrega(
        numero_entrega=form.numero_entrega,
        valor=form.valor,
        frete=frete,
        forma_pagamento=form.forma_pagamento
    )

    try:
        # criando conexão com a base
        session = Session()
        # adicionando livro
        session.add(entrega)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Criando entrega com numero: '{entrega.numero_entrega}'")
        return apresenta_entrega(entrega), 200

    except IntegrityError as e:
        # como a duplicidade do numero de entrega é a provável razão do IntegrityError
        error_msg = "Entrega com o mesmo numero já salvo na base :/"
        logger.warning(f"Erro ao criar entrega '{entrega.numero_entrega}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao criar entrega '{entrega.numero_entrega}', {error_msg}")
        return {"message": error_msg}, 400
