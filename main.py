import MMGame


def main():
    mode = int(input("Input 0 to play the basic mode, 1 to play the advanced mode:\n"))
    unknowns = int(input("Input a number, which will be the number of unknown numbers to sample:\n"))
    min = int(input("Give the minimum of the range of numbers that are possible in the sample:\n"))
    max = int(input("Give the maximum of the range of numbers that are possible in the sample:\n"))
    if mode == 0:
        basic_mode = MMGame.basic(unknowns, list(range(min, max + 1)))
        basic_mode.play()
    elif mode == 1:
        advanced_mode = MMGame.advanced(unknowns, list(range(min, max + 1)))
        advanced_mode.play()
    else:
        print("You're playing the wrong game!")
    replay = int(input("Do you want to play again? (type 1 for yes, 0 to exit)\n"))
    if replay == 1:
        main()

if __name__ == "__main__":
    main()
