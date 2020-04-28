EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr User 5906 4724
encoding utf-8
Sheet 1 1
Title "CatBit"
Date "2020-04-27"
Rev "0.1"
Comp "easytarget.org"
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Regulator_Linear:LD1117S33TR_SOT223 U1
U 1 1 5EA77872
P 2150 2300
F 0 "U1" H 2150 2542 50  0000 C CNN
F 1 "LD33" H 2150 2451 50  0000 C CNN
F 2 "Package_TO_SOT_THT:TO-220-3_Vertical" H 2150 2500 50  0001 C CNN
F 3 "http://www.st.com/st-web-ui/static/active/en/resource/technical/document/datasheet/CD00000544.pdf" H 2250 2050 50  0001 C CNN
	1    2150 2300
	1    0    0    -1  
$EndComp
$Comp
L Transistor_FET:2N7000 Q1
U 1 1 5EA78FB1
P 1300 1300
F 0 "Q1" H 1505 1346 50  0000 L CNN
F 1 "2N7000" H 1505 1255 50  0000 L CNN
F 2 "Package_TO_SOT_THT:TO-92_Inline_Wide" H 1500 1225 50  0001 L CIN
F 3 "https://www.fairchildsemi.com/datasheets/2N/2N7000.pdf" H 1300 1300 50  0001 L CNN
	1    1300 1300
	-1   0    0    -1  
$EndComp
$Comp
L Device:R R2
U 1 1 5EA7A163
P 1600 1500
F 0 "R2" H 1530 1454 50  0000 R CNN
F 1 "10K" H 1530 1545 50  0000 R CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 1530 1500 50  0001 C CNN
F 3 "~" H 1600 1500 50  0001 C CNN
	1    1600 1500
	-1   0    0    1   
$EndComp
$Comp
L Device:R R1
U 1 1 5EA7A7ED
P 1850 1300
F 0 "R1" V 2057 1300 50  0000 C CNN
F 1 "220R" V 1966 1300 50  0000 C CNN
F 2 "Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal" V 1780 1300 50  0001 C CNN
F 3 "~" H 1850 1300 50  0001 C CNN
	1    1850 1300
	0    -1   -1   0   
$EndComp
$Comp
L Device:CP C2
U 1 1 5EA7B32E
P 2650 2450
F 0 "C2" H 2768 2496 50  0000 L CNN
F 1 "100uF" H 2768 2405 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D6.3mm_P2.50mm" H 2688 2300 50  0001 C CNN
F 3 "~" H 2650 2450 50  0001 C CNN
	1    2650 2450
	1    0    0    -1  
$EndComp
$Comp
L Device:CP C1
U 1 1 5EA7BD3B
P 1450 2450
F 0 "C1" H 1568 2496 50  0000 L CNN
F 1 "10uF" H 1568 2405 50  0000 L CNN
F 2 "Capacitor_THT:CP_Radial_D5.0mm_P2.50mm" H 1488 2300 50  0001 C CNN
F 3 "~" H 1450 2450 50  0001 C CNN
	1    1450 2450
	1    0    0    -1  
$EndComp
$Comp
L Connector_Generic:Conn_01x02 J4
U 1 1 5EA7C88F
P 900 2400
F 0 "J4" H 818 2075 50  0000 C CNN
F 1 "5V DC in" H 818 2166 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 900 2400 50  0001 C CNN
F 3 "~" H 900 2400 50  0001 C CNN
	1    900  2400
	-1   0    0    1   
$EndComp
Wire Wire Line
	1100 2400 1100 2600
Wire Wire Line
	1100 2600 1450 2600
Wire Wire Line
	2150 2600 2650 2600
Connection ~ 2150 2600
Wire Wire Line
	1100 2300 1300 2300
Connection ~ 1450 2300
Wire Wire Line
	2450 2300 2650 2300
Text GLabel 3200 2300 2    50   Output ~ 0
3V
Text GLabel 3200 2600 2    50   Output ~ 0
GND
$Comp
L Connector_Generic:Conn_01x02 J1
U 1 1 5EA860B1
P 900 1000
F 0 "J1" H 818 675 50  0000 C CNN
F 1 "5V LED Laser" H 818 766 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x02_P2.54mm_Vertical" H 900 1000 50  0001 C CNN
F 3 "~" H 900 1000 50  0001 C CNN
	1    900  1000
	-1   0    0    1   
$EndComp
$Comp
L Connector_Generic:Conn_01x03 J2
U 1 1 5EA86C4D
P 3000 1000
F 0 "J2" H 2918 675 50  0000 C CNN
F 1 "ServoX" H 2918 766 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 3000 1000 50  0001 C CNN
F 3 "~" H 3000 1000 50  0001 C CNN
	1    3000 1000
	-1   0    0    1   
$EndComp
Text GLabel 1400 2050 2    50   Output ~ 0
5V
Wire Wire Line
	1400 2050 1300 2050
Wire Wire Line
	1300 2050 1300 2300
Connection ~ 1300 2300
Wire Wire Line
	1300 2300 1450 2300
Text GLabel 2100 900  2    50   Input ~ 0
5V
Wire Wire Line
	1200 1000 1200 1100
Wire Wire Line
	1500 1300 1600 1300
Wire Wire Line
	1600 1300 1600 1350
Connection ~ 1600 1300
Wire Wire Line
	1600 1300 1700 1300
Wire Wire Line
	1200 1500 1200 1700
Wire Wire Line
	1200 1700 1600 1700
Wire Wire Line
	1600 1700 1600 1650
Text GLabel 2100 1700 2    50   Input ~ 0
GND
Connection ~ 1600 1700
Text GLabel 2100 1300 2    50   Input ~ 0
LASER
Wire Wire Line
	1600 1700 2100 1700
Wire Wire Line
	2000 1300 2100 1300
Wire Wire Line
	1100 1000 1200 1000
Wire Wire Line
	1100 900  2100 900 
Text GLabel 3300 1000 2    50   Input ~ 0
5V
Text GLabel 3300 1750 2    50   Input ~ 0
5V
Text GLabel 3300 1850 2    50   Input ~ 0
GND
Text GLabel 3300 1100 2    50   Input ~ 0
GND
Text GLabel 3300 900  2    50   Input ~ 0
X
Text GLabel 3300 1650 2    50   Input ~ 0
Y
Wire Wire Line
	3200 900  3300 900 
Wire Wire Line
	3200 1000 3300 1000
Wire Wire Line
	3200 1100 3300 1100
Wire Wire Line
	3200 1650 3300 1650
Wire Wire Line
	3200 1750 3300 1750
Wire Wire Line
	3200 1850 3300 1850
Wire Wire Line
	2650 2600 3200 2600
Connection ~ 2650 2600
Wire Wire Line
	2650 2300 3200 2300
Connection ~ 2650 2300
Wire Wire Line
	1450 2300 1850 2300
Wire Wire Line
	1450 2600 2150 2600
Connection ~ 1450 2600
$Comp
L microbit:BBC-MicroBit BIT1
U 1 1 5EA74BB3
P 4800 1650
F 0 "BIT1" H 4700 2400 50  0000 L CNN
F 1 "BBC-MicroBit" H 4550 2300 50  0000 L CNN
F 2 "catbit:MicroBit" H 5000 1650 50  0001 C CNN
F 3 "" H 5000 1650 50  0001 C CNN
	1    4800 1650
	1    0    0    -1  
$EndComp
Wire Wire Line
	4250 1150 4350 1150
Wire Wire Line
	4250 1400 4350 1400
Wire Wire Line
	4250 1650 4350 1650
Text GLabel 4250 1650 0    50   Output ~ 0
LASER
Text GLabel 4250 1400 0    50   Output ~ 0
Y
Text GLabel 4250 1150 0    50   Output ~ 0
X
Wire Wire Line
	4250 2150 4350 2150
Wire Wire Line
	4250 1900 4350 1900
Text GLabel 4250 2150 0    50   Input ~ 0
GND
Text GLabel 4250 1900 0    50   Input ~ 0
3V
$Comp
L Connector_Generic:Conn_01x03 J3
U 1 1 5EA87483
P 3000 1750
F 0 "J3" H 2950 1400 50  0000 C CNN
F 1 "ServoY" H 2900 1500 50  0000 C CNN
F 2 "Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical" H 3000 1750 50  0001 C CNN
F 3 "~" H 3000 1750 50  0001 C CNN
	1    3000 1750
	-1   0    0    1   
$EndComp
$EndSCHEMATC
