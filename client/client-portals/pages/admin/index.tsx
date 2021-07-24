import router from "next/router";
import React, { useEffect, useContext, useState } from "react";
import AdminLogin from "components/admin/login";
import AdminRegister from "components/admin/register";
import { AuthContext } from "context/authContext";
import { Layout } from "@/shared/index";

const IndexPage = () => {
  const [register, setRegister] = useState(false);
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

  return (
    <Layout type="admin">
      <div className="bg-base-blue flex justify-center items-center flex-col lg:flex-row ">
        <button
          onClick={() => setRegister(true)}
          className="py-7 cursor-pointer hover:opacity-50 px-16 lg:mt-6 mr-5 rounded-xl shadow-xl bg-base-green font-bold text-white text-xl transform hover:scale-110 hover:opacity-80"
        >
          Register
        </button>
        <button
          onClick={() => setRegister(false)}
          className="py-7 cursor-pointer hover:opacity-50 px-20 mt-6 mr-5 rounded-xl shadow-xl bg-base-green font-bold text-white text-xl transform hover:scale-110 hover:opacity-80"
        >
          Login
        </button>
      </div>
      {register ? <AdminRegister /> : <AdminLogin />}
    </Layout>
  );
};

export default IndexPage;
