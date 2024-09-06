import string

from concurrent.futures import ThreadPoolExecutor
from collections import defaultdict

import requests
import matplotlib.pyplot as plt


def get_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Перевірка на помилки HTTP
        return response.text
    except requests.RequestException as e:
        print(e)
        return None

# Функція для видалення знаків пунктуації


def remove_punctuation(text):
    return text.translate(str.maketrans("", "", string.punctuation))


def map_function(word):
    return word, 1


def shuffle_function(mapped_values):
    shuffled = defaultdict(list)
    for key, value in mapped_values:
        shuffled[key].append(value)
    return shuffled.items()


def reduce_function(key_values):
    key, values = key_values
    return key, sum(values)

# Виконання MapReduce


def map_reduce(text, search_words=None):
    # Видалення знаків пунктуації
    text = remove_punctuation(text)
    words = text.split()

    # Якщо задано список слів для пошуку, враховувати тільки ці слова
    if search_words:
        words = [word for word in words if word in search_words]

    # Паралельний Мапінг
    with ThreadPoolExecutor() as executor:
        mapped_values = list(executor.map(map_function, words))

    # Крок 2: Shuffle
    shuffled_values = shuffle_function(mapped_values)

    # Паралельна Редукція
    with ThreadPoolExecutor() as executor:
        reduced_values = list(executor.map(reduce_function, shuffled_values))

    return dict(reduced_values)

# visualize top words


def visualize_top_words(n, words):
    sorted_words = list(
        dict(sorted(words.items(), key=lambda word: word[1])).items())[-n:]
    print(sorted_words)
    # print(words[sorted_words[0]])
    # for w in sorted_words.keys():
    #    print(w)
    plt.barh([i[0] for i in sorted_words], [i[1]
             for i in sorted_words], color='green')
    plt.xlabel('Count')
    plt.ylabel('Word')
    plt.title(f'Top {n} words chart')
    plt.show()


if __name__ == '__main__':
    # Вхідний текст для обробки
    url = "https://gutenberg.net.au/ebooks01/0100021.txt"
    text = get_text(url)
    # if text:
    # Виконання MapReduce на вхідному тексті
    #    search_words = ['war', 'peace', 'love']
    #    result = map_reduce(text, search_words)

    #    print("Результат підрахунку слів:", result)
    # else:
    #    print("Помилка: Не вдалося отримати вхідний текст.")

    if text:
        result = map_reduce(text)
        visualize_top_words(10, result)
        print("Data was vizualized")
    else:
        print("Error: Can't reach content")
