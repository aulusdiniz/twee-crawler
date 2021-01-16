Usando o Docker podemos fazer o seguinte:

Para 'copiar' a imagem do container usamos o comando
    $ docker pull mongo

Para 'executar' o container use o comando
    $ docker run --name twittery -d mongo:latest

A seguir, a ultima linha do output deste comando deve ser o IP para acessar o Mongo.
    $ docker exec twittery cat /etc/hosts

Para 'parar' o container use o comando
    $ docker stop twittery

Para 'iniciar' o container use o comando
    $ docker start twittery