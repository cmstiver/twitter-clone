import { Link, useNavigate } from "react-router-dom";

export default function NavBar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("authToken");
    navigate("/");
  };

  return (
    <nav className="bg fixed bottom-0 w-full justify-center bg-[#16161d] lg:flex lg:h-screen lg:w-[200px]">
      <ul className="flex w-full justify-around">
        <li>
          <Link to="/home">
            <button className="material-symbols-outlined p-5 text-4xl text-white">
              home
            </button>
          </Link>
        </li>
        <li>
          <button className="material-symbols-outlined p-5 text-4xl text-white">
            person
          </button>
        </li>
        <li>
          <button
            className="material-symbols-outlined p-5 text-4xl text-white"
            onClick={handleLogout}
          >
            logout
          </button>
        </li>
      </ul>
    </nav>
  );
}
