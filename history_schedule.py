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
    dataItemList = ["x", "y", "z", "v"]
    if numDataItem == 4:
        return dataItemList
    else:
        return random.choices(population=dataItemList, k=numOfDataItem)


# Random Generator : Pick 1 Operation
def operation_generator(op):
    if op == "rw":
        rw_operationList = ["r", "w"]
        op_pick = random.choice(rw_operationList)
    elif op == "ac":
        ac_operationList = ["c", "a"]
        op_pick = random.choice(ac_operationList)

    return op_pick


# Create JSON Object per Transaction
def JSON_Obj_generator(numOfOperation, TNum, dataItemL):
    transactionList = []
    for idx in range(1, numOfOperation+1):
        JSON_Obj = {
                   "Index": idx,
                   "Transaction": TNum,
                   "Data Item": random.choice(dataItemL),
                   "Operation": operation_generator("rw"),
                   "IsHistory": "False"
                   }
        transactionList.append(JSON_Obj)

    return transactionList


# Relabel Index
def relabel(HTransaction):
    for idx in range(1, len(HTransaction) + 1):
        HTransaction[idx-1]['Index'] = idx

    return HTransaction


# Check if History has at least 1 conflict2
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
    countNumT = []

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

    # Put in commit and abort for each transaction
    for numT_count in range(1, len(finalHistoryT)+1):
        if finalHistoryT[-numT_count]['Transaction'] not in countNumT:
            countNumT.append(finalHistoryT[-numT_count]['Transaction'])
            finalHistoryT[-numT_count]['Operation'] = operation_generator("ac")


    # Label IsHistroy to True
    for flipIdx in range(0, len(finalHistoryT)):
        finalHistoryT[flipIdx]['IsHistory'] = "True"

    return finalHistoryT


# Determine Serializability
def serializability_pat(finalHistT):
    conflict_Case = {
                1: ["r", "w"],
                2: ["w", "w"],
                3: ["w", "r"]
            }
    conflict_Order = {1: [], 2: [], 3: []}

    # Different Transaction, Same Data Item, One of them is write
    for idx in range(1, len(finalHistT)+1):
        for searchIdx in range(2, len(finalHistT)+1):
            tempOp = []
            if (finalHistT[idx-1]['Transaction'] != finalHistT[searchIdx-1]['Transaction']) and \
                    (finalHistT[idx-1]['Data Item'] == finalHistT[searchIdx-1]['Data Item']):
                        tempOp.append(finalHistT[idx-1]['Operation'])
                        tempOp.append(finalHistT[searchIdx-1]['Operation'])
                        temp_T_order = [finalHistT[idx-1]['Transaction'], finalHistT[searchIdx-1]['Transaction']]

                        for caseNum in range(1, 4):
                            if (tempOp == conflict_Case.get(caseNum)) and (temp_T_order not in conflict_Order[caseNum]):
                                conflict_Order[caseNum].append(temp_T_order)

    if (len(conflict_Order[1]) == len(conflict_Order[2]) and len(conflict_Order[2]) == len(conflict_Order[3]) and len(conflict_Order[1]) == len(conflict_Order[3])) and \
            ((conflict_Order[1] == conflict_Order[2]) and (conflict_Order[2] == conflict_Order[3]) and (conflict_Order[1] == conflict_Order[3])):
        return True
    else:
        return False

# Get the Transaction order for abort and commit
def AC_order(finalHistT):
    ac_order_list = []
    for idx in range(0, len(finalHistT)):
        if (finalHistT[idx]['Operation'] == 'a' or finalHistT[idx]['Operation'] == 'c') and \
                (finalHistT[idx]['Transaction'] not in ac_order_list):
                    ac_order_list.append(finalHistT[idx]['Transaction'])

    return ac_order_list


# Determine RC or not
def RC_mate(finalHistT):
    abort_commit_dataI = []
    for pivot in range(0, len(finalHistT)):
        for idx in range(1, len(finalHistT)):
            # Find different Transaction
            if finalHistT[pivot]['Transaction'] != finalHistT[idx]['Transaction']:
                # Find operation working on the same data item
                if (finalHistT[pivot]['Data Item'] == finalHistT[idx]['Data Item']) and \
                                finalHistT[pivot]['Operation'] == 'w' and \
                                finalHistT[pivot]['Transaction'] not in abort_commit_dataI:
                    abort_commit_dataI.append(finalHistT[pivot]['Transaction'])

                    # Check if it's 'read from' or not
                    if (finalHistT[idx]['Operation'] == 'r' or finalHistT[idx]['Operation'] == 'w') and \
                            (finalHistT[pivot]['Transaction'] not in abort_commit_dataI):
                            abort_commit_dataI.append(finalHistT[idx]['Transaction'])

            elif finalHistT[pivot]['Transaction'] not in abort_commit_dataI:
                abort_commit_dataI.append(finalHistT[pivot]['Transaction'])

    # RC : abort and commit order = operation on the same data item transaction order
    ###################################  Not finished with different RC cases just yet
    if abort_commit_dataI == AC_order(finalHistT):
        return "RC"
    else:
        return "NRC"



# Prompt user input for num of Data Items & num of Transactions & Max Num of Operation
# Max size of 4 for Data item and transaction, Max size of 5 for Operation
numDataItem = check_input(1)
numTransaction = check_input(2)
numOperation = check_input(3)

# Set up Data Item
dataItemList = data_item_generator(numDataItem)

# Generate History
historyyy = History_generator(dataItemList, numTransaction, numOperation)


# Check if there's at least one conflict in the history or not
# If not, generate a history again
while conflict_raid(historyyy):
    historyyy = History_generator(dataItemList, numTransaction, numOperation)


# Dump JSON - History - into text file
with open("HistoryJSON.txt", 'w') as JSONfile:
    outputJSON = json.dumps(historyyy, indent=4)
    JSONfile.write(outputJSON)

# Serializable or not
serializability = serializability_pat(historyyy)
print(serializability)


test = RC_mate(historyyy)
print(test)