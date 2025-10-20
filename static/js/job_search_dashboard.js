// Job Search Dashboard JavaScript
class JobSearchDashboard {
    constructor() {
        this.currentJobId = null;
        this.jobCache = new Map();
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.loadJobData();
    }
    
    bindEvents() {
        // Back to dashboard button
        const backBtn = document.getElementById('back-to-dashboard');
        if (backBtn) {
            backBtn.addEventListener('click', () => {
                this.showDashboard();
            });
        }
    }
    
    loadJobData() {
        // Extract job data from the existing page content
        const jobTiles = document.querySelectorAll('.job-tile');
        jobTiles.forEach(tile => {
            const jobId = tile.dataset.jobId;
            const jobData = this.extractJobDataFromTile(tile);
            this.jobCache.set(jobId, jobData);
        });
    }
    
    extractJobDataFromTile(tile) {
        const title = tile.querySelector('.job-tile-title').textContent;
        const company = tile.querySelector('.job-tile-company').textContent;
        const location = tile.querySelector('.job-location').textContent;
        const salary = tile.querySelector('.job-salary').textContent;
        const description = tile.querySelector('.job-tile-description').textContent;
        const skills = Array.from(tile.querySelectorAll('.skill-tag')).map(tag => tag.textContent);
        const hasApplied = tile.querySelector('.job-status.applied') !== null;
        
        return {
            title,
            company,
            location,
            salary,
            description,
            skills,
            hasApplied
        };
    }
    
    showJobDetails(jobId) {
        // Update active job tile
        this.updateActiveJobTile(jobId);
        
        // Get job data (from cache or fetch)
        const jobData = this.jobCache.get(jobId);
        if (jobData) {
            this.updateJobDetailsPanel(jobData);
            this.showJobDetailsPanel();
        } else {
            // If not in cache, fetch from server
            this.fetchJobDetails(jobId);
        }
    }
    
    async fetchJobDetails(jobId) {
        this.showLoadingState();
        
        try {
            const response = await fetch(`/jobs/${jobId}/`);
            if (response.ok) {
                // Parse the HTML response to extract job details
                const html = await response.text();
                const parser = new DOMParser();
                const doc = parser.parseFromString(html, 'text/html');
                
                // Extract job details from the job detail page
                const jobData = this.extractJobDataFromDetailPage(doc);
                this.jobCache.set(jobId, jobData);
                
                this.updateJobDetailsPanel(jobData);
                this.showJobDetailsPanel();
            } else {
                this.showErrorState('Failed to load job details');
            }
        } catch (error) {
            console.error('Error fetching job details:', error);
            this.showErrorState('Error loading job details');
        }
    }
    
    extractJobDataFromDetailPage(doc) {
        // Extract data from the job detail page HTML
        const title = doc.querySelector('h1, h2, .job-title')?.textContent || 'Job Title';
        const company = doc.querySelector('.company-name, .recruiter-company')?.textContent || 'Company';
        const description = doc.querySelector('.job-description, .description')?.innerHTML || 'Job description not available';
        const skills = Array.from(doc.querySelectorAll('.skill-tag, .skills span')).map(el => el.textContent);
        const location = doc.querySelector('.job-location, .location')?.textContent || 'Location not specified';
        const salary = doc.querySelector('.salary, .job-salary')?.textContent || 'Salary not specified';
        
        return {
            title,
            company,
            location,
            salary,
            description,
            skills,
            hasApplied: false // This would need to be determined from the page
        };
    }
    
    updateActiveJobTile(jobId) {
        // Remove active class from all job tiles
        document.querySelectorAll('.job-tile').forEach(tile => {
            tile.classList.remove('active');
        });
        
        // Add active class to clicked tile
        const activeTile = document.querySelector(`[data-job-id="${jobId}"]`);
        if (activeTile) {
            activeTile.classList.add('active');
        }
        
        this.currentJobId = jobId;
    }
    
    updateJobDetailsPanel(jobData) {
        const detailsBody = document.getElementById('job-details-body');
        if (!detailsBody) return;
        
        detailsBody.innerHTML = `
            <div class="job-detail-header">
                <h2 class="job-detail-title">${jobData.title}</h2>
                <div class="job-detail-company">${jobData.company}</div>
                <div class="job-detail-meta">
                    <span class="job-detail-location">📍 ${jobData.location}</span>
                    <span class="job-detail-salary">💰 ${jobData.salary}</span>
                </div>
            </div>
            
            <div class="job-detail-section">
                <h3>Job Description</h3>
                <div class="job-detail-description">${jobData.description}</div>
            </div>
            
            ${jobData.skills.length > 0 ? `
            <div class="job-detail-section">
                <h3>Required Skills</h3>
                <div class="job-detail-skills">
                    ${jobData.skills.map(skill => `<span class="skill-tag">${skill}</span>`).join('')}
                </div>
            </div>
            ` : ''}
            
            <div class="job-detail-actions">
                ${jobData.hasApplied ? 
                    '<div class="applied-status">✅ You have already applied to this job</div>' :
                    '<button class="btn btn-primary apply-btn" onclick="applyToJob(' + this.currentJobId + ')">Apply Now</button>'
                }
            </div>
        `;
        
        // Update panel header title
        const titleElement = document.getElementById('job-detail-title');
        if (titleElement) {
            titleElement.textContent = jobData.title;
        }
    }
    
    showJobDetailsPanel() {
        const dashboardContent = document.getElementById('dashboard-content');
        const jobDetailsContent = document.getElementById('job-details-content');
        
        if (dashboardContent && jobDetailsContent) {
            dashboardContent.style.display = 'none';
            jobDetailsContent.style.display = 'block';
        }
    }
    
    showDashboard() {
        const dashboardContent = document.getElementById('dashboard-content');
        const jobDetailsContent = document.getElementById('job-details-content');
        
        if (dashboardContent && jobDetailsContent) {
            jobDetailsContent.style.display = 'none';
            dashboardContent.style.display = 'block';
        }
        
        // Clear active job tile
        this.clearActiveJobTile();
    }
    
    clearActiveJobTile() {
        document.querySelectorAll('.job-tile').forEach(tile => {
            tile.classList.remove('active');
        });
        this.currentJobId = null;
    }
    
    showLoadingState() {
        const loadingState = document.getElementById('job-details-loading');
        const detailsBody = document.getElementById('job-details-body');
        
        if (loadingState && detailsBody) {
            loadingState.style.display = 'flex';
            detailsBody.style.display = 'none';
        }
    }
    
    hideLoadingState() {
        const loadingState = document.getElementById('job-details-loading');
        const detailsBody = document.getElementById('job-details-body');
        
        if (loadingState && detailsBody) {
            loadingState.style.display = 'none';
            detailsBody.style.display = 'block';
        }
    }
    
    showErrorState(message) {
        const detailsBody = document.getElementById('job-details-body');
        if (detailsBody) {
            detailsBody.innerHTML = `
                <div class="error-state">
                    <h3>Error</h3>
                    <p>${message}</p>
                    <button class="btn btn-secondary" onclick="jobSearchDashboard.showDashboard()">Back to Dashboard</button>
                </div>
            `;
        }
        this.hideLoadingState();
    }
}

// Global function for job tile clicks (called from HTML)
function showJobDetails(jobId) {
    if (window.jobSearchDashboard) {
        window.jobSearchDashboard.showJobDetails(jobId);
    }
}

// Global function for applying to jobs
function applyToJob(jobId) {
    // Check if user is logged in
    const isLoggedIn = document.body.classList.contains('logged-in') || 
                      document.querySelector('.nav-link[href*="logout"]') !== null;
    
    if (!isLoggedIn) {
        // Redirect to login page with return URL
        window.location.href = `/accounts/login/?next=/jobs/${jobId}/apply/`;
    } else {
        // Redirect to the existing job application page
        window.location.href = `/jobs/${jobId}/apply/`;
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.jobSearchDashboard = new JobSearchDashboard();
});

// Add CSS for job details
const jobDetailsCSS = `
.job-detail-header {
    margin-bottom: 2rem;
    padding-bottom: 1rem;
    border-bottom: 1px solid #e2e8f0;
}

.job-detail-title {
    color: var(--brand);
    margin: 0 0 0.5rem 0;
    font-size: 1.5rem;
    line-height: 1.3;
}

.job-detail-company {
    color: var(--muted);
    font-size: 1.1rem;
    font-weight: 500;
    margin-bottom: 0.75rem;
}

.job-detail-meta {
    display: flex;
    gap: 1.5rem;
    font-size: 0.9rem;
    color: var(--text-muted);
}

.job-detail-section {
    margin-bottom: 2rem;
}

.job-detail-section h3 {
    color: var(--brand);
    margin: 0 0 1rem 0;
    font-size: 1.1rem;
}

.job-detail-description {
    line-height: 1.6;
    color: var(--text);
}

.job-detail-skills {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.job-detail-skills .skill-tag {
    background: var(--brand-accent);
    color: var(--brand);
    padding: 0.5rem 1rem;
    border-radius: 20px;
    font-size: 0.9rem;
    font-weight: 500;
}

.job-detail-actions {
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid #e2e8f0;
}

.apply-btn {
    padding: 0.75rem 2rem;
    font-size: 1rem;
    font-weight: 600;
}

.applied-status {
    background: #e8f5e8;
    color: #2e7d32;
    padding: 1rem;
    border-radius: 8px;
    text-align: center;
    font-weight: 500;
}

.error-state {
    text-align: center;
    padding: 2rem;
    color: var(--muted);
}

.error-state h3 {
    color: var(--danger);
    margin-bottom: 1rem;
}
`;

// Inject the CSS
const style = document.createElement('style');
style.textContent = jobDetailsCSS;
document.head.appendChild(style);
