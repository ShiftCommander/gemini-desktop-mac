# Gemini Desktop Security Fixes Summary

## Implemented fixes

### 1. Exact host matching for media permission checks
- Fixed `requestMediaCapturePermissionFor` host validation `contains` bug.
- Now grants only to `gemini.google.com` and `accounts.google.com`.

### 2. Download extension allowlist
- Added allowed extension check: `pdf, txt, csv, jpg, jpeg, png, gif, doc, docx, xls, xlsx, json`.
- Rejects unknown or empty file extensions with `completionHandler(nil)`.

### 3. Quarantine xattr for downloads
- Sets `com.apple.quarantine` via `setxattr` (system API) in `downloadDidFinish`.
- Keeps the warning for macOS "downloaded from internet" behavior.

### 4. HTTPS enforcement
- In `WebViewModel.createWebView`, set:
  - `allowsInsecureMediaLoad = false`
  - `allowsInsecureScripting = false`
- Prevents loading insecure resources.

### 5. Strict internal URL whitelist
- Replaced suffix-based checks (`.googleapis.com`, `.gstatic.com`) with explicit allowlist:
  - `gemini.google.com`, `www.gemini.google.com`, `accounts.google.com`, `auth.google.com`, `fonts.googleapis.com`, `fonts.gstatic.com`, `google.com`, `www.google.com`.

### 6. Debug-only console bridge
- `WebViewModel` registers console log handler only under `#if DEBUG`.

## Tests
- `security_tests.py` is now path-independent using `REPO_ROOT = pathlib.Path(__file__).resolve().parent`.
- 6 checks all passing:
  - Media permissions
  - Download validation
  - Quarantine attribute
  - HTTPS enforcement
  - Domain whitelist
  - console.log bridge

## Verification command
```
python3 security_tests.py
```
