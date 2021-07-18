import React, { useState, useEffect, useContext } from "react";
import { useRouter } from "next/router";
import { AuthContext } from "../../../context/authContext";
import instance from "../../../services/api";
import { successToast, errToast } from "../../../utils/functions/toast";
import { TiTick } from "react-icons/ti";
import { FiGithub } from "react-icons/fi";
import { Layout } from "../../../components/shared";
import Link from "next/link";
import { getRecaptchaToken } from "../../../services/recaptcha";
import { MaintainersProps } from "../../../utils/interfaces";
import CSSLoader from "../../../components/shared/loader";

const MaintainerPage = () => {
  const [maintainerData, setMaintainerData] = useState<MaintainersProps[]>([]);
  const [projectName, setProjectName] = useState<string>("");
  const [projectId, setProjectId] = useState<string>("");
  const [accepted, setAccepted] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  const router = useRouter();
  const authContext = useContext(AuthContext);

  useEffect(() => {
    const { slug } = router.query;
    if (!authContext.isAuth || !authContext.isAdmin) {
      router.replace("/");
    }
  }, [authContext]);

  const acceptMaintainerHandler = async (project_id, maintainer_id, email) => {
    const recaptchaToken = await getRecaptchaToken("post");
    const token = sessionStorage.getItem("token");
    await instance
      .post(
        "admin/projects?role=maintainer",
        { project_id: project_id, maintainer_id: maintainer_id, email },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "X-RECAPTCHA-TOKEN": recaptchaToken,
          },
        }
      )
      .then((res) => {
        setAccepted(true);
        successToast("Maintainer Approved sucessfully!");
      })
      .catch((err) => {
        errToast(err.message);
      });
  };

  useEffect(() => {
    const { slug } = router.query;
    const token = sessionStorage.getItem("token");
    instance
      .get(
        `admin/projects?projectId=${slug}&contributor=false&maintainer=true`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      .then((res) => {
        setMaintainerData(res.data.maintainer.maintainer);
        setProjectName(res.data.project.project_name);
        setProjectId(res.data.project._id);
        setLoading(false);
      })
      .catch((err) => {
        setLoading(false);
      });
  }, [accepted]);

  return loading ? (
    <div className="flex flex-col items-center justify-center w-screen min-h-screen bg-base-blue">
      <CSSLoader />
    </div>
  ) : (
    <Layout type="admin">
      <h1 className="text-4xl text-center font-extrabold text-white mb-7">
        Maintainer Applications of "{projectName}"
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {maintainerData.map((person) => (
          <div
            key={person._id}
            className="p-5 rounded-xl shadow-2xl bg-white text-base-black"
          >
            <h2 className="text-xl font-medium mb-5">
              <span className="font-bold">Name: </span>
              {person.name}
            </h2>
            <h2 className="text-xl font-medium mb-5">
              <span className="font-bold">Email: </span>
              {person.email}
            </h2>
            <Link href={person.github_id}>
              <div className="cursor-pointer hover:text-gray-800 flex text-xl font-medium mb-5">
                <span className="font-bold">Github ID: </span>
                <span className="ml-1 flex">
                  <FiGithub />
                  {person.github_id}
                </span>
              </div>
            </Link>
            <h2 className="text-xl font-medium mb-5">
              <span className="font-bold">Registration Number: </span>
              {person.reg_number}
            </h2>
            <h2 className="text-xl font-medium mb-5">
              <span className="font-bold">Branch: </span>
              {person.branch}
            </h2>
            {person.is_admin_approved ? (
              <div className="flex flex-col justify-center items-center text-4xl font-medium text-base-green mt-5">
                <TiTick className="text-green-500 text-5xl" />
                <p>Approved</p>
              </div>
            ) : (
              <button
                onClick={() =>
                  acceptMaintainerHandler(projectId, person._id, person.email)
                }
                className="flex justify-center w-1/8 mx-auto mt-4 bg-green-400 p-2 font-bold text-white rounded-xl"
              >
                Approve Maintainer
              </button>
            )}
          </div>
        ))}
      </div>
    </Layout>
  );
};

export default MaintainerPage;
