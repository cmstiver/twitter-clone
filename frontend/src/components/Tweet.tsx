import { useContext, useEffect, useState } from "react";
import { likes, user, userAuth } from "../App";
import axios from "axios";
import { Link, useNavigate } from "react-router-dom";
import { getRelativeTime } from "../utilities";

interface Tweet {
  id: number;
  user: {
    id: number;
    username: string;
    email: string;
    profile: {
      name: string;
      image: string;
      bio: string;
      location: string;
      website_url: string;
      following_count: number;
      followers_count: number;
      created_at: string;
    };
  };
  content: string;
  image: string | null;
  created_at: string;
  reply_count: number;
  retweet_count: number;
  like_count: number;
}

interface TweetProps {
  tweetData: Tweet;
}

const Tweet: React.FC<TweetProps> = ({ tweetData }) => {
  const { authToken, setAuthToken } = useContext(userAuth);
  const { likedTweets, setLikedTweets } = useContext(likes);

  const navigate = useNavigate();

  const [isLiked, setIsLiked] = useState(false);

  function createLike() {
    try {
      axios.post(
        `/api/tweets/${tweetData.id}/like`,
        {},
        {
          headers: {
            Authorization: `Token ${authToken}`,
          },
        }
      );
    } catch (error) {
      console.error(error);
    } finally {
      if (isLiked === false) {
        tweetData.like_count += 1;
        setIsLiked(true);
      } else {
        tweetData.like_count -= 1;
        setIsLiked(false);
      }
    }
  }

  useEffect(() => {
    if (Array.isArray(likedTweets)) {
      likedTweets.forEach((likedTweet) => {
        if (likedTweet.id == tweetData.id) {
          setIsLiked(true);
        }
      });
    }
  }, [likedTweets]);

  return (
    <div
      onClick={() => {
        navigate(`/tweets/${tweetData.id}`);
        window.location.reload();
      }}
      className="grid grid-cols-[auto_1fr] gap-2 border-b-2 p-2 text-white hover:cursor-pointer hover:bg-[#2c2c39]"
    >
      <img
        onClick={(e) => {
          e.stopPropagation();
          navigate(`/profiles/${tweetData.user.username}`);
        }}
        src={tweetData.user.profile.image}
        className="h-12 w-12 rounded-full"
      ></img>
      <div>
        <span className="font-bold">{tweetData.user.profile.name}</span>
        <span className="text-gray-400"> @{tweetData.user.username}</span>
        <span className="text-gray-400">
          {" "}
          • {getRelativeTime(tweetData.created_at)}
        </span>
        <div>{tweetData.content}</div>
        <div className="flex">
          <button className="flex rounded-md py-2 px-1 align-middle hover:bg-[#4d7eac]">
            <span className="material-symbols-outlined not-filled">
              comment
            </span>
            <span className="ml-1">{tweetData.reply_count}</span>
          </button>
          <button
            onClick={(e) => {
              e.stopPropagation();
              createLike();
            }}
            className="ml-4 flex rounded-md py-2 px-1 align-middle hover:bg-[#824343]"
          >
            <span
              className={`material-symbols-outlined  ${
                isLiked ? "text-red-600" : "not-filled"
              }`}
            >
              favorite
            </span>
            <span className="ml-1">{tweetData.like_count}</span>
          </button>
        </div>
      </div>
    </div>
  );
};

export default Tweet;
