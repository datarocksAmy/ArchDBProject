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

# Check if # of Data Item is correct
def dataItem_raid(finalHistT, numOfDataItem):
    dataItem_check = []
    # Different Transaction, Same Data Item, One of them is write
    for idx in range(0, len(finalHistT)):
        if finalHistT[idx]['Data Item'] not in dataItem_check:
            dataItem_check.append(finalHistT[idx]['Data Item'])

    if len(dataItem_check) == numOfDataItem:
        return True
    else:
        return False


# Create History JSON with Transactions
def History_generator(dataItemL, numTransaction, numOperation):
    history = {}
    chainTransactions = []
    countNumT = []
    dataItemCheck = []

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
        if finalHistoryT[-numT_count]['Transaction'] not in countNumT and finalHistoryT[-numT_count]['Data Item'] not in dataItemCheck:
            countNumT.append(finalHistoryT[-numT_count]['Transaction'])
            dataItemCheck.append(finalHistoryT[-numT_count]['Data Item'])
            finalHistoryT[-numT_count]['Operation'] = operation_generator("ac")
            finalHistoryT[-numT_count]['Data Item'] = ""


    return finalHistoryT


# Determine 'Serializability'
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
        return "Serializable"
    else:
        return "Not Serializable"

# Get the Transaction order for abort and commit
def AC_order(finalHistT):
    ac_order_list = []
    for idx in range(0, len(finalHistT)):
        if (finalHistT[idx]['Operation'] == 'a' or finalHistT[idx]['Operation'] == 'c') and \
                (finalHistT[idx]['Transaction'] not in ac_order_list):
                    ac_order_list.append(finalHistT[idx]['Transaction'])

    return ac_order_list


# Determine 'RC'
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


# Check Read/Write Operation after Commit
def wr_check_after_commmit(finalHistT, commitIdx, TDataItemDict, startNum, endNum):
    for wr_after in range(startNum, endNum):
        # Check if there's r or w operation after commit
        if finalHistT[wr_after]['Operation'] == 'w' or finalHistT[wr_after]['Operation'] == 'r':
            for key, val in TDataItemDict.items():
                # Different transaction but operate on the same data item AFTER commit
                if finalHistT[wr_after]['Transaction'] != key and finalHistT[wr_after]['Data Item'] == val:
                    return "Strict"
        else:
            return "Not Strict"


# Determine 'Strict'
def strict_eh(finalHistT):
    commitIdx = []
    T_DataItem = {}

    for cIdx in range(0, len(finalHistT)):
        if finalHistT[cIdx]['Operation'] == 'c':
            commitIdx.append(cIdx)
            if finalHistT[cIdx]['Transaction'] in commitIdx:
                T_DataItem[finalHistT[cIdx]['Transaction']].append(finalHistT[cIdx]['Data Item'])
            else:
                T_DataItem[finalHistT[cIdx]['Transaction']] = [finalHistT[cIdx]['Data Item']]

    # Num of Commit in CommitIdx List
    lenCommitIdx = len(commitIdx)

    # No commit operation --> Not Strict
    if lenCommitIdx == 0 or commitIdx[-1] == len(finalHistT)-1:
        return "Not Strict"

    else:
        # Check if there's w or r after commit

        # Only 1 Commit
        if lenCommitIdx == 1:
            strict_verdict = wr_check_after_commmit(finalHistT, commitIdx, T_DataItem, commitIdx[0]+1, len(finalHistT))
            return strict_verdict

        # 2+ Commit
        else:
            for multipleCommitIdx in range(0, lenCommitIdx):
                if multipleCommitIdx != lenCommitIdx and commitIdx[multipleCommitIdx] != len(finalHistT):
                    strict_verdict = wr_check_after_commmit(finalHistT, commitIdx, T_DataItem, commitIdx[multipleCommitIdx] + 1, commitIdx[multipleCommitIdx+1])
                    return strict_verdict

                else:
                    strict_verdict = wr_check_after_commmit(finalHistT, commitIdx, T_DataItem, commitIdx[multipleCommitIdx] + 1, len(finalHistT))
                return strict_verdict


# Check Read Operation after Commit
def r_check_after_commmit(finalHistT, commitIndex, startNum, endNum):
    for r_after in range(startNum, endNum):
        for item in range(0, len(commitIndex)):
            # Check if there's r after commit
            if finalHistT[r_after]['Operation'] == 'r':
                # Read from a committed transaction or not
                if finalHistT[r_after]['Transaction'] != commitIndex[item][0]:
                        return "ACA"
    return "Not ACA"


# Determine 'ACA' : Must read from a committed transaction
def ACA_huh(finalHistT):
    CI_List = []
    for findC in range(0, len(finalHistT)):
        commit_index = []
        if finalHistT[findC]['Operation'] == 'c':
            commit_index.append(finalHistT[findC]['Transaction'])
            commit_index.append(findC)

            CI_List.append(commit_index)

    numCommit = len(CI_List)

    if numCommit == 0:
        return "Not ACA"

    # 1 Commit
    elif numCommit == 1:
        if CI_List[0][1] != len(finalHistT):
            # Search for read operation and see if it's reading from a committed transaction
            ACA_result = r_check_after_commmit(finalHistT, CI_List, CI_List[numCommit-1][1]+1, len(finalHistT))
            return ACA_result

        else:
            return "Not ACA"

    # 2+ Commit
    else:
            for multipleCommitIdx in range(2, numCommit):
                if CI_List[multipleCommitIdx][1] != len(finalHistT) and multipleCommitIdx != numCommit:
                    ACA_result = r_check_after_commmit(finalHistT, CI_List, CI_List[multipleCommitIdx-1][1]+1, CI_List[multipleCommitIdx][1])
                    return ACA_result

                elif CI_List[multipleCommitIdx][1] != len(finalHistT):
                    ACA_result = wr_check_after_commmit(finalHistT, CI_List, CI_List[multipleCommitIdx][1] + 1, len(finalHistT))
                    return ACA_result
                else:
                    return "Not ACA"

# ---------------------------------------------------- Main ----------------------------------------------------
# Prompt user input for num of Data Items & num of Transactions & Max Num of Operation
# Max size of 4 for Data item and transaction, Max size of 5 for Operation
numDataItem = check_input(1)
numTransaction = check_input(2)
numOperation = check_input(3)

# Set up Data Item
dataItemList = data_item_generator(numDataItem)

# Generate History
historyyy = History_generator(dataItemList, numTransaction, numOperation)


# Check if there's at least one conflict in the history or not AND # of data item is correct
# If not, generate a history again
while conflict_raid(historyyy) and dataItem_raid(historyyy, numDataItem):
    historyyy = History_generator(dataItemList, numTransaction, numOperation)


# Dump JSON - History - into text file
with open("HistoryJSON.txt", 'w') as JSONfile:
    outputJSON = json.dumps(historyyy, indent=4)
    JSONfile.write(outputJSON)

# Serializable or not
serializability = serializability_pat(historyyy)
print(serializability)

# Recoverable or not
recoverable = RC_mate(historyyy)
print(recoverable)

# Strict or not
strict = strict_eh(historyyy)
print(strict)

# ACA or not
ACA = ACA_huh(historyyy)
print(ACA)
