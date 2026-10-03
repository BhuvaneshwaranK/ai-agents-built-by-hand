# Shop data (synthetic)

All data describes **The Bike Stop**, a fictional bicycle repair shop.
Every name, order, price, address, and review was hand-written for this
book. None of it describes a real business or person.

Provenance: hand-authored synthetic data, created October 2026.
License: CC0 1.0 (public domain dedication).

## Data dictionary

`shop/repairs.json`: a list of repair orders.

| Field | Type | Meaning |
|---|---|---|
| order_id | text | Order number, format `R-` plus four digits |
| customer | text | Customer first name (fictional) |
| bike | text | Short bike description |
| problem | text | What the customer reported |
| status | text | One of: received, in progress, waiting for parts, ready for pickup |
| ready_by | text | Expected day, in plain words |
| quote_usd | number | Agreed price in US dollars |

`shop/price_list.csv`: columns `service`, `price_usd`, `minutes`.

`shop/slots.json`: `free` is a list of slot labels such as `Mon 10:00`;
`booked` is a list of objects with `slot`, `customer`, and `service`.
Booking tools change this file, so keep a clean copy.

`shop/docs/*.md`: short shop documents used for retrieval.
`customer_reviews.md` deliberately contains a **prompt-injection example**
(the "Special Offer" review). It is used in Chapter 11 to show why text
from documents must be treated as untrusted data.

`shop/notes.json` is created at run time by the `remember` tool.
