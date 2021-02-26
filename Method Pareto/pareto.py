pos_criterion_name = []
neg_criterion_name = []
alternatives = []

# Input alternative from file input.txt
def input_alternative():
    f = open("input.txt", "r")    
    for line in f:
        alter = []
        alternative = line.strip("\n").split("|")
        for criterion in alternative:
            alter.append(criterion.split(","))
        alternatives.append(alter)

# Formated output alternative
def print_alternative(number_pos, number_neg, alternatives):
    row_format = "{:^35} |" + "{:^11} | " * (number_pos + number_neg)
    for alternative in alternatives:
        al = [alternative[i][j] for i in range(len(alternative)) for j in range(len(alternative[i]))]
        print(row_format.format(*al))

# Check alternative1 is dominates alternative2?
def dominates(alternative1, alternative2):
    for i in range(len(pos_criterion_name)):
        if float(alternative1[1][i]) < float(alternative2[1][i]):
            return False
    
    for i in range(len(neg_criterion_name)):
        if float(alternative1[2][i]) > float(alternative2[2][i]):
            return False
    
    return True

def pareto_optimal(alternatives):
    pareto_element = []
    dominatedAlter = []
    candidateRowNr = 0
    tag = alternatives[0]  
    copy_alternatives = alternatives.copy()
    copy_alternatives.pop(0)

    while True:
        candidateRow = copy_alternatives[candidateRowNr]
        copy_alternatives.remove(candidateRow)
        rowNr = 0
        nonDominated = True
        while len(copy_alternatives) != 0 and rowNr < len(copy_alternatives):
            row = copy_alternatives[rowNr]
            if dominates(candidateRow, row):
                copy_alternatives.remove(row)
                dominatedAlter.append(row)
            elif dominates(row, candidateRow):
                nonDominated = False
                dominatedAlter.append(candidateRow)
                rowNr += 1
            else:
                rowNr += 1
        
        if nonDominated:
            pareto_element.append(candidateRow)

        if len(copy_alternatives) == 0:
            break
    
    pareto_element.insert(0, tag)
    dominatedAlter.insert(0, tag)
    return pareto_element, dominatedAlter

def check_in_pareto(pareto_element, alternative):
    for ele in pareto_element:
        if ele[0][0] == alternative[0][0]:
            return True
    return False

def f_limit_element(alternatives, NCriterion, limit, sign):
    limit_ele = []
    copy_alternatives = alternatives.copy()
    tag = copy_alternatives.pop(0)
    
    if NCriterion <= len(pos_criterion_name):
        NCriterion -= 1
        for alternative in copy_alternatives:
            if sign == '>=':
                if float(alternative[1][NCriterion]) >= limit:
                    limit_ele.append(alternative)
            elif sign == '<=':
                if float(alternative[1][NCriterion]) <= limit:
                    limit_ele.append(alternative)
    elif NCriterion > len(pos_criterion_name):
        NCriterion -= (len(pos_criterion_name) + 1)
        for alternative in copy_alternatives:
            if sign == '>=':
                if float(alternative[2][NCriterion]) >= limit:
                    limit_ele.append(alternative)
            elif sign == "<=":
                if float(alternative[2][NCriterion]) <= limit:
                    limit_ele.append(alternative)
    limit_ele.insert(0, tag)
    return limit_ele

def set_limit(alternatives):
    limit_element = alternatives.copy()

    while True:
        print("Choose 1 criterion for set limit: ")
        index = 1
        for pos_criterion in pos_criterion_name:
            print("\t" + str(index) + " - " + pos_criterion)
            index += 1
        for neg_criterion in neg_criterion_name:
            print("\t" + str(index) + " - " + neg_criterion)
            index += 1
        print("\t0 - Done!")

        choose = int(input("\tEnter your choose: "))
        if choose == 0:
            break
        
        print("\t\tSet limit for this criterion: ")
        print("\t\t\t1 - Less than or equal")
        print("\t\t\t2 - Greater than or equal")
        choose_limit = int(input("\t\t\tEnter your choose: "))

        if choose_limit == 1:
            if choose <= len(pos_criterion_name):
                lim = float(input("\t\tLimit for criterion " + pos_criterion_name[choose - 1] + " is less than or equal: "))
                limit_element = f_limit_element(limit_element, choose, lim, "<=")
            else:
                lim = float(input("\t\tLimit for criterion " + neg_criterion_name[choose - len(pos_criterion_name) - 1] + " is less than or equal: "))
                limit_element = f_limit_element(limit_element, choose, lim, "<=")
        elif choose_limit == 2:
            if choose <= len(pos_criterion_name):
                lim = float(input("\t\tLimit for criterion " + pos_criterion_name[choose - 1] + " is greater than or equal: "))
                limit_element = f_limit_element(limit_element, choose, lim, ">=")
            else:
                lim = float(input("\t\tLimit for criterion " + neg_criterion_name[choose - len(pos_criterion_name) - 1] + " is greater than or equal: "))
                limit_element = f_limit_element(limit_element, choose, lim, ">=")
    
    return limit_element

def find_best_alternative(alternatives, NCriterion):
    best_alternative = []
    copy_alternatives = alternatives.copy()
    tag = copy_alternatives.pop(0)
    
    if NCriterion <= len(pos_criterion_name):
        NCriterion -= 1
        a_max = copy_alternatives[0]
        for i in range(1, len(copy_alternatives)):
            if float(copy_alternatives[i][1][NCriterion]) > float(a_max[1][NCriterion]):
                a_max = copy_alternatives[i]
        for i in range(0, len(copy_alternatives)):
            if float(copy_alternatives[i][1][NCriterion]) == float(a_max[1][NCriterion]):
                best_alternative.append(copy_alternatives[i])

    elif NCriterion > len(pos_criterion_name):
        NCriterion -= (len(pos_criterion_name) + 1)
        a_min = copy_alternatives[0]
        for i in range(1, len(copy_alternatives)):
            if float(copy_alternatives[i][2][NCriterion]) < float(a_min[2][NCriterion]):
                a_min = copy_alternatives[i]

        for i in range(0, len(copy_alternatives)):
            if float(copy_alternatives[i][2][NCriterion]) == float(a_min[2][NCriterion]):
                best_alternative.append(copy_alternatives[i])

    best_alternative.insert(0, tag)
    return best_alternative

def sub_optimization():
    sub_set = set_limit(alternatives)

    print("Choose main criterion: ")
    index = 1
    for pos_criterion in pos_criterion_name:
        print("\t" + str(index) + " - " + pos_criterion)
        index += 1
    for neg_criterion in neg_criterion_name:
        print("\t" + str(index) + " - " + neg_criterion)
        index += 1
    print("\t0 - Done!")

    choose = int(input("\tEnter your choose: "))

    return find_best_alternative(sub_set, choose)

def lexico_optimization(alternatives):
    print("Set the order of criterion: ")
    index = 1
    for pos_criterion in pos_criterion_name:
        print("\t" + str(index) + " - " + pos_criterion)
        index += 1
    for neg_criterion in neg_criterion_name:
        print("\t" + str(index) + " - " + neg_criterion)
        index += 1

    orders = [int(x) for x in input("Enter your order: ").split()]

    lexico_set = alternatives.copy()

    for order in orders:
        lexico_set = find_best_alternative(lexico_set, order)
    
    return lexico_set


input_alternative()
pos_criterion_name = alternatives[0][1]
neg_criterion_name = alternatives[0][2]

while True:
    print("\n" + "-" * 40 + "MENU" + "-" * 40)
    print("[1] - Print all alternatives")
    print("[2] - Pareto optimal set")
    print("[3] - Optimal solutions when setting limits")
    print("[4] - Sub-optimization")
    print("[5] - Lexicographic optimization")
    print("[0] - Exit!")
    print("-" * 40 + "----" + "-" * 40)
    my_choice = int(input("Enter your choice: "))

    pareto_set, dominated_set = pareto_optimal(alternatives)

    if my_choice == 1:
        print("\n" + "-"*49 + "All alternatives" + "-"*49)
        print_alternative(len(pos_criterion_name), len(neg_criterion_name), alternatives)

    elif my_choice == 2:
        print("\n" + "-"*48 + "Pareto Optimal Set" + "-"*48)
        print_alternative(len(pos_criterion_name), len(neg_criterion_name), pareto_set)

    elif my_choice == 3:
        print("\n" + "-"*40 + "Specifying limit of criteria" + "-"*40)
        limit_ele = set_limit(alternatives)
        print("\n" + "-"*36 + "Set of element when limit has been applied" + "-"*36)
        print_alternative(len(pos_criterion_name), len(neg_criterion_name), limit_ele)
        print("\n" + "-"*29 + "Set of element when limit has been applied in Pareto set" + "-"*29)
        pareto_limit = []
        for ele in limit_ele:
            if ele in pareto_set:
                pareto_limit.append(ele)
        print_alternative(len(pos_criterion_name), len(neg_criterion_name), pareto_limit)

    elif my_choice == 4:
        print("\n" + "-"*40 + "Sub-optimization" + "-"*40)
        sub_opt_ele = sub_optimization()
        print("\n" + "-"*41 + "Set of element sub-optimization" + "-"*42)
        print_alternative(len(pos_criterion_name), len(neg_criterion_name), sub_opt_ele)

    elif my_choice == 5:
        print("\n" + "-"*40 + "Lexicographic optimization" + "-"*40)
        lexico_set = lexico_optimization(alternatives)
        print()
        print_alternative(len(pos_criterion_name), len(neg_criterion_name), lexico_set)

    else:
        print("Thank you for using!")
        break