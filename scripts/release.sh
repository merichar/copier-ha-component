#!/usr/bin/env bash
# Release script for copier-ha-component template
# Usage: ./scripts/release.sh <version>

set -e

# Get latest tag for usage message
LATEST_TAG=$(git tag --sort=-v:refname | head -n1 || echo "")

if [ $# -ne 1 ]; then
    echo "Usage: $0 <version>"
    echo "Example: $0 1.0.0"
    if [ -z "$LATEST_TAG" ]; then
        echo "Current latest tag: none"
    else
        echo "Current latest tag: $LATEST_TAG"
    fi
    exit 1
fi

VERSION=$1

# Validate semantic versioning format
if ! [[ $VERSION =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    echo "Error: Version must be in X.Y.Z format (e.g., 1.2.3)"
    exit 1
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "Error: You have uncommitted changes. Commit or stash them first."
    exit 1
fi

# Check if tag already exists
if git rev-parse "v$VERSION" >/dev/null 2>&1; then
    echo "Error: Tag v$VERSION already exists"
    exit 1
fi

# Get latest tag and compare versions
LATEST_TAG=$(git tag --sort=-v:refname | head -n1 | sed 's/^v//' || echo "0.0.0")

# Function to compare semantic versions
version_gt() {
    # Split versions into arrays
    IFS='.' read -ra V1 <<< "$1"
    IFS='.' read -ra V2 <<< "$2"
    
    # Compare major
    if [ "${V1[0]}" -gt "${V2[0]}" ]; then return 0; fi
    if [ "${V1[0]}" -lt "${V2[0]}" ]; then return 1; fi
    
    # Compare minor
    if [ "${V1[1]}" -gt "${V2[1]}" ]; then return 0; fi
    if [ "${V1[1]}" -lt "${V2[1]}" ]; then return 1; fi
    
    # Compare patch
    if [ "${V1[2]}" -gt "${V2[2]}" ]; then return 0; fi
    
    return 1
}

if ! version_gt "$VERSION" "$LATEST_TAG"; then
    echo "Error: New version ($VERSION) must be greater than latest tag (v$LATEST_TAG)"
    echo "Latest tag: v$LATEST_TAG"
    echo "Provided:   $VERSION"
    exit 1
fi

echo "Releasing template v$VERSION (previous: v$LATEST_TAG)"
echo ""

# Create annotated tag
git tag -a "v$VERSION" -m "Release template v$VERSION"

echo "Tagged v$VERSION"
echo ""
echo "Push with:"
echo "  git push origin main --tags"
echo ""
read -p "Push now? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push origin main --tags
    echo "Released template v$VERSION"
else
    echo "Push cancelled. Run manually when ready:"
    echo "  git push origin main --tags"
fi
