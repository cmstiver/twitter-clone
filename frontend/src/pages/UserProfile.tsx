import axios from "axios";
import { useContext, useEffect, useState } from "react";
import { user, userAuth } from "../App";
import { useParams } from "react-router-dom";
import { formatDate } from "../utilities";
import Tweet from "../components/Tweet";

interface UserProfile {
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
}

export default function UserProfile() {
  const { authToken, setAuthToken } = useContext(userAuth);
  const { userInfo, setUserInfo } = useContext(user);

  const [profileData, setProfileData] = useState<UserProfile | null>(null);
  const [currentTab, setCurrentTab] = useState("All Posts");
  const [isFollowing, setIsFollowing] = useState(false);

  const [tweets, setTweets] = useState([]);

  const username = useParams().username as string;

  function fetchProfileData() {
    axios
      .get(`/api/profiles/${username}`)
      .then((response) => {
        setProfileData(response.data);
      })
      .catch((error) => {
        console.error(error);
      });
  }

  function fetchUserTweets() {
    axios
      .get(`/api/profiles/${username}/tweets`)
      .then((response) => {
        setTweets(response.data);
        setCurrentTab("Tweets");
      })
      .catch((error) => {
        console.log(error);
      });
  }

  function fetchLikedTweets() {
    axios
      .get(`/api/profiles/${username}/likes`)
      .then((response) => {
        setTweets(response.data);
        setCurrentTab("Likes");
      })
      .catch((error) => {
        console.error(error);
      });
  }

  function followToggle() {
    axios
      .post(
        `/api/profiles/${username}/follow`,
        {},
        {
          headers: {
            Authorization: `Token ${authToken}`,
          },
        }
      )
      .then((response) => {
        window.location.reload();
      })
      .catch((error) => {
        console.log(error);
      });
  }

  function isCurrentUser() {
    if (userInfo.username !== profileData?.username) {
      return true;
    } else {
      return false;
    }
  }

  function checkFollowing() {
    axios
      .get(`/api/profiles/${username}/followers`)
      .then((response) => {
        response.data.map((user: { username: string }) => {
          if (user.username === userInfo.username) {
            setIsFollowing(true);
          }
        });
      })
      .catch((error) => {
        console.error(error);
      });
    setIsFollowing(false);
  }

  useEffect(() => {
    fetchProfileData();
    fetchUserTweets();
    checkFollowing();
  }, [userInfo]);

  return (
    <>
      {profileData ? (
        <>
          <div className="relative mb-5">
            <div className="h-[100px] bg-blue-600"></div>
            <img
              src={profileData.profile.image}
              className="absolute top-[30px] left-[20px] h-32 w-32 rounded-full"
            ></img>
            {isCurrentUser() ? (
              isFollowing ? (
                <button
                  onClick={followToggle}
                  className="absolute right-4 mt-4 rounded-lg bg-red-600 px-4 py-2"
                >
                  Unfollow
                </button>
              ) : (
                <button
                  onClick={followToggle}
                  className="absolute right-4 mt-4 rounded-lg bg-blue-600 px-4 py-2"
                >
                  Follow
                </button>
              )
            ) : null}

            <div className="mt-[65px] ml-4 text-white">
              <div className=" text-2xl font-bold">
                {profileData.profile.name}
              </div>
              <div className="text-gray-400">@{profileData.username}</div>
              <div className="text-gray-400">
                Joined {formatDate(profileData.profile.created_at)}
              </div>
              <span className="m-2 ml-0 hover:cursor-pointer hover:underline">
                {profileData.profile.following_count} following
              </span>
              <span className="m-2 hover:cursor-pointer hover:underline">
                {profileData.profile.followers_count} followers
              </span>
            </div>
          </div>
          <div className="flex">
            <button
              onClick={fetchUserTweets}
              className={`border-r-1 flex flex-grow justify-center border-b-8 py-5 text-white ${
                currentTab === "Tweets"
                  ? "border-b-8 border-blue-400 bg-[#2c2c39]"
                  : ""
              }`}
            >
              Tweets
            </button>
            <button
              onClick={fetchLikedTweets}
              className={`flex flex-grow justify-center border-b-8 py-5 text-white ${
                currentTab === "Likes"
                  ? "border-b-8 border-blue-400 bg-[#2c2c39]"
                  : ""
              }`}
            >
              Likes
            </button>
          </div>
          {tweets.map((tweet) => {
            if (currentTab === "Likes" || !tweet["parent_tweet"]) {
              return <Tweet tweetData={tweet} />;
            }
          })}
        </>
      ) : (
        <div className="text-white">Loading Profile...</div>
      )}
    </>
  );
}
