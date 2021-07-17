import React, { useState, useEffect, useContext } from "react";
import { useRouter } from "next/router";
import OtherMaintainers from "../../../components/maintainer/dashboard/othermaintainers";
import { Layout } from "../../../components/shared";
import instance from "../../../services/api";
import { getRecaptchaToken } from "../../../services/recaptcha";
import { successToast, errToast } from "../../../utils/functions/toast";
import { AuthContext } from "../../../context/authContext";
import { TiTick } from "react-icons/ti";
import { ImCross } from "react-icons/im";
import {
  ContributorProps,
  OtherMaintainersProps,
} from "../../../utils/interfaces";
import Link from "next/link";
import Loader from "../../../components/shared/loader";
import { postAcceptContributor } from "../../../services/api";

const headings = [
  "Name",
  "Email",
  "SRM",
  "Github",
  "Reg No",
  "Branch",
  "Proposal",
];

const ProjectDetail = () => {
  const [contributorsData, setContributorsData] = useState<ContributorProps[]>(
    []
  );
  const [maintainers, setMaintainers] = useState<OtherMaintainersProps[]>([]);
  const [projectName, setProjectName] = useState<string>("");
  const [projectId, setProjectId] = useState<string>("");
  const [accepted, setAccepted] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);
  const router = useRouter();
  const authContext = useContext(AuthContext);

  useEffect(() => {
    if (!authContext.isAuth || authContext.isAdmin) {
      router.replace("/");
    }
  }, [authContext]);

  const acceptContributorHandler = async (project_id, contributor_id) => {
    setLoading(true);
    const res = await postAcceptContributor(project_id, contributor_id);
    if (res) {
      setAccepted(true);
      successToast("Contributor Approved sucessfully!");
      setLoading(false);
    }
  };

  useEffect(() => {
    const { slug } = router.query;
    const token = sessionStorage.getItem("token");
    instance
      .get(
        `maintainer/projects?projectId=${slug}&contributor=true&maintainer=1`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      )
      .then((res) => {
        setContributorsData(res.data.contributor);
        setProjectName(res.data.project_name);
        setProjectId(res.data._id);
        setMaintainers(res.data.maintainer);
        setLoading(false);
      })
      .catch((err) => {
        setLoading(false);
      });
  }, [accepted]);

  return !loading ? (
    <Layout type="maintainer">
      <div className="flex flex-col justify-center items-center">
        <h2 className="text-4xl font-extrabold text-white mb-5">
          {projectName}
        </h2>
        <OtherMaintainers
          otherMaintainers={maintainers?.filter(
            (m) => m.name !== authContext.username
          )}
        />
        <div className="overflow-scroll w-full">
          {contributorsData.length > 0 ? (
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

                    <td className="p-3 ">
                      {person.is_maintainer_approved ? (
                        <TiTick className="text-green-500 text-center text-3xl" />
                      ) : (
                        <button
                          onClick={() =>
                            acceptContributorHandler(projectId, person._id)
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
            <h2 className="text-4xl font-extrabold text-white mb-5">
              No contributor applications yet!
            </h2>
          )}
        </div>
      </div>
    </Layout>
  ) : (
    <div className="min-h-screen flex justify-center p-5 bg-base-blue">
      <Loader />
    </div>
  );
};

export default ProjectDetail;
