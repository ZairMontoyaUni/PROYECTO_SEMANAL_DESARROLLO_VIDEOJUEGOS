# SPACE HUNTERS

Proyecto semanal de Desarrollo de Videojuegos (Python + pygame-ce + esper / ECS).

ENLACE DEL JUEGO EN ITCH.IO:
PEGAR_AQUI_EL_ENLACE

Autor: Zair Samuel Montoya Bello

## CONTROLES

Flechas ........ mover la nave
Clic izquierdo . disparar hacia el ratón (máximo de balas definido en el nivel)
Clic derecho ... ataque especial: 4 balas en diagonal (recarga de 2.5 s)
P .............. pausar / reanudar
F11 ............ pantalla completa

## CÓMO JUGAR

- Los asteroides rebotan por la pantalla; los Hunter (naves rojas) te persiguen
  si te acercas y regresan a su origen si se alejan demasiado.
- Si un enemigo te toca, vuelves al punto de origen y el nivel se reinicia.
- En la esquina superior izquierda ves el estado del ataque especial:
  verde "LISTO" o amarillo con los segundos que faltan para recargar.

## EJECUTAR DESDE EL CÓDIGO

pip install -r requirements.txt
python main.py
