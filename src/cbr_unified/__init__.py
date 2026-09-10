"""Lossless, provenance-aware Bank of Russia statistics unification."""

from .build import BuildResult, build_database
from .query import QueryError, UnifiedDatabase
from .registry import SOURCES, SourceSpec, get_source

__all__ = [
    "BuildResult",
    "QueryError",
    "SOURCES",
    "SourceSpec",
    "UnifiedDatabase",
    "build_database",
    "get_source",
]

__version__ = "0.1.0"
