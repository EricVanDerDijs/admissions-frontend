# Para correr el cliente, debe:

1. activar el venv de python (posicionandose en la carpeta raíz del proyecto):

`source bin/activate`

2. correr el sieguiente comando especificando algúno de los servidores a los cuales se conectará, suponiendo que cada cliente estará confinado a un recinto de pruebas y tendrá un servidor local sincronizado con sus replicas.

`python src/index.py $(ip) $(port)`

ejemplo:

`python src/index.py 172.17.0.1 3010`

las direcciones de las replicas al correr el comando withreplicas de api son (para la configuración default del bridge de docker)

172.17.0.1:3010
172.17.0.1:3020
172.17.0.1:3030