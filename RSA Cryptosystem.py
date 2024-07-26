import random

# Using BEARCATII to restrict the characters to the blank and lowercase
bearcatii = ' abcdefghijklmnopqrstuvwxyz'

#using Miller-Robin primality testing to check prime numbers 
def MillerRobinPrimalityTest(n,k=5):
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
#ramping up correctness using MCRepeat
    def MCRepeat(k):
        for _ in range(k):
            a = random.randint(2, n - 2)
            x = pow(a, n - 1, n)
            if x != 1:
                return False
        return True
    return MCRepeat(k)

#Method to generate prime number
def generate_prime():
    while True:
        #specifying number range within 676-65536 because 456975 < n < 4,294,967,297
        prime_value = random.randint(676,65536)
        if prime_value % 2 == 0:
            # Making sure the prime_value is odd
            prime_value += 1  
        if MillerRobinPrimalityTest(prime_value):
            return prime_value

#Function to generate p & q using generate_prime()
def generate_pq():  
    while True:
        p = generate_prime()
        q = generate_prime()
        # Regenerate q if it's equal to p
        while p == q:
            p, q = generate_prime()  
        return p, q
    
   
#Function to set n value
def set_n_value(p, q):
   n = p * q
   #Checking if n is greater than 14348906, if yes, return n value, otherwise generate p and q again
   if n>14348906:
    return n
   else:
    p,q= generate_pq()
    return set_n_value(p, q)
    
#Function to compute phi value
def compute_phi_n(p, q):
    return (p - 1) * (q - 1)

#Using extended Euclid algorithm to calculate GCD
def ext_Euclid_gcd(a, b):
    if b == 0:
        g = a
        s = 1
        t = 0
        return g, s, t
    else:
        r = a % b
        q = a // b
        g, s, t = ext_Euclid_gcd(b, r)
        s_temp = s
        s = t
        t = s_temp - t * q
        return g, s, t

#Function to compute private key d using extended Euclid algorithm 
def compute_private_key(e, phi_n):
    g, s, t = ext_Euclid_gcd(e, phi_n)
    if g == 1:
        d = s % phi_n
        #if s in negative then add phi_n to the private key value
        if d <0:
            d = d + phi_n
        return d
    
# Function to encode a message into a list of integers based on the bearcatii
def encode_message(message):
    encoded_chars = []
    for char in message:
        if char in bearcatii:
            encoded_chars.append(bearcatii.index(char.lower()))
    return encoded_chars

# Function to decode a list of integers back into a message using the bearcatii
def decode_message(encoded_message):
    decoded_chars = []
    for digit in encoded_message:
        decoded_chars.append(bearcatii[digit])
    return "".join(decoded_chars)

# Function to encrypt a message using the RSA encryption algorithm
def encrypt_message(m, e, n):
    decimal_message = encode_message(m)
    encrypted_message = [pow(char, e, n) for char in decimal_message]
    encrypted_chars = [bearcatii[decimal % len(bearcatii)] for decimal in encrypted_message]
    new_encrypted_chars= "".join(encrypted_chars)
    return encrypted_message, new_encrypted_chars 

# Function to decrypt an encrypted message using the RSA decryption algorithm
def decrypt_message(encrypted_message, d, n):
    decrypted_decimal = [pow(char, d, n) for char in encrypted_message]
    decrypted_chars = [bearcatii[decimal % len(bearcatii)] for decimal in decrypted_decimal]
    return "".join(decrypted_chars)

if __name__ == "__main__":
    while True:
        try:
            #Taking public key as input
            e = int(input('Input a positive integer for public key (e): '))
            if e > 0:
                p, q = generate_pq()
                phi_n = compute_phi_n(p, q)
                n = set_n_value(p, q)
                g, s, t = ext_Euclid_gcd(e, phi_n)
                #Checking if n = pq is relatively prime to the public key e 
                if g == 1:
                    break
                else:
                    print("The input 'e' is not relatively prime to n.")
            else:
                print("Please enter a positive integer for 'e'.")
        #If public key is not a positive integer, raise ValueError
        except ValueError:
            print("Invalid input. Please enter a positive integer for 'e'.")
        #Re-enter value of e
        retry = input("Do you want to enter 'e' again? (y/n): ")
        if retry.lower() != 'y':
            break
        
    #Taking input message and converting the message into lowercase
    M = input("Input your message: ").lower()
    d = compute_private_key(e, phi_n)
    encrypted_message, encrypted_chars = encrypt_message(M, e, n)
    decrypted_message = decrypt_message(encrypted_message, d, n)
    
    print("Original message (in lowercase), M:", M)
    print("p:", p)
    print("q:", q)
    print("n:", n)
    print("Phi value:",phi_n)
    print("Public key:", e)
    print("Private key:", d)
    print("Encrypted message, C:", encrypted_chars)
    print("Decrypted message, P:", decrypted_message)

