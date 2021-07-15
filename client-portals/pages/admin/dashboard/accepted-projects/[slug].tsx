import React, { useState, useEffect, useContext } from "react";
import { useRouter } from "next/router";
import { AuthContext } from "../../../../context/AuthContext";
import instance from "../../../../services/api";
import { successToast, errToast } from "../../../../utils/functions/toast";
import { TiTick } from "react-icons/ti";
import { Layout } from "../../../../components/shared";
import { FiGithub } from "react-icons/fi";
import Link from "next/link";
import { getRecaptchaToken } from "../../../../services/recaptcha";

const ContributorsPage = () => {
  const [contributorsData, setContributorsData] = useState([]);
  const [projectName, setProjectName] = useState("");
  const [projectId, setProjectId] = useState("");
  const [accepted, setAccepted] = useState<boolean>(false);
  const router = useRouter();
  const authContext = useContext(AuthContext);

  useEffect(() => {
    if (authContext.isAuth === false) {
      router.push("/admin");
    }
  }, [authContext]);

  var token = null;
  useEffect(() => {
    token = sessionStorage.getItem("token");
  }, []);

  const acceptMaintainerHandler = async (project_id, contributor_id) => {
    const recaptchaToken = await getRecaptchaToken("post");
    await instance
      .post(
        "admin/projects?role=contributor",
        { project_id: project_id, contributor_id: contributor_id },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "X-RECAPTCHA-TOKEN": recaptchaToken,
          },
        }
      )
      .then((res) => {
        console.log(res);
        setAccepted(true);
        successToast("Contributor Approved sucessfully!");
      })
      .catch((err) => {
        errToast(err.message);
      });
  };

  useEffect(() => {
    const { slug } = router.query;
    instance
      .get(
        `admin/projects?projectId=${slug}&contributor=true&maintainer=true`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      .then((res) => {
        setContributorsData(res.data.contributor.contributor);
        setProjectName(res.data.project.project_name);
        setProjectId(res.data.project._id);
        console.log(res.data);
      })
      .catch((err) => {
        errToast(err.message);
      });
  }, [accepted]);

  return (
    <Layout type="admin">
      <h1 className="text-5xl font-extrabold underline text-white mb-5">
        {projectName}
      </h1>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 ">
        {contributorsData.map((person) => (
          <div key={person._id} className="p-5 rounded-xl 0 shadow-2xl">
            <h2 className="text-2xl font-medium text-white mb-5">
              {person.name}
            </h2>
            <h2 className="text-2xl font-medium text-white mb-10">
              {person.email}
            </h2>
            <Link href={person.github_id}>
              <div className="cursor-pointer hover:text-gray-800 p-2  flex text-2xl font-medium text-white mb-5">
                <FiGithub /> <span className="ml-2">{person.github_id}</span>
              </div>
            </Link>
            <h2 className="text-2xl font-medium text-white mb-5">
              {person.reg_number}
            </h2>
            <h2 className="text-2xl font-medium text-white mb-5">
              {person.branch}
            </h2>
            {person.is_admin_approved ? (
              <div className="flex flex-col justify-center items-center text-4xl font-medium text-base-green mt-5">
                <TiTick className="text-green-500 text-5xl" />
                <p>approved</p>
              </div>
            ) : (
              <button
                onClick={() => acceptMaintainerHandler(projectId, person._id)}
                className="flex justify-center w-1/8 mx-auto mt-4 bg-green-400 p-2 font-bold text-white rounded-xl"
              >
                Approve Contributor
              </button>
            )}
          </div>
        ))}
      </div>
    </Layout>
  );
};

export default ContributorsPage;
