document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('modal-add-project');
    const btnAdd = document.getElementById('btn-add-project');
    const btnClose = document.getElementById('btn-close-modal');
    const formAdd = document.getElementById('form-add-project');
    const container = document.getElementById('projects-container');

    async function fetchProjects() {
        try {
            const data = await window.api.getProjects();
            
            if (data.length === 0) {
                container.innerHTML = '<div class="loading-state">No projects found. Click + Add Project to start.</div>';
                return;
            }

            container.innerHTML = '';
            data.forEach(proj => {
                const card = document.createElement('div');
                card.className = 'project-card glass-panel';
                card.innerHTML = `
                    <h3>${proj.name}</h3>
                    <p>${proj.description || 'No description provided'}</p>
                    <div style="font-size: 0.8rem; color: var(--text-muted);">Nodes: ${proj.nodesCount}</div>
                `;
                container.appendChild(card);
            });
        } catch (error) {
            container.innerHTML = '<div class="loading-state" style="color: var(--danger)">Error loading projects.</div>';
        }
    }

    btnAdd.addEventListener('click', () => {
        modal.style.display = 'flex';
    });

    btnClose.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    formAdd.addEventListener('submit', async (e) => {
        e.preventDefault();
        const name = document.getElementById('proj-name').value;
        const desc = document.getElementById('proj-desc').value;

        try {
            const res = await window.api.addProject({ name, description: desc });
            if (res.success) {
                modal.style.display = 'none';
                formAdd.reset();
                fetchProjects();
            }
        } catch (err) {
            alert('Failed to create project');
        }
    });

    fetchProjects();
});
