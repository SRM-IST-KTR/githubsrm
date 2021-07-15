import router from "next/router";
import React, { useEffect, useContext, useState } from "react";
import AdminLogin from "../../components/admin/login";
import AdminRegister from "../../components/admin/register";
import { AuthContext } from "../../context/AuthContext";

const IndexPage = () => {
  const [register, setRegister] = useState(false);
  const authContext = useContext(AuthContext);

  useEffect(() => {
    if (authContext.isAuth) {
      router.push("/admin/dashboard");
    }
  }, [authContext]);

  return (
    <div>
      <div className="bg-base-blue flex justify-center items-center flex-col lg:flex-row ">
        <button
          onClick={() => setRegister(true)}
          className="py-7 cursor-pointer hover:opacity-50 px-16 mt-6 mr-5 rounded-xl shadow-xl bg-base-green text-gray-100 font-bold"
        >
          Register
        </button>
        <button
          onClick={() => setRegister(false)}
          className="py-7 cursor-pointer hover:opacity-50 px-20 mt-6 rounded-xl shadow-xl bg-base-green text-gray-100 font-bold"
        >
          Login
        </button>
      </div>
      <div className={`${register ? "hidden" : "block"}`}>
        <AdminLogin />
      </div>
      <div className={`${register ? "block" : "hidden"}`}>
        <AdminRegister />
      </div>
    </div>
  );
};

export default IndexPage;
