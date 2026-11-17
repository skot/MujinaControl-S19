# RV1106G2 pin allocation

> For the current state in one place, written for firmware work, see [firmware-pins.md](firmware-pins.md). This page is the record of how the allocation was made and changed; some early statements here were superseded (for example, plug detect now has pull-downs, not pull-ups).

Draft hardware allocation checked against Rockchip Rev 2.2 package pin table and the supplied rv1106-pinctrl.dtsi. SoC pin numbers below are QFN contact numbers, not Linux GPIO numbers. The firmware/device tree remains to be implemented.

| Net | SoC pin | Selected function | Original pin capabilities / reset-pull suffix |
| --- | ---: | --- | --- |
| SD_DET_N | 11 | SDMMC0_DET | SDMMC0_DET/GPIO3_A1_u |
| SD_D1 | 12 | SDMMC0_D1 | SDMMC0_D1/UART2_TX_M0/PWM9_M0/GPIO3_A2_u |
| SD_D0 | 14 | SDMMC0_D0 | SDMMC0_D0/UART2_RX_M0/PWM8_M0/GPIO3_A3_u |
| SD_CLK_SOC | 15 | SDMMC0_CLK | SDMMC0_CLK/UART5_RTS_M0/I2C0_SCL_M2/JTAG_LPMCU_TCK_M1/PWM10_M0/GPIO3_A4_d |
| SD_CMD | 16 | SDMMC0_CMD | SDMMC0_CMD/UART5_CTS_M0/I2C0_SDA_M2/JTAG_LPMCU_TMS_M1/PWM11_IR_M0/GPIO3_A5_u |
| SD_D3 | 17 | SDMMC0_D3 | SDMMC0_D3/UART5_TX_M0/JTAG_CPU_TMS_M0/JTAG_HPMCU_TMS_M1/GPIO3_A6_u |
| SD_D2 | 18 | SDMMC0_D2 | SDMMC0_D2/UART5_RX_M0/JTAG_CPU_TCK_M0/JTAG_HPMCU_TCK_M1/GPIO3_A7_u |
| RTC_XOUT | 20 | RTC_XOUT | RTC_XOUT |
| RTC_XIN | 21 | RTC_XIN | RTC_XIN |
| BOOT_ADC | 23 | SARADC_IN0 | SARADC_IN0/GPI4_C0_z |
| USB_VBUS_DET | 25 | USB_VBUSDET | USB_VBUSDET |
| USB_DM_SOC | 26 | USB_DM | USB_DM |
| USB_DP_SOC | 27 | USB_DP | USB_DP |
| CODEC_VCM | 30 | CODEC_VCM | CODEC_VCM |
| FSPI_D3 | 39 | FSPI_D3 | EMMC_D3/FSPI_D3/GPIO4_A6_u |
| FSPI_D0 | 41 | FSPI_D0 | EMMC_D0/FSPI_D0/GPIO4_A4_u |
| FSPI_D1 | 42 | FSPI_D1 | EMMC_D1/FSPI_D1/GPIO4_A3_u |
| FSPI_D2 | 44 | FSPI_D2 | EMMC_D2/FSPI_D2/GPIO4_A2_u |
| HB_SCL | 45 | I2C0_SCL_M1 | EMMC_D6/SPI1_MOSI_M0/UART0_TX_M2/I2C0_SCL_M1/GPIO4_A1_u |
| HB_SDA | 46 | I2C0_SDA_M1 | EMMC_D7/SPI1_MISO_M0/UART0_RX_M2/I2C0_SDA_M1/GPIO4_A0_u |
| FSPI_CS_N | 47 | FSPI_CS0 | EMMC_CMD/FSPI_CS0/GPIO4_B0_u |
| FSPI_CLK_SOC | 48 | FSPI_CLK | EMMC_CLK/FSPI_CLK/GPIO4_B1_d |
| DRAM_ZQ | 52 | DRAM_ZQ | DRAM_ZQ |
| PSU_SCL | 64 | I2C1_SCL_M0 | I2C1_SCL_M0/UART1_RTS_M0/PWM5_M0/GPIO0_A5_d |
| PSU_SDA | 65 | I2C1_SDA_M0 | I2C1_SDA_M0/UART1_CTS_M0/PWM6_M0/GPIO0_A6_d |
| RESET_N | 66 | nPOR | nPOR |
| OSC_XIN | 68 | OSC_XIN | OSC_XIN |
| OSC_XOUT | 69 | OSC_XOUT | OSC_XOUT |
| HB1_TX | 72 | UART3_TX_M0 | UART3_TX_M0/I2C2_SCL_M0/PWM7_IR_M0/GPIO1_A0_d |
| HB1_RX | 73 | UART3_RX_M0 | UART3_RX_M0/I2C2_SDA_M0/PWM4_M0/GPIO1_A1_d |
| FAN1_PWM | 74 | PWM0_M0 | PWM0_M0/CPU_AVS/VI_CIF_D0_M1/GPIO1_A2_d |
| HB0_TX | 75 | UART1_TX_M0 | UART1_TX_M0/I2C0_SCL_M0/GPIO1_A3_d |
| HB0_RX | 76 | UART1_RX_M0 | UART1_RX_M0/I2C0_SDA_M0/GPIO1_A4_d |
| HB2_RX | 77 | UART4_RX_M0 | UART4_RX_M0/PWM3_IR_M1/GPIO1_B0_d |
| HB2_TX | 78 | UART4_TX_M0 | UART4_TX_M0/PWM7_IR_M1/SPI1_CS1_M0/VI_CIF_D1_M1/GPIO1_B1_d |
| DEBUG_TX | 79 | UART2_TX_M1 | JTAG_CPU_TCK_M1/UART2_TX_M1/JTAG_HPMCU_TCK_M0/JTAG_LPMCU_TCK_M0/GPIO1_B2_d |
| DEBUG_RX | 80 | UART2_RX_M1 | JTAG_CPU_TMS_M1/UART2_RX_M1/JTAG_HPMCU_TMS_M0/JTAG_LPMCU_TMS_M0/GPIO1_B3_u |
| ETH_LED_LINK | 85 | GPIO1_D3 | VO_LCDC_CLK/VI_CIF_CLKO_M1/I2C3_SCL_M1/UART5_TX_M1/PWM11_IR_M2/AUD_DSM_N/GPIO1_D3_d |
| ETH_LED_SPEED | 86 | GPIO1_D2 | VO_LCDC_VSYNC/VI_CIF_VSYNC_M1/I2C3_SDA_M1/UART5_RX_M1/SPI0_CS1_M0/PWM0_M1/AUD_DSM_P/GPIO1_D2_d |
| FAN4_TACH | 89 | GPIO1_D0 | VO_LCDC_DEN/VI_CIF_CLKI_M1/PWM3_IR_M2/UART5_RTS_M1/UART3_TX_M1/GPIO1_D0_d |
| WIFI_SDIO_D2 | 90 | SDMMC1_D2_M1 | VO_LCDC_D2/VI_CIF_D7_M1/PWM9_M1/UART4_TX_M1/SDMMC1_D2_M1/GPIO1_C5_d |
| WIFI_SDIO_D3 | 91 | SDMMC1_D3_M1 | VO_LCDC_D3/VI_CIF_D6_M1/PWM8_M1/UART4_RX_M1/SDMMC1_D3_M1/GPIO1_C4_d |
| WIFI_SDIO_CMD | 92 | SDMMC1_CMD_M1 | VO_LCDC_D4/VI_CIF_D5_M1/PWM6_M2/I2C4_SDA_M1/SDMMC1_CMD_M1/SPI0_MISO_M0/GPIO1_C3_d |
| WIFI_SDIO_CLK_SOC | 93 | SDMMC1_CLK_M1 | VO_LCDC_D5/VI_CIF_D4_M1/PWM5_M2/I2C4_SCL_M1/SDMMC1_CLK_M1/SPI0_MOSI_M0/GPIO1_C2_d |
| WIFI_SDIO_D0 | 94 | SDMMC1_D0_M1 | VO_LCDC_D6/VI_CIF_D3_M1/PWM4_M2/SPI0_CLK_M0/SDMMC1_D0_M1/GPIO1_C1_d |
| WIFI_SDIO_D1 | 95 | SDMMC1_D1_M1 | VO_LCDC_D7/VI_CIF_D2_M1/PWM2_M2/SPI0_CS0_M0/SDMMC1_D1_M1/GPIO1_C0_d |
| ETH_RX_N | 97 | ETH_PHY_RXN | ETH_PHY_RXN |
| ETH_RX_P | 98 | ETH_PHY_RXP | ETH_PHY_RXP |
| ETH_TX_N | 99 | ETH_PHY_TXN | ETH_PHY_TXN |
| ETH_TX_P | 100 | ETH_PHY_TXP | ETH_PHY_TXP |
| ETH_BIAS | 102 | ETH_EXTR | ETH_EXTR |
| HB0_RST_N | 104 | GPIO2_B1 | UART0_TX_M1/I2C1_SDA_M1/VO_LCDC_D17/PWM6_M1/GPIO2_B1_d |
| HB1_RST_N | 105 | GPIO2_B0 | UART0_RX_M1/I2C1_SCL_M1/VO_LCDC_D16/PWM5_M1/GPIO2_B0 |
| HB2_RST_N | 106 | GPIO2_A7 | UART0_CTS_M1/I2S0_SDO1_SDI3/VO_LCDC_D15/PWM4_M1/I2C3_SDA_M0/PRELIGHT_TRIG_OUT/GPIO2_A7_d |
| HB0_PLUG | 107 | GPIO2_A6 | UART0_RTS_M1/I2S0_SDO2_SDI2/VO_LCDC_D14/PWM2_M1/I2C3_SCL_M0/FLASH_TRIG_OUT/GPIO2_A6_d |
| DISPLAY_SDA | 109 | I2C4_SDA_M0 | SDMMC1_D1_M0/I2S0_SCLK/VO_LCDC_D8/UART1_CTS_M1/I2C4_SDA_M0/GPIO2_A0_d |
| DISPLAY_SCL | 110 | I2C4_SCL_M0 | SDMMC_D0/I2S0_LRCK/VO_LCDC_D9/UART1_RTS_M1/I2C4_SCL_M0/GPIO2_A1_d |
| HB1_PLUG | 111 | GPIO2_A2 | SDMMC1_CLK_M0/I2S0_MCLK/VO_LCDC_D10/GPIO2_A2_d |
| HB2_PLUG | 112 | GPIO2_A3 | SDMMC1_CMD_M0/I2S0_SDO3_SDI1/VO_LCDC_D11/GPIO2_A3_d |
| PSU_EN | 113 | GPIO2_A4 | SDMMC1_D3_M0/I2S0_SDO0/VO_LCDC_D12/UART1_TX_M1/GPIO2_A4_d |
| STATUS_LED | 114 | GPIO2_A5 | SDMMC1_D2_M0/I2S0_SDI0/VO_LCDC_D13/UART1_RX_M1/GPIO2_A5_d |

All miner-facing GPIO banks are supplied at 3.3 V. The unused camera bank remains at its required 1.8 V. Suffix `_d` means the vendor pin name specifies pull-down, `_u` pull-up and `_z` neither; firmware must program the selected pin mux and pull state explicitly. Pin 105 has no suffix in the supplied Rev 2.2 table.

## Software allocation

| Interface | Mux group | Connection |
| --- | --- | --- |
| Hashboard 0 | uart1m0_xfer | J3.11 TX / J3.12 RX |
| Hashboard 1 | uart3m0_xfer | J4.11 TX / J4.12 RX |
| Hashboard 2 | uart4m0_xfer | J5.11 TX / J5.12 RX |
| Console | uart2m1_xfer | J16.1 TX / J16.3 RX |
| Hashboard management | i2c0m1_xfer | J3/J4/J5.4 SCL / .3 SDA |
| PSU management | i2c1m0_xfer | J10.6 SCL / .3 SDA |
| Display | i2c4m0_xfer | J15.3 SCL / .4 SDA |
| Fan 1 | pwm0m0_pins | Inverted through Q2 |
| Fan 2 | pwm2m0_pins | Inverted through Q3 |
| Fan 3 | pwm3m0_pins | Inverted through Q4 |
| Fan 4 | pwm1m0_pins | Inverted through Q5 |
| WiFi | sdmmc1m1 (clk, cmd, bus4) | U160 AP6212, 3.3 V SDIO |

Fan tach inputs are GPIO edge counters. Hashboard reset outputs default low through external 100k resistors; plug inputs have external 10k pull-ups. PSU enable defaults low. Set the PWM polarity to account for the inverting NMOS and ensure failure handling leaves fan PWM open.

Ethernet LEDs use GPIO1_D3 and GPIO1_D2 as in Raven; check the exact BSP LED trigger/mux configuration. SDMMC0 uses its dedicated group and FSPI uses the eMMC/FSPI bank; no eMMC is fitted.

These allocations do not establish driver performance, firmware readiness or the electrical behavior of a particular miner.

## Hashboard supply enables — 2026-11-10

| Net | SoC contact | GPIO mode | Removed accessory connection |
| --- | ---: | --- | --- |
| HB0_PWR_EN | 83 | GPIO1_C6, mode 0, 3.3 V output | J15.21 now NC |
| HB1_PWR_EN | 84 | GPIO1_C7, mode 0, 3.3 V output | J15.22 now NC |
| HB2_PWR_EN | 87 | GPIO1_D1, mode 0, 3.3 V output | J15.18 now NC |

Active high; 4.7k external pull-ups make supplies default ON despite reset input pulldowns. Reserve these GPIOs in bootloader and OS, preload output state before setting direction, and do not enable their alternate functions. Stop UART and keep signal outputs low/Hi-Z before disabling power; assert reset low. Always-on shared I²C pull-ups can back-power a disabled port: this is not full signal isolation. Preserve all other J15 functions and numbering. Detailed source evidence, power budget, and verification: `build/MujinaControl-S19/hashboard-power/report.md` at the project root. The PCB was updated from this schematic on 2026-11-10: U150-U152 and their passives are placed under J3 and beside each connector, unrouted.

## On-board WiFi and moved fan pins — 2026-11-12 (branch onboard-wifi)

The AP6212 module takes the SDMMC1 port in its M1 position (pins 90–95), which the fans used before. Pins come from the accessory header J15; the J15 pins that lose their signal are not connected.

| Net | SoC contact | Function | Level | Note |
| --- | ---: | --- | --- | --- |
| FAN1_TACH | 2 | GPIO3_C4 | 1.8 V | was J15.27; pull-up R263 and clamp D230 now on +1V8 |
| FAN2_TACH | 3 | GPIO3_C5 | 1.8 V | was J15.28; R265 / D231 on +1V8 |
| FAN3_TACH | 4 | GPIO3_C6 | 1.8 V | was J15.29; R267 / D232 on +1V8 |
| WIFI_HOST_WAKE | 40 | GPIO4_A5 | 3.3 V | was J15.12; interrupt from the module |
| WIFI_LPO_32K | 58 | RTC_CLK_OUT (GPIO0_A0) | 3.3 V | was J15.10; 32.768 kHz from the SoC RTC |
| FAN2_PWM | 59 | PWM2_M0 (GPIO0_A1) | 3.3 V | was J15.9 |
| FAN3_PWM | 60 | PWM3_IR_M0 (GPIO0_A2) | 3.3 V | was J15.15 |
| WIFI_REG_ON | 62 | GPIO0_A3 | 3.3 V | was J15.17; reset pull-up on the pin, 4.7k pull-down R311 on the board |
| FAN4_PWM | 63 | PWM1_M0 (GPIO0_A4) | 3.3 V | was J15.16; PWM1 is no longer free for J15.30 |

FAN1_PWM (pin 74) and FAN4_TACH (pin 89) are unchanged. The three 1.8 V tach inputs must not be driven above 1.8 V: their pull-ups and upper clamp diodes go to +1V8. J15 is now a 2×7 header: I2C4 on pins 3 / 4, GPIO4_A7 on 5, GPIO3_C7 / D0 / D1 / D2 / D3 on 9–13 (1.8 V), supplies on 1 / 2 / 7, ground on 6 / 8 / 14. Details: [onboard-wifi.md](onboard-wifi.md).
