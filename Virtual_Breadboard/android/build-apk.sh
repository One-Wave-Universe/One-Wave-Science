#!/usr/bin/env bash
# Builds VirtualBreadboardSimulator.apk from the smali source using only
# tools packaged in Ubuntu/Debian's apt repos (no Android Studio, no
# Google SDK download required):
#
#   sudo apt-get install --no-install-recommends \
#     aapt zipalign apksigner android-sdk-platform-23 libsmali-java
#
# Usage: ./build-apk.sh
set -euo pipefail
cd "$(dirname "$0")"

ANDROID_JAR=/usr/lib/android-sdk/platforms/android-23/android.jar
BUILD=build
KEYSTORE=$BUILD/release.keystore
APK_UNSIGNED=$BUILD/app-with-dex.apk
APK_ALIGNED=$BUILD/app-aligned.apk
APK_OUT=$BUILD/VirtualBreadboardSimulator.apk

rm -rf "$BUILD" assets
mkdir -p "$BUILD" assets/js

echo "==> copying web app into assets/"
cp ../index.html ../style.css assets/
cp ../js/*.js assets/js/

echo "==> assembling smali -> classes.dex"
smali assemble -a 23 -o "$BUILD/classes.dex" smali

echo "==> aapt package (manifest + assets)"
aapt package -f -M AndroidManifest.xml -A assets -I "$ANDROID_JAR" -F "$APK_UNSIGNED"

echo "==> adding classes.dex"
( cd "$BUILD" && zip -j "$(basename "$APK_UNSIGNED")" classes.dex )

echo "==> zipalign"
zipalign -f -p 4 "$APK_UNSIGNED" "$APK_ALIGNED"

if [ ! -f "$KEYSTORE" ]; then
  echo "==> generating a signing key (self-signed, for sideloading)"
  keytool -genkeypair -v -keystore "$KEYSTORE" -alias virtualbreadboard \
    -keyalg RSA -keysize 2048 -validity 10000 \
    -storepass breadboard123 -keypass breadboard123 \
    -dname "CN=Virtual Breadboard Simulator, OU=One Wave Science, O=One Wave Science, L=Unknown, S=Unknown, C=US"
fi

echo "==> signing"
apksigner sign --ks "$KEYSTORE" --ks-pass pass:breadboard123 --ks-key-alias virtualbreadboard \
  --out "$APK_OUT" "$APK_ALIGNED"

apksigner verify "$APK_OUT"
echo "==> built $APK_OUT"
