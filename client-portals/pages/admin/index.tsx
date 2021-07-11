import React, { useEffect, useState } from "react";
import AdminLogin from "../../components/portals/admin/login";
import AdminRegister from "../../components/portals/admin/register";
import { useRouter } from "next/router";

const IndexPage = () => {
  const [register, setRegister] = React.useState(false);
  const router = useRouter();

  useEffect(() => {
    if (sessionStorage.getItem("token")) {
      router.push("/admin/dashboard");
    }
  }, []);

  return (
    <div>
      <div className="bg-base-blue  p-10">
        <button
          onClick={() => setRegister(true)}
          className="bg-base-green font-bold text-xl p-2 mx-2 rounded"
        >
          Register
        </button>
        <button
          onClick={() => setRegister(false)}
          className="bg-base-green font-bold text-xl p-2 mx-2 rounded"
        >
          Login
        </button>

        <div className={`${register ? "hidden" : "block"}`}>
          <AdminLogin />
        </div>
        <div className={`${register ? "block" : "hidden"}`}>
          <AdminRegister />
        </div>
      </div>
    </div>
  );
};

export default IndexPage;
