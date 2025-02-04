with open('INPUT.TXT', 'r') as file:
    n = int(file.read().strip())

sum_of_divisors = 0


for i in range(1, n + 1):
    if n % i == 0:
        sum_of_divisors += i


with open('OUTPUT.TXT', 'w') as file:
    file.write(str(sum_of_divisors))