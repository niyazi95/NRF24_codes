#coding=utf-8

#Raspi receiver
import RPi.GPIO as GPIO
from lib_nrf24 import NRF24
import time
import spidev

GPIO.setmode(GPIO.BCM)

pipes = [[0xE8, 0xE8, 0xF0, 0xF0, 0xE1], [0xF0, 0xF0, 0xF0, 0xF0, 0xF0, 0xE1]]

radio = NRF24(GPIO, spidev.SpiDev())
radio.begin(9, 10)

radio.setPayloadSize(32)
radio.setChannel(0x76)
radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)

radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openReadingPipe(1, pipes[1]) #FO FO FO olarak giden
radio.printDetails()
radio.startListening()

while True:
	while not radio.available(0) :
		time.sleep(1/100)
	
	receivedMessage = []
	radio.read(receivedMessage, radio.getDynamicPayloadSize())
	print("Received: {}".format(receivedMessage))
	
	print("Translating our receivedMessage into unicode characters...\n")
	
	string = ""
	for n in receivedMessage:
		if(n>=32 and n<=126):
			string += chr(n)
	print("Our receivedMessage decodes to: {}".format(string))


