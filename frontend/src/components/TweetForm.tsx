import { useContext, useEffect, useState } from "react";
import { user, userAuth } from "../App";
import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function TweetForm() {
  const { userInfo, setUserInfo } = useContext(user);
  const { authToken, setAuthToken } = useContext(userAuth);
  const navigate = useNavigate();

  const [content, setContent] = useState("");

  function postTweet() {
    axios
      .post(
        "/api/tweets",
        {
          content,
        },
        {
          headers: {
            Authorization: `Token ${authToken}`,
          },
        }
      )
      .then((response) => {
        console.log("Tweet posted successfully!");
        window.location.reload();
      })
      .catch((error) => {
        console.error("Error posting tweet:", error);
      });
  }

  return (
    <div className="relative border-b-2 pb-12">
      <div className="grid grid-cols-[auto_1fr] gap-2 p-2 text-white">
        <img
          onClick={(e) => {
            e.stopPropagation();
            navigate(`/profiles/${userInfo.username}`);
          }}
          src={userInfo.profile.image}
          className="h-12 w-12 rounded-full hover:cursor-pointer"
        ></img>
        <textarea
          className="block w-full resize-none bg-inherit outline-none"
          rows={3}
          wrap="soft"
          placeholder="What's happening?"
          onChange={(e) => setContent(e.target.value)}
        ></textarea>
      </div>
      <button
        onClick={postTweet}
        className="absolute right-3 rounded-[100px] bg-blue-500 py-2 px-4"
      >
        Send
      </button>
    </div>
  );
}
