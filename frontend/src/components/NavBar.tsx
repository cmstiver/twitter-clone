import { useContext } from "react";
import { Link, useNavigate } from "react-router-dom";
import { user } from "../App";

export default function NavBar() {
  const navigate = useNavigate();

  const { userInfo, setUserInfo } = useContext(user);

  const handleLogout = () => {
    localStorage.removeItem("authToken");
    navigate("/");
  };

  return (
    <nav className="fixed bottom-0 w-full justify-center bg-[#16161d] lg:relative lg:flex lg:h-screen lg:w-[200px]">
      <ul className="flex w-full justify-around py-2 lg:flex-col lg:justify-start">
        <li>
          <Link to="/home">
            <button className="flex items-center rounded-md p-2 text-white hover:bg-[#21212e]">
              <span className="material-symbols-outlined text-4xl">home</span>
              <span className="hidden text-xl lg:block">Home</span>
            </button>
          </Link>
        </li>
        <li>
          <Link to={`/profiles/${userInfo.username}`}>
            <button className="flex items-center rounded-md p-2 text-white hover:bg-[#21212e]">
              <span className="material-symbols-outlined text-4xl">person</span>
              <span className="hidden text-xl lg:block">Profile</span>
            </button>
          </Link>
        </li>
        <li>
          <button
            className="flex items-center rounded-md p-2 text-white hover:bg-[#21212e]"
            onClick={handleLogout}
          >
            <span className="material-symbols-outlined text-4xl">logout</span>
            <span className="hidden text-xl lg:block">Logout</span>
          </button>
        </li>
      </ul>
    </nav>
  );
}
