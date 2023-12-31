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
    """Adiciona uma nova entrega à base de dados e gera valor do frete dependendo da região

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
        logradouro = cep_data.get('logradouro') # obtendo nome da rua
        uf = cep_data.get('uf')  # obtendo UF do CEP
        frete = get_frete(uf)  # Obtenha a taxa de frete com base na UF
    else:
        # Caso em que a API de CEP retornou um status de erro
        return {"message": "Erro ao obter informações do CEP"}, 500

    entrega = Entrega(
        numero_entrega=form.numero_entrega,
        valor=form.valor,
        frete=frete,
        logradouro=logradouro,
        forma_pagamento=form.forma_pagamento
    )

    try:
        # criando conexão com a base
        session = Session()
        # adicionando entrega
        session.add(entrega)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Criando entrega com numero: '{entrega.numero_entrega}'")
        return apresenta_entrega(entrega), 200

    except IntegrityError as e:
        # como a duplicidade do numero de entrega é a provável razão do IntegrityError
        error_msg = "Entrega com o mesmo numero já salvo na base :/"
        logger.warning(
            f"Erro ao criar entrega '{entrega.numero_entrega}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(
            f"Erro ao criar entrega '{entrega.numero_entrega}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/buscar_entregas', tags=[entrega_tag],
         responses={"200": ListagemEntregasSchema, "404": ErrorSchema})
def buscar_entregas():
    """Faz a busca por todas as entregas na base

    Retorna uma representação da listagem de entregas.
    """
    logger.debug(f"Coletando entregas ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    entregas = session.query(Entrega).all()

    if not entregas:
        # se não há entregas cadastrados
        return {"entregas": []}, 200
    else:
        logger.debug(f"%d entregas encontrados" % len(entregas))
        # retorna a representação de entregas
        print(entregas)
        return apresenta_entregas(entregas), 200


@app.get('/buscar_entrega_numero', tags=[entrega_tag],
         responses={"200": EntregaViewSchema, "404": ErrorSchema})
def buscar_entrega_numero(query: EntregaBuscaSchema):
    """Faz a busca por uma entrega a partir do numero da entrega

    Retorna uma representação de entrega.
    """
    numero = query.numero_entrega
    logger.debug(f"Coletando dados sobre a entrega #{numero}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    entrega = session.query(Entrega).filter(
        Entrega.numero_entrega == numero).first()

    if not entrega:
        # se a entrega não foi encontrada
        error_msg = "Entrega não encontrada na base :/"
        logger.warning(f"Erro ao buscar entrega '{numero}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Entrega encontrada: '{numero}'")
        # retorna a representação de entrega
        return apresenta_entrega(entrega), 200


@app.delete('/deletar_entrega', tags=[entrega_tag],
            responses={"200": EntregaDelSchema, "404": ErrorSchema})
def deletar_entrega(query: EntregaBuscaSchema):
    """Deleta uma entrega a partir do numero da entrega informada

    Retorna uma mensagem de confirmação da remoção.
    """
    numero_entrega = query.numero_entrega
    print(numero_entrega)
    logger.debug(f"Deletando dados da entrega numero #{numero_entrega}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Entrega).filter(
        Entrega.numero_entrega == numero_entrega).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletada entrega #{numero_entrega}")
        return {"message": "entrega removida", "numero_entrega": numero_entrega}
    else:
        # se a entrega não foi encontrada
        error_msg = "Entrega não encontrada na base :/"
        logger.warning(
            f"Erro ao deletar entrega #'{numero_entrega}', {error_msg}")
        return {"message": error_msg}, 404


@app.put('/atualizar_status_entrega', tags=[entrega_tag],
         responses={"200": EntregaDelSchema, "404": ErrorSchema})
def atualizar_status_entrega(query: EntregaStatusSchema):
    """Atualizar o status de uma entrega a partir do numero da entrega informada

    Retorna uma mensagem de confirmação da atualização.
    """

    numero = query.numero_entrega
    novo_status = query.entrega_realizada

    # criando conexão com a base
    session = Session()
    try:
        # Encontre a entrega com base no número da entrega fornecido
        entrega = session.query(Entrega).filter(
            Entrega.numero_entrega == numero).first()

        if not entrega:
            # Se a entrega não existe, retorne um erro 404
            error_msg = "Entrega não encontrada na base :/"
            logger.warning(f"Erro ao buscar entrega '{numero}', {error_msg}")
            return {"message": "Entrega não encontrada."}, 404

        # Atualize o status da entrega com o novo status fornecido
        entrega.entrega_realizada = novo_status

        # Commit da atualização no banco de dados
        session.commit()

        return {"message": "Status da entrega atualizado com sucesso.", "numero_entrega": numero}
    except Exception as e:
        # Em caso de erro, retorne um erro 500
        logger.error(f"Erro ao atualizar status da entrega: {str(e)}")
        return {"message": "Erro ao atualizar status da entrega."}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)