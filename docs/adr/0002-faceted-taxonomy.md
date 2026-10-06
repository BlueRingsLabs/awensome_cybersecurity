# 2. A faceted taxonomy grounded in CyBOK and NICE

- Status: accepted
- Date: 2026-10-04

## Context

v1 had two ad-hoc axes: a "domain" (literature/papers/web) that mixed *resource
type* with *depth*, and five "subdomains" (`blue_team`, `red_team`, ...) that
forced one offensive/defensive label onto inherently cross-cutting material. A
guide to Active Directory attacks is both red and blue; a format ("paper") is not
a topic.

## Decision

Separate the axes. One **category** is the primary topic and decides the folder;
**format**, **language** and **tags** are orthogonal facets stored in front
matter. Categories are grounded in two public bodies of knowledge — CyBOK v1.1
Knowledge Areas and the NICE Workforce Framework — so the library maps onto how
industry and academia already reason, and each category records its CyBOK/NICE
codes. The taxonomy is defined once in `schema/taxonomy.yaml` and every component
reads it from there.

## Consequences

- Classification is a topic decision, not a false offensive/defensive binary.
- Format and depth are queryable independently of topic.
- Adding a category/format/tag is a one-file change that propagates everywhere.
- A migration from the old tree was required (see the migration audit).
