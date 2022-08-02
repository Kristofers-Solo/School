def main():
    try:
        user_input = input("Input: ")
        user_input_array = user_input.split(" ")
        if user_input == "all":
            pages = list(map(int, range(1, 17 + 1)))
        else:
            for page_range in user_input_array:
                if "-" in page_range:
                    # gets first number
                    first_num = int(page_range[:page_range.find("-")])
                    # gets second number
                    second_num = int(page_range[page_range.find("-") + 1:]) + 1
                    user_input_array = user_input_array + \
                        list(map(str, range(first_num, second_num))
                             )  # creates list with str range
            # removes all elements containing "-"
            pages = [elem for elem in user_input_array if not "-" in elem]
            pages = list(map(int, pages))  # convers str to int
            pages.sort()  # sorts list
            pages = list(set(pages))  # removes duplicates from list
        print(pages)

    except:
        print("Something went wrong. Try again.")


if __name__ == '__main__':
    main()

# 3 1 5 2 7-11 3-30
