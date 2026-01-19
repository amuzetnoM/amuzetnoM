# 🔄 Auto-Updating GitHub Metrics System

This repository includes an **automated, always-live GitHub metrics tracking system** that updates continuously without requiring login.

## 🌟 Features

### ✅ Always Live
- Metrics are automatically updated every 6 hours
- No manual intervention required
- Works whether you're logged in or not

### 🤖 Fully Automated
- GitHub Actions workflow runs on schedule
- Updates tracked via Git commits
- Publishes to GitHub Gist
- Deploys to GitHub Pages

### 🌐 Multiple Access Points
1. **Live Dashboard**: Hosted on GitHub Pages (always accessible)
2. **GitHub Gist**: Auto-updated gist with all metrics files
3. **Repository Files**: Committed directly to the repo

## 📊 What Gets Tracked

The system tracks **every metric GitHub offers**, including:
- Repository statistics (stars, forks, watchers)
- Code metrics (commits, lines of code, languages)
- Community metrics (contributors, issues, PRs)
- Security metrics (vulnerabilities, alerts)
- Traffic metrics (views, clones)
- GitHub Actions metrics
- Custom calculated metrics

For complete details, see [GITHUB_METRICS_TRACKER_README.md](GITHUB_METRICS_TRACKER_README.md)

## 🚀 Quick Setup

### 1. Enable GitHub Actions

The workflow is already configured in `.github/workflows/update-metrics.yml`

### 2. (Optional) Create a Gist Token

For automatic gist updates:

1. Go to: https://github.com/settings/tokens/new
2. Create token with `gist` scope
3. Add to repository secrets as `GIST_TOKEN`

**Note**: The default `GITHUB_TOKEN` works for most features except gist creation.

### 3. Enable GitHub Pages

1. Go to repository Settings → Pages
2. Set source to `gh-pages` branch
3. Your live dashboard will be at: `https://yourusername.github.io/repository-name/live_metrics_dashboard.html`

### 4. Manual Trigger (First Run)

Go to Actions tab → "Update GitHub Metrics" → Run workflow

## 📅 Update Schedule

The metrics update automatically:
- ⏰ **Every 6 hours** (0:00, 6:00, 12:00, 18:00 UTC)
- 🔄 **On every push** to main branch (for workflow changes)
- 🎯 **Manual trigger** available in Actions tab

## 🔗 Access Your Metrics

### Option 1: Live Dashboard (Recommended)
Visit: `https://yourusername.github.io/repository-name/live_metrics_dashboard.html`

Features:
- Real-time countdown to next update
- Interactive visualizations
- Auto-refresh every 6 hours
- Download links for all formats

### Option 2: GitHub Gist
After first run, check the workflow logs for your gist URL.
The gist will be automatically updated on each run.

### Option 3: Repository Files
Download directly from the repository:
- `github_metrics.json` - Complete data
- `github_metrics.csv` - Spreadsheet format  
- `github_metrics_report.html` - Detailed report

## 📁 File Structure

```
.
├── github_metrics_tracker.py          # Main tracking script
├── live_metrics_dashboard.html        # Live web dashboard
├── requirements.txt                   # Python dependencies
├── .github/
│   ├── workflows/
│   │   └── update-metrics.yml        # GitHub Actions workflow
│   └── scripts/
│       └── update_gist.py            # Gist update script
├── github_metrics.json               # Generated: JSON data
├── github_metrics.csv                # Generated: CSV data
└── github_metrics_report.html        # Generated: Full report
```

## 🔧 Configuration

### Change Update Frequency

Edit `.github/workflows/update-metrics.yml`:

```yaml
schedule:
  - cron: '0 */6 * * *'  # Every 6 hours (default)
  # - cron: '0 */3 * * *'  # Every 3 hours
  # - cron: '0 0 * * *'    # Daily at midnight
  # - cron: '0 0 * * 0'    # Weekly on Sunday
```

### Track Different User

Edit the workflow to add `--username` parameter:

```yaml
- name: Run metrics tracker
  run: |
    python github_metrics_tracker.py --username different-user --output github_metrics --format all
```

### Customize Output

Modify the script parameters in the workflow:

```yaml
# JSON only
python github_metrics_tracker.py --format json

# Different output name
python github_metrics_tracker.py --output my_custom_name
```

## 🔐 Security & Permissions

### Required Permissions

The workflow needs:
- `contents: write` - To commit metrics files
- `pages: write` - To deploy to GitHub Pages
- `id-token: write` - For Pages deployment

These are already configured in the workflow file.

### GitHub Token

The workflow uses `GITHUB_TOKEN` automatically provided by GitHub Actions. This token:
- Has access to your public and private repositories
- Resets after each workflow run
- Is never exposed in logs
- Rate limit: 5,000 requests/hour

### Optional: Gist Token

For gist updates, add a personal access token:
1. Create token with `gist` scope
2. Add as repository secret: `GIST_TOKEN`
3. Token is used securely via GitHub Secrets

## 📊 Monitoring

### Check Workflow Status

1. Go to repository **Actions** tab
2. Click on "Update GitHub Metrics" workflow
3. View run history and logs

### View Metrics History

All metrics updates are committed to the repository:
```bash
git log --oneline -- github_metrics.json
```

### Debug Issues

Workflow logs show:
- Each repository being tracked
- Metrics collection progress
- Any API errors or rate limits
- Gist creation/update status
- Deployment status

## 🛠️ Troubleshooting

### Workflow Not Running

- Check that Actions are enabled in repository settings
- Verify the workflow file is on the main branch
- Check for syntax errors in the workflow YAML

### Rate Limiting

If you have many repositories (100+):
- The workflow might take longer
- GitHub API limits: 5,000 requests/hour with token
- The script handles rate limits automatically

### Gist Not Updating

- Ensure `GIST_TOKEN` is set in repository secrets
- Check workflow logs for gist-related errors
- Verify token has `gist` scope

### Pages Not Deploying

- Enable GitHub Pages in repository settings
- Set source to `gh-pages` branch
- Wait a few minutes after first deployment
- Check Pages build status in repository settings

## 🎯 Use Cases

1. **Personal Portfolio**: Showcase GitHub activity on your website
2. **Team Dashboard**: Monitor organization repositories
3. **Project Tracking**: Keep tabs on multiple projects
4. **Historical Analysis**: Track growth over time via Git history
5. **Public Stats**: Share accomplishments via gist
6. **Automated Reporting**: Receive metrics without manual work

## 🚀 Advanced Usage

### Embed in Your Website

The live dashboard can be embedded as an iframe:

```html
<iframe 
  src="https://yourusername.github.io/repository-name/live_metrics_dashboard.html"
  width="100%" 
  height="800px" 
  frameborder="0">
</iframe>
```

### API Access

Fetch metrics programmatically:

```javascript
// From GitHub Pages
fetch('https://yourusername.github.io/repository-name/github_metrics.json')
  .then(res => res.json())
  .then(data => console.log(data));
```

```python
# From Python
import requests
response = requests.get('https://yourusername.github.io/repository-name/github_metrics.json')
metrics = response.json()
print(f"Total stars: {metrics['summary']['total_stars']}")
```

### Webhook Integration

Use GitHub Actions to trigger webhooks when metrics update:

```yaml
- name: Send webhook
  run: |
    curl -X POST https://your-webhook-url.com/metrics \
      -H "Content-Type: application/json" \
      -d @github_metrics.json
```

## 📈 Metrics History

Since metrics are committed to Git, you can:

```bash
# View metrics from 30 days ago
git show 'main@{30 days ago}':github_metrics.json

# Compare with current
git diff 'main@{30 days ago}' main -- github_metrics.json

# Extract historical data
git log --format="%H %ci" --follow github_metrics.json | \
  while read hash date; do
    echo "$date"
    git show $hash:github_metrics.json | jq '.summary.total_stars'
  done
```

## 🎉 Benefits

✅ **No Manual Work**: Set it and forget it  
✅ **Always Current**: Updates automatically  
✅ **Always Accessible**: Multiple access points  
✅ **No Login Required**: Public dashboard works for everyone  
✅ **Version History**: Track changes over time via Git  
✅ **Multiple Formats**: JSON, CSV, HTML  
✅ **Comprehensive**: Every GitHub metric tracked  
✅ **Reliable**: GitHub Actions infrastructure  
✅ **Free**: Uses GitHub's free tier  

## 📚 Documentation

- [Complete Metrics Documentation](GITHUB_METRICS_TRACKER_README.md)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Pages Documentation](https://docs.github.com/en/pages)
- [GitHub API Documentation](https://docs.github.com/en/rest)

## 🤝 Contributing

To modify the tracking system:

1. Edit `github_metrics_tracker.py` for new metrics
2. Update `update-metrics.yml` for workflow changes
3. Modify `live_metrics_dashboard.html` for dashboard changes
4. Test locally before pushing

## 📄 License

This automated metrics system is provided as-is. Use responsibly and in accordance with GitHub's Terms of Service.

---

**🎯 Result**: Your GitHub metrics are now **always live, auto-updated, and accessible 24/7** without any login required!
