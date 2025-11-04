import { useEffect, useState } from "react";
import PassengerTable from "../components/PassengerTable";
import { Passenger } from "../types/Passenger";

export default function PassengersPage() {
  const [data, setData] = useState<Passenger[]>([]);
  const [uploading, setUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  // TODO: Improvement: set in  .env
  const PASSENGER_API = "http://localhost:8001/api/v1/passengers";

  const fetchPassengers = async () => {
      try {
        const response = await fetch(`${PASSENGER_API}/`);
        if (!response.ok) {
          throw new Error("Failed to fetch passengers");
        }
        const data: Passenger[] = await response.json();
        console.log({data});

        setData(data);
      } catch (error) {
        console.error("Error fetching passengers:", error);
      }
  };

  useEffect(() => {
    fetchPassengers();
  }, []);


  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0] || null;
    setSelectedFile(file);
  };

  const handleFileUpload = async () => {
    if (!selectedFile) return;

    setUploading(true);
    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(`${PASSENGER_API}/upload-csv`, {
        method: "POST",
        body: formData,
      });

      if (response.ok) {
        alert("File uploaded successfully!");
      } else {
        alert("Upload failed");
      }

    } catch (error) {
      console.error(error);

    } finally {
      setUploading(false);
      setSelectedFile(null);
      fetchPassengers();
    }
  };

  return (
    <div>
      <div className="page-header">
      <h2>Passengers</h2>

      <div className="upload-container">
        <p className="upload-label">Upload Titanic Dataset</p>
        <input type="file" accept=".csv" onChange={handleFileSelect} />
        <button
          onClick={handleFileUpload}
          disabled={!selectedFile || uploading}
          className="upload-btn"
        >
          {uploading ? "Uploading..." : "Upload"}
        </button>
      </div>
    </div>

    <PassengerTable passengers={data} />
    </div>
  );
}

