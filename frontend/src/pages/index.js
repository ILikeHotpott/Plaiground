import React from "react";
import "../globals.css";
import Sidebar from "../components/Sidebar";
import MainContent from "../components/MainContent";
import RightSidebar from "../components/RightSidebar";

const Home = () => {
  return (
    <div className="relative bg-black text-white h-screen w-screen">
      {/* MainContent now occupies full width */}
      <MainContent />
      {/* Sidebar */}
      <Sidebar />
      {/* RightSidebar */}
      <RightSidebar />
    </div>
  );
};

export default Home;