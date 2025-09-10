from collections import Counter
import heapq
import math

class ShannonFano:
    def __init__(self, text):
        self.text = text
        self.freq = dict(Counter(text))
        self.codes = {}
        self._build_codes()
    
    def _build_codes(self):
        items = sorted(self.freq.items(), key=lambda x: x[1], reverse=True)
        self._shannon_fano(items, "")
    
    def _shannon_fano(self, items, prefix):
        if len(items) == 1:
            char, _ = items[0]
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
        return "".join(self.codes[c] for c in self.text)
    
    def decode(self, encoded_text):
        rev_codes = {v: k for k, v in self.codes.items()}
        result = ""
        buffer = ""
        for bit in encoded_text:
            buffer += bit
            if buffer in rev_codes:
                result += rev_codes[buffer]
                buffer = ""
        return result
    
    def analytics(self):
        total = sum(self.freq.values())
        print("Символ | Частота | Код | Длина кода")
        for char, f in self.freq.items():
            print(f"'{char}' | {f/total:.3f} | {self.codes[char]} | {len(self.codes[char])}")
        avg_len = sum((len(self.codes[c]) * f/total) for c, f in self.freq.items())
        entropy = -sum((f/total) * math.log2(f/total) for f in self.freq.values())
        print(f"\nСредняя длина кода: {avg_len:.3f}")
        print(f"Энтропия: {entropy:.3f}")


class Huffman:
    def __init__(self, text):
        self.text = text
        self.freq = dict(Counter(text))
        self.codes = {}
        self._build_codes()
    
    def _build_codes(self):
        heap = [[f, [char, ""]] for char, f in self.freq.items()]
        heapq.heapify(heap)
        while len(heap) > 1:
            lo = heapq.heappop(heap)
            hi = heapq.heappop(heap)
            for pair in lo[1:]:
                pair[1] = '0' + pair[1]
            for pair in hi[1:]:
                pair[1] = '1' + pair[1]
            heapq.heappush(heap, [lo[0]+hi[0]] + lo[1:] + hi[1:])
        for pair in heapq.heappop(heap)[1:]:
            self.codes[pair[0]] = pair[1]
    
    def encode(self):
        return "".join(self.codes[c] for c in self.text)
    
    def decode(self, encoded_text):
        rev_codes = {v: k for k, v in self.codes.items()}
        result = ""
        buffer = ""
        for bit in encoded_text:
            buffer += bit
            if buffer in rev_codes:
                result += rev_codes[buffer]
                buffer = ""
        return result
    
    def analytics(self):
        total = sum(self.freq.values())
        print("Символ | Частота | Код | Длина кода")
        for char, f in self.freq.items():
            print(f"'{char}' | {f/total:.3f} | {self.codes[char]} | {len(self.codes[char])}")
        avg_len = sum((len(self.codes[c]) * f/total) for c, f in self.freq.items())
        entropy = -sum((f/total) * math.log2(f/total) for f in self.freq.values())
        print(f"\nСредняя длина кода: {avg_len:.3f}")
        print(f"Энтропия: {entropy:.3f}")


# Пример использования
text = "hello world"
sf = ShannonFano(text)
hf = Huffman(text)

print("=== Shannon-Fano ===")
sf.analytics()
encoded_sf = sf.encode()
decoded_sf = sf.decode(encoded_sf)
print(f"Закодировано: {encoded_sf}")
print(f"Декодировано: {decoded_sf}")

print("\n=== Huffman ===")
hf.analytics()
encoded_hf = hf.encode()
decoded_hf = hf.decode(encoded_hf)
print(f"Закодировано: {encoded_hf}")
print(f"Декодировано: {decoded_hf}")
