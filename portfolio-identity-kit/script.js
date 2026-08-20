document.addEventListener('DOMContentLoaded', () => {
    loadSavedSkills();
    loadSavedCerts();
});

// 1. Skill Management
function addNewSkill() {
    const iconInput = document.getElementById('skillIconInput');
    const titleInput = document.getElementById('skillTitleInput');
    const descInput = document.getElementById('skillDescInput');

    const icon = iconInput?.value.trim() || '⚡';
    const title = titleInput?.value.trim();
    const desc = descInput?.value.trim();

    if (!title || !desc) {
        alert('Please enter both a skill category title and details.');
        return;
    }

    const id = Date.now();
    const skillData = { id, icon, title, desc };
    
    renderSkillCard(skillData);

    const savedSkills = JSON.parse(localStorage.getItem('customSkills') || '[]');
    savedSkills.push(skillData);
    localStorage.setItem('customSkills', JSON.stringify(savedSkills));

    iconInput.value = '';
    titleInput.value = '';
    descInput.value = '';
}

function renderSkillCard({ id, icon, title, desc }) {
    const grid = document.getElementById('skillsGrid');
    if (!grid) return;

    const newCard = document.createElement('div');
    newCard.className = 'skill-card';
    newCard.id = `skill-${id}`;
    newCard.style.position = 'relative';
    newCard.innerHTML = `
        <button onclick="deleteSkill(${id})" style="position: absolute; top: 10px; right: 10px; background: transparent; border: none; color: #ef4444; cursor: pointer; font-weight: bold; font-size: 14px;">✕</button>
        <div class="skill-icon">${icon}</div>
        <h3>${title}</h3>
        <p>${desc}</p>
    `;
    grid.appendChild(newCard);
}

function loadSavedSkills() {
    const savedSkills = JSON.parse(localStorage.getItem('customSkills') || '[]');
    savedSkills.forEach(skill => renderSkillCard(skill));
}

function deleteSkill(id) {
    document.getElementById(`skill-${id}`)?.remove();
    let savedSkills = JSON.parse(localStorage.getItem('customSkills') || '[]');
    savedSkills = savedSkills.filter(item => item.id !== id);
    localStorage.setItem('customSkills', JSON.stringify(savedSkills));
}

// 2. Certification Management
function addNewCert() {
    const titleInput = document.getElementById('certTitleInput');
    const badgeSelect = document.getElementById('certBadgeInput');

    const title = titleInput?.value.trim();
    const badgeType = badgeSelect?.value || 'Completed';

    if (!title) {
        alert('Please enter a certificate title.');
        return;
    }

    const id = Date.now();
    const certData = { id, title, badgeType };

    renderCertCard(certData);

    const savedCerts = JSON.parse(localStorage.getItem('customCerts') || '[]');
    savedCerts.push(certData);
    localStorage.setItem('customCerts', JSON.stringify(savedCerts));

    titleInput.value = '';
}

function renderCertCard({ id, title, badgeType }) {
    const grid = document.getElementById('certificationsGrid');
    if (!grid) return;

    const newCard = document.createElement('div');
    newCard.className = 'cert-card';
    newCard.id = `cert-${id}`;
    newCard.style.position = 'relative';
    
    const badgeClass = badgeType.toLowerCase() === 'beginner' ? 'cert-badge beginner' : 'cert-badge';

    newCard.innerHTML = `
        <button onclick="deleteCert(${id})" style="position: absolute; top: 8px; right: 8px; background: transparent; border: none; color: #ef4444; cursor: pointer; font-weight: bold; font-size: 14px;">✕</button>
        <span class="cert-title" style="padding-right: 15px;">${title}</span>
        <span class="${badgeClass}">${badgeType}</span>
    `;

    grid.appendChild(newCard);
}

function loadSavedCerts() {
    const savedCerts = JSON.parse(localStorage.getItem('customCerts') || '[]');
    savedCerts.forEach(cert => renderCertCard(cert));
}

function deleteCert(id) {
    document.getElementById(`cert-${id}`)?.remove();
    let savedCerts = JSON.parse(localStorage.getItem('customCerts') || '[]');
    savedCerts = savedCerts.filter(item => item.id !== id);
    localStorage.setItem('customCerts', JSON.stringify(savedCerts));
}