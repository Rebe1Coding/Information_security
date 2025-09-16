
from services import *


h = Huffman()


text = "hello world"
h.text = text
print("Shannon-Fano Encoding:")
encoded_sh = h.encode()
print(f"Encoded: {encoded_sh}")
decoded_sh = h.decode(encoded_sh)
print(f"Decoded: {decoded_sh}") 
df, a, s = h.analytics()
print(df.to_markdown())
print(f"Average code length: {a:.3f}")
print(f"Entropy: {s:.3f}")   