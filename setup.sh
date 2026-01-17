#!/bin/bash
# Setup script for GitHub Metrics Auto-Update System

set -e

echo "🚀 GitHub Metrics Auto-Update Setup"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.7 or higher.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python 3 detected${NC}"

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${BLUE}Python version: $PYTHON_VERSION${NC}"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}⚠️  Not in a virtual environment. Installing with --user flag for safety.${NC}"
    pip3 install -q --user -r requirements.txt
else
    echo -e "${GREEN}✅ Virtual environment detected${NC}"
    pip3 install -q -r requirements.txt
fi

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Dependencies installed${NC}"
else
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi

# Check for GitHub token
echo ""
if [ -z "$GITHUB_TOKEN" ]; then
    echo -e "${YELLOW}⚠️  No GITHUB_TOKEN environment variable found${NC}"
    echo ""
    echo "To use this tool, you need a GitHub Personal Access Token."
    echo ""
    echo "Steps to create one:"
    echo "1. Go to: https://github.com/settings/tokens/new"
    echo "2. Select scopes: repo, read:user, read:org, security_events"
    echo "3. Generate token and copy it"
    echo ""
    read -p "Enter your GitHub token (or press Enter to skip): " token
    
    if [ ! -z "$token" ]; then
        export GITHUB_TOKEN="$token"
        echo -e "${GREEN}✅ Token set for this session${NC}"
        echo ""
        echo "To make it permanent, add this to your ~/.bashrc or ~/.zshrc:"
        echo "export GITHUB_TOKEN='$token'"
    fi
else
    echo -e "${GREEN}✅ GITHUB_TOKEN found${NC}"
fi

# Test run
echo ""
echo "🧪 Running test to verify setup..."
echo ""

# Get current username
USERNAME=$(git config user.name 2>/dev/null || echo "")

if [ -z "$USERNAME" ]; then
    read -p "Enter GitHub username to track (or press Enter for authenticated user): " USERNAME
fi

# Run the tracker
echo ""
echo "Running metrics tracker..."
if [ ! -z "$USERNAME" ]; then
    python3 github_metrics_tracker.py --username "$USERNAME" --output test_metrics --format json
else
    python3 github_metrics_tracker.py --output test_metrics --format json
fi

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✅ Setup complete!${NC}"
    echo ""
    echo "Generated files:"
    ls -lh test_metrics.json 2>/dev/null && rm test_metrics.json
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo -e "${BLUE}📚 Next Steps:${NC}"
    echo ""
    echo "1️⃣  Enable GitHub Actions:"
    echo "   - Go to your repository → Actions tab"
    echo "   - Enable workflows if not already enabled"
    echo ""
    echo "2️⃣  (Optional) Setup Gist Auto-Update:"
    echo "   - Create a token with 'gist' scope"
    echo "   - Add as repository secret: GIST_TOKEN"
    echo ""
    echo "3️⃣  Enable GitHub Pages:"
    echo "   - Go to Settings → Pages"
    echo "   - Set source to 'gh-pages' branch"
    echo "   - Your dashboard will be at:"
    echo "     https://YOUR_USERNAME.github.io/YOUR_REPO/live_metrics_dashboard.html"
    echo ""
    echo "4️⃣  Trigger First Run:"
    echo "   - Go to Actions → 'Update GitHub Metrics'"
    echo "   - Click 'Run workflow'"
    echo ""
    echo "5️⃣  Metrics will auto-update every 6 hours! 🎉"
    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""
    echo "📖 For more information:"
    echo "   - AUTO_UPDATE_SETUP.md - Setup guide"
    echo "   - GITHUB_METRICS_TRACKER_README.md - Complete documentation"
    echo ""
else
    echo -e "${RED}❌ Test run failed. Please check your token and try again.${NC}"
    exit 1
fi
