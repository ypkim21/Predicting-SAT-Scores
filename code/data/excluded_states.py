file_path = input("Please input file path:\n")

with open(file_path) as file:
    states = file.readlines()

    states = [state.lower().strip() for state in states]

while True:
    prompt = input("Input state: ")

    if prompt == "quit":
        break
    else:
        if prompt.lower() in states:
            print("FAILURE!")
        else:
            print("SUCCESS!")
