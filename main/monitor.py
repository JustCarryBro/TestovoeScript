import subprocess
import time
import os
import signal
import sys


def start_process(command, output_file):
    """Запускает процесс и возвращает его объект."""
    with open(output_file, 'a') as out:
        print(f"Запускаю процесс: {' '.join(command)}")
        process = subprocess.Popen(command, stdout=out, stderr=subprocess.STDOUT)
    return process


def check_process(process):
    """Проверяет, запущен ли процесс."""
    return process.poll() is None


def kill_process(process):
    """Убивает процесс."""
    print(f"Убиваю процесс с PID: {process.pid}")
    os.kill(process.pid, signal.SIGKILL)


def main(command, kill_time, output_file):
    """Основная функция мониторинга процесса."""
    process = start_process(command, output_file)

    while True:
        time.sleep(kill_time)

        if not check_process(process):
            print("Процесс упал. Перезапуск...")
            process = start_process(command, output_file)
        else:
            print("Процесс все еще работает.")

        time.sleep(1)


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Использование: python monitor.py <команда> <время_убийства> <файл_вывода>")
        sys.exit(1)

    command = sys.argv[1].split()
    kill_time = int(sys.argv[2])
    output_file = sys.argv[3]

    main(command, kill_time, output_file)