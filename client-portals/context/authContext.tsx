import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import { successToast } from "../utils/functions/toast";
import jwt from "jsonwebtoken";

export const AuthContext = React.createContext({
  isAuth: false,
  isAdmin: false,
  username: "",
  setIsAuth: (_auth) => {},
  logoutHandler: () => {},
  decode: () => {},
});

const AuthContextProvider: React.FC = (props) => {
  const [isAuth, setIsAuth] = useState<boolean>(false);
  const [isAdmin, setIsAdmin] = useState<boolean>(false);
  const [username, setUserName] = useState<string>("");
  const router = useRouter();

  const decode = () => {
    const token = sessionStorage.getItem("token");
    if (token) {
      var decodedToken = jwt.decode(token);
      var dateNow = new Date();
      if (decodedToken.exp && decodedToken.exp < dateNow.getTime() / 1000) {
        setIsAuth(false);
        setIsAdmin(false);
      } else {
        setIsAuth(true);
        if (decodedToken.admin) {
          setUserName(decodedToken.user);
          setIsAdmin(true);
        } else {
          setUserName(decodedToken.name);
        }
      }
    } else {
      setIsAuth(false);
      setIsAdmin(false);
    }
  };

  useEffect(() => {
    let mounted = true;
    if (mounted) {
      decode();
    }
    return () => {
      mounted = false;
    };
  }, []);

  const logoutHandler = () => {
    setIsAuth(false);
    setIsAdmin(false);
    sessionStorage.removeItem("token");
    router.replace("/");
    successToast("Logged out!");
  };

  return (
    <AuthContext.Provider
      value={{
        isAuth,
        setIsAuth,
        isAdmin,
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
