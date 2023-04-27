import { Outlet, useLocation, useNavigate } from "react-router-dom";
import NavBar from "./components/NavBar";
import { createContext, useEffect, useState } from "react";
import axios from "axios";

export const userAuth = createContext({
  authToken: "",
  setAuthToken: ((value: string) => {}) as React.Dispatch<
    React.SetStateAction<string>
  >,
});

interface UserInfo {
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

export const user = createContext<{
  userInfo: UserInfo;
  setUserInfo: React.Dispatch<React.SetStateAction<UserInfo>>;
}>({
  userInfo: {
    id: 0,
    username: "",
    email: "",
    profile: {
      name: "",
      image: "",
      bio: "",
      location: "",
      website_url: "",
      following_count: 0,
      followers_count: 0,
      created_at: "",
    },
  },
  setUserInfo: () => {},
});

function App() {
  const [authToken, setAuthToken] = useState("");
  const [userInfo, setUserInfo] = useState<UserInfo>({
    id: 0,
    username: "",
    email: "",
    profile: {
      name: "",
      image: "",
      bio: "",
      location: "",
      website_url: "",
      following_count: 0,
      followers_count: 0,
      created_at: "",
    },
  });

  const navigate = useNavigate();
  const location = useLocation();

  const fetchData = async () => {
    try {
      const response = await axios.get("/api/my-profile", {
        headers: {
          Authorization: `Token ${authToken}`,
        },
      });
      setUserInfo(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    const authTokenFromStorage = localStorage.getItem("authToken");
    if (authTokenFromStorage) {
      setAuthToken(authTokenFromStorage);
    }
    const currentUrl = location.pathname;
    if (currentUrl === "/" && authTokenFromStorage) {
      navigate("home");
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [authToken]);

  return (
    <user.Provider value={{ userInfo, setUserInfo }}>
      <userAuth.Provider value={{ authToken, setAuthToken }}>
        <div className="flex justify-center">
          <NavBar />
          <div className="h-screen w-[600px] lg:border-x-2">
            <Outlet />
          </div>
          <div className="hidden w-[200px] lg:flex"></div>
        </div>
      </userAuth.Provider>
    </user.Provider>
  );
}

export default App;
