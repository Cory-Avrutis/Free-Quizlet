import random 
def validQuiz(cards):
    if len(cards) < 2:
        return False
    # needs at least two different definitions to make a quiz
    values = list(cards.values())
    for term in cards:
        if values[0] != cards[term]:
            return True
    return False

def createQuiz(cards):
    values = list(cards.values())
    questions = []
    for term in cards:
        ans = cards[term]
        answer = random.randint(1, 4)
        if answer == 1:
            question = {'question': term, 'answer': 'A', 'choiceA': ans, 'choiceB': randAns(ans, values), 'choiceC': randAns(ans, values), 'choiceD': randAns(ans, values)}
        elif answer == 2:
            question = {'question': term, 'answer': 'B', 'choiceA': randAns(ans, values), 'choiceB': ans, 'choiceC': randAns(ans, values), 'choiceD': randAns(ans, values)}
        elif answer == 3:
            question = {'question': term, 'answer': 'C', 'choiceA': randAns(ans, values), 'choiceB': randAns(ans, values), 'choiceC': ans, 'choiceD': randAns(ans, values)}
        elif answer == 4:
            question = {'question': term, 'answer': 'D', 'choiceA': randAns(ans, values), 'choiceB': randAns(ans, values), 'choiceC': randAns(ans, values), 'choiceD': ans}
        questions.append(question)
    return questions

def randAns(ans, values):
    randAns = values[random.randint(0, len(values)-1)]
    while randAns == ans:
        randAns = values[random.randint(0, len(values)-1)]
    return randAns
