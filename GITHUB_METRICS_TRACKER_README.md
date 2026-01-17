# 📊 GitHub Metrics Tracker

A comprehensive, exhaustive GitHub metrics tracking tool that collects **ALL** available GitHub metrics across all your repositories, plus additional custom metrics not provided by GitHub's API.

## 🌟 Features

### **Exhaustive GitHub API Metrics Coverage**

This tool tracks every metric available through the GitHub API, organized into comprehensive categories:

#### 📦 **Repository Basic Metrics**
- Stars, forks, watchers, subscribers
- Repository size, visibility, and status
- Creation, update, and push timestamps
- License, topics, and homepage
- Feature flags (issues, wiki, pages, discussions, projects)
- Network count and more

#### 💻 **Code Metrics**
- Language statistics (bytes per language)
- Code frequency (additions/deletions over time)
- Total lines of code added/deleted
- Net lines of code
- Weekly code activity patterns

#### 👥 **Community & Contribution Metrics**
- Complete contributor list with contribution counts
- Commit activity (last year, weekly breakdown)
- Participation statistics (owner vs. community commits)
- Community health percentage
- Community profile completeness (README, CODE_OF_CONDUCT, CONTRIBUTING, etc.)

#### 🔧 **Issues & Pull Requests**
- Open/closed issue counts
- Open/closed/merged PR counts
- PR merge rate statistics
- Issue and PR filtering (excludes PRs from issues count)

#### 🚀 **Release & Deployment Metrics**
- Total release count
- Latest release information
- Release asset download counts
- Draft and prerelease statistics
- Release publishing dates

#### 🌳 **Branch & Tag Metrics**
- Total branch count
- Protected branch identification
- Complete branch listings
- Total tag count
- Latest tags

#### 📈 **Traffic Metrics** (requires repository access)
- Page views (count and unique visitors)
- Repository clones (count and unique cloners)
- Top referral sources
- Most popular repository paths
- Daily traffic breakdown

#### 🔒 **Security Metrics**
- Dependabot alerts (by severity and state)
- Code scanning alerts (by severity and state)
- Vulnerability alert status
- Critical security issue counts

#### ⚙️ **GitHub Actions/Workflows**
- Total workflow count
- Active workflow identification
- Workflow run statistics
- Success/failure rates per workflow
- Individual workflow performance metrics

### **🎯 Additional Custom Metrics**

Beyond GitHub's native metrics, this tool calculates:

- **Repository Age**: Days and years since creation
- **Activity Status**: Days since last push, active/inactive classification
- **Engagement Score**: Weighted popularity metric combining stars, forks, and watchers
- **Fork Ratio**: Fork-to-star ratio for collaboration analysis
- **Popularity Category**: Classification (highly_popular, popular, moderate, low)
- **Activity Patterns**: Custom analysis of repository health

### **📊 Comprehensive Summaries**

The tool generates aggregate statistics across all repositories:

- Total counts (repositories, stars, forks, watchers, contributors, releases)
- Language distribution (percentage and byte counts)
- Active vs. archived repository counts
- Public vs. private repository breakdown
- Forked repository identification
- Most starred repositories (top 10)
- Most forked repositories (top 10)
- Total commit activity
- Total code additions/deletions

### **📤 Multiple Export Formats**

Export your metrics in three formats:

1. **JSON**: Complete data structure with all metrics and nested details
2. **CSV**: Flattened data for spreadsheet analysis
3. **HTML**: Beautiful, interactive report with GitHub-style dark theme

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- `requests` library

### Install Dependencies

```bash
pip install requests
```

Or if you have a `requirements.txt`:

```bash
pip install -r requirements.txt
```

## 🔑 Authentication

### GitHub Personal Access Token

To use this tool effectively, you need a GitHub Personal Access Token (PAT) with appropriate permissions:

1. Go to GitHub Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
2. Generate a new token with these scopes:
   - `repo` (full control of private repositories)
   - `read:user` (read user profile data)
   - `read:org` (read organization data)
   - `security_events` (read security events - for vulnerability alerts)

3. Set your token as an environment variable:

```bash
export GITHUB_TOKEN='your_token_here'
```

Or pass it directly via the `--token` flag.

## 📖 Usage

### Basic Usage (Track Your Own Repositories)

```bash
python github_metrics_tracker.py
```

This will:
- Use the `GITHUB_TOKEN` environment variable
- Track all repositories for the authenticated user
- Generate JSON, CSV, and HTML reports

### Track Specific User

```bash
python github_metrics_tracker.py --username amuzetnoM
```

### Specify Output Format

```bash
# JSON only
python github_metrics_tracker.py --format json

# CSV only
python github_metrics_tracker.py --format csv

# HTML only
python github_metrics_tracker.py --format html

# All formats (default)
python github_metrics_tracker.py --format all
```

### Custom Output Filename

```bash
python github_metrics_tracker.py --output my_metrics
```

This will create:
- `my_metrics.json`
- `my_metrics.csv`
- `my_metrics_report.html`

### Complete Example

```bash
python github_metrics_tracker.py \
  --token ghp_yourTokenHere \
  --username amuzetnoM \
  --output amuzetnoM_github_stats \
  --format all
```

## 📋 Command-Line Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--token` | GitHub personal access token | `GITHUB_TOKEN` env var |
| `--username` | GitHub username to track | Authenticated user |
| `--output` | Output filename prefix | `github_metrics` |
| `--format` | Output format: `json`, `csv`, `html`, `all` | `all` |

## 📊 Output Files

### JSON Output (`github_metrics.json`)

Complete hierarchical data structure containing:
- User information
- All repository metrics (nested by category)
- Summary statistics
- Timestamp information

**Structure:**
```json
{
  "user_info": { ... },
  "repositories": [
    {
      "repository": "username/repo",
      "basic": { ... },
      "languages": { ... },
      "contributors": [ ... ],
      "commit_activity": { ... },
      "code_frequency": { ... },
      "issues": { ... },
      "pull_requests": { ... },
      "releases": { ... },
      "traffic": { ... },
      "security": { ... },
      "workflows": { ... },
      "custom": { ... }
    }
  ],
  "summary": { ... },
  "timestamp": "2026-01-17T19:46:00Z"
}
```

### CSV Output (`github_metrics.csv`)

Flattened spreadsheet with key metrics per repository:
- Repository name
- Stars, forks, watchers
- Open issues and PRs
- Primary language
- Size, contributors, commits
- Age and activity status
- Configuration flags

Perfect for:
- Excel/Google Sheets analysis
- Data visualization tools
- Quick comparisons

### HTML Report (`github_metrics_report.html`)

Beautiful, interactive HTML report featuring:
- GitHub-style dark theme
- Metric cards with hover effects
- User information section
- Repository overview with statistics
- Code statistics
- Language distribution chart
- Top starred repositories table
- Top forked repositories table
- Complete repository listing

**Open in any browser** for a comprehensive visual overview.

## 🔍 Metrics Categories Explained

### Basic Metrics
Core repository information including popularity metrics (stars, forks), repository settings, and configuration.

### Language Metrics
Distribution of programming languages used, measured in bytes and percentages across all repositories.

### Contributors
Everyone who has contributed to the repository, with their contribution counts.

### Commit Activity
Temporal analysis of commits, including weekly patterns and yearly totals.

### Code Frequency
Track how much code is being added vs. deleted over time - useful for understanding repository growth.

### Participation
Breakdown of commits by owner vs. community contributors.

### Issues & Pull Requests
Track the volume and status of issues and PRs to understand repository maintenance and collaboration.

### Releases
Version history and release cadence, including download statistics for release assets.

### Branches & Tags
Repository branch strategy and tagging practices.

### Traffic Metrics
*Requires push access* - Understand how people discover and interact with your repository.

### Community Profile
Assess how well-documented and welcoming your repository is to contributors.

### Security Metrics
Track security vulnerabilities and alerts across dependencies and code.

### Workflows
GitHub Actions performance and reliability metrics.

### Custom Metrics
Calculated insights like repository age, activity status, and engagement scores.

## 🎯 Use Cases

1. **Portfolio Analysis**: Showcase your GitHub presence with comprehensive statistics
2. **Project Management**: Track project health across multiple repositories
3. **Open Source Metrics**: Demonstrate community engagement and project activity
4. **Security Auditing**: Identify repositories with security vulnerabilities
5. **Code Quality Tracking**: Monitor commit activity and code changes over time
6. **Team Analytics**: Understand contributor patterns and collaboration
7. **Growth Tracking**: Watch your GitHub presence grow over time
8. **Job Applications**: Provide detailed metrics for your coding portfolio

## ⚠️ Rate Limiting

GitHub API has rate limits:
- **Authenticated**: 5,000 requests per hour
- **Unauthenticated**: 60 requests per hour

This tool:
- Automatically handles rate limiting
- Waits and retries when limits are reached
- Tracks a complete portfolio efficiently

For large portfolios (100+ repos), tracking may take several minutes.

## 🔐 Permissions & Privacy

### Required Permissions
- Public repository data: No token required (with rate limits)
- Private repositories: Token with `repo` scope
- Traffic data: Push access to repositories
- Security alerts: Token with `security_events` scope

### Privacy Notes
- The tool only accesses data you have permission to view
- No data is sent to external services
- All data is stored locally on your machine
- Token is never logged or stored

## 🛠️ Troubleshooting

### "Rate limit exceeded"
Wait for the rate limit to reset (shown in error message) or authenticate with a token for higher limits.

### "404 Not Found" for a repository
- Check that the repository name is correct
- Ensure you have access to private repositories (if applicable)
- Verify your token has appropriate permissions

### Missing traffic or security metrics
Some metrics require specific permissions:
- Traffic: Push access to the repository
- Security alerts: `security_events` scope in token

### Slow performance
For accounts with many repositories:
- The tool fetches comprehensive data for each repo
- Progress is shown in console
- Consider running overnight for 100+ repositories

## 🚀 Advanced Usage

### Use as a Python Module

```python
from github_metrics_tracker import GitHubMetricsTracker

# Initialize
tracker = GitHubMetricsTracker(token='your_token', username='amuzetnoM')

# Track all repositories
metrics = tracker.track_all_repositories()

# Access specific data
print(f"Total stars: {metrics['summary']['total_stars']}")

# Export
tracker.export_to_json('my_metrics.json')
tracker.export_to_csv('my_metrics.csv')
tracker.generate_html_report('my_report.html')
```

### Track Single Repository

```python
tracker = GitHubMetricsTracker(token='your_token')
repo_metrics = tracker.collect_all_metrics_for_repo('username/repository')
print(json.dumps(repo_metrics, indent=2))
```

## 📚 Complete Metrics List

Here's every metric tracked by this tool:

**Repository Basics**: name, full_name, description, private, fork, created_at, updated_at, pushed_at, size, stargazers_count, watchers_count, forks_count, open_issues_count, default_branch, language, has_issues, has_projects, has_downloads, has_wiki, has_pages, has_discussions, archived, disabled, visibility, license, topics, homepage, network_count, subscribers_count

**Languages**: All languages with byte counts

**Contributors**: login, contributions, type (for all contributors)

**Commit Activity**: total_commits_last_year, weekly_activity (52 weeks)

**Code Frequency**: total_additions, total_deletions, net_lines, weekly_data

**Participation**: owner_commits, all_commits, community_commits

**Issues**: open_count, closed_count, total_count

**Pull Requests**: open_count, closed_count, merged_count, total_count, merge_rate

**Releases**: total_releases, latest_release, latest_release_date, total_asset_downloads, release details

**Branches**: total_branches, branch names, protected status

**Tags**: total_tags, tag names

**Traffic**: views (count, uniques, daily), clones (count, uniques, daily), top_referrers, top_paths

**Community**: health_percentage, files (code_of_conduct, contributing, issue_template, pull_request_template, license, readme)

**Security**: dependabot_alerts (total, by_severity, by_state, open_critical), code_scanning_alerts (total, by_severity, by_state)

**Workflows**: total_workflows, active_workflows, workflow details (name, state, path, runs, success_rate)

**Custom**: age_days, age_years, days_since_last_push, is_active, engagement_score, fork_ratio, popularity

## 🤝 Contributing

This tool is designed to be comprehensive and exhaustive. If you find any GitHub metrics that aren't being tracked, please let us know!

## 📄 License

This tool is provided as-is for tracking GitHub metrics. Use responsibly and in accordance with GitHub's Terms of Service and API guidelines.

## 🎉 Happy Tracking!

Now you can track **every single metric** GitHub offers, plus additional custom insights, all in one comprehensive tool!
