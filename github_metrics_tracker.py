#!/usr/bin/env python3
"""
GitHub Metrics Tracker - Comprehensive Analytics Tool
Tracks all GitHub metrics exhaustively across all repositories
"""

import requests
import json
import csv
import os
import sys
from datetime import datetime, timedelta, timezone
from collections import defaultdict
from typing import Dict, List, Any, Optional
import time


class GitHubMetricsTracker:
    """
    Comprehensive GitHub metrics tracking system that collects and analyzes
    all available GitHub metrics plus additional custom metrics.
    """

    def __init__(self, token: Optional[str] = None, username: Optional[str] = None):
        """
        Initialize the GitHub Metrics Tracker.
        
        Args:
            token: GitHub personal access token (optional, but required for private repos and higher rate limits)
            username: GitHub username to track (if not provided, will track authenticated user)
        """
        self.token = token or os.environ.get('GITHUB_TOKEN')
        self.username = username
        self.headers = {
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28'
        }
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'
        
        self.base_url = 'https://api.github.com'
        self.metrics = {
            'repositories': [],
            'summary': {},
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'user_info': {}
        }
    
    def _make_request(self, url: str, params: Optional[Dict] = None) -> Optional[Any]:
        """Make a request to the GitHub API with rate limit handling."""
        try:
            response = requests.get(url, headers=self.headers, params=params)
            
            # Handle rate limiting
            if response.status_code == 403 and 'rate limit' in response.text.lower():
                reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                wait_time = max(reset_time - int(time.time()), 0) + 1
                print(f"Rate limit reached. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                response = requests.get(url, headers=self.headers, params=params)
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error making request to {url}: {e}")
            return None
    
    def _get_all_pages(self, url: str, params: Optional[Dict] = None) -> List[Any]:
        """Fetch all pages of paginated results."""
        all_results = []
        page = 1
        per_page = 100
        
        while True:
            page_params = {'page': page, 'per_page': per_page}
            if params:
                page_params.update(params)
            
            results = self._make_request(url, page_params)
            if not results or len(results) == 0:
                break
            
            all_results.extend(results)
            
            if len(results) < per_page:
                break
            
            page += 1
        
        return all_results
    
    def get_user_info(self) -> Dict[str, Any]:
        """Fetch comprehensive user information."""
        if not self.username:
            user_data = self._make_request(f'{self.base_url}/user')
            if user_data:
                self.username = user_data.get('login')
        else:
            user_data = self._make_request(f'{self.base_url}/users/{self.username}')
        
        if not user_data:
            return {}
        
        # Get additional user metrics
        user_metrics = {
            'basic_info': {
                'login': user_data.get('login'),
                'name': user_data.get('name'),
                'company': user_data.get('company'),
                'blog': user_data.get('blog'),
                'location': user_data.get('location'),
                'email': user_data.get('email'),
                'bio': user_data.get('bio'),
                'twitter_username': user_data.get('twitter_username'),
                'created_at': user_data.get('created_at'),
                'updated_at': user_data.get('updated_at'),
            },
            'account_metrics': {
                'public_repos': user_data.get('public_repos', 0),
                'public_gists': user_data.get('public_gists', 0),
                'followers': user_data.get('followers', 0),
                'following': user_data.get('following', 0),
                'total_private_repos': user_data.get('total_private_repos', 0),
                'owned_private_repos': user_data.get('owned_private_repos', 0),
                'disk_usage': user_data.get('disk_usage', 0),
                'collaborators': user_data.get('collaborators', 0),
            }
        }
        
        self.metrics['user_info'] = user_metrics
        return user_metrics
    
    def get_repository_basic_metrics(self, repo_full_name: str) -> Dict[str, Any]:
        """Fetch basic repository metrics."""
        repo_data = self._make_request(f'{self.base_url}/repos/{repo_full_name}')
        
        if not repo_data:
            return {}
        
        return {
            'name': repo_data.get('name'),
            'full_name': repo_data.get('full_name'),
            'description': repo_data.get('description'),
            'private': repo_data.get('private', False),
            'fork': repo_data.get('fork', False),
            'created_at': repo_data.get('created_at'),
            'updated_at': repo_data.get('updated_at'),
            'pushed_at': repo_data.get('pushed_at'),
            'size': repo_data.get('size', 0),
            'stargazers_count': repo_data.get('stargazers_count', 0),
            'watchers_count': repo_data.get('watchers_count', 0),
            'forks_count': repo_data.get('forks_count', 0),
            'open_issues_count': repo_data.get('open_issues_count', 0),
            'default_branch': repo_data.get('default_branch'),
            'language': repo_data.get('language'),
            'has_issues': repo_data.get('has_issues', False),
            'has_projects': repo_data.get('has_projects', False),
            'has_downloads': repo_data.get('has_downloads', False),
            'has_wiki': repo_data.get('has_wiki', False),
            'has_pages': repo_data.get('has_pages', False),
            'has_discussions': repo_data.get('has_discussions', False),
            'archived': repo_data.get('archived', False),
            'disabled': repo_data.get('disabled', False),
            'visibility': repo_data.get('visibility'),
            'license': repo_data.get('license', {}).get('name') if repo_data.get('license') else None,
            'topics': repo_data.get('topics', []),
            'homepage': repo_data.get('homepage'),
            'network_count': repo_data.get('network_count', 0),
            'subscribers_count': repo_data.get('subscribers_count', 0),
        }
    
    def get_languages(self, repo_full_name: str) -> Dict[str, int]:
        """Fetch language statistics for a repository."""
        languages = self._make_request(f'{self.base_url}/repos/{repo_full_name}/languages')
        return languages or {}
    
    def get_contributors(self, repo_full_name: str) -> List[Dict[str, Any]]:
        """Fetch contributor statistics."""
        contributors = self._get_all_pages(f'{self.base_url}/repos/{repo_full_name}/contributors')
        
        return [{
            'login': c.get('login'),
            'contributions': c.get('contributions', 0),
            'type': c.get('type')
        } for c in contributors]
    
    def get_commit_activity(self, repo_full_name: str) -> Dict[str, Any]:
        """Fetch commit activity statistics."""
        # Get commit activity for the last year
        commit_activity = self._make_request(f'{self.base_url}/repos/{repo_full_name}/stats/commit_activity')
        
        if not commit_activity:
            return {'total_commits': 0, 'weekly_activity': []}
        
        total_commits = sum(week.get('total', 0) for week in commit_activity)
        
        return {
            'total_commits_last_year': total_commits,
            'weekly_activity': commit_activity
        }
    
    def get_code_frequency(self, repo_full_name: str) -> Dict[str, Any]:
        """Fetch code frequency statistics (additions/deletions)."""
        code_freq = self._make_request(f'{self.base_url}/repos/{repo_full_name}/stats/code_frequency')
        
        if not code_freq:
            return {'total_additions': 0, 'total_deletions': 0}
        
        total_additions = sum(week[1] for week in code_freq)
        total_deletions = sum(abs(week[2]) for week in code_freq)
        
        return {
            'total_additions': total_additions,
            'total_deletions': total_deletions,
            'net_lines': total_additions - total_deletions,
            'weekly_data': code_freq
        }
    
    def get_participation(self, repo_full_name: str) -> Dict[str, Any]:
        """Fetch participation statistics."""
        participation = self._make_request(f'{self.base_url}/repos/{repo_full_name}/stats/participation')
        
        if not participation:
            return {}
        
        return {
            'owner_commits': sum(participation.get('owner', [])),
            'all_commits': sum(participation.get('all', [])),
            'community_commits': sum(participation.get('all', [])) - sum(participation.get('owner', []))
        }
    
    def get_issues_metrics(self, repo_full_name: str) -> Dict[str, Any]:
        """Fetch comprehensive issue metrics."""
        # Open issues
        open_issues = self._get_all_pages(
            f'{self.base_url}/repos/{repo_full_name}/issues',
            {'state': 'open', 'per_page': 100}
        )
        
        # Closed issues
        closed_issues = self._get_all_pages(
            f'{self.base_url}/repos/{repo_full_name}/issues',
            {'state': 'closed', 'per_page': 100}
        )
        
        # Filter out pull requests (they show up in issues endpoint)
        open_issues_only = [i for i in open_issues if 'pull_request' not in i]
        closed_issues_only = [i for i in closed_issues if 'pull_request' not in i]
        
        return {
            'open_count': len(open_issues_only),
            'closed_count': len(closed_issues_only),
            'total_count': len(open_issues_only) + len(closed_issues_only),
            'open_prs': len(open_issues) - len(open_issues_only),
            'closed_prs': len(closed_issues) - len(closed_issues_only),
        }
    
    def get_pull_requests_metrics(self, repo_full_name: str) -> Dict[str, Any]:
        """Fetch comprehensive pull request metrics."""
        # Open PRs
        open_prs = self._get_all_pages(
            f'{self.base_url}/repos/{repo_full_name}/pulls',
            {'state': 'open', 'per_page': 100}
        )
        
        # Closed PRs
        closed_prs = self._get_all_pages(
            f'{self.base_url}/repos/{repo_full_name}/pulls',
            {'state': 'closed', 'per_page': 100}
        )
        
        # Merged PRs
        merged_prs = [pr for pr in closed_prs if pr.get('merged_at')]
        
        return {
            'open_count': len(open_prs),
            'closed_count': len(closed_prs),
            'merged_count': len(merged_prs),
            'total_count': len(open_prs) + len(closed_prs),
            'merge_rate': len(merged_prs) / len(closed_prs) if closed_prs else 0
        }
    
    def get_releases_metrics(self, repo_full_name: str) -> Dict[str, Any]:
        """Fetch release metrics."""
        releases = self._get_all_pages(f'{self.base_url}/repos/{repo_full_name}/releases')
        
        total_downloads = 0
        for release in releases:
            for asset in release.get('assets', []):
                total_downloads += asset.get('download_count', 0)
        
        return {
            'total_releases': len(releases),
            'latest_release': releases[0].get('tag_name') if releases else None,
            'latest_release_date': releases[0].get('published_at') if releases else None,
            'total_asset_downloads': total_downloads,
            'releases': [{
                'tag_name': r.get('tag_name'),
                'name': r.get('name'),
                'published_at': r.get('published_at'),
                'draft': r.get('draft'),
                'prerelease': r.get('prerelease'),
                'assets_count': len(r.get('assets', []))
            } for r in releases[:10]]  # Last 10 releases
        }
    
    def get_branches_metrics(self, repo_full_name: str) -> Dict[str, Any]:
        """Fetch branch metrics."""
        branches = self._get_all_pages(f'{self.base_url}/repos/{repo_full_name}/branches')
        
        return {
            'total_branches': len(branches),
            'branches': [{
                'name': b.get('name'),
                'protected': b.get('protected', False)
            } for b in branches]
        }
    
    def get_tags_metrics(self, repo_full_name: str) -> Dict[str, Any]:
        """Fetch tag metrics."""
        tags = self._get_all_pages(f'{self.base_url}/repos/{repo_full_name}/tags')
        
        return {
            'total_tags': len(tags),
            'latest_tags': [t.get('name') for t in tags[:10]]
        }
    
    def get_traffic_metrics(self, repo_full_name: str) -> Dict[str, Any]:
        """Fetch traffic metrics (requires push access to the repository)."""
        traffic_data = {}
        
        # Views
        views = self._make_request(f'{self.base_url}/repos/{repo_full_name}/traffic/views')
        if views:
            traffic_data['views'] = {
                'count': views.get('count', 0),
                'uniques': views.get('uniques', 0),
                'daily': views.get('views', [])
            }
        
        # Clones
        clones = self._make_request(f'{self.base_url}/repos/{repo_full_name}/traffic/clones')
        if clones:
            traffic_data['clones'] = {
                'count': clones.get('count', 0),
                'uniques': clones.get('uniques', 0),
                'daily': clones.get('clones', [])
            }
        
        # Popular referrers
        referrers = self._make_request(f'{self.base_url}/repos/{repo_full_name}/traffic/popular/referrers')
        if referrers:
            traffic_data['top_referrers'] = [{
                'referrer': r.get('referrer'),
                'count': r.get('count', 0),
                'uniques': r.get('uniques', 0)
            } for r in referrers[:10]]
        
        # Popular paths
        paths = self._make_request(f'{self.base_url}/repos/{repo_full_name}/traffic/popular/paths')
        if paths:
            traffic_data['top_paths'] = [{
                'path': p.get('path'),
                'title': p.get('title'),
                'count': p.get('count', 0),
                'uniques': p.get('uniques', 0)
            } for p in paths[:10]]
        
        return traffic_data
    
    def get_community_metrics(self, repo_full_name: str) -> Dict[str, Any]:
        """Fetch community profile metrics."""
        community = self._make_request(f'{self.base_url}/repos/{repo_full_name}/community/profile')
        
        if not community:
            return {}
        
        return {
            'health_percentage': community.get('health_percentage', 0),
            'files': {
                'code_of_conduct': community.get('files', {}).get('code_of_conduct') is not None,
                'contributing': community.get('files', {}).get('contributing') is not None,
                'issue_template': community.get('files', {}).get('issue_template') is not None,
                'pull_request_template': community.get('files', {}).get('pull_request_template') is not None,
                'license': community.get('files', {}).get('license') is not None,
                'readme': community.get('files', {}).get('readme') is not None,
            }
        }
    
    def get_vulnerability_alerts(self, repo_full_name: str) -> Dict[str, Any]:
        """Fetch vulnerability alerts (requires appropriate permissions)."""
        # Note: This requires specific OAuth scopes
        alerts = self._make_request(
            f'{self.base_url}/repos/{repo_full_name}/vulnerability-alerts',
            headers={'Accept': 'application/vnd.github.dorian-preview+json'}
        )
        
        return {
            'has_vulnerability_alerts_enabled': alerts is not None
        }
    
    def get_dependabot_alerts(self, repo_full_name: str) -> Dict[str, Any]:
        """Fetch Dependabot alerts."""
        alerts = self._get_all_pages(f'{self.base_url}/repos/{repo_full_name}/dependabot/alerts')
        
        if not alerts:
            return {'total_alerts': 0, 'by_severity': {}, 'by_state': {}}
        
        by_severity = defaultdict(int)
        by_state = defaultdict(int)
        
        for alert in alerts:
            severity = alert.get('security_advisory', {}).get('severity', 'unknown')
            state = alert.get('state', 'unknown')
            by_severity[severity] += 1
            by_state[state] += 1
        
        return {
            'total_alerts': len(alerts),
            'by_severity': dict(by_severity),
            'by_state': dict(by_state),
            'open_critical': sum(1 for a in alerts if a.get('state') == 'open' and 
                               a.get('security_advisory', {}).get('severity') == 'critical')
        }
    
    def get_code_scanning_alerts(self, repo_full_name: str) -> Dict[str, Any]:
        """Fetch code scanning alerts."""
        alerts = self._get_all_pages(f'{self.base_url}/repos/{repo_full_name}/code-scanning/alerts')
        
        if not alerts:
            return {'total_alerts': 0, 'by_severity': {}, 'by_state': {}}
        
        by_severity = defaultdict(int)
        by_state = defaultdict(int)
        
        for alert in alerts:
            severity = alert.get('rule', {}).get('severity', 'unknown')
            state = alert.get('state', 'unknown')
            by_severity[severity] += 1
            by_state[state] += 1
        
        return {
            'total_alerts': len(alerts),
            'by_severity': dict(by_severity),
            'by_state': dict(by_state)
        }
    
    def get_workflows_metrics(self, repo_full_name: str) -> Dict[str, Any]:
        """Fetch GitHub Actions workflow metrics."""
        workflows = self._make_request(f'{self.base_url}/repos/{repo_full_name}/actions/workflows')
        
        if not workflows or 'workflows' not in workflows:
            return {'total_workflows': 0, 'workflows': []}
        
        workflow_stats = []
        for workflow in workflows['workflows']:
            workflow_id = workflow['id']
            runs = self._make_request(
                f'{self.base_url}/repos/{repo_full_name}/actions/workflows/{workflow_id}/runs',
                {'per_page': 100}
            )
            
            if runs and 'workflow_runs' in runs:
                successful = sum(1 for r in runs['workflow_runs'] if r.get('conclusion') == 'success')
                failed = sum(1 for r in runs['workflow_runs'] if r.get('conclusion') == 'failure')
                total = len(runs['workflow_runs'])
                
                workflow_stats.append({
                    'name': workflow.get('name'),
                    'state': workflow.get('state'),
                    'path': workflow.get('path'),
                    'total_runs': total,
                    'successful_runs': successful,
                    'failed_runs': failed,
                    'success_rate': successful / total if total > 0 else 0
                })
        
        return {
            'total_workflows': len(workflows['workflows']),
            'active_workflows': sum(1 for w in workflows['workflows'] if w.get('state') == 'active'),
            'workflows': workflow_stats
        }
    
    def _parse_github_datetime(self, date_string: str) -> Optional[datetime]:
        """Parse GitHub API datetime string safely."""
        if not date_string:
            return None
        try:
            # GitHub API returns ISO 8601 format with 'Z' suffix for UTC
            # Replace 'Z' with '+00:00' for proper timezone parsing
            if date_string.endswith('Z'):
                date_string = date_string[:-1] + '+00:00'
            return datetime.fromisoformat(date_string)
        except (ValueError, AttributeError) as e:
            print(f"Warning: Failed to parse datetime '{date_string}': {e}")
            return None
    
    def get_custom_metrics(self, repo_full_name: str, basic_metrics: Dict) -> Dict[str, Any]:
        """Calculate custom metrics not directly provided by GitHub API."""
        custom = {}
        
        # Repository age
        created = self._parse_github_datetime(basic_metrics.get('created_at'))
        if created:
            age_days = (datetime.now(timezone.utc) - created).days
            custom['age_days'] = age_days
            custom['age_years'] = round(age_days / 365.25, 2)
        
        # Activity metrics
        last_push = self._parse_github_datetime(basic_metrics.get('pushed_at'))
        if last_push:
            days_since_push = (datetime.now(timezone.utc) - last_push).days
            custom['days_since_last_push'] = days_since_push
            custom['is_active'] = days_since_push < 90  # Active if pushed in last 90 days
        
        # Engagement metrics
        stars = basic_metrics.get('stargazers_count', 0)
        forks = basic_metrics.get('forks_count', 0)
        watchers = basic_metrics.get('watchers_count', 0)
        
        custom['engagement_score'] = stars + (forks * 2) + (watchers * 0.5)
        custom['fork_ratio'] = forks / stars if stars > 0 else 0
        
        # Popularity category
        if stars >= 1000:
            custom['popularity'] = 'highly_popular'
        elif stars >= 100:
            custom['popularity'] = 'popular'
        elif stars >= 10:
            custom['popularity'] = 'moderate'
        else:
            custom['popularity'] = 'low'
        
        return custom
    
    def collect_all_metrics_for_repo(self, repo_full_name: str) -> Dict[str, Any]:
        """Collect all available metrics for a single repository."""
        print(f"Collecting metrics for {repo_full_name}...")
        
        repo_metrics = {
            'repository': repo_full_name,
            'collected_at': datetime.now(timezone.utc).isoformat()
        }
        
        # Basic metrics
        repo_metrics['basic'] = self.get_repository_basic_metrics(repo_full_name)
        
        # Language metrics
        repo_metrics['languages'] = self.get_languages(repo_full_name)
        
        # Contributors
        repo_metrics['contributors'] = self.get_contributors(repo_full_name)
        repo_metrics['contributor_count'] = len(repo_metrics['contributors'])
        
        # Commit activity
        repo_metrics['commit_activity'] = self.get_commit_activity(repo_full_name)
        
        # Code frequency
        repo_metrics['code_frequency'] = self.get_code_frequency(repo_full_name)
        
        # Participation
        repo_metrics['participation'] = self.get_participation(repo_full_name)
        
        # Issues
        repo_metrics['issues'] = self.get_issues_metrics(repo_full_name)
        
        # Pull requests
        repo_metrics['pull_requests'] = self.get_pull_requests_metrics(repo_full_name)
        
        # Releases
        repo_metrics['releases'] = self.get_releases_metrics(repo_full_name)
        
        # Branches
        repo_metrics['branches'] = self.get_branches_metrics(repo_full_name)
        
        # Tags
        repo_metrics['tags'] = self.get_tags_metrics(repo_full_name)
        
        # Traffic (may require special permissions)
        repo_metrics['traffic'] = self.get_traffic_metrics(repo_full_name)
        
        # Community
        repo_metrics['community'] = self.get_community_metrics(repo_full_name)
        
        # Security metrics
        repo_metrics['dependabot_alerts'] = self.get_dependabot_alerts(repo_full_name)
        repo_metrics['code_scanning_alerts'] = self.get_code_scanning_alerts(repo_full_name)
        
        # Workflows
        repo_metrics['workflows'] = self.get_workflows_metrics(repo_full_name)
        
        # Custom metrics
        repo_metrics['custom'] = self.get_custom_metrics(repo_full_name, repo_metrics['basic'])
        
        return repo_metrics
    
    def get_all_repositories(self) -> List[str]:
        """Get all repositories for the user."""
        if not self.username:
            self.get_user_info()
        
        repos = self._get_all_pages(f'{self.base_url}/users/{self.username}/repos', {'per_page': 100})
        
        return [repo['full_name'] for repo in repos]
    
    def track_all_repositories(self) -> Dict[str, Any]:
        """Track metrics for all repositories."""
        print("Starting comprehensive GitHub metrics tracking...")
        
        # Get user info
        self.get_user_info()
        print(f"Tracking repositories for user: {self.username}")
        
        # Get all repositories
        repo_names = self.get_all_repositories()
        print(f"Found {len(repo_names)} repositories")
        
        # Collect metrics for each repository
        for repo_name in repo_names:
            try:
                repo_metrics = self.collect_all_metrics_for_repo(repo_name)
                self.metrics['repositories'].append(repo_metrics)
            except Exception as e:
                print(f"Error collecting metrics for {repo_name}: {e}")
        
        # Calculate summary statistics
        self.calculate_summary()
        
        return self.metrics
    
    def calculate_summary(self):
        """Calculate summary statistics across all repositories."""
        repos = self.metrics['repositories']
        
        if not repos:
            self.metrics['summary'] = {}
            return
        
        summary = {
            'total_repositories': len(repos),
            'total_stars': sum(r['basic'].get('stargazers_count', 0) for r in repos),
            'total_forks': sum(r['basic'].get('forks_count', 0) for r in repos),
            'total_watchers': sum(r['basic'].get('watchers_count', 0) for r in repos),
            'total_open_issues': sum(r['issues'].get('open_count', 0) for r in repos),
            'total_contributors': sum(r.get('contributor_count', 0) for r in repos),
            'total_releases': sum(r['releases'].get('total_releases', 0) for r in repos),
            'total_commits': sum(r['commit_activity'].get('total_commits_last_year', 0) for r in repos),
            'total_code_additions': sum(r['code_frequency'].get('total_additions', 0) for r in repos),
            'total_code_deletions': sum(r['code_frequency'].get('total_deletions', 0) for r in repos),
            'active_repositories': sum(1 for r in repos if r['custom'].get('is_active', False)),
            'archived_repositories': sum(1 for r in repos if r['basic'].get('archived', False)),
            'private_repositories': sum(1 for r in repos if r['basic'].get('private', False)),
            'public_repositories': sum(1 for r in repos if not r['basic'].get('private', False)),
            'forked_repositories': sum(1 for r in repos if r['basic'].get('fork', False)),
            'total_open_prs': sum(r['pull_requests'].get('open_count', 0) for r in repos),
            'total_merged_prs': sum(r['pull_requests'].get('merged_count', 0) for r in repos),
        }
        
        # Language distribution
        language_stats = defaultdict(int)
        for repo in repos:
            for lang, bytes_count in repo.get('languages', {}).items():
                language_stats[lang] += bytes_count
        
        total_bytes = sum(language_stats.values())
        summary['languages'] = {
            lang: {
                'bytes': bytes_count,
                'percentage': round((bytes_count / total_bytes * 100), 2) if total_bytes > 0 else 0
            }
            for lang, bytes_count in sorted(language_stats.items(), key=lambda x: x[1], reverse=True)
        }
        
        # Most popular repositories
        summary['most_starred'] = sorted(
            [{'name': r['basic']['full_name'], 'stars': r['basic'].get('stargazers_count', 0)} 
             for r in repos],
            key=lambda x: x['stars'],
            reverse=True
        )[:10]
        
        summary['most_forked'] = sorted(
            [{'name': r['basic']['full_name'], 'forks': r['basic'].get('forks_count', 0)} 
             for r in repos],
            key=lambda x: x['forks'],
            reverse=True
        )[:10]
        
        self.metrics['summary'] = summary
    
    def export_to_json(self, filename: str = 'github_metrics.json'):
        """Export metrics to JSON file."""
        with open(filename, 'w') as f:
            json.dump(self.metrics, f, indent=2)
        print(f"Metrics exported to {filename}")
    
    def export_to_csv(self, filename: str = 'github_metrics.csv'):
        """Export repository metrics to CSV file."""
        if not self.metrics['repositories']:
            print("No repository data to export")
            return
        
        with open(filename, 'w', newline='') as f:
            # Define CSV headers
            headers = [
                'repository', 'stars', 'forks', 'watchers', 'open_issues',
                'language', 'size_kb', 'contributors', 'commits_last_year',
                'open_prs', 'merged_prs', 'releases', 'age_days', 'is_active',
                'has_wiki', 'has_pages', 'archived', 'private'
            ]
            
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            
            for repo in self.metrics['repositories']:
                writer.writerow({
                    'repository': repo['basic']['full_name'],
                    'stars': repo['basic'].get('stargazers_count', 0),
                    'forks': repo['basic'].get('forks_count', 0),
                    'watchers': repo['basic'].get('watchers_count', 0),
                    'open_issues': repo['issues'].get('open_count', 0),
                    'language': repo['basic'].get('language', 'N/A'),
                    'size_kb': repo['basic'].get('size', 0),
                    'contributors': repo.get('contributor_count', 0),
                    'commits_last_year': repo['commit_activity'].get('total_commits_last_year', 0),
                    'open_prs': repo['pull_requests'].get('open_count', 0),
                    'merged_prs': repo['pull_requests'].get('merged_count', 0),
                    'releases': repo['releases'].get('total_releases', 0),
                    'age_days': repo['custom'].get('age_days', 0),
                    'is_active': repo['custom'].get('is_active', False),
                    'has_wiki': repo['basic'].get('has_wiki', False),
                    'has_pages': repo['basic'].get('has_pages', False),
                    'archived': repo['basic'].get('archived', False),
                    'private': repo['basic'].get('private', False),
                })
        
        print(f"Metrics exported to {filename}")
    
    def generate_html_report(self, filename: str = 'github_metrics_report.html'):
        """Generate an HTML report with all metrics."""
        summary = self.metrics.get('summary', {})
        user_info = self.metrics.get('user_info', {})
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GitHub Metrics Report</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: #0d1117;
            color: #c9d1d9;
            padding: 20px;
            line-height: 1.6;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        h1, h2, h3 {{
            color: #58a6ff;
            margin: 20px 0 10px;
        }}
        h1 {{
            font-size: 2.5em;
            border-bottom: 2px solid #21262d;
            padding-bottom: 10px;
        }}
        .metric-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }}
        .metric-card {{
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 20px;
            transition: transform 0.2s;
        }}
        .metric-card:hover {{
            transform: translateY(-2px);
            border-color: #58a6ff;
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: bold;
            color: #58a6ff;
        }}
        .metric-label {{
            color: #8b949e;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        .repo-list {{
            list-style: none;
        }}
        .repo-item {{
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 15px;
            margin: 10px 0;
        }}
        .repo-name {{
            color: #58a6ff;
            font-weight: bold;
            font-size: 1.1em;
        }}
        .repo-stats {{
            display: flex;
            gap: 20px;
            margin-top: 10px;
            color: #8b949e;
        }}
        .language-bar {{
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 6px;
            padding: 15px;
            margin: 10px 0;
        }}
        .language-item {{
            display: flex;
            justify-content: space-between;
            margin: 8px 0;
        }}
        .timestamp {{
            color: #8b949e;
            font-size: 0.9em;
            margin: 20px 0;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #30363d;
        }}
        th {{
            background: #161b22;
            color: #58a6ff;
            font-weight: bold;
        }}
        tr:hover {{
            background: #161b22;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 GitHub Metrics Report</h1>
        <p class="timestamp">Generated: {self.metrics.get('timestamp', 'N/A')}</p>
        
        <h2>👤 User Information</h2>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-value">{user_info.get('basic_info', {}).get('login', 'N/A')}</div>
                <div class="metric-label">Username</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{user_info.get('account_metrics', {}).get('followers', 0)}</div>
                <div class="metric-label">Followers</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{user_info.get('account_metrics', {}).get('following', 0)}</div>
                <div class="metric-label">Following</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{user_info.get('account_metrics', {}).get('public_repos', 0)}</div>
                <div class="metric-label">Public Repos</div>
            </div>
        </div>
        
        <h2>📈 Repository Overview</h2>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-value">{summary.get('total_repositories', 0)}</div>
                <div class="metric-label">Total Repositories</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary.get('total_stars', 0)}</div>
                <div class="metric-label">Total Stars</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary.get('total_forks', 0)}</div>
                <div class="metric-label">Total Forks</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary.get('total_watchers', 0)}</div>
                <div class="metric-label">Total Watchers</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary.get('total_contributors', 0)}</div>
                <div class="metric-label">Total Contributors</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary.get('total_commits', 0)}</div>
                <div class="metric-label">Commits (Last Year)</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary.get('total_releases', 0)}</div>
                <div class="metric-label">Total Releases</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary.get('active_repositories', 0)}</div>
                <div class="metric-label">Active Repositories</div>
            </div>
        </div>
        
        <h2>💻 Code Statistics</h2>
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-value">{summary.get('total_code_additions', 0):,}</div>
                <div class="metric-label">Total Lines Added</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary.get('total_code_deletions', 0):,}</div>
                <div class="metric-label">Total Lines Deleted</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary.get('total_open_issues', 0)}</div>
                <div class="metric-label">Open Issues</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{summary.get('total_open_prs', 0)}</div>
                <div class="metric-label">Open Pull Requests</div>
            </div>
        </div>
        
        <h2>🌐 Language Distribution</h2>
        <div class="language-bar">
"""
        
        # Add language statistics
        languages = summary.get('languages', {})
        for lang, stats in list(languages.items())[:10]:
            html += f"""
            <div class="language-item">
                <span>{lang}</span>
                <span>{stats.get('percentage', 0)}%</span>
            </div>
"""
        
        html += """
        </div>
        
        <h2>⭐ Most Starred Repositories</h2>
        <table>
            <thead>
                <tr>
                    <th>Repository</th>
                    <th>Stars</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for repo in summary.get('most_starred', [])[:10]:
            html += f"""
                <tr>
                    <td>{repo['name']}</td>
                    <td>{repo['stars']}</td>
                </tr>
"""
        
        html += """
            </tbody>
        </table>
        
        <h2>🔱 Most Forked Repositories</h2>
        <table>
            <thead>
                <tr>
                    <th>Repository</th>
                    <th>Forks</th>
                </tr>
            </thead>
            <tbody>
"""
        
        for repo in summary.get('most_forked', [])[:10]:
            html += f"""
                <tr>
                    <td>{repo['name']}</td>
                    <td>{repo['forks']}</td>
                </tr>
"""
        
        html += """
            </tbody>
        </table>
        
        <h2>📦 All Repositories</h2>
        <ul class="repo-list">
"""
        
        for repo in self.metrics.get('repositories', []):
            basic = repo.get('basic', {})
            html += f"""
            <li class="repo-item">
                <div class="repo-name">{basic.get('full_name', 'N/A')}</div>
                <div>{basic.get('description', 'No description')}</div>
                <div class="repo-stats">
                    <span>⭐ {basic.get('stargazers_count', 0)}</span>
                    <span>🔱 {basic.get('forks_count', 0)}</span>
                    <span>👁️ {basic.get('watchers_count', 0)}</span>
                    <span>📝 {repo.get('issues', {}).get('open_count', 0)} issues</span>
                    <span>💻 {basic.get('language', 'N/A')}</span>
                </div>
            </li>
"""
        
        html += """
        </ul>
    </div>
</body>
</html>
"""
        
        with open(filename, 'w') as f:
            f.write(html)
        
        print(f"HTML report generated: {filename}")


def main():
    """Main function to run the metrics tracker."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Comprehensive GitHub Metrics Tracker - Track all GitHub metrics exhaustively'
    )
    parser.add_argument(
        '--token',
        help='GitHub personal access token (or set GITHUB_TOKEN env variable)'
    )
    parser.add_argument(
        '--username',
        help='GitHub username to track (defaults to authenticated user)'
    )
    parser.add_argument(
        '--output',
        default='github_metrics',
        help='Output filename prefix (default: github_metrics)'
    )
    parser.add_argument(
        '--format',
        choices=['json', 'csv', 'html', 'all'],
        default='all',
        help='Output format (default: all)'
    )
    
    args = parser.parse_args()
    
    # Initialize tracker
    tracker = GitHubMetricsTracker(token=args.token, username=args.username)
    
    # Track all repositories
    metrics = tracker.track_all_repositories()
    
    # Export in requested formats
    if args.format in ['json', 'all']:
        tracker.export_to_json(f'{args.output}.json')
    
    if args.format in ['csv', 'all']:
        tracker.export_to_csv(f'{args.output}.csv')
    
    if args.format in ['html', 'all']:
        tracker.generate_html_report(f'{args.output}_report.html')
    
    print("\n✅ Metrics tracking complete!")
    print(f"Total repositories tracked: {len(metrics['repositories'])}")
    print(f"Total stars: {metrics['summary'].get('total_stars', 0)}")
    print(f"Total forks: {metrics['summary'].get('total_forks', 0)}")


if __name__ == '__main__':
    main()
