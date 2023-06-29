;  ___           _        __ ___  __ ___
; / __|_ _  __ _| |_____ / /| __|/  \_  )
; \__ \ ' \/ _` | / / -_) _ \__ \ () / /
; |___/_||_\__,_|_\_\___\___/___/\__/___|

; Change direction: W A S D

define appleL         $00 ; screen location of apple, low byte
define appleH         $01 ; screen location of apple, high byte
define snakeHeadL     $10 ; screen location of snake head, low byte
define snakeHeadH     $11 ; screen location of snake head, high byte
define snakeBodyStart $12 ; start of snake body byte pairs
define snakeDirection $02 ; direction (possible values are below)
define snakeLength    $03 ; snake length, in bytes

; Directions (each using a separate bit)
define movingUp      1
define movingRight   2
define movingDown    4
define movingLeft    8

; ASCII values of keys controlling the snake
define ASCII_w      $77
define ASCII_a      $61
define ASCII_s      $73
define ASCII_d      $64

; System variables
define sysRandom    $fe
define sysLastKey   $ff


  JSR init
  JSR loop

init:
  JSR initSnake
  JSR generateApplePosition
  RTS


initSnake:
  LDA #movingRight  ;start direction
  STA snakeDirection

  LDA #4  ;start length (2 segments)
  STA snakeLength
  
  LDA #$11
  STA snakeHeadL
  
  LDA #$10
  STA snakeBodyStart
  
  LDA #$0f
  STA $14 ; body segment 1
  
  LDA #$04
  STA snakeHeadH
  STA $13 ; body segment 1
  STA $15 ; body segment 2
  RTS


generateApplePosition:
  ;load a new random byte into $00
  LDA sysRandom
  STA appleL

  ;load a new random number from 2 to 5 into $01
  LDA sysRandom
  AND #$03 ;mask out lowest 2 bits
  CLC
  ADC #2
  STA appleH

  RTS


loop:
  JSR readKeys
  JSR checkCollision
  JSR updateSnake
  JSR drawApple
  JSR drawSnake
  JSR spinWheels
  JMP loop


readKeys:
  LDA sysLastKey
  CMP #ASCII_w
  BEQ upKey
  CMP #ASCII_d
  BEQ rightKey
  CMP #ASCII_s
  BEQ downKey
  CMP #ASCII_a
  BEQ leftKey
  RTS
upKey:
  LDA #movingDown
  BIT snakeDirection
  BNE illegalMove

  LDA #movingUp
  STA snakeDirection
  RTS
rightKey:
  LDA #movingLeft
  BIT snakeDirection
  BNE illegalMove

  LDA #movingRight
  STA snakeDirection
  RTS
downKey:
  LDA #movingUp
  BIT snakeDirection
  BNE illegalMove

  LDA #movingDown
  STA snakeDirection
  RTS
leftKey:
  LDA #movingRight
  BIT snakeDirection
  BNE illegalMove

  LDA #movingLeft
  STA snakeDirection
  RTS
illegalMove:
  RTS


checkCollision:
  JSR checkAppleCollision
  JSR checkSnakeCollision
  RTS


checkAppleCollision:
  LDA appleL
  CMP snakeHeadL
  BNE doneCheckingAppleCollision
  LDA appleH
  CMP snakeHeadH
  BNE doneCheckingAppleCollision

  ;eat apple
  INC snakeLength
  INC snakeLength ;increase length
  JSR generateApplePosition
doneCheckingAppleCollision:
  RTS


checkSnakeCollision:
  LDX #2 ;start with second segment
snakeCollisionLoop:
  LDA snakeHeadL,x
  CMP snakeHeadL
  BNE continueCollisionLoop

maybeCollided:
  LDA snakeHeadH,x
  CMP snakeHeadH
  BEQ didCollide

continueCollisionLoop:
  INX
  INX
  CPX snakeLength          ;got to last section with no collision
  BEQ didntCollide
  JMP snakeCollisionLoop

didCollide:
  JMP gameOver
didntCollide:
  RTS


updateSnake:
  LDX snakeLength
  DEX
  TXA
updateloop:
  LDA snakeHeadL,x
  STA snakeBodyStart,x
  DEX
  BPL updateloop

  LDA snakeDirection
  LSR
  BCS up
  LSR
  BCS right
  LSR
  BCS down
  LSR
  BCS left
up:
  LDA snakeHeadL
  SEC
  SBC #$20
  STA snakeHeadL
  BCC upup
  RTS
upup:
  DEC snakeHeadH
  LDA #$1
  CMP snakeHeadH
  BEQ collision
  RTS
right:
  INC snakeHeadL
  LDA #$1f
  BIT snakeHeadL
  BEQ collision
  RTS
down:
  LDA snakeHeadL
  CLC
  ADC #$20
  STA snakeHeadL
  BCS downdown
  RTS
downdown:
  INC snakeHeadH
  LDA #$6
  CMP snakeHeadH
  BEQ collision
  RTS
left:
  DEC snakeHeadL
  LDA snakeHeadL
  AND #$1f
  CMP #$1f
  BEQ collision
  RTS
collision:
  JMP gameOver


drawApple:
  LDY #0
  LDA sysRandom
  STA (appleL),y
  RTS


drawSnake:
  LDX snakeLength
  LDA #0
  STA (snakeHeadL,x) ; erase end of tail

  LDX #0
  LDA #1
  STA (snakeHeadL,x) ; paint head
  RTS


spinWheels:
  LDX #0
spinloop:
  NOP
  NOP
  DEX
  BNE spinloop
  RTS


gameOver:
