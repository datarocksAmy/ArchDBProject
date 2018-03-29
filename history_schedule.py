# Libraries
import json
import random
import itertools


# Check Data Item and Transaction input type and range
def check_input(param):
    # Input Choices
    choice = {
            1: "Data Item",
            2: "Transaction",
            3: "Maximum Num of Operations per Transaction"
            }
    # Invalid Input Warnings
    warning = {
            1: "1-4",
            2: "1-4",
            3: "3-5"
             }

    # Prompt user for choices
    inputArg = "Please enter the number of " + choice.get(param) + " : "
    errorArg = ">>> Invalid Input. Please enter a number between " + warning.get(param) + "\n"
    inputData = input(inputArg)

    # Error handling
    while True:
        try:
            inputData = int(inputData)
            if param == 3 and not(3 <= inputData <= 5):
                raise ValueError
            elif (param == 1 or param == 2) and not (1 <= inputData <= 4):
                raise ValueError
            else:
                return inputData

        except ValueError:
            print(errorArg)
            inputData = input(inputArg)

        except:
            print(errorArg)
            inputData = input(inputArg)


# Random Generator : Data Item
def data_item_generator(numOfDataItem):
    dataItemList = ["x", "y", "z", "w"]
    if numDataItem == 4:
        return dataItemList
    else:
        return random.choices(population=dataItemList, k=numOfDataItem)


# Random Generator : Pick 1 Operation
def operation_generator():
    operationList = ["r", "w", "c", "a"]
    return random.choice(operationList)


# Create JSON Object per Transaction
def JSON_Obj_generator(numOfOperation, TNum, dataItemL):
    transactionList = []
    for idx in range(1, numOfOperation+1):
        JSON_Obj = {
                   "Index": idx,
                   "Transaction": TNum,
                   "Data Item": random.choice(dataItemL),
                   "Operation": operation_generator(),
                   "IsHistory": "False"
                   }
        transactionList.append(JSON_Obj)

    return transactionList


# Relabel Index
def relabel(HTransaction):
    for idx in range(1, len(HTransaction) + 1):
        HTransaction[idx-1]['Index'] = idx

    return HTransaction


# Check if History has at least 1 conflict
def conflict_raid(finalHistT):
    conflict_Case = {
                1: ["r", "w"],
                2: ["w", "w"],
                3: ["w", "r"]
            }
    # Different Transaction, Same Data Item, One of them is write
    for idx in range(1, len(finalHistT)+1):
        for searchIdx in range(2, len(finalHistT)+1):
            tempOp = []
            if (finalHistT[idx-1]['Transaction'] != finalHistT[searchIdx-1]['Transaction']) and \
                    (finalHistT[idx-1]['Data Item'] == finalHistT[searchIdx-1]['Data Item']):
                        tempOp.append(finalHistT[idx-1]['Operation'])
                        tempOp.append(finalHistT[searchIdx-1]['Operation'])
                        for caseNum in range(1, 4):
                            if tempOp == conflict_Case.get(caseNum):
                                return True
    return False

# Create History JSON with Transactions
def History_generator(dataItemL, numTransaction, numOperation):
    history = {}
    chainTransactions = []

    for numT in range(1, numTransaction+1):
        transaction = JSON_Obj_generator(numOperation, numT, dataItemL)
        keyT = "T" + str(numT)
        history[keyT] = transaction
        chainTransactions.append(transaction)
    # Concat Multiple Lists into 1
    historyT = list(itertools.chain.from_iterable(chainTransactions))

    # Randomly Shuffle order of items
    random.shuffle(historyT)

    # Relabel 'Index'
    finalHistoryT = relabel(historyT)

    return finalHistoryT


# Prompt user input for num of Data Items & num of Transactions & Max Num of Operation
# Max size of 4 for Data item and transaction, Max size of 5 for Operation
numDataItem = check_input(1)
numTransaction = check_input(2)
numOperation = check_input(3)

# Set up Data Item
dataItemList = data_item_generator(numDataItem)

# Generate History
flag = False
while not flag:
    historyyy = History_generator(dataItemList, numTransaction, numOperation)
    flag = conflict_raid(historyyy)



# Dump JSON - History - into text file
with open("HistoryJSON.txt", 'w') as JSONfile:
    outputJSON = json.dumps(historyyy, indent=4)
    JSONfile.write(outputJSON)

