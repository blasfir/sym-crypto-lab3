import re
alphabet = "абвгдежзийклмнопрстуфхцчшщьыэюя"

def letter_frequencies(text, alphabet):
    result = []
    for char in alphabet:
        count = text.count(char)
        result.append(count)
    return result

def bigram_frequencies(text, alphabet, step=1):
    alphabet_len = len(alphabet)
    result = []
    for i in range(alphabet_len):
        row = []
        for j in range(alphabet_len):
            row.append(0)
        result.append(row)
    filtered_text = ""
    for char in text:
        if char in alphabet:
            filtered_text += char 
    text = filtered_text           
    i = 0
    while i < len(text) - 1:
        first = text[i]
        second = text[i + 1]
        row_idx = alphabet.index(first)
        col_idx = alphabet.index(second)
        result[row_idx][col_idx] += 1
        i += step
    return result

def clean_text(text):
    text = text.lower()
    result = ''
    for char in text:
        if char in alphabet:
            result += char
    return result

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

#щбернене за модулем
def mod_inverse(num, mod):
    t = 0
    new_t = 1
    r = mod
    new_r = num
    while new_r != 0:
        quotient = r // new_r
        t, new_t = new_t, t - quotient * new_t
        r, new_r = new_r, r - quotient * new_r
    if r > 1:
        return None 
    if t < 0:
        t += mod
    return t

#лінійне порівняння
def solve_linear_congruence(a, b, mod):
    d = gcd(a, mod)
    if b % d != 0:
        return []
    new_a = a // d
    new_b = b // d
    new_mod = mod // d
    inverse = mod_inverse(new_a, new_mod)
    if inverse == None:
        return []
    x0 = (inverse * new_b) % new_mod
    result = []
    for i in range(d):
        r = (x0 + i * new_mod) % mod
        result.append(r)
    return result

#знайти 5 найчастіших біграм 
def top_5_bigrams(text, alphabet, step):
    frequencies_matrix = bigram_frequencies(text, alphabet, step)
    bigram_freq = []
    alphabet_len = len(alphabet)
    for i in range(alphabet_len):
        for j in range(alphabet_len):
            frequency = frequencies_matrix[i][j]
            if frequency > 0:
                bigram = alphabet[i] + alphabet[j]
                pair = (bigram, frequency)
                bigram_freq.append(pair)
    bigram_freq.sort(key=lambda x: x[1], reverse=True)
    result = []
    idx = 0
    while idx < 5 and idx < len(bigram_freq):
        bigram = bigram_freq[idx][0]
        result.append(bigram)
        idx += 1
    return result

def find_X(bigram, alphabet):
    i = alphabet.index(bigram[0])
    j = alphabet.index(bigram[1])
    c = len(alphabet)
    result = i * c + j
    return result

def find_bigram(number, alphabet):
    m = len(alphabet)
    i = number // m  
    j = number % m  
    result = alphabet[i] + alphabet[j]
    return result

def decrypt_X(a, b, Y, alphabet):
    m = len(alphabet)
    mod = m ** 2
    inverse = mod_inverse(a, mod)
    if inverse is None:
        return None
    result = (Y - b) * inverse % mod
    return result

def find_a(Y1, Y2, X1, X2, alphabet):
    m = len(alphabet)
    mod = m ** 2
    Y = (Y1 - Y2) % (mod)
    X = (X1 - X2) % (mod)
    result = solve_linear_congruence(X, Y, mod)
    return result

def find_b(Y1, X1, A, alphabet):
    m = len(alphabet)
    mod = m ** 2
    result = []
    for a in A:
        b = (Y1 - a * X1) % mod
        result.append(b)
    return result

def find_keys(real_top_5_bigrams, cipher_top_5_bigrams, alphabet):
    result = []
    for real_bigram1 in real_top_5_bigrams:
        for real_bigram2 in real_top_5_bigrams:
            if real_bigram1 == real_bigram2:
                continue
            for cipher_bigram1 in cipher_top_5_bigrams:
                for cipher_bigram2 in cipher_top_5_bigrams:
                    if cipher_bigram1 == cipher_bigram2:
                        continue
                    X1 = find_X(real_bigram1, alphabet)
                    X2 = find_X(real_bigram2, alphabet)
                    Y1 = find_X(cipher_bigram1, alphabet)
                    Y2 = find_X(cipher_bigram2, alphabet)
                    A = find_a(Y1, Y2, X1, X2, alphabet)
                    if not A:
                        continue
                    B = find_b(Y1, X1, A, alphabet)
                    for i in range(len(A)):
                        a = A[i]
                        b = B[i]
                        result.append((a, b))
    return result

def decrypt_affine(text, key, alphabet):
    a, b = key
    result = ""
    for i in range(0, len(text) - 1, 2):
        bigram = text[i:i+2]
        if len(bigram) < 2:
            continue  
        Y = find_X(bigram, alphabet)
        X = decrypt_X(a, b, Y, alphabet)
        if X is None:
            continue 
        bigram = find_bigram(X, alphabet)
        result += bigram
    return result

def russian_language_recognizer(text):
    consonants = "бвгджзйклмнпрстфхцчшщ"
    if re.search(f"[{consonants}]{{9,}}", text):
        return False
    if "ьь" in text or "ыы" in text:
        return False
    freqs = letter_frequencies(text, alphabet)
    total_letters = sum(freqs)
    if total_letters == 0:
        return False 
    expected_freq_ranges = {
        'о': (0.05, 0.20),
        'е': (0.05, 0.15),
        'а': (0.05, 0.15),
        'и': (0.04, 0.12),
        'н': (0.04, 0.10),
        'т': (0.04, 0.10),
        'с': (0.03, 0.09),
        'р': (0.03, 0.09),
    }
    for i, letter in enumerate(alphabet):
        if letter in expected_freq_ranges:
            count = freqs[i]
            freq = count / total_letters
            min_f, max_f = expected_freq_ranges[letter]
            if freq < min_f or freq > max_f:
                return False
    return True

def try_keys(text, keys, alphabet):
    result = []
    for pair in keys:
        decrypted = decrypt_affine(text, pair, alphabet)
        if russian_language_recognizer(decrypted):
            result.append(pair)
    return result
        

with open("text.txt", encoding="utf-8") as f:
    text = f.read().lower()

with open("text1.txt", encoding="utf-8") as f:
    text1 = f.read().lower()
    text1 = clean_text(text1) 

top_5_bigrams_text = top_5_bigrams(text, alphabet, 2)
real_top_5_bigrams = ['ст', 'но', 'то', 'на', 'ен']
top_5_bigrams_text1 = top_5_bigrams(text1, alphabet, 2)
keys = find_keys(real_top_5_bigrams, top_5_bigrams_text1, alphabet)
valid_keys = try_keys(text1, keys, alphabet)

print()
print(f"5 найчастіших біграм, які я шукала за допомогою функції:\n{top_5_bigrams_text}")
print()
print(f"5 реально найчастіших біграм:\n{real_top_5_bigrams}")
print()
print(f"5 найчастіших біграм шифротексту:\n{top_5_bigrams_text1}")
print()
#print(keys)
#print()
#print(valid_keys)
#(a=654, b=777)
for key in valid_keys:
    text2 = decrypt_affine(text1, key, alphabet)
    a, b = key
    if russian_language_recognizer(text2):
        print(f"Ключ (a={a}, b={b}):\n{text2}")