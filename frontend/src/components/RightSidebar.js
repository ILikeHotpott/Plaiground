import React from "react";

const RightSidebar = () => {
  return (
    <div className="right-sidebar  w-[33.333%] h-screen p-4 fixed top-0 right-0 overflow-y-auto z-10">
      {/* 子内容容器，宽度占 RightSidebar 的 70%，水平居中 */}
      <div className="w-[85%] mx-auto">
        <div className="mb-4">
          <input
            type="text"
            placeholder="Search"
            className="bg-gray-800 text-white w-full p-2 rounded-full"
          />
        </div>
        <div className="bg-gray-800 p-4 rounded-2xl mb-4">
          <div className="font-bold mb-2">Subscribe to Premium</div>
          <div className="text-gray-500 mb-2">
            Subscribe to unlock new features and if eligible, receive a share of
            revenue.
          </div>
          <button className="bg-blue-500 text-white py-1 px-4 rounded-full">
            Subscribe
          </button>
        </div>
        <Trending />
        <WhoToFollow />
      </div>
    </div>
  );
};

const Trending = () => (
  <div className="bg-gray-800 p-4 rounded-2xl mb-4">
    <div className="font-bold mb-2">What's happening</div>
    {/* Trending topics can be mapped here */}
    <div className="text-blue-500 cursor-pointer">Show more</div>
  </div>
);

const WhoToFollow = () => (
  <div className="bg-gray-800 p-4 rounded-2xl">
    <div className="font-bold mb-2">Who to follow</div>
    {/* Suggestions can be mapped here */}
  </div>
);

export default RightSidebar;