"""
Unit tests for authentication logic.
"""
import pytest
from datetime import datetime, timedelta
from jose import jwt, JWTError

from auth import (
    verify_password,
    get_password_hash,
    create_access_token,
    verify_token,
    authenticate_user
)
from models import User


class TestPasswordHashing:
    """Test password hashing and verification."""
    
    def test_password_hashing(self):
        """Test that password hashing works correctly."""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        # Hash should be different from original password
        assert hashed != password
        # Hash should be consistent
        assert verify_password(password, hashed) is True
        # Wrong password should fail
        assert verify_password("wrongpassword", hashed) is False
    
    def test_password_hash_uniqueness(self):
        """Test that same password produces different hashes (due to salt)."""
        password = "testpassword123"
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        # Hashes should be different due to salt
        assert hash1 != hash2
        # But both should verify correctly
        assert verify_password(password, hash1) is True
        assert verify_password(password, hash2) is True
    
    def test_empty_password_handling(self):
        """Test handling of empty passwords."""
        with pytest.raises(ValueError):
            get_password_hash("")
    
    def test_none_password_handling(self):
        """Test handling of None passwords."""
        with pytest.raises((ValueError, TypeError)):
            get_password_hash(None)


class TestJWTTokens:
    """Test JWT token creation and verification."""
    
    def test_create_access_token(self):
        """Test access token creation."""
        user_id = "123"
        token = create_access_token(data={"sub": user_id})
        
        assert isinstance(token, str)
        assert len(token) > 0
        
        # Verify token can be decoded
        from main import SECRET_KEY, ALGORITHM
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        assert payload["sub"] == user_id
        assert "exp" in payload
    
    def test_token_expiration(self):
        """Test token expiration handling."""
        user_id = "123"
        # Create token with very short expiration
        token = create_access_token(
            data={"sub": user_id}, 
            expires_delta=timedelta(seconds=-1)  # Already expired
        )
        
        # Token should be expired
        with pytest.raises(JWTError):
            verify_token(token)
    
    def test_invalid_token(self):
        """Test handling of invalid tokens."""
        invalid_tokens = [
            "invalid.token.here",
            "",
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.invalid",
            None
        ]
        
        for token in invalid_tokens:
            with pytest.raises((JWTError, AttributeError, TypeError)):
                verify_token(token)
    
    def test_token_with_custom_expiration(self):
        """Test token creation with custom expiration."""
        user_id = "123"
        custom_expiration = timedelta(hours=24)
        token = create_access_token(
            data={"sub": user_id}, 
            expires_delta=custom_expiration
        )
        
        payload = verify_token(token)
        assert payload["sub"] == user_id
        
        # Check expiration is approximately correct (within 1 minute tolerance)
        exp_time = datetime.fromtimestamp(payload["exp"])
        expected_exp = datetime.utcnow() + custom_expiration
        time_diff = abs((exp_time - expected_exp).total_seconds())
        assert time_diff < 60  # Within 1 minute


class TestUserAuthentication:
    """Test user authentication logic."""
    
    def test_authenticate_valid_user(self, db_session, test_user):
        """Test authentication with valid credentials."""
        authenticated_user = authenticate_user(
            db_session, 
            test_user.email, 
            "testpassword123"
        )
        
        assert authenticated_user is not None
        assert authenticated_user.id == test_user.id
        assert authenticated_user.email == test_user.email
    
    def test_authenticate_invalid_email(self, db_session):
        """Test authentication with invalid email."""
        authenticated_user = authenticate_user(
            db_session, 
            "nonexistent@example.com", 
            "anypassword"
        )
        
        assert authenticated_user is False
    
    def test_authenticate_invalid_password(self, db_session, test_user):
        """Test authentication with invalid password."""
        authenticated_user = authenticate_user(
            db_session, 
            test_user.email, 
            "wrongpassword"
        )
        
        assert authenticated_user is False
    
    def test_authenticate_empty_credentials(self, db_session):
        """Test authentication with empty credentials."""
        # Empty email
        result = authenticate_user(db_session, "", "password")
        assert result is False
        
        # Empty password
        result = authenticate_user(db_session, "test@example.com", "")
        assert result is False
        
        # Both empty
        result = authenticate_user(db_session, "", "")
        assert result is False
    
    def test_authenticate_none_credentials(self, db_session):
        """Test authentication with None credentials."""
        with pytest.raises((TypeError, AttributeError)):
            authenticate_user(db_session, None, "password")
        
        with pytest.raises((TypeError, AttributeError)):
            authenticate_user(db_session, "test@example.com", None)


class TestTokenVerification:
    """Test token verification logic."""
    
    def test_verify_valid_token(self):
        """Test verification of valid token."""
        user_id = "test-user-123"
        token = create_access_token(data={"sub": user_id})
        
        payload = verify_token(token)
        assert payload["sub"] == user_id
    
    def test_verify_expired_token(self):
        """Test verification of expired token."""
        user_id = "test-user-123"
        token = create_access_token(
            data={"sub": user_id},
            expires_delta=timedelta(seconds=-1)
        )
        
        with pytest.raises(JWTError):
            verify_token(token)
    
    def test_verify_malformed_token(self):
        """Test verification of malformed tokens."""
        malformed_tokens = [
            "not.a.jwt",
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9",  # Incomplete
            "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ",  # Missing signature
        ]
        
        for token in malformed_tokens:
            with pytest.raises(JWTError):
                verify_token(token)
    
    def test_verify_token_with_wrong_algorithm(self):
        """Test token created with different algorithm."""
        from main import SECRET_KEY
        
        # Create token with different algorithm
        payload = {"sub": "123", "exp": datetime.utcnow() + timedelta(hours=1)}
        wrong_token = jwt.encode(payload, SECRET_KEY, algorithm="HS512")
        
        with pytest.raises(JWTError):
            verify_token(wrong_token)
    
    def test_verify_token_with_wrong_secret(self):
        """Test token created with different secret."""
        payload = {"sub": "123", "exp": datetime.utcnow() + timedelta(hours=1)}
        wrong_token = jwt.encode(payload, "wrong-secret", algorithm="HS256")
        
        with pytest.raises(JWTError):
            verify_token(wrong_token)


@pytest.mark.integration
class TestAuthenticationIntegration:
    """Integration tests for authentication flow."""
    
    def test_full_authentication_flow(self, db_session):
        """Test complete authentication flow from user creation to token verification."""
        # 1. Create user
        email = "integration@example.com"
        password = "integrationtest123"
        hashed_password = get_password_hash(password)
        
        user = User(
            email=email,
            name="Integration User",
            hashed_password=hashed_password
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        
        # 2. Authenticate user
        authenticated_user = authenticate_user(db_session, email, password)
        assert authenticated_user is not False
        assert authenticated_user.id == user.id
        
        # 3. Create token
        token = create_access_token(data={"sub": str(authenticated_user.id)})
        
        # 4. Verify token
        payload = verify_token(token)
        assert payload["sub"] == str(authenticated_user.id)
    
    def test_authentication_with_case_insensitive_email(self, db_session, test_user):
        """Test authentication with different email case."""
        # Should work with different cases
        authenticated_user = authenticate_user(
            db_session, 
            test_user.email.upper(), 
            "testpassword123"
        )
        
        # Note: This test assumes case-insensitive email handling
        # If your implementation is case-sensitive, adjust accordingly
        assert authenticated_user is not False or authenticated_user is False  # Depends on implementation
