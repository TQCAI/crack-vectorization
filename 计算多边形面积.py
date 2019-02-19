# -*- coding: cp936 -*-
import math


class Point():
	def __init__(self, x, y):
		self[0] = x
		self[1] = y


def GetAreaOfPolyGon(points):
	area = 0
	if (len(points) < 3):
		raise Exception("error")

	p1 = points[0]
	p2 = points[1]
	p3 = points[2]
	for i in range(1, len(points) - 1):
		# ��������
		vecp1p2 = Point(p2[0] - p1[0], p2[1] - p1[1])
		vecp2p3 = Point(p3[0] - p2[0], p3[1] - p2[1])

		# �ж�˳ʱ�뻹����ʱ�룬˳ʱ�����Ϊ������ʱ�����Ϊ��
		vecMult = vecp1p2[0] * vecp2p3[1] - vecp1p2[1] * vecp2p3[0]  # �ж���������Ƚ�����˼
		sign = 0
		if (vecMult > 0):
			sign = 1
		elif (vecMult < 0):
			sign = -1

		triArea = GetAreaOfTriangle(p1, p2, p3) * sign
		area += triArea
	return abs(area)


def GetAreaOfTriangle(p1, p2, p3):
	'''�������������   ���׹�ʽ'''
	area = 0
	p1p2 = GetLineLength(p1, p2)
	p2p3 = GetLineLength(p2, p3)
	p3p1 = GetLineLength(p3, p1)
	s = (p1p2 + p2p3 + p3p1) / 2
	area = s * (s - p1p2) * (s - p2p3) * (s - p3p1)  # ���׹�ʽ
	area = math.sqrt(area)
	return area


def GetLineLength(p1, p2):
	'''����߳�'''
	length = math.pow((p1[0] - p2[0]), 2) + math.pow((p1[1] - p2[1]), 2)  # pow  �η�
	length = math.sqrt(length)
	return length


def main():
	p1 = Point(1, 1)
	p2 = Point(2, 1)
	p3 = Point(2, 2)
	p4 = Point(1, 2)
	points = [p1, p2, p3, p4]
	area = GetAreaOfPolyGon(points)
	print(math.ceil(area))
	assert math.ceil(area) == 1


if __name__ == '__main__':
	main()