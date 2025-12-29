import { useEffect, useState } from "react";

import "../stylesheets/Dashboard.css";

const Dashboard = () => {
  const [img, setImg] = useState<string>("");
  const [data, setData] = useState(null);

  useEffect(() => {
    const websocket = new WebSocket("ws://localhost:8000/camera");

    websocket.binaryType = "arraybuffer";

    websocket.onmessage = (payload) => {
      const blob = new Blob([payload.data], { type: "image/png" });
      const url = URL.createObjectURL(blob);
      setImg(url);
    };

    websocket.onerror = (err) => {
      console.error("WebSocket error: ", err);
    };

    return () => {
      websocket.close();
    };
  }, []);

  useEffect(() => {
    const websocket = new WebSocket("ws://localhost:8000/data");

    websocket.binaryType = "arraybuffer";

    websocket.onmessage = (payload) => {
      //   setData(payload);
      console.error(payload);
    };

    websocket.onerror = (err) => {
      console.error("WebSocket error: ", err);
    };

    return () => {
      websocket.close();
    };
  }, []);

  return (
    <div className="dashboard">
      <div className="activity">
        <div className="live-view-wrapper">
          <img
            className="live-view"
            src={img ? img : "/images/black.png"}
          ></img>
        </div>
        <div className="encounterments"></div>
      </div>
      <div className="analytics">
        <div className="movement-over-time-graph graph"></div>
        <div className="acitivity-distribution-graph graph"></div>
      </div>
    </div>
  );
};

export default Dashboard;
