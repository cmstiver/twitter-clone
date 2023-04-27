import axios from "axios";
import { useContext, useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { formatDate } from "../utilities";
import { likes, user, userAuth } from "../App";
import Tweet from "../components/Tweet";

interface TweetInterface {
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
  parent_tweet: TweetInterface | null;
  content: string;
  image: string | null;
  created_at: string;
  reply_count: number;
  retweet_count: number;
  like_count: number;
  replies: TweetInterface[];
  retweets: TweetInterface[];
  likes: {
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
  }[];
}

interface TweetFormMiniProps {
  id: string;
}

function TweetFormMini({ id }: TweetFormMiniProps) {
  const { userInfo, setUserInfo } = useContext(user);
  const { authToken, setAuthToken } = useContext(userAuth);
  const { likedTweets, setLikedTweets } = useContext(likes);

  const [content, setContent] = useState("");

  const navigate = useNavigate();

  function postTweet() {
    axios
      .post(
        `/api/tweets/${id}/reply`,
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
            navigate(`/profiles/${userInfo.username}`);
          }}
          src={userInfo.profile.image}
          className="h-12 w-12 rounded-full hover:cursor-pointer"
        ></img>
        <textarea
          className="block w-full resize-none bg-inherit outline-none"
          rows={2}
          wrap="soft"
          placeholder="Reply..."
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

export default function TweetDetail() {
  const [tweetData, setTweetData] = useState<TweetInterface | null>(null);

  const id = useParams().id as string;

  const navigate = useNavigate();

  function fetchTweetData() {
    axios
      .get(`/api/tweets/${id}`)
      .then((response) => {
        setTweetData(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }

  useEffect(() => {
    fetchTweetData();
  }, []);

  return (
    <div>
      {tweetData ? (
        <>
          <div className="grid grid-cols-[auto_1fr] gap-2 border-b-2 p-2 text-white ">
            <img
              onClick={(e) => {
                navigate(`/profiles/${tweetData.user.username}`);
              }}
              src={tweetData.user.profile.image}
              className="h-12 w-12 rounded-full hover:cursor-pointer"
            ></img>
            <div>
              <span className="font-bold">{tweetData.user.profile.name}</span>
              <span className="text-gray-400"> @{tweetData.user.username}</span>
              <span className="text-gray-400">
                {" "}
                • {formatDate(tweetData.created_at)}
              </span>
              <div className="my-5">{tweetData.content}</div>
              <div className="flex">
                <button className="my-2 flex align-middle">
                  <span className="material-symbols-outlined not-filled">
                    comment
                  </span>
                  <span className="ml-1">{tweetData.reply_count}</span>
                </button>
                <button className="my-2 ml-4 flex align-middle">
                  <span className="material-symbols-outlined not-filled">
                    favorite
                  </span>
                  <span className="ml-1">{tweetData.like_count}</span>
                </button>
              </div>
            </div>
          </div>
          <TweetFormMini id={id} />
          <div className=" w-full border-b-2 font-bold">
            <div className="m-4 text-white">Replies:</div>
          </div>
          {tweetData.replies.map((data) => {
            return <Tweet tweetData={data} />;
          })}
        </>
      ) : (
        <div className="text-white">Loading tweet details...</div>
      )}
    </div>
  );
}
