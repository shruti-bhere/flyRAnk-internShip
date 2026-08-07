document.addEventListener("DOMContentLoaded", () => {
    // Input your personal GitHub username target profile here
    fetchGitHubProjects("bhereshruti29"); 
});

async function fetchGitHubProjects(username) {
    const gridContainer = document.getElementById("githubRepoGrid");
    if (!gridContainer) return;
    
    try {
        const response = await fetch(`http://localhost:8000/api/v1/projects/github/${username}`);
        if (!response.ok) throw new Error("Upstream data resolution failed.");
        
        const repositories = await response.json();
        gridContainer.innerHTML = ""; // Wipe loading fallback state
        
        if (repositories.length === 0) {
            gridContainer.innerHTML = `<p class="text-muted">No open public repositories found.</p>`;
            return;
        }
        
        repositories.forEach(repo => {
            const repoCard = document.createElement("div");
            repoCard.className = "bento-card";
            repoCard.style.padding = "1.5rem";
            
            repoCard.innerHTML = `
                <h4 style="font-family: 'Fira Code', monospace; color: var(--accent); margin-bottom: 0.5rem;">
                    📂 ${repo.name}
                </h4>
                <p class="text-muted" style="font-size: 0.85rem; margin-bottom: 1rem; flex-grow: 1;">
                    ${repo.description || "No public description cataloged for this workspace repository."}
                </p>
                <div style="display: flex; justify-content: space-between; align-items: center; font-size: 0.8rem;">
                    <span>🛠️ ${repo.language || "Markdown/Text"}</span>
                    <span style="font-weight: 600;">⭐ ${repo.stars}</span>
                </div>
                <a href="${repo.github_link}" target="_blank" class="btn btn-secondary" 
                   style="margin-top: 1rem; padding: 0.4rem; text-align: center; font-size: 0.8rem;">
                   View Source Code
                </a>
            `;
            gridContainer.appendChild(repoCard);
        });
        
    } catch (error) {
        console.error("Error communicating with GitHub API pipeline:", error);
        gridContainer.innerHTML = `
            <p style="color: var(--text-muted); font-size: 0.9rem; grid-column: 1/-1;" class="text-center">
                ⚠️ Live system integration currently unavailable. Check back shortly.
            </p>
        `;
    }
}