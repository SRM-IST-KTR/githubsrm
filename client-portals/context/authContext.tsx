import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import { successToast } from "../utils/functions/toast";
import jwt from "jsonwebtoken";

export const AuthContext = React.createContext({
  isAuth: false,
  user: {},
  isAdmin: false,
  username: "",
  setIsAuth: ({}) => {},
  logoutHandler: () => {},
  decode: () => {},
});

const AuthContextProvider: React.FC = (props) => {
  const [isAuth, setIsAuth] = useState<boolean>(false);
  const [isAdmin, setIsAdmin] = useState<boolean>(false);
  const [user, setUser] = useState({});
  const [username, setUserName] = useState<string>("");
  const router = useRouter();

  const decode = () => {
    const token = sessionStorage.getItem("token");
    if (token) {
      var decodedToken = jwt.decode(token);
      var dateNow = new Date();
      if (decodedToken.exp && decodedToken.exp < dateNow.getTime() / 1000) {
        setIsAuth(false);
        setUser({});
        setIsAdmin(false);
      } else {
        setIsAuth(true);
        setUser(decodedToken);
        if (decodedToken.admin) {
          setUserName(decodedToken.user);
        } else {
          setUserName(decodedToken.name);
        }
        if (decodedToken.admin) {
          setIsAdmin(true);
        }
      }
    } else {
      setIsAuth(false);
      setUser({});
      setIsAdmin(false);
    }
  };

  useEffect(() => {
    decode();
  }, []);

  const logoutHandler = () => {
    setIsAuth(false);
    setIsAdmin(false);
    sessionStorage.removeItem("token");
    router.push("/admin");
    successToast("Logged out!");
  };

  return (
    <AuthContext.Provider
      value={{
        isAuth,
        setIsAuth,
        isAdmin,
        user,
        username,
        logoutHandler,
        decode,
      }}
    >
      {props.children}
    </AuthContext.Provider>
  );
};

export default AuthContextProvider;
