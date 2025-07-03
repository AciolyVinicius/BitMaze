# 🎮 BitMaze — Jogo Interativo com BitDogLab

## 📝 Descrição

BitMaze é um jogo eletrônico desenvolvido em MicroPython para microcontroladores, que utiliza uma **matriz de LEDs NeoPixel 5x5**, joystick analógico, botões físicos e um display OLED para criar uma experiência interativa e dinâmica.

O jogador controla um personagem (player) que navega por diversos mapas interconectados, evitando obstáculos, coletando itens como radar e vidas extras, e precisa alcançar a posição final para vencer o desafio.

---

## ⚙️ Funcionalidades Principais

- 🎯 Controle preciso do player via joystick analógico.
- 🗺️ Navegação por múltiplos mapas interconectados.
- 💥 Obstáculos aleatórios que podem causar perda de vidas.
- 📡 Itens de radar que revelam áreas próximas no mapa.
- ❤️ Itens de vida extra e mini-jogos para ganhar mais vidas.
- 🔴 Indicadores visuais com LED RGB e display OLED.
- 🎨 Animações fluídas para movimento, dano, radar e vitória.
- 🔌 Comunicação UART para controle do display Nextion.

---

## 🛠️ Estrutura do Projeto

- Configuração e inicialização do hardware (GPIO, ADC, PWM, UART, I2C).
- Implementação da lógica dos mapas, movimentação e colisões.
- Gerenciamento da jogabilidade: vidas, itens e condições de vitória/derrota.
- Animações assíncronas usando `uasyncio` para maior fluidez.
- Envio de comandos para display Nextion via UART.
- Sincronismo entre BitDogLab e Nextion.
- Funções auxiliares para geração e manipulação dos mapas e LEDs.

---

## 🔧 Requisitos de Hardware

| Componente                    | Descrição                         | Conexão                    |
|------------------------------|---------------------------------|----------------------------|
| Microcontrolador              | Suporte a MicroPython            | Exemplo: Raspberry Pi Pico  |
| Matriz NeoPixel 5x5           | LEDs RGB controláveis            | Pino 7                      |
| Joystick analógico           | Controle de direção              | ADC pinos 26 (X), 27 (Y)   |
| Botões físicos               | Entrada de comandos (A e B)      | Pinos 5 e 6 (pull-up)      |
| LED RGB                      | Indicador visual                 | PWM nos pinos 11 (G), 12 (R), 13 (B) |
| Display OLED SSD1306         | Exibição de status               | I2C (pinos 14 - SDA, 15 - SCL) |
| UART para Display Nextion    | Comunicação serial               | Pinos 16 (TX), 17 (RX)     |

---

## 🚀 Como Executar

1. Monte o hardware conforme as conexões indicadas acima.
2. Copie o arquivo `ProjetoFinal_BitMaze.py` para seu microcontrolador.
3. Acesse o terminal REPL do MicroPython.
4. Execute o script para iniciar o jogo.
5. Pressione o botão **A** para iniciar.
6. Use o joystick para movimentar o player pelo mapa.
7. Pressione o botão **B** para ativar o radar quando disponível.
8. Evite obstáculos, colete itens e alcance a meta para vencer.

---

## 💡 Possíveis Melhorias Futuras

- Calibração avançada do joystick e sensores.
- Expansão dos mini-jogos para maior variedade.
- Inclusão de som e feedback tátil (vibração).
- Mais mapas e níveis de dificuldade progressiva.
- Melhorias na interface do display Nextion.

---

## 👤 Autoria

Desenvolvido por Igor Origuela da Graça e Vinícius Acioly Elias da Silva para trabalho acadêmico no curso de Engenharia Elétrica da Unicamp - EA801.

---

## 📷 Fotos do Projeto

### Protótipo Montado
![image](https://github.com/user-attachments/assets/e82e4cfa-05a3-4e90-a87f-07cf523ee123)

### Jogo no Display Nextion
![image](https://github.com/user-attachments/assets/ebd44c9e-1343-423f-bf6d-69ba3f40bd1d)


### Controle BitDogLab
![image](https://github.com/user-attachments/assets/24a5f90d-821a-43cd-b7bc-8fc06602c2c0)



✨ Obrigado por conferir o BitMaze! Divirta-se jogando e explorando o código! ✨

