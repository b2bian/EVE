#!/bin/bash

# EVE App - Build Script for macOS 14.0+ / Linux / Windows 10+
# This script can be run on a machine with Flutter 3.0+ installed
# It will build both APK (Android) and DMG (macOS) packages

set -e

echo "=========================================="
echo "EVE Cross-Platform App Builder"
echo "=========================================="
echo ""
echo "Requirements:"
echo "  - macOS 14.0+ OR Linux OR Windows 10+"
echo "  - Flutter 3.0.0+ installed"
echo "  - Xcode 14.0+ (for macOS builds)"
echo "  - Android SDK (for APK builds)"
echo ""

# Check Flutter
if ! command -v flutter &> /dev/null; then
    echo "❌ Flutter not found. Install from: https://flutter.dev/docs/get-started/install"
    exit 1
fi

echo "✓ Flutter found: $(flutter --version | head -1)"
echo ""

# Detect OS
OS="unknown"
if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
    OS="windows"
fi

echo "Detected OS: $OS"
echo ""

# Ensure we're in the right directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Create flutter project if it doesn't exist
if [ ! -d "eve_app" ]; then
    echo "📱 Creating Flutter project..."
    flutter create eve_app --org com.aiaiai --project-name eve_app
    cd eve_app
else
    cd eve_app
fi

echo "📦 Getting dependencies..."
flutter pub get

echo "🔨 Building..."

# Build APK
if [ "$OS" = "linux" ] || [ "$OS" = "macos" ] || [ "$OS" = "windows" ]; then
    echo ""
    echo "Building Android APK..."
    flutter build apk --release
    
    if [ -f "build/app/outputs/flutter-app.apk" ]; then
        echo "✓ APK built successfully!"
        echo "  Location: build/app/outputs/flutter-app.apk"
        mkdir -p ../installers
        cp build/app/outputs/flutter-app.apk ../installers/EVE-Android.apk
        echo "  Copied to: ../installers/EVE-Android.apk"
    fi
fi

# Build macOS app (only on macOS)
if [ "$OS" = "macos" ]; then
    echo ""
    echo "Building macOS app..."
    flutter build macos --release
    
    if [ -d "build/macos/Build/Products/Release/eve_app.app" ]; then
        echo "✓ macOS app built successfully!"
        
        # Create DMG
        echo "Creating DMG installer..."
        mkdir -p ../installers
        
        # Use hdiutil to create DMG
        hdiutil create -volname "EVE" \
                      -srcfolder build/macos/Build/Products/Release/eve_app.app \
                      -ov -format UDZO ../installers/EVE-macOS.dmg
        
        echo "✓ DMG created successfully!"
        echo "  Location: ../installers/EVE-macOS.dmg"
    fi
fi

echo ""
echo "=========================================="
echo "Build Complete!"
echo "=========================================="
echo ""
echo "📦 Output files:"
ls -lh ../installers/ 2>/dev/null || echo "  (No installers created)"
echo ""
echo "Next steps:"
echo "  1. APK: Install on Android device or emulator"
echo "  2. DMG: Double-click to mount and drag app to Applications folder"
echo ""
