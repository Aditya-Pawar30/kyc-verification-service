# KYC Verification Frontend

A modern, responsive web interface for uploading and verifying PAN and Aadhaar cards.

## Features

- **Search Bar**: Search by PAN number, Aadhaar number, or name
- **PAN Card Upload**: Upload PAN card images or PDFs
- **Aadhaar Card Upload**: Upload Aadhaar card images or PDFs
- **Drag & Drop**: Easy file upload with drag and drop support
- **File Validation**: Automatic validation of file types and sizes
- **Real-time Feedback**: Loading indicators and result display
- **Responsive Design**: Works on desktop and mobile devices

## Supported File Types

- PNG
- JPG/JPEG
- PDF

## File Size Limit

Maximum file size: 10MB per document

## How to Use

1. **Start the Backend Server**:
   ```bash
   cd app
   uvicorn main:app --reload
   ```

2. **Access the Frontend**:
   Open your browser and navigate to:
   ```
   http://localhost:8000
   ```

3. **Upload Documents**:
   - Click on the PAN Card upload area or drag and drop your PAN card file
   - Click on the Aadhaar Card upload area or drag and drop your Aadhaar card file
   - Both files are required for verification

4. **Verify Documents**:
   - Click the "Verify Documents" button
   - Wait for the processing to complete
   - View the verification results

## API Endpoint

The frontend communicates with the backend at:
- **POST** `/process-and-detect` - Upload and process PAN and Aadhaar files

## Technologies Used

- HTML5
- CSS3 (with modern features like Grid, Flexbox, and Gradients)
- Vanilla JavaScript (ES6+)
- Fetch API for backend communication

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

## File Structure

```
frontend/
├── index.html          # Main HTML file with embedded CSS and JavaScript
└── README.md          # This file
```

## Customization

### Changing Colors

The color scheme can be modified by updating the CSS variables in the `<style>` section:
- Primary gradient: `#667eea` to `#764ba2`
- Success color: `#4caf50`
- Error color: `#ff5252`

### Modifying File Size Limit

To change the maximum file size, update the validation in the JavaScript section:
```javascript
if (file.size > 10 * 1024 * 1024) { // Change 10 to desired MB
    showError('File size exceeds 10MB limit.');
    return;
}
```

### Adding More File Types

To support additional file types, update:
1. The `accept` attribute in the file input elements
2. The `allowedTypes` array in the JavaScript validation

## Troubleshooting

### Files Not Uploading

- Ensure both PAN and Aadhaar files are selected
- Check that file types are supported (PNG, JPG, JPEG, PDF)
- Verify file size is under 10MB

### Backend Connection Error

- Ensure the FastAPI backend is running
- Check that the API endpoint `/process-and-detect` is accessible
- Verify CORS settings if accessing from a different domain

### Styling Issues

- Clear browser cache
- Check for CSS conflicts with other stylesheets
- Ensure viewport meta tag is present for mobile responsiveness
