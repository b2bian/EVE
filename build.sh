#!/bin/bash
# EVE Cross-Platform App Build Script
# Automatically builds APK and DMG installers

set -e

PROJECT_ROOT="/Users/admin/Documents/AIAIAI/EVE"
BUILD_LOG="$PROJECT_ROOT/build.log"

log() {
    echo "[$(date +'%H:%M:%S')] $1" | tee -a "$BUILD_LOG"
}

log "=========================================="
log "EVE Cross-Platform App Build - Started"
log "=========================================="

# Step 1: Ensure Flutter is available
log "Step 1: Checking Flutter installation..."
if ! command -v flutter &> /dev/null; then
    log "ERROR: Flutter not found. Install Flutter first:"
    log "  brew install flutter"
    log "  OR: git clone https://github.com/flutter/flutter.git /opt/flutter"
    exit 1
fi
log "✓ Flutter found: $(flutter --version | head -1)"

# Step 2: Create Flutter project if it doesn't exist
log "Step 2: Setting up Flutter project..."
if [ ! -d "$PROJECT_ROOT/eve_app" ]; then
    cd "$PROJECT_ROOT"
    flutter create eve_app
    cd eve_app
    flutter config --enable-android
    flutter config --enable-macos
    flutter pub add http sqflite provider intl
else
    log "✓ Flutter project already exists"
fi

# Step 3: Copy code files into Flutter structure
log "Step 3: Integrating code files..."
mkdir -p "$PROJECT_ROOT/eve_app/lib/services"
mkdir -p "$PROJECT_ROOT/eve_app/lib/screens"
mkdir -p "$PROJECT_ROOT/eve_app/lib/widgets"

cp "$PROJECT_ROOT/eve_app_main.dart" "$PROJECT_ROOT/eve_app/lib/main.dart"
cp "$PROJECT_ROOT/eve_app_api_service.dart" "$PROJECT_ROOT/eve_app/lib/services/api_service.dart"
cp "$PROJECT_ROOT/eve_app_chat_screen.dart" "$PROJECT_ROOT/eve_app/lib/screens/chat_screen.dart"
cp "$PROJECT_ROOT/eve_app_message_bubble.dart" "$PROJECT_ROOT/eve_app/lib/widgets/message_bubble.dart"

log "✓ Code files integrated"

# Step 4: Build Android APK
log "Step 4: Building Android APK..."
log "This may take 5-15 minutes on first build..."
cd "$PROJECT_ROOT/eve_app"

flutter build apk --split-per-abi
APK_PATH="$PROJECT_ROOT/eve_app/build/app/outputs/flutter-apk"

if [ -d "$APK_PATH" ]; then
    log "✓ Android APK built successfully"
    log "  Location: $APK_PATH"
    ls -lh "$APK_PATH"/app-*.apk
else
    log "ERROR: APK build failed"
    exit 1
fi

# Step 5: Build macOS app
log "Step 5: Building macOS app..."
log "This may take 10-20 minutes..."
flutter build macos --release

MACOS_APP="$PROJECT_ROOT/eve_app/build/macos/Build/Products/Release/eve_app.app"

if [ -d "$MACOS_APP" ]; then
    log "✓ macOS app built successfully"
    log "  Location: $MACOS_APP"
else
    log "ERROR: macOS build failed"
    exit 1
fi

# Step 6: Create macOS DMG installer
log "Step 6: Creating macOS DMG installer..."
DMG_OUTPUT="$PROJECT_ROOT/EVE-macOS.dmg"

# Create temporary directory for DMG contents
TMP_DMG_DIR=$(mktemp -d)
cp -r "$MACOS_APP" "$TMP_DMG_DIR/"

# Create the DMG
hdiutil create -volname "EVE" \
    -srcfolder "$TMP_DMG_DIR" \
    -ov -format UDZO \
    "$DMG_OUTPUT"

rm -rf "$TMP_DMG_DIR"

if [ -f "$DMG_OUTPUT" ]; then
    log "✓ macOS DMG created successfully"
    log "  Location: $DMG_OUTPUT"
    ls -lh "$DMG_OUTPUT"
else
    log "ERROR: DMG creation failed"
    exit 1
fi

# Step 7: Copy APKs to deliverables location
log "Step 7: Organizing deliverables..."
mkdir -p "$PROJECT_ROOT/installers"

# Copy APKs
for apk in "$APK_PATH"/app-*.apk; do
    if [ -f "$apk" ]; then
        cp "$apk" "$PROJECT_ROOT/installers/"
        log "  ✓ Copied $(basename $apk)"
    fi
done

# Copy DMG
cp "$DMG_OUTPUT" "$PROJECT_ROOT/installers/EVE-macOS.dmg"
log "  ✓ Copied EVE-macOS.dmg"

# Summary
log "=========================================="
log "✓ BUILD COMPLETE - All installers ready!"
log "=========================================="
log ""
log "Deliverables:"
log "  Android APK: $PROJECT_ROOT/installers/"
log "  macOS DMG:   $PROJECT_ROOT/installers/EVE-macOS.dmg"
log ""
log "Installation instructions:"
log "  Android: Transfer APK to phone and install"
log "  macOS:   Download DMG, double-click to mount, drag EVE.app to Applications"
log ""
log "Build log saved to: $BUILD_LOG"
