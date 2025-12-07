"""Batch processing utilities for Solid Engine."""

from __future__ import annotations

from typing import Iterable, Iterator

from .models import ReadingBatch


def process_batches_in_chunks(
    batches: Iterable[ReadingBatch], chunk_size: int = 10
) -> Iterator[list[ReadingBatch]]:
    """Process batches in chunks of specified size."""
    batch_list = list(batches)
    for i in range(0, len(batch_list), chunk_size):
        yield batch_list[i : i + chunk_size]


def merge_batches(batches: Iterable[ReadingBatch], source_name: str = "merged") -> ReadingBatch:
    """Merge multiple batches into a single batch."""
    all_readings = []
    for batch in batches:
        all_readings.extend(batch.readings)
    return ReadingBatch(source=source_name, readings=all_readings)

