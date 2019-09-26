definitions = {}

def execute(pieces):
    states = {
        'getPreOp': 0,
        'getOp': 1,
        'getPostOp': 2,
        'error': 3
    }

    state = states['getPreOp']
    pointer = 0
    while state != states['error']:
        if pieces[pointer] == '=':
            try:
                return definitions[num]
            except:
                return 'unknown'

        try:
            if state == states['getPreOp']:
                num = definitions[pieces[pointer]]
                state = states['getOp']
            elif state == states['getOp']:
                op = pieces[pointer]
                state = states['getPostOp']
            elif state == states['getPostOp']:
                operand = definitions[pieces[pointer]]
                state = states['getOp']

                if op == '+':
                    num += operand
                elif op == '-':
                    num -= operand
        except:
            return 'unknown'
        finally:
            pointer += 1

def setName(name, value):
    if name in definitions:
        del definitions[definitions[name]]
    definitions[name] = value
    definitions[value] = name

while True:
    try:
        line = input().split()
    except EOFError:
        break

    command = line[0]
    if command == 'def':
        word = line[1].lower()
        num = int(line[2])
        setName(word, num)
    elif command == 'clear':
        definitions = {}
    elif command == 'calc':
        print(*line[1:], sep=' ', end=' ')
        print(execute(line[1:]))
