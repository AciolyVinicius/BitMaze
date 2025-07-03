# Arquivo: ProjetoFinal_comentado.py
# Comentado por ChatGPT em revisão de projeto BitMaze
# Comentários foram adicionados para esclarecer funcionalidades e sugerir melhorias

from machine import ADC, Pin, SoftI2C, PWM, I2C, UART
from ssd1306 import SSD1306_I2C
from mpu6050 import MPU6050
import uasyncio as asyncio
import random
import neopixel
import time

# Inicializa o barramento I2C (use os pinos corretos para seu hardware)
i2c = I2C(0, scl=Pin(17), sda=Pin(16))

# MPU - acelerometro
#mpu1 = MPU6050(i2c)
#mpu1.write_accel_range(0)
#mpu1.wake()

uart = UART(0, baudrate=9600, tx=16, rx=17)

# Inicializa o display OLED via I2C nos pinos 14 (SDA) e 15 (SCL)
i2c_oled = SoftI2C(scl=Pin(15), sda=Pin(14))
oled = SSD1306_I2C(128, 64, i2c_oled)

# Configura os eixos do joystick (entrada analógica)
adc_y_pin = ADC(Pin(26))
adc_x_pin = ADC(Pin(27))

# Configura os pinos PWM para controle do LED RGB
led_r = PWM(Pin(12))
led_g = PWM(Pin(11))
led_b = PWM(Pin(13))
led_r.freq(1000)
led_g.freq(1000)
led_b.freq(1000)

# Settando botão A e B como entrada com resistor de pull-up
button_a = Pin(5, Pin.IN, Pin.PULL_UP)
button_b = Pin(6, Pin.IN, Pin.PULL_UP)

# Matriz de leds 5x5 e suas respectivas posições
LED_MATRIZ = [
    [24, 23, 22, 21, 20],    
    [15, 16, 17, 18, 19],
    [14, 13, 12, 11, 10],
    [5, 6, 7, 8, 9],
    [4, 3, 2, 1, 0]
]
right_side = [20, 19, 10, 9, 0]
left_side = [24, 15, 14, 5, 4]
top = [0, 1, 2, 3, 4]
botton = [20, 21, 22, 23, 24]

heart = [
    0, 0, 45, 0, 0,
    0, 45, 45, 45, 0,
    45, 45, 45, 45, 45,
    45, 45, 45, 45, 45,
    0, 45, 0, 45, 0
]

plus = [
    0, 0, 45, 0, 0,
    0, 0, 45, 0, 0,
    45, 45, 45, 45, 45,
    0, 0, 45, 0, 0,
    0, 0, 45, 0, 0
]

one = [
    0, 45, 45, 45, 0,
    0, 0, 45, 0, 0,
    0, 0, 45, 0, 0,
    0, 0, 45, 45, 0,
    0, 0, 45, 0, 0
]

all_map = [[[None]*5 for _ in range(5)] for _ in range(4)]

# Inicializa a matriz de leds
np = neopixel.NeoPixel(Pin(7), 25) # Pino responsavel pelo led e o numero de leds

def led(r, g, b):
    """
        Define a cor do LED RGB convertendo valores de 0-255 para 0-65535.
    """
    led_r.duty_u16(int(r * 65535 / 255))
    led_g.duty_u16(int(g * 65535 / 255))
    led_b.duty_u16(int(b * 65535 / 255))

def set_new_position(position_, new_position):
    """
        Seta nova posição do player na matrix de leds
        Delay de 0.25 sec entre cada movimento
    """
    global np

    np[position_] = (0, 0, 0)
    np[new_position] = (10, 10, 10)
    np.write()
    position = new_position
    time.sleep(0.25)
    return position

async def set_position_animation(position_, new_position):
    np[position_] = (0, 0, 0)
    np[new_position] = (10, 10, 10)
    np.write()    

def control_joystick(adc_x, adc_y, position):
    """
        Função que obtem a coordenada atual da posição do player e atualiza conforme
        valor no joystick (adc_x, adc_y).
    """
    
    row_index, column_index = next(((index, row.index(position)) for index, row in enumerate(LED_MATRIZ) if position in row))
    if adc_x >= 20000:
        if position in right_side:
            return -1
        position = position - 1 if row_index % 2 == 0 else position + 1
    elif adc_x <= -20000:
        if position in left_side:
            return -2
        position = position - 1 if row_index % 2 == 1 else position + 1
    if adc_y >= 20000:
        if position in top:
            return -3
        position = LED_MATRIZ[row_index+1][column_index]
    elif adc_y <= -20000:
        if position in botton:
            return -4
        position = LED_MATRIZ[row_index-1][column_index]
        
    return position

def set_radar(position_, list_obs, list_radar, list_life, final_position, current_map):
    """
        Obtém as posições de cada led do radar e realiza sua animação ao ser utilizado
    """
    radar_leds = radar_position(position_)
    
    # Fade-in radar
    for i in range(0, 20):
        for led in radar_leds:
            if led == final_position and current_map == 3:
                np[led] = (i, i, 0)
            elif led in list_obs:
                np[led] = (i, 0, 0)
            elif led in list_radar:
                np[led] = (0, 0, i)
            elif led in list_life:
                np[led] = (i, i//2, i//2)
            elif led:
                np[led] = (0, i, 0)
        np.write()
        time.sleep(0.02)
    # Fade-out radar    
    for i in range(20, -1, -1):
        for led in radar_leds:
            if led == final_position and current_map == 3:
                np[led] = (i, i, 0)
            elif led in list_obs:
                np[led] = (i, 0, 0)
            elif led in list_radar:
                np[led] = (0, 0, i)
            elif led in list_life:
                np[led] = (i, i//2, i//2)
            elif led:            
                np[led] = (0, i, 0)
        np.write()            
        time.sleep(0.02)
    
def radar_position(position_):
    """
        Retorna as posições dos LEDs ao redor (laterais e diagonais) da posição atual do player.
    """
    
    # Varíaveis que permitem ou não os leds nos cantos da esquerda e nos canto da direita
    radar_diagonal_left, radar_diagonal_right = False, False
    # Varíaveis responsáveis por cara led ao redor do player (r- right, l- left, t- top, b- botton)
    radar_r, radar_l, radar_t, radar_b, radar_tr, radar_tl, radar_br, radar_bl = None, None, None, None, None, None, None, None
    
    # Percorre pela matriz de led até achar a linha correspondente a posição atual do player
    # após checar a condição, guarda o valor de linha e da coluna da posição atual, para
    # assim, calcular as posições dos leds a sua volta.
    row_index, column_index = next(((index, row.index(position)) for index, row in enumerate(LED_MATRIZ) if position in row))
    
    # Calcula posição de todos os leds usados no radar
    if position not in left_side:     # Caso não esteja no lado esquerda, leds da esquerda podem ser acessos. A mesma lógica é aplicada abaixo
        radar_l = LED_MATRIZ[row_index][column_index - 1]
        radar_diagonal_left = True
    if position not in right_side:
        radar_r = LED_MATRIZ[row_index][column_index + 1]
        radar_diagonal_right = True
    if position not in botton:
        radar_b = LED_MATRIZ[row_index - 1][column_index]
        if radar_diagonal_left:
            radar_bl = LED_MATRIZ[row_index - 1][column_index - 1]
        if radar_diagonal_right:
            radar_br = LED_MATRIZ[row_index - 1][column_index + 1]
    if position not in top:
        radar_t = LED_MATRIZ[row_index + 1][column_index]
        if radar_diagonal_left:
            radar_tl = LED_MATRIZ[row_index + 1][column_index - 1]
        if radar_diagonal_right:
            radar_tr = LED_MATRIZ[row_index + 1][column_index + 1]
        
    return radar_l, radar_r, radar_b, radar_t, radar_tr, radar_tl, radar_br, radar_bl

def loss_life(position_, new_position):
    """
        Reduz a vida do jogador e chama a função de animação de dano.
    """
    global new_health

    new_health -= 1
    asyncio.run(damage_main(position_, new_position))
    life_id = life_images[new_health]
    new_image(id_=25)
    for _ in range(2):
        send_cmd(f"{life_id}.pic=22")
        time.sleep(0.1)
        send_cmd(f"{life_id}.pic=20")
        time.sleep(0.15)
    send_cmd(f"{life_id}.pic=22")

async def loss_life_animation(position_, new_position):
    """
        Animação de perda de vida ao atingir um obstáculo.
    """

    global np
    
    # Apaga player na posição original
    np[position_] = (0, 0, 0)
    np.write()
    
    # Player aparece onde está o obstáculo
    np[new_position] = (10, 10, 10)
    np.write()
    await asyncio.sleep(0.3)
    
    # Pisca o player 3 vezes em vermelho
    for _ in range(3):
        np[new_position] = (10, 0, 0)
        np.write()
        led(40, 0, 0)
        await asyncio.sleep(0.2)
        np[new_position] = (0, 0, 0)
        np.write()
        led(0, 0, 0)
        await asyncio.sleep(0.1)
    
    np[position] = (10, 10, 10)
    np.write()

async def gameover():
    """
        Responsável pela animação do player ao perder todas as vidas
        
    """
    global np

    oled.fill(0)
    oled.text("    GAME OVER", 0, 30)
    oled.show()
    
    np[position] = (10, 10, 10)
    np.write()
    await asyncio.sleep(0.3)
 
    # Pisca player 4 vezes
    for _ in range(4):
        np[position] = (10, 0, 0)
        np.write()
        led(40, 0, 0)
        time.sleep(0.2)
        np[position] = (0, 0, 0)
        np.write()
        led(0, 0, 0)
        await asyncio.sleep(0.1)
    await asyncio.sleep(0.3)
    
    # Fade-out no player
    for i in range(10, -1, -1):
        np[position] = (i, i, i)
        led(100*i//10, 100*i//10, 100*i//10)
        np.write()
        await asyncio.sleep(0.25)
    
    for i in range(25):
        np[i] = (0, 0, 0)
    np.write()   
    
    # Faz um X vermelho na tela
    x_position = [0, 8, 12, 16, 24, 20, 18, 6, 4]
    for pos in x_position:
        np[pos] = (30, 0, 0)
        np.write()
        await asyncio.sleep(0.08)
    await asyncio.sleep(0.1)
    for pos in x_position:
        np[pos] = (0, 0, 0)
        np.write()
    
async def win():
    """
        Verifica se o player chegou na posição final.
        Caso positivo, os leds piscam 5 vezes e seta mensagem de vitória na tela
    """
    global np
    
    led(0, 30, 0)
    oled.fill(0)
    oled.text("    Vitoria!", 0, 30)
    oled.show()
    for i in range(5):
        for i in range(0, 25):
            np[i] = (5, 5, 5)
        np.write()
        led(0, 30, 0)
        await asyncio.sleep(0.3)
        for i in range(0, 25):
            np[i] = (0, 0, 0)
        np.write()
        led(0, 0, 0)
        await asyncio.sleep(0.3)
    return True            

# ---------------------------------------------------------------------------

# Mapeia valor do LED para coordenada (linha, coluna)
value_to_coord = {LED_MATRIZ[i][j]: (i, j) for i in range(5) for j in range(5)} #dado o número de um LED (ex: 22), retorna a posição na matriz (linha, coluna)
coord_to_value = {(i, j): LED_MATRIZ[i][j] for i in range(5) for j in range(5)} #dado (linha, coluna), retorna o número do LED

#Essa função retorna os LEDs vizinhos adjacentes (sem diagonais) ao LED atual. Ela garante que não vai sair fora da matriz (com os if 0 <= ...)
def get_adjacent(pos):
    i, j = value_to_coord[pos]
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # cima, baixo, esquerda, direita
    adjacents = []

    for di, dj in moves:
        ni, nj = i + di, j + dj
        # Lógica para não sairmos para fora da matriz de leds
        if 0 <= ni < 5 and 0 <= nj < 5: 
            adjacents.append(LED_MATRIZ[ni][nj]) # adiciona o LED vizinho
    return adjacents # retorna os LEDs vizinhos válidos

#Se o LED atual está preso (sem vizinhos livres), essa função procura o caminho mais curto até o LED livre mais próximo
def shortest_path(start, visited):
    # Encontra a menor rota para um LED não visitado
    # Inicializa a fila com uma tupla contendo:
    # - a posição atual (start)
    # - um caminho vazio (representando o trajeto até o momento)
    list_ = [(start, [])]
    
    # Conjunto para rastrear os nós que já foram visitados pela busca (para evitar ciclos)
    seen = set({})

    # Enquanto ainda houver elementos na fila para explorar
    while list_:
        # Remove e obtém o primeiro elemento da fila (FIFO: garante menor caminho)
        current, path = list_.pop(0)
        
        # Se esse LED atual ainda não foi visitado na caminhada original:
        # significa que encontramos um caminho válido até ele
        if current not in visited:
            return path + [current] # retorna o caminho percorrido até aqui + esse LED
            
        # Se já foi visitado, expandimos para os vizinhos adjacentes
        for neighbor in get_adjacent(current):
            # Se esse vizinho ainda não foi verificado na busca (BFS)
            if neighbor not in seen:
                seen.add(neighbor)# marca como visto para evitar visitas duplicadas
                # Adiciona o vizinho na fila, com o caminho atualizado
                list_.append((neighbor, path + [current]))
        # Se não houver nenhum LED livre (todos foram visitados), retorna caminho vazio
    return []

# Função de caminhada randomica (lugar inicial, quantidade de passos)
def random_walk(start, steps=20):
    current = start # inicia com a posição inicial
    path = [current] # posição atual
    visited = set([current]) # mantém um conjunto de LEDs já visitado

    for _ in range(steps - 1): # já começamos com o primeiro passo, então (steps - 1)
        # Obtém os vizinhos do LED atual
        adj = get_adjacent(current)
        
        # Filtra apenas os que ainda não foram visitados
        choices = [a for a in adj if a not in visited]

        if choices:
            # Escolhe aleatoriamente um dos vizinhos disponíveis
            next_step = random.choice(choices)
        else:
            # Se estiver preso, tenta encontrar o LED não visitado mais próximo
            # preso — busca rota mais curta para LED não visitado
            escape_path = shortest_path(current, visited)
            if not escape_path:
                # se não há caminho de saída (todos visitados), termina
                break  # não há saída
            # Segue o caminho encontrado até o LED livre    
            for step in escape_path:
                path.append(step)
                visited.add(step)
            current = path[-1]
            continue # volta para o loop principal
            
        # Atualiza o caminho e os LEDs visitados
        path.append(next_step)
        visited.add(next_step)
        current = next_step

    return path # retorna a sequência completa da caminhada

def random_sample(source_list, k, num_map = None):
    # Garante que estamos trabalhando com uma lista mutável
    source_list = list(source_list)
    result = []
    dict_map = {0: right_side + top, 1: left_side + top, 2: right_side + botton, 3: left_side + botton}
    
    if num_map:
        filtered_source = [x for x in source_list if x not in dict_map[num_map]]
    else:
        filtered_source = source_list
    for _ in range(min(k, len(filtered_source))):
        index = random.randint(0, len(filtered_source) - 1)
        result.append(filtered_source[index])
        del filtered_source[index]

    # Retorna a amostra aleatória sem repetições
    return result

def create_map(steps = 9, dangers = 5, radar = 2):
    dict_obstacles = {}
    dict_radar = {}
    dict_life = {}
    for num_map in range(0, 4):
        caminho_do_heroi = random_walk(22, steps=steps)
    
        to_find_not_visited_all_leds = {LED_MATRIZ[i][j] for i in range(5) for j in range(5)}
        visited = set(caminho_do_heroi)
        not_visited = (to_find_not_visited_all_leds - visited)

        dangerous_places = set(random_sample(not_visited, min(dangers, len(not_visited)), num_map))
        not_visited = not_visited - dangerous_places
        radar = random.randint(1, radar)
        radar_itens = set(random_sample(not_visited, min(radar, len(not_visited)), num_map))
        not_visited = not_visited - radar_itens
        extra_life = set(random_sample(not_visited, 1, num_map))
        
        dict_obstacles[num_map] = dangerous_places
        dict_radar[num_map] = radar_itens
        dict_life[num_map] = extra_life
    
    return dict_obstacles, dict_radar, dict_life, caminho_do_heroi[-1]

# -------------------------- New Functions ----------------------------
def map_transition(position, new_position):
    global new_current_map

    if current_map == 0:
        if new_position == -3:
            new_current_map = 2
            return position + 20
        
        elif new_position == -1:
            new_current_map = 1
            if (position // 5) % 2 == 0:
                return position + 4
            else:
                return position - 4
        
    elif current_map == 1:
        if new_position == -3:
            new_current_map = 3
            return position + 20
        
        elif new_position == -2:
            new_current_map = 0
            if (position // 5) % 2 == 0:
                return position - 4
            else:
                return position + 4
        
    elif current_map == 2:
        if new_position == -4:
            new_current_map = 0
            return position - 20
        
        elif new_position == -1:
            new_current_map = 3
            if (position // 5) % 2 == 0:
                return position + 4
            else:
                return position - 4
        
    elif current_map == 3:
        if new_position == -4:
            new_current_map = 1
            return position - 20
        
        elif new_position == -2:
            new_current_map = 2
            if (position // 5) % 2 == 0:
                return position - 4
            else:
                return position + 4
        
    return position

# find position out of bounds
def find_position_oob(new_position):
    global LED_MATRIZ
    
    for row in LED_MATRIZ:
        if new_position in row:
            return False
    return True
    
def motor_intensity(position, final_position):
    global new_current_map
    
    x_position =  5-(position%5) if (position//5)%2 == 0 else position%5+1
    y_position = 5 - position // 5
    
    x_final = 10-(final_position%5) if (final_position//5)%2 == 0 else final_position%5+6
    y_final = 10 - final_position // 5
    
    if new_current_map == 1 or new_current_map == 3:
        x_position += 5
    if new_current_map == 2 or new_current_map == 3:
        y_position += 5
    
    dist = abs(x_final - x_position) + abs(y_final - y_position)
    max_dist = 18
    progress = (1 - (dist / max_dist)) * 100
    
    return int(progress//1)

def new_map_animation(new_position, list_radar, list_life, position):
    np[position] = (0, 0, 0)
    for i in range(20):
        for radar in list_radar:
            np[radar] = (0, 0, i)
        for life in list_life:
            np[life] = (i, i//2, i//2)        
        np[new_position] = (i//4, i//4, i//4)        
        np.write()
        time.sleep(0.02)
        
    for i in range(20, -1, -1):
        for radar in list_radar:
            np[radar] = (0, 0, i)
        for life in list_life:
            np[life] = (i, i//2, i//2)                  
        np[new_position] = (5 + i//4, 5 + i//4, 5 + i//4)
        np.write()
        time.sleep(0.02)
    np[new_position] = (10, 10, 10)
    np.write()

def player_fade_in(position):
    for i in range(10):
        np[position] = (i, i, i)
        np.write()
        time.sleep(0.2)

async def get_radar_animation(position):
    np[position] = (0, 0, 0)
    np.write()
    for _ in range(3):
        np[position] = (0, 0, 10)
        np.write()
        await asyncio.sleep(0.2)
        np[position] = (0, 0, 0)
        np.write()
        await asyncio.sleep(0.2)
    np[position] = (10, 10, 10)
    np.write()

def extra_life_animation():
    for _ in range(3):
        for index, position in enumerate(heart):
            np[24-index] = (position//4, 0, 0)
        np.write()
        send_cmd('t2.pco=6371')
        send_cmd('t2.txt="MINI GAME"')
        time.sleep(0.5)
        for index in range(25):
            np[index] = (0, 0, 0)
        np.write()
        send_cmd('t2.txt=""')
        time.sleep(0.5)

def extra_life_game():
    meio = [22, 17, 12, 7, 2]
    np[12] = (10, 0, 0)
    extra_life_animation()
    oled.fill(0)
    oled.text(f"    Aperte B", 0, 20)
    oled.text(f"   e acerte o", 0, 30)
    oled.text(f"      alvo", 0, 40)
    oled.show()
    while True:
        for index in meio:
            if index == 12:
                np[index] = (50, 10, 40)
            else:
                np[index] = (10, 10, 10)
                np[12] = (10, 0, 0)
            np.write()
            time.sleep(0.2)
            if button_b.value() == 0:
                asyncio.run(game_main())
                if index == 12:
                    return True
                else:
                    return False
            np[index] = (0, 0, 0)
            np.write()
        for index in meio[::-1]:
            if index == 12:
                np[index] = (50, 10, 40)
            else:
                np[index] = (10, 10, 10)
                np[12] = (10, 0, 0)
            np.write()
            time.sleep(0.2)
            if button_b.value() == 0:
                asyncio.run(game_main())
                if index == 12:
                    return True
                else:
                    return False
            np[index] = (0, 0, 0)
            np.write()

def control_mpu(ax, ay, position):
    row_index, column_index = next(((index, row.index(position)) for index, row in enumerate(LED_MATRIZ) if position in row))
    if ax < -0.3 and position not in right_side:
        position = position - 1 if row_index % 2 == 0 else position + 1
    elif ax > 0.3 and position not in left_side:
        position = position - 1 if row_index % 2 == 1 else position + 1
    if ay < -0.3 and position not in top:
        position = LED_MATRIZ[row_index+1][column_index]
    if ay > 0.3 and position not in botton:
        position = LED_MATRIZ[row_index-1][column_index]
    
    return position

def send_cmd(cmd):
    uart.write(cmd.encode('utf-8') + b'\xff\xff\xff')
    
def new_image(id_: int, image: str = 'p1'):
    send_cmd(f'{image}.pic=6')
    send_cmd(f'{image}.pic={id_}')
    
def set_progress_bar(percent: int):
    send_cmd(f'j0.val={percent}')
    
def set_initial_display():
    send_cmd('p5.pic=20')
    send_cmd('p0.pic=20')
    send_cmd('p2.pic=20')
    send_cmd('p3.pic=22')
    send_cmd('p4.pic=22')
    send_cmd('p6.pic=22')
    send_cmd('p7.pic=26')
    send_cmd('p8.pic=26')
    send_cmd('p9.pic=22')
    send_cmd('p10.pic=22')
    send_cmd('p11.pic=22')
    send_cmd('p12.pic=22')
    send_cmd('p1.pic=25')
    send_cmd('p13.pic=37')
    send_cmd('t1.txt="MAPA"')
    send_cmd('t0.txt="Aperte A para iniciar"')
    send_cmd('j0.val=0')
    send_cmd('t2.txt=""')

async def damage_animation():
    new_image(id_=10)
    await asyncio.sleep(0.2)
    new_image(id_=7)
    await asyncio.sleep(0.2)
    new_image(id_=9)
    await asyncio.sleep(0.2)
    for _ in range(2):
        new_image(id_=8)
        await asyncio.sleep(0.2)
        new_image(id_=12)
        await asyncio.sleep(0.2)
        new_image(id_=11)
        await asyncio.sleep(0.2)

async def run_animation():
    for _ in range(2):
        new_image(id_=13)
        await asyncio.sleep(0.2)
        new_image(id_=14)
        await asyncio.sleep(0.2)
    new_image(id_=25)
    
async def radar_animation():
    for _ in range(3):
        new_image(id_=19)
        await asyncio.sleep(0.2)
        new_image(id_=18)
        await asyncio.sleep(0.2)
    new_image(id_=25)
    
async def mini_game_animation():
    new_image(id_=17)
    await asyncio.sleep(0.3)
    new_image(id_=16)
    await asyncio.sleep(0.3)
    new_image(id_=15)
    await asyncio.sleep(0.8)
    new_image(id_=25)
    
async def vida_animation():
    send_cmd('t2.pco=59392')
    for _ in range(3):
        send_cmd('t2.txt="+1 VIDA"')
        await asyncio.sleep(0.2)
        send_cmd('t2.txt=""')
        await asyncio.sleep(0.1)
    
async def life_animation():
    new_image(id_=31)
    await asyncio.sleep(0.2)
    new_image(id_=30)
    await asyncio.sleep(0.2)
    new_image(id_=29)
    await asyncio.sleep(0.2)
    new_image(id_=28)
    await asyncio.sleep(0.2)
    new_image(id_=27)
    await asyncio.sleep(0.2)
    new_image(id_=25)
    
async def win_animation():
    send_cmd('t2.txt="VITORIA!!"')
    for _ in range(2):
        new_image(id_=31)
        await asyncio.sleep(0.2)
        new_image(id_=30)
        await asyncio.sleep(0.2)
        new_image(id_=29)
        await asyncio.sleep(0.2)
        new_image(id_=28)
        await asyncio.sleep(0.2)
        new_image(id_=27)
        await asyncio.sleep(0.2)
    new_image(id_=25)

async def death_animation():
    send_cmd('t2.txt="GAME OVER"')
    for _ in range(4):
        new_image(id_=8)
        await asyncio.sleep(0.2)
        new_image(id_=12)
        await asyncio.sleep(0.2)
        new_image(id_=11)
        await asyncio.sleep(0.2)

async def run_main(position_, new_position):
    await asyncio.gather(run_animation(), set_position_animation(position_, new_position))
    
async def damage_main(position_, new_position):
    await asyncio.gather(damage_animation(), loss_life_animation(position_, new_position))

async def radar_main(position_):
    await asyncio.gather(radar_animation(), get_radar_animation(position_))
    
async def map_main():
    await asyncio.gather(run_animation())
    
async def win_main():
    await asyncio.gather(win_animation(), win())
    
async def game_main():
    await asyncio.gather(mini_game_animation())

async def life_main():
    await asyncio.gather(life_animation(), vida_animation())
    
async def gameover_main():
    await asyncio.gather(death_animation(), gameover())
# Texto inicial
oled.text("    Bem-vindo", 0, 0)
oled.text("       ao", 0, 10)
oled.text("     BitMaze", 0, 20)
oled.text(" botao 'A' para", 0, 40)
oled.text("     iniciar", 0, 50)
oled.show()

# Inicializações de variáveis do jogo
initial_position = 22
np[initial_position] = (10, 10, 10)
position = initial_position

# Quantidade máxima de uso do radar
radar_number = 2
new_radar_number = 2 # Usado para setar novo placar de radar
radar_images = ["p7", "p8", "p9", "p10", "p11", "p12"]
# Quantidade de vidas
health = 3
new_health = 3    # Usado para setar novo placar de vida
life_images = ["p5", "p0", "p2", "p3", "p4", "p6"]
# Mapa atual
current_map = 0
new_current_map = 0
map_images = ["36", "35", "34", "33"]

# Variável que indica se o jogo começou
start = False
for i in range(25):
    np[i] = (0, 0, 0)
np.write()

# Contador para colocar no display
c = 0
while True:
    # Espera botão A para começar o jogo
    while not start:
        if c == 0:
            led(0, 0, 0)
            oled.fill(0)
            oled.text("    Bem-vindo", 0, 0)
            oled.text("       ao", 0, 10)
            oled.text("     BitMaze", 0, 20)
            oled.text(" botao 'A' para", 0, 40)
            oled.text("     iniciar", 0, 50)
            oled.show()
            set_initial_display()
            c = 1
        if button_a.value() == 0:
            c = 0
            new_position = 22
            dict_obstacles, dict_radar, dict_life, final_position = create_map()
            new_map_animation(new_position, dict_radar[0], dict_life[0], position)
            start = True
            oled.fill(0)
            oled.text(f"Vidas: {new_health}", 0, 10)
            oled.text(f"Radar: {new_radar_number}", 0, 30)
            oled.text(f"Mapa atual: {new_current_map}", 0, 50)
            oled.show()
            send_cmd('t1.txt="MAPA  1/4"')
            send_cmd(f'p13.pic=36')
            send_cmd('t0.txt="Distancia ate chegada"')
        
    # Verifica fim de jogo
    if health <= 0:
        asyncio.run(gameover_main())
        position = set_new_position(position, 22)
        new_position = 22
        start = False
        radar_number = 2
        new_radar_number = 2
        health = 3
        new_health = 3
        current_map = 0
        new_current_map = 0

    # Verifica vitória
    if current_map == 3 and position == final_position:
        asyncio.run(win_main())
        position = set_new_position(position, 22)
        new_position = 22
        start = False
        radar_number = 2
        new_radar_number = 2
        health = 3
        new_health = 3
        current_map = 0
        new_current_map = 0
        led(0, 0, 0)
    
    # Leitura do joystick
    adc_y = 32400 - adc_y_pin.read_u16()
    adc_x = 32400 - adc_x_pin.read_u16()
    new_position = control_joystick(adc_x, adc_y, position)
    #print(f"\njoystick x: {adc_x}")
    #print(f"joystick y: {adc_y}")
    #print(f"position: {position}")
    
    # Verifica se o player quer ir para outra parte do mapa
    if find_position_oob(new_position):
        new_position = map_transition(position, new_position)
        asyncio.run(map_main())
        send_cmd(f"p13.pic={map_images[new_current_map]}")
        send_cmd(f't1.txt="MAPA  {new_current_map+1}/4"')
        new_map_animation(new_position, dict_radar[new_current_map], dict_life[new_current_map], position)
        position = set_new_position(position, new_position)

    # Aciona radar com botão B
    if button_b.value() == 0 and radar_number > 0:
        new_radar_number -= 1
        set_radar(position, dict_obstacles[new_current_map], dict_radar[new_current_map], dict_life[new_current_map], final_position, current_map)
        radar_id = radar_images[new_radar_number]
        for _ in range(2):
            send_cmd(f"{radar_id}.pic=22")
            time.sleep(0.1)
            send_cmd(f"{radar_id}.pic=26")
            time.sleep(0.15)
        send_cmd(f"{radar_id}.pic=22")

    # Verifica se a próxima posição está dentro da lista de obstáculos, lista de radares
    #ou lista de vidas por mapa, caso sim, realiza a ação
    if new_position not in dict_obstacles[new_current_map]:
        if position != new_position:
            asyncio.run(run_main(position, new_position))
            position = new_position
            percent = motor_intensity(position, final_position)
            set_progress_bar(percent)
    elif new_position:
        loss_life(position, new_position)
    if position in dict_radar[new_current_map]:
        new_radar_number += 1
        asyncio.run(radar_main(position))
        radar_id = radar_images[new_radar_number-1]
        send_cmd(f"{radar_id}.pic=26") 
        dict_radar[new_current_map].remove(position)
    elif position in dict_life[new_current_map]:
        if extra_life_game():
            asyncio.run(life_main())
            new_health += 1
            life_id = life_images[new_health-1]
            send_cmd(f"{life_id}.pic=20")
        else:
            send_cmd('t2.txt="Perdeu!"')
            time.sleep(2)
            send_cmd('t2.txt=""')
            send_cmd('t2.txt="mais sorte"')
            time.sleep(1)
            send_cmd('t2.txt=""')
            send_cmd('t2.txt="na proxima"')
            time.sleep(1)
            send_cmd('t2.txt=""')
        for i in range(25):
            np[i] = (0, 0, 0)
        player_fade_in(position)
        dict_life[new_current_map].remove(position)
        oled.fill(0)
        oled.text(f"Vidas: {new_health}", 0, 10)
        oled.text(f"Radar: {new_radar_number}", 0, 30)
        oled.text(f"Mapa atual: {new_current_map}", 0, 50)
        oled.show()
        
    #Atualiza variaveis do jogo e mostra no display
    if (new_radar_number != radar_number) or (new_health != health) or (new_current_map != current_map):
        # Atualiza display com status do jogo
        oled.fill(0)
        oled.text(f"Vidas: {new_health}", 0, 10)
        oled.text(f"Radar: {new_radar_number}", 0, 30)
        oled.text(f"Mapa atual: {new_current_map+1}", 0, 50)
        oled.show()
        radar_number = new_radar_number
        health = new_health
        current_map = new_current_map