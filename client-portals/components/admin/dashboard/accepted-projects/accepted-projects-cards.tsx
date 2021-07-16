import Card from "../../../shared/card";
import React, { useState, useEffect } from "react";
import instance from "../../../../services/api";
import { errToast } from "../../../../utils/functions/toast";
import { GrNext, GrPrevious } from "react-icons/gr";
import { AcceptedProjectProps } from "../../../../utils/interfaces";

const AcceptedProjectsCards = () => {
  const [acceptedProjects, setAcceptedProjects] = useState<
    AcceptedProjectProps[]
  >([]);
  const [pageNo, setPageNo] = useState<number>(1);
  const [hasNextPage, sethasNextPage] = useState<boolean>(false);
  const [hasPrevPage, sethasPrevPage] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const token = sessionStorage.getItem("token");
    instance
      .get(`admin/projects/accepted?page=${pageNo}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((res) => {
        setAcceptedProjects(res.data.records);
        sethasNextPage(res.data.hasNextPage);
        sethasPrevPage(res.data.hasPreviousPage);
        setLoading(false);
      })
      .catch((err) => {
        setLoading(false);
      });
  }, [pageNo]);

  return !loading ? (
    <>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 ">
        {acceptedProjects[0] &&
          acceptedProjects.map(
            (item) =>
              item.is_admin_approved && (
                <Card
                  url={`/admin/dashboard/accepted-projects/${item._id}`}
                  name={item.project_name}
                  desc={item.description}
                  key={item._id}
                />
              )
          )}
      </div>
      {acceptedProjects[0] ? (
        <div className="flex justify-center my-14">
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
      ) : (
        <h1 className="text-5xl text-gray-200 text-center">
          No Accepted projects yet!
        </h1>
      )}
    </>
  ) : (
    <h1 className="text-7xl font-extrabold text-gray-100 text-center pt-20 animate-pulse">
      loading..
    </h1>
  );
};

export default AcceptedProjectsCards;
