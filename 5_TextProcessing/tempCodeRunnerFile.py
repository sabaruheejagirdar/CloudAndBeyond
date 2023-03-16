g_question = 'cat dog 42 compu5 1huh 0 apple'
    updatedList = []

    spacedList = g_question.split()

    for i in spacedList:
        if i.isdigit():
            i = '#{0}'.format(i)
            updatedList.append(i)
        elif i.isalpha():
            i = '${0}'.format(i)
            updatedList.append(i)
        else:
            updatedList.append(i)

    updatedString = ' '.join(updatedList)
    prin