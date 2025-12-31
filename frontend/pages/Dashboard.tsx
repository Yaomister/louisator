import { useEffect, useState } from "react";
import { CartesianGrid, Line, LineChart, XAxis, YAxis } from "recharts";

import "../stylesheets/Dashboard.css";

type State = {
  speed: number;
  activity: string;
  time: number;
};

const Dashboard = () => {
  const [img, setImg] = useState<string | null>(null);
  const [data, setData] = useState<State[]>([]);
  const [events, setEvents] = useState<State[]>([]);

  useEffect(() => {
    const websockets = [
      new WebSocket("ws://localhost:8000/camera"),
      new WebSocket("ws://localhost:8000/data"),
      new WebSocket("ws://localhost:8000/events"),
    ];

    for (const websocket of websockets) {
      websocket.binaryType = "arraybuffer";

      websocket.onerror = (err) => {
        console.error("Websocket error: ", err);
      };
    }

    websockets[0].onmessage = (payload) => {
      const blob = new Blob([payload.data], { type: "image/png" });
      const url = URL.createObjectURL(blob);
      setImg(url);
    };

    websockets[1].onmessage = (payload) => {
      const _data = JSON.parse(payload.data);
      setData((prev) => [...prev, _data]);
    };

    websockets[2].onmessage = (payload) => {
      const _data = JSON.parse(payload.data);
      setEvents((prev) => [...prev, _data.message]);
    };

    return () => {
      for (const websocket of websockets) {
        websocket.close();
      }
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
        <div className="encounterments">
          {events.map((message) => {
            return <div>{message}</div>;
          })}
        </div>
      </div>
      <div className="analytics">
        <div className="acitivity-distribution-graph graph">
          <LineChart
            style={{ width: "100%", height: "100%" }}
            responsive
            data={data.slice(data.length > 20 ? data.length - 20 : 0)}
          >
            <CartesianGrid strokeDasharray="5 5" stroke="#eee" />
            <YAxis width={"auto"} />
            <XAxis dataKey={"time"} />
            <Line dataKey={"speed"} />
          </LineChart>
        </div>
        <div className="num-obj-detected-graph graph">
          <LineChart
            style={{ width: "100%", height: "100%" }}
            responsive
            data={data.slice(data.length > 20 ? data.length - 20 : 0)}
          >
            <CartesianGrid strokeDasharray="5 5" stroke="#eee" />
            <YAxis width={"auto"} />
            <XAxis dataKey={"time"} />
            <Line dataKey={"num_obj_detect"} />
          </LineChart>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
