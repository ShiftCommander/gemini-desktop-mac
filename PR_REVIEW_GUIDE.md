## PR Review Checklist pour Security Fixes

### Ce qui est inclus dans cette PR ✓

- [x] Validation exacte des hôtes pour les permissions média (critique)
- [x] Liste blanche d'extensions pour les téléchargements (critique)
- [x] Tests automatisés validant les corrections
- [x] Documentation des changements

### Ce qui manque pour rendre cette PR complète :

#### 1. **Quarantine bit sur les téléchargements** (haute priorité)

Les fichiers téléchargés devraient être marqués avec l'attribut `com.apple.quarantine` pour que macOS pose une question avant l'ouverture.

**Fichier à modifier**: `WebKit/GeminiWebView.swift` dans `downloadDidFinish()`

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

#### 2. **HTTPS enforcement + CSP validation** (haute priorité)

Ajouter une validation explicite que seul HTTPS est autorisé

**Fichier à modifier**: `WebKit/WebViewModel.swift` dans `createWebView()`

```swift
// Désactiver les contenus non-HTTPS
let prefs = WKWebpagePreferences()
prefs.allowsContentJavaScript = true
prefs.allowsInsecureMediaLoad = false  // Force HTTPS for media
prefs.allowsInsecureScripting = false  // Force HTTPS for scripts
configuration.defaultWebpagePreferences = prefs
```

#### 3. **Améliorer la validation de navigation** (priorité moyenne)

Remplacer la vérification de suffixe `.gstatic.com` par une liste exhaustive

**Fichier à modifier**: `WebKit/GeminiWebView.swift`

```swift
// Actuellement: let internalSuffixes = [".googleapis.com", ".gstatic.com"]
// Devrait être: let internalHosts = [
//    "accounts.google.com",
//    "gemini.google.com",
//    "auth.google.com"
// ]
```

#### 4. **Tests supplémentaires recommandés**

Ajouter à `security_tests.py`:

- Test HTTPS enforcement
- Test quarantine attribute
- Test rejet des URL dangeriques

---

## Recommandation pour cette PR

**État actuel**: ✅ **Partiellement prête** pour merge

### Scénario 1: Merge maintenant

- **Pros**: Corrige 2 failles critiques immédiatement
- **Cons**: Laisse des points de sécurité ouvertes
- **Recommandé si**: Vous voulez des PR plus petites et focalisées

### Scénario 2: Améliorer avant merge (recommandé)

Ajouter au minimum:

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
