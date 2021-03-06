EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:arduino_shieldsNCL
LIBS:adr4550
LIBS:PowerSupplyControl-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 5 5
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L LM324N U1
U 1 1 57999088
P 8800 1150
F 0 "U1" H 8950 1300 50  0000 C CNN
F 1 "LM324N" H 8950 950 50  0000 C CNN
F 2 "SMD_Packages:SOIC-14_N" H 8750 1250 50  0001 C CNN
F 3 "" H 8850 1350 50  0000 C CNN
	1    8800 1150
	1    0    0    -1  
$EndComp
Text GLabel 1550 1550 0    60   Input ~ 0
V_PWM1
Text GLabel 1550 2250 0    60   Input ~ 0
I_PWM1
Text GLabel 1550 3150 0    60   Input ~ 0
V_PWM2
Text GLabel 1500 3850 0    60   Input ~ 0
I_PWM2
$Comp
L R R2
U 1 1 57999093
P 1700 1550
F 0 "R2" V 1780 1550 50  0000 C CNN
F 1 "10k" V 1700 1550 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 1630 1550 50  0001 C CNN
F 3 "" H 1700 1550 50  0000 C CNN
	1    1700 1550
	0    1    1    0   
$EndComp
$Comp
L C_Small C2
U 1 1 5799909A
P 1950 1750
F 0 "C2" H 1960 1820 50  0000 L CNN
F 1 "47uF" H 1960 1670 50  0000 L CNN
F 2 "Capacitors_SMD:C_1210" H 1950 1750 50  0001 C CNN
F 3 "" H 1950 1750 50  0000 C CNN
	1    1950 1750
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR89
U 1 1 579990A1
P 1950 1850
F 0 "#PWR89" H 1950 1600 50  0001 C CNN
F 1 "GND" H 1950 1700 50  0000 C CNN
F 2 "" H 1950 1850 50  0000 C CNN
F 3 "" H 1950 1850 50  0000 C CNN
	1    1950 1850
	0    1    1    0   
$EndComp
$Comp
L R R3
U 1 1 579990A7
P 1700 2250
F 0 "R3" V 1780 2250 50  0000 C CNN
F 1 "10k" V 1700 2250 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 1630 2250 50  0001 C CNN
F 3 "" H 1700 2250 50  0000 C CNN
	1    1700 2250
	0    1    1    0   
$EndComp
$Comp
L C_Small C3
U 1 1 579990AE
P 1950 2450
F 0 "C3" H 1960 2520 50  0000 L CNN
F 1 "47uF" H 1960 2370 50  0000 L CNN
F 2 "Capacitors_SMD:C_1210" H 1950 2450 50  0001 C CNN
F 3 "" H 1950 2450 50  0000 C CNN
	1    1950 2450
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR90
U 1 1 579990B5
P 1950 2550
F 0 "#PWR90" H 1950 2300 50  0001 C CNN
F 1 "GND" H 1950 2400 50  0000 C CNN
F 2 "" H 1950 2550 50  0000 C CNN
F 3 "" H 1950 2550 50  0000 C CNN
	1    1950 2550
	0    1    1    0   
$EndComp
$Comp
L R R4
U 1 1 579990BB
P 1700 3150
F 0 "R4" V 1780 3150 50  0000 C CNN
F 1 "10k" V 1700 3150 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 1630 3150 50  0001 C CNN
F 3 "" H 1700 3150 50  0000 C CNN
	1    1700 3150
	0    1    1    0   
$EndComp
$Comp
L C_Small C4
U 1 1 579990C2
P 1950 3350
F 0 "C4" H 1960 3420 50  0000 L CNN
F 1 "47uF" H 1960 3270 50  0000 L CNN
F 2 "Capacitors_SMD:C_1210" H 1950 3350 50  0001 C CNN
F 3 "" H 1950 3350 50  0000 C CNN
	1    1950 3350
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR91
U 1 1 579990C9
P 1950 3450
F 0 "#PWR91" H 1950 3200 50  0001 C CNN
F 1 "GND" H 1950 3300 50  0000 C CNN
F 2 "" H 1950 3450 50  0000 C CNN
F 3 "" H 1950 3450 50  0000 C CNN
	1    1950 3450
	0    1    1    0   
$EndComp
$Comp
L R R1
U 1 1 579990CF
P 1650 3850
F 0 "R1" V 1730 3850 50  0000 C CNN
F 1 "10k" V 1650 3850 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 1580 3850 50  0001 C CNN
F 3 "" H 1650 3850 50  0000 C CNN
	1    1650 3850
	0    1    1    0   
$EndComp
$Comp
L C_Small C1
U 1 1 579990D6
P 1900 4050
F 0 "C1" H 1910 4120 50  0000 L CNN
F 1 "47uF" H 1910 3970 50  0000 L CNN
F 2 "Capacitors_SMD:C_1210" H 1900 4050 50  0001 C CNN
F 3 "" H 1900 4050 50  0000 C CNN
	1    1900 4050
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR88
U 1 1 579990DD
P 1900 4150
F 0 "#PWR88" H 1900 3900 50  0001 C CNN
F 1 "GND" H 1900 4000 50  0000 C CNN
F 2 "" H 1900 4150 50  0000 C CNN
F 3 "" H 1900 4150 50  0000 C CNN
	1    1900 4150
	0    1    1    0   
$EndComp
Text GLabel 1950 1550 2    60   Input ~ 0
V_OUT1
Text GLabel 1950 2250 2    60   Input ~ 0
I_OUT1
Text GLabel 1950 3150 2    60   Input ~ 0
V_OUT2
Text GLabel 1900 3850 2    60   Input ~ 0
I_OUT2
Text GLabel 8500 1050 0    60   Input ~ 0
V_OUT1
Text GLabel 9400 4100 2    60   Input ~ 0
I_OUT1
$Comp
L R R22
U 1 1 579990E9
P 9250 1150
F 0 "R22" V 9330 1150 50  0000 C CNN
F 1 "20k" V 9250 1150 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 9180 1150 50  0001 C CNN
F 3 "" H 9250 1150 50  0000 C CNN
	1    9250 1150
	0    1    1    0   
$EndComp
$Comp
L R R16
U 1 1 579990F0
P 8350 1600
F 0 "R16" V 8430 1600 50  0000 C CNN
F 1 "20k" V 8350 1600 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 8280 1600 50  0001 C CNN
F 3 "" H 8350 1600 50  0000 C CNN
	1    8350 1600
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR103
U 1 1 579990F7
P 8700 1450
F 0 "#PWR103" H 8700 1200 50  0001 C CNN
F 1 "GND" H 8700 1300 50  0000 C CNN
F 2 "" H 8700 1450 50  0000 C CNN
F 3 "" H 8700 1450 50  0000 C CNN
	1    8700 1450
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR104
U 1 1 579990FD
P 9200 3700
F 0 "#PWR104" H 9200 3450 50  0001 C CNN
F 1 "GND" H 9200 3550 50  0000 C CNN
F 2 "" H 9200 3700 50  0000 C CNN
F 3 "" H 9200 3700 50  0000 C CNN
	1    9200 3700
	0    1    1    0   
$EndComp
$Comp
L +12V #PWR105
U 1 1 57999103
P 9200 4300
F 0 "#PWR105" H 9200 4150 50  0001 C CNN
F 1 "+12V" H 9200 4440 50  0000 C CNN
F 2 "" H 9200 4300 50  0000 C CNN
F 3 "" H 9200 4300 50  0000 C CNN
	1    9200 4300
	0    -1   -1   0   
$EndComp
$Comp
L +12V #PWR102
U 1 1 57999109
P 8700 850
F 0 "#PWR102" H 8700 700 50  0001 C CNN
F 1 "+12V" H 8700 990 50  0000 C CNN
F 2 "" H 8700 850 50  0000 C CNN
F 3 "" H 8700 850 50  0000 C CNN
	1    8700 850 
	0    1    1    0   
$EndComp
$Comp
L GND #PWR100
U 1 1 5799910F
P 8200 1600
F 0 "#PWR100" H 8200 1350 50  0001 C CNN
F 1 "GND" H 8200 1450 50  0000 C CNN
F 2 "" H 8200 1600 50  0000 C CNN
F 3 "" H 8200 1600 50  0000 C CNN
	1    8200 1600
	0    1    1    0   
$EndComp
$Comp
L R R23
U 1 1 57999115
P 9550 1150
F 0 "R23" V 9630 1150 50  0000 C CNN
F 1 "1k" V 9550 1150 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 9480 1150 50  0001 C CNN
F 3 "" H 9550 1150 50  0000 C CNN
	1    9550 1150
	0    1    1    0   
$EndComp
$Comp
L SPST SW4
U 1 1 5799911C
P 9800 1900
F 0 "SW4" H 9800 2000 50  0000 C CNN
F 1 "SPST" H 9800 1800 50  0000 C CNN
F 2 "Buttons_Switches_ThroughHole:SW_DIP_x1_Slide" H 9800 1900 50  0001 C CNN
F 3 "" H 9800 1900 50  0000 C CNN
	1    9800 1900
	0    1    1    0   
$EndComp
Text GLabel 9700 1150 2    60   Input ~ 0
V_CONTROL1
$Comp
L R R25
U 1 1 57999124
P 9650 2400
F 0 "R25" V 9730 2400 50  0000 C CNN
F 1 "1k" V 9650 2400 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 9580 2400 50  0001 C CNN
F 3 "" H 9650 2400 50  0000 C CNN
	1    9650 2400
	0    1    1    0   
$EndComp
$Comp
L GND #PWR106
U 1 1 5799912B
P 9500 2400
F 0 "#PWR106" H 9500 2150 50  0001 C CNN
F 1 "GND" H 9500 2250 50  0000 C CNN
F 2 "" H 9500 2400 50  0000 C CNN
F 3 "" H 9500 2400 50  0000 C CNN
	1    9500 2400
	-1   0    0    1   
$EndComp
$Comp
L R R21
U 1 1 57999131
P 8650 4000
F 0 "R21" V 8730 4000 50  0000 C CNN
F 1 "20k" V 8650 4000 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 8580 4000 50  0001 C CNN
F 3 "" H 8650 4000 50  0000 C CNN
	1    8650 4000
	0    -1   -1   0   
$EndComp
$Comp
L R R20
U 1 1 57999138
P 8350 4000
F 0 "R20" V 8430 4000 50  0000 C CNN
F 1 "1k" V 8350 4000 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 8280 4000 50  0001 C CNN
F 3 "" H 8350 4000 50  0000 C CNN
	1    8350 4000
	0    -1   -1   0   
$EndComp
$Comp
L SPST SW3
U 1 1 5799913F
P 8200 3500
F 0 "SW3" H 8200 3600 50  0000 C CNN
F 1 "SPST" H 8200 3400 50  0000 C CNN
F 2 "Buttons_Switches_ThroughHole:SW_DIP_x1_Slide" H 8200 3500 50  0001 C CNN
F 3 "" H 8200 3500 50  0000 C CNN
	1    8200 3500
	0    -1   -1   0   
$EndComp
Text GLabel 8200 4000 0    60   Input ~ 0
I_CONTROL1
$Comp
L R R17
U 1 1 57999147
P 8350 3000
F 0 "R17" V 8430 3000 50  0000 C CNN
F 1 "1k" V 8350 3000 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 8280 3000 50  0001 C CNN
F 3 "" H 8350 3000 50  0000 C CNN
	1    8350 3000
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR101
U 1 1 5799914E
P 8500 3000
F 0 "#PWR101" H 8500 2750 50  0001 C CNN
F 1 "GND" H 8500 2850 50  0000 C CNN
F 2 "" H 8500 3000 50  0000 C CNN
F 3 "" H 8500 3000 50  0000 C CNN
	1    8500 3000
	1    0    0    -1  
$EndComp
$Comp
L R R24
U 1 1 57999154
P 9550 3550
F 0 "R24" V 9630 3550 50  0000 C CNN
F 1 "20k" V 9550 3550 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 9480 3550 50  0001 C CNN
F 3 "" H 9550 3550 50  0000 C CNN
	1    9550 3550
	0    1    1    0   
$EndComp
$Comp
L GND #PWR107
U 1 1 5799915B
P 9700 3550
F 0 "#PWR107" H 9700 3300 50  0001 C CNN
F 1 "GND" H 9700 3400 50  0000 C CNN
F 2 "" H 9700 3550 50  0000 C CNN
F 3 "" H 9700 3550 50  0000 C CNN
	1    9700 3550
	0    -1   -1   0   
$EndComp
Text GLabel 4650 1000 0    60   Input ~ 0
V_OUT2
Text GLabel 6200 4050 2    60   Input ~ 0
I_OUT2
$Comp
L R R10
U 1 1 57999163
P 5400 1100
F 0 "R10" V 5480 1100 50  0000 C CNN
F 1 "20k" V 5400 1100 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 5330 1100 50  0001 C CNN
F 3 "" H 5400 1100 50  0000 C CNN
	1    5400 1100
	0    1    1    0   
$EndComp
$Comp
L R R6
U 1 1 5799916A
P 4500 1550
F 0 "R6" V 4580 1550 50  0000 C CNN
F 1 "20k" V 4500 1550 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 4430 1550 50  0001 C CNN
F 3 "" H 4500 1550 50  0000 C CNN
	1    4500 1550
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR94
U 1 1 57999171
P 4850 1400
F 0 "#PWR94" H 4850 1150 50  0001 C CNN
F 1 "GND" H 4850 1250 50  0000 C CNN
F 2 "" H 4850 1400 50  0000 C CNN
F 3 "" H 4850 1400 50  0000 C CNN
	1    4850 1400
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR97
U 1 1 57999177
P 6000 3650
F 0 "#PWR97" H 6000 3400 50  0001 C CNN
F 1 "GND" H 6000 3500 50  0000 C CNN
F 2 "" H 6000 3650 50  0000 C CNN
F 3 "" H 6000 3650 50  0000 C CNN
	1    6000 3650
	0    1    1    0   
$EndComp
$Comp
L +12V #PWR98
U 1 1 5799917D
P 6000 4250
F 0 "#PWR98" H 6000 4100 50  0001 C CNN
F 1 "+12V" H 6000 4390 50  0000 C CNN
F 2 "" H 6000 4250 50  0000 C CNN
F 3 "" H 6000 4250 50  0000 C CNN
	1    6000 4250
	0    1    1    0   
$EndComp
$Comp
L +12V #PWR93
U 1 1 57999183
P 4850 800
F 0 "#PWR93" H 4850 650 50  0001 C CNN
F 1 "+12V" H 4850 940 50  0000 C CNN
F 2 "" H 4850 800 50  0000 C CNN
F 3 "" H 4850 800 50  0000 C CNN
	1    4850 800 
	0    1    1    0   
$EndComp
$Comp
L GND #PWR92
U 1 1 57999189
P 4350 1550
F 0 "#PWR92" H 4350 1300 50  0001 C CNN
F 1 "GND" H 4350 1400 50  0000 C CNN
F 2 "" H 4350 1550 50  0000 C CNN
F 3 "" H 4350 1550 50  0000 C CNN
	1    4350 1550
	0    1    1    0   
$EndComp
$Comp
L R R13
U 1 1 5799918F
P 5700 1100
F 0 "R13" V 5780 1100 50  0000 C CNN
F 1 "1k" V 5700 1100 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 5630 1100 50  0001 C CNN
F 3 "" H 5700 1100 50  0000 C CNN
	1    5700 1100
	0    1    1    0   
$EndComp
$Comp
L SPST SW2
U 1 1 57999196
P 5850 1600
F 0 "SW2" H 5850 1700 50  0000 C CNN
F 1 "SPST" H 5850 1500 50  0000 C CNN
F 2 "Buttons_Switches_ThroughHole:SW_DIP_x1_Slide" H 5850 1600 50  0001 C CNN
F 3 "" H 5850 1600 50  0000 C CNN
	1    5850 1600
	0    1    1    0   
$EndComp
Text GLabel 5850 1100 2    60   Input ~ 0
V_CONTROL2
$Comp
L R R14
U 1 1 5799919E
P 5700 2100
F 0 "R14" V 5780 2100 50  0000 C CNN
F 1 "1k" V 5700 2100 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 5630 2100 50  0001 C CNN
F 3 "" H 5700 2100 50  0000 C CNN
	1    5700 2100
	0    1    1    0   
$EndComp
$Comp
L GND #PWR96
U 1 1 579991A5
P 5550 2100
F 0 "#PWR96" H 5550 1850 50  0001 C CNN
F 1 "GND" H 5550 1950 50  0000 C CNN
F 2 "" H 5550 2100 50  0000 C CNN
F 3 "" H 5550 2100 50  0000 C CNN
	1    5550 2100
	-1   0    0    1   
$EndComp
$Comp
L R R12
U 1 1 579991AB
P 5450 3950
F 0 "R12" V 5530 3950 50  0000 C CNN
F 1 "20k" V 5450 3950 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 5380 3950 50  0001 C CNN
F 3 "" H 5450 3950 50  0000 C CNN
	1    5450 3950
	0    -1   -1   0   
$EndComp
$Comp
L R R9
U 1 1 579991B2
P 5150 3950
F 0 "R9" V 5230 3950 50  0000 C CNN
F 1 "1k" V 5150 3950 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 5080 3950 50  0001 C CNN
F 3 "" H 5150 3950 50  0000 C CNN
	1    5150 3950
	0    -1   -1   0   
$EndComp
$Comp
L SPST SW1
U 1 1 579991B9
P 5000 3450
F 0 "SW1" H 5000 3550 50  0000 C CNN
F 1 "SPST" H 5000 3350 50  0000 C CNN
F 2 "Buttons_Switches_ThroughHole:SW_DIP_x1_Slide" H 5000 3450 50  0001 C CNN
F 3 "" H 5000 3450 50  0000 C CNN
	1    5000 3450
	0    -1   -1   0   
$EndComp
Text GLabel 5000 3950 0    60   Input ~ 0
I_CONTROL2
$Comp
L R R7
U 1 1 579991C1
P 5150 2950
F 0 "R7" V 5230 2950 50  0000 C CNN
F 1 "1k" V 5150 2950 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 5080 2950 50  0001 C CNN
F 3 "" H 5150 2950 50  0000 C CNN
	1    5150 2950
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR95
U 1 1 579991C8
P 5300 2950
F 0 "#PWR95" H 5300 2700 50  0001 C CNN
F 1 "GND" H 5300 2800 50  0000 C CNN
F 2 "" H 5300 2950 50  0000 C CNN
F 3 "" H 5300 2950 50  0000 C CNN
	1    5300 2950
	1    0    0    -1  
$EndComp
$Comp
L R R15
U 1 1 579991CE
P 6350 3500
F 0 "R15" V 6430 3500 50  0000 C CNN
F 1 "20k" V 6350 3500 50  0000 C CNN
F 2 "Resistors_SMD:R_0603" V 6280 3500 50  0001 C CNN
F 3 "" H 6350 3500 50  0000 C CNN
	1    6350 3500
	0    1    1    0   
$EndComp
$Comp
L GND #PWR99
U 1 1 579991D5
P 6500 3500
F 0 "#PWR99" H 6500 3250 50  0001 C CNN
F 1 "GND" H 6500 3350 50  0000 C CNN
F 2 "" H 6500 3500 50  0000 C CNN
F 3 "" H 6500 3500 50  0000 C CNN
	1    6500 3500
	0    -1   -1   0   
$EndComp
$Comp
L LM324N U2
U 1 1 579991DB
P 4950 1100
F 0 "U2" H 5050 1250 50  0000 C CNN
F 1 "LM324N" H 5100 900 50  0000 C CNN
F 2 "SMD_Packages:SOIC-14_N" H 4900 1200 50  0001 C CNN
F 3 "" H 5000 1300 50  0000 C CNN
	1    4950 1100
	1    0    0    -1  
$EndComp
$Comp
L LM324N U2
U 2 1 579991E2
P 5900 3950
F 0 "U2" H 6000 4100 50  0000 C CNN
F 1 "LM324N" H 6050 3750 50  0000 C CNN
F 2 "SMD_Packages:SOIC-14_N" H 5850 4050 50  0001 C CNN
F 3 "" H 5950 4150 50  0000 C CNN
	2    5900 3950
	-1   0    0    1   
$EndComp
$Comp
L LM324N U1
U 2 1 579991E9
P 9100 4000
F 0 "U1" H 9150 4200 50  0000 C CNN
F 1 "LM324N" H 9250 3800 50  0000 C CNN
F 2 "SMD_Packages:SOIC-14_N" H 9050 4100 50  0001 C CNN
F 3 "" H 9150 4200 50  0000 C CNN
	2    9100 4000
	-1   0    0    1   
$EndComp
Wire Wire Line
	1900 3950 1900 3850
Wire Wire Line
	1900 3850 1800 3850
Wire Wire Line
	1950 3250 1950 3150
Wire Wire Line
	1950 3150 1850 3150
Wire Wire Line
	1950 2350 1950 2250
Wire Wire Line
	1950 2250 1850 2250
Wire Wire Line
	1950 1650 1950 1550
Wire Wire Line
	1950 1550 1850 1550
Wire Wire Line
	8500 1250 8500 1600
Wire Wire Line
	9400 1600 9400 1150
Connection ~ 9400 1150
Connection ~ 8500 1600
Connection ~ 1900 3850
Connection ~ 1950 3150
Connection ~ 1950 2250
Connection ~ 1950 1550
Connection ~ 9700 1150
Wire Wire Line
	8500 3550 8500 4000
Connection ~ 8500 4000
Connection ~ 8200 4000
Wire Wire Line
	8500 1600 9400 1600
Wire Wire Line
	9400 3900 9400 3550
Connection ~ 9400 3550
Wire Wire Line
	9400 3550 8500 3550
Wire Wire Line
	4650 1200 4650 1550
Wire Wire Line
	5550 1550 5550 1100
Connection ~ 5550 1100
Connection ~ 4650 1550
Connection ~ 5850 1100
Wire Wire Line
	5300 3500 5300 3950
Connection ~ 5300 3950
Connection ~ 5000 3950
Wire Wire Line
	4650 1550 5550 1550
Wire Wire Line
	6200 3850 6200 3500
Connection ~ 6200 3500
Wire Wire Line
	6200 3500 5300 3500
$EndSCHEMATC
