#!/bin/bash

# Automated security checks script for Gemini Desktop

echo "=== Security checks for Gemini Desktop ==="

# Step 1: Static code analysis
echo "1. Static code analysis..."

# Search for evaluateJavaScript
echo "   - evaluateJavaScript usages:"
grep -n "evaluateJavaScript" *.swift WebKit/*.swift ChatBar/*.swift || echo "   None found"

# Search for .contains for hosts
echo "   - .contains() usages for hosts:"
grep -n "\.contains(" WebKit/GeminiWebView.swift || echo "   None found"

# Search for downloads without validation
echo "   - Downloads without validation:"
grep -A 10 "decideDestinationUsing" WebKit/GeminiWebView.swift || echo "   None found"

# Search for console.log bridge
echo "   - console.log bridge:"
grep -n "consoleLog" WebKit/WebViewModel.swift WebKit/UserScripts.swift || echo "   None found"

# Step 2: Configuration checks
echo "2. Configuration checks..."

# Sandbox
if grep -q "ENABLE_APP_SANDBOX = YES" GeminiDesktop.xcodeproj/project.pbxproj; then
    echo "   ✓ App Sandbox enabled"
else
    echo "   ✗ App Sandbox not enabled"
fi

# Hardened Runtime
if grep -q "ENABLE_HARDENED_RUNTIME = YES" GeminiDesktop.xcodeproj/project.pbxproj; then
    echo "   ✓ Hardened Runtime enabled"
else
    echo "   ✗ Hardened Runtime not enabled"
fi

# User Script Sandboxing
if grep -q "ENABLE_USER_SCRIPT_SANDBOXING = YES" GeminiDesktop.xcodeproj/project.pbxproj; then
    echo "   ✓ User Script Sandboxing enabled"
else
    echo "   ✗ User Script Sandboxing not enabled"
fi

# Incoming Network
if grep -q "ENABLE_INCOMING_NETWORK_CONNECTIONS = NO" GeminiDesktop.xcodeproj/project.pbxproj; then
    echo "   ✓ Incoming network connections disabled"
else
    echo "   ✗ Incoming network connections enabled"
fi

# Step 3: Binary scanner (if compiled)
echo "3. Binary scanner..."
if [ -f "build/Release/GeminiDesktop.app/Contents/MacOS/GeminiDesktop" ]; then
    echo "   Binary found. Checks to implement (codesign, etc.)"
    # codesign -dv build/Release/GeminiDesktop.app
else
    echo "   No compiled binary found. Build first with xcodebuild."
fi

# Step 4: Automated tests (simulation)
echo "4. Automated tests..."
echo "   - Download validation test: To implement (check allowed extensions)"
echo "   - Media permissions test: To implement (check exact hosts)"

# Step 5: Logs and data audit
echo "5. Logs and data audit..."
echo "   - Check ~/Library/Containers/com.alexcding.geminidesktop/ for sensitive data"
echo "   - Check system logs for leaks"

echo "=== End of checks ==="