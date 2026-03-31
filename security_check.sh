#!/bin/bash

# Script de vérifications automatisées de sécurité pour Gemini Desktop

echo "=== Vérifications de sécurité pour Gemini Desktop ==="

# Étape 1: Analyse statique du code
echo "1. Analyse statique du code..."

# Chercher evaluateJavaScript
echo "   - Usages de evaluateJavaScript:"
grep -n "evaluateJavaScript" *.swift WebKit/*.swift ChatBar/*.swift || echo "   Aucun trouvé"

# Chercher .contains pour les hôtes
echo "   - Usages de .contains() pour les hôtes:"
grep -n "\.contains(" WebKit/GeminiWebView.swift || echo "   Aucun trouvé"

# Chercher téléchargements sans validation
echo "   - Téléchargements sans validation:"
grep -A 10 "decideDestinationUsing" WebKit/GeminiWebView.swift || echo "   Aucun trouvé"

# Chercher console.log bridge
echo "   - Pont console.log:"
grep -n "consoleLog" WebKit/WebViewModel.swift WebKit/UserScripts.swift || echo "   Aucun trouvé"

# Étape 2: Vérifications des configurations
echo "2. Vérifications des configurations..."

# Sandbox
if grep -q "ENABLE_APP_SANDBOX = YES" GeminiDesktop.xcodeproj/project.pbxproj; then
    echo "   ✓ App Sandbox activé"
else
    echo "   ✗ App Sandbox non activé"
fi

# Hardened Runtime
if grep -q "ENABLE_HARDENED_RUNTIME = YES" GeminiDesktop.xcodeproj/project.pbxproj; then
    echo "   ✓ Hardened Runtime activé"
else
    echo "   ✗ Hardened Runtime non activé"
fi

# User Script Sandboxing
if grep -q "ENABLE_USER_SCRIPT_SANDBOXING = YES" GeminiDesktop.xcodeproj/project.pbxproj; then
    echo "   ✓ User Script Sandboxing activé"
else
    echo "   ✗ User Script Sandboxing non activé"
fi

# Incoming Network
if grep -q "ENABLE_INCOMING_NETWORK_CONNECTIONS = NO" GeminiDesktop.xcodeproj/project.pbxproj; then
    echo "   ✓ Connexions réseau entrantes désactivées"
else
    echo "   ✗ Connexions réseau entrantes activées"
fi

# Étape 3: Scanner le binaire (si compilé)
echo "3. Scanner le binaire..."
if [ -f "build/Release/GeminiDesktop.app/Contents/MacOS/GeminiDesktop" ]; then
    echo "   Binaire trouvé. Vérifications à implémenter (codesign, etc.)"
    # codesign -dv build/Release/GeminiDesktop.app
else
    echo "   Aucun binaire compilé trouvé. Compiler d'abord avec xcodebuild."
fi

# Étape 4: Tests automatisés (simulation)
echo "4. Tests automatisés..."
echo "   - Test de validation de téléchargement: À implémenter (vérifier extensions autorisées)"
echo "   - Test de permissions média: À implémenter (vérifier hôtes exacts)"

# Étape 5: Audit des logs et données
echo "5. Audit des logs et données..."
echo "   - Vérifier ~/Library/Containers/com.alexcding.geminidesktop/ pour données sensibles"
echo "   - Vérifier les logs système pour fuites"

echo "=== Fin des vérifications ==="