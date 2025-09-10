// ===================================================================================
// SCRIPT.JS - VERSIÓN FINAL CON MÁXIMA COMPATIBILIDAD MÓVIL
// ===================================================================================
document.addEventListener('DOMContentLoaded', function () {
    'use strict';

    // --- URL de la API ---
    const API_BASE_URL = 'https://certificadosloto-app.onrender.com'; // URL del backend en Render

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

        options.credentials = 'include'; // Incluye cookies si es necesario
        options.mode = 'cors'; // Asegura que las peticiones sean CORS

        try {
            const response = await fetch(finalUrl, options);
            if (!response.ok) {
                console.error('Error en la solicitud:', response.statusText);
                throw new Error(`Error HTTP: ${response.status}`);
            }
            return response.json();
        } catch (error) {
            console.error('Error de conexión:', error);
            alert('Hubo un problema al conectarse con el servidor. Por favor, intenta más tarde.');
        }
    }

    // --- LÓGICA DE AUTENTICACIÓN Y UI ---
    async function updateLoginUI() {
        try {
            const data = await fetchAPI('/api/is_admin');
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
        document.getElementById('loginForm')?.addEventListener('submit', async function (e) {
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

                if (response.message === 'Login successful') {
                    await updateLoginUI();
                    showSection('homeSection');
                } else {
                    if (loginMessage) loginMessage.textContent = response.message || 'Credenciales incorrectas.';
                }
            } catch (error) {
                if (loginMessage) loginMessage.textContent = 'Error de conexión.';
            }
        });

        // Búsqueda de Certificados
        document.getElementById('searchCertBtn')?.addEventListener('click', async () => {
            const cedula = document.getElementById('cedulaSearchInput').value;
            if (!cedula) {
                alert('Por favor, ingresa un número de cédula.');
                return;
            }

            try {
                const data = await fetchAPI(`/api/certificate?cedula=${cedula}`);
                const certificateResult = document.getElementById('certificateResult');
                const noCertificateFound = document.getElementById('noCertificateFound');

                if (data && data.certificado) {
                    document.getElementById('certTipoDocumento').textContent = data.certificado.tipo_documento || 'N/A';
                    document.getElementById('certNombrePersona').textContent = data.certificado.nombre || 'N/A';
                    document.getElementById('certApellidoPersona').textContent = data.certificado.apellido || 'N/A';
                    document.getElementById('certNumeroIdentificacion').textContent = data.certificado.numero_identificacion || 'N/A';
                    document.getElementById('certFechaCreacion').textContent = data.certificado.fecha_creacion || 'N/A';
                    document.getElementById('certFechaVencimiento').textContent = data.certificado.fecha_vencimiento || 'N/A';

                    certificateResult.style.display = 'block';
                    noCertificateFound.style.display = 'none';
                } else {
                    certificateResult.style.display = 'none';
                    noCertificateFound.style.display = 'block';
                }
            } catch (error) {
                console.error('Error al buscar certificado:', error);
                alert('Hubo un problema al buscar el certificado. Por favor, intenta más tarde.');
            }
        });

        // Descargar PDF
        document.getElementById('downloadCertBtn')?.addEventListener('click', async () => {
            const cedula = document.getElementById('cedulaSearchInput').value;
            if (!cedula) {
                alert('Por favor, busca un certificado antes de descargarlo.');
                return;
            }

            try {
                const response = await fetch(`${API_BASE_URL}/api/download_cert?cedula=${cedula}`);
                if (response.ok) {
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `certificado_${cedula}.pdf`;
                    a.click();
                    window.URL.revokeObjectURL(url);
                } else {
                    alert('No se pudo descargar el certificado.');
                }
            } catch (error) {
                console.error('Error al descargar certificado:', error);
                alert('Hubo un problema al descargar el certificado. Por favor, intenta más tarde.');
            }
        });

        // Enviar por Email
        document.getElementById('sendEmailCertBtn')?.addEventListener('click', async () => {
            const emailRecipient = document.getElementById('emailRecipientInput').value;
            const cedula = document.getElementById('cedulaSearchInput').value;

            if (!emailRecipient || !cedula) {
                alert('Por favor, ingresa un correo electrónico válido y busca un certificado.');
                return;
            }

            try {
                const response = await fetchAPI('/api/send_cert_email', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email: emailRecipient, cedula })
                });

                if (response.message === 'Email sent successfully') {
                    alert('El certificado ha sido enviado por correo electrónico.');
                } else {
                    alert('No se pudo enviar el certificado por correo electrónico.');
                }
            } catch (error) {
                console.error('Error al enviar certificado por email:', error);
                alert('Hubo un problema al enviar el certificado. Por favor, intenta más tarde.');
            }
        });
    }

    // --- INICIALIZACIÓN ---
    showSection('homeSection');
    updateLoginUI();
    setupEventListeners();
});