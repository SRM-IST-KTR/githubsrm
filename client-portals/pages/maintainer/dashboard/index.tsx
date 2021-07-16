import React, { useEffect, useContext } from "react";
import { Dashboard } from "../../../components/maintainer/dashboard";
import { AuthContext } from "../../../context/AuthContext";
import { useRouter } from "next/router";

const Index = () => {
  const router = useRouter();
  const authContext = useContext(AuthContext);

  useEffect(() => {
    if (!authContext.isAuth || authContext.isAdmin) {
      router.replace("maintainer/dashboard","/");
    }
  }, [authContext]);

  return <Dashboard />;
};

export default Index;
