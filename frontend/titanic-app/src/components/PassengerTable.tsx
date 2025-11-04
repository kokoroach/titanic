import { Link } from "react-router-dom";
import { Passenger } from "../types/Passenger";

interface Props {
  passengers: Passenger[];
}

export default function PassengerTable({ passengers }: Props) {
  return (
    <table>
      <thead>
        <tr>
          <th>Passenger ID</th>
          <th>Name</th>
          <th>Sex</th>
          <th>Age</th>
          <th>Survived</th>
          <th>Ticket Class</th>
        </tr>
      </thead>
      <tbody>
        {passengers.map(p => (
          <tr key={p.passenger_id}>
            <td>{p.passenger_id}</td>
            <td>
              <Link to={`/passenger/${p.passenger_id}`}>
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
  );
}
