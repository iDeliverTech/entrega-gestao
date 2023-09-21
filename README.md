# Microsserviço A - Entrega-Gestao
 Este repositório conterá o código-fonte e os recursos relacionados ao microsserviço responsável pelo gerenciamento de entregas em seu sistema.


> É de suma importância que este Microsserviço seja iniciado antes do Microsserviço B (Cliente-Gestão) para garantir que ambos estejam na mesma rede e possam se comunicar.

---

## Como executar via Docker 
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.


&nbsp;


Este comando constrói uma imagem Docker com a tag `ideliver-tech-entrega:1.0` a partir do contexto atual (diretório atual).
```
(env) docker build -t ideliver-tech-entrega:1.0 .
```


&nbsp;


Este comando cria uma rede Docker chamada `rede-deliver`. As redes permitem que contêineres Docker se comuniquem entre si de maneira isolada.
```
(env) docker network create rede-deliver
```

&nbsp;


Este comando executa um contêiner Docker com o nome `ideliver-entrega` usando a imagem `ideliver-tech-entrega:1.0`. Ele mapeia a porta 5000 do host para a porta 5000 do contêiner e conecta o contêiner à rede `rede-deliver`. Isso inicia sua aplicação em um ambiente Docker.
```
(env) docker run -p 5000:5000 --name ideliver-entrega --network rede-deliver ideliver-tech-entrega:1.0
```

&nbsp;


Após a execução destes comandos passados, é ideal iniciar o Componente B (Cliente-Gestão). Isso garantirá que ambos os microsserviços possam se comunicar efetivamente na mesma rede Docker.
> Após a execução dos comandos passados, Abra o http://127.0.0.1:5000/#/ no navegador desejado.

---


&nbsp;


## Como executar por via linha de comando

Será necessário ter todas as libs python listadas no `requirements.txt` instaladas.
Após clonar o repositório, é necessário ir ao diretório raiz, pelo terminal, para poder executar os comandos descritos abaixo.

> É fortemente indicado o uso de ambientes virtuais do tipo [virtualenv](https://virtualenv.pypa.io/en/latest/installation.html).


&nbsp;


Execute o seguinte comando para utilizar o ambiente virtual.

```
(Unix/macOS)
$ source env/Scripts/activate

(Windows)
$ .\env\Scripts\activate
```

&nbsp;


Agora, estando no ambiente virtual, execute o comando abaixo para execução via docker:

Estando no ambiente virtual, execute o comando abaixo:

```
(env)$ pip install -r requirements.txt
```

Este comando instala as dependências/bibliotecas, descritas no arquivo `requirements.txt`.


&nbsp;


> Caso ocorra algum erro de instalação com greenlet, execute o seguinte comando:

```
(env)$ pip install greenlet
```

Este comando instala a biblioteca, chamada Greenlet que permite a execução de tarefas concorrentes de forma controlada em um único thread.


&nbsp;


Para executar a API  basta executar:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```


&nbsp;


Em modo de desenvolvimento é recomendado executar utilizando o parâmetro reload, que reiniciará o servidor
automaticamente após uma mudança no código fonte. 

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

Abra o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução. 
