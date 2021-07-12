import ProjectApplications from "../../../components/portals/admin/dashboard";
import { useRouter } from "next/router";
import React, { useEffect } from "react";
import AuthContextProvider from "../../../context/authContext";

const AdminDashPage = () => {
  const router = useRouter();

  useEffect(() => {
    if (!sessionStorage.getItem("token")) {
      router.push("/admin");
    }
  }, []);

  return (
    <AuthContextProvider>
      <ProjectApplications />
    </AuthContextProvider>
  );
};

export default AdminDashPage;
