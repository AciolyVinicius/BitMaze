# 🎮 BitMaze — Jogo Interativo com BitDogLab

BitMaze é um jogo interativo desenvolvido como projeto final da disciplina **EA801 – Sistemas Embarcados** da UNICAMP. O jogo utiliza o microcontrolador **BitDogLab**, integrando uma matriz de LEDs, joystick, botões, LED RGB, display OLED e display Nextion, formando um sistema completo de jogabilidade em tempo real com múltiplos mapas, radares, obstáculos e minijogos.

## 🧠 Equipe

- **Igor Origuela da Graça** — RA 199002  
- **Vinícius Acioly Elias da Silva** — RA 245220

## 🕹️ Funcionalidades

- Controle do personagem via **joystick analógico**
- **Labirinto gerado aleatoriamente**, com garantia de caminho até o destino
- Transições entre **4 blocos/matrizes** com mapa interconectado
- Sistema de **radar** que mostra perigos, vidas e radares próximos
- **Obstáculos** que reduzem vida ao serem tocados
- Coleta de **vidas extras** por meio de um **minigame de precisão**
- Display OLED para status do jogo
- Display Nextion com:
  - Animações do personagem (andar, dano, vitória, derrota)
  - Mapa atual, número de vidas e radares disponíveis
  - **Barra de progresso** indicando proximidade do ponto final
- LED RGB para indicar o resultado da partida:  
  - 🟢 **Verde**: vitória  
  - 🔴 **Vermelho**: derrota

## 📷 Fotos do Projeto

### Protótipo Montado
![Protótipo Montado](link-da-imagem-1)

### Jogo em Execução
![Jogo rodando](link-da-imagem-2)

### Radar Ativado
![Radar ativo](link-da-imagem-3)

### Minigame de Vida Extra
![Minigame](link-da-imagem-4)

> Substitua os `link-da-imagem` pelos links reais das suas imagens no GitHub ou em um serviço de hospedagem de imagens.

## 🧩 Componentes Utilizados

- Microcontrolador **BitDogLab**
- Matriz de LEDs 5x5
- Joystick analógico
- 2 botões (Radar / Minigame)
- LED RGB
- Display OLED via I2C
- Display **Nextion** (serial)
- Bibliotecas MicroPython compatíveis

## 📁 Organização do Repositório

