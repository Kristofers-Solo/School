# Author - Kristiāns Francis Cagulis
# Date - 15.09.2021


# task 1 - train
def trains():
    # blue train from Jelgava to Riga
    blue_train_speed = 57
    blue_train_time_driven = 10 / 60

    # green train form Riga to Jelgava
    green_train_speed = 60

    # red train from Valka to Jelgava
    red_train_speed = 60
    red_train_time_driven = 4

    # distances
    distance_riga_jelgava = 42  # from Riga to Jelgava (blue and green train)
    distance_riga_valka = 164  # from Riga to Valka (red train)

    def blue_green_train():
        blue_train_already_driven_distance = blue_train_speed * \
            blue_train_time_driven  # blue train driven distance in 10 min
        meeting_time = (distance_riga_jelgava - blue_train_already_driven_distance) / (
            blue_train_speed + green_train_speed)  # time after which the two trains meet
        green_train_distance = meeting_time * \
            green_train_speed  # distance green train has driven
        meeting_distance = distance_riga_jelgava - \
            green_train_distance  # distance from meeting point to Riga

        return f"Zilais un zaļais vilciens tiksies {round(meeting_distance, 2)}km no Rīgas."

    def red_train():
        red_train_distance_driven = red_train_time_driven * \
            red_train_speed  # red train driven distance in given time
        print(
            f"Sarkanais vilciens ir nobraucis {round(red_train_distance_driven, 2)}km.")
        if red_train_distance_driven > distance_riga_valka:
            return "Sarkanais vilciens ir pabraucis garām Rīgai."

    print(blue_green_train())
    print(red_train())


# task 2 - sheep
def farm():
    sheep_amount = 255  # amount of sheep in farm
    sheep_price = 20.5  # price per sheep's wool
    wool_total_price = sheep_amount * sheep_price  # price for all sheep wool

    additional_sheep = 120  # additional sheep
    # sum of original and added sheep
    new_sheep_amount = sheep_amount + additional_sheep
    # price for original and added sheep wool
    new_wool_total_price = new_sheep_amount * wool_total_price

    ostrich_amount = 15  # amount of ostrich in farm
    ostrich_egg_price = 30  # price per egg
    ostrich_time = 2  # time required to get one ostrich egg
    days = 30  # the time when ostriches lay eggs
    ostrich_egg_total_price = ostrich_amount * ostrich_egg_price * \
        days / ostrich_time  # price for all ostrich eggs in 30 days

    if wool_total_price >= ostrich_egg_total_price:
        return "Iegūtās naudas pietiks, lai nopirktu visas mēneša olas."
    else:
        print("Iegūtās naudas nepietiks, lai nopirktu visas mēneša olas.")
        if new_wool_total_price >= ostrich_egg_total_price:
            return f"Ja aitu būtu par {additional_sheep}, tad iegūtās naudas pietiktu, lai nopirktu visas mēneša olas."
        else:
            return f"Ja aitu būtu par {additional_sheep}, tad iegūtās naudas nepietiktu, lai nopirktu visas mēneša olas."


def main():
    task = int(input("""Ivēlieties uzdevumu:
	1 - pirmais uzdevums
	2 - otrais uzdevums
	"""))

    if task == 1:
        trains()
    elif task == 2:
        print(farm())


if __name__ == '__main__':
    main()
