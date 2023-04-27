import { useState, useEffect, useContext } from "react";
import axios from "axios";
import Tweet from "../components/Tweet";
import TweetForm from "../components/TweetForm";
import { userAuth } from "../App";

export default function HomePage() {
  const { authToken, setAuthToken } = useContext(userAuth);

  const [tweets, setTweets] = useState([]);

  function fetchAllTweets() {
    axios
      .get("/api/tweets")
      .then((response) => {
        setTweets(response.data);
      })
      .catch((error) => {
        console.log(error);
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
      })
      .catch((error) => {
        console.log(error);
      });
  }

  useEffect(() => {
    fetchAllTweets();
  }, []);

  return (
    <>
      <div className="flex">
        <button
          onClick={fetchAllTweets}
          className="border-r-1 flex flex-grow justify-center border-b-2 py-5 text-white"
        >
          All Posts
        </button>
        <button
          onClick={fetchFollowingTweets}
          className="flex flex-grow justify-center border-l-2 border-b-2 py-5 text-white"
        >
          My Feed
        </button>
      </div>
      <TweetForm />

      {tweets.map((tweet) => {
        return <Tweet tweetData={tweet} />;
      })}
    </>
  );
}
