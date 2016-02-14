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
LIBS:max485
LIBS:rv3029c2
LIBS:pilc-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 2 4
Title "PiLC HAT - RTC"
Date ""
Rev "0.1"
Comp "Michael Buesch <m@bues.ch>"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L RV-3029-C2 U1
U 1 1 56AD3564
P 5700 3600
F 0 "U1" H 5700 4200 60  0000 C CNN
F 1 "RV-3029-C2" H 5700 3000 60  0000 C CNN
F 2 "" H 5700 3150 60  0000 C CNN
F 3 "" H 5700 3150 60  0000 C CNN
	1    5700 3600
	1    0    0    -1  
$EndComp
NoConn ~ 5050 3450
$Comp
L +3V3 #PWR28
U 1 1 56AD3774
P 4850 3300
F 0 "#PWR28" H 4850 3150 50  0001 C CNN
F 1 "+3V3" H 4850 3440 50  0000 C CNN
F 2 "" H 4850 3300 60  0000 C CNN
F 3 "" H 4850 3300 60  0000 C CNN
	1    4850 3300
	0    -1   -1   0   
$EndComp
$Comp
L GND #PWR30
U 1 1 56AD378C
P 6450 3900
F 0 "#PWR30" H 6450 3650 50  0001 C CNN
F 1 "GND" H 6450 3750 50  0000 C CNN
F 2 "" H 6450 3900 60  0000 C CNN
F 3 "" H 6450 3900 60  0000 C CNN
	1    6450 3900
	0    -1   -1   0   
$EndComp
Wire Wire Line
	6350 3900 6450 3900
Wire Wire Line
	4850 3300 5050 3300
NoConn ~ 6350 3750
NoConn ~ 6350 3300
$Comp
L R R7
U 1 1 56AD3A9C
P 6950 3600
F 0 "R7" V 7030 3600 50  0000 C CNN
F 1 "100" V 6950 3600 50  0000 C CNN
F 2 "" V 6880 3600 30  0000 C CNN
F 3 "" H 6950 3600 30  0000 C CNN
	1    6950 3600
	0    1    1    0   
$EndComp
Wire Wire Line
	7100 3600 7300 3600
Wire Wire Line
	6350 3600 6800 3600
$Comp
L ZENER D2
U 1 1 56AD3B30
P 7450 3950
F 0 "D2" H 7450 4050 50  0000 C CNN
F 1 "5.1V" H 7450 3850 50  0000 C CNN
F 2 "" H 7450 3950 60  0000 C CNN
F 3 "" H 7450 3950 60  0000 C CNN
	1    7450 3950
	1    0    0    -1  
$EndComp
$Comp
L CP C5
U 1 1 56AD3B8F
P 7450 3600
F 0 "C5" H 7475 3700 50  0000 L CNN
F 1 "1F 5.5V" H 7475 3500 50  0000 L CNN
F 2 "" H 7488 3450 30  0000 C CNN
F 3 "" H 7450 3600 60  0000 C CNN
	1    7450 3600
	0    -1   -1   0   
$EndComp
Wire Wire Line
	7200 3600 7200 3950
Wire Wire Line
	7200 3950 7250 3950
Connection ~ 7200 3600
Wire Wire Line
	7650 3950 7700 3950
Wire Wire Line
	7700 3950 7700 3600
Wire Wire Line
	7600 3600 7800 3600
$Comp
L GND #PWR31
U 1 1 56AD3CCC
P 7800 3600
F 0 "#PWR31" H 7800 3350 50  0001 C CNN
F 1 "GND" H 7800 3450 50  0000 C CNN
F 2 "" H 7800 3600 60  0000 C CNN
F 3 "" H 7800 3600 60  0000 C CNN
	1    7800 3600
	0    -1   -1   0   
$EndComp
Connection ~ 7700 3600
Text HLabel 2350 3750 0    60   Input ~ 0
SCL
Text HLabel 2350 3900 0    60   Input ~ 0
SDA
Wire Wire Line
	2350 3750 5050 3750
Wire Wire Line
	2350 3900 5050 3900
$Comp
L C_Small C4
U 1 1 56C07294
P 4950 2950
F 0 "C4" H 4960 3020 50  0000 L CNN
F 1 "100n" H 4960 2870 50  0000 L CNN
F 2 "" H 4950 2950 50  0000 C CNN
F 3 "" H 4950 2950 50  0000 C CNN
	1    4950 2950
	1    0    0    -1  
$EndComp
Wire Wire Line
	4950 3050 4950 3300
Connection ~ 4950 3300
$Comp
L GND #PWR29
U 1 1 56C0744F
P 4950 2750
F 0 "#PWR29" H 4950 2500 50  0001 C CNN
F 1 "GND" H 4950 2600 50  0000 C CNN
F 2 "" H 4950 2750 50  0000 C CNN
F 3 "" H 4950 2750 50  0000 C CNN
	1    4950 2750
	-1   0    0    1   
$EndComp
Wire Wire Line
	4950 2750 4950 2850
$EndSCHEMATC
