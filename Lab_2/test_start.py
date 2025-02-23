import os
import subprocess


script_to_test = "test_negative_case.py"

if __name__ == "__main__":
    print(f"Запуск тестирования негативных случаев для {script_to_test}...")

    if not os.path.exists(script_to_test):
        print(f"Ошибка: Файл {script_to_test} не найден!")
    else:
        try:
            subprocess.run(["python", script_to_test], check=True)
            print("Тестирование завершено успешно. Результаты записаны в results.txt.")
        except subprocess.CalledProcessError as e:
            print(f"Ошибка при выполнении тестов: {e}")
