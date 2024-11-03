import unittest
import subprocess

class TestConfigConverter(unittest.TestCase):

    def run_test_case(self, input_file, expected_output_file):
        # Запускаем скрипт main.py и читаем фактический вывод
        result_file = 'test_output.txt'
        subprocess.run(['python', 'main.py', result_file, input_file])

        # Читаем фактический и ожидаемый вывод
        with open(result_file, 'r', encoding='utf-8') as result_f:
            actual_output = result_f.read()
        
        with open(expected_output_file, 'r', encoding='utf-8') as expected_f:
            expected_output = expected_f.read()
        
        # Сравниваем фактический и ожидаемый результат
        self.assertEqual(actual_output.strip(), expected_output.strip())

    def test_example1(self):
        self.run_test_case('test_input1.xml', 'test_expected_output1.txt')

    def test_example2(self):
        self.run_test_case('test_input2.xml', 'test_expected_output2.txt')

    def test_example3(self):
        self.run_test_case('test_input3.xml', 'test_expected_output3.txt')


if __name__ == '__main__':
    unittest.main()
