// Admin Panel JavaScript

// Mock data for demonstration
const mockData = {
    messages: [
        { id: 1, name: 'John Doe', email: 'john@example.com', service: 'Website', message: 'Need a portfolio website', date: '2025-02-12', status: 'new' },
        { id: 2, name: 'Sarah Smith', email: 'sarah@company.com', service: 'Trading Bot', message: 'Looking for crypto bot', date: '2025-02-11', status: 'new' },
        { id: 3, name: 'Mike Johnson', email: 'mike@tech.com', service: 'WhatsApp', message: 'Business automation', date: '2025-02-10', status: 'replied' }
    ],
    projects: [
        { id: 1, title: 'LuxStore Platform', category: 'E-Commerce', status: 'completed' },
        { id: 2, title: 'CryptoScalp Pro', category: 'Trading Bot', status: 'active' },
        { id: 3, title: 'ShopAssist WA', category: 'WhatsApp Bot', status: 'active' }
    ]
};

// Initialize admin panel
document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();
    initLogin();
    initNavigation();
    initCharts();
    loadMessages();
    loadProjects();
    initSocialTabs();
    initForms();
});

// Login functionality
function initLogin() {
    const loginForm = document.getElementById('loginForm');
    const loginScreen = document.getElementById('loginScreen');
    const adminContainer = document.getElementById('adminContainer');

    loginForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        if (username === 'admin' && password === 'baro2025') {
            loginScreen.style.display = 'none';
            adminContainer.style.display = 'flex';
            lucide.createIcons();
        } else {
            alert('Invalid credentials');
        }
    });

    // Logout
    document.getElementById('logoutBtn').addEventListener('click', () => {
        location.reload();
    });
}

// Navigation
function initNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    const sections = document.querySelectorAll('.content-section');
    const pageTitle = document.getElementById('pageTitle');

    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const targetSection = item.dataset.section;

            // Update active nav
            navItems.forEach(nav => nav.classList.remove('active'));
            item.classList.add('active');

            // Show target section
            sections.forEach(section => section.classList.remove('active'));
            document.getElementById(targetSection).classList.add('active');

            // Update title
            pageTitle.textContent = item.querySelector('span').textContent;

            lucide.createIcons();
        });
    });
}

// Initialize charts
function initCharts() {
    // Traffic chart
    const trafficCtx = document.getElementById('trafficChart');
    if (trafficCtx) {
        new Chart(trafficCtx, {
            type: 'line',
            data: {
                labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                datasets: [{
                    label: 'Views',
                    data: [120, 190, 150, 250, 220, 300, 280],
                    borderColor: '#00f5ff',
                    backgroundColor: 'rgba(0, 245, 255, 0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#6a6a7a' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#6a6a7a' }
                    }
                }
            }
        });
    }

    // Page views chart
    const pageViewsCtx = document.getElementById('pageViewsChart');
    if (pageViewsCtx) {
        new Chart(pageViewsCtx, {
            type: 'bar',
            data: {
                labels: ['Home', 'About', 'Services', 'Work', 'Contact'],
                datasets: [{
                    label: 'Views',
                    data: [450, 320, 280, 390, 210],
                    backgroundColor: [
                        '#00f5ff',
                        '#b829f7',
                        '#ff2d95',
                        '#2979ff',
                        '#22c55e'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: {
                        grid: { color: 'rgba(255, 255, 255, 0.05)' },
                        ticks: { color: '#6a6a7a' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { color: '#6a6a7a' }
                    }
                }
            }
        });
    }

    // Sources chart
    const sourcesCtx = document.getElementById('sourcesChart');
    if (sourcesCtx) {
        new Chart(sourcesCtx, {
            type: 'doughnut',
            data: {
                labels: ['Direct', 'Social', 'Search', 'Referral'],
                datasets: [{
                    data: [40, 30, 20, 10],
                    backgroundColor: ['#00f5ff', '#b829f7', '#ff2d95', '#2979ff']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#a0a0b0' }
                    }
                }
            }
        });
    }

    // Services chart
    const servicesCtx = document.getElementById('servicesChart');
    if (servicesCtx) {
        new Chart(servicesCtx, {
            type: 'pie',
            data: {
                labels: ['Websites', 'Trading Bots', 'WhatsApp', 'Automation'],
                datasets: [{
                    data: [35, 25, 25, 15],
                    backgroundColor: ['#00f5ff', '#b829f7', '#ff2d95', '#2979ff']
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: { color: '#a0a0b0' }
                    }
                }
            }
        });
    }
}

// Load messages
function loadMessages() {
    const tableBody = document.getElementById('messagesTable');
    const recentMessages = document.getElementById('recentMessages');
    const messageBadge = document.getElementById('messageBadge');

    if (tableBody) {
        tableBody.innerHTML = mockData.messages.map(msg => `
            <tr>
                <td>${msg.name}</td>
                <td>${msg.email}</td>
                <td>${msg.service}</td>
                <td>${msg.message.substring(0, 50)}...</td>
                <td>${msg.date}</td>
                <td><span class="status ${msg.status}">${msg.status}</span></td>
                <td>
                    <button class="btn btn-sm btn-secondary">Reply</button>
                </td>
            </tr>
        `).join('');
    }

    if (recentMessages) {
        const recent = mockData.messages.slice(0, 3);
        recentMessages.innerHTML = recent.map(msg => `
            <div class="message-item">
                <div class="message-header">
                    <span class="message-name">${msg.name}</span>
                    <span class="message-date">${msg.date}</span>
                </div>
                <p class="message-preview">${msg.message}</p>
            </div>
        `).join('');
    }

    if (messageBadge) {
        const newCount = mockData.messages.filter(m => m.status === 'new').length;
        messageBadge.textContent = newCount;
        messageBadge.style.display = newCount > 0 ? 'block' : 'none';
    }
}

// Load projects
function loadProjects() {
    const projectsGrid = document.getElementById('projectsGrid');
    if (projectsGrid) {
        projectsGrid.innerHTML = mockData.projects.map(project => `
            <div class="project-card">
                <div class="project-image">
                    <div class="project-placeholder">
                        <i data-lucide="folder"></i>
                    </div>
                </div>
                <div class="project-info">
                    <span class="project-category">${project.category}</span>
                    <h4>${project.title}</h4>
                    <span class="project-status ${project.status}">${project.status}</span>
                </div>
                <div class="project-actions">
                    <button class="btn btn-icon"><i data-lucide="edit"></i></button>
                    <button class="btn btn-icon"><i data-lucide="trash-2"></i></button>
                </div>
            </div>
        `).join('');
        lucide.createIcons();
    }
}

// Social media tabs
function initSocialTabs() {
    const tabBtns = document.querySelectorAll('.tab-btn');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            tabBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });
}

// Form submissions
function initForms() {
    // Profile form
    document.getElementById('profileForm')?.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Profile updated!');
    });

    // Security form
    document.getElementById('securityForm')?.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Password updated!');
    });

    // Refresh button
    document.getElementById('refreshBtn')?.addEventListener('click', () => {
        loadMessages();
        lucide.createIcons();
    });
}

// Simulate real-time updates
setInterval(() => {
    const totalViews = document.getElementById('totalViews');
    if (totalViews) {
        const current = parseInt(totalViews.textContent.replace(',', ''));
        totalViews.textContent = (current + Math.floor(Math.random() * 3)).toLocaleString();
    }
}, 5000);

console.log('Admin panel loaded');
