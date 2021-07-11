import ProjectApplications from "../../../components/portals/admin/dashboard";
import { useRouter } from "next/router";
import React, { useState, useEffect } from "react";

const Index = () => {
  const router = useRouter();

  useEffect(() => {
    if (!sessionStorage.getItem("token")) {
      router.push("/admin");
    }
  }, []);

  return <ProjectApplications />;
};

export default Index;
