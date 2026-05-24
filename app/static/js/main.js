document.addEventListener('DOMContentLoaded', function () {
    initSidebar();
    initAutoDismissAlerts();
    initFormValidation();
});

function initSidebar() {
    const sidebar = document.getElementById('sidebar');
    const menuToggle = document.getElementById('menuToggle');
    const sidebarToggle = document.getElementById('sidebarToggle');

    if (menuToggle) {
        menuToggle.addEventListener('click', function () {
            sidebar.classList.toggle('open');
        });
    }

    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', function () {
            sidebar.classList.remove('open');
        });
    }

    document.addEventListener('click', function (e) {
        if (window.innerWidth <= 768) {
            if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        }
    });
}

function initAutoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            if (alert.parentElement) {
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(function () {
                    if (alert.parentElement) {
                        alert.remove();
                    }
                }, 500);
            }
        }, 5000);
    });
}

function initFormValidation() {
    const forms = document.querySelectorAll('form');
    forms.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            const requiredFields = form.querySelectorAll('[required]');
            let valid = true;

            requiredFields.forEach(function (field) {
                if (!field.value.trim()) {
                    field.style.borderColor = '#f44336';
                    valid = false;
                } else {
                    field.style.borderColor = '';
                }
            });

            if (!valid) {
                e.preventDefault();
                showToast('Please fill in all required fields.', 'warning');
            }
        });
    });
}

function showToast(message, type) {
    type = type || 'info';
    const flashContainer = document.querySelector('.flash-messages');
    if (!flashContainer) {
        const container = document.querySelector('.content-area') || document.querySelector('.auth-container');
        if (!container) return;

        const flashDiv = document.createElement('div');
        flashDiv.className = 'flash-messages';
        container.insertBefore(flashDiv, container.firstChild);
    }

    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-' + type;
    alertDiv.innerHTML = '<span>' + message + '</span><button class="alert-close" onclick="this.parentElement.remove()">&times;</button>';

    const container = document.querySelector('.flash-messages');
    container.appendChild(alertDiv);

    setTimeout(function () {
        alertDiv.style.transition = 'opacity 0.5s ease';
        alertDiv.style.opacity = '0';
        setTimeout(function () {
            if (alertDiv.parentElement) {
                alertDiv.remove();
            }
        }, 500);
    }, 5000);
}

function formatCurrency(value) {
    return parseFloat(value).toFixed(2).replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

function confirmAction(message) {
    return confirm(message || 'Are you sure?');
}
