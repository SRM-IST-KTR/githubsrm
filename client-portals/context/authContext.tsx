import router from "next/router";
import React, { useState } from "react";
import { errToast } from "../utils/functions/toast";
import { useRouter } from "next/router";

export const AuthContext = React.createContext({
  isAuth: false,
  setIsAuth: (_isAuth: boolean) => {},
  logoutHandler: () => {},
});

const AuthContextProvider: React.FC = (props) => {
  const [isAuth, setIsAuth] = useState(false);
  const router = useRouter();
  const logoutHandler = () => {
    setIsAuth(false);
    sessionStorage.removeItem("token");
    errToast("Logged out!");
    router.push("/admin");
  };

  return (
    <AuthContext.Provider value={{ isAuth, setIsAuth, logoutHandler }}>
      {props.children}
    </AuthContext.Provider>
  );
};

export default AuthContextProvider;
