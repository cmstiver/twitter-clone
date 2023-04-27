import { useState, useEffect } from "react";
import axios from "axios";
import Tweet from "../components/Tweet";

export default function HomePage() {
  const [tweets, setTweets] = useState([]);

  useEffect(() => {
    axios
      .get("/api/tweets")
      .then((response) => {
        setTweets(response.data);
      })
      .catch((error) => {
        console.log(error);
      });
  }, []);

  return (
    <>
      <div className="flex">
        <button className="border-r-1 flex flex-grow justify-center border-b-2 py-5 text-white">
          All Posts
        </button>
        <button className="flex flex-grow justify-center border-l-2 border-b-2 py-5 text-white">
          My Feed
        </button>
      </div>
      {tweets.map((tweet) => {
        return <Tweet tweetData={tweet} />;
      })}
    </>
  );
}
