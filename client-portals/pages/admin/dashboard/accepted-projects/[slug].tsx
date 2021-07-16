import React, { useState, useEffect, useContext } from "react";
import { useRouter } from "next/router";
import { AuthContext } from "../../../../context/AuthContext";
import instance from "../../../../services/api";
import { successToast, errToast } from "../../../../utils/functions/toast";
import { TiTick } from "react-icons/ti";
import { ImCross } from "react-icons/im";
import { Layout } from "../../../../components/shared";
import Link from "next/link";
import { getRecaptchaToken } from "../../../../services/recaptcha";
import { ContributorsProps } from "../../../../utils/interfaces";

const headings = [
  "Name",
  "Email",
  "SRM",
  "Github",
  "Reg No",
  "Branch",
  "Proposal",
  "maintainer approved?",
  "Added to repo?",
];

const ContributorsPage = () => {
  const [contributorsData, setContributorsData] = useState<ContributorsProps[]>(
    []
  );
  const [projectName, setProjectName] = useState<string>("");
  const [projectId, setProjectId] = useState<string>("");
  const [accepted, setAccepted] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const router = useRouter();
  const authContext = useContext(AuthContext);

  useEffect(() => {
    if (!authContext.isAuth || !authContext.isAdmin) {
      router.replace("/admin/dashboard/accepted-projects/", "/");
    }
  }, [authContext]);

  const acceptMaintainerHandler = async (project_id, contributor_id) => {
    const recaptchaToken = await getRecaptchaToken("post");
    const token = sessionStorage.getItem("token");
    await instance
      .post(
        "admin/projects?role=contributor",
        { contributor_id: contributor_id, project_id: project_id },
        {
          headers: {
            Authorization: `Bearer ${token}`,
            "X-RECAPTCHA-TOKEN": recaptchaToken,
          },
        }
      )
      .then((res) => {
        setAccepted(true);
        successToast("Contributor Approved sucessfully!");
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
        setLoading(false);
   
      })
      .catch((err) => {
        setLoading(false);
      });
  }, [accepted]);

  return loading ? (
    <div className="min-h-screen flex justify-center p-5 bg-base-blue">
      <h1 className="text-7xl font-extrabold text-gray-100 text-center pt-20 animate-pulse">
        loading..
      </h1>
    </div>
  ) : (
    <Layout type="admin">
      <h1 className="text-5xl font-extrabold underline text-white mb-7">
        {projectName}
      </h1>

      <div className="overflow-scroll w-full">
        {contributorsData[0] ? (
          <table className="table text-white border-separate space-y-6 text-sm">
            <thead className="bg-base-teal text-white">
              <tr>
                {headings.map((head) => (
                  <th key={head} className="px-3 text-left">
                    {head}
                  </th>
                ))}
              </tr>
            </thead>
            <tbody>
              {contributorsData.map((person) => (
                <tr key={person._id} className="bg-gray-800">
                  <td className="p-3">
                    <div className="flex align-items-center">
                      <div> {person.name}</div>
                    </div>
                  </td>
                  <td className="p-3">
                    <div className="flex align-items-center">
                      <div> {person.email}</div>
                    </div>
                  </td>
                  <td className="p-3">
                    <div className="flex align-items-center">
                      <div> {person.srm_email}</div>
                    </div>
                  </td>
                  <td className="p-3">
                    <div className="flex align-items-center">
                      <Link href={person.github_id}>
                        <div> {person.github_id}</div>
                      </Link>
                    </div>
                  </td>

                  <td className="p-3">
                    <div className="flex align-items-center">
                      <div> {person.reg_number}</div>
                    </div>
                  </td>
                  <td className="p-3">
                    <div className="flex align-items-center">
                      <div> {person.branch}</div>
                    </div>
                  </td>
                  <td className="p-3">
                    <div className="flex align-items-center">
                      <div> {person.poa}</div>
                    </div>
                  </td>
                  <td className="p-3">
                    <div className="flex align-items-center">
                      <div>
                        {" "}
                        {person.is_maintainer_approved ? (
                          <TiTick className="text-green-500 text-2xl" />
                        ) : (
                          <ImCross className="text-red-500 text-lg" />
                        )}
                      </div>
                    </div>
                  </td>
                  <td className="p-3">
                    <div className="flex align-items-center">
                      <div>
                        {" "}
                        {person.is_added_to_repo ? (
                          <TiTick className="text-green-500 text-2xl" />
                        ) : (
                          <ImCross className="text-red-500 text-lg" />
                        )}
                      </div>
                    </div>
                  </td>
                  <td className="p-3 ">
                    {person.is_admin_approved ? (
                      <TiTick className="text-green-500 text-center text-3xl" />
                    ) : (
                      <button
                        onClick={() =>
                          acceptMaintainerHandler(projectId, person._id)
                        }
                        className="flex justify-center w-1/8 mx-auto mt-4 bg-green-400 p-2 font-bold text-white rounded-xl"
                      >
                        Approve Contributor
                      </button>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <h1 className="text-5xl text-gray-200 mt-10">
            No Contributors Yet!!
          </h1>
        )}
      </div>
    </Layout>
  );
};

export default ContributorsPage;
