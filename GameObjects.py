import bge
from math import *
from mathutils import Vector
from random import random
import checker

#atas = Vector((0, 1, 0))
#bawah = Vector((0, -1, 0))
#kiri = Vector((-1, 0, 0))
#kanan = Vector((1, 0, 0))

diameter = 25
maxLangkah = 7
maxRoom = 15

def acakLangkah():
	return floor(maxLangkah * random())

def intClose(value):
	if 1.0 - value < 0.5:
		return ceil(value)
	else:
		return floor(value)
		
class Vec(list):
	object = None
	'''
	def __init__(self, old_owner):
		#self.pa = len(old_owner)
		self.object = None
		for i in old_owner:
			self.append(i)
	'''
		
	
	def __add__(self, other):
		if type(other) == Vec:
			i = 0
			h = []
			while i < len(self):
				h.append(self[i] + other[i])
				i+=1
			return Vec(h)
		else:
			raise TypeError
			
	def __radd__(self, other):
		h = self.__add__(other)
		return h
		
	def __sub__(self, other):
		if type(other) == Vec:
			i = 0
			h = []
			while i < len(self):
				h.append(self[i] - other[i])
				i+=1
			return Vec(h)
		else:
			raise TypeError

atas = Vec([0,1])
bawah = Vec([0,-1])
kiri = Vec([-1,0])
kanan = Vec([1,0])

arah = [atas, bawah, kiri, kanan]

class KX_GreenBlock(bge.types.KX_GameObject):
	def __init__(self, old_owner):
		self.jalur = []
		self.v = None
		self.sebelumnya = None
		self.next = []
		
	def run(self):
		if self.sebelumnya != None:
			bge.render.drawLine(self.position, self.sebelumnya.position, [1, 1, 1])
			
	def __repr__(self):
		return "Loc <{0}>".format(str(self.v))

class KX_RedBlock(bge.types.KX_GameObject):
	def __init__(self, old_owner):
		self.sebelumnya = None
		
	def run(self):
		bge.render.drawLine(self.position, self.sebelumnya.position, [1, 1, 1])


class KX_BlockAdder(bge.types.KX_GameObject):
	def __init__(self, old_owner):
		
		self.listBlock = []
		self.usedBlock = []#kumpulan block-block yang sudah terpakai
		self.antrian = []#ujung-ujung jalur yang masigh bisa ditambahkan jalannya
		self.curBlock = None
		self.langkah = acakLangkah()
		self.step = 0
		self.generateStats = "way"
		#self.langkah = 8
		print("langkah yang diambil ialah = " + str(self.langkah))
		pa = len(arah)
		#self.arah = arah[floor(random() * pa)]
		#green_cube
		firstStart = True
		print("building the blocks. Plrease wait...")
		for x in range(diameter):
			for y in range(diameter):
				added = KX_GreenBlock(self.scene.addObject('green_cube', self))
				added.position.x = x
				added.position.y = y
				v = Vec([x, y])
				added.v = v
				v.object = added
				'''
				added.jalur.append(Vec([ x, y+1 ]))
				added.jalur.append(Vec([ x, y-1 ]))
				added.jalur.append(Vec([ x-1, y ]))
				added.jalur.append(Vec([ x+1, y ]))
				b = Vec([3,5])
				c = v+b
				cek = v, b, c
				'''
				#self.listBlock[v] = added
				self.listBlock.append(v)
				if firstStart:
					self.curBlock = v.object
					self.usedBlock.append(v.object)
					firstStart = False
				#self.listBlock[added.position] = added
				
		for added in self.listBlock:
			for i in self.listBlock:
				ada = False
				if added + atas == i:
					ada = True
				if added + bawah == i:
					ada = True
				if added + kiri == i:
					ada = True
				if added + kanan == i:
					ada = True
				
				if ada == True:
					added.object.jalur.append(i.object)
		v = self.curBlock.jalur[floor(random() * len(self.curBlock.jalur))].v
		self.arah = v - self.curBlock.v
		point = KX_RedBlock(self.scene.addObject('red_cube', self.curBlock))
		self.lastRedblock = point
		self.curBlock.visible = False
		
		
		
	def run(self):
		#cek = self.listBlock[0] - atas, self.listBlock[0], atas
		#print(cek)
		#return False
		
		try:
			if self.curBlock == None:
				#print("wew")
				pass
				#bge.logic.endGame()
				#return False#kalo nga pake ini dia bole mo bypass to error yang akan dilaksanakan script yg ada dibawah
			#print(self.curBlock)
			if self.curBlock != None:
				self.step += 1
				print(" ---------------------------- step {0} ---------------------------- ".format(str(self.step)))
				''' - cek antrian - '''
				ant = []
				for i in self.antrian:
					ant.append(i.v)
				print("antriannya ialah " + str(ant))
				''' --------------- '''
				print("currentBlocknya ialah " + str(self.curBlock.v))
				ada = False
				isUjung = False
				if self.langkah > 0:
					print("arahnya ialah " + str(self.arah))
					teredit = False
					if self.arah[0] > 1:
						self.arah[0] = int(1)
						teredit = True
					if self.arah[0] < -1:
						self.arah[0] = int(-1)
						teredit = True
					if self.arah[1] > 1:
						self.arah[1] = int(1)
						teredit = True
					if self.arah[1] < -1:
						self.arah = int(-1)
						teredit = True
					if teredit:
						print("fix arahnya ialah " + str(self.arah))
					x, y = self.arah
					if abs(x) == abs(y):
						print("there's some bug on arah. Rewrite it...")
						jalur = []
						for block in self.curBlock.jalur:
							temp = block.v in self.listBlock
							cek = temp, block.v
							print("hasilnya keberadaan = " + str(cek))
							if block.v not in self.listBlock:
								jalur.append(block)
								ada = True
						if ada:
							acakResult = floor(random() * len(jalur))
							cek = acakResult, len(jalur), jalur, self.curBlock.jalur
							print(cek)
							v = jalur[acakResult].v
							if jalur[acakResult].object.sebelumnya == None:
								jalur[acakResult].object.sebelumnya = self.curBlock
							self.curBlock = jalur[acakResult]
							self.usedBlock.append(jalur[acakResult])
							point = KX_RedBlock(self.scene.addObject('red_cube', jalur[acakResult]))
							self.arah = v - self.curBlock.v
							print("result of self.arah = " + str(self.arah))
						else:
							pass
							#self.antrian.append(self.curBlock)
					else:
						next = self.curBlock.v + self.arah
						print("next block ialah " + str(next))
						ada = next in self.listBlock
						print("next ada di listBlock ialah " + str(ada))
						for i in self.listBlock:
							if i == next:
								ada = True
								if i.object.sebelumnya == None:
									i.object.sebelumnya = self.curBlock
								self.curBlock = i.object
								self.usedBlock.append(i.object)
								point = KX_RedBlock(self.scene.addObject('red_cube', i.object))
								#point.sebelumnya = self.lastRedblock
								#self.lastRedblock = point
								i.object.visible = False
								#print(len(self.listBlock))
								break
							
					if ada == False:
						self.langkah = 0
						self.antrian.append(self.curBlock)
						self.isUjung = True
					else:
						self.langkah -= 1
				else:
					belok = intClose(random())
					#belok = 0
					if belok == 1:
						jalur = []
						for i in self.curBlock.jalur:
							if i not in self.usedBlock:
								ada = True
								jalur.append(i)
								
						if ada:
							jml = len(jalur)
							terpilih = jalur[floor(random() * jml)]
							#print(">>> " + str(terpilih))
							try:
								ar = terpilih.v - self.curBlock.v;
								#self.arah = Vec([ar[0], ar[1]])#kemungkinan nilainya ba hang/miss cukup tinggi
								self.arah = ar#kemungkinan nilainya ba hang/miss cukup tinggi
								self.antrian.append(terpilih)
								self.usedBlock.append(terpilih)
								if terpilih.sebelumnya == None:
									terpilih.sebelumnya = self.curBlock
								point = KX_RedBlock(self.scene.addObject('red_cube', terpilih))
							except:
								cek = terpilih, self.curBlock
								print("error di sini ref : " + str(cek))
								checker.getInfo()
								bge.logic.endGame()
								return False
							
							
							
					else:
						for i in self.curBlock.jalur:
							if i not in self.usedBlock:
								ada = True
								ar = i.position - self.position;
								self.arah = Vec([ar.x, ar.y])#kemungkinan nilainya ba hang/miss cukup tinggi
								self.antrian.append(i)
								self.usedBlock.append(i)
								if i.sebelumnya == None:
									i.sebelumnya = self.curBlock
								point = KX_RedBlock(self.scene.addObject('red_cube', i))
								#let it pass so it can acak lagi self.antrian nya
								
					pa = len(self.antrian)
					if pa > 0:
						pass
						#acak lagi jalur yang kan dipilih
						print("generating new step or langkah")
						terpilih = floor(random() * pa)
						self.curBlock = self.antrian[terpilih]
						self.curBlock.visible = False
						
						#point.sebelumnya = self.lastRedblock
						#self.lastRedblock = point
						del self.antrian[terpilih]
						self.langkah = acakLangkah()
						print("langkah yang diambil ialah = " + str(self.langkah))
						
				pa = len(self.antrian)
				if ada == False and pa == 0 and isUjung == False:
					print("kosong")
					print("done generating maze")
					self.curBlock = None
			else:
				pass
				#memulai tahap selanjutnya
				if self.generateStats == "way":
					print("relating between nodes being")
					self.generateStats = "wayNodes"
					self.wayIndex = 0
				elif self.generateStats == "wayNodes":
					curNode = self.listBlock[self.wayIndex].object
					print("mendata " + str(curNode))
					if curNode.sebelumnya != None:
						curNode.sebelumnya.next.append(curNode)
					self.wayIndex += 1
					if self.wayIndex >= len(self.listBlock):
						self.generateStats = "collectingTheEdge"
						print("collecting the edge of nodes...")
						self.wayIndex = 0
						self.nodeEdge = []
				elif self.generateStats == "collectingTheEdge":
					curNode = self.listBlock[self.wayIndex].object
					if len(curNode.next) == 0 and curNode.sebelumnya != None:
						print("adding edge " + str(curNode))
						self.nodeEdge.append(curNode)
						
					self.wayIndex += 1
						
					if self.wayIndex >= len(self.listBlock):
						print("inserting start point...")
						self.tempEdge = list(self.nodeEdge)
						terpilih = floor(random() * len(self.tempEdge))
						self.startPoint = self.tempEdge[terpilih]
						del self.tempEdge[terpilih]
						print("{0} has been choosen as the start point".format(str(self.startPoint)))
						added = self.scene.addObject('input', self.startPoint)
						
						print("inserting end point...")
						terpilih = floor(random() * len(self.tempEdge))
						self.endPoint = self.tempEdge[terpilih]
						del self.tempEdge[terpilih]
						print("{0} has been choosen as the end point".format(self.endPoint))
						added = self.scene.addObject('output', self.endPoint)
						
						self.generateStats = "insertingRoom"
						print("inserting room...")
						self.wayIndex = 0
						self.roomCount = 0
				elif self.generateStats == "insertingRoom":
					if len(self.tempEdge) > 0:
						terpilih = floor(random() * len(self.tempEdge))
						edge = self.tempEdge[terpilih]
						if self.roomCount < maxRoom:
							#memasukan ruangan
							print("{0} has been choosen as the room".format(str(edge)))
							added = self.scene.addObject('Room', edge)
							self.roomCount += 1
						else:
							pass
							#cuma jalan noh ini
							#print("passing the " + str(edge))
						del self.tempEdge[terpilih]
					else:
						self.generateStats = "done"
						print("done generating maze")
						print("total room is " + str(self.roomCount))
					
				
		except:
			checker.getInfo()
			bge.logic.endGame()
			return False
				
				
		
			