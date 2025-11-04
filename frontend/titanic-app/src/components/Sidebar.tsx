import { Link } from "react-router-dom";

export default function Sidebar() {
  return (
    <div className="sidebar">
      <h2>Titanic Passengers</h2>
      <ul>
        <li><Link to="/passengers">Passengers</Link></li>
        <li><Link to="/stats">Stats</Link></li>
        <li><Link to="/charts">Charts</Link></li>
      </ul>
    </div>
  );
}