# Changelog

## 0.2.1 — 2026-05-21

- Fix: clarify `verify_business` and `search_entities` tool descriptions so LLM agents route verification intent ("verify a company in Delaware") to `verify_business` instead of `search_entities`, and ask for a missing entity name rather than falling back to search. No interface change.

## 0.2.0 — 2026-04-18

BREAKING: tool enum values renamed pre_check→quick, full→deep. Default level changed from full to quick.
