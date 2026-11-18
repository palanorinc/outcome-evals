# Citing Palanor data

Every Palanor MCP result that carries data also carries a `provenance` block, and most add a top-level
`attribution` line for Palanor itself. This page covers how to turn them into a source line, and what each licence
class lets the user do.

## The provenance block

| Field | Meaning | Use it for |
|---|---|---|
| `source` | Palanor's key for the upstream (`bls`, `us_treasury`, `palanor`) | Grouping; don't print it |
| `publisher` | Who publishes the data | The source line when `attribution` is empty |
| `license_class` | The licence class (table below) | Deciding what the user may do with the data |
| `license_name` | The licence in words | The licence part of the source line |
| `license_url` | The licence or terms page | A link when the user republishes |
| `attribution` | The credit line the source asks for | The source line, as written |
| `redistributable` | Whether the data may be passed on | `false` means display-only: see below |
| `notice` (sometimes) | Text the source's terms require next to its data | Print it as given |

## Licence classes

| `license_class` | What it is | Passing the data on |
|---|---|---|
| `public_domain` | Government works and similar (BLS, BEA, Census, Treasury, EIA's own surveys) | Allowed. Credit the publisher anyway; it is good practice and the attribution line asks for it. |
| `open_attribution` | Open licences that require credit (for example CC BY 4.0: World Bank, OECD) | Allowed with the attribution line and the licence name. Keep both with any copy, table or chart. |
| `palanor_derived` | Palanor's own computations: Custom Indices, Currents, Foresight | Allowed with "Data: Palanor (palanor.com)" and a link to the methodology page. |
| `palanor_refined` | Structured data Palanor extracted from public documents (guidance, KPIs, risk factors) | Allowed with the Palanor credit and the primary filing it came from when the result gives one. |
| anything else, or `redistributable: false` | Display-only, share-alike or unclear terms | Not as data. See "Display-only" below. |

The server serves only redistributable signals, so a `provenance` block on a signal you received will almost
always say `redistributable: true`. Other tools can return records that point at outside documents (filings,
news outlets); quote those as references with their own links, not as Palanor data.

## Source line templates

One series:

> Source: U.S. Bureau of Labor Statistics (public domain), via Palanor
> ([palanor.com/signals/fred_unemployment](https://palanor.com/signals/fred_unemployment)).

An openly licensed series that will be republished:

> Source: World Bank Commodity Price Data (The Pink Sheet), CC BY 4.0
> (https://datacatalog.worldbank.org/public-licenses#cc-by), via Palanor.

(Here `attribution` already names the licence, so it isn't repeated.)

Take the publisher and licence wording from the result you received; the names above are examples.

A Custom Index:

> Data: Palanor, Capital Tightness index ([methodology](https://palanor.com/indices/capital_tightness)).

Several series: one line per publisher, in the order they appear in the answer.

A chart from `palanor_get_chart`: print every string in its `attribution` array under the image, unchanged.

## Display-only

The signs that data is display-only:

- an error saying a signal is "not found, not public, or not licensed for redistribution";
- `embeddable: false` from `palanor_get_embed_code`;
- `latest_value_withheld` on a Custom Index component;
- `redistributable: false` in any provenance block.

What to do:

- Say it can be seen on palanor.com, on the page the result links, if there is one.
- Don't describe it as downloadable, exportable, embeddable or "available through the API".
- Don't put its values in a table, file, chart or embed, and don't supply them from memory or another site as if
  they came from Palanor.
- Everything else in the same result (the index value, the other components) is still fine to use.

## Dates in a citation

Cite the observation date, not the retrieval date: "Unemployment rate, October 2026: 4.1% (BLS, via Palanor)".
If the user needs a retrieval date for a bibliography, add "retrieved <today>" after it.
