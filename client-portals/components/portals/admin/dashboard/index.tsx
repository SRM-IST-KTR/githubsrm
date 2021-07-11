import React, { useState, useEffect } from "react";
import ProjectTable from "../../../shared/table";
import Adminnavbar from "./navbar";
import { tableDataProjects } from "../../../shared/tableData";
import AuthContext from "../../../../services/auth-context";

const ProjectApplications = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const storedUserLoggedInInformation = sessionStorage.getItem("isLoggedIn");

    if (storedUserLoggedInInformation === "1") {
      setIsLoggedIn(true);
    }
  }, []);

  return (
    <AuthContext.Provider
      value={{
        isLoggedIn: isLoggedIn,
      }}
    >
      {!isLoggedIn && <p>Not Loggedin</p>}
      {isLoggedIn && (
        <div className="bg-base-blue h-screen flex flex-col justify-center items-center">
          <Adminnavbar />
          <h2 className="text-4xl font-extrabold text-left text-white mb-10">
            Hi, Admin
          </h2>
          <ProjectTable tableData={tableDataProjects} />
        </div>
      )}
    </AuthContext.Provider>
  );
};

export default ProjectApplications;
