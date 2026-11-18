# Data licences

The code in this repository is MIT-licensed (see `LICENSE`). **The data files are not covered by the MIT licence.** Each series keeps its source's own terms, listed below.

Every series shipped here comes from a U.S. federal agency and is in the public domain. The question set uses **only** sources whose row in Palanor's provenance ledger (`data_sources`) has the licence class `public_domain`. It ships nothing from a display-only, share-alike or unknown-licence source, nothing derived from first-release vintages (ALFRED), no prices of single securities and no prediction-market data.

The readings are the latest published values (revisions included) as served by Palanor's public API on the date in `src/outcome_evals/data/series/series.json`. Credit the publishing agency when you use them. Nothing here implies endorsement by any agency.

Each ledger row below is quoted as recorded, with the date its terms were checked.

## U.S. Bureau of Labor Statistics (`bls`)

- Licence class: `public_domain` · redistributable: yes
- Licence: U.S. Government work (public domain) — <https://www.bls.gov/opub/copyright-information.htm>
- Credit line: "Source: U.S. Bureau of Labor Statistics"
- Terms checked: 2026-09-24
- Terms, quoted:
  > BLS: "everything that we publish, both in hard copy and electronically, is in the public domain" (except previously copyrighted photographs and illustrations); "You are free to use our public domain material without specific permission," and "we do ask that you cite the Bureau of Labor Statistics as the source."
  > The BLS series here are received through FRED. FRED lists one source for each of them, the U.S. Bureau of Labor Statistics, and that source's public-domain terms apply.
- Series shipped:
  - `fred_cpi`: Consumer Price Index (BLS CUSR0000SA0 (FRED CPIAUCSL)), readings from 2005 on
  - `fred_core_cpi`: Core CPI (BLS CUSR0000SA0L1E (FRED CPILFESL)), readings from 2005 on
  - `fred_ppi`: Producer Price Index (BLS WPU00000000 (FRED PPIACO)), readings from 2005 on
  - `fred_unemployment`: Unemployment Rate (BLS LNS14000000 (FRED UNRATE)), readings from 2005 on
  - `fred_u6_underemployment`: U-6 Underemployment Rate (BLS LNS13327709 (FRED U6RATE)), readings from 2005 on
  - `fred_lfpr`: Labor Force Participation Rate (BLS LNS11300000 (FRED CIVPART)), readings from 2005 on
  - `fred_nfp`: Nonfarm Payrolls (BLS CES0000000001 (FRED PAYEMS)), readings from 2005 on
  - `avg-hrly-earn`: U.S. Average Hourly Earnings, All Private Employees (BLS CES0500000003), readings from 2006 on
  - `fred_jolts`: JOLTS Job Openings (BLS JTS000000000000000JOL (FRED JTSJOL)), readings from 2005 on

## U.S. Bureau of Economic Analysis (`bea`)

- Licence class: `public_domain` · redistributable: yes
- Licence: U.S. Government work (public domain) — <https://www.bea.gov/taxonomy/term/611?page=2>
- Credit line: "Source: U.S. Bureau of Economic Analysis"
- Terms checked: 2026-09-24
- Terms, quoted:
  > BEA FAQ: "the information posted on this web site is in the public domain and may be used or reproduced without specific permission."
- Series shipped:
  - `fred_pce_deflator`: PCE Price Index (BEA NIPA Table 2.8.4 (FRED PCEPI)), readings from 2005 on
  - `fred_pcepilfe`: U.S. Core PCE Price Index (BEA NIPA Table 2.8.4 (FRED PCEPILFE)), readings from 2005 on
  - `fred_savings_rate`: Personal Savings Rate (BEA NIPA Table 2.1 (FRED PSAVERT)), readings from 2005 on
  - `auto-sales`: Total light-vehicle sales (BEA (FRED TOTALSA)), readings from 2005 on
  - `fred_gdp`: Real GDP (BEA NIPA Table 1.1.6 (FRED GDPC1)), readings from 2005 on

## U.S. Census Bureau (`us_census`)

- Licence class: `public_domain` · redistributable: yes
- Licence: U.S. Government work (17 U.S.C. §105) — <https://www.census.gov/about/policies/open-gov/open-data.html>
- Credit line: "Source: U.S. Census Bureau."
- Terms checked: 2026-09-26
- Terms, quoted:
  > Census open-data page: "The U.S. Census Bureau is committed to open government by sharing its public data as open data". Census works are works of the U.S. Government, which 17 U.S.C. §105 places outside copyright.
  > The Census API terms (census.gov/data/developers/about/terms-of-service.html) ask that the Census name not be used to imply endorsement.
- Series shipped:
  - `fred_housing`: Housing Starts (Census New Residential Construction (FRED HOUST)), readings from 2005 on
  - `permits`: New private housing units authorized (Census New Residential Construction (FRED PERMIT)), readings from 2005 on
  - `retail-sales`: Retail sales · advance (Census Advance Monthly Retail Trade (FRED RSAFS)), readings from 2005 on
  - `construction`: Total construction spending (Census Construction Spending (FRED TTLCONS)), readings from 2005 on
  - `fred_durable_goods_new_orders`: Durable Goods · New Orders (Census M3 (FRED DGORDER)), readings from 2005 on

## U.S. Department of Labor (`us_dol`)

- Licence class: `public_domain` · redistributable: yes
- Licence: Public domain (U.S. Government work) — <https://www.dol.gov/general/aboutdol/copyright>
- Credit line: "Source: U.S. Department of Labor."
- Terms checked: 2026-09-26
- Terms, quoted:
  > dol.gov/general/aboutdol/copyright: "Materials created by the federal government are generally part of the public domain and may be used, reproduced and distributed without permission." Not to be used in a way that implies DOL endorsement.
- Series shipped:
  - `fred_jobless`: Initial Jobless Claims (DOL ETA 539 (FRED ICSA)), readings from 2005 on
  - `continued-claims`: Continued jobless claims (DOL ETA 539 (FRED CCSA)), readings from 2005 on

## U.S. Department of the Treasury, Bureau of the Fiscal Service (`us_treasury`)

- Licence class: `public_domain` · redistributable: yes
- Licence: Fiscal Data API license (public domain) — <https://fiscaldata.treasury.gov/api-documentation/>
- Credit line: "Source: U.S. Treasury, Bureau of the Fiscal Service"
- Terms checked: 2026-09-24
- Terms, quoted:
  > Fiscal Data: "offered free, without restriction … for non-commercial or commercial purposes". The Daily Treasury Par Yield Curve is a work of the U.S. Government (17 U.S.C. §105).
- Series shipped:
  - `rates.ust.par.10y`: U.S. Treasury Par Yield, 10-Year (Daily) (Treasury Daily Par Yield Curve, 10 Yr), readings from 2005 on
  - `rates.ust.par.2y`: U.S. Treasury Par Yield, 2-Year (Daily) (Treasury Daily Par Yield Curve, 2 Yr), readings from 2005 on
  - `rates.ust.par.3m`: U.S. Treasury Par Yield, 3-Month (Daily) (Treasury Daily Par Yield Curve, 3 Mo), readings from 2005 on
  - `rates.spread_2y10y`: Treasury Curve · 2s10s Spread (Treasury Daily Par Yield Curve, 10 Yr − 2 Yr), readings from 2005 on
  - `rates.spread_3m10y`: Treasury Curve · 3m10y Spread (Treasury Daily Par Yield Curve, 10 Yr − 3 Mo), readings from 2005 on

## U.S. Energy Information Administration (`eia`)

- Licence class: `public_domain` · redistributable: yes
- Licence: EIA Copyrights & Reuse (public domain) — <https://www.eia.gov/about/copyrights_reuse.php>
- Credit line: "Source: U.S. Energy Information Administration"
- Terms checked: 2026-09-24
- Terms, quoted:
  > eia.gov/about/copyrights_reuse.php (read again 2026-11-18): "U.S. government publications are in the public domain and are not subject to copyright protection. You may use and/or distribute any of our data, files, databases, reports, graphs, charts, and other information products that are on our website or that you receive through our email distribution service." (Photographs on EIA's site are licensed separately; none are used here.)
- Series shipped:
  - `fred_gas_price_regular`: US Regular Gasoline Price (Weekly) (EIA EMM_EPMR_PTE_NUS_DPG (FRED GASREGW)), readings from 2005 on

## Your own data

When you resolve calls against Palanor's API (`PalanorAPI`), each response carries a `provenance` block with the source's licence; `outcome-evals` keeps it on the series (`SeriesInfo.license`, `license_url`, `attribution`). The API serves only sources whose licence allows redistribution. Calls and series you bring yourself stay yours.
