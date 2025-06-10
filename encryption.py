from werkzeug.security import generate_password_hash, check_password_hash

def hash_password(plain_password):
    return generate_password_hash(plain_password)

print("Admin:", hash_password("admin123"))
print("Supplier:", hash_password("supplier123"))
print("Hospital:", hash_password("hospital123"))