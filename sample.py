pi = [[12, 4, 6, 2, 10, 5, 11, 9, 14, 8, 13, 7, 0, 3, 15, 1],
	[6, 8, 2, 3, 9, 10, 5, 12, 1, 14, 4, 7, 11, 13, 0, 15],
	[11, 3, 5, 8, 2, 15, 10, 13, 14, 1, 7, 4, 12, 9, 6, 0],
	[12, 8, 2, 1, 13, 4, 15, 6, 7, 0, 10, 5, 3, 14, 9, 11],
	[7, 15, 5, 10, 8, 1, 6, 13, 0, 9, 3, 14, 11, 4, 2, 12],
	[5, 13, 15, 6, 9, 2, 12, 10, 11, 7, 8, 1, 4, 3, 14, 0],
	[8, 14, 2, 5, 6, 9, 1, 12, 15, 4, 11, 0, 13, 10, 3, 7],
	[1, 7, 14, 13, 0, 5, 8, 3, 4, 15, 10, 6, 9, 12, 11, 2]]

Range32 = 2 ** 32 - 1 #количество элементов в кольце вычетов 2 в степени 32

#Разделение строки
def split(x):
	first_subblock = x >> 32
	second_subblock = x & Range32
	return first_subblock, second_subblock

#соединение строки
def union(first_subblock, second_subblock):
	return (first_subblock << 32) ^ second_subblock

#Циклический сдвиг на 11 бит
def sdvc(x):
	right_block11 = (x << 11)
	left_block11 = (x >> (32 - 11))
	return (right_block11 ^ left_block11) & Range32

#Операция t
def t(x):
    y = 0
    for i in reversed(range(8)):
        npi = (x >> 4 * i) & 0xf
        y <<= 4
        y ^= pi[i][npi]
    return y


#Операция g
def g(x, k):
    sum = (x+k) % 2 ** 32
    return sdvc(t(sum))

#Операция G
def G(first_subblock, second_subblock, key):
	second_subblock, first_subblock = first_subblock, second_subblock ^ g(first_subblock, key)
	return first_subblock, second_subblock

#Генерация ключей
def magma_key_gen(k):
		keys = []
		for i in reversed(range(8)):
			keys.append((k >> (32 * i)) & Range32)
		for i in range(8):
			keys.append(keys[i])
		for i in range(8):
			keys.append(keys[i])
		for i in reversed(range(8)):
			keys.append(keys[i])
		return keys

def magma_encrypt(x, k):
	keys = magma_key_gen(k)
	L, R = split(x)
	for i in range(31):
			R, L = G(R, L, keys[i])
	R, L = G(R, L, keys[-1])
	return union(R, L)

def magma_decrypt(x, k):
	keys = magma_key_gen(k)
	keys.reverse()
	L, R = split(x)
	for i in range(31):
			R, L = G(R, L, keys[i])
	R, L = G(R, L, keys[-1])
	return union(R, L)

if __name__ == '__main__':
	text = input()
	k = int('ffeeddccbbaa99887766554433221100f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff', 16)

	hexadecimal = text.encode('utf-8').hex()
	if(len(hexadecimal) % 16 != 0):
		while(len(hexadecimal)%16 != 0):
			hexadecimal += "0"

	print(hexadecimal)

	substring_length = 16
	substrings = [hexadecimal[i:i+substring_length] for i in range(0, len(hexadecimal), substring_length)]

	CT = []
	text_chipher = ""
	for i in range(0, len(substrings)):
		CT.append(magma_encrypt(int(substrings[i], 16), k))

	Decr = ""
	for j in range(0, len(CT)):
		DT = magma_decrypt(CT[j], k)
		Decr += str(hex(DT))[2:]

	bytes_obj = bytes.fromhex(Decr)
	text = bytes_obj.decode('utf-8')
	print(text)