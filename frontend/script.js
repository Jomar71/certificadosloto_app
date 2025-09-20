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
        const finalUrl = PROD_API_BASE_URL ? `${PROD_API_BASE_URL}api${url}` : `/api${url}`;
        
        // 'same-origin' es la configuración correcta ahora que todo se sirve desde el mismo dominio.
        // El navegador enviará las cookies automáticamente.
        // Si PROD_API_BASE_URL está definida, significa que estamos en un entorno de producción
        // donde el frontend y el backend pueden estar en diferentes orígenes.
        // En este caso, 'include' es necesario para enviar cookies.
        // Si no, asumimos 'same-origin' para un despliegue unificado.
        options.credentials = PROD_API_BASE_URL ? 'include' : 'same-origin';
        
        return fetch(finalUrl, options);
    }

    // --- LÓGICA DE AUTENTICACIÓN Y UI ---
    async function updateLoginUI() {
        const loginBtn = document.getElementById('loginBtn');
        const adminPanelBtn = document.getElementById('adminPanelBtn');
        const logoutBtn = document.getElementById('logoutBtn');

        try {
            const response = await fetchAPI('/auth/is_admin');
            
            if (response.ok) {
                const data = await response.json();
                if (data.is_admin) {
                    // Usuario es admin
                    if (loginBtn) loginBtn.style.display = 'none';
                    if (adminPanelBtn) adminPanelBtn.style.display = 'inline-block';
                    if (logoutBtn) logoutBtn.style.display = 'inline-block';
                }
            } else {
                // Usuario no es admin o no ha iniciado sesión
                if (loginBtn) loginBtn.style.display = 'inline-block';
                if (adminPanelBtn) adminPanelBtn.style.display = 'none';
                if (logoutBtn) logoutBtn.style.display = 'none';
            }
        } catch (error) {
            // Error de red, no de autenticación
            console.error('Error de conexión al verificar estado de autenticación:', error);
            if (loginBtn) loginBtn.style.display = 'inline-block';
            if (adminPanelBtn) adminPanelBtn.style.display = 'none';
            if (logoutBtn) logoutBtn.style.display = 'none';
        }
    }

    // --- ASIGNACIÓN DE EVENTOS A LOS ELEMENTOS ---
    function setupEventListeners() {
        // Botones de Navegación
        document.getElementById('loginBtn')?.addEventListener('click', () => showSection('loginSection'));
        document.getElementById('adminPanelBtn')?.addEventListener('click', () => showSection('adminPanelSection'));
        document.getElementById('logoutBtn')?.addEventListener('click', async () => {
            await fetchAPI('/auth/logout_admin', { method: 'POST' });
            await updateLoginUI();
            showSection('homeSection');
        });
        
        // Formulario de Login
        document.getElementById('loginForm')?.addEventListener('submit', async function(e) {
            e.preventDefault();
            const loginMessage = document.getElementById('loginMessage');
            if (loginMessage) loginMessage.textContent = 'Procesando...';
            
            try {
                const response = await fetchAPI('/auth/login_admin', {
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
        // Listener para el botón de descarga
        document.getElementById('downloadCertBtn')?.addEventListener('click', function() {
            const certId = this.dataset.certId;
            if (certId) {
                window.location.href = `/api/certificates/${certId}/download`;
            }
        });

        // Lógica para el panel de administración
        document.getElementById('adminPanelBtn')?.addEventListener('click', async () => {
            showSection('adminPanelSection');
            await loadAdminCertificates();
        });
    }

    async function loadAdminCertificates() {
        const certList = document.getElementById('adminCertificatesList');
        if (!certList) return;

        try {
            const response = await fetchAPI('/admin/certificates');
            if (!response.ok) {
                certList.innerHTML = '<tr><td colspan="4">Error al cargar los certificados.</td></tr>';
                return;
            }
            const certificates = await response.json();
            if (certificates.length === 0) {
                certList.innerHTML = '<tr><td colspan="4">No hay certificados para mostrar.</td></tr>';
                return;
            }

            certList.innerHTML = ''; // Limpiar la lista
            certificates.forEach(cert => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${cert.id_documento}</td>
                    <td>${cert.nombre_persona} ${cert.apellido_persona}</td>
                    <td>${cert.numero_identificacion}</td>
                    <td>
                        <button class="btn-edit" data-id="${cert.id_documento}">Editar</button>
                        <button class="btn-delete" data-id="${cert.id_documento}">Eliminar</button>
                    </td>
                `;
                certList.appendChild(row);
            });
        } catch (error) {
            console.error('Error cargando certificados para admin:', error);
            certList.innerHTML = '<tr><td colspan="4">Error de conexión al cargar certificados.</td></tr>';
        }
    }

    // --- INICIALIZACIÓN ---
    showSection('homeSection');
    updateLoginUI();
    setupEventListeners();
});