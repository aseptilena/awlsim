# -*- coding: utf-8 -*-
#
# AWL simulator - instructions
#
# Copyright 2012-2013 Michael Buesch <m@bues.ch>
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

from awlsim.instructions.main import *


class AwlInsn_FP(AwlInsn):
	def __init__(self, cpu, rawInsn):
		AwlInsn.__init__(self, cpu, AwlInsn.TYPE_FP, rawInsn)
		self.assertOpCount(1)

	def run(self):
		s = self.cpu.callStackTop.status
		fm = self.cpu.fetch(self.ops[0], (1,))
		self.cpu.store(self.ops[0], s.VKE, (1,))
		s.OR, s.STA, s.NER = 0, s.VKE, 1
		s.VKE = (s.VKE & ~fm) & 1