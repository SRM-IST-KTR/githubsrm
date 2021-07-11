import AcceptedProjectsCard from "./accepted-projects";
import Adminnavbar from "./navbar";
import React, { useState, useEffect } from "react";
import AuthContext from "../../../../services/auth-context";

const AcceptedProjectDashboard = () => {
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
      {!isLoggedIn && <p>not logged in</p>}
      {isLoggedIn && (
        <div className="min-h-screen p-14 bg-base-blue">
          <Adminnavbar />
          <h2 className="text-4xl font-extrabold text-white mb-10">
            Hi, Admin
          </h2>
          <AcceptedProjectsCard />
        </div>
      )}
    </AuthContext.Provider>
  );
};

export default AcceptedProjectDashboard;
