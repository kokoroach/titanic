import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Sidebar from "./components/Sidebar";
import PassengersPage from "./pages/PassengersPage";
import StatsPage from "./pages/StatsPage";
import ChartsPage from "./pages/ChartsPage";

export default function App() {
  return (
    <BrowserRouter>
      <div className="app-container">
        <Sidebar />
        <main>
          <Routes>
            <Route path="/" element={<Navigate to="/passengers" />} />
            <Route path="/passengers" element={<PassengersPage />} />
            <Route path="/stats" element={<StatsPage />} />
            <Route path="/charts" element={<ChartsPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
