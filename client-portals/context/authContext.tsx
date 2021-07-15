import React, { useState, useEffect } from "react";
import { useRouter } from "next/router";
import { successToast } from "../utils/functions/toast";
import jwt from "jsonwebtoken";

export const AuthContext = React.createContext({
  isAuth: false,
  user: {},
  setIsAuth: ({}) => {},
  logoutHandler: () => {},
});

const AuthContextProvider: React.FC = (props) => {
  const [isAuth, setIsAuth] = useState(false);
  const [user, setUser] = useState({});
  const router = useRouter();

  useEffect(() => {
    const token = sessionStorage.getItem("token");
    if (token) {
      var decodedToken = jwt.decode(token);
      var dateNow = new Date();
      if (decodedToken.exp < dateNow.getTime() / 1000) {
        setIsAuth(false);
        setUser({});
      } else {
        setIsAuth(true);
        setUser(decodedToken);
      }
    } else {
      setIsAuth(false);
      setUser({});
    }
  }, []);

  const logoutHandler = async () => {
    await setIsAuth(false);
    await sessionStorage.removeItem("token");
    await router.push("/admin");
    await successToast("Logged out!");
  };

  return (
    <AuthContext.Provider value={{ isAuth, setIsAuth, user, logoutHandler }}>
      {props.children}
    </AuthContext.Provider>
  );
};

export default AuthContextProvider;
