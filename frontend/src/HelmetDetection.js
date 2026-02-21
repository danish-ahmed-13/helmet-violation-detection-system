import React, { useState } from "react";

function HelmetDetection() {
  const [detections, setDetections] = useState([]);
  const [loading, setLoading] = useState(false);

  const runDetection = async () => {
    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:5000/detect");
      const data = await response.json();

      // If backend returns error message
      if (data.error || data.message) {
        alert(data.error || data.message);
        setDetections([]);
      } else {
        setDetections(data);
      }
    } catch (err) {
      console.error(err);
      alert("Failed to fetch detections from backend.");
    }

    setLoading(false);
  };

  return (
    <div>
      <h2>Helmet Violation Detection</h2>
      <button onClick={runDetection} disabled={loading}>
        {loading ? "Running Detection..." : "Run Detection"}
      </button>

      {detections.length > 0 && (
        <table border="1" style={{ marginTop: "20px", width: "100%" }}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Vehicle Type</th>
              <th>Helmet Status</th>
              <th>Confidence</th>
              <th>Image</th>
            </tr>
          </thead>
          <tbody>
            {detections.map((det) => (
              <tr key={det.id}>
                <td>{det.id}</td>
                <td>{det.vehicle_type}</td>
                <td
                  style={{
                    color: det.helmet_status === "violation" ? "red" : "green",
                  }}
                >
                  {det.helmet_status}
                </td>
                <td>{(det.confidence * 100).toFixed(2)}%</td>
                <td>
                  <img
                    src={`http://127.0.0.1:5000/${det.image_saved}`}
                    alt="vehicle"
                    width="150"
                  />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}

export default HelmetDetection;
