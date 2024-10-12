import collections
import math

import huffman
from collections import Counter

def get_total_information(file_path):
    def calculate_information(probability):
        if probability == 0:
            return 0
        return -math.log2(probability)

    # Открываем файл для анализа (замените "file.txt" на имя вашего файла)
    with open(file_path, 'rb') as file:
        file_content = file.read()

    # Рассчитываем длину файла в байтах
    file_length = len(file_content)

    # Считаем частоту вхождения каждого байта
    byte_frequencies = collections.Counter(file_content)

    # Рассчитываем вероятность и информацию для каждого байта
    byte_probabilities = {byte: freq / file_length for byte, freq in byte_frequencies.items()}
    byte_information = {byte: calculate_information(prob) for byte, prob in byte_probabilities.items()}

    # Рассчитываем суммарное количество информации в файле
    total_information = sum(freq * byte_information[byte] for byte, freq in byte_frequencies.items())
    return total_information

# Функция для чтения содержимого файла
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


# Функция для сжатия данных методом Хаффмана
def huffman_compress(data):
    # Вычисляем частоты символов
    freq_counter = Counter(data)

    # Создание кодировочной таблицы Хаффмана
    huffman_tree = huffman.codebook(freq_counter.items())

    # Кодируем данные
    encoded_data = ''.join(huffman_tree[char] for char in data)

    return huffman_tree, encoded_data


# Функция для декодирования данных
def huffman_decompress(huffman_tree, encoded_data):
    # Создаём обратную кодировочную таблицу для декодирования
    reverse_tree = {v: k for k, v in huffman_tree.items()}

    # Декодируем строку
    decoded_data = ""
    buffer = ""

    for bit in encoded_data:
        buffer += bit
        if buffer in reverse_tree:
            decoded_data += reverse_tree[buffer]
            buffer = ""


    return decoded_data


# Основная функция для демонстрации сжатия и декодирования
def main(input_file):
    # Чтение исходного файла
    data = read_file(input_file)
    print(f"Исходный текст:\n{data}\n")
    print(f"Длина исходных данных: {len(data)} символов")

    # Сжатие данных
    huffman_tree, compressed_data = huffman_compress(data)
    print(f"Сжатые данные:\n{compressed_data}\n")
    print(f"Длина сжатых данных: {len(compressed_data)} бит")
    print(f"Оценка количества информации исходного файла {input_file}: {get_total_information(input_file)}")

    # Декодирование сжатых данных
    decompressed_data = huffman_decompress(huffman_tree, compressed_data)
    print(f"Декодированные данные:\n{decompressed_data}\n")
    print(f"Длина декодированных данных: {len(decompressed_data)} символов")

    # Проверка корректности декодирования
    assert data == decompressed_data, "Ошибка: исходные и декодированные данные не совпадают!"
    print("Сжатие и декодирование прошли успешно!")


main("example.txt")
