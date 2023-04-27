interface TweetData {
  tweetData: {
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
  };
}

const Tweet: React.FC<TweetData> = ({ tweetData }) => {
  console.log(tweetData);

  function getRelativeTime(timestamp: string): string {
    const now = new Date();
    const created = new Date(timestamp);

    const elapsedMs = now.getTime() - created.getTime();

    const MINUTE_MS = 60 * 1000;
    const HOUR_MS = 60 * MINUTE_MS;
    const DAY_MS = 24 * HOUR_MS;

    if (elapsedMs < MINUTE_MS) {
      return "Just now";
    } else if (elapsedMs < HOUR_MS) {
      const minutes = Math.floor(elapsedMs / MINUTE_MS);
      return `${minutes}m`;
    } else if (elapsedMs < DAY_MS) {
      const hours = Math.floor(elapsedMs / HOUR_MS);
      return `${hours}h`;
    } else {
      const month = created.toLocaleString("default", { month: "long" });
      const day = created.getDate();
      const year = created.getFullYear();
      if (year === now.getFullYear()) {
        return `${month} ${day}`;
      } else {
        return `${month} ${day}, ${year}`;
      }
    }
  }

  return (
    <div className="grid grid-cols-[auto_1fr] gap-2 border-b-2 p-2 text-white">
      <img
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
      </div>
    </div>
  );
};

export default Tweet;
