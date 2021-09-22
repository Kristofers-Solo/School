# Author - Kristiāns Francis Cagulis
# Date - 22.09.2021
#
# Uzdevums:
#
# Firma apsolījusi Ziemassvētku bonusu 15% apjomā no mēneša algas par KATRU nostrādāto gadu virs 2 gadiem.
# Uzdevums. Noprasiet lietotājam mēneša algas apjomu un nostrādāto gadu skaitu.
# Izvadiet bonusu.


class Bonuss():
	def __init__(self):
		self.percent = .15
		self.salary = float(input("Mēneša algas apjoms: "))
		self.time_worked = int(input("Nostrādātais gadu skaits: "))

	def _calculate_bonus(self):
		if self.time_worked > 2:
			salary_bonus = self.percent * self.salary * (self.time_worked - 2)
			return f"Jūsu algas bonuss ir {round(salary_bonus, 2)}€"
		else:
			return "Jums algas bonuss nepienākas."


def main():
	print(Bonuss()._calculate_bonus())


if __name__ == "__main__":
	main()