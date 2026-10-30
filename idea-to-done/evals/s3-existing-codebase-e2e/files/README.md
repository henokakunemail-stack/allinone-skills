# shop

Tiny API.

- `POST /login` {user,password} -> {token}
- `GET /items` (Bearer token) -> list
- `POST /cart` (Bearer token) {items:[{id,qty}]} -> {subtotal,total}

Business rule: a 10% discount applies when the subtotal is **over** 100 (strictly greater than 100).
