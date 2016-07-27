from __future__ import division
import time
import socket
import struct


class Client:
	def __init__(self):
		self._host = socket.gethostname()
		self._port = 1192
		self._buffer_size = 2048

		self._tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	def connect(self):
		self._tcp_client.connect((self._host, self._port))

	def close_connection(self):
		self._tcp_client.close()

	'''
	def send_message(self, message):
		msg_length = len(message)
		self._tcp_client.send(message)

	def receive_message(self):
		return self._tcp_client.recv(self._buffer_size)
	'''

	def send_message(self, msg):
		# Prefix each message with a 4-byte length (network byte order)
		msg = struct.pack('>I', len(msg)) + msg
		self._tcp_client.sendall(msg)

		print "I'm done sending message!"

	def receive_message(self):
		# Read message length and unpack it into an integer
		raw_msglen = self.receive_all(4)
		if not raw_msglen:
			return None
		msglen = struct.unpack('>I', raw_msglen)[0]
		# Read the message data
		return self.receive_all(msglen)

	def receive_all(self, n):
		# Helper function to recv n bytes or return None if EOF is hit
		data = ''
		while len(data) < n:
			packet = self._tcp_client.recv(n - len(data))
			if not packet:
				return None
			data += packet
		return data



some_client = Client()

some_client.connect()

some_client.send_message("connect_arduino:2cc580d6-fa29-44a7-9fec-035acd72340e")

response = some_client.receive_message()
arduino_key = response.split("=")[1]

some_client.send_message("q@{}:f0,f1,f2".format(arduino_key))


some_client.close_connection()


# Messages begin with arduino id and a number of lines thing. That tells the server to pass the next N lines to that arduino.

# Or a better option would be to have a connect and disconnect message.
# Maybe have connect:<arduino id> and then the server will keep passing all messages to that arduino  until it receives a disconnect:<arduino id> message.

# Maybe have the server assign an integer, which it will tell back to the GUI, that links it to the correct arduino id?
# This way we'll always know which arduino a particular message is intended for. 
# This is important since multiple arduino messages must probably be done in parallel (kind of parallel, more like arduino 1, arduino 1, arduino 2, arduino 1, arduino 1, arduino 2, arduino 2, arduino 1)