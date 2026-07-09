import os
import requests
from typing import Optional, List, Dict, Tuple

GITHUB_API_BASE = "https://api.github.com"


class GitHubAutomator:
    def __init__(self, token: Optional[str] = None, username: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.username = username or os.getenv("GITHUB_USERNAME")

        if not self.token:
            raise ValueError(
                "GitHub token not provided. Set GITHUB_TOKEN env var or pass token to GitHubAutomator()."
            )
        if not self.username:
            raise ValueError(
                "GitHub username not provided. Set GITHUB_USERNAME env var or pass username to GitHubAutomator()."
            )

        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": f"github-automator-{self.username}",
            }
        )

    # ---------- Basic helpers ---------- #

    def _handle_response(self, resp: requests.Response) -> Dict:
        """
        Handle a GitHub API response.

        Raises:
            RuntimeError: if the response status is not OK.
        """
        if not resp.ok:
            try:
                data = resp.json()
                msg = data.get("message", resp.text)
            except ValueError:
                msg = resp.text

            raise RuntimeError(
                f"GitHub API error {resp.status_code} for {resp.request.method} "
                f"{resp.request.url}: {msg}"
            )

        if not resp.text or not resp.text.strip():
            return {}
        return resp.json()

    # ---------- Auth ---------- #

    def check_auth(self) -> Dict:
        """
        Validate that the configured token and username can access the GitHub API.
        Returns the authenticated user object on success.

        Raises:
            RuntimeError if the token is invalid or the username does not match.
        """
        url = f"{GITHUB_API_BASE}/user"
        resp = self.session.get(url)
        user = self._handle_response(resp)

        api_login = (user.get("login") or "").strip()
        cfg_username = (self.username or "").strip()

        if cfg_username and api_login != cfg_username:
            raise RuntimeError(
                f"Authenticated as '{api_login}', but GitHubAutomator username is '{cfg_username}'."
            )

        return user

    # ---------- Repositories ---------- #

    def list_my_repos(self, visibility: str = "all") -> List[Dict]:
        """
        List your repositories (all pages).
        visibility: 'all', 'public', or 'private'
        """
        url = f"{GITHUB_API_BASE}/user/repos"
        params = {"visibility": visibility, "per_page": 100, "page": 1}
        repos: List[Dict] = []

        while True:
            resp = self.session.get(url, params=params)
            page_data = self._handle_response(resp)
            if not page_data:
                break

            repos.extend(page_data)

            if len(page_data) < params["per_page"]:
                break
            params["page"] += 1

        return repos

    def create_repo(self, name: str, description: str = "", private: bool = True) -> Dict:
        """
        Create a new repository under your account.
        """
        url = f"{GITHUB_API_BASE}/user/repos"
        payload = {
            "name": name,
            "description": description,
            "private": private,
            "auto_init": True,
        }
        resp = self.session.post(url, json=payload)
        return self._handle_response(resp)

    # ---------- Issues ---------- #

    def create_issue(
        self,
        repo: str,
        title: str,
        body: str = "",
        labels: Optional[List[str]] = None,
    ) -> Dict:
        """
        Create an issue in a repo.
        repo: 'owner/repo_name' or just 'repo_name' for your own.
        """
        owner, repo_name = self._normalize_repo(repo)
        url = f"{GITHUB_API_BASE}/repos/{owner}/{repo_name}/issues"
        payload: Dict = {"title": title, "body": body}
        if labels:
            payload["labels"] = labels
        resp = self.session.post(url, json=payload)
        return self._handle_response(resp)

    # ---------- Branches & PRs ---------- #

    def create_branch(self, repo: str, new_branch: str, from_branch: str = "main") -> Dict:
        """
        Create a new branch from an existing branch.
        """
        owner, repo_name = self._normalize_repo(repo)

        # Get SHA of from_branch
        ref_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo_name}/git/ref/heads/{from_branch}"
        ref_resp = self.session.get(ref_url)
        ref_data = self._handle_response(ref_resp)
        sha = ref_data["object"]["sha"]

        # Create new branch ref
        create_ref_url = f"{GITHUB_API_BASE}/repos/{owner}/{repo_name}/git/refs"
        payload = {
            "ref": f"refs/heads/{new_branch}",
            "sha": sha,
        }
        resp = self.session.post(create_ref_url, json=payload)
        return self._handle_response(resp)

    def create_pull_request(
        self,
        repo: str,
        title: str,
        head_branch: str,
        base_branch: str = "main",
        body: str = "",
        draft: bool = False,
    ) -> Dict:
        """
        Create a pull request from head_branch into base_branch.

        repo: 'owner/repo_name' or just 'repo_name' for your own.
        head_branch: name of the branch in the same repo owner namespace.
        """
        owner, repo_name = self._normalize_repo(repo)
        url = f"{GITHUB_API_BASE}/repos/{owner}/{repo_name}/pulls"
        payload = {
            "title": title,
            "head": f"{owner}:{head_branch}",
            "base": base_branch,
            "body": body,
            "draft": draft,
        }
        resp = self.session.post(url, json=payload)
        return self._handle_response(resp)

    # ---------- Internal helpers ---------- #

    def _normalize_repo(self, repo: str) -> Tuple[str, str]:
        """
        Normalize a repo identifier to (owner, name).
        Accepts 'owner/name' or just 'name' (assumed under self.username).
        """
        repo = repo.strip()
        if not repo:
            raise ValueError("Repository name is empty.")

        if "/" in repo:
            owner, repo_name = repo.split("/", 1)
        else:
            owner, repo_name = self.username, repo

        if not owner or not repo_name:
            raise ValueError(f"Invalid repo specification: {repo!r}")
        return owner, repo_name


def demo():
    """
    Simple demo to show how to use the automator.
    Comment/uncomment pieces as you want.
    """
    gh = GitHubAutomator()

    # Validate auth and show who we're authenticated as
    me = gh.check_auth()
    print(f"Authenticated as: {me['login']}")

    print("Listing your repositories...")
    repos = gh.list_my_repos()
    for r in repos[:10]:  # show first 10
        print("-", r["full_name"])

    # Example: create a new repo
    # new_repo = gh.create_repo(
    #     name="test-automation-repo",
    #     description="Repo created by script",
    #     private=True,
    # )
    # print("Created repo:", new_repo["html_url"])

    # Example: create an issue
    # issue = gh.create_issue(
    #     repo="test-automation-repo",
    #     title="Automated issue",
    #     body="This issue was created by a Python script.",
    #     labels=["automation", "bot"],
    # )
    # print("Created issue:", issue["html_url"])

    # Example: create a branch and PR
    # gh.create_branch("test-automation-repo", "feature/auto-branch", from_branch="main")
    # pr = gh.create_pull_request(
    #     repo="test-automation-repo",
    #     title="Automated PR",
    #     head_branch="feature/auto-branch",
    #     base_branch="main",
    #     body="This PR was created by the GitHubAutomator script.",
    # )
    # print("Created PR:", pr["html_url"])


if __name__ == "__main__":
    demo()
