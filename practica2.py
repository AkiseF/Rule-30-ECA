import pygame
import numpy as np
import sys
import os
from datetime import datetime

# Inicializar pygame
pygame.init()

# Obtener las dimensiones de la pantalla para el modo de ventana maximizada
screen_info = pygame.display.Info()
WIDTH, HEIGHT = screen_info.current_w - 100, screen_info.current_h - 100  # Dejar un margen
INITIAL_CELL_SIZE = 5
MIN_CELL_SIZE = 1
MAX_CELL_SIZE = 10
current_cell_size = INITIAL_CELL_SIZE

# Calcular las dimensiones de la cuadrícula - hacerla más grande para permitir zoom
GRID_WIDTH = WIDTH * 2 // current_cell_size
GRID_HEIGHT = HEIGHT * 2 // current_cell_size

# Configurar la pantalla - ventana maximizada en lugar de pantalla completa
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Autómata Celular Regla 30")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # Color para el backbone (columna vertebral)

# Fuente para el contador de generaciones
pygame.font.init()
font = pygame.font.SysFont('Arial', 24)

# Función de la Regla 30
def apply_rule30(a, b, c):
    pattern = (a << 2) | (b << 1) | c
    # Regla 30: 00011110 en binario (30 en decimal)
    return 1 if pattern in [1, 2, 3, 4] else 0

# Inicializar la cuadrícula con una sola célula en el medio
def initialize_grid():
    # Crear un historial de estados para el desplazamiento vertical
    history = []
    first_row = np.zeros(GRID_WIDTH, dtype=int)
    first_row[GRID_WIDTH // 2] = 1  # Establecer la célula central como activa
    history.append(first_row)
    return history

# Calcular la siguiente generación basada en la Regla 30
def next_generation(current_row):
    next_row = np.zeros_like(current_row)
    for i in range(len(current_row)):
        left = current_row[(i - 1) % len(current_row)]
        center = current_row[i]
        right = current_row[(i + 1) % len(current_row)]
        next_row[i] = apply_rule30(left, center, right)
    return next_row

# Dibujar las células en la pantalla
def draw_cells(history, view_x, view_y, cell_size, show_backbone_only=False, auto_scroll=False):
    screen.fill(WHITE)
    
    # Calcular las células visibles según el tamaño actual de la célula
    visible_width = WIDTH // cell_size
    visible_height = HEIGHT // cell_size
    
    # Calcular el rango de filas y columnas a mostrar según la posición de la vista
    start_row = max(0, int(view_y / cell_size))
    end_row = min(len(history), start_row + visible_height + 1)
      # La columna central (backbone)
    backbone_col = GRID_WIDTH // 2
    
    if show_backbone_only:
        # Mostrar solo la columna central (backbone)
        for y in range(start_row, end_row):
            if y >= len(history):
                break
            
            row = history[y]
            x = backbone_col
            
            # Verificar si la columna central es visible
            if x >= int(view_x / cell_size) and x < int(view_x / cell_size) + visible_width:
                if row[x] == 1:                    pygame.draw.rect(
                        screen,
                        RED,  # Destacar el backbone en rojo
                        (x * cell_size - view_x, y * cell_size - view_y, cell_size, cell_size)
                    )
    else:
        # Mostrar el autómata completo
        start_col = max(0, int(view_x / cell_size))
        end_col = min(GRID_WIDTH, start_col + visible_width + 1)
        
        for y in range(start_row, end_row):
            if y >= len(history):
                break
            
            row = history[y]
            for x in range(start_col, end_col):
                if x >= len(row):
                    break
                    
                if row[x] == 1:
                    # Usar color rojo para las células del backbone, negro para las demás
                    cell_color = RED if x == backbone_col else BLACK
                    
                    pygame.draw.rect(
                        screen,
                        cell_color,
                        (x * cell_size - view_x, y * cell_size - view_y, cell_size, cell_size)
                    )
    
    # Mostrar contador de generaciones con un recuadro de fondo
    gen_text = font.render(f"Generación: {len(history)}", True, BLACK)
    text_width, text_height = gen_text.get_size()
    
    # Crear un fondo semi-transparente para mejor visibilidad
    padding = 10  # Relleno alrededor del texto
    box_rect = pygame.Rect(5, 5, text_width + padding*2, text_height + padding*2)
    
    # Dibujar el recuadro de fondo
    box_surface = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
    box_surface.fill((240, 240, 240, 230))  # Gris claro con ligera transparencia
    pygame.draw.rect(box_surface, BLACK, box_surface.get_rect(), 2)  # Borde
    screen.blit(box_surface, (box_rect.x, box_rect.y))
    
    # Dibujar el texto sobre el recuadro
    screen.blit(gen_text, (box_rect.x + padding, box_rect.y + padding))
      # Mostrar información de auto-desplazamiento si está habilitado
    if auto_scroll:
        auto_text = font.render("Auto-Scroll ACTIVADO (ESPACIO para alternar, ↑↓ para ajustar velocidad)", True, BLACK)
        auto_text_width, auto_text_height = auto_text.get_size()
        
        # Crear recuadro de información para auto-scroll
        auto_box_rect = pygame.Rect(5, box_rect.height + 10, auto_text_width + padding*2, auto_text_height + padding*2)
        auto_box_surface = pygame.Surface((auto_box_rect.width, auto_box_rect.height), pygame.SRCALPHA)
        auto_box_surface.fill((240, 240, 240, 230))  # Gris claro con ligera transparencia
        pygame.draw.rect(auto_box_surface, BLACK, auto_box_surface.get_rect(), 2)  # Borde
        
        screen.blit(auto_box_surface, (auto_box_rect.x, auto_box_rect.y))
        screen.blit(auto_text, (auto_box_rect.x + padding, auto_box_rect.y + padding))

# Función para guardar el backbone en un archivo
def save_backbone(history):
    # Crear directorio para guardar los archivos si no existe
    save_dir = "backbone_data"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # Generar nombre de archivo con marca de tiempo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(save_dir, f"backbone_{timestamp}.txt")
    
    # Obtener la columna del backbone
    backbone_col = GRID_WIDTH // 2
    
    # Abrir archivo y escribir los valores del backbone
    with open(filename, 'w') as f:
        f.write(f"# Backbone del Autómata Celular Regla 30 - {timestamp}\n")
        f.write(f"# Total generaciones: {len(history)}\n")
        f.write("# Formato: 1 = célula activa, 0 = célula inactiva\n\n")
        
        # Guardar cada generación del backbone
        for i, row in enumerate(history):
            f.write(f"Generación {i}: {row[backbone_col]}\n")
    
    return filename

def show_save_message(message):
    # Crear texto
    save_text = font.render(message, True, BLACK)
    text_width, text_height = save_text.get_size()
    
    # Crear un fondo semi-transparente para mejor visibilidad
    padding = 10  # Relleno alrededor del texto
    box_rect = pygame.Rect(WIDTH // 2 - text_width // 2 - padding, HEIGHT - text_height - padding*2 - 10, 
                          text_width + padding*2, text_height + padding*2)
    
    # Dibujar el recuadro de fondo
    box_surface = pygame.Surface((box_rect.width, box_rect.height), pygame.SRCALPHA)
    box_surface.fill((240, 240, 240, 230))  # Gris claro con ligera transparencia
    pygame.draw.rect(box_surface, BLACK, box_surface.get_rect(), 2)  # Borde
    screen.blit(box_surface, (box_rect.x, box_rect.y))
    
    # Dibujar el texto sobre el recuadro
    screen.blit(save_text, (box_rect.x + padding, box_rect.y + padding))

def main():
    # Inicializar la cuadrícula
    history = initialize_grid()
    
    # Generar suficientes generaciones para llenar la pantalla inicialmente
    for _ in range(GRID_HEIGHT * 2):  # El doble de la altura de la pantalla para el desplazamiento
        next_row = next_generation(history[-1])
        history.append(next_row)
    
    # Posición de vista para el desplazamiento - inicializar para centrar en la célula semilla
    view_x = max(0, (GRID_WIDTH // 2 * INITIAL_CELL_SIZE) - (WIDTH // 2))
    view_y = 0  # Comenzar desde arriba para ver la evolución
    
    # Para manejar el arrastre del ratón y el zoom
    dragging = False
    prev_mouse_pos = (0, 0)
    cell_size = INITIAL_CELL_SIZE
    
    # Indicadores para diferentes modos de visualización
    show_backbone_only = False
    auto_scroll = False  # Indicador para desplazamiento automático
    auto_scroll_speed = 2  # Píxeles por frame para desplazarse
    
    # Variable para almacenar el mensaje de guardado
    save_message = ""
    save_message_time = 0
    
    # Bucle principal del juego
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_b:  # Alternar vista de backbone con la tecla 'B'
                    show_backbone_only = not show_backbone_only
                elif event.key == pygame.K_SPACE:  # Alternar auto-scroll con la tecla ESPACIO
                    auto_scroll = not auto_scroll
                elif event.key == pygame.K_UP:  # Aumentar velocidad de desplazamiento
                    auto_scroll_speed = min(10, auto_scroll_speed + 1)                
                elif event.key == pygame.K_DOWN:  # Disminuir velocidad de desplazamiento
                    auto_scroll_speed = max(1, auto_scroll_speed - 1)
                elif event.key == pygame.K_s:  # Guardar backbone con la tecla 'S'
                    filename = save_backbone(history)
                    save_message = f"Backbone guardado en: {filename}"
                    save_message_time = pygame.time.get_ticks()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botón izquierdo del ratón
                    dragging = True
                    prev_mouse_pos = event.pos
                    # Desactivar auto-scroll cuando se arrastra manualmente
                    if auto_scroll:
                        auto_scroll = False
                elif event.button == 4:  # Rueda del ratón hacia arriba - alejarse (zoom out)
                    # Guardar la posición del ratón antes del zoom para centrar
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    # Registrar coordenadas del mundo bajo el ratón antes del zoom
                    world_x = view_x + mouse_x
                    world_y = view_y + mouse_y
                    
                    # Calcular coordenadas de la célula
                    cell_x = world_x / cell_size
                    cell_y = world_y / cell_size
                    
                    # Zoom out (aumentar tamaño de célula) si no está en el máximo
                    if cell_size < MAX_CELL_SIZE:
                        cell_size += 1
                    
                    # Ajustar posición de vista para mantener la misma célula lógica bajo el ratón
                    view_x = cell_x * cell_size - mouse_x
                    view_y = cell_y * cell_size - mouse_y
                elif event.button == 5:  # Rueda del ratón hacia abajo - acercarse (zoom in)
                    # Guardar la posición del ratón antes del zoom para centrar
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    
                    # Registrar coordenadas del mundo bajo el ratón antes del zoom
                    world_x = view_x + mouse_x
                    world_y = view_y + mouse_y
                    
                    # Calcular coordenadas de la célula
                    cell_x = world_x / cell_size
                    cell_y = world_y / cell_size
                    
                    # Zoom in (disminuir tamaño de célula) si no está en el mínimo
                    if cell_size > MIN_CELL_SIZE:
                        cell_size -= 1
                    
                    # Ajustar posición de vista para mantener la misma célula lógica bajo el ratón
                    view_x = cell_x * cell_size - mouse_x
                    view_y = cell_y * cell_size - mouse_y            
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    # Calcular el delta de movimiento
                    dx = prev_mouse_pos[0] - event.pos[0]
                    dy = prev_mouse_pos[1] - event.pos[1]
                    
                    # Actualizar la posición de la vista
                    view_x += dx
                    view_y += dy
                    
                    # Asegurar que la vista permanezca dentro de los límites - ajustado para tamaño dinámico de célula
                    max_x = (GRID_WIDTH * cell_size) - WIDTH
                    max_y = (len(history) * cell_size) - HEIGHT
                    view_x = max(0, min(view_x, max_x if max_x > 0 else 0))
                    view_y = max(0, min(view_y, max_y if max_y > 0 else 0))
                    
                    prev_mouse_pos = event.pos        # Manejar el desplazamiento automático
        if auto_scroll:
            # Mover la posición de vista automáticamente hacia abajo
            view_y += auto_scroll_speed
            
            # Generar nuevas filas según sea necesario para mantener un desplazamiento continuo
            if view_y + HEIGHT > (len(history) - GRID_HEIGHT // 4) * cell_size:
                for _ in range(GRID_HEIGHT // 4):  # Generar menos filas a la vez para una experiencia más suave
                    next_row = next_generation(history[-1])
                    history.append(next_row)
        
        # Siempre generar nuevas filas si nos acercamos al final de nuestro historial
        # Esto asegura que siempre tengamos filas para desplazarnos
        elif view_y + HEIGHT > (len(history) - GRID_HEIGHT // 2) * cell_size:
            for _ in range(GRID_HEIGHT // 2):
                next_row = next_generation(history[-1])
                history.append(next_row)
        
        # Dibujar el estado actual with el tamaño actual de célula
        draw_cells(history, view_x, view_y, cell_size, show_backbone_only, auto_scroll)
        
        # Mostrar mensaje de guardado si es necesario
        current_time = pygame.time.get_ticks()
        if save_message and current_time - save_message_time < 3000:  # Mostrar durante 3 segundos
            show_save_message(save_message)
        
        # Actualizar la pantalla
        pygame.display.flip()
        clock.tick(60)
    
    # Cerrar Pygame correctamente después de que el bucle principal termine
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()