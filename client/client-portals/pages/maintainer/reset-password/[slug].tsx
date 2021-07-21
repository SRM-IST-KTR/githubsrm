import React, { useEffect, useContext } from "react";
import { ResetPassword } from "components/maintainer/dashboard";
import { AuthContext } from "context/authContext";
import Router, { useRouter } from "next/router";

const ProfilePage = () => {
  const { query } = useRouter();
  const authContext = useContext(AuthContext);

  useEffect(() => {
    if (authContext.isAdmin) {
      Router.replace("/");
    }
  }, [authContext]);

  return <ResetPassword action={query.slug} queryToken={query.token} />;
};

export default ProfilePage;
