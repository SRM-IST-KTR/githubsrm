import router from "next/router";
import React, { useEffect, useContext } from "react";
import MaintainerLogin from "components/maintainer/login";
import { AuthContext } from "context/authContext";

const MaintainerLoginPage = () => {
  const authContext = useContext(AuthContext);
  useEffect(() => {
    if (authContext.isAuth) {
      if (authContext.isAdmin) {
        router.push("/admin/dashboard");
      } else {
        router.push("/maintainer/dashboard");
      }
    }
  }, [authContext]);

  return <MaintainerLogin />;
};

export default MaintainerLoginPage;
