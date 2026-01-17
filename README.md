<p align="center">
<img src="https://img.shields.io/badge/Python-111111?style=for-the-badge&logo=python&logoColor=white"/><img src="https://img.shields.io/badge/C++-111111?style=for-the-badge&logo=cplusplus&logoColor=white"/><img src="https://img.shields.io/badge/TS%20%2F%20JS-111111?style=for-the-badge&logo=typescript&logoColor=white"/><img src="https://img.shields.io/badge/Solidity-111111?style=for-the-badge&logo=solidity&logoColor=white"/>
</p>

<p align="center">
<img src="https://img.shields.io/badge/Linux-111111?style=for-the-badge&logo=linux&logoColor=white"/><img src="https://img.shields.io/badge/Windows-111111?style=for-the-badge&logo=windows&logoColor=white"/><img src="https://img.shields.io/badge/Android-111111?style=for-the-badge&logo=android&logoColor=white"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/VS%20Code-111111?style=for-the-badge&logo=visualstudiocode&logoColor=white" />
  &nbsp;&nbsp;
  <img src="https://img.shields.io/badge/Antigravity-111111?style=for-the-badge" />
</p>

---

# 📊 Live GitHub Metrics Dashboard

[![Auto-Update](https://img.shields.io/badge/Auto--Update-Every%206%20Hours-brightgreen?style=flat-square)](https://github.com/amuzetnoM/amuzetnoM/actions)
[![Always Live](https://img.shields.io/badge/Status-Always%20Live-success?style=flat-square)](https://amuzetnom.github.io/amuzetnoM/live_metrics_dashboard.html)
[![GitHub Pages](https://img.shields.io/badge/Hosted%20on-GitHub%20Pages-blue?style=flat-square)](https://pages.github.com/)

> **Comprehensive, exhaustive GitHub metrics tracking system** that automatically updates every 6 hours and is always accessible, whether you're logged in or not.

## 🌟 Features

✅ **Tracks ALL GitHub Metrics** - Every metric GitHub offers, plus custom analytics  
✅ **Auto-Updates Every 6 Hours** - Powered by GitHub Actions  
✅ **Always Live & Accessible** - No login required via GitHub Pages  
✅ **Multiple Formats** - JSON, CSV, and beautiful HTML reports  
✅ **Auto-Published to Gist** - Share metrics easily  
✅ **Comprehensive Documentation** - Complete setup guides included  

## 🚀 Quick Start

```bash
# 1. Run setup
./setup.sh

# 2. Enable GitHub Pages (Settings → Pages → Source: gh-pages)

# 3. Trigger first run (Actions → Update GitHub Metrics → Run workflow)

# 4. Done! Your dashboard is live at:
# https://YOUR_USERNAME.github.io/YOUR_REPO/live_metrics_dashboard.html
```

📖 **[Full Quick Start Guide →](QUICKSTART.md)**

## 🎯 What Gets Tracked

The system tracks **every metric GitHub offers**, categorized comprehensively:

### Core Metrics
- 📊 **Repository Stats**: Stars, forks, watchers, size, language
- 💻 **Code Metrics**: Commits, LOC added/deleted, code frequency
- 👥 **Community**: Contributors, participation, community health
- 🔧 **Issues & PRs**: Open/closed counts, merge rates
- 🚀 **Releases**: Version history, download stats
- 🌳 **Branches & Tags**: Branch counts, protection status

### Advanced Metrics
- 📈 **Traffic**: Views, clones, referrers (when you have access)
- 🔒 **Security**: Dependabot alerts, code scanning, vulnerabilities
- ⚙️ **GitHub Actions**: Workflow metrics, success rates
- 🎨 **Custom Analytics**: Age, activity status, engagement scores

📖 **[Complete Metrics List →](GITHUB_METRICS_TRACKER_README.md)**

## 📊 Access Your Metrics

### 🌐 Live Dashboard
Your metrics are always available at:
```
https://YOUR_USERNAME.github.io/YOUR_REPO/live_metrics_dashboard.html
```

### 📥 Download Files
- **JSON**: Complete structured data
- **CSV**: Spreadsheet-ready format
- **HTML**: Detailed static report

### 🔗 GitHub Gist
Auto-updated gist with all formats (check Actions logs for URL after first run)

## 🤖 Auto-Update System

The system runs automatically:
- ⏰ **Every 6 hours** (00:00, 06:00, 12:00, 18:00 UTC)
- 🔄 **On push to main** (for workflow changes)
- 🎯 **Manual trigger** available anytime

**No login required** - Metrics are always live and accessible!

## 📁 Project Structure

```
📦 GitHub Metrics Tracker
├── 📄 github_metrics_tracker.py          # Main tracking script
├── 🌐 live_metrics_dashboard.html        # Live web dashboard
├── 📋 requirements.txt                   # Dependencies
├── 🔧 setup.sh                          # Setup script
├── 📚 QUICKSTART.md                     # Quick start guide
├── 📖 GITHUB_METRICS_TRACKER_README.md  # Complete documentation
├── 🔄 AUTO_UPDATE_SETUP.md              # Auto-update guide
├── 📊 sample_github_metrics.json        # Sample output
└── .github/
    ├── workflows/
    │   └── update-metrics.yml           # Auto-update workflow
    └── scripts/
        └── update_gist.py               # Gist updater
```

## 📚 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[GITHUB_METRICS_TRACKER_README.md](GITHUB_METRICS_TRACKER_README.md)** - Complete feature documentation
- **[AUTO_UPDATE_SETUP.md](AUTO_UPDATE_SETUP.md)** - Auto-update system guide
- **[sample_github_metrics.json](sample_github_metrics.json)** - Example output

## 🛠️ Requirements

- Python 3.7+
- GitHub account
- GitHub Personal Access Token (for enhanced features)

## 💡 Use Cases

- 📊 **Portfolio Analytics** - Showcase your GitHub presence
- 📈 **Project Tracking** - Monitor repository health
- 🔍 **Security Auditing** - Track vulnerabilities
- 🎯 **Team Dashboards** - Organizational insights
- 📱 **Public Stats** - Share via gist or embeddable dashboard

## 🎨 Embed in Your Site

```html
<iframe 
  src="https://YOUR_USERNAME.github.io/YOUR_REPO/live_metrics_dashboard.html"
  width="100%" 
  height="800px">
</iframe>
```

## 🔐 Security & Privacy

- ✅ No data sent to external services
- ✅ All processing done via GitHub Actions
- ✅ Secure token handling via GitHub Secrets
- ✅ Public metrics only (unless you configure for private repos)

## 📊 Example Output

See **[sample_github_metrics.json](sample_github_metrics.json)** for a complete example of tracked metrics.

## 🤝 Contributing

Contributions welcome! This tool tracks every GitHub metric available. If you find something missing, please open an issue.

## 📄 License

This project is provided as-is for tracking GitHub metrics. Use responsibly and in accordance with GitHub's Terms of Service.

---

<p align="center">
  <strong>🚀 Now your GitHub metrics are always live, auto-updated, and accessible 24/7!</strong>
</p>
