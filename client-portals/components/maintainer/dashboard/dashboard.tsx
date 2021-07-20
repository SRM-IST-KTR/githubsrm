import React, { useEffect, useState } from "react";
import { Card } from ".";
import { Layout, Footer, CSSLoader } from "@/shared/index";
import instance from "services/api";
import { MaintainerProjectsProps } from "utils/interfaces";
import Next from "utils/icons/next";
import Previous from "utils/icons/previous";

const index = () => {
  const [projects, setProjects] = useState<MaintainerProjectsProps[]>([]);
  const [accepted, setAccepted] = useState<boolean>(false);
  const [pageNo, setPageNo] = useState<number>(1);
  const [hasNextPage, sethasNextPage] = useState<boolean>(false);
  const [hasPrevPage, sethasPrevPage] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const token = sessionStorage.getItem("token");
    instance
      .get(`maintainer/projects?page=${pageNo}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((res) => {
        setProjects(res.data.records);
        sethasNextPage(res.data.hasNextPage);
        sethasPrevPage(res.data.hasPreviousPage);
        setLoading(false);
      })
      .catch((err) => {
        setLoading(false);
      });
  }, [accepted, pageNo]);

  return loading ? (
    <>
      <div className="flex flex-col items-center justify-center w-screen min-h-screen bg-base-blue">
        <CSSLoader />
      </div>
      <div className="fixed bottom-0 w-full">
        <Footer />
      </div>
    </>
  ) : (
    <>
      <Layout type="maintainer">
        <div className="flex justify-center font-extrabold mb-10 text-white text-5xl">
          My Projects
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 ">
          {projects?.map((item) => (
            <Card
              name={item.project_name}
              url={`/maintainer/dashboard/${item._id}`}
              desc={item.description}
              key={item._id}
            />
          ))}
        </div>
        <div className="fixed inline-flex bottom-0 left-1/2 w-full mb-5 ">
          <button
            disabled={!hasPrevPage}
            className={`${
              !hasPrevPage
                ? "opacity-10 cursor-not-allowed"
                : "hover:bg-base-green focus:bg-base-green"
            } p-3 rounded-full`}
            onClick={() => setPageNo(pageNo - 1)}
          >
            <span className="text-2xl font-extrabold">
              <Previous />
            </span>
          </button>
          <h2 className="text-gray-50 text-4xl  font-medium mx-3">{pageNo}</h2>
          <button
            disabled={!hasNextPage}
            className={`${
              !hasNextPage
                ? "opacity-10 cursor-not-allowed"
                : "hover:bg-base-green focus:bg-base-green"
            } p-3 rounded-full`}
            onClick={() => setPageNo(pageNo + 1)}
          >
            <span className="text-2xl font-extrabold">
              <Next />
            </span>
          </button>
        </div>
      </Layout>
      <div className="fixed bottom-0 w-full">
        <Footer />
      </div>
    </>
  );
};

export default index;
