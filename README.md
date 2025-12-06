# Token Manager

A simple token management system that handles authentication tokens with expiration times.

## Overview

The `TokenManager` class manages authentication tokens with configurable time-to-live (TTL). Each token expires a specified number of seconds after it was generated or renewed.

## Features

- **Generate**: Create new tokens with unique identifiers
- **Renew**: Extend the lifetime of existing unexpired tokens
- **Count**: Count the number of unexpired tokens at a given time

### Usage

The Token Manager CLI allows you to create, renew, count, and display tokens with an expiration time (TTL).  
All commands require the `--ttl` flag, which defines the time-to-live in seconds.

#### Command Syntax

```bash
python cli.py --ttl <seconds> <command> [arguments...]
```

#### Generate a Token

Creates a new token and sets its expiry based on the TTL.

```bash
python cli.py --ttl <ttl_seconds> generate <token_id> <current_time>
```

Example:

```bash
python cli.py --ttl 10 generate user123 100
```

Output:

```
Token 'user123' generated. Expires at time 110
```

#### Renew a Token

Renews an existing token that has not expired.

```bash
python cli.py --ttl <ttl_seconds> renew <token_id> <current_time>
```

Example:

```bash
python cli.py --ttl 10 renew user123 105
```

Output:

```
Token 'user123' renewed. New expiry time: 115
```

#### Count Unexpired Tokens

Returns the number of tokens that are still valid at the given time.

```bash
python cli.py --ttl <ttl_seconds> count <current_time>
```

Example:

```bash
python cli.py --ttl 10 count 120
```

Output:

```
1
```

#### Show All Tokens

Displays all existing tokens along with their expiration timestamps.

```bash
python cli.py --ttl <ttl_seconds> show
```

Example Output:

```
user123: 115
session42: 200
```

## API Reference

### `TokenManager(timeToLive: int)`

Initialize a TokenManager with the specified time-to-live.

**Parameters:**
- `timeToLive` (int): Time in seconds before tokens expire

### `generate(tokenId: str, currentTime: int) -> None`

Generate a new token with the given tokenId at the given currentTime.

**Parameters:**
- `tokenId` (str): Unique identifier for the token
- `currentTime` (int): Current time in seconds

### `renew(tokenId: str, currentTime: int) -> None`

Renew an unexpired token. If the token is expired or doesn't exist, nothing happens.

**Note:** If a token expires at time `t`, expiration happens before renew at time `t`. So renew at time `t` will fail if `expiryTime == t`.

**Parameters:**
- `tokenId` (str): Token identifier to renew
- `currentTime` (int): Current time in seconds

### `countUnexpiredTokens(currentTime: int) -> int`

Count the number of unexpired tokens at the given currentTime.

**Note:** If a token expires at time `t`, expiration happens before count at time `t`. So tokens with `expiryTime == currentTime` are considered expired.

**Parameters:**
- `currentTime` (int): Current time in seconds

**Returns:**
- `int`: Number of unexpired tokens


## Issues to Fix

The following issues have been identified and should be addressed in future improvements:

1. **No thread safety**: The code is not thread-safe. Concurrent access from multiple threads could lead to race conditions and data corruption. Consider adding locks or using thread-safe data structures.

2. **No input validation**: 
   - No validation that `timeToLive` is positive
   - No validation that `currentTime` is non-negative
   - No validation that `tokenId` is not empty or None
   - No type checking at runtime (type hints are not enforced)

3. **No error handling**: Methods don't handle edge cases or raise appropriate exceptions for invalid inputs. Consider adding validation and meaningful error messages.

4. **Inefficient counting**: The `countUnexpiredTokens` method iterates through all tokens (including expired ones) every time it's called. This is inefficient for large numbers of tokens, using a more efficient data structure.

5. **No token expiration mechanism**: There's no way to manually or automatically clean up expired tokens. The token manager should have a min-heap[(token_expiry, token)] and a method to remove expired tokens, and this new method can be invoked everytime a token is generated, renewed and unexpired tokens are counted.

6. **No logging or monitoring**: There's no logging capability for debugging, auditing, or monitoring token operations. Consider adding logging for important operations.

7. **No way to check token existence**: There's no method to check if a token exists or to get token information (like expiry time) without modifying it.

8. **No way to delete tokens**: There's no method to explicitly delete/revoke tokens before they expire.

9. **No way to expire tokens**: There's no method to explicitly expire the tokens at a given time.

10. **Potential integer overflow**: For very large `currentTime` values, adding `timeToLive` could theoretically cause integer overflow (though unlikely in practice with Python's arbitrary precision integers).

## Unit Tests to Add

The following unit tests should be implemented to ensure code quality and catch the issues listed above:

### Basic Functionality Tests
- **Generate token**: Verify that `generate()` creates a token with correct expiry time
- **Renew unexpired token**: Verify that `renew()` extends expiry time correctly
- **Renew expired token**: Verify that `renew()` does nothing for expired tokens
- **Renew non-existent token**: Verify that `renew()` does nothing for tokens that don't exist
- **Count unexpired tokens**: Verify that `countUnexpiredTokens()` returns correct count
- **Generate multiple tokens**: Verify that multiple tokens can be generated independently
- **Overwrite existing token**: Verify that generating a token with existing ID overwrites it

### Expiration Logic Tests
- **Token expires exactly at expiry time**: Verify that tokens with `expiryTime == currentTime` are considered expired
- **Token expires before current time**: Verify that tokens with `expiryTime < currentTime` are considered expired
- **Token unexpired before expiry time**: Verify that tokens with `expiryTime > currentTime` are considered unexpired
- **Renew at exact expiry time**: Verify that renewing at exact expiry time fails (token already expired)
- **Count at exact expiry time**: Verify that tokens expiring at current time are not counted

### Boundary Condition Tests
- **Zero timeToLive**: Test behavior with `timeToLive = 0` (tokens expire immediately)
- **Very large timeToLive**: Test with very large TTL values
- **Negative currentTime**: Test behavior with negative time values
- **Zero currentTime**: Test with `currentTime = 0`
- **Very large currentTime**: Test with very large time values
- **Time going backwards**: Test scenario where `currentTime` decreases between calls

### Input Validation Tests
- **Empty tokenId**: Test with empty string `""`
- **None tokenId**: Test with `None` as tokenId
- **Invalid tokenId types**: Test with non-string types (int, list, etc.)
- **Negative timeToLive**: Test initialization with negative `timeToLive`
- **Zero timeToLive**: Test initialization with `timeToLive = 0`
- **Invalid currentTime types**: Test with non-integer types (string, float, etc.)
- **Negative currentTime**: Test with negative `currentTime` values

### Memory and Cleanup Tests
- **Expired tokens accumulation**: Verify that expired tokens remain in dictionary after expiration
- **Memory growth**: Test that memory usage grows with number of expired tokens
- **Large number of expired tokens**: Test behavior with thousands of expired tokens
- **Mixed expired and unexpired**: Test counting when many expired tokens exist

### Edge Case Scenarios
- **Generate same tokenId multiple times**: Verify that generating overwrites previous token
- **Renew immediately after generation**: Test renewing a token right after it's generated
- **Renew multiple times**: Test renewing the same token multiple times
- **Count with no tokens**: Test counting when no tokens exist
- **Count with all expired tokens**: Test counting when all tokens are expired
- **Count with all unexpired tokens**: Test counting when all tokens are unexpired

### Integration and Workflow Tests
- **Complete token lifecycle**: Test generate → renew → expire → count workflow
- **Multiple tokens with different expiry times**: Test managing multiple tokens simultaneously
- **Token expiration during operations**: Test behavior when tokens expire between operations
- **Example from problem statement**: Test the exact example scenario from the code comments

### Performance Tests
- **Count performance with many tokens**: Test `countUnexpiredTokens()` performance with large number of tokens
- **Generate performance**: Test `generate()` performance with many tokens
- **Renew performance**: Test `renew()` performance with many tokens

### Error Handling Tests
- **Invalid input handling**: Verify that invalid inputs don't crash the system
- **Type error handling**: Test that type errors are handled gracefully (or raise appropriate exceptions)
- **Exception propagation**: Verify that any exceptions are properly raised/handled

### Thread Safety Tests (Future)
- **Concurrent generate operations**: Test multiple threads generating tokens simultaneously
- **Concurrent renew operations**: Test multiple threads renewing tokens simultaneously
- **Concurrent count operations**: Test multiple threads counting tokens simultaneously
- **Race conditions**: Test for race conditions in concurrent access scenarios

## Requirements

- Python 3.7+

## License

This is a demonstration project for educational purposes.
