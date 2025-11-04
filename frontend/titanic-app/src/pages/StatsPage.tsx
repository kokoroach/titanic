import { useEffect, useState } from "react";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { StatsResponse, NumericStats, CategoricalStats } from "../types/Stats";

const COLORS = ["#0088FE", "#00C49F", "#FFBB28", "#FF8042", "#8D44AD"];

const availableColumns = [
  "survived",
  "p_class",
  "sex",
  "age",
  "sib_sp",
  "par_ch",
  "fare",
  "embarked",
];

export default function StatsPage() {
  const [selectedColumn, setSelectedColumn] = useState("age");
  const [stats, setStats] = useState<StatsResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

    const STATS_API = "http://localhost:8001/api/v1/passengers/stats";

  useEffect(() => {
    const fetchStats = async () => {
      setLoading(true);
      setError("");

      try {
        const res = await fetch(`${STATS_API}/${selectedColumn}`);
        if (!res.ok) throw new Error("Failed to fetch stats");

        const data: StatsResponse = await res.json();
        setStats(data);
      } catch (err) {
        if (err instanceof Error) setError(err.message);
        else setError("Unknown error");
      } finally {
        setLoading(false);
      }
    };

    fetchStats();
  }, [selectedColumn]);

  return (
    <div style={{ padding: "2rem" }}>
      <h2>Passenger Statistics</h2>

      <label>Select Column: </label>
      <select
        value={selectedColumn}
        onChange={(e) => setSelectedColumn(e.target.value)}
      >
        {availableColumns.map((col) => (
          <option key={col} value={col}>
            {col}
          </option>
        ))}
      </select>

      {loading && <p>Loading stats...</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}

      {stats && (
        <>
          <h3 style={{ marginTop: "2rem" }}>Column: {stats.column}</h3>

          {/* Numeric stats -> Table */}
          {stats.type === "numeric" && (
            <table
              style={{
                width: "300px",
                border: "1px solid #ddd",
                marginTop: "1rem",
                padding: "0.5rem",
              }}
            >
              <tbody>
                <tr>
                  <th align="left">Min</th>
                  <td>{(stats as NumericStats).min}</td>
                </tr>
                <tr>
                  <th align="left">Max</th>
                  <td>{(stats as NumericStats).max}</td>
                </tr>
                <tr>
                  <th align="left">Avg</th>
                  <td>{(stats as NumericStats).avg}</td>
                </tr>
                <tr>
                  <th align="left">Count</th>
                  <td>{(stats as NumericStats).count}</td>
                </tr>
              </tbody>
            </table>
          )}

          {/* Categorical stats -> Pie chart */}
          {stats.type === "categorical" && (
            <div style={{ width: "400px", height: "300px", marginTop: "1.5rem" }}>
              <ResponsiveContainer>
                <PieChart>
                  <Pie
                    data={(stats as CategoricalStats).values}
                    dataKey="count"
                    nameKey="value"
                    outerRadius={120}
                    fill="#8884d8"
                    label
                  >
                    {(stats as CategoricalStats).values.map((_, index) => (
                      <Cell key={index} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>

                  <Tooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          )}
        </>
      )}
    </div>
  );
}
