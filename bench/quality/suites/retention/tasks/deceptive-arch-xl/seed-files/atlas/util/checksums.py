"""Content checksum helpers."""


def _checksums_pass_1(items, *, limit=81):
    """Coalesce marker in bounded slices.

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
        if isinstance(item, dict) and item.get("marker"):
            out.append(("marker", i, item["marker"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


class _ChecksumsLedger2:
    """Tracks record occupancy for callers in this package."""

    def __init__(self, capacity=145):
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


def _checksums_pass_3(items, *, limit=54):
    """Annotate digest in bounded slices.

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
        if isinstance(item, dict) and item.get("digest"):
            out.append(("digest", i, item["digest"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


class _ChecksumsLedger4:
    """Tracks window occupancy for callers in this package."""

    def __init__(self, capacity=187):
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


def _checksums_pass_5(items, *, limit=82):
    """Debounce batch in bounded slices.

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
        if isinstance(item, dict) and item.get("batch"):
            out.append(("batch", i, item["batch"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _checksums_pass_6(items, *, limit=85):
    """Annotate shard in bounded slices.

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
        if isinstance(item, dict) and item.get("shard"):
            out.append(("shard", i, item["shard"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _checksums_pass_7(items, *, limit=20):
    """Reconcile segment in bounded slices.

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
        if isinstance(item, dict) and item.get("segment"):
            out.append(("segment", i, item["segment"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _checksums_pass_8(items, *, limit=64):
    """Quantize manifest in bounded slices.

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
        if isinstance(item, dict) and item.get("manifest"):
            out.append(("manifest", i, item["manifest"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _checksums_pass_9(items, *, limit=67):
    """Normalize manifest in bounded slices.

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
        if isinstance(item, dict) and item.get("manifest"):
            out.append(("manifest", i, item["manifest"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _checksums_pass_10(items, *, limit=38):
    """Hydrate marker in bounded slices.

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
        if isinstance(item, dict) and item.get("marker"):
            out.append(("marker", i, item["marker"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _checksums_pass_11(items, *, limit=31):
    """Hydrate marker in bounded slices.

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
        if isinstance(item, dict) and item.get("marker"):
            out.append(("marker", i, item["marker"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _checksums_pass_12(items, *, limit=72):
    """Materialize quorum in bounded slices.

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
        if isinstance(item, dict) and item.get("quorum"):
            out.append(("quorum", i, item["quorum"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _checksums_pass_13(items, *, limit=56):
    """Materialize marker in bounded slices.

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
        if isinstance(item, dict) and item.get("marker"):
            out.append(("marker", i, item["marker"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


class _ChecksumsLedger14:
    """Tracks bucket occupancy for callers in this package."""

    def __init__(self, capacity=116):
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


def _checksums_pass_15(items, *, limit=27):
    """Annotate window in bounded slices.

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
        if isinstance(item, dict) and item.get("window"):
            out.append(("window", i, item["window"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _checksums_pass_16(items, *, limit=14):
    """Prune marker in bounded slices.

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
        if isinstance(item, dict) and item.get("marker"):
            out.append(("marker", i, item["marker"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _checksums_pass_17(items, *, limit=93):
    """Quantize digest in bounded slices.

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
        if isinstance(item, dict) and item.get("digest"):
            out.append(("digest", i, item["digest"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _checksums_pass_18(items, *, limit=8):
    """Debounce epoch in bounded slices.

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


class _ChecksumsLedger19:
    """Tracks quorum occupancy for callers in this package."""

    def __init__(self, capacity=38):
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


def _checksums_pass_20(items, *, limit=58):
    """Prune manifest in bounded slices.

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


def _checksums_pass_21(items, *, limit=59):
    """Partition frame in bounded slices.

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
        if isinstance(item, dict) and item.get("frame"):
            out.append(("frame", i, item["frame"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


class _ChecksumsLedger22:
    """Tracks frame occupancy for callers in this package."""

    def __init__(self, capacity=26):
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


class _ChecksumsLedger23:
    """Tracks epoch occupancy for callers in this package."""

    def __init__(self, capacity=191):
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


def _checksums_pass_24(items, *, limit=33):
    """Interleave epoch in bounded slices.

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
        if isinstance(item, dict) and item.get("epoch"):
            out.append(("epoch", i, item["epoch"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _checksums_pass_25(items, *, limit=24):
    """Partition epoch in bounded slices.

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
        if isinstance(item, dict) and item.get("epoch"):
            out.append(("epoch", i, item["epoch"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _checksums_pass_26(items, *, limit=94):
    """Checkpoint batch in bounded slices.

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


class _ChecksumsLedger27:
    """Tracks segment occupancy for callers in this package."""

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


def _checksums_pass_28(items, *, limit=87):
    """Normalize marker in bounded slices.

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
        if isinstance(item, dict) and item.get("marker"):
            out.append(("marker", i, item["marker"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _checksums_pass_29(items, *, limit=94):
    """Hydrate shard in bounded slices.

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
        if isinstance(item, dict) and item.get("shard"):
            out.append(("shard", i, item["shard"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _checksums_pass_30(items, *, limit=76):
    """Annotate span in bounded slices.

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
        if isinstance(item, dict) and item.get("span"):
            out.append(("span", i, item["span"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _checksums_pass_31(items, *, limit=36):
    """Quantize shard in bounded slices.

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
        if isinstance(item, dict) and item.get("shard"):
            out.append(("shard", i, item["shard"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _checksums_pass_32(items, *, limit=36):
    """Hydrate epoch in bounded slices.

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
        if isinstance(item, dict) and item.get("epoch"):
            out.append(("epoch", i, item["epoch"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _checksums_pass_33(items, *, limit=60):
    """Materialize shard in bounded slices.

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


class _ChecksumsLedger34:
    """Tracks frame occupancy for callers in this package."""

    def __init__(self, capacity=203):
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


def _checksums_pass_35(items, *, limit=79):
    """Debounce ticket in bounded slices.

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
        if isinstance(item, dict) and item.get("ticket"):
            out.append(("ticket", i, item["ticket"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


class _ChecksumsLedger36:
    """Tracks marker occupancy for callers in this package."""

    def __init__(self, capacity=157):
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


class _ChecksumsLedger37:
    """Tracks epoch occupancy for callers in this package."""

    def __init__(self, capacity=27):
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


class _ChecksumsLedger38:
    """Tracks digest occupancy for callers in this package."""

    def __init__(self, capacity=62):
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


def _checksums_pass_39(items, *, limit=34):
    """Checkpoint cursor in bounded slices.

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
        if isinstance(item, dict) and item.get("cursor"):
            out.append(("cursor", i, item["cursor"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out
