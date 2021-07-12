import Card from "../../../shared/card";
import React, { useState, useEffect } from "react";
import instance from "../../../../services/api";
import { errToast } from "../../../../utils/functions/toast";

const AcceptedProjectsCards = () => {
  const [acceptedProjects, setAcceptedProjects] = useState([]);

  const token = sessionStorage.getItem("token");

  useEffect(() => {
    instance
      .get("admin/projects?page=1", {
        headers: {
          Authorization: `Bearer ${token}`,
          "X-RECAPTCHA-TOKEN": null,
        },
      })
      .then((res) => {
        setAcceptedProjects(res.data.records);
      })
      .catch((err) => {
        errToast(err.message);
      });
  }, []);
  return (
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
  );
};

export default AcceptedProjectsCards;
