pos_criterion_name = ['Screen', 'SSD', 'Pin', 'Rate']
neg_criterion_name = ['Price', 'Weight']
alternatives = [[['Solution'], ['Screen', 'SSD', 'Pin', 'Rate'], ['Price', 'Weight']], [['Acer Aspire 5 A515-44G'], ['15.6', '256', '10', '5'], ['60.9', '1.8']], [['ASUS ZenBook 13 UX325EA'], ['13.3', '512', '18', '5'], ['76.6', '1.07']], [['Lenovo IdeaPad 5 15'], ['15.6', '512', '14', '4.7'], ['68.9', '1.7']], [['Lenovo Legion Y540-15'], ['15.6', '128', '9', '4.6'], ['68.6', '2.3']], [['Xiaomi RedmiBook 16" Ryzen Edition'], ['16.1', '512', '13', '4.7'], ['61.9', '1.8']], [['HONOR MagicBook Pro'], ['16.1', '512', '11', '4.5'], ['56.8', '1.7']], [['ASUS VivoBook S15 M533IA'], ['15.6', '512', '6', '4.8'], ['57.5', '1.8']], [['Lenovo Yoga Slim 7 14'], ['14', '1024', '15', '4'], ['79.9', '1.4']], [['MSI GF63 Thin 9SCXR'], ['15.6', '512', '7', '4.6'], ['66.6', '1.9']], [['Acer Nitro 5 AN515-54'], ['15.6', '512', '8', '4.5'], ['59.8', '2.3']]]

def input_alternative():
    alternatives_name = []
    print("Enter alternatives name: ")
    while True:
        name = input("\t")
        if name:
            alternatives_name.append(name)
        else:
            break

    pos_criterion_number = int(input("Enter number of positive criterion: "))
    print("\tEnter " + str(pos_criterion_number) + " criterion name: ")
    for i in range(pos_criterion_number):
        pc = input("\t\t")
        pos_criterion_name.append(pc)

    neg_criterion_number = int(input("Enter number of negative criterion: "))
    print("\tEnter " + str(neg_criterion_number) + " criterion name: ")
    for i in range(neg_criterion_number):
        nc = input("\t\t")
        neg_criterion_name.append(nc)

    alternatives.append([["Solution"], pos_criterion_name, neg_criterion_name])

    for i in range(len(alternatives_name)):
        print("* With " + alternatives_name[i] + ":")
        lst_pos_para = []
        lst_neg_para = []
        for j in range(pos_criterion_number):
            para = input("\t - " + pos_criterion_name[j] + ": ")
            lst_pos_para.append(para)
        for j in range(neg_criterion_number):
            para = input("\t - " + neg_criterion_name[j] + ": ")
            lst_neg_para.append(para)

        alternatives.append([[alternatives_name[i]], lst_pos_para, lst_neg_para])

def print_alternative(number_pos, number_neg, alternatives):
    row_format = "{:^35} |" + "{:^10} | " * (number_pos + number_neg)
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

def check_in_pareto(pareto_element, alternative):
    for ele in pareto_element:
        if ele[0][0] == alternative[0][0]:
            return True
    return False

def pareto_optimal(alternatives):
    pareto_element = []
    tag = alternatives[0]

    for num_alternative in range(len(alternatives) - 1):
        copy_alternatives = alternatives.copy()
        copy_alternatives.pop(0)
        alternative1 = copy_alternatives.pop(num_alternative)
    
        for alternative in copy_alternatives:
            if dominates(alternative1, alternative) and not check_in_pareto(pareto_element, alternative1):
                pareto_element.append(alternative1)
    pareto_element.insert(0, tag)
    return pareto_element

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
        NCritetion -= 1
        a_max = copy_alternatives[0]
        for i in range(1, len(copy_alternatives)):
            if float(copy_alternatives[i][1][NCriterion]) > float(a_max[1][NCriterion]):
                a_max = copy_alternatives[i]
        best_alternative.append(a_max)

    elif NCriterion > len(pos_criterion_name):
        NCriterion -= (len(pos_criterion_name) + 1)
        a_min = copy_alternatives[0]
        for i in range(1, len(copy_alternatives)):
            if float(copy_alternatives[i][2][NCriterion]) < float(a_min[2][NCriterion]):
                a_min = copy_alternatives[i]
        best_alternative.append(a_min)

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

# #input_alternative()

while True:
    print("\n" + "-" * 40 + "MENU" + "-" * 40)
    print("[1] - Print all alternatives")
    print("[2] - Pareto optimal set")
    print("[3] - Optimal solutions when setting limits")
    print("[4] - Sub-optimization")
    print("[0] - Exit!")
    print("-" * 40 + "----" + "-" * 40)
    my_choice = int(input("Enter your choice: "))

    pareto_ele = pareto_optimal(alternatives)

    if my_choice == 1:
        print("\n" + "-"*49 + "All alternatives" + "-"*49)
        print_alternative(len(pos_criterion_name), len(neg_criterion_name), alternatives)

    elif my_choice == 2:
        print("\n" + "-"*48 + "Pareto Optimal Set" + "-"*48)
        print_alternative(len(pos_criterion_name), len(neg_criterion_name), pareto_ele)

    elif my_choice == 3:
        print("\n" + "-"*40 + "Specifying limit of criteria" + "-"*40)
        limit_ele = set_limit(alternatives)
        print("\n" + "-"*36 + "Set of element when limit has been applied" + "-"*36)
        print_alternative(len(pos_criterion_name), len(neg_criterion_name), limit_ele)
        print("\n" + "-"*29 + "Set of element when limit has been applied in Pareto set" + "-"*29)
        pareto_limit = []
        for ele in limit_ele:
            if ele in pareto_ele:
                pareto_limit.append(ele)
        print_alternative(len(pos_criterion_name), len(neg_criterion_name), pareto_limit)

    elif my_choice == 4:
        print("\n" + "-"*40 + "Sub-optimization" + "-"*40)
        sub_opt_ele = sub_optimization()
        print("\n" + "-"*41 + "Set of element sub-optimization" + "-"*42)
        print_alternative(len(pos_criterion_name), len(neg_criterion_name), sub_opt_ele)

    else:
        print("Thank you for using!")
        break