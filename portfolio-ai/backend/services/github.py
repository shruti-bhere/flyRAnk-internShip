import httpx
import logging

logger = logging.getLogger("portfolio_backend.github")

async def fetch_github_repositories(username: str) -> list[dict]:
    """
    Queries public repositories for a specified user, extracting 
    relevant engineering metadata, stargazers, and primary languages.
    """
    url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=10"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=10.0)
            response.raise_for_status()
            repos_data = response.json()
            
            structured_repos = []
            for repo in repos_data:
                # Filter out forks to showcase only authentic work
                if not repo.get("fork"):
                    structured_repos.append({
                        "name": repo.get("name"),
                        "description": repo.get("description"),
                        "stars": repo.get("stargazers_count", 0),
                        "language": repo.get("language"),
                        "github_link": repo.get("html_url"),
                    })
            return structured_repos
            
        except httpx.HTTPStatusError as e:
            logger.error(f"GitHub API returned error state: {e.response.status_code} for user {username}")
            raise RuntimeError("Upstream GitHub communication failure.")
        except Exception as e:
            logger.error(f"Unexpected exception during GitHub repo aggregation: {str(e)}")
            raise