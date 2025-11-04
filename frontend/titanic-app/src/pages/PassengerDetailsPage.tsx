import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { Passenger } from "../types/Passenger";

  const PASSENGER_API = "http://localhost:8001/api/v1/passenger";

export default function PassengerDetailsPage() {
  const { id } = useParams();
  const [passenger, setPassenger] = useState<Passenger | null>(null);

  useEffect(() => {
    async function fetchPassenger() {
      const res = await fetch(`${PASSENGER_API}/${id}`);
      const data = await res.json();
      setPassenger(data);
    }
    fetchPassenger();
  }, [id]);

  if (!passenger) return <div>Loading...</div>;

  return (
    <div>
      <h2>{passenger.last_name}, {passenger.first_name}</h2>
      <p>Sex: {passenger.sex.toLowerCase() === "m" ? "Male" : "Female"}</p>
      <p>Age: {passenger.age}</p>
      <p>Survived: {passenger.survived ? "Yes" : "No"}</p>
      <p>Class: {passenger.p_class}</p>
    </div>
  );
}