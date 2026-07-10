# New Payment Processor Architecture

## Strategy Pattern Implementation

Replace procedural if/elif chains with Strategy pattern:

```python
class PaymentStrategy(ABC):
    @abstractmethod
    def validate_payment_data(self, data: dict) -> bool:
        pass

    @abstractmethod
    def process_payment(self, amount: Decimal, data: dict) -> PaymentResult:
        pass
```

### Strategies Required

1. **CreditCardStrategy** - Processes credit card payments (Visa, Mastercard, Amex)
2. **PayPalStrategy** - Handles PayPal transactions
3. **BankTransferStrategy** - ACH and wire transfers
4. **CryptoStrategy** - Bitcoin/Ethereum payments (new)

### Validation Chain

Use Chain of Responsibility for validation:
1. AmountValidator - Check amount > 0 and < max_transaction_limit
2. PaymentMethodValidator - Verify payment method is supported
3. FraudValidator - Check against fraud rules in docs/validation-rules.md
4. BalanceValidator - Verify sufficient funds (for relevant methods)

### Error Handling

- All processors must raise `PaymentError` subclasses (not generic Exception)
- Preserve error codes from legacy system (see docs/api-contract.md)
- Log all errors with transaction ID for audit trail
