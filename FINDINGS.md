# Codebase Findings: Flaws, Security Risks & Missing Features

---

## Critical

### 1. Django SECRET_KEY hardcoded in version control
**File:** `api/nvdnew/settings/base.py:24`

The Django secret key is a plaintext string committed to the repository. Any historical clone of the repo exposes it permanently. This key is used to sign session tokens, CSRF tokens, and password reset links. Both dev and production use the same key (prod only extends base).

**Fix:** Load from environment variable: `SECRET_KEY = os.environ['DJANGO_SECRET_KEY']`

---

### 2. File upload endpoints have no authentication
**File:** `fileserver/main.go:35-36`

`/upload/image` and `/upload/pdf` accept uploads from any unauthenticated request. In production, port 7002 is exposed and nginx routes to it. Anyone can upload arbitrary files to the server.

**Fix:** Require a shared secret header checked against an environment variable, or proxy uploads through the Django API which enforces authentication.

---

### 3. All participant personal data is publicly accessible (GDPR)
**File:** `api/nvdagen/viewsets.py:105`

`ParticipantViewSet` uses `permission_classes = (AllowAny,)`, making `GET /api/participant/` return every registered participant's name, email, phone number, year, study programme, allergies, attendance token, and check-in status — with no login required.

**Fix:** Restrict the list/retrieve actions to authenticated staff. Only the `create` (registration) and `destroy` (deregistration) actions need to be open.

---

### 4. Content-Type validation on file uploads is client-controlled
**File:** `fileserver/main.go:67-75`

The fileserver validates the file type by reading `header.Header.Get("Content-Type")`, which is the MIME type declared by the browser in the multipart form — not derived from the actual file bytes. A client can upload any file and label it `image/png`. SVG is also in the allowed list (`image/svg+xml`), and SVGs can contain embedded JavaScript, enabling stored XSS when served back.

**Fix:** Validate file magic bytes server-side. Remove SVG from allowed types or sanitise it before storing. Use a library like `net/http`'s `DetectContentType` on the raw bytes.

---

### 5. No file size limit on uploads
**File:** `fileserver/main.go:77-79`

`ioutil.ReadAll(file)` reads the entire upload into memory with no size cap. A large upload will consume all available RAM and crash the container.

**Fix:** Wrap the request body: `r.Body = http.MaxBytesReader(w, r.Body, 10<<20)` (10 MB) before reading.

---

## High

### 6. `CORS_ORIGIN_ALLOW_ALL = True` overrides the whitelist
**File:** `api/nvdnew/settings/base.py:76`

`CORS_ORIGIN_ALLOW_ALL = True` is set directly below the `CORS_ORIGIN_WHITELIST`. The whitelist is completely ignored. Any origin on the internet can make credentialed requests to the API.

**Fix:** Remove `CORS_ORIGIN_ALLOW_ALL = True`. The whitelist alone is sufficient for dev.

---

### 7. Database password hardcoded in base settings (used in production)
**File:** `api/nvdnew/settings/base.py:108`

The database password `1234` is hardcoded in `base.py`, which `prod.py` imports unchanged. Production runs with this trivially guessable password.

**Fix:** Load from environment variable: `'PASSWORD': os.environ.get('POSTGRES_PASSWORD', '1234')`.

---

### 8. Duplicate viewset registration exposes unintended CRUD routes
**File:** `api/nvdnew/routers.py:13`

`router.register(r'participant-count', ParticipantViewSet)` registers the full `ParticipantViewSet` a second time under `/api/participant-count/`. This is presumably intended to provide a count endpoint, but it actually exposes full list, create, retrieve, update, and delete operations for participants at an undocumented URL — bypassing any URL-level access controls or monitoring.

**Fix:** Remove this registration. The `count` action is already reachable as `/api/participant/count/`.

---

### 9. `/api/participant/verify/` exposes participant data without authentication
**File:** `api/nvdagen/viewsets.py:319-334`

The `verify` endpoint is a `GET` with no permission restriction (inherits `AllowAny` from the viewset). It returns name, email, study, year, allergies, and the `attendance_token` UUID for any valid token. Since the token is also included in the email sent to the participant, forwarding an email could allow a third party to look up the participant's personal details.

**Fix:** Restrict to `IsAuthenticated` — only the QR scanner (a logged-in admin) needs to call this.

---

### 10. Race condition in participant registration
**File:** `api/nvdagen/viewsets.py:113-116`

The duplicate-registration check (`notRegistered = Participant.objects.filter(...).count() == 0`) and the subsequent `super().create(request)` are not wrapped in a database transaction or protected by a unique constraint. Two concurrent POST requests with the same email and event can both pass the check and create duplicate registrations.

**Fix:** Add a unique constraint on `(email, event)` in the model, or wrap the check-and-create in `transaction.atomic()` with `select_for_update`.

---

### 11. Auth token stored in `localStorage` (XSS risk)
**File:** `frontend/src/store/admin.module.js:58-59`

The DRF auth token is written to `localStorage`. Any JavaScript running on the page (e.g., from a third-party script or an XSS vector) can read it and impersonate an admin.

**Fix:** Store the token in a `HttpOnly` cookie set by the server, which JavaScript cannot read.

---

### 12. Email enumeration via deregistration code endpoint
**File:** `api/nvdagen/viewsets.py:172-198`

`GET /api/participant/{id}/` sends a deregistration-code email to the participant at that integer ID. IDs are sequential, so an attacker can iterate from 1 upward to spam every registered participant with unsolicited emails and confirm which IDs are valid.

**Fix:** Require the caller to provide the participant's email in the request and verify it matches before sending. Also restrict this endpoint to POST rather than GET.

---

## Medium

### 13. No HTTPS security headers in production settings
**File:** `api/nvdnew/settings/prod.py`

The production settings file only sets `ALLOWED_HOSTS` and `DEBUG = False`. Missing Django security settings include:
- `SECURE_SSL_REDIRECT = True`
- `SECURE_HSTS_SECONDS = 31536000`
- `SESSION_COOKIE_SECURE = True`
- `CSRF_COOKIE_SECURE = True`
- `SECURE_BROWSER_XSS_FILTER = True`

---

### 14. No rate limiting on registration or login
Neither the participant registration endpoint (`POST /api/participant/`) nor the login endpoint (`POST /rest-auth/login/`) has any rate limiting. Both can be brute-forced or flooded freely.

**Fix:** Add `django-ratelimit` or configure rate limiting in nginx.

---

### 15. No input validation on participant fields
**File:** `api/nvdagen/serializers.py:39-42`

`ParticipantSerializer` uses `fields = '__all__'` with no custom validators. Email format, phone number format, and string lengths are not validated beyond the model's `max_length`. A registration with `email = "notanemail"` will succeed.

**Fix:** Add field-level validators in the serializer (e.g., `EmailField`, regex for phone).

---

### 16. `attendance_stats` endpoint is unauthenticated
**File:** `api/nvdagen/viewsets.py:336-387`

`GET /api/participant/attendance_stats/` returns per-event attendance counts to any unauthenticated caller. While counts alone are low-sensitivity, it leaks event names and registration volumes.

**Fix:** Add `permission_classes = [IsAuthenticated]` to this action.

---

### 17. Frontend fetches all participant data when only a count is needed
**File:** `frontend/src/store/participant.module.js:12`

A TODO comment in the code acknowledges this: the store fetches the full participant list (`/api/participant/`) and stores it in state, when the only use is to display a count. This loads all personal data into the browser's memory and `localStorage` (via `vuex-persistedstate`).

**Fix:** Use the dedicated `/api/participant/count/` endpoint and remove participant personal data from the Vuex store entirely.

---

### 18. Program times stored as Unix integer timestamps with hardcoded timezone offset
**File:** `api/nvdagen/viewsets.py:140`, `api/nvdagen/models.py:118-119`

`timeStart` and `timeEnd` are plain `IntegerField` columns. The viewset then calls `datetime.fromtimestamp(program.timeStart+3600)` — hardcoding a +1 hour UTC offset to get Oslo time. This breaks during daylight saving time and is not portable.

**Fix:** Use `DateTimeField` with `USE_TZ = True` and `TIME_ZONE = 'Europe/Oslo'`, or store timestamps as proper UTC and convert with `pytz`/`zoneinfo`.

---

### 19. No pagination on list endpoints
All viewsets return unbounded lists. As the database grows, `GET /api/participant/`, `GET /api/listing/`, etc., will return increasingly large payloads.

**Fix:** Set `PAGE_SIZE` in `REST_FRAMEWORK` settings and add `DEFAULT_PAGINATION_CLASS`.

---

### 20. Fileserver CORS is a wildcard
**File:** `fileserver/main.go:229`

`Access-Control-Allow-Origin: *` is set on all fileserver responses. Any website can make cross-origin requests to the upload endpoint from a user's browser.

**Fix:** Restrict to the known frontend origin.

---

## Low

### 21. `saveThumb` errors are silently ignored
**File:** `fileserver/main.go:103-106`

The three `saveThumb` calls in `uploadHandler` return errors that are never checked. A thumbnail generation failure is silently swallowed and a 200 is still returned.

---

### 22. Deprecated `ioutil` package in Go fileserver
**File:** `fileserver/main.go:77, 98, 201, 211`

`ioutil.ReadAll` and `ioutil.WriteFile` have been deprecated since Go 1.16. The replacements are `io.ReadAll` and `os.WriteFile`.

---

### 23. Debug `console.log` statements in production frontend
**File:** `frontend/src/store/participant.module.js:13-15`

`console.log(response)` and `console.log(all)` log raw API responses including participant data to the browser console.

---

### 24. Vue 2 is end-of-life
Vue 2 reached end-of-life on 31 December 2023 and no longer receives security patches.

---

### 25. `Program` has no day association
**File:** `api/nvdagen/models.py:113-125`

`Business` has a `days` field (Day 1 / Day 2 / Both), but `Program` does not. There is no way to mark a programme event as belonging to a specific day of the event.

---

## Missing Features

| # | Feature | Notes |
|---|---------|-------|
| 1 | **Brute-force protection on login** | No account lockout or CAPTCHA after repeated failures |
| 2 | **Admin audit log** | No record of who created/edited/deleted content via the admin panel |
| 3 | **Automated database backups** | README describes manual restore procedure but no scheduled backup mechanism exists |
| 4 | **Environment-variable-driven production config** | DB password, secret key, and allowed hosts should all come from env vars, not hardcoded values |
| 5 | **Search and filtering on listings/businesses** | No server-side filtering; the frontend must load everything to search |
| 6 | **Waiting list position visibility** | Participants placed on the waiting list are told their position in the email but have no way to check their current position later |
| 7 | **Participant self-service deregistration link** | Currently requires a separate GET to trigger a code email, then a DELETE with the code — a one-click email link would be simpler |
| 8 | **File deletion** | Uploaded images and PDFs cannot be deleted through the fileserver; orphaned files accumulate indefinitely |
