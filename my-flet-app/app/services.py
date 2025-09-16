# Модуль содержит реализации алгоритмов построения префиксных кодов:
# ShannonFano и Huffman. Каждая реализация умеет:
# - принимать текст,
# - строить таблицу частот и коды для символов,
# - кодировать и декодировать строки,
# - возвращать статистику в виде DataFrame, средней длины кода и энтропии.
from collections import Counter
import heapq
import math
import pandas as pd
from typing import Tuple

class ShannonFano:
    # Класс реализует алгорим Шеннона—Фано.
    def __init__(self, text=None):
        # text: исходная строка (может быть None).
        # freq: словарь частот символов.
        # codes: словарь соответствия символ -> код.
        self.__text = text
        self.freq = dict(Counter(text))
        self.codes = {}
        self._build_codes()
    
    @property
    def text(self):
        # Геттер для текста.
        return self.__text
    
    @text.setter
    def text(self, value):
        # Сеттер: при установке текста пересчитываем частоты и коды.
        self.__text = value
        self.freq = dict(Counter(value))
        self.codes = {}
        self._build_codes()

    def _build_codes(self):
        # Строит коды, если есть текст и частоты.
        if self.text is None or not self.freq:
            return 
        # Сортируем символы по убыванию частоты и запускаем рекурсивную разметку.
        items = sorted(self.freq.items(), key=lambda x: x[1], reverse=True)
        self._shannon_fano(items, "")
    
    def _shannon_fano(self, items, prefix):
        # Рекурсивная функция разбиения списка символов на две части с близкими суммами частот.
        # Левой части приписывается '0', правой — '1'.
        if len(items) == 1:
            char, _ = items[0]
            # Если только один символ, даём ему код (или "0" если префикс пуст).
            self.codes[char] = prefix or "0"
            return
        total = sum(f for _, f in items)
        acc = 0
        for i in range(len(items)):
            acc += items[i][1]
            if acc >= total / 2:
                break
        left, right = items[:i+1], items[i+1:]
        self._shannon_fano(left, prefix + "0")
        if right:
            self._shannon_fano(right, prefix + "1")
    
    def encode(self):
        # Кодирует исходный текст, заменяя каждый символ на его код.
        return "".join(self.codes[c] for c in self.text)
    
    def decode(self, encoded_text):
        # Декодирует последовательность битов, перебирая буфер до нахождения соответствия в словаре.
        rev_codes = {v: k for k, v in self.codes.items()}
        result = ""
        buffer = ""
        for bit in encoded_text:
            buffer += bit
            if buffer in rev_codes:
                result += rev_codes[buffer]
                buffer = ""
        return result
    
    def analytics(self) -> Tuple[pd.DataFrame, float, float]:
        # Возвращает (DataFrame с символами, средняя длина кода, энтропия).
        total = sum(self.freq.values())
        analytics = []
        for char, f in self.freq.items():
            analytics.append({"Символ": char, 
                              "Вероятность": f/total, 
                              "Код": self.codes[char], 
                              "Длина кода":len(self.codes[char])
                              })
        # Средняя длина кода (в битах на символ)
        avg_len = sum((len(self.codes[c]) * f/total) for c, f in self.freq.items())
        # Энтропия исходного распределения
        entropy = -sum((f/total) * math.log2(f/total) for f in self.freq.values())
        df = pd.DataFrame(analytics)
        return df, avg_len, entropy 

class Huffman:
    # Класс реализует алгоритм Хаффмана.
    def __init__(self, text=None):
        # Аналогично: хранит текст, частоты и коды.
        self.__text = text
        self.freq = dict(Counter(text))
        self.codes = {}
        self._build_codes()
    
    @property
    def text(self):
        return self.__text
    @text.setter
    def text(self, value):
        # При установке текста обновляем данные и перестраиваем коды.
        if value is None:
            return 
        self.__text = value
        self.freq = dict(Counter(value))
        self.codes = {}
        self._build_codes()
        
    def _build_codes(self):
        # Построение кодов через мин-кучу (heap).
        if self.text is None or not self.freq:
            return
        # Каждый элемент кучи: [частота, [символ, код]]
        heap = [[f, [char, ""]] for char, f in self.freq.items()]
        heapq.heapify(heap)
        # Объединяем два наименьших узла, приписываем 0/1
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0]+hi[0]] + lo[1:] + hi[1:])
        # Распаковываем коды из итоговой кучи
        for pair in heapq.heappop(heap)[1:]:
            self.codes[pair[0]] = pair[1]
    
    def encode(self):
        # Кодирование строки по словарю codes.
        return "".join(self.codes[c] for c in self.text)
    
    def decode(self, encoded_text):
        # Декодирование как и в ShannonFano по обратному словарю.
        rev_codes = {v: k for k, v in self.codes.items()}
        result = ""
        buffer = ""
        for bit in encoded_text:
            buffer += bit
            if buffer in rev_codes:
                result += rev_codes[buffer]
                buffer = ""
        return result
    
    def analytics(self) -> Tuple[pd.DataFrame, float, float]:
        # Формируем DataFrame со статистикой, среднюю длину и энтропию.
        total = sum(self.freq.values())
        analytics = []
        for char, f in self.freq.items():
            analytics.append({"Символ": char, 
                              "Вероятность": f/total, 
                              "Код": self.codes[char], 
                              "Длина кода":len(self.codes[char])
                              })
        avg_len = sum((len(self.codes[c]) * f/total) for c, f in self.freq.items())
        entropy = -sum((f/total) * math.log2(f/total) for f in self.freq.values())
        df = pd.DataFrame(analytics)
        return df, avg_len, entropy
