"""
CLI for TokenManager using argparse.
"""

import argparse
import sys
from token_manager import TokenManager


def main():
    parser = argparse.ArgumentParser(
        description='Token Manager CLI - Manage authentication tokens with expiration'
    )
    parser.add_argument(
        '--ttl',
        type=int,
        required=True,
        help='Time-to-live in seconds for tokens'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate a new token')
    generate_parser.add_argument('token_id', type=str, help='Token identifier')
    generate_parser.add_argument('current_time', type=int, help='Current time in seconds')
    
    # Renew command
    renew_parser = subparsers.add_parser('renew', help='Renew an unexpired token')
    renew_parser.add_argument('token_id', type=str, help='Token identifier')
    renew_parser.add_argument('current_time', type=int, help='Current time in seconds')
    
    # Count command
    count_parser = subparsers.add_parser('count', help='Count unexpired tokens')
    count_parser.add_argument('current_time', type=int, help='Current time in seconds')
    
    # Show command
    subparsers.add_parser('show', help='Show all tokens and their expiry times')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    token_manager = TokenManager(args.ttl)
    
    if args.command == 'generate':
        token_manager.generate(args.token_id, args.current_time)
        expiry_time = args.current_time + args.ttl
        print(f"Token '{args.token_id}' generated. Expires at time {expiry_time}")
    
    elif args.command == 'renew':
        if args.token_id not in token_manager.tokens:
            print(f"Token '{args.token_id}' does not exist")
            sys.exit(1)
        
        old_expiry = token_manager.tokens[args.token_id]
        token_manager.renew(args.token_id, args.current_time)
        new_expiry = token_manager.tokens[args.token_id]
        
        if new_expiry == old_expiry:
            print(f"Token '{args.token_id}' is expired or already expired")
            sys.exit(1)
        else:
            print(f"Token '{args.token_id}' renewed. New expiry time: {new_expiry}")
    
    elif args.command == 'count':
        count = token_manager.countUnexpiredTokens(args.current_time)
        print(count)
    
    elif args.command == 'show':
        if not token_manager.tokens:
            print("No tokens exist")
        else:
            for token_id, expiry_time in sorted(token_manager.tokens.items()):
                print(f"{token_id}: {expiry_time}")


if __name__ == '__main__':
    main()

