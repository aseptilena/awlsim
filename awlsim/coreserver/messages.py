# -*- coding: utf-8 -*-
#
# AWL simulator - PLC core server messages
#
# Copyright 2013 Michael Buesch <m@bues.ch>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#

from awlsim.util import *
from awlsim.cpuspecs import *

import struct
import socket
import errno


class TransferError(Exception):
	pass

class AwlSimMessage(object):
	# Header format:
	#	Magic (16 bit)
	#	Message ID (16 bit)
	#	Sequence count (16 bit)
	#	Reserved (16 bit)
	#	Payload length (32 bit)
	#	Payload (optional)
	hdrStruct = struct.Struct(">HHHHI")

	HDR_MAGIC		= 0x5710
	HDR_LENGTH		= hdrStruct.size

	enum.start
	MSG_ID_REPLY		= enum.item # Generic status reply
	MSG_ID_EXCEPTION	= enum.item
	MSG_ID_PING		= enum.item
	MSG_ID_PONG		= enum.item
	MSG_ID_RUNSTATE		= enum.item
	MSG_ID_LOAD_CODE	= enum.item
	MSG_ID_LOAD_HW		= enum.item
	MSG_ID_SET_OPT		= enum.item
	MSG_ID_CPUDUMP		= enum.item
	MSG_ID_MAINTREQ		= enum.item
	MSG_ID_GET_CPUSPECS	= enum.item
	MSG_ID_CPUSPECS		= enum.item
	enum.end

	_strLenStruct = struct.Struct(">H")

	@classmethod
	def packString(cls, string):
		try:
			data = string.encode("utf-8", "strict")
			return cls._strLenStruct.pack(len(data)) + data
		except (UnicodeError, struct.error) as e:
			raise ValueError

	@classmethod
	def unpackString(cls, data, offset = 0):
		try:
			(length, ) = cls._strLenStruct.unpack_from(data, offset)
			strBytes = data[offset + cls._strLenStruct.size :
					offset + cls._strLenStruct.size + length]
			if len(strBytes) != length:
				raise ValueError
			return (strBytes.decode("utf-8", "strict"),
				cls._strLenStruct.size + length)
		except (UnicodeError, struct.error) as e:
			raise ValueError

	def __init__(self, msgId, seq=0):
		self.msgId = msgId
		self.seq = seq

	def toBytes(self, payloadLength=0):
		return self.hdrStruct.pack(self.HDR_MAGIC,
					   self.msgId,
					   self.seq,
					   0,
					   payloadLength)

	@classmethod
	def fromBytes(cls, payload):
		return cls()

class AwlSimMessage_REPLY(AwlSimMessage):
	enum.start
	STAT_OK		= enum.item
	STAT_FAIL	= enum.item
	enum.end

	plStruct = struct.Struct(">HHH")

	@classmethod
	def make(cls, inReplyToMsg, status):
		return cls(inReplyToMsg.msgId, inReplyToMsg.seq, status)

	def __init__(self, inReplyToId, inReplyToSeq, status):
		AwlSimMessage.__init__(self, AwlSimMessage.MSG_ID_REPLY)
		self.inReplyToId = inReplyToId
		self.inReplyToSeq = inReplyToSeq
		self.status = status

	def toBytes(self):
		pl = self.plStruct.pack(self.inReplyToId,
					self.inReplyToSeq,
					self.status)
		return AwlSimMessage.toBytes(self, len(pl)) + pl

	@classmethod
	def fromBytes(cls, payload):
		try:
			inReplyToId, inReplyToSeq, status =\
				cls.plStruct.unpack(payload)
		except struct.error as e:
			raise TransferError("REPLY: Invalid data format")
		return cls(inReplyToId, inReplyToSeq, status)

class AwlSimMessage_PING(AwlSimMessage):
	def __init__(self):
		AwlSimMessage.__init__(self, AwlSimMessage.MSG_ID_PING)

class AwlSimMessage_PONG(AwlSimMessage):
	def __init__(self):
		AwlSimMessage.__init__(self, AwlSimMessage.MSG_ID_PONG)

class AwlSimMessage_RUNSTATE(AwlSimMessage):
	enum.start
	STATE_STOP	= enum.item
	STATE_RUN	= enum.item
	enum.end

	plStruct = struct.Struct(">H")

	def __init__(self, runState):
		AwlSimMessage.__init__(self, AwlSimMessage.MSG_ID_RUNSTATE)
		self.runState = runState

	def toBytes(self):
		pl = self.plStruct.pack(self.runState)
		return AwlSimMessage.toBytes(self, len(pl)) + pl

	@classmethod
	def fromBytes(cls, payload):
		try:
			(runState, ) = cls.plStruct.unpack(payload)
		except struct.error as e:
			raise TransferError("RUNSTATE: Invalid data format")
		return cls(runState)

class AwlSimMessage_EXCEPTION(AwlSimMessage):
	def __init__(self, exceptionText):
		AwlSimMessage.__init__(self, AwlSimMessage.MSG_ID_EXCEPTION)
		self.exceptionText = exceptionText

	def toBytes(self):
		try:
			textBytes = self.exceptionText.encode()
			return AwlSimMessage.toBytes(self, len(textBytes)) + textBytes
		except UnicodeError:
			raise TransferError("EXCEPTION: Unicode error")

	@classmethod
	def fromBytes(cls, payload):
		try:
			text = payload.decode()
		except UnicodeError:
			raise TransferError("EXCEPTION: Unicode error")
		return cls(text)

class AwlSimMessage_LOAD_CODE(AwlSimMessage):
	def __init__(self, code):
		AwlSimMessage.__init__(self, AwlSimMessage.MSG_ID_LOAD_CODE)
		self.code = code

	def toBytes(self):
		try:
			code = self.code.encode()
			return AwlSimMessage.toBytes(self, len(code)) + code
		except UnicodeError:
			raise TransferError("LOAD_CODE: Unicode error")

	@classmethod
	def fromBytes(cls, payload):
		try:
			code = payload.decode()
		except UnicodeError:
			raise TransferError("LOAD_CODE: Unicode error")
		return cls(code)

class AwlSimMessage_LOAD_HW(AwlSimMessage):
	def __init__(self, name, paramDict):
		AwlSimMessage.__init__(self, AwlSimMessage.MSG_ID_LOAD_HW)
		self.name = name
		self.paramDict = paramDict

	def toBytes(self):
		payload = b""
		try:
			payload += self.packString(self.name)
			for pname, pval in self.paramDict.items():
				payload += self.packString(pname)
				payload += self.packString(pval)
			return AwlSimMessage.toBytes(self, len(payload)) + payload
		except (ValueError) as e:
			raise TransferError("LOAD_HW: Invalid data format")

	@classmethod
	def fromBytes(cls, payload):
		paramDict = {}
		offset = 0
		try:
			name, count = cls.unpackString(payload, offset)
			offset += count
			while offset < len(payload):
				pname, count = cls.unpackString(payload, offset)
				offset += count
				pval, count = cls.unpackString(payload, offset)
				offset += count
				paramDict[pname] = pval
		except (ValueError) as e:
			raise TransferError("LOAD_HW: Invalid data format")
		return cls(name = name, paramDict = paramDict)

class AwlSimMessage_SET_OPT(AwlSimMessage):
	def __init__(self, name, value):
		AwlSimMessage.__init__(self, AwlSimMessage.MSG_ID_SET_OPT)
		self.name = name
		self.value = value

	def getIntValue(self):
		try:
			return int(self.value)
		except ValueError as e:
			raise AwlSimError("SET_OPT: Value is not an integer")

	def getBoolValue(self):
		try:
			return bool(self.value)
		except ValueError as e:
			raise AwlSimError("SET_OPT: Value is not a boolean")

	def toBytes(self):
		try:
			payload = self.packString(self.name)
			payload += self.packString(self.value)
		except ValueError as e:
			raise TransferError("SET_OPT: Invalid data format")
		return AwlSimMessage.toBytes(self, len(payload)) + payload

	@classmethod
	def fromBytes(cls, payload):
		try:
			offset = 0
			name, count = cls.unpackString(payload, offset)
			offset += count
			value, count = cls.unpackString(payload, offset)
			offset += count
		except ValueError as e:
			raise TransferError("SET_OPT: Invalid data format")
		return cls(name = name, value = value)

class AwlSimMessage_CPUDUMP(AwlSimMessage):
	def __init__(self, dumpText):
		AwlSimMessage.__init__(self, AwlSimMessage.MSG_ID_CPUDUMP)
		self.dumpText = dumpText

	def toBytes(self):
		try:
			dumpBytes = self.dumpText.encode()
			return AwlSimMessage.toBytes(self, len(dumpBytes)) + dumpBytes
		except UnicodeError:
			raise TransferError("CPUDUMP: Unicode error")

	@classmethod
	def fromBytes(cls, payload):
		try:
			dumpText = payload.decode()
		except UnicodeError:
			raise TransferError("CPUDUMP: Unicode error")
		return cls(dumpText)

class AwlSimMessage_MAINTREQ(AwlSimMessage):
	plStruct = struct.Struct(">H")

	def __init__(self, requestType):
		AwlSimMessage.__init__(self, AwlSimMessage.MSG_ID_MAINTREQ)
		self.requestType = requestType

	def toBytes(self):
		pl = self.plStruct.pack(self.requestType)
		return AwlSimMessage.toBytes(self, len(pl)) + pl

	@classmethod
	def fromBytes(cls, payload):
		try:
			(requestType, ) = cls.plStruct.unpack(payload)
		except struct.error as e:
			raise TransferError("MAINTREQ: Invalid data format")
		return cls(requestType)

class AwlSimMessage_GET_CPUSPECS(AwlSimMessage):
	def __init__(self):
		AwlSimMessage.__init__(self, AwlSimMessage.MSG_ID_GET_CPUSPECS)

class AwlSimMessage_CPUSPECS(AwlSimMessage):
	plStruct = struct.Struct(">32I")

	def __init__(self, cpuspecs):
		AwlSimMessage.__init__(self, AwlSimMessage.MSG_ID_CPUSPECS)
		self.cpuspecs = cpuspecs
		self.cpuspecs.cpu = None

	def toBytes(self):
		pl = self.plStruct.pack(self.cpuspecs.getConfiguredMnemonics(),
					self.cpuspecs.nrAccus,
					self.cpuspecs.nrTimers,
					self.cpuspecs.nrCounters,
					self.cpuspecs.nrFlags,
					self.cpuspecs.nrInputs,
					self.cpuspecs.nrOutputs,
					self.cpuspecs.nrLocalbytes,
					*( (0,) * 24 ) # padding
		)
		return AwlSimMessage.toBytes(self, len(pl)) + pl

	@classmethod
	def fromBytes(cls, payload):
		try:
			data = cls.plStruct.unpack(payload)
			(mnemonics, nrAccus, nrTimers,
			 nrCounters, nrFlags, nrInputs,
			 nrOutputs, nrLocalbytes) = data[:8]
		except struct.error as e:
			raise TransferError("CPUSPECS: Invalid data format")
		cpuspecs = S7CPUSpecs()
		cpuspecs.setConfiguredMnemonics(mnemonics)
		cpuspecs.setNrAccus(nrAccus)
		cpuspecs.setNrTimers(nrTimers)
		cpuspecs.setNrCounters(nrCounters)
		cpuspecs.setNrFlags(nrFlags)
		cpuspecs.setNrInputs(nrInputs)
		cpuspecs.setNrOutputs(nrOutputs)
		cpuspecs.setNrLocalbytes(nrLocalbytes)
		return cls(cpuspecs)

class AwlSimMessageTransceiver(object):
	class RemoteEndDied(Exception): pass

	id2class = {
		AwlSimMessage.MSG_ID_REPLY		: AwlSimMessage_REPLY,
		AwlSimMessage.MSG_ID_EXCEPTION		: AwlSimMessage_EXCEPTION,
		AwlSimMessage.MSG_ID_PING		: AwlSimMessage_PING,
		AwlSimMessage.MSG_ID_PONG		: AwlSimMessage_PONG,
		AwlSimMessage.MSG_ID_RUNSTATE		: AwlSimMessage_RUNSTATE,
		AwlSimMessage.MSG_ID_LOAD_CODE		: AwlSimMessage_LOAD_CODE,
		AwlSimMessage.MSG_ID_LOAD_HW		: AwlSimMessage_LOAD_HW,
		AwlSimMessage.MSG_ID_SET_OPT		: AwlSimMessage_SET_OPT,
		AwlSimMessage.MSG_ID_CPUDUMP		: AwlSimMessage_CPUDUMP,
		AwlSimMessage.MSG_ID_MAINTREQ		: AwlSimMessage_MAINTREQ,
		AwlSimMessage.MSG_ID_GET_CPUSPECS	: AwlSimMessage_GET_CPUSPECS,
		AwlSimMessage.MSG_ID_CPUSPECS		: AwlSimMessage_CPUSPECS,
	}

	def __init__(self, sock):
		self.sock = sock

		# Transmit status
		self.txSeqCount = 0

		# Receive buffer
		self.buf = b""
		self.msgId = None
		self.seq = None
		self.payloadLen = None

		self.sock.setblocking(False)

	def send(self, msg):
		msg.seq = self.txSeqCount
		self.txSeqCount = (self.txSeqCount + 1) & 0xFFFF

		offset, data = 0, msg.toBytes()
		while offset < len(data):
			try:
				offset += self.sock.send(data[offset : ])
			except socket.error as e:
				if e.errno != errno.EAGAIN:
					raise TransferError(str(e))

	def receive(self):
		hdrLen = AwlSimMessage.HDR_LENGTH
		if len(self.buf) < hdrLen:
			data = self.sock.recv(hdrLen - len(self.buf))
			if not data:
				# The remote end closed the connection
				raise self.RemoteEndDied()
			self.buf += data
			if len(self.buf) < hdrLen:
				return None
			try:
				magic, self.msgId, self.seq, _reserved, self.payloadLen =\
					AwlSimMessage.hdrStruct.unpack(self.buf)
			except struct.error as e:
				raise AwlSimError("Received message with invalid "
					"header format.")
			if magic != AwlSimMessage.HDR_MAGIC:
				raise AwlSimError("Received message with invalid "
					"magic value (was 0x%04X, expected 0x%04X)." %\
					(magic, AwlSimMessage.HDR_MAGIC))
			if self.payloadLen:
				return None
		if len(self.buf) < hdrLen + self.payloadLen:
			data = self.sock.recv(hdrLen + self.payloadLen - len(self.buf))
			if not data:
				# The remote end closed the connection
				raise self.RemoteEndDied()
			self.buf += data
			if len(self.buf) < hdrLen + self.payloadLen:
				return None
		try:
			cls = self.id2class[self.msgId]
		except KeyError:
			raise AwlSimError("Received unknown message: 0x%04X" %\
				self.msgId)
		msg = cls.fromBytes(self.buf[hdrLen : ])
		msg.seq = self.seq
		self.buf, self.msgId, self.seq, self.payloadLen = b"", None, None, None
		return msg

	def receiveBlocking(self, timeoutSec=None):
		try:
			self.sock.settimeout(timeoutSec)
			msg = self.receive()
		except socket.timeout:
			return None
		finally:
			self.sock.setblocking(False)
		return msg