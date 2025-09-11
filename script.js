// ===================================================================================
// SCRIPT.JS - VERSIÓN FINAL CON CORRECCIONES EN LA BÚSQUEDA
// ===================================================================================
document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    // --- URL de la API ---
    // En producción, esta URL debe ser la de Render. Para desarrollo local, usa la local.
    const API_BASE_URL = 'https://certificadosloto-app.onrender.com'; 
    // const API_BASE_URL = 'http://127.0.0.1:5000'; // Descomenta esta para pruebas locales

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
        const finalUrl = `${API_BASE_URL}${url}`;
        console.log('Haciendo solicitud a:', finalUrl); // Mensaje de depuración

        options.credentials = 'include';
        options.mode = 'cors';

        try {
            const response = await fetch(finalUrl, options);
            if (!response.ok) {
                console.error('Error en la respuesta del servidor:', response.status, response.statusText);
                // Intentamos leer el mensaje de error del backend
                const errorData = await response.json().catch(() => ({ message: 'Respuesta no es JSON' }));
                throw new Error(errorData.message || `Error HTTP: ${response.status}`);
            }
            return response.json();
        } catch (error) {
            console.error('Error de conexión o fetch:', error);
            alert(`Hubo un problema al conectarse con el servidor: ${error.message}`);
            // Devolvemos una promesa rechazada para que el 'catch' del llamador también se active
            return Promise.reject(error);
        }
    }

    // --- LÓGICA DE AUTENTICACIÓN Y UI ---
    async function updateLoginUI() {
        try {
            const data = await fetchAPI('/api/is_admin');
            const loginBtn = document.getElementById('loginBtn');
            const adminPanelBtn = document.getElementById('adminPanelBtn');
            const logoutBtn = document.getElementById('logoutBtn');

            if (data && data.is_admin) {
                if (loginBtn) loginBtn.style.display = 'none';
                if (adminPanelBtn) adminPanelBtn.style.display = 'inline-block';
                if (logoutBtn) logoutBtn.style.display = 'inline-block';
            } else {
                if (loginBtn) loginBtn.style.display = 'inline-block';
                if (adminPanelBtn) adminPanelBtn.style.display = 'none';
                if (logoutBtn) logoutBtn.style.display = 'none';
            }
        } catch (error) {
            // El error ya se muestra en fetchAPI, aquí no hacemos nada más
        }
    }

    // --- ASIGNACIÓN DE EVENTOS A LOS ELEMENTOS ---
    function setupEventListeners() {
        document.getElementById('loginBtn')?.addEventListener('click', () => showSection('loginSection'));
        document.getElementById('adminPanelBtn')?.addEventListener('click', () => {
            // Aquí iría la lógica para cargar el panel de admin
            showSection('adminPanelSection');
        });
        document.getElementById('logoutBtn')?.addEventListener('click', async () => {
            await fetchAPI('/api/logout_admin', { method: 'POST' });
            await updateLoginUI();
            showSection('homeSection');
        });

        document.getElementById('loginForm')?.addEventListener('submit', async function (e) {
            e.preventDefault();
            const loginMessage = document.getElementById('loginMessage');
            if (loginMessage) loginMessage.textContent = 'Procesando...';
            try {
                const data = await fetchAPI('/api/login_admin', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        login_user: document.getElementById('loginUser').value,
                        login_pass: document.getElementById('loginPass').value
                    })
                });
                await updateLoginUI();
                showSection('homeSection');
            } catch (error) {
                if (loginMessage) loginMessage.textContent = error.message || 'Credenciales incorrectas.';
            }
        });

        // --- BÚSQUEDA DE CERTIFICADOS (CORREGIDO) ---
        document.getElementById('searchCertBtn')?.addEventListener('click', async () => {
            const cedula = document.getElementById('cedulaSearchInput').value;
            if (!cedula) {
                alert('Por favor, ingresa un número de cédula.');
                return;
            }

            const certificateResult = document.getElementById('certificateResult');
            const noCertificateFound = document.getElementById('noCertificateFound');
            certificateResult.style.display = 'none';
            noCertificateFound.style.display = 'none';

            try {
                // CORRECCIÓN 1: La URL correcta es '/api/certificates/search'
                const data = await fetchAPI(`/api/certificates/search?cedula=${cedula}`);

                // CORRECCIÓN 2: La estructura de datos no tiene un sub-objeto 'certificado'
                document.getElementById('certTipoDocumento').textContent = data.tipo_documento || 'N/A';
                document.getElementById('certNombrePersona').textContent = data.nombre_persona || 'N/A';
                document.getElementById('certApellidoPersona').textContent = data.apellido_persona || 'N/A';
                document.getElementById('certNumeroIdentificacion').textContent = data.numero_identificacion || 'N/A';
                document.getElementById('certFechaCreacion').textContent = data.fecha_creacion || 'N/A';
                document.getElementById('certFechaVencimiento').textContent = data.fecha_vencimiento || 'N/A';
                
                // Guardamos el ID para usarlo en la descarga
                window.currentCertificateId = data.id_documento;

                certificateResult.style.display = 'block';
            } catch (error) {
                // Si fetchAPI rechaza la promesa (ej. por un 404), este bloque se ejecuta
                noCertificateFound.style.display = 'block';
            }
        });

        // Descargar PDF (Corregido para usar la variable global)
        document.getElementById('downloadCertBtn')?.addEventListener('click', () => {
            if (!window.currentCertificateId) {
                alert('Por favor, busca un certificado válido primero.');
                return;
            }
            // La descarga no es una petición fetch, es una navegación, así que no usamos fetchAPI
            const downloadUrl = `${API_BASE_URL}/api/certificates/${window.currentCertificateId}/download`;
            window.open(downloadUrl, '_blank');
        });

        // (La lógica de Enviar por Email necesitaría una corrección similar si la usas)
    }

    // --- INICIALIZACIÓN ---
    showSection('homeSection');
    updateLoginUI();
    setupEventListeners();
});