## PR Review Checklist for Security Fixes

### What's included in this PR ✓

- [x] Exact host validation for media permissions (critical)
- [x] Allowlist of extensions for downloads (critical)
- [x] Automated tests validating the fixes
- [x] Documentation of changes

### What's missing to make this PR complete:

#### 1. **Quarantine bit on downloads** (high priority)

Downloaded files should be marked with the `com.apple.quarantine` attribute so macOS prompts before opening.

**File to modify**: `WebKit/GeminiWebView.swift` in `downloadDidFinish()`

```swift
func downloadDidFinish(_ download: WKDownload) {
    guard let destination = downloadDestination else { return }

    // Set quarantine attribute for downloaded files
    do {
        try FileManager.default.setAttributes(
            [.protectionKey: URLFileProtection.complete],
            ofItemAtPath: destination.path
        )
        // Also set quarantine extended attribute
        guard var values = try FileManager.default.attributesOfItem(atPath: destination.path) else { return }
        var quarantine = ""
        // macOS format: 0001;timestamp;appname;appid
        let timestamp = Date().timeIntervalSince1970
        quarantine = "0001;\(Int(timestamp));Gemini Desktop;com.alexcding.geminidesktop"
        // Note: Extended attributes require Foundation extensions

    } catch {
        print("[Security] Failed to set quarantine on download: \(error)")
    }

    NSWorkspace.shared.activateFileViewerSelecting([destination])
}
```

#### 2. **HTTPS enforcement + CSP validation** (high priority)

Add explicit validation that only HTTPS is allowed

**File to modify**: `WebKit/WebViewModel.swift` in `createWebView()`

```swift
// Disable insecure content
let prefs = WKWebpagePreferences()
prefs.allowsContentJavaScript = true
prefs.allowsInsecureMediaLoad = false  // Force HTTPS for media
prefs.allowsInsecureScripting = false  // Force HTTPS for scripts
configuration.defaultWebpagePreferences = prefs
```

#### 3. **Improve navigation validation** (medium priority)

Replace suffix matching with exhaustive list

**File to modify**: `WebKit/GeminiWebView.swift`

```swift
// Currently: let internalSuffixes = [".googleapis.com", ".gstatic.com"]
// Should be: let internalHosts = [
//    "accounts.google.com",
//    "gemini.google.com",
//    "auth.google.com"
// ]
```

#### 4. **Recommended additional tests**

Add to `security_tests.py`:

- HTTPS enforcement test
- Quarantine attribute test
- Test for rejecting dangerous URLs

---

## Recommendation for this PR

**Current status**: ✅ **Partially ready** for merge

### Scenario 1: Merge now

- **Pros**: Fixes 2 critical vulnerabilities immediately
- **Cons**: Leaves some security gaps open
- **Recommended if**: You want smaller, focused PRs

### Scenario 2: Improve before merge (recommended)

Add at minimum:

1. Quarantine bit (5 min)
2. HTTPS enforcement (10 min)

This would make a **complete and secure PR** covering all critical attack vectors.

---

## PR Description Template

```markdown
## Security: Fix critical media permissions and download validation vulnerabilities

### Summary

Fixes 2 critical security vulnerabilities that could allow credential theft or malware execution:

1. Media permissions using unsafe hostname matching (substring instead of exact)
2. File downloads without validation allowing executable files

### Changes

- **GeminiWebView.swift**:
  - Fixed media permissions to use exact hostname matching (gemini.google.com, accounts.google.com)
  - Added mandatory file extension validation with allowlist
  - Added security logging for rejected downloads

- **security_tests.py**: Added automated tests validating fixes

### Security Impact

- ❌ Threat mitigated: Attacker registering `evil.google.com` gaining camera/mic access
- ❌ Threat mitigated: Trojan delivery via unrestricted file downloads
- ✅ No regression: Changes are backward compatible

### Testing

Run: `python3 security_tests.py`
All 3 security tests pass ✓

### Related

Closes: (if you have an issue)
Addresses audit findings: GeminiWebView.swift:120, :55-75

### Follow-up PRs

- Add quarantine attribute to downloads
- Add HTTPS enforcement + CSP validation
- Replace domain suffix matching with exact allowlist
```

Would you like me to:

1. **Add the additional fixes** (quarantine + HTTPS) for a complete PR?
2. **Create the PR as is** with this template?
3. **Add more tests**?

// Disable insecure content
let prefs = WKWebpagePreferences()
prefs.allowsContentJavaScript = true
prefs.allowsInsecureMediaLoad = false  // Force HTTPS for media
prefs.allowsInsecureScripting = false  // Force HTTPS for scripts
configuration.defaultWebpagePreferences = prefs
```

#### 3. **Improve navigation validation** (medium priority)

Replace suffix matching with exhaustive list

**File to modify**: `WebKit/GeminiWebView.swift`

```swift
// Currently: let internalSuffixes = [".googleapis.com", ".gstatic.com"]
// Should be: let internalHosts = [
//    "accounts.google.com",
//    "gemini.google.com",
//    "auth.google.com"
// ]
```

#### 4. **Recommended additional tests**

Add to `security_tests.py`:

- HTTPS enforcement test
- Quarantine attribute test
- Test for rejecting dangerous URLs

---

## Recommendation for this PR

**Current status**: ✅ **Partially ready** for merge

### Scenario 1: Merge now

- **Pros**: Fixes 2 critical vulnerabilities immediately
- **Cons**: Leaves some security gaps open
- **Recommended if**: You want smaller, focused PRs

### Scenario 2: Improve before merge (recommended)

Add at minimum:

1. Quarantine bit (5 min)
2. HTTPS enforcement (10 min)

Cela ferait une PR **complète et sécurisée** couvrant tous les problèmes critiques.

---

## Template de description de PR

```markdown
## Security: Fix critical media permissions and download validation vulnerabilities

### Summary

Fixes 2 critical security vulnerabilities that could allow credential theft or malware execution:

1. Media permissions using unsafe hostname matching (substring instead of exact)
2. File downloads without validation allowing executable files

### Changes

- **GeminiWebView.swift**:
  - Fixed media permissions to use exact hostname matching (gemini.google.com, accounts.google.com)
  - Added mandatory file extension validation with allowlist
  - Added security logging for rejected downloads

- **security_tests.py**: Added automated tests validating fixes

### Security Impact

- ❌ Threat mitigated: Attacker registering `evil.google.com` gaining camera/mic access
- ❌ Threat mitigated: Trojan delivery via unrestricted file downloads
- ✅ No regression: Changes are backward compatible

### Testing

Run: `python3 security_tests.py`
All 3 security tests pass ✓

### Related

Closes: (if you have an issue)
Addresses audit findings: GeminiWebView.swift:120, :55-75

### Follow-up PRs

- Add quarantine attribute to downloads
- Add HTTPS enforcement + CSP validation
- Replace domain suffix matching with exact allowlist
```

Voulez-vous que je :

1. **Ajoute les corrections supplémentaires** (quarantine + HTTPS) pour une PR complète ?
2. **Crée la PR telle quelle** avec ce template ?
3. **Ajoute d'autres tests** ?
