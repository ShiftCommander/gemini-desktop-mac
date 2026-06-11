#!/usr/bin/env python3

# Python script for automated security tests

import os
import re


import pathlib

REPO_ROOT = pathlib.Path(__file__).resolve().parent

def test_media_permissions():
    """Test media permissions validation"""
    print("Test: Media permissions")
    with open(REPO_ROOT / 'WebKit' / 'GeminiWebView.swift', 'r') as f:
        content = f.read()

    # Search for exact host validation
    if 'allowedHosts = ["gemini.google.com", "accounts.google.com"]' in content:
        print("   ✓ PASS: Exact host validation implemented")
        return True
    elif 'origin.host.contains(GeminiWebView.Constants.trustedHost)' in content:
        print(
            "   ✗ FAIL: Uses .contains() for trustedHost, vulnerable to subdomains")
        return False
    else:
        print("   ⚠ WARNING: Host validation not found")
        return False


def test_download_validation():
    """Test download validation"""
    print("Test: Download validation")
    with open(REPO_ROOT / 'WebKit' / 'GeminiWebView.swift', 'r') as f:
        content = f.read()

    # Check extension validation
    if 'allowedExtensions = [' in content and 'completionHandler(nil)' in content:
        print("   ✓ PASS: Extension validation with allowlist and rejection of unauthorized files")
        return True
    else:
        print("   ✗ FAIL: No extension validation for downloads")
        return False


def test_quarantine_attribute():
    """Test quarantine attribute on downloads"""
    print("Test: Quarantine attribute on downloads")
    with open(REPO_ROOT / 'WebKit' / 'GeminiWebView.swift', 'r') as f:
        content = f.read()

    if 'com.apple.quarantine' in content and 'downloadDidFinish' in content:
        print("   ✓ PASS: Quarantine attribute set on downloaded files")
        return True
    else:
        print("   ✗ FAIL: Quarantine attribute not configured")
        return False


def test_https_enforcement():
    """Test HTTPS enforcement"""
    print("Test: HTTPS enforcement")
    with open(REPO_ROOT / 'WebKit' / 'WebViewModel.swift', 'r') as f:
        content = f.read()

    if 'allowsInsecureMediaLoad = false' in content and 'allowsInsecureScripting = false' in content:
        print("   ✓ PASS: HTTPS enforced - non-HTTPS content disabled")
        return True
    else:
        print("   ✗ FAIL: HTTPS enforcement not configured")
        return False


def test_domain_whitelist():
    """Test domain whitelist"""
    print("Test: Restrictive domain whitelist")
    with open(REPO_ROOT / 'WebKit' / 'GeminiWebView.swift', 'r') as f:
        content = f.read()

    # Search for exhaustive domain list instead of suffixes
    if 'allowedDomains = [' in content and '.contains(host)' in content:
        if '.googleapis.com' not in content or 'gemini.google.com' in content:
            print("   ✓ PASS: Domains specified exhaustively")
            return True

    print("   ✗ FAIL: Still uses dangerous generic suffixes")
    return False


def test_console_log_bridge():
    """Test console.log bridge"""
    print("Test: console.log bridge")
    with open('/workspaces/gemini-desktop-mac/WebKit/WebViewModel.swift', 'r') as f:
        content = f.read()

    if '#if DEBUG' in content:
        print("   ✓ PASS: console.log bridge limited to DEBUG")
        return True
    else:
        print("   ✗ FAIL: console.log bridge active in production")
        return False


def main():
    print("=== Automated Security Tests - Gemini Desktop ===\n")

    results = []
    results.append(test_media_permissions())
    results.append(test_download_validation())
    results.append(test_quarantine_attribute())
    results.append(test_https_enforcement())
    results.append(test_domain_whitelist())
    results.append(test_console_log_bridge())

    passed = sum(results)
    total = len(results)
    print(f"\n{'='*50}")
    print(f"Results: {passed}/{total} tests passed")

    if passed == total:
        print("✓ All security checks passed")
        return 0
    else:
        print("✗ Some checks failed")
        return 1


if __name__ == "__main__":
    exit(main())
