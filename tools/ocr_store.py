from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any, Dict, List

from smolagents import tool

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "ocr_cache.db"


def _get_conn() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS ocr_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT NOT NULL,
            source_type TEXT NOT NULL,
            doc_ref TEXT,
            text_ocr TEXT,
            text_advanced TEXT,
            meta_json TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_ocr_records_ticker_source ON ocr_records(ticker, source_type)"
    )
    conn.execute(
        "CREATE INDEX IF NOT EXISTS idx_ocr_records_created_at ON ocr_records(created_at)"
    )
    return conn


def persist_ocr_records(
    ticker: str,
    source_type: str,
    records: List[Dict[str, Any]],
    doc_ref_prefix: str | None = None,
) -> int:
    if not records:
        return 0
    conn = _get_conn()
    inserted = 0
    with conn:
        for idx, record in enumerate(records):
            meta = {
                "keys": list(record.keys()),
            }
            doc_ref = f"{doc_ref_prefix}_{idx}" if doc_ref_prefix else str(idx)
            conn.execute(
                """
                INSERT INTO ocr_records(ticker, source_type, doc_ref, text_ocr, text_advanced, meta_json)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    ticker,
                    source_type,
                    doc_ref,
                    record.get("text_ocr", ""),
                    record.get("text_advanced", ""),
                    json.dumps(meta),
                ),
            )
            inserted += 1
    conn.close()
    return inserted


def _row_to_record(row: sqlite3.Row, include_full_text: bool = False) -> Dict[str, Any]:
    text_ocr = row["text_ocr"] or ""
    text_advanced = row["text_advanced"] or ""
    snippet = (text_advanced or text_ocr)[:900]
    out = {
        "id": row["id"],
        "ticker": row["ticker"],
        "source_type": row["source_type"],
        "doc_ref": row["doc_ref"],
        "snippet": snippet,
        "created_at": row["created_at"],
    }
    if include_full_text:
        out["text_ocr"] = text_ocr
        out["text_advanced"] = text_advanced
    return out


@tool
def get_ocr_aggregate(ticker: str, source_type: str = "all") -> Dict[str, Any]:
    """
    Returns aggregate OCR stats for a ticker.

    Args:
        ticker (str): Stock ticker symbol (for example, ``MTNN``).
        source_type (str): OCR source to filter by. Use ``all`` for every source,
            or a specific source like ``financial_statements``,
            ``director_disclosures``, or ``corporate_disclosures``.

    Returns:
        Dict[str, Any]: Aggregate metadata including total record count and
        first/last seen timestamps.
    """
    conn = _get_conn()
    conn.row_factory = sqlite3.Row
    params: list[Any] = [ticker]
    where = "ticker = ?"
    if source_type != "all":
        where += " AND source_type = ?"
        params.append(source_type)
    row = conn.execute(
        f"""
        SELECT
            COUNT(*) AS total_records,
            MIN(created_at) AS first_seen,
            MAX(created_at) AS last_seen
        FROM ocr_records
        WHERE {where}
        """,
        params,
    ).fetchone()
    conn.close()
    return {
        "ticker": ticker,
        "source_type": source_type,
        "total_records": int(row["total_records"] or 0),
        "first_seen": row["first_seen"],
        "last_seen": row["last_seen"],
    }


@tool
def get_ocr_records(ticker: str, source_type: str = "all", limit: int = 40, offset: int = 0) -> List[Dict[str, Any]]:
    """
    Returns paginated OCR evidence snippets for a ticker.

    Args:
        ticker (str): Stock ticker symbol to query.
        source_type (str): OCR source filter. Use ``all`` for every source.
        limit (int): Maximum number of records to return (capped internally).
        offset (int): Number of records to skip for pagination.

    Returns:
        List[Dict[str, Any]]: Lightweight evidence records containing ids and snippets.
    """
    safe_limit = max(1, min(limit, 200))
    safe_offset = max(0, offset)
    conn = _get_conn()
    conn.row_factory = sqlite3.Row
    params: list[Any] = [ticker]
    where = "ticker = ?"
    if source_type != "all":
        where += " AND source_type = ?"
        params.append(source_type)
    params.extend([safe_limit, safe_offset])
    rows = conn.execute(
        f"""
        SELECT id, ticker, source_type, doc_ref, text_ocr, text_advanced, created_at
        FROM ocr_records
        WHERE {where}
        ORDER BY id DESC
        LIMIT ? OFFSET ?
        """,
        params,
    ).fetchall()
    conn.close()
    return [_row_to_record(r, include_full_text=False) for r in rows]


@tool
def get_ocr_record_text(record_id: int) -> Dict[str, Any]:
    """
    Fetch full OCR text for one stored record id.

    Args:
        record_id (int): Primary key id of the OCR record in the cache.

    Returns:
        Dict[str, Any]: Full stored OCR payload for the record, or an error dict
        if the id does not exist.
    """
    conn = _get_conn()
    conn.row_factory = sqlite3.Row
    row = conn.execute(
        """
        SELECT id, ticker, source_type, doc_ref, text_ocr, text_advanced, created_at
        FROM ocr_records
        WHERE id = ?
        """,
        (record_id,),
    ).fetchone()
    conn.close()
    if not row:
        return {"error": f"record_id {record_id} not found"}
    return _row_to_record(row, include_full_text=True)

