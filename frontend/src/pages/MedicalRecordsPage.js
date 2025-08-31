import React, { useState, useEffect } from 'react';

const MedicalRecordsPage = () => {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploadLoading, setUploadLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMessage, setSuccessMessage] = useState(null);

  // Fetch medical records on component mount
  useEffect(() => {
    fetchRecords();
  }, []);

  // Function to fetch medical records from MongoDB
  const fetchRecords = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Normally we would call a real API endpoint
      // Since MongoDB is being set up by another team member, we'll simulate the API call
      // In production, replace this with a real API call
      
      // Simulate API response delay
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      // For testing purposes, we'll use mock data stored in localStorage
      const storedRecords = JSON.parse(localStorage.getItem('medivault_records') || '[]');
      setRecords(storedRecords);
    } catch (err) {
      console.error('Error fetching medical records:', err);
      setError('Failed to load medical records. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  // Function to handle file upload
  const handleFileUpload = async (event) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;
    
    setUploadLoading(true);
    setError(null);
    setSuccessMessage(null);
    
    try {
      // Process each file
      const newRecords = [];
      
      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        
        // Check file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
          setError(`File ${file.name} exceeds the maximum size of 10MB.`);
          continue;
        }
        
        // Check file type
        const validTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/jpg'];
        if (!validTypes.includes(file.type)) {
          setError(`File ${file.name} is not a supported format. Please upload PDF or image files.`);
          continue;
        }
        
        // In a real application, we would upload the file to a server/MongoDB
        // For this prototype, we'll read the file and store some metadata in localStorage
        
        // Create a record object
        const record = {
          id: `record_${Date.now()}_${i}`,
          fileName: file.name,
          fileType: file.type,
          uploadDate: new Date().toISOString(),
          size: file.size,
          // Store a data URL for preview (in a real app, this would be a URL to the stored file)
          dataUrl: file.type.includes('image') ? await readFileAsDataURL(file) : null
        };
        
        newRecords.push(record);
      }
      
      if (newRecords.length > 0) {
        // Update state with new records
        const updatedRecords = [...records, ...newRecords];
        setRecords(updatedRecords);
        
        // Store in localStorage (in a real app, this would be stored in MongoDB)
        localStorage.setItem('medivault_records', JSON.stringify(updatedRecords));
        
        setSuccessMessage(`Successfully uploaded ${newRecords.length} file(s).`);
      }
    } catch (err) {
      console.error('Error uploading files:', err);
      setError('Failed to upload files. Please try again later.');
    } finally {
      setUploadLoading(false);
      // Clear the file input
      event.target.value = null;
    }
  };

  // Helper function to read file as data URL
  const readFileAsDataURL = (file) => {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve(reader.result);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  };

  // Function to format file size
  const formatFileSize = (bytes) => {
    if (bytes < 1024) return bytes + ' bytes';
    else if (bytes < 1048576) return (bytes / 1024).toFixed(1) + ' KB';
    else return (bytes / 1048576).toFixed(1) + ' MB';
  };

  // Function to handle file view/download
  const handleFileAction = (record, action) => {
    if (action === 'view') {
      // In a real app, this would open the file in a new tab or preview modal
      if (record.dataUrl) {
        window.open(record.dataUrl, '_blank');
      } else {
        alert('Preview not available for PDF files in this prototype');
      }
    } else if (action === 'download') {
      // In a real app, this would trigger a download of the actual file
      if (record.dataUrl) {
        const a = document.createElement('a');
        a.href = record.dataUrl;
        a.download = record.fileName;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
      } else {
        alert('Download not available in this prototype for PDF files');
      }
    }
  };

  // Function to delete a record
  const handleDeleteRecord = (recordId) => {
    if (window.confirm('Are you sure you want to delete this record?')) {
      const updatedRecords = records.filter(record => record.id !== recordId);
      setRecords(updatedRecords);
      localStorage.setItem('medivault_records', JSON.stringify(updatedRecords));
      setSuccessMessage('Record deleted successfully.');
    }
  };

  // Function to get the appropriate icon for a file type
  const getFileIcon = (fileType) => {
    if (fileType.includes('pdf')) {
      return <i className="fas fa-file-pdf text-red-500"></i>;
    } else if (fileType.includes('image')) {
      return <i className="fas fa-file-image text-blue-500"></i>;
    } else {
      return <i className="fas fa-file text-gray-500"></i>;
    }
  };

  // Function to format date
  const formatDate = (isoDate) => {
    const date = new Date(isoDate);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  return (
    <div className="py-6">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Medical Records</h1>
      
      {/* Upload Section */}
      <div className="card mb-6">
        <div className="card-header">
          <h2 className="card-title">Upload Medical Reports</h2>
        </div>
        <div className="card-content">
          <p className="mb-4 text-gray-600">
            <i className="fas fa-shield-alt text-primary mr-2"></i>
            Upload your medical reports securely. We support PDF and image files (JPG, PNG) up to 10MB.
          </p>
          
          <div className="document-upload-area">
            <div className="upload-container">
              <label htmlFor="medical-record-upload" className="upload-label">
                <i className="fas fa-cloud-upload-alt"></i>
                <span>Drag & drop files or click to browse</span>
                <small>Supports PDF, JPG, PNG (Max 10MB)</small>
              </label>
              <input 
                type="file" 
                id="medical-record-upload" 
                className="hidden" 
                multiple 
                accept=".pdf,.jpg,.jpeg,.png"
                onChange={handleFileUpload}
                disabled={uploadLoading}
              />
            </div>
          </div>
          
          {uploadLoading && (
            <div className="flex justify-center items-center mt-4">
              <div className="animate-spin rounded-full h-6 w-6 border-b-2 border-primary"></div>
              <span className="ml-2">Uploading...</span>
            </div>
          )}
          
          {error && (
            <div className="mt-4 p-3 bg-red-100 text-red-700 rounded-md">
              <i className="fas fa-exclamation-circle mr-2"></i>
              {error}
            </div>
          )}
          
          {successMessage && (
            <div className="mt-4 p-3 bg-green-100 text-green-700 rounded-md">
              <i className="fas fa-check-circle mr-2"></i>
              {successMessage}
            </div>
          )}
        </div>
      </div>
      
      {/* Records List */}
      <div className="card">
        <div className="card-header">
          <h2 className="card-title">Your Medical Records</h2>
          <button 
            className="btn-primary" 
            onClick={fetchRecords}
            disabled={loading}
          >
            <i className="fas fa-sync-alt mr-1"></i> Refresh
          </button>
        </div>
        <div className="card-content">
          {loading ? (
            <div className="flex justify-center items-center py-8">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              <span className="ml-2">Loading records...</span>
            </div>
          ) : records.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              <i className="fas fa-folder-open text-4xl mb-3"></i>
              <p>No medical records found. Upload your first record above.</p>
            </div>
          ) : (
            <div className="records-list">
              {records.map(record => (
                <div key={record.id} className="record-item">
                  <div className="record-icon">
                    {getFileIcon(record.fileType)}
                  </div>
                  <div className="record-details">
                    <h4 className="title">{record.fileName}</h4>
                    <p className="date">
                      {formatDate(record.uploadDate)} • {formatFileSize(record.size)}
                    </p>
                  </div>
                  <div className="record-actions">
                    <button 
                      className="record-btn" 
                      title="View"
                      onClick={() => handleFileAction(record, 'view')}
                    >
                      <i className="fas fa-eye"></i>
                    </button>
                    <button 
                      className="record-btn" 
                      title="Download"
                      onClick={() => handleFileAction(record, 'download')}
                    >
                      <i className="fas fa-download"></i>
                    </button>
                    <button 
                      className="record-btn" 
                      title="Delete"
                      onClick={() => handleDeleteRecord(record.id)}
                    >
                      <i className="fas fa-trash-alt text-red-500"></i>
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default MedicalRecordsPage; 