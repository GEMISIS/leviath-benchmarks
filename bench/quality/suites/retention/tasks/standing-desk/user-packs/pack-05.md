Request 6 of 12 - hotel blocks

Reserve hotel blocks from `reference/hotels.md` to cover 60% of the
request-1 attendance (rounded up) in rooms, one attendee per room.
Take hotels nearest-first by distance_m (ties by code A-Z), taking
from each the smaller of its rooms_available and the rooms still
needed, until the target is met.

blended_rate = the room-weighted average nightly rate over the rooms
you took, rounded DOWN to the cent.

Write exactly these lines to `answers/phase-06.md` (pairs sorted by
hotel code):

```
hotels: <CODE=rooms,CODE=rooms,...>
blended_rate: <$X.XX>
```

Then ask the desk for your next assignment.
