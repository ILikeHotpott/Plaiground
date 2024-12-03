import React from "react";
import { FaCheckCircle } from "react-icons/fa";

const Post = ({ username, date, content, image }) => {
    return (
        <div className="pb-4">
            <div className="bg-black text-white shadow-lg rounded-lg">
                {/* Header Section */}
                <div className={"p-2"}>
                    <div className="flex items-center space-x-4">
                        <img
                            src="https://placehold.co/50x50" // Placeholder profile image
                            alt="Profile"
                            className="rounded-full w-12 h-12"
                        />
                        <div>
                            <div className="flex items-center space-x-2">
                                <span className="font-bold text-lg">{username}</span>
                                <FaCheckCircle className="text-blue-500" />
                            </div>
                            <div className="text-gray-400 text-sm">{date}</div>
                        </div>
                    </div>

                    {/* Post Content */}
                    <div className="mt-4 text-gray-300">
                        {content.split("\n").map((line, index) => (
                            <p key={index}>{line}</p>
                        ))}
                    </div>
                </div>

                {/* Image Section */}
                {image && (
                    <div className="mt-4">
                        <img
                            src={image}
                            alt="Post content"
                            className="w-full h-auto rounded-lg"
                        />
                    </div>
                )}

                {/* Footer Section */}
                <div className="px-8 mt-4 flex items-center text-gray-400 text-sm space-x-4">
                    <span>4,174点赞</span>
                    <span>320条评论</span>
                    <span>241次分享</span>
                </div>
            </div>
        </div>
    );
};

export default Post;