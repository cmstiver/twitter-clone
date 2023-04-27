import { Outlet, useLocation, useNavigate } from "react-router-dom";
import NavBar from "./components/NavBar";
import { createContext, useEffect, useState } from "react";

export const userAuth = createContext({
  authToken: "",
  setAuthToken: ((value: string) => {}) as React.Dispatch<
    React.SetStateAction<string>
  >,
});

function App() {
  const [authToken, setAuthToken] = useState("");
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const authTokenFromStorage = localStorage.getItem("authToken");
    if (authTokenFromStorage) {
      setAuthToken(authToken);
    }
    const currentUrl = location.pathname;
    if (currentUrl === "/" && authTokenFromStorage) {
      navigate("home");
    }
  }, []);

  return (
    <userAuth.Provider value={{ authToken, setAuthToken }}>
      <div className="flex justify-center">
        <NavBar />
        <div className="h-screen w-[600px] lg:border-x-2">
          <Outlet />
        </div>
        <div className="hidden w-[200px] lg:flex"></div>
      </div>
    </userAuth.Provider>
  );
}

export default App;
