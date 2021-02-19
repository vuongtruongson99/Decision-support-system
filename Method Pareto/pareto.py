pos_criterion_name = ['Screen', 'SSD', 'Pin', 'Rate']
neg_criterion_name = ['Price', 'Weight']
criteria = [[['Solution'], ['Screen', 'SSD', 'Pin', 'Rate'], ['Price', 'Weight']], [['Acer Aspire 5 A515-44G'], ['15.6', '256', '10', '5'], ['60.9', '1.8']], [['ASUS ZenBook 13 UX325EA'], ['13.3', '512', '18', '5'], ['76.6', '1.07']], [['Lenovo IdeaPad 5 15'], ['15.6', '512', '14', '4.7'], ['68.9', '1.7']], [['Lenovo Legion Y540-15'], ['15.6', '128', '9', '4.6'], ['68.6', '2.3']], [['Xiaomi RedmiBook 16" Ryzen Edition'], ['16.1', '512', '13', '4.7'], ['61.9', '1.8']], [['HONOR MagicBook Pro'], ['16.1', '512', '11', '4.5'], ['56.8', '1.7']], [['ASUS VivoBook S15 M533IA'], ['15.6', '512', '6', '4.8'], ['57.5', '1.8']], [['Lenovo Yoga Slim 7 14'], ['14', '1024', '15', '4'], ['79.9', '1.4']], [['MSI GF63 Thin 9SCXR'], ['15.6', '512', '7', '4.6'], ['66.6', '1.9']], [['Acer Nitro 5 AN515-54'], ['15.6', '512', '8', '4.5'], ['59.8', '2.3']]]

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

    criteria.append([["Solution"], pos_criterion_name, neg_criterion_name])

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

        criteria.append([[alternatives_name[i]], lst_pos_para, lst_neg_para])

def print_criteria(number_pos, number_neg, criteria):
    row_format = "{:^10} | " * (number_pos + number_neg)
    row_format = "{:^35} |" + row_format
    for crit in criteria:
        c = [crit[i][j] for i in range(len(crit)) for j in range(len(crit[i]))]
        print(row_format.format(*c))

# Check criteria1 is dominates criteria2?
def dominates(criteria1, criteria2):
    for i in range(len(pos_criterion_name)):
        if float(criteria1[1][i]) < float(criteria2[1][i]):
            return False
    
    for i in range(len(neg_criterion_name)):
        if float(criteria1[2][i]) > float(criteria2[2][i]):
            return False
    
    return True

def check_in_pareto(pareto_element, criterion):
    for ele in pareto_element:
        if ele[0][0] == criterion[0][0]:
            return True
    return False

def pareto_optimal(criteria):
    pareto_element = []
    tag = criteria[0]

    for num_criteria in range(len(criteria) - 1):
        copy_criteria = criteria.copy()
        copy_criteria.pop(0)
        criterion1 = copy_criteria.pop(num_criteria)
    
        for criterion in copy_criteria:
            if dominates(criterion1, criterion) and not check_in_pareto(pareto_element, criterion1):
                pareto_element.append(criterion1)
    pareto_element.insert(0, tag)
    return pareto_element

def limit_element(criteria, NCritetion, limit, sign):
    limit_ele = []
    copy_criteria = criteria.copy()
    tag = copy_criteria.pop(0)
    
    if NCritetion <= len(pos_criterion_name):
        NCritetion -= 1
        for criterion in copy_criteria:
            if sign == '>=':
                if float(criterion[1][NCritetion]) >= limit:
                    limit_ele.append(criterion)
            elif sign == '<=':
                if float(criterion[1][NCritetion]) <= limit:
                    limit_ele.append(criterion)
    elif NCritetion > len(pos_criterion_name):
        NCritetion -= (len(pos_criterion_name) + 1)
        for criterion in copy_criteria:
            if sign == '>=':
                if float(criterion[2][NCritetion]) >= limit:
                    limit_ele.append(criterion)
            elif sign == "<=":
                if float(criterion[2][NCritetion]) <= limit:
                    limit_ele.append(criterion)
    limit_ele.insert(0, tag)
    return limit_ele

def set_limit(limit_ele):
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
                limit_ele = limit_element(limit_ele, choose, lim, "<=")
            else:
                lim = float(input("\t\tLimit for criterion " + neg_criterion_name[choose - len(pos_criterion_name) - 1] + " is less than or equal: "))
                limit_ele = limit_element(limit_ele, choose, lim, "<=")
        elif choose_limit == 2:
            if choose <= len(pos_criterion_name):
                lim = float(input("\t\tLimit for criterion " + pos_criterion_name[choose - 1] + " is greater than or equal: "))
                limit_ele = limit_element(limit_ele, choose, lim, ">=")
            else:
                lim = float(input("\t\tLimit for criterion " + neg_criterion_name[choose - len(pos_criterion_name) - 1] + " is greater than or equal: "))
                limit_ele = limit_element(limit_ele, choose, lim, ">=")
                
#input_alternative()
print_criteria(len(pos_criterion_name), len(neg_criterion_name), criteria)
#print(criteria)

# Pareto element
print("\n" + "-"*40 + "{}".format("Pareto Optimal Set") + "-"*40)
pareto_ele = pareto_optimal(criteria)
print_criteria(len(pos_criterion_name), len(neg_criterion_name), pareto_ele)

# Set limit for each criterion
print("\n" + "-"*40 + "{}".format("Specifying limit of criteria") + "-"*40)
limit_ele = criteria.copy()
set_limit(limit_ele)

# Print list of element when have limit
print("Element when have limit")
print_criteria(len(pos_criterion_name), len(neg_criterion_name), limit_ele)

# Print list of element have limit and in pareto-element
print("Element when have limit and in pareto-optimal")
pareto_limit = []
for ele in limit_ele:
    if ele in pareto_ele:
        pareto_limit.append(ele)
print_criteria(len(pos_criterion_name), len(neg_criterion_name), pareto_limit)