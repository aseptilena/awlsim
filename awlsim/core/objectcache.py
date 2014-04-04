# -*- coding: utf-8 -*-
#
# Generic object cache
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

class ObjectCache(object):
	def __init__(self, createCallback):
		self.__createCallback = createCallback
		self.reset()

	def get(self, callbackData=None):
		try:
			return self.__cache.pop()
		except IndexError:
			return self.__createCallback(callbackData)

	def put(self, obj):
		self.__cache.append(obj)

	def reset(self):
		self.__cache = []