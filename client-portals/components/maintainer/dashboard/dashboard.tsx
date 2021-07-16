import React, { useContext, useEffect, useState } from "react";
import { Card } from ".";
import { Layout } from "../../shared";
import { AuthContext } from "../../../context/AuthContext";
import instance from "../../../services/api";
import { GrNext, GrPrevious } from "react-icons/gr";
import { successToast, errToast } from "../../../utils/functions/toast";
import { MaintainerProjectsProps } from "../../../utils/interfaces";

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
    <div className="min-h-screen flex justify-center p-5 bg-base-blue">
      <h1 className="text-7xl font-extrabold text-gray-100 text-center pt-20 animate-pulse">
        loading..
      </h1>
    </div>
  ) : (
    <Layout type="maintainer">
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
      <div className="flex justify-center my-5">
        <button
          disabled={!hasPrevPage}
          className={`${
            !hasPrevPage
              ? "opacity-10 cursor-not-allowed"
              : "hover:bg-base-green focus:bg-base-green"
          } p-3 rounded-full`}
          onClick={() => setPageNo(pageNo - 1)}
        >
          <GrPrevious className="text-2xl font-extrabold" />
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
          <GrNext className="text-2xl font-extrabold" />
        </button>
      </div>
    </Layout>
  );
};

export default index;
