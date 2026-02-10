import { useState, useRef } from 'react';
import { api } from '../services/api';

function Detection() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [dragover, setDragover] = useState(false);
  const fileInput = useRef(null);

  const handleFile = (f) => {
    if (f && f.type.startsWith('image/')) {
      setFile(f);
      setPreview(URL.createObjectURL(f));
      setResult(null);
      setError('');
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragover(false);
    if (e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = async () => {
    if (!file) return;
    setLoading(true);
    setError('');

    try {
      const data = await api.detectImage(file);
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setFile(null);
    setPreview(null);
    setResult(null);
    setError('');
  };

  return (
    <div>
      <h2 className="page-title">Upload Image</h2>
      <p className="page-desc">Select an image to detect objects</p>

      {error && <div className="error-box">{error}</div>}

      <div className="detection-container">
        <div className="upload-area">
          <div 
            className={`dropzone ${dragover ? 'dragover' : ''}`}
            onDragOver={(e) => { e.preventDefault(); setDragover(true); }}
            onDragLeave={() => setDragover(false)}
            onDrop={handleDrop}
            onClick={() => !preview && fileInput.current?.click()}
          >
            {preview ? (
              <img src={preview} alt="Preview" />
            ) : (
              <>
                <p>Drop image here</p>
                <span>or click to select</span>
              </>
            )}
            <input
              ref={fileInput}
              type="file"
              accept="image/*"
              onChange={(e) => handleFile(e.target.files[0])}
              style={{ display: 'none' }}
            />
          </div>

          {preview && (
            <div className="btn-group">
              <button className="btn btn-secondary" onClick={handleClear}>
                Clear
              </button>
              <button 
                className="btn btn-primary" 
                onClick={handleSubmit}
                disabled={loading}
              >
                {loading ? 'Processing...' : 'Detect Objects'}
              </button>
            </div>
          )}
        </div>

        {result && (
          <div className="results-area">
            <h3>Results</h3>
            
            <div className="result-image">
              <img src={api.getImageUrl(result.image_path)} alt="Result" />
            </div>

            <div>
              {result.detections.map((det, i) => (
                <div key={i} className="detection-item">
                  <div className="detection-item-header">
                    <span className="obj-name">{det.object}</span>
                    <span className="confidence">{(det.confidence * 100).toFixed(1)}%</span>
                  </div>
                  <div className="light-info">Suggested: {det.light}</div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Detection;