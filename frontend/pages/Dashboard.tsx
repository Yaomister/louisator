import "../stylesheets/Dashboard.css";

const Dashboard = () => {
  return (
    <div className="dashboard">
      <div className="activity">
        <div className="live-view-wrapper">
          <img className="live-view" src="/images/black.png"></img>
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
