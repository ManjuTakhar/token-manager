"""
Token Manager

Manages authentication tokens with expiration times.
Each token expires timeToLive seconds after it was generated or renewed.
"""


class TokenManager:
    """
    Manages authentication tokens with expiration.
    
    Methods:
        - generate(tokenId, currentTime): Generate a new token
        - renew(tokenId, currentTime): Renew an unexpired token
        - countUnexpiredTokens(currentTime): Count unexpired tokens
    """
    
    def __init__(self, timeToLive: int):
        """
        Initialize TokenManager with time-to-live.
        
        Args:
            timeToLive: Time in seconds before tokens expire
        """
        self.timeToLive = timeToLive
        self.tokens = {}  # tokenId -> expiryTime
    
    def generate(self, tokenId: str, currentTime: int) -> None:
        """
        Generate a new token with the given tokenId at the given currentTime.
        
        Args:
            tokenId: Unique identifier for the token
            currentTime: Current time in seconds
        """
        expiryTime = currentTime + self.timeToLive
        self.tokens[tokenId] = expiryTime
    
    def renew(self, tokenId: str, currentTime: int) -> None:
        """
        Renew an unexpired token. If token is expired or doesn't exist, do nothing.
        
        Note: If a token expires at time t, expiration happens before renew at time t.
        So renew at time t will fail if expiryTime == t.
        
        Args:
            tokenId: Token identifier to renew
            currentTime: Current time in seconds
        """
        # Check if token exists
        if tokenId not in self.tokens:
            return
        
        # Check if token is expired (expiration happens before renew)
        # If expiryTime <= currentTime, token is already expired
        if self.tokens[tokenId] <= currentTime:
            return
        
        # Renew the token - extend expiry time
        self.tokens[tokenId] = currentTime + self.timeToLive
    
    def countUnexpiredTokens(self, currentTime: int) -> int:
        """
        Count the number of unexpired tokens at the given currentTime.
        
        Note: If a token expires at time t, expiration happens before count at time t.
        So tokens with expiryTime == currentTime are considered expired.
        
        Args:
            currentTime: Current time in seconds
            
        Returns:
            Number of unexpired tokens
        """
        count = 0
        for expiryTime in self.tokens.values():
            # Token is unexpired if expiryTime > currentTime
            if expiryTime > currentTime:
                count += 1
        return count
