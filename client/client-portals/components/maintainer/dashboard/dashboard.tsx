import React, { useEffect, useState } from "react";
import { Card } from ".";
import { Layout, CSSLoader } from "@/shared/index";
import instance from "services/api";
import { MaintainerProjectsProps } from "utils/interfaces";
import { PaginationButtons } from "@/shared/index";
import { errToast } from "utils/functions/toast";
import router from "next/router";

const index = () => {
  const [projects, setProjects] = useState<MaintainerProjectsProps[]>([]);
  const [accepted, setAccepted] = useState<boolean>(false);
  const [pageNo, setPageNo] = useState<number>(1);
  const [hasNextPage, sethasNextPage] = useState<boolean>(false);
  const [hasPrevPage, sethasPrevPage] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    (async () => {
      let API;
      try {
        API = await instance();
      } catch (error) {
        errToast("Session Expired! Please Login again!");
      } finally {
        API?.get(`maintainer/projects?page=${pageNo}`)
          .then((res) => {
            setProjects(res.data.records);
            sethasNextPage(res.data.hasNextPage);
            sethasPrevPage(res.data.hasPreviousPage);
            setLoading(false);
          })
          .catch((err) => {
            setLoading(false);
          });
      }
    })();
  }, [accepted, pageNo]);

  return loading ? (
    <Layout type="maintainer">
      <div className="flex flex-col items-center justify-center mt-52">
        <CSSLoader />
      </div>
    </Layout>
  ) : (
    <Layout type="maintainer">
      <div className="flex justify-center font-extrabold my-10 text-white text-5xl">
        My Projects
      </div>
      {projects.length === 0 && (
        <h1 className="mt-20 text-3xl text-white text-center">
          None of your projects has been accepted yet!
        </h1>
      )}
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
      <div className="mt-7">
        {projects.length > 0 && (
          <PaginationButtons
            hasNextPage={hasNextPage}
            hasPrevPage={hasPrevPage}
            pageNo={pageNo}
            setPageNo={setPageNo}
          />
        )}
      </div>
    </Layout>
  );
};

export default index;
