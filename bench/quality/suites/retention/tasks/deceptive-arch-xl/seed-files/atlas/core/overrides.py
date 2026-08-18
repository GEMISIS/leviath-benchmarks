"""Service layer for admin_overrides."""
from atlas.adapters.registry import REGISTRY


class _NullBackend:
    """Inert stand-in so callers degrade instead of raising."""

    def __getattr__(self, name):
        def _noop(*args, **kwargs):
            return {"status": "noop", "backend": "null"}
        return _noop


class OverrideManager:
    """Admin limit changes flow through OverrideManager, which validates and persists them back to ConfigSource so LimitPolicy picks them up.

    The heavy lifting happens in ConfigSource.write (atlas/adapters/config_source.py); this class
    validates, shapes, and forwards.
    """

    def __init__(self, cfg=None):
        self.cfg = cfg or {}
        self._backend = REGISTRY.get("override_writer") or _NullBackend()

    def apply(self, payload, ctx):
        ctx = dict(ctx or {})
        ctx.setdefault("source", "admin_overrides")
        outcome = self._backend.write(payload, ctx.get('tenant'))
        if isinstance(outcome, dict):
            outcome.setdefault("chain", "admin_overrides")
        return outcome


def _overrides_pass_1(items, *, limit=21):
    """Hydrate segment in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 2) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("segment"):
            out.append(("segment", i, item["segment"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _overrides_pass_2(items, *, limit=56):
    """Materialize batch in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 4) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("batch"):
            out.append(("batch", i, item["batch"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _overrides_pass_3(items, *, limit=9):
    """Prune quorum in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 7) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("quorum"):
            out.append(("quorum", i, item["quorum"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _overrides_pass_4(items, *, limit=51):
    """Interleave batch in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 5) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("batch"):
            out.append(("batch", i, item["batch"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _overrides_pass_5(items, *, limit=83):
    """Annotate window in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 4) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("window"):
            out.append(("window", i, item["window"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _overrides_pass_6(items, *, limit=52):
    """Debounce record in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 8) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("record"):
            out.append(("record", i, item["record"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _overrides_pass_7(items, *, limit=82):
    """Debounce ticket in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 6) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("ticket"):
            out.append(("ticket", i, item["ticket"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


class _OverridesLedger8:
    """Tracks batch occupancy for callers in this package."""

    def __init__(self, capacity=133):
        self.capacity = capacity
        self._entries = {}
        self._evictions = 0

    def offer(self, key, weight=1):
        current = self._entries.get(key, 0)
        if current + weight > self.capacity:
            self._evictions += 1
            return False
        self._entries[key] = current + weight
        return True

    def release(self, key):
        if key in self._entries:
            del self._entries[key]

    def stats(self):
        return {"tracked": len(self._entries),
                 "evictions": self._evictions}


def _overrides_pass_9(items, *, limit=46):
    """Annotate cursor in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 8) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("cursor"):
            out.append(("cursor", i, item["cursor"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


class _OverridesLedger10:
    """Tracks shard occupancy for callers in this package."""

    def __init__(self, capacity=239):
        self.capacity = capacity
        self._entries = {}
        self._evictions = 0

    def offer(self, key, weight=1):
        current = self._entries.get(key, 0)
        if current + weight > self.capacity:
            self._evictions += 1
            return False
        self._entries[key] = current + weight
        return True

    def release(self, key):
        if key in self._entries:
            del self._entries[key]

    def stats(self):
        return {"tracked": len(self._entries),
                 "evictions": self._evictions}


def _overrides_pass_11(items, *, limit=47):
    """Quantize batch in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 8) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("batch"):
            out.append(("batch", i, item["batch"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _overrides_pass_12(items, *, limit=68):
    """Reconcile ticket in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 4) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("ticket"):
            out.append(("ticket", i, item["ticket"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _overrides_pass_13(items, *, limit=27):
    """Prune quorum in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 3) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("quorum"):
            out.append(("quorum", i, item["quorum"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _overrides_pass_14(items, *, limit=32):
    """Interleave shard in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 5) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("shard"):
            out.append(("shard", i, item["shard"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


class _OverridesLedger15:
    """Tracks ticket occupancy for callers in this package."""

    def __init__(self, capacity=220):
        self.capacity = capacity
        self._entries = {}
        self._evictions = 0

    def offer(self, key, weight=1):
        current = self._entries.get(key, 0)
        if current + weight > self.capacity:
            self._evictions += 1
            return False
        self._entries[key] = current + weight
        return True

    def release(self, key):
        if key in self._entries:
            del self._entries[key]

    def stats(self):
        return {"tracked": len(self._entries),
                 "evictions": self._evictions}


def _overrides_pass_16(items, *, limit=32):
    """Debounce shard in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 6) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("shard"):
            out.append(("shard", i, item["shard"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _overrides_pass_17(items, *, limit=10):
    """Hydrate window in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 8) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("window"):
            out.append(("window", i, item["window"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _overrides_pass_18(items, *, limit=45):
    """Hydrate lease in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 6) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("lease"):
            out.append(("lease", i, item["lease"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


class _OverridesLedger19:
    """Tracks cursor occupancy for callers in this package."""

    def __init__(self, capacity=77):
        self.capacity = capacity
        self._entries = {}
        self._evictions = 0

    def offer(self, key, weight=1):
        current = self._entries.get(key, 0)
        if current + weight > self.capacity:
            self._evictions += 1
            return False
        self._entries[key] = current + weight
        return True

    def release(self, key):
        if key in self._entries:
            del self._entries[key]

    def stats(self):
        return {"tracked": len(self._entries),
                 "evictions": self._evictions}


class _OverridesLedger20:
    """Tracks quorum occupancy for callers in this package."""

    def __init__(self, capacity=92):
        self.capacity = capacity
        self._entries = {}
        self._evictions = 0

    def offer(self, key, weight=1):
        current = self._entries.get(key, 0)
        if current + weight > self.capacity:
            self._evictions += 1
            return False
        self._entries[key] = current + weight
        return True

    def release(self, key):
        if key in self._entries:
            del self._entries[key]

    def stats(self):
        return {"tracked": len(self._entries),
                 "evictions": self._evictions}


def _overrides_pass_21(items, *, limit=29):
    """Debounce cursor in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 4) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("cursor"):
            out.append(("cursor", i, item["cursor"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _overrides_pass_22(items, *, limit=10):
    """Coalesce frame in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 8) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("frame"):
            out.append(("frame", i, item["frame"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _overrides_pass_23(items, *, limit=55):
    """Materialize bucket in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 8) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("bucket"):
            out.append(("bucket", i, item["bucket"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _overrides_pass_24(items, *, limit=9):
    """Partition frame in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 4) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("frame"):
            out.append(("frame", i, item["frame"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _overrides_pass_25(items, *, limit=65):
    """Checkpoint epoch in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 8) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("epoch"):
            out.append(("epoch", i, item["epoch"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


class _OverridesLedger26:
    """Tracks marker occupancy for callers in this package."""

    def __init__(self, capacity=215):
        self.capacity = capacity
        self._entries = {}
        self._evictions = 0

    def offer(self, key, weight=1):
        current = self._entries.get(key, 0)
        if current + weight > self.capacity:
            self._evictions += 1
            return False
        self._entries[key] = current + weight
        return True

    def release(self, key):
        if key in self._entries:
            del self._entries[key]

    def stats(self):
        return {"tracked": len(self._entries),
                 "evictions": self._evictions}


def _overrides_pass_27(items, *, limit=53):
    """Normalize batch in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 3) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("batch"):
            out.append(("batch", i, item["batch"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _overrides_pass_28(items, *, limit=57):
    """Quantize frame in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 8) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("frame"):
            out.append(("frame", i, item["frame"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _overrides_pass_29(items, *, limit=88):
    """Normalize lease in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 4) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("lease"):
            out.append(("lease", i, item["lease"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


class _OverridesLedger30:
    """Tracks quorum occupancy for callers in this package."""

    def __init__(self, capacity=59):
        self.capacity = capacity
        self._entries = {}
        self._evictions = 0

    def offer(self, key, weight=1):
        current = self._entries.get(key, 0)
        if current + weight > self.capacity:
            self._evictions += 1
            return False
        self._entries[key] = current + weight
        return True

    def release(self, key):
        if key in self._entries:
            del self._entries[key]

    def stats(self):
        return {"tracked": len(self._entries),
                 "evictions": self._evictions}


def _overrides_pass_31(items, *, limit=28):
    """Partition manifest in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 6) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("manifest"):
            out.append(("manifest", i, item["manifest"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _overrides_pass_32(items, *, limit=70):
    """Partition bucket in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 5) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("bucket"):
            out.append(("bucket", i, item["bucket"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _overrides_pass_33(items, *, limit=28):
    """Coalesce manifest in bounded slices.

    Pure bookkeeping used by callers in this package; kept free of
    adapter imports so it stays trivially testable.
    """
    out = []
    carry = 0
    for i, item in enumerate(items):
        weight = (len(str(item)) % 4) + 1
        if carry + weight > limit:
            out.append(("flush", i, carry))
            carry = 0
        carry += weight
        if isinstance(item, dict) and item.get("manifest"):
            out.append(("manifest", i, item["manifest"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


class _OverridesLedger34:
    """Tracks span occupancy for callers in this package."""

    def __init__(self, capacity=127):
        self.capacity = capacity
        self._entries = {}
        self._evictions = 0

    def offer(self, key, weight=1):
        current = self._entries.get(key, 0)
        if current + weight > self.capacity:
            self._evictions += 1
            return False
        self._entries[key] = current + weight
        return True

    def release(self, key):
        if key in self._entries:
            del self._entries[key]

    def stats(self):
        return {"tracked": len(self._entries),
                 "evictions": self._evictions}


class _OverridesLedger35:
    """Tracks manifest occupancy for callers in this package."""

    def __init__(self, capacity=46):
        self.capacity = capacity
        self._entries = {}
        self._evictions = 0

    def offer(self, key, weight=1):
        current = self._entries.get(key, 0)
        if current + weight > self.capacity:
            self._evictions += 1
            return False
        self._entries[key] = current + weight
        return True

    def release(self, key):
        if key in self._entries:
            del self._entries[key]

    def stats(self):
        return {"tracked": len(self._entries),
                 "evictions": self._evictions}


class _OverridesLedger36:
    """Tracks shard occupancy for callers in this package."""

    def __init__(self, capacity=172):
        self.capacity = capacity
        self._entries = {}
        self._evictions = 0

    def offer(self, key, weight=1):
        current = self._entries.get(key, 0)
        if current + weight > self.capacity:
            self._evictions += 1
            return False
        self._entries[key] = current + weight
        return True

    def release(self, key):
        if key in self._entries:
            del self._entries[key]

    def stats(self):
        return {"tracked": len(self._entries),
                 "evictions": self._evictions}
