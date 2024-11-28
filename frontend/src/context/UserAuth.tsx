// Importing required dependencies
import axios, { Axios, AxiosError } from "axios"; // Importing Axios for HTTP requests
import { createContext, useEffect, useState } from "react"; // React hooks for state and context management
import { useNavigate } from "react-router-dom"; // Hook to navigate between routes

// Interface defining the structure of the UserContext, which will provide user authentication functionality
interface UserContextInterface {
  username: string | null; // Username of the currently logged-in user (null if not logged in)
  token: string | null; // Token for authentication (null if not logged in)
  axiosFetch: Axios; // Axios instance with authentication headers
  registerUser: (username: string, password: string) => void; // Function to register a new user
  loginUser: (username: string, password: string) => void; // Function to log in a user
  logout: () => void; // Function to log out the user
  isLoggedIn: () => boolean; // Function to check if the user is logged in
  checkToken: () => Promise<boolean>; // Function to check if the token is valid
}

// Interface to handle error responses (optional message)
interface ErrorResponse {
  message?: string; // Error message (if any)
}

// Props for the UserProvider component, which wraps the children components with the UserContext
type Props = { children: React.ReactNode };

// Creating the UserContext with the structure defined in UserContextInterface
export const UserContext = createContext<UserContextInterface>(
  {} as UserContextInterface
);

// UserProvider component that provides authentication functionality and context to its children
export const UserProvider = ({ children }: Props) => {
  // State variables for storing user information and token
  const [username, setUsername] = useState<string | null>(null); // Stores the username
  const [token, setToken] = useState<string | null>(null); // Stores the authentication token
  const [isReady, setIsReady] = useState<boolean>(false); // Flag to indicate if the context is ready

  // Axios instance configured with the base URL and authorization token (if available)
  const axiosFetch = axios.create({
    baseURL: "https://advanced-web-dev-project-backend.onrender.com", // Base URL of the backend API
    headers: {
      Authorization: `Bearer ${token}`, // Adding the token to the Authorization header for requests
    },
  });

  const navigate = useNavigate(); // Hook to navigate programmatically between routes

  // Effect hook to check if user data (username and token) is available in sessionStorage on component mount
  useEffect(() => {
    const user = sessionStorage.getItem("username"); // Get username from session storage
    const token = sessionStorage.getItem("token"); // Get token from session storage

    // If both username and token exist in sessionStorage, set them in the state
    if (user && token) {
      setUsername(user);
      setToken(token);
    }

    // Mark the context as ready
    setIsReady(true);
  }, []);

  // Function to register a new user by sending a POST request to the backend
  const registerUser = async (username: string, password: string) => {
    await axiosFetch
      .post("/register", {
        username: username,
        password: password,
      })
      .then(() => {
        navigate("/login");
      })
      .catch((err: AxiosError) => {
        // Log any errors (e.g., if registration fails)
        console.log(err.response);
      });
  };

  // Function to log in a user by sending a POST request to the backend
  const loginUser = async (username: string, password: string) => {
    await axiosFetch
      .post("/login", {
        // Sending the username and password to the backend's /login endpoint
        username: username,
        password: password,
      })
      .then((response) => {
        // On successful login, store the token and username in sessionStorage and update state
        sessionStorage.setItem("token", response?.data.token);
        sessionStorage.setItem("username", username);
        setToken(response?.data.token);
        setToken(username); // Mistakenly setting token as username, should be username here
        axios.defaults.headers.common = { Authorization: `Bearer ${token}` }; // Setting default headers for all axios requests
        navigate("/"); // After successful login, redirect to the homepage
      })
      .catch((err: AxiosError) => {
        // Handle login errors (e.g., invalid credentials)
        const errorMessage =
          (err.response?.data as ErrorResponse)?.message ?? // Get the error message if available
          "An unknown error occurred"; // Default error message if none exists
        alert(errorMessage); // Show the error message in an alert box
      });
  };

  // Function to check if the user is logged in by verifying if username is set
  const isLoggedIn = () => {
    return !!username; // Returns true if username exists (meaning the user is logged in)
  };

  // Function to check if the token is valid by sending a request to a protected endpoint
  const checkToken = async () => {
    if (!isLoggedIn) {
      console.log("You must be logged in to access this page"); // Log a message if not logged in
      return false; // Return false if not logged in
    }

    // Sending a request to a protected route to validate the token
    await axiosFetch
      .get("/protected") // Send a GET request to the /protected endpoint
      .catch(() => {
        console.log("Your token has expired!"); // If the token is invalid, log a message
        logout(); // Log out the user
        navigate("/login"); // Redirect to the login page
        return false; // Return false if the token is expired
      });

    return true; // Return true if the token is valid
  };

  // Function to log out the user by removing the token and username from sessionStorage and resetting the state
  const logout = () => {
    sessionStorage.removeItem("token"); // Remove the token from sessionStorage
    sessionStorage.removeItem("username"); // Remove the username from sessionStorage
    setToken(null); // Reset token state to null
    setUsername(null); // Reset username state to null
  };

  // Returning the context provider with user-related functions and state values available for children components
  return (
    <UserContext.Provider
      value={{
        loginUser, // Function to log in a user
        axiosFetch, // Axios instance for making authenticated requests
        username, // Current username
        token, // Current token
        logout, // Function to log out the user
        checkToken, // Function to check token validity
        isLoggedIn, // Function to check if the user is logged in
        registerUser, // Function to register a new user
      }}
    >
      {isReady ? children : null}{" "}
      {/* Render children only when context is ready */}
    </UserContext.Provider>
  );
};
