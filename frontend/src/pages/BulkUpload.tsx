import React, { useState } from 'react';
import axios from 'axios';

export default function BulkUpload() {
  const [file, setFile] = useState<File | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const selectedFile = e.target.files ? e.target.files[0] : null;
    setFile(selectedFile);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Por favor selecciona un archivo CSV");
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      await axios.post('http://localhost:8000/api/bulk-upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert('Carga masiva exitosa');
    } catch (error) {
      alert('Error en la carga masiva');
    }
  };

  return (
    <div>
      <h2>Carga Masiva de Datos</h2>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Subir Archivo CSV</button>
    </div>
  );
}

