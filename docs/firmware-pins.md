# RV1106G2 pins on MujinaControl-S19: what each one does

For bringing up Linux and Mujina on this board. Generated on 2026-11-16 from the schematic netlist (`build/MujinaControl-S19/fwdoc/gen.py`); every pin-to-net entry below was checked against it. It describes the hardware as drawn. **Nothing here has run on a board yet**: no MujinaControl-S19 has been built, and the device-tree fragments are starting points, not tested code.

Conventions:
- **SoC pin** is the QFN-128 contact number.
- **GPIO** is the Rockchip name; in brackets the Linux controller and line (`gpio1 line 22` = `<&gpio1 RK_PC6 ...>` in a device tree, `gpiochip1` line 22 in libgpiod if the chips enumerate in order) and the legacy global number (bank × 32 + line).
- **Level** is the I/O voltage of the pin. Most are 3.3 V; the pins on the camera bank are **1.8 V and not 3.3 V tolerant**.
- Mux group names (`uart1m0_xfer` and so on) were checked against `rv1106-pinctrl.dtsi` in the Luckfox SDK kernel kept in `research/rv1106/software/luckfox-sdk/`. Node labels (`&sdio`, `&sfc`, ...) are from that kernel's `rv1106.dtsi`; a mainline kernel may name them differently.

## At a glance

| Function | Controller | Pin group / GPIO | Connector or part |
|---|---|---|---|
| Console | UART2 | `uart2m1_xfer` | J16: 1 TX, 2 GND, 3 RX; 3.3 V |
| Boot flash | FSPI (`&sfc`) | `fspi_pins`, `fspi_cs0` | U130 W25N02KVZEIR, 2 Gbit SPI NAND |
| microSD | SDMMC0 (`&sdmmc`) | `sdmmc0_clk`, `sdmmc0_cmd`, `sdmmc0_bus4`, `sdmmc0_det` | J101 |
| Ethernet | GMAC with internal PHY (`&gmac`, `&rmii_phy`) | dedicated pins | J100, 10/100 |
| USB | USB 2.0 OTG (`&usbdrd_dwc3`, `&u2phy`) | dedicated pins | J2 USB-C, device only |
| Hashboard 0 UART | UART1 | `uart1m0_xfer` | J3 |
| Hashboard 1 UART | UART3 | `uart3m0_xfer` | J4 |
| Hashboard 2 UART | UART4 | `uart4m0_xfer` | J5 |
| Hashboard I²C (shared) | I2C0 | `i2c0m1_xfer` | J3, J4, J5 |
| Hashboard reset, plug detect, power enable | GPIO | see Hashboards | J3, J4, J5; U150–U152 |
| Fan PWM 1 / 2 / 3 / 4 | PWM0 / PWM2 / PWM3 / PWM1 | `pwm0m0_pins`, `pwm2m0_pins`, `pwm3m0_pins`, `pwm1m0_pins` | fan connectors, inverted |
| Fan tach 1–4 | GPIO edge counting | GPIO3_C4, C5, C6 (1.8 V), GPIO1_D0 | fan connectors |
| PSU I²C and enable | I2C1, GPIO | `i2c1m0_xfer`, GPIO2_A4 | J10 |
| WiFi | SDMMC1 (`&sdio`), GPIO, RTC clock output | `sdmmc1m1_clk`, `sdmmc1m1_cmd`, `sdmmc1m1_bus4`, `rtc_pins` | U160 AP6212 |
| Accessory header | I2C4, GPIO | `i2c4m0_xfer`, GPIO4_A7, GPIO3_C7–D3 | J15 (not fitted) |
| LEDs | GPIO | GPIO2_A5, GPIO1_D3, GPIO1_D2 | D100, jack LEDs |
| Buttons | nPOR, SARADC_IN0 | dedicated pins | SW1 RESET, SW2 BOOT |

## Power, I/O voltages and clocks

There is no PMIC. Six fixed buck regulators come up in sequence under five supervisors and the SoC is released from reset last. Firmware cannot change any rail, so there is nothing to configure, but three things follow:

- **CPU rail is fixed at 0.9 V** (`+0V9_CPU`, pin 115). Do not give the CPU a regulator in the device tree, and remove or disable operating points that need more than 0.9 V. In the Luckfox SDK's table the points up to 1296 MHz ask for 0.85–0.875 V; the 1608 MHz point asks for 1.0 V and must not be used. Check the points in between in the kernel you build.
- **DDR** is the 128 MB DDR3L inside the RV1106G2, on 1.35 V. Use the vendor DDR init for RV1106G2.
- **RTC** has its 32.768 kHz crystal but no backup battery: the clock does not survive power loss. The RTC also supplies the 32.768 kHz clock for the WiFi module (see WiFi).

| I/O supply pin | Rail | Pins it powers on this board |
|---|---|---|
| 61 PMU_VCC3V3 | +3V3 | GPIO0_A0–A6 (pins 58–65): WiFi clock and enable, fan PWM 2–4, PSU I²C |
| 81 GPIO1_VCC3V3 | +3V3 | GPIO1_A / B (pins 72–80): hashboard UARTs, fan 1 PWM, console |
| 88 GPIO6_VCC | +3V3 | GPIO1_C / D (pins 83–95): hashboard power enables, Ethernet LEDs, fan 4 tach, WiFi SDIO |
| 108 GPIO5_VCC | +3V3 | GPIO2_A / B (pins 104–114): hashboard reset and plug detect, accessory I²C, PSU enable, status LED |
| 43 GPIO3_VCC | +3V3 | GPIO4_A / B (pins 38–48): SPI NAND, hashboard I²C, WiFi host wake, one accessory GPIO |
| 13 GPIO4_VCC | +3V3 | GPIO3_A (pins 11–18): microSD |
| 1 MIPI_AVDD1V8 / GPIO7_VCC1V8 | +1V8 | GPIO3_B / C / D (pins 2–9, 117–128): fan tach 1–3, five accessory GPIOs, unused camera inputs |

Which pins belong to which supply pin follows the Rockchip pin table; on this board every domain except the camera one is tied to the same 3.3 V rail. If the kernel has an I/O-domain node for the RV1106, set every domain to 3.3 V except the camera domain (pin 1), which is 1.8 V. The microSD bank is hard-wired to 3.3 V, so the card cannot switch to 1.8 V signalling: use `no-1-8-v`.

Clocks: 24 MHz crystal on OSC_XIN / OSC_XOUT (pins 68, 69); 32.768 kHz crystal on RTC_XIN / RTC_XOUT (pins 21, 20).

## Reset and boot

| Net | SoC pin | Pin | On the board |
|---|---|---|---|
| RESET_N | 66 | nPOR | power-on reset, low = reset: supervisor chain U120–U124, RESET button SW1, 10k pull-up, 10 nF |
| BOOT_ADC | 23 | SARADC_IN0 | BOOT button SW2: 10k pull-up to +1V8, button to ground through 100 Ω |

- **RESET** (SW1) pulls nPOR low. The supervisors also hold it low until every rail is good.
- **BOOT** (SW2) pulls SARADC_IN0 to about 18 mV; released it sits at 1.8 V. Holding it while releasing RESET (or applying power) is the usual Rockchip way into maskrom / USB download mode. In Linux it can be an `adc-keys` button on `saradc` channel 0 with a 1.8 V reference.
- **Boot media**: the SPI NAND on FSPI and the microSD on SDMMC0. A bootable NAND is tried before the card. There is no eMMC.
- **USB recovery needs 12 V**: the USB-C port does not power the board; VBUS is only sensed.

## Storage

| Net | SoC pin | GPIO | Function to select | Level | On the board |
|---|---|---|---|---|---|
| FSPI_CS_N | 47 | GPIO4_B0 (gpio4 line 8, no. 136) | FSPI_CS0 | 3.3 V | SPI NAND chip select; 10k pull-up |
| FSPI_CLK_SOC | 48 | GPIO4_B1 (gpio4 line 9, no. 137) | FSPI_CLK | 3.3 V | 22 Ω series at the SoC |
| FSPI_D0 | 41 | GPIO4_A4 (gpio4 line 4, no. 132) | FSPI_D0 | 3.3 V |  |
| FSPI_D1 | 42 | GPIO4_A3 (gpio4 line 3, no. 131) | FSPI_D1 | 3.3 V |  |
| FSPI_D2 | 44 | GPIO4_A2 (gpio4 line 2, no. 130) | FSPI_D2 | 3.3 V | 10k pull-up (WP#) |
| FSPI_D3 | 39 | GPIO4_A6 (gpio4 line 6, no. 134) | FSPI_D3 | 3.3 V | 10k pull-up (HOLD#) |
| SD_CLK_SOC | 15 | GPIO3_A4 (gpio3 line 4, no. 100) | SDMMC0_CLK | 3.3 V | 22 Ω series at the SoC |
| SD_CMD | 16 | GPIO3_A5 (gpio3 line 5, no. 101) | SDMMC0_CMD | 3.3 V | 10k pull-up |
| SD_D0 | 14 | GPIO3_A3 (gpio3 line 3, no. 99) | SDMMC0_D0 | 3.3 V | 10k pull-up |
| SD_D1 | 12 | GPIO3_A2 (gpio3 line 2, no. 98) | SDMMC0_D1 | 3.3 V | 10k pull-up |
| SD_D2 | 18 | GPIO3_A7 (gpio3 line 7, no. 103) | SDMMC0_D2 | 3.3 V | 10k pull-up |
| SD_D3 | 17 | GPIO3_A6 (gpio3 line 6, no. 102) | SDMMC0_D3 | 3.3 V | 10k pull-up |
| SD_DET_N | 11 | GPIO3_A1 (gpio3 line 1, no. 97) | SDMMC0_DET | 3.3 V | card detect, low = card present; 10k pull-up |

- NAND: Winbond W25N02KVZEIR, 2 Gbit (256 MB) SPI NAND, quad capable, 3.3 V, following the Luckfox Pico Pro / Max (`compatible = "spi-nand"` under `&sfc`).
- microSD: 4-bit, 3.3 V only, card detect on the dedicated SDMMC0_DET pin (low = card in).

## Console

| Net | SoC pin | GPIO | Function to select | Level | On the board |
|---|---|---|---|---|---|
| DEBUG_TX | 79 | GPIO1_B2 (gpio1 line 10, no. 42) | UART2_TX_M1 | 3.3 V | J16 pin 1 |
| DEBUG_RX | 80 | GPIO1_B3 (gpio1 line 11, no. 43) | UART2_RX_M1 | 3.3 V | J16 pin 3; 10k pull-up |

J16 is a 1×3 2.54 mm header: pin 1 = TX (from the SoC), pin 2 = ground, pin 3 = RX (into the SoC). 3.3 V levels. UART2 in its M1 position is the Rockchip default console; the Luckfox SDK runs it at 115200 8N1 through `fiq_debugger` (`rockchip,serial-id = <2>`).

## Ethernet

| Net | SoC pin | Pin | On the board |
|---|---|---|---|
| ETH_TX_P | 100 | ETH_PHY_TXP | internal 100BASE-TX PHY, to the jack through 0 Ω and ESD diode |
| ETH_TX_N | 99 | ETH_PHY_TXN |  |
| ETH_RX_P | 98 | ETH_PHY_RXP |  |
| ETH_RX_N | 97 | ETH_PHY_RXN |  |
| ETH_BIAS | 102 | ETH_EXTR | 6.04 kΩ bias resistor to ground |

| Net | SoC pin | GPIO | Function to select | Level | On the board |
|---|---|---|---|---|---|
| ETH_LED_LINK | 85 | GPIO1_D3 (gpio1 line 27, no. 59) | GPIO out | 3.3 V | jack green LED (left) through 510 Ω, high = lit |
| ETH_LED_SPEED | 86 | GPIO1_D2 (gpio1 line 26, no. 58) | GPIO out | 3.3 V | jack yellow LED (right) through 510 Ω, high = lit |

- 10/100 through the SoC's internal PHY (`&gmac` with `&rmii_phy`, `phy-is-integrated`) and the magnetics inside the jack. No external PHY, no MDIO pins, no PHY reset GPIO.
- The two jack LEDs are plain GPIOs, not PHY LED outputs: drive them from Linux (for example `gpio-leds` with a `netdev` trigger). Link is the green LED on the left seen from the front, speed the yellow one on the right. Both light when the GPIO is high.
- The MAC address has to come from firmware (there is no EEPROM for it on the board).

## USB

| Net | SoC pin | Pin | On the board |
|---|---|---|---|
| USB_DP_SOC | 27 | USB_DP | USB-C J2 through 2.2 Ω |
| USB_DM_SOC | 26 | USB_DM | USB-C J2 through 2.2 Ω |
| USB_VBUS_DET | 25 | USB_VBUSDET | VBUS through 12.4k / 18k divider (about 2.96 V at 5 V) |

USB-C receptacle J2, USB 2.0, **device only** (`dr_mode = "peripheral"`): both CC pins have 5.1 kΩ pull-downs and nothing can supply VBUS. Used for maskrom / recovery download and, if wanted, a gadget (serial, RNDIS, ADB).

## Hashboards

Three ports, J3 (hashboard 0), J4 (1), J5 (2). Each has its own UART; all three share one I²C bus.

**Port 0 (J3)**

| Net | SoC pin | GPIO | Function to select | Level | On the board |
|---|---|---|---|---|---|
| HB0_TX | 75 | GPIO1_A3 (gpio1 line 3, no. 35) | UART1_TX_M0 | 3.3 V | J3 pin 11 |
| HB0_RX | 76 | GPIO1_A4 (gpio1 line 4, no. 36) | UART1_RX_M0 | 3.3 V | J3 pin 12 |
| HB0_RST_N | 104 | GPIO2_B1 (gpio2 line 9, no. 73) | GPIO out | 3.3 V | J3 pin 15; 100k pull-down |
| HB0_PLUG | 107 | GPIO2_A6 (gpio2 line 6, no. 70) | GPIO in | 3.3 V | J3 pin 5; 4.7k pull-down |
| HB0_PWR_EN | 83 | GPIO1_C6 (gpio1 line 22, no. 54) | GPIO out | 3.3 V | U150 ON; 4.7k pull-up |

**Port 1 (J4)**

| Net | SoC pin | GPIO | Function to select | Level | On the board |
|---|---|---|---|---|---|
| HB1_TX | 72 | GPIO1_A0 (gpio1 line 0, no. 32) | UART3_TX_M0 | 3.3 V | J4 pin 11 |
| HB1_RX | 73 | GPIO1_A1 (gpio1 line 1, no. 33) | UART3_RX_M0 | 3.3 V | J4 pin 12 |
| HB1_RST_N | 105 | GPIO2_B0 (gpio2 line 8, no. 72) | GPIO out | 3.3 V | J4 pin 15; 100k pull-down |
| HB1_PLUG | 111 | GPIO2_A2 (gpio2 line 2, no. 66) | GPIO in | 3.3 V | J4 pin 5; 4.7k pull-down |
| HB1_PWR_EN | 84 | GPIO1_C7 (gpio1 line 23, no. 55) | GPIO out | 3.3 V | U151 ON; 4.7k pull-up |

**Port 2 (J5)**

| Net | SoC pin | GPIO | Function to select | Level | On the board |
|---|---|---|---|---|---|
| HB2_TX | 78 | GPIO1_B1 (gpio1 line 9, no. 41) | UART4_TX_M0 | 3.3 V | J5 pin 11 |
| HB2_RX | 77 | GPIO1_B0 (gpio1 line 8, no. 40) | UART4_RX_M0 | 3.3 V | J5 pin 12 |
| HB2_RST_N | 106 | GPIO2_A7 (gpio2 line 7, no. 71) | GPIO out | 3.3 V | J5 pin 15; 100k pull-down |
| HB2_PLUG | 112 | GPIO2_A3 (gpio2 line 3, no. 67) | GPIO in | 3.3 V | J5 pin 5; 4.7k pull-down |
| HB2_PWR_EN | 87 | GPIO1_D1 (gpio1 line 25, no. 57) | GPIO out | 3.3 V | U152 ON; 4.7k pull-up |

**Shared I²C**

| Net | SoC pin | GPIO | Function to select | Level | On the board |
|---|---|---|---|---|---|
| HB_SCL | 45 | GPIO4_A1 (gpio4 line 1, no. 129) | I2C0_SCL_M1 | 3.3 V | J3 / J4 / J5 pin 4; 4.7k pull-up to +3V3 |
| HB_SDA | 46 | GPIO4_A0 (gpio4 line 0, no. 128) | I2C0_SDA_M1 | 3.3 V | J3 / J4 / J5 pin 3; 4.7k pull-up to +3V3 |

Connector pinout (2×9, 2 mm), the same on all three:

| Pin | Signal | Pin | Signal |
|---|---|---|---|
| 1 | GND | 2 | GND |
| 3 | HB_SDA | 4 | HB_SCL |
| 5 | HBn_PLUG | 6 | address bit 2 |
| 7 | address bit 1 | 8 | address bit 0 |
| 9 | GND | 10 | GND |
| 11 | HBn_TX | 12 | HBn_RX |
| 13 | GND | 14 | GND |
| 15 | HBn_RST_N | 16 | HBn_3V3 |
| 17 | not connected | 18 | not connected |

What firmware needs to know:
- **Power enable** (HBn_PWR_EN) switches that port's 3.3 V logic supply (HBn_3V3, connector pin 16) through a TPS22919 load switch. High = on. A 4.7 kΩ pull-up makes each port **on by default** from power-up, before firmware runs. Set the output value before switching the pin to output.
- **Reset** (HBn_RST_N) is active low. A 100 kΩ pull-down holds each hashboard in reset until firmware drives the line high.
- **Plug detect** (HBn_PLUG) has a 4.7 kΩ pull-down on this board, so it reads low with nothing plugged; the hashboard is expected to pull it high. That polarity follows the Braiins BCB100 and has not been confirmed on a real S19 hashboard.
- **UART** lines have 4.7 kΩ pull-ups to the port's switched 3.3 V. Before switching a port off, stop its UART and leave TX low or high-impedance, and hold reset low, so the hashboard is not fed through its signal pins.
- **I²C** pull-ups (4.7 kΩ) go to the always-on +3V3, so a switched-off port still sees the bus pull-ups.
- **Address bits**: connector pins 8, 7, 6 are address-select straps (the hashboard EEPROM address pins on S19 boards, as on the Braiins BCB100), set differently per port so the three hashboards can share the bus: port 0 = 000 (bits 2, 1, 0); port 1 = 001 (bits 2, 1, 0); port 2 = 010 (bits 2, 1, 0). Each bit has a pull-up position to the port's 3.3 V and a pull-down position; one of the two is fitted.
- Baud rate and protocol are the hashboard's (BM13xx chain); the board only provides 3.3 V UARTs.

## Fans

| Net | SoC pin | GPIO | Function to select | Level | On the board |
|---|---|---|---|---|---|
| FAN1_PWM | 74 | GPIO1_A2 (gpio1 line 2, no. 34) | PWM0_M0 | 3.3 V | through 1k to Q2 (inverts) |
| FAN2_PWM | 59 | GPIO0_A1 (gpio0 line 1, no. 1) | PWM2_M0 | 3.3 V | through 1k to Q3 (inverts) |
| FAN3_PWM | 60 | GPIO0_A2 (gpio0 line 2, no. 2) | PWM3_IR_M0 | 3.3 V | through 1k to Q4 (inverts) |
| FAN4_PWM | 63 | GPIO0_A4 (gpio0 line 4, no. 4) | PWM1_M0 | 3.3 V | through 1k to Q5 (inverts) |
| FAN1_TACH | 2 | GPIO3_C4 (gpio3 line 20, no. 116) | GPIO in (edge count) | 1.8 V | 10k series; fan side pulled up to +1V8 |
| FAN2_TACH | 3 | GPIO3_C5 (gpio3 line 21, no. 117) | GPIO in (edge count) | 1.8 V | 10k series; fan side pulled up to +1V8 |
| FAN3_TACH | 4 | GPIO3_C6 (gpio3 line 22, no. 118) | GPIO in (edge count) | 1.8 V | 10k series; fan side pulled up to +1V8 |
| FAN4_TACH | 89 | GPIO1_D0 (gpio1 line 24, no. 56) | GPIO in (edge count) | 3.3 V | 10k series; fan side pulled up to +3V3 |

- **PWM is inverted.** Each PWM pin drives the gate of an N-MOSFET (1 kΩ series, 100 kΩ gate pull-down) whose open drain is the fan's PWM wire. SoC pin high = fan PWM wire pulled low. Either set inverted polarity on the PWM (`PWM_POLARITY_INVERTED`) or program duty = 100 % − wanted fan duty.
- **Fail-safe**: with the SoC in reset, or the PWM pin low or floating, the MOSFET is off, the fan's own pull-up takes the wire high and the fan runs at full speed. Keep it that way in the bootloader.
- 4-wire fans expect about 25 kHz on the PWM wire.
- Note the channel-to-controller order: fan 1 = PWM0, fan 2 = PWM2, fan 3 = PWM3, fan 4 = PWM1.
- **Tach** is an open-collector pulse from the fan (normally two pulses per revolution), pulled up on the board, clamped, and fed to the SoC through 10 kΩ. Count falling edges on the GPIO interrupt. **Fans 1–3 are on 1.8 V pins** (pulled up to 1.8 V); fan 4 is on a 3.3 V pin. Do not enable internal pull-ups that fight these, and never configure the 1.8 V pins as outputs toward a 3.3 V load.
- All fan connectors are left unpopulated by the fab; whichever connector is soldered in per channel carries the same four signals.

## PSU

| Net | SoC pin | GPIO | Function to select | Level | On the board |
|---|---|---|---|---|---|
| PSU_SCL | 64 | GPIO0_A5 (gpio0 line 5, no. 5) | I2C1_SCL_M0 | 3.3 V | J10 pin 6; pull-up position not fitted |
| PSU_SDA | 65 | GPIO0_A6 (gpio0 line 6, no. 6) | I2C1_SDA_M0 | 3.3 V | J10 pin 3; pull-up position not fitted |
| PSU_EN | 113 | GPIO2_A4 (gpio2 line 4, no. 68) | GPIO out | 3.3 V | J10 pin 5; 100k pull-down |

J10 (2×3, 2 mm): 1 = spare (test point TP29), 2 = GND, 3 = PSU_SDA, 4 = spare (test point TP30), 5 = PSU_EN, 6 = PSU_SCL.

- **No I²C pull-ups are fitted** on PSU_SCL / PSU_SDA (positions R272 / R273 are empty): the PSU is expected to provide them. If the bus is dead with a given PSU, fit the two 4.7 kΩ resistors or enable the pins' internal pull-ups.
- **PSU_EN** has a 100 kΩ pull-down, so it is low from power-up. Whether low or high turns the PSU output on has not been confirmed against a real APW PSU.
- The I²C protocol and address are the PSU's.

## WiFi (AP6212)

| Net | SoC pin | GPIO | Function to select | Level | On the board |
|---|---|---|---|---|---|
| WIFI_SDIO_CLK_SOC | 93 | GPIO1_C2 (gpio1 line 18, no. 50) | SDMMC1_CLK_M1 | 3.3 V | 22 Ω series at the SoC |
| WIFI_SDIO_CMD | 92 | GPIO1_C3 (gpio1 line 19, no. 51) | SDMMC1_CMD_M1 | 3.3 V |  |
| WIFI_SDIO_D0 | 94 | GPIO1_C1 (gpio1 line 17, no. 49) | SDMMC1_D0_M1 | 3.3 V |  |
| WIFI_SDIO_D1 | 95 | GPIO1_C0 (gpio1 line 16, no. 48) | SDMMC1_D1_M1 | 3.3 V |  |
| WIFI_SDIO_D2 | 90 | GPIO1_C5 (gpio1 line 21, no. 53) | SDMMC1_D2_M1 | 3.3 V |  |
| WIFI_SDIO_D3 | 91 | GPIO1_C4 (gpio1 line 20, no. 52) | SDMMC1_D3_M1 | 3.3 V |  |
| WIFI_REG_ON | 62 | GPIO0_A3 (gpio0 line 3, no. 3) | GPIO out | 3.3 V | module enable, high = on; 4.7k pull-down |
| WIFI_HOST_WAKE | 40 | GPIO4_A5 (gpio4 line 5, no. 133) | GPIO in (interrupt) | 3.3 V | module WL_HOST_WAKE |
| WIFI_LPO_32K | 58 | GPIO0_A0 (gpio0 line 0, no. 0) | RTC_CLKO | 3.3 V | 32.768 kHz to the module LPO pin |

- AMPAK AP6212 (Broadcom / Cypress BCM43438), 2.4 GHz 802.11 b/g/n on 4-bit SDIO at 3.3 V. Driver `brcmfmac`, with its firmware and an NVRAM file for the AP6212. The firmware file name depends on the chip revision the module reports (43430 A0 or A1), so check the kernel log on first boot.
- **SDMMC1 in its M1 position**, non-removable, SDIO only, no 1.8 V switching.
- **WIFI_REG_ON** (GPIO0_A3) is the power-sequence pin: high = module on. A 4.7 kΩ pull-down keeps the module off until firmware raises it (`mmc-pwrseq-simple` with `reset-gpios = <&gpio0 RK_PA3 GPIO_ACTIVE_LOW>`).
- **WIFI_HOST_WAKE** (GPIO4_A5) is the module's out-of-band interrupt to the host (optional for `brcmfmac`; SDIO in-band interrupts also work).
- **32.768 kHz**: the module's LPO input is fed from the SoC RTC's clock output on GPIO0_A0 (function RTC_CLKO, group `rtc_pins`). The RTC must be enabled and outputting the clock before REG_ON goes high. Whether the kernel's RTC driver turns the output on by itself has not been checked.
- The module has its own 26 MHz crystal. **Bluetooth is not wired** (no UART, no BT enable): leave it out.
- An external antenna on the U.FL connector J19 is required.

## Accessory header J15

| Net | SoC pin | GPIO | Function to select | Level | On the board |
|---|---|---|---|---|---|
| ACC_I2C4_SCL | 110 | GPIO2_A1 (gpio2 line 1, no. 65) | I2C4_SCL_M0 | 3.3 V | J15 pin 3; 4.7k pull-up |
| ACC_I2C4_SDA | 109 | GPIO2_A0 (gpio2 line 0, no. 64) | I2C4_SDA_M0 | 3.3 V | J15 pin 4; 4.7k pull-up |
| ACC_GPIO4_A7 | 38 | GPIO4_A7 (gpio4 line 7, no. 135) | GPIO | 3.3 V | J15 pin 5 |
| ACC1V8_GPIO3_C7 | 5 | GPIO3_C7 (gpio3 line 23, no. 119) | GPIO | 1.8 V | J15 pin 9 |
| ACC1V8_GPIO3_D0 | 7 | GPIO3_D0 (gpio3 line 24, no. 120) | GPIO | 1.8 V | J15 pin 10 |
| ACC1V8_GPIO3_D1 | 6 | GPIO3_D1 (gpio3 line 25, no. 121) | GPIO | 1.8 V | J15 pin 11 |
| ACC1V8_GPIO3_D2 | 8 | GPIO3_D2 (gpio3 line 26, no. 122) | GPIO | 1.8 V | J15 pin 12 |
| ACC1V8_GPIO3_D3 | 9 | GPIO3_D3 (gpio3 line 27, no. 123) | GPIO | 1.8 V | J15 pin 13 |

J15 (2×7, 2.54 mm, not fitted): 1 = +5V_SYS, 2 = +3V3, 3 = ACC_I2C4_SCL, 4 = ACC_I2C4_SDA, 5 = ACC_GPIO4_A7, 6 = GND, 7 = +1V8, 8 = GND, 9 = ACC1V8_GPIO3_C7, 10 = ACC1V8_GPIO3_D0, 11 = ACC1V8_GPIO3_D1, 12 = ACC1V8_GPIO3_D2, 13 = ACC1V8_GPIO3_D3, 14 = GND.

- I2C4 is meant for a small display; pull-ups are on the board.
- Pins 9–13 are **1.8 V GPIOs**; pin 7 gives the 1.8 V reference for level shifting. They have other functions if wanted (for example UART5 M2 on GPIO3_C7 / D0, PWM1 M2 on GPIO3_D3).

## Status LED

| Net | SoC pin | GPIO | Function to select | Level | On the board |
|---|---|---|---|---|---|
| STATUS_LED | 114 | GPIO2_A5 (gpio2 line 5, no. 69) | GPIO out | 3.3 V | green LED D100 through 1k, high = lit |

## Pins not used

- Not connected: 22, 29, 32, 33, 34, 35, 36, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128. These are the input-only camera pins GPI3_B0–C3 (117–128) and GPI4_C1 (22), and the audio codec pins (29, 32–36). Leave the camera, ISP and audio codec nodes disabled.
- UART0, UART5, SPI0 / SPI1, I2C2 / I2C3, PWM4–PWM11, eMMC, the LCD and camera interfaces are not used on this board. JTAG has no header: its M1 pins carry the console and its M0 pins are two of the microSD data lines.

## Every pin, in order

| SoC pin | Pin | Net | Use |
|---|---|---|---|
| 1 | MIPI_AVDD1V8 / GPIO7_VCC1V8 | +1V8 | supply |
| 2 | GPIO3_C4 | FAN1_TACH | GPIO in (edge count) |
| 3 | GPIO3_C5 | FAN2_TACH | GPIO in (edge count) |
| 4 | GPIO3_C6 | FAN3_TACH | GPIO in (edge count) |
| 5 | GPIO3_C7 | ACC1V8_GPIO3_C7 | GPIO |
| 6 | GPIO3_D1 | ACC1V8_GPIO3_D1 | GPIO |
| 7 | GPIO3_D0 | ACC1V8_GPIO3_D0 | GPIO |
| 8 | GPIO3_D2 | ACC1V8_GPIO3_D2 | GPIO |
| 9 | GPIO3_D3 | ACC1V8_GPIO3_D3 | GPIO |
| 10 | DVDD | +0V9_CORE | supply |
| 11 | GPIO3_A1 | SD_DET_N | SDMMC0_DET |
| 12 | GPIO3_A2 | SD_D1 | SDMMC0_D1 |
| 13 | GPIO4_VCC | +3V3 | supply |
| 14 | GPIO3_A3 | SD_D0 | SDMMC0_D0 |
| 15 | GPIO3_A4 | SD_CLK_SOC | SDMMC0_CLK |
| 16 | GPIO3_A5 | SD_CMD | SDMMC0_CMD |
| 17 | GPIO3_A6 | SD_D3 | SDMMC0_D3 |
| 18 | GPIO3_A7 | SD_D2 | SDMMC0_D2 |
| 19 | RTC_AVDD3V3 | RTC_3V3 | supply |
| 20 | RTC_XOUT | RTC_XOUT | dedicated |
| 21 | RTC_XIN | RTC_XIN | dedicated |
| 22 | GPI4_C1 / SARADC_IN1 | – | not connected |
| 23 | SARADC_IN0 | BOOT_ADC | dedicated |
| 24 | SARADC_USB_AVDD1V8 | USB_1V8 | supply |
| 25 | USB_VBUSDET | USB_VBUS_DET | dedicated |
| 26 | USB_DM | USB_DM_SOC | dedicated |
| 27 | USB_DP | USB_DP_SOC | dedicated |
| 28 | USB_AVDD3V3 | +3V3 | supply |
| 29 | CODEC_LINEOUT | – | not connected |
| 30 | CODEC_VCM | CODEC_VCM | dedicated |
| 31 | CODEC_AVDD1V8 | +1V8 | supply |
| 32 | CODEC_MICBIAS | – | not connected |
| 33 | CODEC_MIC0N | – | not connected |
| 34 | CODEC_MIC0P | – | not connected |
| 35 | CODEC_MIC1N | – | not connected |
| 36 | CODEC_MIC1P | – | not connected |
| 37 | CODEC_AVSS | GND | ground |
| 38 | GPIO4_A7 | ACC_GPIO4_A7 | GPIO |
| 39 | GPIO4_A6 | FSPI_D3 | FSPI_D3 |
| 40 | GPIO4_A5 | WIFI_HOST_WAKE | GPIO in (interrupt) |
| 41 | GPIO4_A4 | FSPI_D0 | FSPI_D0 |
| 42 | GPIO4_A3 | FSPI_D1 | FSPI_D1 |
| 43 | GPIO3_VCC | +3V3 | supply |
| 44 | GPIO4_A2 | FSPI_D2 | FSPI_D2 |
| 45 | GPIO4_A1 | HB_SCL | I2C0_SCL_M1 |
| 46 | GPIO4_A0 | HB_SDA | I2C0_SDA_M1 |
| 47 | GPIO4_B0 | FSPI_CS_N | FSPI_CS0 |
| 48 | GPIO4_B1 | FSPI_CLK_SOC | FSPI_CLK |
| 49 | DDR_VDDQ | +1V35_DDR | supply |
| 50 | DDR_VDDQ | +1V35_DDR | supply |
| 51 | DVDD | +0V9_CORE | supply |
| 52 | DRAM_ZQ | DRAM_ZQ | dedicated |
| 53 | DDR_PLL_AVDD1V8 | +1V8 | supply |
| 54 | DVDD | +0V9_CORE | supply |
| 55 | DVDD | +0V9_CORE | supply |
| 56 | DDR_VDDQ | +1V35_DDR | supply |
| 57 | TVSS | GND | ground |
| 58 | GPIO0_A0 | WIFI_LPO_32K | RTC_CLKO |
| 59 | GPIO0_A1 | FAN2_PWM | PWM2_M0 |
| 60 | GPIO0_A2 | FAN3_PWM | PWM3_IR_M0 |
| 61 | PMU_VCC3V3 | +3V3 | supply |
| 62 | GPIO0_A3 | WIFI_REG_ON | GPIO out |
| 63 | GPIO0_A4 | FAN4_PWM | PWM1_M0 |
| 64 | GPIO0_A5 | PSU_SCL | I2C1_SCL_M0 |
| 65 | GPIO0_A6 | PSU_SDA | I2C1_SDA_M0 |
| 66 | nPOR | RESET_N | dedicated |
| 67 | PMU_DVDD0V9 | +0V9_CORE | supply |
| 68 | OSC_XIN | OSC_XIN | dedicated |
| 69 | OSC_XOUT | OSC_XOUT | dedicated |
| 70 | OSC_AVDD1V8 / PLL_AVDD1V8 | +1V8 | supply |
| 71 | OSC_PLL_DVDD | +0V9_CORE | supply |
| 72 | GPIO1_A0 | HB1_TX | UART3_TX_M0 |
| 73 | GPIO1_A1 | HB1_RX | UART3_RX_M0 |
| 74 | GPIO1_A2 | FAN1_PWM | PWM0_M0 |
| 75 | GPIO1_A3 | HB0_TX | UART1_TX_M0 |
| 76 | GPIO1_A4 | HB0_RX | UART1_RX_M0 |
| 77 | GPIO1_B0 | HB2_RX | UART4_RX_M0 |
| 78 | GPIO1_B1 | HB2_TX | UART4_TX_M0 |
| 79 | GPIO1_B2 | DEBUG_TX | UART2_TX_M1 |
| 80 | GPIO1_B3 | DEBUG_RX | UART2_RX_M1 |
| 81 | GPIO1_VCC3V3 | +3V3 | supply |
| 82 | DVDD | +0V9_CORE | supply |
| 83 | GPIO1_C6 | HB0_PWR_EN | GPIO out |
| 84 | GPIO1_C7 | HB1_PWR_EN | GPIO out |
| 85 | GPIO1_D3 | ETH_LED_LINK | GPIO out |
| 86 | GPIO1_D2 | ETH_LED_SPEED | GPIO out |
| 87 | GPIO1_D1 | HB2_PWR_EN | GPIO out |
| 88 | GPIO6_VCC | +3V3 | supply |
| 89 | GPIO1_D0 | FAN4_TACH | GPIO in (edge count) |
| 90 | GPIO1_C5 | WIFI_SDIO_D2 | SDMMC1_D2_M1 |
| 91 | GPIO1_C4 | WIFI_SDIO_D3 | SDMMC1_D3_M1 |
| 92 | GPIO1_C3 | WIFI_SDIO_CMD | SDMMC1_CMD_M1 |
| 93 | GPIO1_C2 | WIFI_SDIO_CLK_SOC | SDMMC1_CLK_M1 |
| 94 | GPIO1_C1 | WIFI_SDIO_D0 | SDMMC1_D0_M1 |
| 95 | GPIO1_C0 | WIFI_SDIO_D1 | SDMMC1_D1_M1 |
| 96 | OTP / ETH / TSADC AVDD1V8 | ETH_1V8 | supply |
| 97 | ETH_PHY_RXN | ETH_RX_N | dedicated |
| 98 | ETH_PHY_RXP | ETH_RX_P | dedicated |
| 99 | ETH_PHY_TXN | ETH_TX_N | dedicated |
| 100 | ETH_PHY_TXP | ETH_TX_P | dedicated |
| 101 | ETH_AVDD3V3 | ETH_3V3 | supply |
| 102 | ETH_EXTR | ETH_BIAS | dedicated |
| 103 | DVDD | +0V9_CORE | supply |
| 104 | GPIO2_B1 | HB0_RST_N | GPIO out |
| 105 | GPIO2_B0 | HB1_RST_N | GPIO out |
| 106 | GPIO2_A7 | HB2_RST_N | GPIO out |
| 107 | GPIO2_A6 | HB0_PLUG | GPIO in |
| 108 | GPIO5_VCC | +3V3 | supply |
| 109 | GPIO2_A0 | ACC_I2C4_SDA | I2C4_SDA_M0 |
| 110 | GPIO2_A1 | ACC_I2C4_SCL | I2C4_SCL_M0 |
| 111 | GPIO2_A2 | HB1_PLUG | GPIO in |
| 112 | GPIO2_A3 | HB2_PLUG | GPIO in |
| 113 | GPIO2_A4 | PSU_EN | GPIO out |
| 114 | GPIO2_A5 | STATUS_LED | GPIO out |
| 115 | CPU_DVDD | +0V9_CPU | supply |
| 116 | DVDD | +0V9_CORE | supply |
| 117 | GPI3_B0 | – | not connected |
| 118 | GPI3_B1 | – | not connected |
| 119 | GPI3_B2 | – | not connected |
| 120 | GPI3_B3 | – | not connected |
| 121 | GPI3_B4 | – | not connected |
| 122 | GPI3_B5 | – | not connected |
| 123 | GPI3_B6 | – | not connected |
| 124 | GPI3_B7 | – | not connected |
| 125 | GPI3_C0 | – | not connected |
| 126 | GPI3_C1 | – | not connected |
| 127 | GPI3_C2 | – | not connected |
| 128 | GPI3_C3 | – | not connected |
| 129 | VSS (exposed pad) | GND | ground |

## Device-tree starting points

Untested fragments against the Luckfox SDK kernel's `rv1106.dtsi` labels, to show which controller takes which pin group and which GPIO has which polarity. Adapt to the kernel you build.

```dts
/* console: UART2 M1, 115200 8N1 */
&fiq_debugger { status = "okay"; };

/* hashboards */
&uart1 { pinctrl-names = "default"; pinctrl-0 = <&uart1m0_xfer>; status = "okay"; };  /* port 0, J3 */
&uart3 { pinctrl-names = "default"; pinctrl-0 = <&uart3m0_xfer>; status = "okay"; };  /* port 1, J4 */
&uart4 { pinctrl-names = "default"; pinctrl-0 = <&uart4m0_xfer>; status = "okay"; };  /* port 2, J5 */
&i2c0  { pinctrl-names = "default"; pinctrl-0 = <&i2c0m1_xfer>; status = "okay"; };   /* shared hashboard bus */

/* PSU, accessory */
&i2c1  { pinctrl-names = "default"; pinctrl-0 = <&i2c1m0_xfer>; status = "okay"; };   /* J10; no pull-ups on the board */
&i2c4  { pinctrl-names = "default"; pinctrl-0 = <&i2c4m0_xfer>; status = "okay"; };   /* J15 */

/* fans: output inverted by a MOSFET */
&pwm0 { pinctrl-names = "active"; pinctrl-0 = <&pwm0m0_pins>; status = "okay"; };     /* fan 1 */
&pwm2 { pinctrl-names = "active"; pinctrl-0 = <&pwm2m0_pins>; status = "okay"; };     /* fan 2 */
&pwm3 { pinctrl-names = "active"; pinctrl-0 = <&pwm3m0_pins>; status = "okay"; };     /* fan 3 */
&pwm1 { pinctrl-names = "active"; pinctrl-0 = <&pwm1m0_pins>; status = "okay"; };     /* fan 4 */

/* storage */
&sfc {
	status = "okay";
	flash@0 { compatible = "spi-nand"; reg = <0>; spi-max-frequency = <75000000>;
	          spi-rx-bus-width = <4>; spi-tx-bus-width = <1>; };
};
&sdmmc {
	bus-width = <4>; cap-sd-highspeed; disable-wp; no-1-8-v; no-sdio; no-mmc;
	pinctrl-names = "default";
	pinctrl-0 = <&sdmmc0_clk &sdmmc0_cmd &sdmmc0_det &sdmmc0_bus4>;
	status = "okay";
};

/* network, USB */
&gmac { status = "okay"; };
&u2phy { status = "okay"; };
&usbdrd_dwc3 { dr_mode = "peripheral"; status = "okay"; };

/* BOOT button on SARADC channel 0, 1.8 V reference */
&saradc { status = "okay"; };

/* WiFi: AP6212 on SDMMC1 M1 */
&rtc { pinctrl-names = "default"; pinctrl-0 = <&rtc_pins>; status = "okay"; };        /* 32.768 kHz out on GPIO0_A0 */
/ {
	wifi_pwrseq: wifi-pwrseq {
		compatible = "mmc-pwrseq-simple";
		reset-gpios = <&gpio0 RK_PA3 GPIO_ACTIVE_LOW>;                          /* WIFI_REG_ON, high = on */
	};
	leds {
		compatible = "gpio-leds";
		status   { gpios = <&gpio2 RK_PA5 GPIO_ACTIVE_HIGH>; };
		eth-link { gpios = <&gpio1 RK_PD3 GPIO_ACTIVE_HIGH>; };                 /* green, left */
		eth-speed { gpios = <&gpio1 RK_PD2 GPIO_ACTIVE_HIGH>; };                /* yellow, right */
	};
};
&sdio {
	bus-width = <4>; cap-sd-highspeed; cap-sdio-irq; non-removable; no-1-8-v; no-sd; no-mmc;
	keep-power-in-suspend;
	mmc-pwrseq = <&wifi_pwrseq>;
	pinctrl-names = "default";
	pinctrl-0 = <&sdmmc1m1_clk &sdmmc1m1_cmd &sdmmc1m1_bus4>;
	#address-cells = <1>; #size-cells = <0>;
	status = "okay";
	wifi@1 {
		compatible = "brcm,bcm4329-fmac";
		reg = <1>;
		interrupt-parent = <&gpio4>;
		interrupts = <RK_PA5 IRQ_TYPE_LEVEL_HIGH>;                              /* WIFI_HOST_WAKE */
		interrupt-names = "host-wake";
	};
};
```

GPIO lines Mujina (or a board service) drives or reads directly:

| Signal | GPIO | Controller, line | Global no. | Direction and meaning |
|---|---|---|---|---|
| HB0_PWR_EN | GPIO1_C6 | gpio1 line 22 | 54 | out, high = on, default on |
| HB1_PWR_EN | GPIO1_C7 | gpio1 line 23 | 55 | out, high = on, default on |
| HB2_PWR_EN | GPIO1_D1 | gpio1 line 25 | 57 | out, high = on, default on |
| HB0_RST_N | GPIO2_B1 | gpio2 line 9 | 73 | out, low = reset, default low |
| HB1_RST_N | GPIO2_B0 | gpio2 line 8 | 72 | out, low = reset, default low |
| HB2_RST_N | GPIO2_A7 | gpio2 line 7 | 71 | out, low = reset, default low |
| HB0_PLUG | GPIO2_A6 | gpio2 line 6 | 70 | in, high = plugged (unconfirmed) |
| HB1_PLUG | GPIO2_A2 | gpio2 line 2 | 66 | in, high = plugged (unconfirmed) |
| HB2_PLUG | GPIO2_A3 | gpio2 line 3 | 67 | in, high = plugged (unconfirmed) |
| PSU_EN | GPIO2_A4 | gpio2 line 4 | 68 | out, default low, polarity unconfirmed |
| FAN1_TACH | GPIO3_C4 | gpio3 line 20 | 116 | in, falling-edge count, 1.8 V |
| FAN2_TACH | GPIO3_C5 | gpio3 line 21 | 117 | in, falling-edge count, 1.8 V |
| FAN3_TACH | GPIO3_C6 | gpio3 line 22 | 118 | in, falling-edge count, 1.8 V |
| FAN4_TACH | GPIO1_D0 | gpio1 line 24 | 56 | in, falling-edge count |
| STATUS_LED | GPIO2_A5 | gpio2 line 5 | 69 | out, high = lit |

## Not yet confirmed

1. Nothing in this document has been exercised on hardware.
2. Hashboard plug-detect polarity, reset behaviour, logic levels and what the three address straps select, against a real S19 hashboard; PSU enable polarity and whether the PSU pulls up its I²C lines.
3. That the kernel's RTC driver outputs 32.768 kHz on GPIO0_A0 with `rtc_pins` selected, and that the AP6212 starts from it.
4. Which CPU operating points are valid at the fixed 0.9 V rail in the kernel you use.
5. Ethernet LED behaviour: they are GPIOs here; a BSP that expects PHY-driven LEDs needs a trigger set up instead.
6. The I/O-domain property names and the node labels in a mainline kernel.
