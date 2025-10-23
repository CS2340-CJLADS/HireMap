// Simple job search dashboard - only panel switching
document.addEventListener('DOMContentLoaded', () => {
    // Handle job tile clicks
    document.querySelectorAll('.job-tile').forEach(tile => {
        tile.addEventListener('click', () => {
            const jobId = tile.dataset.jobId;
            showJobDetails(jobId);
        });
    });
    
    // Handle application bar clicks
    document.querySelectorAll('.application-bar').forEach(bar => {
        bar.addEventListener('click', () => {
            const applicationId = bar.dataset.applicationId;
            showApplicationDetails(applicationId);
        });
    });
    
    // Handle back to dashboard button
    const backBtn = document.getElementById('back-to-dashboard');
    if (backBtn) {
        backBtn.addEventListener('click', showDashboard);
    }
});

function showJobDetails(jobId) {
    // Update active job tile
    document.querySelectorAll('.job-tile').forEach(tile => {
        tile.classList.remove('active');
    });
    document.querySelector(`[data-job-id="${jobId}"]`).classList.add('active');
    
    // Switch to job details panel
    document.getElementById('dashboard-content').style.display = 'none';
    document.getElementById('job-details-content').style.display = 'block';
    
    // Load job details from backend
    loadJobDetails(jobId);
}

function showApplicationDetails(applicationId) {
    // Update active application bar
    document.querySelectorAll('.application-bar').forEach(bar => {
        bar.classList.remove('active');
    });
    document.querySelector(`[data-application-id="${applicationId}"]`).classList.add('active');
    
    // Switch to application details panel
    document.getElementById('dashboard-content').style.display = 'none';
    document.getElementById('job-details-content').style.display = 'block';
    
    // Load application details from backend
    loadApplicationDetails(applicationId);
}

function loadJobDetails(jobId) {
    // Show loading state
    const loadingState = document.getElementById('job-details-loading');
    const jobDetailsBody = document.getElementById('job-details-body');
    
    if (loadingState) loadingState.style.display = 'flex';
    if (jobDetailsBody) jobDetailsBody.style.display = 'none';
    
    // Fetch job details from backend
    fetch(`/api/jobs/${jobId}/`)
        .then(response => response.json())
        .then(data => {
            // Populate job details
            populateJobDetails(data);
            
            // Hide loading state
            if (loadingState) loadingState.style.display = 'none';
            if (jobDetailsBody) jobDetailsBody.style.display = 'block';
        })
        .catch(error => {
            console.error('Error loading job details:', error);
            // Hide loading state
            if (loadingState) loadingState.style.display = 'none';
            if (jobDetailsBody) jobDetailsBody.style.display = 'block';
        });
}

function loadApplicationDetails(applicationId) {
    // Show loading state
    const loadingState = document.getElementById('job-details-loading');
    const jobDetailsBody = document.getElementById('job-details-body');
    
    if (loadingState) loadingState.style.display = 'flex';
    if (jobDetailsBody) jobDetailsBody.style.display = 'none';
    
    // Fetch application details from backend
    fetch(`/api/applications/${applicationId}/`)
        .then(response => response.json())
        .then(data => {
            // Populate application details
            populateApplicationDetails(data);
            
            // Hide loading state
            if (loadingState) loadingState.style.display = 'none';
            if (jobDetailsBody) jobDetailsBody.style.display = 'block';
        })
        .catch(error => {
            console.error('Error loading application details:', error);
            // Hide loading state
            if (loadingState) loadingState.style.display = 'none';
            if (jobDetailsBody) jobDetailsBody.style.display = 'block';
        });
}

function populateJobDetails(jobData) {
    // Populate header
    document.getElementById('job-description-company').textContent = jobData.company_name || 'Company';
    document.getElementById('job-description-position').textContent = jobData.title || 'Position';
    
    // Populate about section
    const location = jobData.remote ? `${jobData.location} (Remote)` : jobData.location;
    document.getElementById('job-description-location').textContent = location || 'Location';
    document.getElementById('job-description-salary').textContent = `$${jobData.salary_min} - $${jobData.salary_max}`;
    document.getElementById('job-description-visa').textContent = jobData.visa_sponsorship ? 'Visa Required' : 'No Visa Required';
    
    // Populate skills
    document.getElementById('job-description-skills').textContent = jobData.skills_required || 'Skills';
    
    // Populate requirements
    document.getElementById('job-description-requirements').textContent = jobData.requirements || 'Requirements';
    
    // Populate description
    document.getElementById('job-description-description').textContent = jobData.description || 'Description';
}

function populateApplicationDetails(applicationData) {
    // Populate header with job information
    document.getElementById('job-description-company').textContent = applicationData.listing.recruiter.company_name || 'Company';
    document.getElementById('job-description-position').textContent = applicationData.listing.title || 'Position';
    
    // Add status badge to header
    const companyElement = document.getElementById('job-description-company');
    const existingStatusBadge = companyElement.parentNode.querySelector('.status-badge');
    if (existingStatusBadge) {
        existingStatusBadge.remove();
    }
    
    const statusBadge = document.createElement('div');
    statusBadge.className = `status-badge status-${applicationData.status.toLowerCase()}`;
    statusBadge.textContent = applicationData.status;
    companyElement.parentNode.appendChild(statusBadge);
    
    // Populate about section
    const location = applicationData.listing.remote ? `${applicationData.listing.location} (Remote)` : applicationData.listing.location;
    document.getElementById('job-description-location').textContent = location || 'Location';
    document.getElementById('job-description-salary').textContent = `$${applicationData.listing.salary_min} - $${applicationData.listing.salary_max}`;
    document.getElementById('job-description-visa').textContent = applicationData.listing.visa_sponsorship ? 'Visa Required' : 'No Visa Required';
    
    // Populate skills
    document.getElementById('job-description-skills').textContent = applicationData.listing.skills_required || 'Skills';
    
    // Populate requirements
    document.getElementById('job-description-requirements').textContent = applicationData.listing.requirements || 'Requirements';
    
    // Populate description
    document.getElementById('job-description-description').textContent = applicationData.listing.description || 'Description';
    
    // Populate application note
    document.getElementById('application-note').textContent = applicationData.message || 'No message provided';
}

function showDashboard() {
    // Clear active job tile
    document.querySelectorAll('.job-tile').forEach(tile => {
        tile.classList.remove('active');
    });
    
    // Switch to dashboard panel
    document.getElementById('job-details-content').style.display = 'none';
    document.getElementById('dashboard-content').style.display = 'block';
}

// Notification function
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Style the notification
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'error' ? '#dc3545' : type === 'warning' ? '#ffc107' : '#007bff'};
        color: white;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 1000;
        font-weight: 500;
        max-width: 300px;
        word-wrap: break-word;
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Remove after 3 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 3000);
}

// Global function for applying to jobs
function applyToJob(jobId) {
    // Check if already applied
    const jobTile = document.querySelector(`[data-job-id="${jobId}"]`);
    if (jobTile && jobTile.querySelector('.applied-badge')) {
        showNotification('You have already applied to this job.', 'warning');
        return;
    }
    
    window.location.href = `/jobs/${jobId}/apply/`;
}

// Add event listener for apply button
document.addEventListener('DOMContentLoaded', () => {
    // Handle apply button clicks
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('apply-button')) {
            const activeJobTile = document.querySelector('.job-tile.active');
            if (activeJobTile) {
                const jobId = activeJobTile.dataset.jobId;
                applyToJob(jobId);
            }
        }
    });
});