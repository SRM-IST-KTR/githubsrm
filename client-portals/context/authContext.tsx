import React, { useState } from "react";
import { useRouter } from "next/router";
import { successToast } from "../utils/functions/toast";

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
    successToast("Logged out!");
    router.push("/admin");
  };

  return (
    <AuthContext.Provider value={{ isAuth, setIsAuth, logoutHandler }}>
      {props.children}
    </AuthContext.Provider>
  );
};

export default AuthContextProvider;
