import Card from "../../../shared/card";
import React, { useState, useEffect } from "react";
import instance from "../../../../services/api";
import { errToast } from "../../../../utils/functions/toast";
import { GrNext, GrPrevious } from "react-icons/gr";

const AcceptedProjectsCards = () => {
  const [acceptedProjects, setAcceptedProjects] = useState([]);
  const [pageNo, setPageNo] = useState(1);
  const [hasNextPage, sethasNextPage] = useState<boolean>(false);
  const [hasPrevPage, sethasPrevPage] = useState<boolean>(false);

  var token = null;
  useEffect(() => {
    token = sessionStorage.getItem("token");
  }, [pageNo]);

  useEffect(() => {
    instance
      .get(`admin/projects?page=${pageNo}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })
      .then((res) => {
        setAcceptedProjects(res.data.records);
        sethasNextPage(res.data.hasNextPage);
        sethasPrevPage(res.data.hasPreviousPage);
      })
      .catch((err) => {
        errToast(err.message);
      });
  }, [pageNo]);

  return (
    <>
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 ">
        {acceptedProjects.map(
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
    </>
  );
};

export default AcceptedProjectsCards;
