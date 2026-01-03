import { useEffect, useState } from "react";
import {
  CartesianGrid,
  Line,
  LineChart,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { Toaster } from "react-hot-toast";

import { AddKnownFacesForm } from "../components/AddKnownFacesForm";

import "../stylesheets/Dashboard.css";

type State = {
  speed: number;
  activity: string;
  time: Date;
};

type Message = {
  message: string;
  time: Date;
};

const Dashboard = () => {
  const [img, setImg] = useState<string | null>(null);
  const [data, setData] = useState<State[]>([]);
  const [events, setEvents] = useState<Message[]>([]);

  const [showAddKnownFacesForm, setShowAddKnownFacesForm] = useState(false);

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
      setData((prev) => [
        ...prev,
        {
          ..._data,
          time: new Date(_data.time * 1000).toLocaleTimeString("en-GB", {
            hour12: false,
          }),
        },
      ]);
    };

    websockets[2].onmessage = (payload) => {
      const _data = JSON.parse(payload.data);
      setEvents((prev) => [
        {
          ..._data,
          time: new Date(_data.time * 1000).toLocaleTimeString("en-GB", {
            hour12: false,
          }),
        },
        ...prev,
      ]);
    };

    return () => {
      for (const websocket of websockets) {
        websocket.close();
      }
    };
  }, []);

  return (
    <div className="dashboard">
      <Toaster position="top-right" />
      {showAddKnownFacesForm && (
        <AddKnownFacesForm
          close={() => {
            setShowAddKnownFacesForm(false);
          }}
        />
      )}
      <div className="activity">
        <div className="live-view-wrapper">
          <img className="live-view" src={img ? img : "/images/black.png"} />
          <button
            className="add-known-faces-button"
            onClick={() => {
              setShowAddKnownFacesForm(true);
            }}
          >
            Add Known Faces
          </button>
        </div>
        <div className="events-wrapper">
          <h2 className="events-title">Events</h2>
          <div className="events">
            {events.map((message) => {
              return (
                <p className="event-text">{`${message.time}: ${message.message}`}</p>
              );
            })}
          </div>
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
            <Line dataKey={"speed"} type={"monotone"} />
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
            <Line dataKey={"num_obj_detect"} type={"monotone"} />
            <Tooltip cursor={{ strokeDasharray: "3 3" }} />
          </LineChart>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
