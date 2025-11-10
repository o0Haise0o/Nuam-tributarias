import { BrowserRouter, Routes, Route } from "react-router-dom";
import Layout from "./components/Layout";
import Home from "./pages/Home";
import CalificacionesList from "./pages/CalificacionesList";
import BulkUpload from "./pages/BulkUpload";
import AuditList from "./pages/AuditList";

export default function App() {
  return (
    <BrowserRouter>
      <Layout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/calificaciones" element={<CalificacionesList />} />
          <Route path="/bulk" element={<BulkUpload />} />
          <Route path="/audit" element={<AuditList />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  );
}