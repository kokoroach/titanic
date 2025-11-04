import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Passenger } from "../types/Passenger";

interface Props {
  passengers: Passenger[];
}

export default function PassengerTable({ passengers }: Props) {
  const rowsPerPage = 20;
  const [page, setPage] = useState(0);

  const start = page * rowsPerPage;
  const currentRows = passengers.slice(start, start + rowsPerPage);
  const totalPages = Math.ceil(passengers.length / rowsPerPage);

  const prevPage = () => setPage((p) => Math.max(p - 1, 0));
  const nextPage = () => setPage((p) => Math.min(p + 1, totalPages - 1));

  return (
    <div className="passenger-table-container">
      <table className="passenger-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Passenger Name</th>
            <th>Sex</th>
            <th>Age</th>
            <th>Survived</th>
            <th>Passenger Class</th>
          </tr>
        </thead>
        <tbody>
          {currentRows.map((p) => (
            <tr key={p.passenger_id}>
              <td>{p.passenger_id}</td>
              <td>
                <Link to={`/passengers/${p.passenger_id}`} className="link-name">
                  {p.last_name}, {p.first_name}
                </Link>
              </td>
              <td>{p.sex.toLowerCase() === "m" ? "Male" : "Female"}</td>
              <td>{p.age}</td>
              <td>{p.survived ? "Yes" : "No"}</td>
              <td>{p.p_class}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* Result pagination */}
      <div className="pagination">
        <button onClick={prevPage} disabled={page === 0}>
          Previous
        </button>
        <span>
          Page {page + 1} of {totalPages}
        </span>
        <button onClick={nextPage} disabled={page === totalPages - 1}>
          Next
        </button>
      </div>
    </div>
  );
}
