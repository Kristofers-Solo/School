# Author - Kristiāns Francis Cagulis

# Date - 22.09.2021


class SalaryBonus():
	def __init__(self):
		self.percent = .15  # percent
		self.salary = float(input("Mēneša algas apjoms: "))  # salary per month
		self.time_worked = int(input("Nostrādātais gadu skaits: "))  # number of years worked

	def _calculate_bonus(self):
		if self.time_worked > 2:  # if worked for more than 2 years
			salary_bonus = self.percent * self.salary * (self.time_worked - 2)  # calculates salary bonus
			return f"Algas bonuss ir {round(salary_bonus, 2)}€"
		else:
			return "Algas bonuss nepienākas."


def main():
	print(SalaryBonus()._calculate_bonus())


if __name__ == "__main__":
	main()