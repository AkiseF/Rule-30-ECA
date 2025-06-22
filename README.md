# Rule-30-ECA
Práctica 2 del curso Cellular Automata | Complex Systems

Este proyecto implementa una visualización interactiva del Autómata Celular Elemental de la Regla 30.

## Objetivos de la Práctica
1. Calcular el mayor número de generaciones sin que las células de la frontera se acerquen. Utilizar cualquier método que ayude a resolver este problema.
2. Tratar de responder las tres preguntas planteadas por Stephen Wolfram.

Más información: https://www.rule30prize.org

## Descripción del Proyecto

El Autómata Celular Elemental de la Regla 30 es uno de los ejemplos más estudiados de sistemas complejos emergentes. Este programa permite visualizar la evolución de este autómata a partir de una única célula inicial, observar su desarrollo a lo largo del tiempo y estudiar su comportamiento.

## Características

- **Visualización dinámica**: Permite ver la evolución del autómata celular en tiempo real
- **Zoom interactivo**: Acercar y alejar con la rueda del ratón
- **Navegación por arrastre**: Explorar diferentes regiones del autómata
- **Modo backbone**: Visualizar solo la "columna vertebral" central del autómata
- **Desplazamiento automático**: Visualización automática de nuevas generaciones
- **Exportación de datos**: Guardar la secuencia del backbone en formato de texto

## Controles

| Tecla/Acción | Función |
|--------------|---------|
| Arrastrar con ratón | Navegar por el espacio del autómata |
| Rueda del ratón arriba | Alejar (zoom out) |
| Rueda del ratón abajo | Acercar (zoom in) |
| Tecla `B` | Alternar entre vista completa y solo backbone |
| Tecla `ESPACIO` | Activar/desactivar desplazamiento automático |
| Flecha `ARRIBA` | Aumentar velocidad de desplazamiento automático |
| Flecha `ABAJO` | Disminuir velocidad de desplazamiento automático |
| Tecla `S` | Guardar la secuencia del backbone en un archivo de texto |
| Tecla `ESC` | Salir del programa |

## Funcionamiento del Autómata Celular - Regla 30

La Regla 30 determina el estado de una célula en la siguiente generación basándose en su estado actual y el de sus vecinas inmediatas:

| Patrón actual | 111 | 110 | 101 | 100 | 011 | 010 | 001 | 000 |
|--------------|-----|-----|-----|-----|-----|-----|-----|-----|
| Estado siguiente | 0 | 0 | 0 | 1 | 1 | 1 | 1 | 0 |

El número "30" viene de interpretar esta tabla como un número binario: 00011110₂ = 30₁₀

## Exportación de Datos

Al presionar la tecla `S`, el programa guarda la secuencia del backbone (la columna central del autómata) en un archivo de texto en el directorio `backbone_data`. Esta secuencia contiene los valores (0 o 1) de la columna central para cada generación, concatenados en una sola cadena.

Formato del archivo generado:
```
# Backbone del Autómata Celular Regla 30 - [timestamp]
# Total generaciones: [número]
# Formato: 1 = célula viva, 0 = célula muerta

[secuencia de 0s y 1s]
```

## Requisitos

- Python 3.x
- Pygame
- NumPy

## Instalación

1. Asegúrate de tener Python instalado
2. Instala las dependencias: `pip install pygame numpy`
3. Ejecuta el programa: `python practica2.py`

---

Proyecto desarrollado como práctica para el curso de Sistemas Complejos del semestre 2025/2.
