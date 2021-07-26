import React, { useState, useEffect, useContext } from "react";
import { useRouter } from "next/router";
import { AuthContext } from "context/authContext";
import {
  getMaintainerApplications,
  postAcceptMaintainer,
  deleteMaintainer,
} from "services/api";
import { successToast, alertToast } from "utils/functions/toast";
import { Layout } from "components/shared";
import Link from "next/link";
import { MaintainersProps } from "utils/interfaces";
import { CSSLoader } from "@/shared/index";
import { CardGithub, Tick, Loading, Cross } from "@/icons/index";
import { Button } from "@/shared/index";

const MaintainerPage = () => {
  const [maintainerData, setMaintainerData] = useState<MaintainersProps[]>([]);
  const [projectName, setProjectName] = useState<string>("");
  const [projectId, setProjectId] = useState<string>("");
  const [clickedAcceptBtn, setClickedAcceptBtn] = useState<string>("");
  const [clickedRejectBtn, setClickedRejectBtn] = useState<string>("");
  const [accepted, setAccepted] = useState<boolean>(false);
  const [rejected, setRejected] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(false);
  const [loading2, setLoading2] = useState<boolean>(true);
  const [rejectLoading, setRejectLoading] = useState<boolean>(false);

  const router = useRouter();
  const authContext = useContext(AuthContext);

  useEffect(() => {
    if (authContext.authReady) {
      if (!authContext.isAuth || !authContext.isAdmin) {
        router.replace("/");
      }
    }
  }, [authContext]);

  const acceptMaintainerHandler = async (project_id, maintainer_id, email) => {
    setClickedAcceptBtn(maintainer_id);
    setLoading(true);
    const res = await postAcceptMaintainer(project_id, maintainer_id, email);
    if (res) {
      setAccepted(true);
      successToast("Maintainer Approved sucessfully!");
      setLoading(false);
    } else {
      setLoading(false);
    }
  };

  const rejectMaintainerHandler = async (maintainer_id) => {
    setClickedRejectBtn(maintainer_id);
    setRejectLoading(true);
    const res = await deleteMaintainer(maintainer_id);
    if (res) {
      setRejected(true);
      alertToast("Maintainer Rejected successfully");
      setRejectLoading(false);
      router.replace("/admin/dashboard");
    } else {
      setRejectLoading(false);
    }
  };

  const _getMaintainerApplications = async (slug) => {
    const res = await getMaintainerApplications(slug);
    if (res) {
      setMaintainerData(res.maintainer.maintainer);
      setProjectName(res.project.project_name);
      setProjectId(res.project._id);
      setLoading2(false);
    } else {
      setLoading2(false);
    }
  };

  useEffect(() => {
    const { slug } = router.query;
    if (slug) {
      _getMaintainerApplications(slug);
    }
  }, [router.query, accepted, rejected]);

  return loading2 ? (
    <Layout type="admin">
      <div className="flex flex-col items-center justify-center">
        <CSSLoader />
      </div>
    </Layout>
  ) : (
    <Layout type="admin">
      <h1 className="text-4xl text-center font-extrabold text-white mb-7">
        Maintainer Applications of "{projectName}"
      </h1>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {maintainerData.map((person) => (
          <div
            key={person._id}
            className="p-4 rounded-xl shadow-2xl bg-white text-base-black "
          >
            <h2 className="text-xl font-medium mb-3 word-wrap">
              <span className="font-bold">Name: </span>
              {person.name}
            </h2>
            <h2 className="text-xl font-medium mb-3">
              <span className="font-bold">Email: </span>
              {person.email.split("@")[0]}
              <br className="sm:hidden" />@{person.email.split("@")[1]}
            </h2>
            <div className="cursor-pointer hover:text-gray-800 flex text-xl font-medium mb-3">
              <span className="font-bold">Github ID: </span>
              <span className="flex items-center">
                <span className="mx-2">
                  <CardGithub />
                </span>
                <div className="flex align-items-center">
                  <a
                    className="hover:text-base-teal"
                    target="_blank"
                    rel="noopener noreferrer"
                    href={`https://github.com/${person.github_id}`}
                  >
                    <div> {person.github_id}</div>
                  </a>
                </div>
              </span>
            </div>
            <h2 className="text-xl font-medium mb-3">
              <span className="font-bold">Registration Number: </span>
              {person.reg_number}
            </h2>
            <h2 className="text-xl font-medium mb-3">
              <span className="font-bold">Branch: </span>
              {person.branch}
            </h2>
            {person.is_admin_approved && !person.is_admin_rejected ? (
              <div className="flex flex-col items-center text-2xl font-medium text-base-green mt-2">
                <span className="text-green-500 text-5xl">
                  <Tick />
                </span>
                <p>Approved</p>
              </div>
            ) : person.is_admin_rejected ? (
              <div></div>
            ) : (
              <Button
                onClick={() =>
                  acceptMaintainerHandler(projectId, person._id, person.email)
                }
              >
                {loading && clickedAcceptBtn === person._id ? (
                  <span className="flex w-6 mx-auto">
                    <Loading />
                  </span>
                ) : (
                  "Approve Maintainer"
                )}
              </Button>
            )}
            {person.is_admin_rejected && !person.is_admin_approved ? (
              <div className="flex flex-col items-center text-2xl font-medium text-red-500 mt-2">
                <span className="text-red-500 text-3xl">
                  <Cross />
                </span>
                <p>Rejected</p>
              </div>
            ) : person.is_admin_approved ? (
              <div></div>
            ) : (
              <button
                className="flex justify-center w-1/8 mx-auto mt-4 bg-red-400 p-2 font-bold text-white rounded-xl"
                onClick={() => rejectMaintainerHandler(person._id)}
              >
                {rejectLoading && clickedRejectBtn === person._id ? (
                  <span className="flex w-6 mx-auto">
                    <Loading />
                  </span>
                ) : (
                  "Reject Maintainer"
                )}
              </button>
            )}
          </div>
        ))}
      </div>
    </Layout>
  );
};

export default MaintainerPage;
