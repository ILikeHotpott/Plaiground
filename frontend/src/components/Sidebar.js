import React from "react";
import {
    FaHome,
    FaSearch,
    FaBell,
    FaEnvelope,
    FaUser,
} from "react-icons/fa";

const Sidebar = () => {
    return (
        <div
            className="sidebar w-[26.666%] h-screen pl-32 py-4 border-r border-gray-700 flex flex-col items-start fixed top-0 left-0 overflow-y-auto z-10">
            <div className="flex flex-col items-start w-full">
                <div className="text-2xl font-bold mb-4">X</div>
                {/* 垂直间距调整 */}
                <div className="space-y-0 w-full">
                    <SidebarItem icon={<FaHome/>} label="Home"/>
                    <SidebarItem icon={<FaSearch/>} label="Explore"/>
                    <SidebarItem icon={<FaBell/>} label="Notifications"/>
                    <SidebarItem icon={<FaEnvelope/>} label="Messages"/>
                    <SidebarItem icon={<FaUser/>} label="Profile"/>
                </div>
            </div>
            <div className="flex flex-col items-start mt-4 w-full">
                <div className="flex items-center space-x-2">
                    <img
                        src="https://placehold.co/40x40"
                        alt="User profile"
                        className="rounded-full"
                    />
                    <div>
                        <div className="font-bold">Vista</div>
                        <div className="text-gray-500">@loveIsJustALie1</div>
                    </div>
                </div>
            </div>
        </div>
    );
};

const SidebarItem = ({icon, label}) => (
    <div
        className="flex items-center space-x-3 p-3 rounded-full cursor-pointer hover:bg-gray-800 transition-colors duration-200 w-full">
        <div className="text-xl">{icon}</div>
        <span className="text-lg">{label}</span>
    </div>
);

export default Sidebar;