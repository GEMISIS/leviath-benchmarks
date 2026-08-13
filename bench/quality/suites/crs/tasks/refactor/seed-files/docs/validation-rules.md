# Payment Validation Rules

## Amount Validation
- Minimum transaction: $0.01
- Maximum transaction: $50,000.00 (credit card), $250,000.00 (bank transfer)
- Must be positive decimal with max 2 decimal places

## Credit Card Validation
- Card number: 13-19 digits, pass Luhn algorithm
- CVV: 3-4 digits
- Expiry: must be future date, format MM/YY
- Billing zip: 5 or 9 digits (US only for v1)

## PayPal Validation
- Email: valid email format
- Transaction ID: 17-character alphanumeric

## Bank Transfer Validation
- Routing number: 9 digits, valid ABA format
- Account number: 4-17 digits
- Account type: checking or savings

## Fraud Detection Rules
1. Velocity check: Max 5 transactions per card per hour
2. Amount spike: Flag if transaction >3x user's 30-day average
3. Geo check: Flag if country != card country (for now, just log warning)
4. Blacklist: Check card number against `data/blacklist.txt`

**IMPORTANT**: Fraud checks should NOT block transactions in v1, only log warnings.
