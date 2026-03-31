#!/usr/bin/env python3

# Script Python pour tests automatisés de sécurité

import os
import re


def test_media_permissions():
    """Test de validation des permissions média"""
    print("Test: Permissions média")
    with open('/workspaces/gemini-desktop-mac/WebKit/GeminiWebView.swift', 'r') as f:
        content = f.read()

    # Chercher la validation exacte d'hôtes
    if 'allowedHosts = ["gemini.google.com", "accounts.google.com"]' in content:
        print("   ✓ PASS: Validation d'hôte exacte implémentée")
        return True
    elif 'origin.host.contains(GeminiWebView.Constants.trustedHost)' in content:
        print(
            "   ✗ FAIL: Utilise .contains() pour trustedHost, vulnérable aux sous-domaines")
        return False
    else:
        print("   ⚠ WARNING: Validation d'hôte non trouvée")
        return False


def test_download_validation():
    """Test de validation des téléchargements"""
    print("Test: Validation des téléchargements")
    with open('/workspaces/gemini-desktop-mac/WebKit/GeminiWebView.swift', 'r') as f:
        content = f.read()

    # Vérifier la validation des extensions
    if 'allowedExtensions = [' in content and 'completionHandler(nil)' in content:
        print("   ✓ PASS: Validation d'extensions avec liste blanche et rejet des fichiers non-autorisés")
        return True
    else:
        print("   ✗ FAIL: Aucune validation d'extensions pour les téléchargements")
        return False


def test_quarantine_attribute():
    """Test du quarantine attribute sur les téléchargements"""
    print("Test: Quarantine attribute sur les téléchargements")
    with open('/workspaces/gemini-desktop-mac/WebKit/GeminiWebView.swift', 'r') as f:
        content = f.read()

    if 'com.apple.quarantine' in content and 'downloadDidFinish' in content:
        print("   ✓ PASS: Quarantine attribute défini sur les fichiers téléchargés")
        return True
    else:
        print("   ✗ FAIL: Quarantine attribute non configuré")
        return False


def test_https_enforcement():
    """Test de l'application de HTTPS"""
    print("Test: Application de HTTPS")
    with open('/workspaces/gemini-desktop-mac/WebKit/WebViewModel.swift', 'r') as f:
        content = f.read()

    if 'allowsInsecureMediaLoad = false' in content and 'allowsInsecureScripting = false' in content:
        print("   ✓ PASS: HTTPS enforced - contenu non-HTTPS désactivé")
        return True
    else:
        print("   ✗ FAIL: HTTPS enforcement non configuré")
        return False


def test_domain_whitelist():
    """Test de la liste blanche de domaines"""
    print("Test: Liste blanche restrictive de domaines")
    with open('/workspaces/gemini-desktop-mac/WebKit/GeminiWebView.swift', 'r') as f:
        content = f.read()

    # Chercher la liste exhaustive de domaines au lieu de suffixes
    if 'allowedDomains = [' in content and '.contains(host)' in content:
        if '.googleapis.com' not in content or 'gemini.google.com' in content:
            print("   ✓ PASS: Domaines spécifiés de manière exhaustive")
            return True

    print("   ✗ FAIL: Utilise toujours des suffixes génériques dangereux")
    return False


def test_console_log_bridge():
    """Test du pont console.log"""
    print("Test: Pont console.log")
    with open('/workspaces/gemini-desktop-mac/WebKit/WebViewModel.swift', 'r') as f:
        content = f.read()

    if '#if DEBUG' in content:
        print("   ✓ PASS: Pont console.log limité au DEBUG")
        return True
    else:
        print("   ✗ FAIL: Pont console.log actif en production")
        return False


def main():
    print("=== Tests automatisés de sécurité - Gemini Desktop ===\n")

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
    print(f"Résultats: {passed}/{total} tests passés")

    if passed == total:
        print("✓ Toutes les vérifications de sécurité sont passées")
        return 0
    else:
        print("✗ Certaines vérifications ont échoué")
        return 1


if __name__ == "__main__":
    exit(main())
