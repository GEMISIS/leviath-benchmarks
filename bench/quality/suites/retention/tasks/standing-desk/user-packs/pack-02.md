Request 3 of 12 - keynote lineup

Select the keynote lineup from `reference/speakers.csv`. A speaker is
eligible if their available_days field lists at least one event day.
Rank eligible speakers by rating, highest first; break rating ties by
name A-Z. Walk that ranking in order, taking a speaker whenever their
fee still fits inside speaker_budget (`reference/budget.md`) given
what you have already committed; skip any who do not fit; stop once
you have five.

Write exactly these lines to `answers/phase-03.md` (names in the rank
order you took them, separated by semicolons):

```
keynotes: <name; name; name; name; name>
keynote_fees: <$X.XX total>
```

Then ask the desk for your next assignment.
