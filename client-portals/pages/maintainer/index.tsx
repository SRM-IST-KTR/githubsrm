import router from "next/router";
import React, { useEffect, useContext } from "react";
import MaintainerLogin from "../../components/maintainer/login";
import { AuthContext } from "../../context/AuthContext";

const MaintainerLoginPage = () => {
  const authContext = useContext(AuthContext);

  return <MaintainerLogin />;
};

export default MaintainerLoginPage;
