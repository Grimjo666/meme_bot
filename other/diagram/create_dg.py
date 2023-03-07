import matplotlib.pyplot as plt
import os


def create_diagram(person_info_list):
    # Создаем список долей каждого сектора
    percents = []
    # Создаем список меток для каждого сектора
    labels = []

    for person in person_info_list[:5]:

        labels.append(person[0])
        percents.append(person[1])

    colors = [(0.3, 0.4, 0.8), (0.8, 0.3, 0.3), (0.8, 0.6, 0.3), (0.3, 0.8, 0.8)]

    plt.cla()

    fig, ax = plt.subplots()

    # Строим круговую диаграмму на основе списка долей
    plt.pie(percents, autopct='%1.1f%%', colors=colors)
    ax.legend(labels, loc='center left', bbox_to_anchor=(0.9, 0.1))

    # сдвигаем диаграмму влево
    fig.subplots_adjust(left=-0.2)

    # Добавляем заголовок
    title = plt.title('Актив на 119:', fontsize=18)
    title.set_position([0.75, 1.05 - 20 / fig.dpi])

    # Сохраняем диаграмму
    plt.savefig('other/diagram/statistic_person_activ.png')
