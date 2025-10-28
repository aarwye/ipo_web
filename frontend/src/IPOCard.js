import React from "react";

const IPOCard = ({ ipo }) => {
  return (
    <div style={styles.card}>
      <h2 style={styles.company}>{ipo.company_name}</h2>
      <p><strong>Price Band:</strong> {ipo.price_band}</p>
      <p><strong>Open Date:</strong> {ipo.open_date}</p>
      <p><strong>Close Date:</strong> {ipo.close_date}</p>
      <p><strong>Issue Size:</strong> {ipo.issue_size}</p>
      <p><strong>Issue Type:</strong> {ipo.issue_type}</p>
      <p><strong>Listing Date:</strong> {ipo.listing_date || "—"}</p>
      <p><strong>Status:</strong> {ipo.status}</p>
      <p><strong>IPO Price:</strong> ₹{ipo.ipo_price || "—"}</p>
      <p><strong>Listing Price:</strong> ₹{ipo.listing_price || "—"}</p>
      <p><strong>Listing Gain:</strong> {ipo.listing_gain || "—"}</p>
    </div>
  );
};

const styles = {
  card: {
    background: "#fff",
    borderRadius: "12px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.1)",
    padding: "20px",
    margin: "15px",
    width: "300px",
    transition: "transform 0.2s ease",
  },
  company: {
    fontSize: "1.3rem",
    color: "#1a237e",
    marginBottom: "10px",
  },
};

export default IPOCard;
