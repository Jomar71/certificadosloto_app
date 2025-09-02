// ===================================================================================
// SCRIPT.JS - VERSIÓN ESTABLE Y FUNCIONAL
// ===================================================================================
document.addEventListener('DOMContentLoaded', () => {
    const API_BASE_URL = 'http://127.0.0.1:5000';
    
    // --- Selección de Elementos ---
    const loginBtn = document.getElementById('loginBtn');
    const adminPanelBtn = document.getElementById('adminPanelBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const homeSection = document.getElementById('homeSection');
    const loginSection = document.getElementById('loginSection');
    const adminPanelSection = document.getElementById('adminPanelSection');
    const loginForm = document.getElementById('loginForm');
    const loginUser = document.getElementById('loginUser');
    const loginPass = document.getElementById('loginPass');
    const loginMessage = document.getElementById('loginMessage');
    const certificateList = document.getElementById('certificateList');
    const searchCertBtn = document.getElementById('searchCertBtn');
    const cedulaSearchInput = document.getElementById('cedulaSearchInput');
    const certificateResult = document.getElementById('certificateResult');
    const noCertificateFound = document.getElementById('noCertificateFound');
    const downloadCertBtn = document.getElementById('downloadCertBtn');
    let currentCertificateId = null;

    // --- Funciones ---
    function showSection(sectionId) {
        homeSection.style.display = 'none';
        loginSection.style.display = 'none';
        adminPanelSection.style.display = 'none';
        const section = document.getElementById(sectionId);
        if (section) section.style.display = 'block';
    }

    async function fetchAPI(url, options = {}) {
        options.credentials = 'include';
        return fetch(`${API_BASE_URL}${url}`, options);
    }

    async function updateLoginUI() {
        try {
            const response = await fetchAPI('/api/is_admin');
            const data = await response.json();
            if (data.is_admin) {
                loginBtn.style.display = 'none';
                adminPanelBtn.style.display = 'inline-block';
                logoutBtn.style.display = 'inline-block';
            } else {
                loginBtn.style.display = 'inline-block';
                adminPanelBtn.style.display = 'none';
                logoutBtn.style.display = 'none';
            }
        } catch (error) { console.error('Error al verificar estado:', error); }
    }

    async function loadAdminCertificates() {
        if (!certificateList) return;
        try {
            const response = await fetchAPI('/api/admin/certificates');
            if (!response.ok) throw new Error(`Error ${response.status}`);
            const certificates = await response.json();
            certificateList.innerHTML = '';
            certificates.forEach(cert => {
                const li = document.createElement('li');
                li.innerHTML = `<span>${cert.nombre_persona} ${cert.apellido_persona} (${cert.numero_identificacion})</span><button class="edit-btn" data-id="${cert.id_documento}">Editar/Generar PDF</button>`;
                certificateList.appendChild(li);
            });
        } catch (error) { certificateList.innerHTML = `<li>Error al cargar certificados.</li>`; }
    }

    async function regeneratePdf(certId) {
        const confirmation = confirm(`¿Quieres regenerar el PDF para el certificado ID ${certId}?`);
        if (!confirmation) return;
        try {
            let response = await fetchAPI(`/api/admin/certificates/${certId}`);
            if (!response.ok) throw new Error('No se pudieron obtener los datos.');
            const certData = await response.json();
            response = await fetchAPI(`/api/admin/certificates/${certId}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(certData)
            });
            if (!response.ok) throw new Error('El backend falló al regenerar.');
            const result = await response.json();
            alert(result.message || 'PDF regenerado.');
        } catch (error) { alert(`Error: ${error.message}`); }
    }

    // --- Asignación de Eventos ---
    loginBtn.addEventListener('click', () => showSection('loginSection'));
    logoutBtn.addEventListener('click', async () => { await fetchAPI('/api/logout_admin', { method: 'POST' }); await updateLoginUI(); showSection('homeSection'); });
    adminPanelBtn.addEventListener('click', () => { showSection('adminPanelSection'); loadAdminCertificates(); });
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        loginMessage.textContent = 'Procesando...';
        try {
            const response = await fetchAPI('/api/login_admin', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ login_user: loginUser.value, login_pass: loginPass.value }) });
            const data = await response.json();
            if (response.ok) { await updateLoginUI(); showSection('homeSection'); } else { loginMessage.textContent = data.message; }
        } catch (error) { loginMessage.textContent = 'Error de conexión.'; }
    });
    certificateList.addEventListener('click', (e) => { if (e.target && e.target.classList.contains('edit-btn')) { regeneratePdf(e.target.dataset.id); } });
    
    // Búsqueda pública y descarga
    if(searchCertBtn) {
        searchCertBtn.addEventListener('click', async () => {
            certificateResult.style.display = 'none';
            noCertificateFound.style.display = 'none';
            try {
                const response = await fetch(`${API_BASE_URL}/api/certificates/search?cedula=${cedulaSearchInput.value}`);
                if (response.ok) {
                    const data = await response.json();
                    currentCertificateId = data.id_documento;
                    document.getElementById('certNombrePersona').textContent = `${data.nombre_persona} ${data.apellido_persona}`;
                    document.getElementById('certNumeroIdentificacion').textContent = data.numero_identificacion;
                    certificateResult.style.display = 'block';
                } else {
                    noCertificateFound.style.display = 'block';
                }
            } catch (error) { console.error("Error en búsqueda:", error); }
        });
    }
    if(downloadCertBtn) {
        downloadCertBtn.addEventListener('click', () => { if (currentCertificateId) { window.open(`${API_BASE_URL}/api/certificates/${currentCertificateId}/download`, '_blank'); } });
    }

    // --- Inicialización ---
    updateLoginUI();
    showSection('homeSection');
});