import React, { useEffect, useContext } from "react";
import { ResetPassword } from "../../../../components/maintainer/dashboard";
import { AuthContext } from "../../../../context/AuthContext";
import { useRouter } from "next/router";

const ProfilePage = () => {
  const router = useRouter();
  const authContext = useContext(AuthContext);

  useEffect(() => {
    if (!authContext.isAuth || authContext.isAdmin) {
      router.replace("/");
    }
  }, [authContext]);

  const { slug } = router.query;

  return <ResetPassword action={slug} />;
};

export default ProfilePage;
