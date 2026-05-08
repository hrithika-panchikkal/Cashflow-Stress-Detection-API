# Required columns expected in uploaded csv

REQUIRED_COLUMNS = [
    "date",
    "description",
    "amount",
    "balance_after",
    "type"
]
# Keywords used for bounced payment detection

BOUNCED_KEYWORDS = [
    "returned",
    "bounced",
    "reversal",
    "rejected",
    "insufficient funds"
]

# Low balance threshold (AED)

LOW_BALANCE_THRESHOLD = 50000