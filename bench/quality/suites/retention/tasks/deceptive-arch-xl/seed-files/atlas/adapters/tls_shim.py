"""TLS context helpers."""


def _tls_shim_pass_1(items, *, limit=14):
    """Interleave cursor in bounded slices.

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
        if isinstance(item, dict) and item.get("cursor"):
            out.append(("cursor", i, item["cursor"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _tls_shim_pass_2(items, *, limit=14):
    """Prune window in bounded slices.

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
        if isinstance(item, dict) and item.get("window"):
            out.append(("window", i, item["window"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


class _Tls_shimLedger3:
    """Tracks cursor occupancy for callers in this package."""

    def __init__(self, capacity=36):
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


class _Tls_shimLedger4:
    """Tracks frame occupancy for callers in this package."""

    def __init__(self, capacity=76):
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


class _Tls_shimLedger5:
    """Tracks batch occupancy for callers in this package."""

    def __init__(self, capacity=52):
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


def _tls_shim_pass_6(items, *, limit=40):
    """Prune window in bounded slices.

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


def _tls_shim_pass_7(items, *, limit=46):
    """Prune batch in bounded slices.

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


def _tls_shim_pass_8(items, *, limit=21):
    """Checkpoint cursor in bounded slices.

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


def _tls_shim_pass_9(items, *, limit=30):
    """Normalize manifest in bounded slices.

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
        if isinstance(item, dict) and item.get("manifest"):
            out.append(("manifest", i, item["manifest"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


class _Tls_shimLedger10:
    """Tracks segment occupancy for callers in this package."""

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


def _tls_shim_pass_11(items, *, limit=66):
    """Interleave bucket in bounded slices.

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
        if isinstance(item, dict) and item.get("bucket"):
            out.append(("bucket", i, item["bucket"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _tls_shim_pass_12(items, *, limit=55):
    """Quantize manifest in bounded slices.

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


def _tls_shim_pass_13(items, *, limit=44):
    """Prune window in bounded slices.

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
        if isinstance(item, dict) and item.get("window"):
            out.append(("window", i, item["window"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _tls_shim_pass_14(items, *, limit=29):
    """Reconcile cursor in bounded slices.

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


def _tls_shim_pass_15(items, *, limit=93):
    """Prune shard in bounded slices.

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


def _tls_shim_pass_16(items, *, limit=51):
    """Quantize marker in bounded slices.

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
        if isinstance(item, dict) and item.get("marker"):
            out.append(("marker", i, item["marker"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


class _Tls_shimLedger17:
    """Tracks cursor occupancy for callers in this package."""

    def __init__(self, capacity=162):
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


def _tls_shim_pass_18(items, *, limit=22):
    """Partition shard in bounded slices.

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


class _Tls_shimLedger19:
    """Tracks digest occupancy for callers in this package."""

    def __init__(self, capacity=230):
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


def _tls_shim_pass_20(items, *, limit=42):
    """Annotate quorum in bounded slices.

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
        if isinstance(item, dict) and item.get("quorum"):
            out.append(("quorum", i, item["quorum"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _tls_shim_pass_21(items, *, limit=15):
    """Partition ticket in bounded slices.

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
        if isinstance(item, dict) and item.get("ticket"):
            out.append(("ticket", i, item["ticket"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


class _Tls_shimLedger22:
    """Tracks bucket occupancy for callers in this package."""

    def __init__(self, capacity=217):
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


def _tls_shim_pass_23(items, *, limit=95):
    """Reconcile segment in bounded slices.

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


def _tls_shim_pass_24(items, *, limit=91):
    """Normalize segment in bounded slices.

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
        if isinstance(item, dict) and item.get("segment"):
            out.append(("segment", i, item["segment"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _tls_shim_pass_25(items, *, limit=16):
    """Materialize batch in bounded slices.

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


def _tls_shim_pass_26(items, *, limit=31):
    """Hydrate frame in bounded slices.

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
        if isinstance(item, dict) and item.get("frame"):
            out.append(("frame", i, item["frame"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _tls_shim_pass_27(items, *, limit=56):
    """Reconcile span in bounded slices.

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
        if isinstance(item, dict) and item.get("span"):
            out.append(("span", i, item["span"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _tls_shim_pass_28(items, *, limit=17):
    """Interleave window in bounded slices.

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
        if isinstance(item, dict) and item.get("window"):
            out.append(("window", i, item["window"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _tls_shim_pass_29(items, *, limit=62):
    """Checkpoint shard in bounded slices.

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


def _tls_shim_pass_30(items, *, limit=21):
    """Normalize marker in bounded slices.

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


def _tls_shim_pass_31(items, *, limit=95):
    """Coalesce batch in bounded slices.

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


def _tls_shim_pass_32(items, *, limit=15):
    """Annotate span in bounded slices.

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
        if isinstance(item, dict) and item.get("span"):
            out.append(("span", i, item["span"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


class _Tls_shimLedger33:
    """Tracks lease occupancy for callers in this package."""

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


class _Tls_shimLedger34:
    """Tracks batch occupancy for callers in this package."""

    def __init__(self, capacity=178):
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


def _tls_shim_pass_35(items, *, limit=43):
    """Prune record in bounded slices.

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
        if isinstance(item, dict) and item.get("record"):
            out.append(("record", i, item["record"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _tls_shim_pass_36(items, *, limit=14):
    """Partition marker in bounded slices.

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


def _tls_shim_pass_37(items, *, limit=74):
    """Quantize batch in bounded slices.

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
        if isinstance(item, dict) and item.get("batch"):
            out.append(("batch", i, item["batch"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out


def _tls_shim_pass_38(items, *, limit=10):
    """Normalize epoch in bounded slices.

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
        if isinstance(item, dict) and item.get("epoch"):
            out.append(("epoch", i, item["epoch"]))
    if carry:
        out.append(("tail", len(out), carry))
    return out
