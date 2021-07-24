import React from "react";
import Link from "next/link";
import { AuthContext } from "context/authContext";
import Router from "next/router";

const IndexPage = () => {
  const authContext = React.useContext(AuthContext);

  React.useEffect(() => {
    if (authContext.isAuth) {
      if (authContext.isAdmin) {
        Router.push("/admin/dashboard");
      } else {
        Router.push("/maintainer/dashboard");
      }
    } else {
      Router.push("/maintainer");
    }
  }, [authContext]);

  return <div></div>;
};

export default IndexPage;
