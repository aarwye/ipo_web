import React, { useEffect, useState } from "react";
import axios from "axios";
import IPOCard from "./IPOCard";

function App() {
  const [ipos, setIpos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:8000/api/all-ipos/")
      .then((res) => {
        setIpos(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error fetching IPOs:", err);
        setLoading(false);
      });
  }, []);

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>IPO Dashboard</h1>

      {loading ? (
        <p style={styles.loading}>Loading IPO data...</p>
      ) : ipos.length === 0 ? (
        <p style={styles.noData}>No IPOs available</p>
      ) : (
        <div style={styles.cardContainer}>
          {ipos.map((ipo) => (
            <IPOCard key={ipo.id} ipo={ipo} />
          ))}
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    backgroundColor: "#f8f9fa",
    minHeight: "100vh",
    padding: "30px",
    fontFamily: "Arial, sans-serif",
  },
  title: {
    textAlign: "center",
    color: "#0d47a1",
    marginBottom: "30px",
  },
  cardContainer: {
    display: "flex",
    flexWrap: "wrap",
    justifyContent: "center",
  },
  loading: {
    textAlign: "center",
    color: "#757575",
  },
  noData: {
    textAlign: "center",
    color: "#757575",
  },
};

export default App;
