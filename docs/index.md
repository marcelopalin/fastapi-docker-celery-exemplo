# Projeto FastAPI Docker Celery

!!! note "Objetivo do Projeto"
    O objetivo desse projeto é mostrar como utilizar o FastAPI com Celery
    dentro de containers.

Utilizamos o REDIS como Broker. Também utilizamos o Flower para monitorar
o envio das tarefas. Para simularmos a função do Flower criamos um
frontend que fica requisitando o status da tarefa a cada 1 segundo.
