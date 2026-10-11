# Flying Bear Ghost 6 — Полная конфигурация Klipper (MKS Robin Nano V3.1 + Orange Pi Zero 2 + TMC2209 UART)

Готовая, протестированная и полностью рабочая конфигурация **Klipper** для 3D-принтера **Flying Bear Ghost 6** на базе связки:
* **Одноплатный компьютер**: Orange Pi Zero 2 (Allwinner H616, Armbian)
* **Материнская плата**: **Makerbase MKS Robin Nano V3.1 (ревизия с AliExpress)** на микроконтроллере **STM32F407VET6**
* **Драйверы шаговых двигателей**: **TMC2209 v2.0** по **UART** (все 4 оси: X, Y, Z, Extruder)
* **Экран и тачскрин**: ST7796S (SPI) + тачскрин XPT2046 / ADS7846 (KlipperScreen)
* **Датчики**: Магнитный/индуктивный датчик стола (Omron TL-Q5MC2) + датчик окончания филамента

---

## 💾 Готовый образ SD-карты (Скачать и записать)

Для быстрой установки собран полный побитовый образ системы со всеми драйверами, службами и калибровками.
* **[Скачать образ в разделе Releases](https://github.com/alexxttss/FlyingBear-Ghost-6-Klipper-Robin-Nano-V3.1/releases)**
* **Файлы:**
  * `orangepizero2_ghost6_armbian_full_backup_final.img.gz.part1`
  * `orangepizero2_ghost6_armbian_full_backup_final.img.gz.part2`
  * `orangepizero2_ghost6_armbian_full_backup_final.img.gz.sha256`

### Инструкция по записи образа:
1. Скачайте обе части архива в одну папку.
2. Объедините части в один файл:
   * **В Windows (Командная строка CMD):**
     ```cmd
     copy /b orangepizero2_ghost6_armbian_full_backup_final.img.gz.part1 + orangepizero2_ghost6_armbian_full_backup_final.img.gz.part2 orangepizero2_ghost6_armbian_full_backup_final.img.gz
     ```
   * **В Linux / macOS:**
     ```bash
     cat orangepizero2_ghost6_armbian_full_backup_final.img.gz.part* > orangepizero2_ghost6_armbian_full_backup_final.img.gz
     ```
3. Запишите полученный `.img.gz` файл на MicroSD карту (от 16 ГБ) с помощью **[BalenaEtcher](https://etcher.balena.io/)** или **Raspberry Pi Imager**.
4. Вставьте карту в Orange Pi Zero 2 и включите принтер — всё запустится автоматически.

---

## ⚙️ Особенности настройки драйверов TMC2209 v2.0 на MKS Robin Nano V3.1

### 1. Аппаратные перемычки UART
На плате Makerbase MKS Robin Nano V3.1 (AliExpress) под каждым слотом драйвера необходимо переставить джамперы в положение **UART** (замыкание соответствующих контактов UART согласно шелкографии платы).

### 2. Пины аппаратного UART (MKS Robin Nano V3.1)
В распространённых старых конфигах из сети часто указаны ложные пины слота E1 (`PA1`, `PD15`, `PA3`), из-за чего Klipper аварийно завершался с ошибкой:
`Unable to read tmc uart 'stepper_x' register IFCNT`.

На плате **MKS Robin Nano V3.1** аппаратные дорожки UART разведены жестко:
* **Драйвер X (UART TX/RX)**: `PD5`
* **Драйвер Y (UART TX/RX)**: `PD7`
* **Драйвер Z (UART TX/RX)**: `PD4`
* **Экструдер E0 (UART TX/RX)**: `PD9`

Конфигурация `tmc.cfg`:
```ini
[tmc2209 stepper_x]
uart_pin: PD5
run_current: 0.800
hold_current: 0.400

[tmc2209 stepper_y]
uart_pin: PD7
run_current: 0.800
hold_current: 0.400

[tmc2209 stepper_z]
uart_pin: PD4
run_current: 0.800
hold_current: 0.500

[tmc2209 extruder]
uart_pin: PD9
run_current: 0.600
hold_current: 0.200
```

### 3. Инверсия направления моторов (DIR Polarity)
При замене заводских драйверов Flying Bear (TMC2225 / A4988) на **TMC2209 v2.0** фазировка катушек и логика DIR инвертируется на 180°:
* Без исправления каретка X едет вправо в стенку вместо концевика слева, стол Z едет вниз на дно вместо сопла вверху.
* **Решение в `printer.cfg`:**
  * `[stepper_x]`: `dir_pin: PE2` (убран знак `!`)
  * `[stepper_y]`: `dir_pin: PB9` (убран знак `!`)
  * `[stepper_z]`: `dir_pin: PB4` (убран знак `!`)
  * `[extruder]`: `dir_pin: !PD3` (добавлен знак `!`)

---

## 📌 Полная карта пинов платы MKS Robin Nano V3.1 (AliExpress)

| Функция / Узел | Обозначение на плате | Пин MCU STM32F407 | Примечание |
|---|---|---|---|
| **Мотор X Step** | X-STEP | `PE3` | Шаг мотора X |
| **Мотор X Dir** | X-DIR | `PE2` | Направление (для TMC2209 прямой) |
| **Мотор X Enable** | X-EN | `!PE4` | Включение драйвера X |
| **Мотор X UART** | X-UART | `PD5` | Опрос регистров TMC2209 |
| **Концевик X** | J11 (X) | `!PA15` | Механический микрик слева |
| **Мотор Y Step** | Y-STEP | `PE0` | Шаг мотора Y |
| **Мотор Y Dir** | Y-DIR | `PB9` | Направление (для TMC2209 прямой) |
| **Мотор Y Enable** | Y-EN | `!PE1` | Включение драйвера Y |
| **Мотор Y UART** | Y-UART | `PD7` | Опрос регистров TMC2209 |
| **Концевик Y** | J12 (Y) | `!PD2` | Механический микрик спереди |
| **Мотор Z Step** | Z1-STEP | `PB5` | Шаг винта Z |
| **Мотор Z Dir** | Z1-DIR | `PB4` | Направление (для TMC2209 прямой, подъем вверх) |
| **Мотор Z Enable** | Z1-EN | `!PB8` | Включение драйвера Z |
| **Мотор Z UART** | Z1-UART | `PD4` | Опрос регистров TMC2209 |
| **Датчик уровня стола (Probe)** | J13 (Z−) | `^PC8` | Индуктивный/магнитный датчик (Omron) |
| **Верхний концевик Z+** | J14 (Z+) | `PC4` | Оптический верхний концевик (если задействован) |
| **Мотор Extruder Step** | E0-STEP | `PD6` | Шаг фидера экструдера |
| **Мотор Extruder Dir** | E0-DIR | `!PD3` | Направление подачи филамента вперед |
| **Мотор Extruder Enable** | E0-EN | `!PB3` | Включение драйвера E0 |
| **Мотор Extruder UART** | E0-UART | `PD9` | Опрос регистров TMC2209 |
| **Датчик филамента** | J54 (MT_DET1) | `^!PA4` | Подтяжка pull-up с инверсией |
| **Нагреватель хотэнда** | HE0 | `PE5` | Мосфет картриджа нагревателя |
| **Термистор хотэнда** | TH1 | `PC1` | NTC 100K (Generic 3950) |
| **Нагреватель стола** | H-BED | `PA0` | Мосфет грелки стола |
| **Термистор стола** | TB | `PC0` | NTC 100K (EPCOS 100K B57560G104F) |
| **Вентилятор обдува детали** | FAN1 | `PC14` | Управляемый ШИМ вентилятор улитки |
| **Вентилятор хотэнда** | FAN2 | `PB1` | Авто-включение при T > 50°C |
| **Зуммер / Beeper** | BEEPER | `PC5` | Звуковой сигнал завершения/паузы |

---

## 📐 Калибровка датчика стола и сетка `[bed_mesh]`

Магнитный датчик стола смонтирован со смещением относительно сопла:
* `x_offset: -15.0` (на 15 мм левее сопла)
* `y_offset: 20.0` (на 20 мм сзади сопла)

### Безопасные границы сетки стола:
Глубина стола Flying Bear Ghost 6 составляет 210 мм.  
Чтобы датчик не вылетал за пределы металлического листа сзади принтера (что вызывало ошибку `No trigger on probe after full movement`), границы сетки настроены с запасом:
```ini
[bed_mesh]
speed: 100
horizontal_move_z: 5
mesh_min: 20.0, 25.0    # Безопасный отступ от переднего и левого края
mesh_max: 220.0, 185.0   # Запас 25 мм от заднего среза стола
probe_count: 5, 5        # Сетка 5x5 точек
algorithm: bicubic
```

---

## 🖥️ Экран ST7796S и тачскрин ADS7846 (Orange Pi Zero 2)

В Armbian на Allwinner H616 тачскрин ADS7846 / XPT2046 при работе X11 склонен терять прерывания из-за отсутствия физической подтяжки на пинах SPI1/GPIO.  
В образе применены проверенные решения:
1. **Device Tree Overlay** (`sun50i-h616-st7796s.dts`): правильная адресация шины SPI1 и прерываний IRQ.
2. **Аппаратная подтяжка линии PENIRQ** (`touch-pullup.service`): скрипт активирует встроенный pull-up регистр чипа Allwinner H616 на старте системы.
3. **Автоматический сторожевой таймер** (`touch-watchdog.service`): фоновый демон отслеживает шину ввода и мгновенно перезапускает драйвер в случае зависания прерываний, обеспечивая 100% стабильность сенсора.
