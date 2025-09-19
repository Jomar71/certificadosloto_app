// ===================================================================================
// SCRIPT.JS - VERSIÓN FINAL CON MÁXIMA COMPATIBILIDAD MÓVIL
// ===================================================================================
document.addEventListener('DOMContentLoaded', () => {
    // --- URLs y constantes ---
    // Esta URL se usará solo en el entorno local. Se reemplazará al desplegar.

    // --- Selección de Elementos ---
    // (Esta sección no cambia)
    
    // --- Funciones ---
    // (No cambian, pero las incluyo para que el archivo esté completo)

    // --- Asignación de Eventos ---
    // Esta es la parte que vamos a reescribir para máxima compatibilidad
    
    function initializeApp() {
        const loginBtn = document.getElementById('loginBtn');
        const adminPanelBtn = document.getElementById('adminPanelBtn');
        // ... (el resto de tus getElementById)

        if (loginBtn) {
            loginBtn.addEventListener('click', () => {
                // ...
            });
        }
        
        // ... (el resto de tus addEventListener)
    }

    initializeApp();
});

// --- CÓDIGO COMPLETO PARA COPIAR Y PEGAR ---

document.addEventListener('DOMContentLoaded', function() {
    'use strict';


    // --- FUNCIONES DE MANEJO DE LA UI ---
    function showSection(sectionId) {
        document.querySelectorAll('main section').forEach(section => {
            section.style.display = 'none';
        });
        const sectionToShow = document.getElementById(sectionId);
        if (sectionToShow) {
            sectionToShow.style.display = 'block';
        }
    }

    // --- FUNCIÓN CENTRAL PARA LLAMADAS A LA API ---
    async function fetchAPI(url, options = {}) {
        // En producción, la URL base se obtiene del archivo config.js
        const finalUrl = `${PROD_API_BASE_URL}/api${url}`;
        
        options.credentials = 'include';
        options.mode = 'cors'; // Asegura que las peticiones sean CORS
        
        return fetch(finalUrl, options);
    }

    // --- LÓGICA DE AUTENTICACIÓN Y UI ---
    async function updateLoginUI() {
        try {
            const response = await fetchAPI('/api/is_admin');
            const data = await response.json();
            
            const loginBtn = document.getElementById('loginBtn');
            const adminPanelBtn = document.getElementById('adminPanelBtn');
            const logoutBtn = document.getElementById('logoutBtn');
            
            if (data.is_admin) {
                if (loginBtn) loginBtn.style.display = 'none';
                if (adminPanelBtn) adminPanelBtn.style.display = 'inline-block';
                if (logoutBtn) logoutBtn.style.display = 'inline-block';
            } else {
                if (loginBtn) loginBtn.style.display = 'inline-block';
                if (adminPanelBtn) adminPanelBtn.style.display = 'none';
                if (logoutBtn) logoutBtn.style.display = 'none';
            }
        } catch (error) {
            console.error('Error al verificar estado de autenticación:', error);
        }
    }

    // --- ASIGNACIÓN DE EVENTOS A LOS ELEMENTOS ---
    function setupEventListeners() {
        // Botones de Navegación
        document.getElementById('loginBtn')?.addEventListener('click', () => showSection('loginSection'));
        document.getElementById('adminPanelBtn')?.addEventListener('click', () => showSection('adminPanelSection'));
        document.getElementById('logoutBtn')?.addEventListener('click', async () => {
            await fetchAPI('/api/logout_admin', { method: 'POST' });
            await updateLoginUI();
            showSection('homeSection');
        });
        
        // Formulario de Login
        document.getElementById('loginForm')?.addEventListener('submit', async function(e) {
            e.preventDefault();
            const loginMessage = document.getElementById('loginMessage');
            if (loginMessage) loginMessage.textContent = 'Procesando...';
            
            try {
                const response = await fetchAPI('/api/login_admin', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        login_user: document.getElementById('loginUser').value,
                        login_pass: document.getElementById('loginPass').value
                    })
                });
                const data = await response.json();
                if (response.ok) {
                    await updateLoginUI();
                    showSection('homeSection');
                } else {
                    if (loginMessage) loginMessage.textContent = data.message;
                }
            } catch (error) {
                if (loginMessage) loginMessage.textContent = 'Error de conexión.';
            }
        });
        
        // Búsqueda de Certificado por Cédula
        document.getElementById('searchCertBtn')?.addEventListener('click', async () => {
            const cedula = document.getElementById('cedulaSearchInput').value.trim();
            if (!cedula) {
                alert('Por favor, ingresa un número de cédula.');
                return;
            }

            const certificateResultDiv = document.getElementById('certificateResult');
            const noCertificateFoundDiv = document.getElementById('noCertificateFound');
            
            try {
                const response = await fetchAPI(`/certificates/search?cedula=${cedula}`);
                const data = await response.json();

                if (response.ok) {
                    document.getElementById('certTipoDocumento').textContent = data.tipo_documento;
                    document.getElementById('certNombrePersona').textContent = data.nombre_persona;
                    document.getElementById('certApellidoPersona').textContent = data.apellido_persona;
                    document.getElementById('certNumeroIdentificacion').textContent = data.numero_identificacion;
                    document.getElementById('certFechaCreacion').textContent = data.fecha_creacion;
                    document.getElementById('certFechaVencimiento').textContent = data.fecha_vencimiento;
                    
                    // Guardar ID para descarga y email
                    const downloadBtn = document.getElementById('downloadCertBtn');
                    if(downloadBtn) downloadBtn.dataset.certId = data.id_documento;

                    certificateResultDiv.style.display = 'block';
                    noCertificateFoundDiv.style.display = 'none';
                } else {
                    certificateResultDiv.style.display = 'none';
                    noCertificateFoundDiv.style.display = 'block';
                }
            } catch (error) {
                console.error('Error al buscar certificado:', error);
                alert('Hubo un problema al conectarse con el servidor.');
                certificateResultDiv.style.display = 'none';
                noCertificateFoundDiv.style.display = 'block';
            }
        });
        // (Aquí irían los listeners para la búsqueda, descarga, y el panel de admin)
    }

    // --- INICIALIZACIÓN ---
    showSection('homeSection');
    updateLoginUI();
    setupEventListeners();
});