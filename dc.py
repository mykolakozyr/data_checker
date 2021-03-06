# -*- coding: utf-8 -*-

#DATA CHECKER
file = open ('temp.csv','r')
file_output = open ('test.csv','a')

#function for checking Users' answer
def check_answer(a, b):
    while True:
        attr_names = raw_input(b)
        if attr_names == 'y':
            a = 1
            break
        elif attr_names == 'n':
            a = 0
            break
        else:
            print 'Invalid input'
            continue
    return a

quest = 'Does your file have the attributes names (y/n)? '
count = 0
count = check_answer(count, quest) #checking if we got some attribute names

separator = raw_input('Enter the delimiter symbol: ')

list_names = list() #list for attributes names

#add rules for the attribute
def add_rules(a):
    while True:
        inp = raw_input('Enter the possible option for the "' + str(a) + '" value: ')
        if inp == 'secret word':
            break
        globals()['list_'+str(a)].append(inp)
    print globals()['list_'+str(a)]

#check if the value exists in our rules table
def check_value(a, b):
    if a in globals()['list_'+str(b)]:
        file_output.write(str(a)+',')
        pass
    elif str(a) in globals()['dict_'+str(b)]:
            file_output.write(str(globals()['dict_'+str(b)][str(a)])+',')
    else:
        corrected_value = raw_input(unicode(('There is a value "' + str(a) + '" in the column "'+str(b)+'" . Enter the correct value: '), 'utf-8')) #enter the corrected value
        globals()['dict_'+str(b)][str(a)] = corrected_value
        file_output.write(str(corrected_value)+',')

#upload rules via the same named file
def upload_rules(a):
    try:
        file = open (str(a)+'.txt','r')
        for line in file:
            line = line.split(',')
            for v in line:
                v = v.strip()
                globals()['list_'+str(a)].append(v)
    except KeyError:
        print 'Cannot find the file'
        add_rules(a)
    print globals()['list_'+str(a)]
    
for line in file:
    if count == 1: #checking data with attributes names
        line = line.split(separator)
        for i in line:
            i = i.strip()
            quest = 'Do we have some special attributes for the column "'+str(i)+'" ? (y/n)'
            rule_need = 0
            rule_need = check_answer(rule_need, quest) #checking if we need rules to selected attributes
            file_output.write(str(i) + ',')  # write the first row
            if rule_need == 1:
                list_names.append(i) #add the attribute name to the list
                globals()['list_'+str(i)] = list() #create a list for every attribute name. Rules are going to be store here
                globals()['dict_'+str(i)] = dict() #create a dict for every attribute name. New rules are going to be store here
                count = int(count)+1
                quest = 'Should I try to upload the rules? (y/n)'
                upl_need = 0
                upl_need = check_answer(upl_need, quest)
                if upl_need == 1:
                    upload_rules(i)
                else:
                    add_rules(i)
            else:
                list_names.append('0')
                continue
        file_output.write('\n')
        count = count + 1 #for preventing ask rules for the second line
    else: #checking next data lines
        line = line.split(separator)
        cnt = 0
        for i in line:
            i = i.strip()
            try:
                if list_names[cnt] == '0':
                    file_output.write(str(i)+',')
                    cnt = cnt + 1
                    continue
                else:
                    check_value(i, list_names[cnt])
                    cnt = cnt + 1
            except IndexError:
                continue
        file_output.write('\n')


file = open ('test.csv','r')
file_final = open ('output.txt','w')
for line in file:
    file_final.write(str(line[0:-2])+'\n')