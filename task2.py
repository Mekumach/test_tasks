import json
import random


def generate_versions(template, num_versions=2, max_value=9):
    # Разбираем шаблон на части, заменяя '*' на место для генерации случайных значений
    parsed_template = [(int(part) if part.isdigit() else '*') for part in template.split(".")]
    versions = []

    # Генерируем два случайных варианта вместо '*'
    for i in range(num_versions):
        version = []
        for part in parsed_template:
            if part == "*":
                version.append(str(random.randint(0, max_value)))
            else:
                version.append(str(part))
        versions.append(".".join(version))

    return versions


def main(version, config_file):
    # Считываем конфигурационный файл
    with open(config_file, 'r') as file:
        config_data = json.load(file)

    all_versions = []
    for key, template in config_data.items():
        generated_versions = generate_versions(template)
        all_versions.extend(generated_versions[:2])  # Берем по два варианта для каждого шаблона

    # Сортируем версии
    all_versions = sorted(all_versions, key=lambda s: list(map(int, s.split('.'))))

    # Версии старее указанной
    filtered_versions = [v for v in all_versions if list(map(int, v.split('.'))) < list(map(int, version.split('.')))]

    print("Все версии:", ", ".join(all_versions))
    print("Версии меньше чем", version, ":", ", ".join(filtered_versions))


version = input('Введите номер версии: ')
config_file = input("Введите путь к конфигурационному файлу: ")

main(version, config_file)
