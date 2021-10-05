# Author - Kristiāns Francis Cagulis
# Date - 29.09.2021

import math


# 1. uzdevums
def is_prime():
	number = int(input("Ievadiet skaitli: "))
	if number > 0:
		if number == 1:
			return "1 nav pirmsskaitlis"
		else:
			for i in range(2, int(math.sqrt(number)) + 1):
				if number % i == 0:
					return f"Skaitlis {number} nav pirmsskaitlis"
			return f"Skaitlis {number} ir pirmsskaitlis"
	else:
		return "Skaitlim jābūt lielākam par 0"


# 2. uzdevums
class Cities:
	def __init__(self, p0, perc, delta, p):
		self.p0 = p0
		self.perc = float(perc[:-1]) / 100
		self.delta = delta
		self.p = p

	def _calculate(self):
		years = 0
		while (True):
			result = self.p0 + self.p0 * self.perc + self.delta
			self.p0 = result
			years += 1
			if result >= self.p:
				return f"{self.p} iedzīvotāju skaits tiks sasniegts pēc {years} gadiem"
			if result < 0:
				return -1


city_0 = Cities(1000, "2%", 50, 1200)
city_1 = Cities(1000, "2%", -50, 5000)
city_2 = Cities(1500, "5%", 100, 5000)
city_3 = Cities(1_500_000, "2.5%", 10_000, 2_000_000)


def main():
	task = int(input("""Ivēlieties uzdevumu:
	1 - pirmais uzdevums
	2 - otrais uzdevums
	"""))

	if task == 1:
		print(is_prime())
	elif task == 2:
		city = int(input("""Izvēlieties pilsētu:
		0 - piemēra pilsēta
		1 - pirmā pilsēta
		2 - otrā pilsēta
		3 - trešā pilsēta
		"""))
		if city == 0:
			print(city_0._calculate())
		elif city == 1:
			print(city_1._calculate())
		elif city == 2:
			print(city_2._calculate())
		elif city == 3:
			print(city_3._calculate())
		else:
			print("Ievadīts nepareizs skaitlis.")
	else:
		print("Ievadīts nepareizs skaitlis.")


if __name__ == '__main__':
	main()