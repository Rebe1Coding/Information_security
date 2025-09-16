
# Тестовый файл для проверки функционала без GUI
from services import *


h = Huffman()
sh = ShannonFano()

text = "hello world"
sh.text = text
print("Зашифрованное сообщение с помощью Шанно - Фано:")
encoded_sh = sh.encode()
print(f"Encoded: {encoded_sh}")
decoded_sh = sh.decode(encoded_sh)
print(f"Decoded: {decoded_sh}") 
df, a, e = sh.analytics()
print(df.to_markdown())
print(f"Average code length: {a:.3f}")
print(f"Entropy: {e:.3f}") 

h.text = text
print("\nЗашифрованное сообщение с помощью Хаффмана:")  
encoded_h = h.encode()
print(f"Encoded: {encoded_h}")  
decoded_h = h.decode(encoded_h)
print(f"Decoded: {decoded_h}")
df, a, e = h.analytics()
print(df.to_markdown())
print(f"Average code length: {a:.3f}")  
print(f"Entropy: {e:.3f}")