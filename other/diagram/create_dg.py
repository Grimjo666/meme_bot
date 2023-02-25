import matplotlib.pyplot as plt


def create_diagram(person_info_list):
    # Создаем список долей каждого сектора
    sizes = []
    # Создаем список меток для каждого сектора
    labels = []

    for person in person_info_list[:5]:

        labels.append(person[0])
        sizes.append(person[1])

    colors = [(0.3, 0.4, 0.8), (0.8, 0.3, 0.3), (0.8, 0.6, 0.3), (0.3, 0.8, 0.8)]

    plt.rcParams['figure.facecolor'] = (0.6, 0.8, 0.7)

    # Строим круговую диаграмму на основе списка долей
    plt.pie(sizes, labels=labels, colors=colors)

    # Добавляем заголовок
    plt.title('Актив на 119')

    # Сохраняем диаграмму
    plt.savefig('other/diagram/statistic_person_activ.png')
