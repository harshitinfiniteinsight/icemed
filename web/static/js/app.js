// ICE Reconciliation Mock System - Frontend JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Load sample files on page load
    loadSampleFiles();

    // File input change handler
    const fileInput = document.getElementById('fileInput');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const fileName = e.target.files[0]?.name || 'Choose Excel file (.xlsx)';
            document.getElementById('fileName').textContent = fileName;
        });
    }

    // Upload form handler
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', handleFileUpload);
    }

    // Sample form handler
    const sampleForm = document.getElementById('sampleForm');
    if (sampleForm) {
        sampleForm.addEventListener('submit', handleSampleProcess);
    }
});

/**
 * Load available sample files from server
 */
async function loadSampleFiles() {
    const sampleSelect = document.getElementById('sampleSelect');
    if (!sampleSelect) return;

    try {
        const response = await fetch('/api/sample-files');
        const data = await response.json();

        if (data.success && data.files) {
            sampleSelect.innerHTML = '<option value="">Select a sample file...</option>';
            
            data.files.forEach(file => {
                const option = document.createElement('option');
                option.value = file.filename;
                option.textContent = file.description;
                sampleSelect.appendChild(option);
            });
        } else {
            sampleSelect.innerHTML = '<option value="">Error loading sample files</option>';
        }
    } catch (error) {
        console.error('Error loading sample files:', error);
        sampleSelect.innerHTML = '<option value="">Error loading sample files</option>';
    }
}

/**
 * Handle file upload form submission
 */
async function handleFileUpload(e) {
    e.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const uploadBtn = document.getElementById('uploadBtn');
    
    if (!fileInput.files || fileInput.files.length === 0) {
        showStatus('Please select a file', 'error');
        return;
    }

    const file = fileInput.files[0];
    
    // Validate file type
    if (!file.name.endsWith('.xlsx')) {
        showStatus('Please select an Excel file (.xlsx)', 'error');
        return;
    }

    // Disable button and show progress
    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Processing...';
    showStatus('Uploading and processing file...', 'info');
    showProgress(true);

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            showStatus('File processed successfully!', 'success');
            showProgress(false);
            
            // Show results inline
            displayResults(data);
        } else {
            throw new Error(data.error || 'Processing failed');
        }
    } catch (error) {
        console.error('Error uploading file:', error);
        showStatus(`Error: ${error.message}`, 'error');
        showProgress(false);
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '<span class="btn-icon">🚀</span> Process File';
    }
}

/**
 * Preview raw data when sample file is selected
 */
async function handleSamplePreview() {
    const select = document.getElementById('sampleSelect');
    const sampleName = select.value;
    const previewSection = document.getElementById('rawDataPreview');
    const previewContainer = document.getElementById('rawDataContainer');
    
    // Hide preview if no file selected
    if (!sampleName) {
        previewSection.style.display = 'none';
        return;
    }
    
    showStatus('Loading file preview...', 'info');
    showProgress(true);
    
    try {
        const response = await fetch('/api/preview-sample', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ sample_name: sampleName })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Build preview table
            let tableHTML = `
                <div class="table-container">
                    <p style="margin-bottom: 10px;"><strong>Total Encounters:</strong> ${data.total_rows} | <strong>Showing:</strong> ${data.showing_rows} rows</p>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Patient Name</th>
                                <th>Date of Service</th>
                                <th>Facility</th>
                                <th>Type of Care</th>
                                <th>CPT</th>
                                <th>DX (Assessment)</th>
                                <th>Provider</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            data.preview_data.forEach(row => {
                const patientName = row['Patient Name'] || '';
                const dos = row['Date of Service'] || '';
                const facility = row['Facility'] || '';
                const typeOfCare = row['Type of Care'] || '';
                const cpt = row['CPT'] || '';
                const dx = row['Assessment'] || row['Assestment'] || '';
                const provider = row['Servicing Provider'] || '';
                
                tableHTML += `
                    <tr>
                        <td>${patientName}</td>
                        <td>${dos}</td>
                        <td>${facility}</td>
                        <td>${typeOfCare}</td>
                        <td>${cpt}</td>
                        <td>${dx}</td>
                        <td>${provider}</td>
                    </tr>
                `;
            });
            
            tableHTML += `
                        </tbody>
                    </table>
                </div>
            `;
            
            previewContainer.innerHTML = tableHTML;
            previewSection.style.display = 'block';
            showStatus('File loaded! Review data below, then click "Process Sample" to continue.', 'success');
            
            // Scroll to preview
            previewSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        } else {
            showStatus('Error: ' + data.error, 'error');
            previewSection.style.display = 'none';
        }
    } catch (error) {
        showStatus('Error loading preview: ' + error.message, 'error');
        previewSection.style.display = 'none';
    } finally {
        showProgress(false);
    }
}

/**
 * Handle sample file processing
 */
async function handleSampleProcess(e) {
    e.preventDefault();

    const sampleSelect = document.getElementById('sampleSelect');
    const sampleBtn = document.getElementById('sampleBtn');
    const sampleName = sampleSelect.value;

    if (!sampleName) {
        showStatus('Please select a sample file', 'error');
        return;
    }

    // Disable button and show progress
    sampleBtn.disabled = true;
    sampleBtn.textContent = 'Processing...';
    showStatus(`Processing sample file: ${sampleName}...`, 'info');
    showProgress(true);

    try {
        const response = await fetch('/api/process-sample', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                sample_name: sampleName
            })
        });

        const data = await response.json();

        if (data.success) {
            showStatus('Sample file processed successfully!', 'success');
            showProgress(false);
            
            // Show results inline
            displayResults(data);
        } else {
            throw new Error(data.error || 'Processing failed');
        }
    } catch (error) {
        console.error('Error processing sample:', error);
        showStatus(`Error: ${error.message}`, 'error');
        showProgress(false);
        sampleBtn.disabled = false;
        sampleBtn.innerHTML = '<span class="btn-icon">📊</span> Process Sample';
    }
}

/**
 * Show status message
 */
function showStatus(message, type) {
    const statusSection = document.getElementById('statusSection');
    const statusMessage = document.getElementById('statusMessage');

    if (!statusSection || !statusMessage) return;

    statusSection.style.display = 'block';
    statusMessage.textContent = message;
    statusMessage.className = `status-message ${type}`;
}

/**
 * Show/hide progress bar
 */
function showProgress(show) {
    const progressBar = document.getElementById('progressBar');
    if (progressBar) {
        progressBar.style.display = show ? 'block' : 'none';
    }
}

/**
 * Display results inline on the same page
 */
async function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    const statsGrid = document.getElementById('statsGrid');
    const masterMissingStats = document.getElementById('masterMissingStats');
    const dataTableContainer = document.getElementById('dataTableContainer');
    
    // Get preview data
    const jobId = data.job_id;
    const resultsResponse = await fetch(`/api/results/${jobId}`);
    const resultsData = await resultsResponse.json();
    
    if (!resultsData.success) {
        showStatus('Error loading results', 'error');
        return;
    }
    
    const summary = resultsData.results.summary;
    const previewData = resultsData.results.preview_data || [];
    
    // Build stats grid
    statsGrid.innerHTML = `
        <div class="stat-card">
            <div class="stat-value">${summary.total_encounters}</div>
            <div class="stat-label">Total Encounters</div>
        </div>
        <div class="stat-card success">
            <div class="stat-value">${summary.billed_count}</div>
            <div class="stat-label">Billed Successfully</div>
        </div>
        <div class="stat-card error">
            <div class="stat-value">${summary.not_billed_count}</div>
            <div class="stat-label">Not Billed</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">${summary.success_rate.toFixed(1)}%</div>
            <div class="stat-label">Success Rate</div>
        </div>
    `;
    
    // Build master missing stats
    masterMissingStats.innerHTML = `
        <div class="mm-stat">
            <span class="mm-label">Added:</span>
            <span class="mm-value">${summary.master_missing_added}</span>
        </div>
        <div class="mm-stat">
            <span class="mm-label">Updated:</span>
            <span class="mm-value">${summary.master_missing_updated}</span>
        </div>
        <div class="mm-stat">
            <span class="mm-label">Removed:</span>
            <span class="mm-value">${summary.master_missing_removed}</span>
        </div>
    `;
    
    // Build data table
    if (previewData && previewData.length > 0) {
        let tableHTML = `
            <div class="table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Patient Name</th>
                            <th>Date of Service</th>
                            <th>Facility</th>
                            <th>Type of Care</th>
                            <th>CPT</th>
                            <th>Billed</th>
                            <th>Reason</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        previewData.forEach(row => {
            const rowClass = row.Billed === 'Yes' ? 'success-row' : 'error-row';
            const badgeClass = row.Billed === 'Yes' ? 'badge-success' : 'badge-error';
            const reason = row['Reason for not billed'] || '-';
            
            tableHTML += `
                <tr class="${rowClass}">
                    <td>${row['Patient Name'] || ''}</td>
                    <td>${row['Date of Service'] || ''}</td>
                    <td>${row.Facility || ''}</td>
                    <td>${row['Type of Care'] || ''}</td>
                    <td>${row.CPT || ''}</td>
                    <td><span class="badge ${badgeClass}">${row.Billed}</span></td>
                    <td>${reason}</td>
                </tr>
            `;
        });
        
        tableHTML += `
                    </tbody>
                </table>
            </div>
            <p class="table-footer">Showing ${previewData.length} of ${summary.total_encounters} encounters</p>
        `;
        
        dataTableContainer.innerHTML = tableHTML;
    } else {
        dataTableContainer.innerHTML = '<p>No preview data available</p>';
    }
    
    // Update download links with proper session
    const reconciliationFile = resultsData.results.output_files.general_reconciliation;
    const masterMissingFile = resultsData.results.output_files.master_missing;
    
    // Store file paths for download (session is already set on server)
    window.currentJobId = jobId;
    
    // Hide upload section, show results
    document.querySelector('.upload-section').style.display = 'none';
    document.querySelector('.info-card').style.display = 'none';
    resultsSection.style.display = 'block';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });
}

/**
 * Download file helper using job ID
 */
function downloadFileByJob(fileType) {
    if (!window.currentJobId) {
        alert('No results available. Please process a file first.');
        return;
    }
    const url = `/api/download-by-job/${window.currentJobId}/${fileType}`;
    window.location.href = url;
}

/**
 * Download file helper (fallback)
 */
function downloadFile(fileType) {
    if (window.currentJobId) {
        downloadFileByJob(fileType);
    } else {
        const url = `/api/download/${fileType}`;
        window.location.href = url;
    }
}
