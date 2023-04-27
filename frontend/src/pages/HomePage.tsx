import { useState, useEffect, useContext } from "react";
import axios from "axios";
import Tweet from "../components/Tweet";
import TweetForm from "../components/TweetForm";
import { user, userAuth } from "../App";

export default function HomePage() {
  const { authToken, setAuthToken } = useContext(userAuth);
  const { userInfo, setUserInfo } = useContext(user);

  const [currentTab, setCurrentTab] = useState("All Posts");

  const [tweets, setTweets] = useState([]);

  function fetchAllTweets() {
    axios
      .get("/api/tweets")
      .then((response) => {
        setTweets(response.data);
        setCurrentTab("All Posts");
      })
      .catch((error) => {
        console.error(error);
      });
  }

  function fetchFollowingTweets() {
    axios
      .get("/api/following_tweets", {
        headers: {
          Authorization: `Token ${authToken}`,
        },
      })
      .then((response) => {
        setTweets(response.data);
        setCurrentTab("My Feed");
      })
      .catch((error) => {
        console.error(error);
      });
  }

  useEffect(() => {
    fetchAllTweets();
  }, [userInfo]);

  return (
    <>
      <div className="flex">
        <button
          onClick={fetchAllTweets}
          className={`border-r-1 flex flex-grow justify-center border-b-8 py-5 text-white ${
            currentTab === "All Posts"
              ? "border-b-8 border-blue-400 bg-[#2c2c39]"
              : ""
          }`}
        >
          All Posts
        </button>
        <button
          onClick={fetchFollowingTweets}
          className={`flex flex-grow justify-center border-b-8 py-5 text-white ${
            currentTab === "My Feed"
              ? "border-b-8 border-blue-400 bg-[#2c2c39]"
              : ""
          }`}
        >
          My Feed
        </button>
      </div>
      <TweetForm />

      {tweets.map((tweet) => {
        if (!tweet["parent_tweet"]) {
          return <Tweet tweetData={tweet} />;
        }
      })}
    </>
  );
}
