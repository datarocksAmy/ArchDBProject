# Check Data Item and Transaction input type and range
def check_input(param):
    choice = {
            1: "Data Item",
            2: "Transaction"
            }

    inputArg = "Please enter the number of " + choice.get(param) + " : "
    inputData = input(inputArg)

    while True:
        try:
            inputData = int(inputData)
            if not (1 <= inputData <= 4):
                raise ValueError
            else:
                return inputData
        except ValueError:
            print(">>> Invalid Input. Please enter a number between 1-4.")
            inputData = input(inputArg)
        except:
            print(">>> Invalid Input. Please enter a number between 1-4.")
            inputData = input(inputArg)

# Check Transaction Serializable or not
#def seriously_serializable():

# Prompt user input for num of Data Items & num of Transactions
# Max size 4 for Data item and transaction
numDataItem = check_input(1)
numTransaction = check_input(2)
