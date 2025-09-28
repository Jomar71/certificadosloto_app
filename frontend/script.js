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
            if (loginMessage) {
                loginMessage.textContent = 'Procesando...';
                loginMessage.style.display = 'block';
            }
            
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
                    if (loginMessage) loginMessage.style.display = 'none'; // Ocultar al tener éxito
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
                    
                    // También guardamos el ID en el botón de email
                    const sendEmailBtn = document.getElementById('sendEmailCertBtn');
                    if(sendEmailBtn) sendEmailBtn.dataset.certId = data.id_documento;


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

        // Listener para el botón de enviar por email
        document.getElementById('sendEmailCertBtn')?.addEventListener('click', async function() {
            const emailInput = document.getElementById('emailRecipientInput');
            const certId = this.dataset.certId;

            // Si el campo de email no es visible, lo mostramos y cambiamos el texto del botón
            if (emailInput.style.display === 'none') {
                emailInput.style.display = 'inline-block';
                this.textContent = 'Confirmar Envío';
                emailInput.focus();
                return; // Salimos para esperar la confirmación del usuario
            }

            // Si el campo ya es visible, procedemos a enviar
            const email = emailInput.value.trim();
            if (!email) {
                alert('Por favor, ingresa una dirección de correo.');
                return;
            }

            if (certId) {
                try {
                    const response = await fetchAPI(`/certificates/${certId}/send_email`, {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ email: email })
                    });
                    const data = await response.json();
                    alert(data.message);

                    if (response.ok) {
                        // Ocultar campo y restaurar botón tras envío exitoso
                        emailInput.style.display = 'none';
                        emailInput.value = '';
                        this.textContent = 'Enviar por Email';
                    }
                } catch (error) {
                    console.error('Error al enviar certificado por email:', error);
                    alert('Error de conexión al intentar enviar el correo.');
                }
            }
        });

        // Lógica para el panel de administración
        document.getElementById('adminPanelBtn')?.addEventListener('click', async () => {
            showSection('adminPanelSection');
            await loadAdminCertificates();
            // También cargamos la lista de administradores al abrir el panel
            await loadAdminUsers();
        });

        // Botones para mostrar formularios en el panel de admin
        document.getElementById('showAddAdminFormBtn')?.addEventListener('click', () => {
            const form = document.getElementById('addAdminForm');
            if (form) form.style.display = form.style.display === 'none' ? 'block' : 'none';
        });

        document.getElementById('showAddCertFormBtn')?.addEventListener('click', () => {
            const form = document.getElementById('addCertForm');
            if (form) form.style.display = form.style.display === 'none' ? 'block' : 'none';
        });

        // Botón para añadir un nuevo administrador
        document.getElementById('addAdminBtn')?.addEventListener('click', async () => {
            const user = document.getElementById('newAdminUser').value;
            const pass = document.getElementById('newAdminPass').value;
            const messageEl = document.getElementById('addAdminMessage');

            if (!user || !pass) {
                if (messageEl) {
                    messageEl.textContent = 'Usuario y contraseña son requeridos.';
                    messageEl.style.display = 'block';
                }
                return;
            }

            const response = await fetchAPI('/admin/admins', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ login_user: user, login_pass: pass })
            });

            const data = await response.json();
            if (messageEl) {
                messageEl.textContent = data.message;
                messageEl.style.display = 'block';
            }
            
            if (response.ok) {
                document.getElementById('newAdminUser').value = '';
                document.getElementById('newAdminPass').value = '';
                await loadAdminUsers(); // Recargar la lista de administradores
            }
        });

        // Botón para añadir un nuevo certificado
        document.getElementById('addCertBtn')?.addEventListener('click', async () => {
            const certData = {
                tipo_documento: document.getElementById('newCertTipoDocumento').value,
                nombre_persona: document.getElementById('newCertNombrePersona').value,
                apellido_persona: document.getElementById('newCertApellidoPersona').value,
                numero_identificacion: document.getElementById('newCertNumeroIdentificacion').value,
                fecha_creacion: document.getElementById('newCertFechaCreacion').value,
                fecha_vencimiento: document.getElementById('newCertFechaVencimiento').value,
                email_persona: document.getElementById('newCertEmailPersona').value
            };
            const messageEl = document.getElementById('addCertMessage');

            const response = await fetchAPI('/admin/certificates', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(certData)
            });

            const data = await response.json();
            if (messageEl) {
                messageEl.textContent = data.message;
                messageEl.style.display = 'block';
            }

            if (response.ok) {
                await loadAdminCertificates(); // Recargar la lista
                document.getElementById('addCertForm').reset(); // Limpiar formulario
            }
        });

        // --- DELEGACIÓN DE EVENTOS PARA BOTONES DE LA TABLA DE CERTIFICADOS ---
        document.getElementById('adminCertificatesList')?.addEventListener('click', function(e) {
            const target = e.target;
            const certId = target.dataset.id;

            if (target.classList.contains('btn-delete')) {
                handleDeleteCertificate(certId);
            } else if (target.classList.contains('btn-edit')) {
                handleEditCertificate(certId);
            }
        });

        // --- EVENTOS DEL MODAL DE EDICIÓN ---
        const editModal = document.getElementById('editCertModal');
        const closeBtn = editModal?.querySelector('.close-btn');
        const saveCertBtn = document.getElementById('saveCertBtn');

        closeBtn?.addEventListener('click', () => {
            if (editModal) editModal.style.display = 'none';
        });

        saveCertBtn?.addEventListener('click', async () => {
            const certId = document.getElementById('editCertId').value;
            const updatedData = {
                tipo_documento: document.getElementById('editCertTipoDocumento').value,
                nombre_persona: document.getElementById('editCertNombrePersona').value,
                apellido_persona: document.getElementById('editCertApellidoPersona').value,
                numero_identificacion: document.getElementById('editCertNumeroIdentificacion').value,
                fecha_creacion: document.getElementById('editCertFechaCreacion').value,
                fecha_vencimiento: document.getElementById('editCertFechaVencimiento').value,
                email_persona: document.getElementById('editCertEmailPersona').value
            };

            try {
                const response = await fetchAPI(`/admin/certificates/${certId}`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(updatedData)
                });

                if (response.ok) {
                    alert('Certificado actualizado con éxito.');
                    if (editModal) editModal.style.display = 'none';
                    await loadAdminCertificates(); // Recargar la lista
                } else {
                    const data = await response.json();
                    alert(`Error al actualizar: ${data.message}`);
                }
            } catch (error) {
                console.error('Error al guardar cambios del certificado:', error);
                alert('Error de conexión al guardar los cambios.');
            }
        });
    }

    async function handleDeleteCertificate(certId) {
        if (!confirm(`¿Estás seguro de que quieres eliminar el certificado con ID ${certId}?`)) {
            return;
        }

        try {
            const response = await fetchAPI(`/admin/certificates/${certId}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                alert('Certificado eliminado con éxito.');
                await loadAdminCertificates(); // Recargar la lista
            } else {
                const data = await response.json();
                alert(`Error al eliminar: ${data.message}`);
            }
        } catch (error) {
            console.error('Error al eliminar certificado:', error);
            alert('Error de conexión al intentar eliminar el certificado.');
        }
    }

    async function handleEditCertificate(certId) {
        const modal = document.getElementById('editCertModal');
        if (!modal) return;

        try {
            const response = await fetchAPI(`/admin/certificates/${certId}`);
            if (!response.ok) {
                alert('No se pudieron cargar los datos del certificado.');
                return;
            }
            const cert = await response.json();

            // Rellenar el formulario del modal
            document.getElementById('editCertId').value = cert.id_documento;
            document.getElementById('editCertTipoDocumento').value = cert.tipo_documento;
            document.getElementById('editCertNombrePersona').value = cert.nombre_persona;
            document.getElementById('editCertApellidoPersona').value = cert.apellido_persona;
            document.getElementById('editCertNumeroIdentificacion').value = cert.numero_identificacion;
            // Asegurarse de que las fechas se asignen correctamente, incluso si son nulas
            document.getElementById('editCertFechaCreacion').value = cert.fecha_creacion || '';
            document.getElementById('editCertFechaVencimiento').value = cert.fecha_vencimiento || '';
            document.getElementById('editCertEmailPersona').value = cert.email_persona || '';
            
            // Mostrar la ruta del PDF (no editable directamente)
            const rutaPdfSpan = document.getElementById('displayEditCertRutaPdf');
            if (rutaPdfSpan) rutaPdfSpan.textContent = cert.ruta_pdf || 'No disponible';

            modal.style.display = 'block';

        } catch (error) {
            console.error('Error al obtener datos del certificado para editar:', error);
            alert('Error de conexión al cargar los datos para editar.');
        }
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

    async function loadAdminUsers() {
        const adminList = document.getElementById('adminList');
        if (!adminList) return;

        try {
            const response = await fetchAPI('/admin/admins');
            if (!response.ok) {
                adminList.innerHTML = '<li>Error al cargar administradores.</li>';
                return;
            }
            const admins = await response.json();
            adminList.innerHTML = ''; // Limpiar
            admins.forEach(admin => {
                const li = document.createElement('li');
                li.textContent = admin.login_user;
                // Aquí se podrían añadir botones de editar/eliminar para admins
                adminList.appendChild(li);
            });
        } catch (error) {
            console.error('Error cargando administradores:', error);
            adminList.innerHTML = '<li>Error de conexión.</li>';
        }
    }

    // --- INICIALIZACIÓN ---
    showSection('homeSection');
    updateLoginUI();
    setupEventListeners();
});