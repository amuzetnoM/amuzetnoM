# 🚀 Quick Start Guide - Live GitHub Metrics

Get your GitHub metrics dashboard up and running in **5 minutes**!

## ⚡ Lightning Setup

### 1. Run Setup Script

```bash
./setup.sh
```

This will:
- ✅ Install dependencies
- ✅ Verify Python installation
- ✅ Test your GitHub token
- ✅ Run a test metrics collection

### 2. Enable GitHub Pages

1. Go to your repository on GitHub
2. Click **Settings** → **Pages**
3. Under "Source", select **`gh-pages`** branch
4. Click **Save**
5. Wait ~1 minute for deployment

Your live dashboard will be at:
```
https://YOUR_USERNAME.github.io/YOUR_REPO/live_metrics_dashboard.html
```

### 3. Trigger First Update

1. Go to **Actions** tab
2. Click **"Update GitHub Metrics"**
3. Click **"Run workflow"** → **"Run workflow"**
4. Wait 2-3 minutes for completion

### 4. Done! 🎉

Your metrics will now:
- ✅ Update automatically every 6 hours
- ✅ Be accessible 24/7 via GitHub Pages
- ✅ Be available as downloadable files
- ✅ Work without requiring login

## 🌐 Access Your Metrics

Once setup is complete, you can access your metrics at:

### Live Dashboard (Recommended)
```
https://YOUR_USERNAME.github.io/YOUR_REPO/live_metrics_dashboard.html
```

### Download Files
- JSON: `https://YOUR_USERNAME.github.io/YOUR_REPO/github_metrics.json`
- CSV: `https://YOUR_USERNAME.github.io/YOUR_REPO/github_metrics.csv`
- Report: `https://YOUR_USERNAME.github.io/YOUR_REPO/github_metrics_report.html`

## 🔐 Token Setup (First Time Only)

### Create GitHub Token

1. Visit: https://github.com/settings/tokens/new
2. Give it a name: "GitHub Metrics Tracker"
3. Select scopes:
   - ✅ `repo` (Full control of private repositories)
   - ✅ `read:user` (Read user profile data)
   - ✅ `read:org` (Read org data)
   - ✅ `security_events` (Security alerts)
4. Click **Generate token**
5. Copy the token (you won't see it again!)

### Set Token

**For local testing:**
```bash
export GITHUB_TOKEN='your_token_here'
```

**For GitHub Actions (automatic):**
The workflow uses `GITHUB_TOKEN` automatically - no setup needed!

### Optional: Gist Auto-Update

To auto-update a gist:

1. Create another token with `gist` scope
2. Go to repository **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `GIST_TOKEN`
5. Value: your gist token
6. Click **Add secret**

## 📅 Update Schedule

By default, metrics update:
- ⏰ Every 6 hours (00:00, 06:00, 12:00, 18:00 UTC)
- 🔄 On push to main branch (workflow changes only)
- 🎯 Manual trigger anytime via Actions tab

### Change Update Frequency

Edit `.github/workflows/update-metrics.yml`:

```yaml
schedule:
  - cron: '0 */3 * * *'  # Every 3 hours
  # OR
  - cron: '0 0 * * *'    # Daily at midnight
  # OR
  - cron: '0 */12 * * *' # Every 12 hours
```

## 🧪 Test Locally

Run the tracker manually:

```bash
# Track your repos
python3 github_metrics_tracker.py

# Track specific user
python3 github_metrics_tracker.py --username amuzetnoM

# JSON only
python3 github_metrics_tracker.py --format json

# Custom output name
python3 github_metrics_tracker.py --output my_metrics
```

## 📊 What You Get

### Metrics Tracked (ALL GitHub Metrics!)

✅ **Basic**: Stars, forks, watchers, size, language  
✅ **Code**: Commits, additions, deletions, frequency  
✅ **Community**: Contributors, participation, health  
✅ **Issues**: Open/closed issues and PRs  
✅ **Releases**: Versions, downloads, dates  
✅ **Security**: Vulnerabilities, alerts, dependencies  
✅ **Traffic**: Views, clones, referrers (if you have access)  
✅ **Workflows**: CI/CD metrics, success rates  
✅ **Custom**: Age, activity, popularity, engagement  

### Output Formats

1. **JSON** - Complete structured data
2. **CSV** - Spreadsheet-ready format
3. **HTML Report** - Detailed static report
4. **Live Dashboard** - Interactive real-time dashboard

## 🛠️ Troubleshooting

### "Python not found"
```bash
# Install Python 3.7+
# macOS: brew install python3
# Ubuntu: sudo apt install python3 python3-pip
# Windows: Download from python.org
```

### "Permission denied: ./setup.sh"
```bash
chmod +x setup.sh
./setup.sh
```

### "Rate limit exceeded"
You need a GitHub token for higher rate limits (5000/hour vs 60/hour).
See "Token Setup" above.

### "Workflow not running"
1. Check that Actions are enabled: Settings → Actions → Allow all actions
2. Verify workflow file is on main branch
3. Check for YAML syntax errors

### "Pages not deploying"
1. Enable Pages: Settings → Pages → Source: gh-pages
2. Wait 2-5 minutes after first workflow run
3. Check Pages build status in Settings → Pages

## 🎯 Example URLs

Replace `YOUR_USERNAME` and `YOUR_REPO`:

```
Live Dashboard:
https://YOUR_USERNAME.github.io/YOUR_REPO/live_metrics_dashboard.html

JSON Data:
https://YOUR_USERNAME.github.io/YOUR_REPO/github_metrics.json

CSV Data:
https://YOUR_USERNAME.github.io/YOUR_REPO/github_metrics.csv

Full Report:
https://YOUR_USERNAME.github.io/YOUR_REPO/github_metrics_report.html
```

## 🔗 Embedding in Your Site

### As IFrame

```html
<iframe 
  src="https://YOUR_USERNAME.github.io/YOUR_REPO/live_metrics_dashboard.html"
  width="100%" 
  height="800px" 
  frameborder="0"
  style="border: none; border-radius: 8px;">
</iframe>
```

### Fetch Data with JavaScript

```javascript
fetch('https://YOUR_USERNAME.github.io/YOUR_REPO/github_metrics.json')
  .then(res => res.json())
  .then(data => {
    console.log('Total Stars:', data.summary.total_stars);
    console.log('Total Repos:', data.summary.total_repositories);
  });
```

### Fetch Data with Python

```python
import requests

url = 'https://YOUR_USERNAME.github.io/YOUR_REPO/github_metrics.json'
metrics = requests.get(url).json()

print(f"Total Stars: {metrics['summary']['total_stars']}")
print(f"Total Repos: {metrics['summary']['total_repositories']}")
```

## 📚 Full Documentation

For complete details, see:
- **[AUTO_UPDATE_SETUP.md](AUTO_UPDATE_SETUP.md)** - Full setup guide
- **[GITHUB_METRICS_TRACKER_README.md](GITHUB_METRICS_TRACKER_README.md)** - Complete API documentation

## 💡 Pro Tips

1. **Bookmark your dashboard** for quick access
2. **Check Actions tab** to monitor updates
3. **View commit history** to see metrics over time
4. **Share the dashboard URL** - it's public and always live
5. **Download CSV** to analyze trends in Excel/Sheets

## ✨ That's It!

You now have a **fully automated, always-live GitHub metrics dashboard** that:
- ✅ Updates every 6 hours automatically
- ✅ Tracks every GitHub metric
- ✅ Works without login
- ✅ Accessible 24/7
- ✅ Multiple formats (JSON, CSV, HTML)
- ✅ Free to run

**Happy tracking! 📊🚀**
