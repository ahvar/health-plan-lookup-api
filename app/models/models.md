## ORM Design Overview

The ORM models mirror the CSV sources in `data/` and are organized around a small set of
lookup tables for geography plus plan-specific tables.

### Core Geography
- **State** (`states`): keyed by `abbreviation`, with a unique `name`. A state owns
  counties, rate areas, zip codes, and plans.
- **County** (`counties`): identified by a surrogate `id`, with `code` and `name`
  unique within a state. Each county belongs to one state and owns many zip codes.

### Plans + Rating Context
- **RateArea** (`rate_areas`): unique per `(state_abbreviation, area_number)`. A rate
  area belongs to one state and is referenced by both plans and zip codes.
- **MetalLevel** (`metal_levels`): normalized lookup table for plan metal tiers, unique
  per `name`.
- **Plan** (`plans`): uniquely identified by `plan_id`, with `rate`, and references to
  `state`, `rate_area`, and `metal_level`.

### Postal + SLCSP Inputs
- **ZipCode** (`zip_codes`): unique per `(zipcode, state_abbreviation, county_id)`,
  connected to one county and one rate area. Used to resolve rate-area context for
  requests, including cases where a zipcode spans multiple counties or states.
- **SlcspRequest** (`slcsp_requests`): stores the incoming zipcode list for SLCSP
  evaluation as raw zip strings.

### Relationship Summary
- `State` → `County`, `RateArea`, `ZipCode`, `Plan`
- `County` → `ZipCode`
- `RateArea` → `Plan`, `ZipCode`
- `MetalLevel` → `Plan`
- `ZipCode` provides rate-area context for `SlcspRequest` lookups by zipcode.

Indexes and unique constraints are defined to reflect expected lookup patterns:
state name and abbreviation, county code/name per state, zipcode/state/county tuples,
rate-area identifiers per state, and metal-level lookups by normalized name.
