import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const LoginForm = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = async () => {
    try {
      const response = await axios.post("/api/obtain-auth", {
        username,
        password,
      });
      const token = response.data.token;
      localStorage.setItem("authToken", token);
      navigate("home");
      location.reload();
    } catch (error) {
      alert(error);
    }
  };

  return (
    <div className="flex flex-col items-center text-white">
      <h2 className="my-10 text-3xl">Login</h2>
      <input
        id="username"
        className="h-12 w-full border-b-2 bg-inherit"
        type="username"
        value={username}
        placeholder="Username..."
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        id="password"
        className="h-12 w-full border-b-2 bg-inherit"
        type="password"
        value={password}
        placeholder="Password..."
        onChange={(e) => setPassword(e.target.value)}
      />
      <button className="material-symbols-outlined m-10" onClick={handleLogin}>
        login
      </button>
    </div>
  );
};

const SignupForm = () => {
  const [username, setUsername] = useState("");
  const [handle, setHandle] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const navigate = useNavigate();

  const handleSignup = async () => {
    if (password !== confirmPassword) {
      console.log("Passwords do not match.");
      return;
    }

    try {
      const response = await axios.post("/api/register", {
        username,
        password,
        profile: { name: handle },
      });
    } catch (error) {
      alert(error);
      return;
    }

    try {
      const response = await axios.post("/api/obtain-auth", {
        username,
        password,
      });
      const token = response.data.token;
      localStorage.setItem("authToken", token);
      navigate("home");
      location.reload();
    } catch (error) {
      alert(error);
      return;
    }
  };

  return (
    <div className="flex flex-col items-center text-white">
      <h2 className="my-10 text-3xl">Signup</h2>
      <input
        className="h-12 w-full border-b-2 bg-inherit"
        type="username"
        value={username}
        placeholder="Username (Unique)..."
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        className="h-12 w-full border-b-2 bg-inherit"
        type="handle"
        value={handle}
        placeholder="Handle (Non-Unique)..."
        onChange={(e) => setHandle(e.target.value)}
      />

      <input
        className="h-12 w-full border-b-2 bg-inherit"
        type="password"
        value={password}
        placeholder="Password..."
        onChange={(e) => setPassword(e.target.value)}
      />

      <input
        className="h-12 w-full border-b-2 bg-inherit"
        type="password"
        value={confirmPassword}
        placeholder="Confirm Password..."
        onChange={(e) => setConfirmPassword(e.target.value)}
      />

      <button className="material-symbols-outlined m-10" onClick={handleSignup}>
        login
      </button>
    </div>
  );
};

const Auth = () => {
  const navigate = useNavigate();

  const createRandomUser = async () => {
    try {
      const response = await axios.post("/api/register_random");
      console.log(response.data);
      const token = response.data.auth_token;
      localStorage.setItem("authToken", token);
      navigate("home");
      location.reload();
    } catch (error) {
      alert(error);
      return;
    }
  };

  return (
    <div className="flex flex-col items-center">
      <button
        onClick={createRandomUser}
        className="mt-20 w-[200px] rounded-lg bg-blue-400 font-bold"
      >
        Create Random User
      </button>
      <LoginForm />
      <SignupForm />
    </div>
  );
};

export default Auth;
