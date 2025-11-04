import { Passenger } from "../types/Passenger";

interface Props {
  passengers: Passenger[];
}

export default function PassengerTable({ passengers }: Props) {
  return (
    <table>
      <thead>
        <tr>
          <th>ID</th><th>Name</th><th>Sex</th><th>Age</th><th>Class</th><th>Survived</th>
        </tr>
      </thead>
      <tbody>
        {passengers.map(p => (
          <tr key={p.passenger_id}>
            <td>{p.passenger_id}</td>
            <td>{p.name}</td>
            <td>{p.sex}</td>
            <td>{p.age}</td>
            <td>{p.p_class}</td>
            <td>{p.survived ? "Yes" : "No"}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
