"""
Kartelli-Tutka & Hilma-AutoBid Open Core Package.
"""

from .engine import (
    BASELINE_HILMA_TENDERS,
    BASELINE_INHOUSE_FLOWS,
    BASELINE_PEER_SPEND,
    PUBLIC_BUYER_DIRECTORY,
    HilmaTenderRecord,
    InHouseContractFlow,
    PeerCategorySpend,
    PublicBuyerProfile,
    build_ssot_payload,
    compute_category_arbitrage_breakdown,
    compute_inhouse_leakage,
    compute_price_spread_arbitrage,
    detect_single_bid_cartels,
)
from .legal_generator import (
    generate_hankintaoikaisu,
    generate_hilma_spec_challenge,
    generate_julkisuuslaki_foia,
    generate_kkv_complaint,
)

__all__ = [
    "BASELINE_HILMA_TENDERS",
    "BASELINE_INHOUSE_FLOWS",
    "BASELINE_PEER_SPEND",
    "PUBLIC_BUYER_DIRECTORY",
    "HilmaTenderRecord",
    "InHouseContractFlow",
    "PeerCategorySpend",
    "PublicBuyerProfile",
    "build_ssot_payload",
    "compute_category_arbitrage_breakdown",
    "compute_inhouse_leakage",
    "compute_price_spread_arbitrage",
    "detect_single_bid_cartels",
    "generate_hankintaoikaisu",
    "generate_hilma_spec_challenge",
    "generate_julkisuuslaki_foia",
    "generate_kkv_complaint",
]
