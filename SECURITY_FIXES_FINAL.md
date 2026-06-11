# Gemini Desktop Security Hardening Summary

## Background
This PR hardens Gemini Desktop WebView behavior to prevent credential theft, malware delivery, and MITM risk.

## What changed
- `GeminiWebView` download gating and quarantine xattr.
- Media capture host check to exact domain allowlist.
- `WebViewModel` enforces HTTPS for media/script content.
- URL filtering on external links changed to exact domain allowlist.
- Tests and scripts updated to English and to path-independent paths.

## Why this is safe
- Uses App Sandbox and hardened runtime settings preserved.
- No new insecure APIs introduced.
- Non-blocking failures for quarantine setxattr log warning only.

## How to test
1. `python3 security_tests.py`
2. `./security_check.sh`
3. `xcodebuild -scheme GeminiDesktop build`

## Result
- 6/6 tests passed in security tests.
- PR is ready for review.
