import React, { Component } from "react";

class Footer extends Component {
  render() {
    const defaultStyle = {
      color: "#764abc",
      fontWeight: "bold",
    };

    return (
      <footer
        style={{
          padding: "0.5em",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          fontSize: "14px",
          backgroundColor: "white",
        }}
      >
        <p>
          <span style={defaultStyle}>Zuckerburgers IDE</span>
        </p>
        <p>
          <span style={defaultStyle}>Hypercube</span>
        </p>
      </footer>
    );
  }
}

export default Footer;
