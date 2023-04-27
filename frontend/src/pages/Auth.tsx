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
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h2>Login</h2>
      <label>
        Username:
        <input
          type="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </label>
      <label>
        Password:
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </label>
      <button onClick={handleLogin}>Login</button>
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
      console.error(error);
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
    } catch (error) {
      console.error(error);
      return;
    }
  };

  return (
    <div>
      <h2>Signup</h2>
      <label>
        Username:
        <input
          type="username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
      </label>
      <label>
        Handle:
        <input
          type="handle"
          value={handle}
          onChange={(e) => setHandle(e.target.value)}
        />
      </label>
      <label>
        Password:
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
      </label>
      <label>
        Confirm Password:
        <input
          type="password"
          value={confirmPassword}
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
      </label>
      <button onClick={handleSignup}>Sign Up</button>
    </div>
  );
};

const Auth = () => {
  return (
    <div>
      <LoginForm />
      <SignupForm />
    </div>
  );
};

export default Auth;
