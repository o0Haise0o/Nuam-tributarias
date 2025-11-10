import { Link, NavLink } from "react-router-dom";

const navClass = ({ isActive }: { isActive: boolean }) =>
  isActive ? "nav-link nav-link-active" : "nav-link";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div style={{ minHeight: "100vh", background: "#fff", color: "#222" }}>
      <header style={{ display: "flex", gap: 16, padding: "12px 20px", borderBottom: "1px solid #eee" }}>
        <Link to="/" style={{ fontWeight: 700 }}>NUAM</Link>
        <nav style={{ display: "flex", gap: 12 }}>
          <NavLink to="/" className={navClass}>Inicio</NavLink>
        </nav>
      </header>
      <main style={{ maxWidth: 1100, margin: "0 auto", padding: 20 }}>
        {children}
      </main>
    </div>
  );
}

