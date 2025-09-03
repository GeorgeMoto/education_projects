import os
import sys
import subprocess
import shutil


def check_virtual_env():
    # проверка, запущен ли скрипт в виртуальной среде
    if not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        raise RuntimeError("Скрипт должен быть запущен в виртуальной среде!")


def install_libraries():
    # Установка библиотек одновременно
    libraries = ['beautifulsoup4', 'pytest', 'termgraph']

    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + libraries)
    except subprocess.CalledProcessError:
        print("Ошибка при установке библиотек")
        sys.exit(1)


def save_requirements():
    # Сохранение списка в requirements.txt
    try:
        result = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'], text=True)
        with open('requirements.txt', 'w') as f:
            f.write(result)
        print(result)
    except subprocess.CalledProcessError:
        print("Не удалось сохранить requirements")
        sys.exit(1)


def archive_env():
    # архивация виртуальной среды

    # Получаем путь к текущей виртуальной среде
    venv_path = os.path.dirname(os.path.dirname(sys.executable))

    # Создаем архив
    shutil.make_archive('venv_archive', 'zip', venv_path)
    print("Архив виртуальной среды создан: venv_archive.zip")


def main():
    check_virtual_env()
    install_libraries()
    save_requirements()
    archive_env()


if __name__ == '__main__':
    main()