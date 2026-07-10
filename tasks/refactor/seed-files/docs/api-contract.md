# API Contract (MUST NOT CHANGE)

## External Interface

```python
def process_payment(payment_method: str, amount: float, payment_data: dict) -> dict:
    """
    Process a payment transaction.

    Args:
        payment_method: One of 'credit_card', 'paypal', 'bank_transfer'
        amount: Payment amount in USD
        payment_data: Method-specific payment details

    Returns:
        {
            'success': bool,
            'transaction_id': str,
            'error_code': str | None,  # EC001, EC002, etc.
            'message': str
        }
    """
```

## Error Codes (PRESERVE THESE EXACTLY)

- `EC001` - Invalid payment method
- `EC002` - Invalid amount
- `EC003` - Validation failed
- `EC004` - Processing error
- `EC005` - Database error

These codes are used by external systems and MUST NOT change.
