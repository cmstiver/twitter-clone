import ReactDOM from "react-dom/client";
import App from "./App";
import "./index.css";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import HomePage from "./pages/HomePage";
import Auth from "./pages/Auth";
import TweetDetail from "./pages/TweetDetail";
import UserProfile from "./pages/UserProfile";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        index: true,
        element: <Auth />,
      },
      {
        path: "home",
        element: <HomePage />,
      },
      {
        path: "tweets/:id",
        element: <TweetDetail />,
      },
      {
        path: "profiles/:username",
        element: <UserProfile />,
      },
    ],
  },
]);

const rootElement = document.getElementById("root") as Element;

ReactDOM.createRoot(rootElement).render(<RouterProvider router={router} />);
