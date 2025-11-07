from utils.security import hash_password, verify_password, generate_refresh_token, create_access_token, decode_token
import re

def test_password_hash_and_verify():
    hashed = hash_password('Secret123!')
    assert hashed != 'Secret123!'
    assert verify_password('Secret123!', hashed)


def test_generate_refresh_token_unique():
    t1 = generate_refresh_token()
    t2 = generate_refresh_token()
    assert t1 != t2
    assert re.fullmatch(r'[0-9a-f]{64}', t1)


def test_access_token_round_trip():
    token = create_access_token('subject-1', extra_claims={'role': 'manager'}, expires_minutes=5)
    decoded = decode_token(token)
    assert decoded['sub'] == 'subject-1'
    assert decoded['role'] == 'manager'
    assert 'exp' in decoded
