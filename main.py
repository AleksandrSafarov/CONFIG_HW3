import sys
import argparse
import re
import xml.etree.ElementTree as ET

# Константы для синтаксиса конфигурационного языка
COMMENT_START = "{{!--"
COMMENT_END = "--}}"

# Регулярные выражения для проверки имен и значений
NAME_REGEX = r'^[a-zA-Z][a-zA-Z0-9]*$'
NUMBER_REGEX = r'^\d+$'

# Функции для вычислений в префиксной нотации
def evaluate_expression(expr, constants):
    tokens = expr.strip("|").split()
    if len(tokens) < 3:
        raise ValueError(f"Неверное выражение: {expr}")
    operation, *operands = tokens

    # Преобразуем операнды
    operands = [constants.get(op, op) for op in operands]
    # Преобразуем операнды в целые числа, если это возможно
    operands = [int(op) if isinstance(op, str) and op.isdigit() else op for op in operands]

    if operation == '+':
        return sum(operands)
    elif operation == '-':
        return operands[0] - operands[1]
    elif operation == '*':
        return operands[0] * operands[1]
    elif operation == '/':
        return operands[0] // operands[1]
    elif operation == 'mod':
        return operands[0] % operands[1]
    elif operation == 'max':
        return max(operands)
    else:
        raise ValueError(f"Неизвестная операция: {operation}")

def parse_xml(input_xml):
    try:
        tree = ET.ElementTree(ET.fromstring(input_xml))
        return tree
    except ET.ParseError as e:
        raise ValueError(f"Ошибка синтаксиса XML: {e}")

def xml_to_config(tree):
    output = []
    constants = {}

    for elem in tree.iter():
        if elem.tag == 'comment':
            output.append(f"{COMMENT_START}\n{elem.text}\n{COMMENT_END}")
        
        elif elem.tag == 'const':
            name = elem.get('name')
            value = elem.get('value')
            if not re.match(NAME_REGEX, name):
                raise ValueError(f"Недопустимое имя константы: {name}")
            if not re.match(NUMBER_REGEX, value):
                raise ValueError(f"Недопустимое значение константы: {value}")
            output.append(f"(def {name} {value})")
            constants[name] = int(value)

        elif elem.tag == 'dictionary':
            output.append("$[")
            for entry in elem:
                if entry.tag == 'entry':
                    entry_name = entry.get('name')
                    entry_value = entry.get('value')
                    if not re.match(NAME_REGEX, entry_name):
                        raise ValueError(f"Недопустимое имя словаря: {entry_name}")
                    output.append(f"  {entry_name} : {entry_value},")
            output.append("]")

        elif elem.tag == 'expr':
            expr = elem.get('value')
            result = evaluate_expression(expr, constants)
            output.append(f"# Вычислено значение выражения {expr}: {result}")

    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Конвертер XML в учебный конфигурационный язык")
    parser.add_argument("output_file", help="Путь к выходному файлу для сохранения результата")
    parser.add_argument("input_file", help="Путь к входному XML-файлу")
    args = parser.parse_args()

    # Чтение XML-данных из указанного файла
    with open(args.input_file, 'r', encoding="utf-8") as f:
        input_xml = f.read()



    # Разбор XML и преобразование
    tree = parse_xml(input_xml)
    config_output = xml_to_config(tree)

    # Запись в выходной файл
    # Запись в выходной файл
    with open(args.output_file, 'w', encoding="utf-8") as f:
        f.write(config_output)
    print(f"Конфигурация успешно сохранена в {args.output_file}")

if __name__ == "__main__":
    main()
