import ProjectApplications from "../../../components/admin/dashboard";
import { useRouter } from "next/router";
import React, { useEffect, useContext } from "react";
import { AuthContext } from "../../../context/authContext";

const AdminDashPage = () => {
  const router = useRouter();
  const authContext = useContext(AuthContext);

  useEffect(() => {
    if (!sessionStorage.getItem("token")) {
      authContext.setIsAuth(false);
      router.push("/admin");
    }
  }, [authContext]);

  return <ProjectApplications />;
};

export default AdminDashPage;
