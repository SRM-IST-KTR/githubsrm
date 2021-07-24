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
      <div className="bg-base-blue flex justify-center ">
        <button
          onClick={() => setRegister(true)}
          className={`${
            !register ? "" : "border-b-4 border-base-green"
          } py-4 cursor-pointer px-7 mt-1 mr-5  shadow-lg font-bold text-white text-xl hover:opacity-80`}
        >
          Register
        </button>
        <button
          onClick={() => setRegister(false)}
          s
          className={`${
            register ? "" : "border-b-4 border-base-green"
          } py-4 cursor-pointer  px-10 mt-1 mr-5  shadow-lg  font-bold text-white text-xl hover:opacity-80`}
        >
          Login
        </button>
      </div>
      <div>{register ? <AdminRegister /> : <AdminLogin />}</div>
    </Layout>
  );
};

export default IndexPage;
