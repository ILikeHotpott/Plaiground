import React, { useState } from "react";
import Post from "./Post";
import mockPosts from "../data/mock.js";

const MainContent = () => {
  const [selectedTab, setSelectedTab] = useState("For you"); // 控制选中状态

  return (
      <div
          className="absolute top-0 left-0 w-full h-screen overflow-y-auto border-gray-700"
          style={{paddingLeft: "26.666%", paddingRight: "33.333%"}}
      > {/* 顶部固定导航 */}
        <div className="sticky top-0 bg-black/60 backdrop-blur-md z-20 border-r border-b border-gray-700">
          <div className="flex">
            {/* For You 按钮 */}
            <div
                onClick={() => setSelectedTab("For you")}
                className={`relative w-1/2 py-4 text-center cursor-pointer ${
                    selectedTab === "For you" ? "text-white font-bold" : "text-gray-400"
                } hover:bg-gray-800`}
            >
              <span className="inline-block">For you</span>
              {selectedTab === "For you" && (
                  <div
                      className="absolute bottom-0 left-1/2 transform -translate-x-1/2 h-[4px] rounded-full"
                      style={{width: "60px", backgroundColor: "#4a99e9"}}
                  ></div>
              )}
            </div>

            {/* Following 按钮 */}
            <div
                onClick={() => setSelectedTab("Following")}
                className={`relative w-1/2 py-4 text-center cursor-pointer ${
                    selectedTab === "Following" ? "text-white font-bold" : "text-gray-400"
                } hover:bg-gray-800`}
            >
              <span className="inline-block">Following</span>
              {selectedTab === "Following" && (
                  <div
                      className="absolute bottom-0 left-1/2 transform -translate-x-1/2 h-[4px] rounded-full"
                      style={{width: "90px", backgroundColor: "#4a99e9"}}
                  ></div>
              )}
            </div>
          </div>
        </div>

        {/* 帖子列表 */}
        {mockPosts.map((post, index) => (
            <div key={index} className="border-r border-b border-gray-700 w-full">
              <Post
                  username={post.username}
                  date={post.date}
                  content={post.content}
                  image={post.image}
              />
            </div>
        ))}
      </div>
  );
};

export default MainContent;