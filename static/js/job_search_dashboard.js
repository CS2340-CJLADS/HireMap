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
    const applicationBar = document.querySelector(`[data-application-id="${applicationId}"]`);
    if (!applicationBar) return;
    
    applicationBar.classList.add('active');
    
    // Switch to application details panel
    document.getElementById('dashboard-content').style.display = 'none';
    document.getElementById('job-details-content').style.display = 'block';
    
    // Extract data from DOM data attributes
    const applicationData = {
        id: applicationId,
        status: applicationBar.dataset.status,
        message: applicationBar.dataset.message || '',
        created_at: applicationBar.dataset.createdAt || '',
        listing: {
            id: applicationBar.dataset.listingId,
            title: applicationBar.dataset.position,
            description: applicationBar.dataset.description || '',
            skills_required: applicationBar.dataset.skills || '',
            location: applicationBar.dataset.location || '',
            remote: applicationBar.dataset.remote === 'true',
            salary_min: applicationBar.dataset.salaryMin || '0',
            salary_max: applicationBar.dataset.salaryMax || '0',
            visa_sponsorship: applicationBar.dataset.visa === 'true',
            recruiter: {
                company_name: applicationBar.dataset.company
            }
        }
    };
    
    // Populate application details directly
    populateApplicationDetails(applicationData);
}

function loadJobDetails(jobId) {
    // Show loading state
    const loadingState = document.getElementById('job-details-loading');
    const jobDetailsContent = document.getElementById('job-details-content');
    
    if (loadingState) loadingState.style.display = 'flex';
    
    // Fetch job details from backend
    fetch(`/api/jobs/${jobId}/`)
        .then(response => response.json())
        .then(data => {
            // Populate job details
            populateJobDetails(data);
            
            // Hide loading state
            if (loadingState) loadingState.style.display = 'none';
            if (jobDetailsContent) jobDetailsContent.style.display = 'flex';
        })
        .catch(error => {
            console.error('Error loading job details:', error);
            // Hide loading state
            if (loadingState) loadingState.style.display = 'none';
            if (jobDetailsContent) jobDetailsContent.style.display = 'flex';
        });
}

// loadApplicationDetails is no longer needed - data is extracted from DOM

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
    const header = document.querySelector('.job-description-header');
    const companyElement = document.getElementById('job-description-company');
    const positionElement = document.getElementById('job-description-position');
    
    if (!header || !companyElement || !positionElement) {
        console.error('Job description elements not found');
        return;
    }
    
    // Populate company name
    companyElement.textContent = applicationData.listing.recruiter.company_name || 'Company';
    
    // Remove existing status badge if any
    const existingStatusBadge = header.querySelector('.status-badge');
    if (existingStatusBadge) {
        existingStatusBadge.remove();
    }
    
    // Create header row wrapper for company and status badge
    let headerRow = header.querySelector('.job-description-header-row');
    if (!headerRow) {
        headerRow = document.createElement('div');
        headerRow.className = 'job-description-header-row';
        // Move company element into the row
        header.insertBefore(headerRow, companyElement);
        headerRow.appendChild(companyElement);
    }
    
    // Add status badge next to company name
    const statusBadge = document.createElement('div');
    // Map status to CSS class names
    const statusMap = {
        'Applied': 'applied',
        'Under Review': 'review',
        'Interview': 'interviewing',
        'Offer': 'offer',
        'Closed': 'closed'
    };
    const statusClass = statusMap[applicationData.status] || applicationData.status.toLowerCase().replace(' ', '-').replace('_', '-');
    statusBadge.className = `status-badge status-${statusClass}`;
    statusBadge.textContent = applicationData.status;
    headerRow.appendChild(statusBadge);
    
    // Populate position
    positionElement.textContent = applicationData.listing.title || 'Position';
    
    // Populate applied date
    const appliedDateEl = document.getElementById('job-description-applied-date');
    if (appliedDateEl && applicationData.created_at) {
        const appliedDate = new Date(applicationData.created_at);
        const now = new Date();
        const diffTime = Math.abs(now - appliedDate);
        const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24));
        
        let dateText = 'Applied ';
        if (diffDays === 0) {
            dateText += 'today';
        } else if (diffDays === 1) {
            dateText += 'yesterday';
        } else if (diffDays < 7) {
            dateText += `${diffDays} days ago`;
        } else if (diffDays < 30) {
            const weeks = Math.floor(diffDays / 7);
            dateText += `${weeks} week${weeks > 1 ? 's' : ''} ago`;
        } else if (diffDays < 365) {
            const months = Math.floor(diffDays / 30);
            dateText += `${months} month${months > 1 ? 's' : ''} ago`;
        } else {
            const years = Math.floor(diffDays / 365);
            dateText += `${years} year${years > 1 ? 's' : ''} ago`;
        }
        
        // Also show the actual date in a readable format
        const dateOptions = { year: 'numeric', month: 'long', day: 'numeric' };
        const formattedDate = appliedDate.toLocaleDateString('en-US', dateOptions);
        dateText += ` (${formattedDate})`;
        
        appliedDateEl.textContent = dateText;
    }
    
    // Populate about section
    const location = applicationData.listing.remote ? `${applicationData.listing.location} (Remote)` : applicationData.listing.location;
    const locationEl = document.getElementById('job-description-location');
    const salaryEl = document.getElementById('job-description-salary');
    const visaEl = document.getElementById('job-description-visa');
    
    if (locationEl) locationEl.textContent = location || 'Location';
    if (salaryEl) {
        const salaryMin = parseFloat(applicationData.listing.salary_min) || 0;
        const salaryMax = parseFloat(applicationData.listing.salary_max) || 0;
        salaryEl.textContent = `$${salaryMin.toLocaleString()} - $${salaryMax.toLocaleString()}`;
    }
    if (visaEl) visaEl.textContent = applicationData.listing.visa_sponsorship ? 'Visa sponsorship available' : 'No visa sponsorship';
    
    // Populate skills
    const skillsEl = document.getElementById('job-description-skills');
    if (skillsEl) skillsEl.textContent = applicationData.listing.skills_required || 'Not specified';
    
    // Populate description
    const descriptionEl = document.getElementById('job-description-description');
    if (descriptionEl) descriptionEl.textContent = applicationData.listing.description || 'No description provided';
    
    // Populate application note
    const noteEl = document.getElementById('application-note');
    if (noteEl) noteEl.textContent = applicationData.message || 'No message provided';
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