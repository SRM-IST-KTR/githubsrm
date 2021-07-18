import { useState } from "react";
import { Formik, Form, FormikState } from "formik";
import {
  projectVisibilityInputs,
  projectVisibiltyValidation,
} from "../../../utils/constants";
import { ProjectVisibilityData } from "../../../utils/interfaces";
import Loading from "../../../utils/icons/loading";
import { Input } from "../../shared";

const ProjectVisibility = () => {
  const [loading, setLoading] = useState<boolean>(false);
  //@ts-ignore
  const initialValues: ProjectVisibilityData = {
    private: "",
    project_url: "",
  };

  const submitValues = () => {};

  const projectType = [
    {
      label: "Public",
      value: "public",
    },
    {
      label: "Private",
      value: "private",
    },
  ];

  return (
    <div>
      <div>
        <h1>Select the project type</h1>
      </div>
      <Formik
        initialValues={initialValues}
        onSubmit={submitValues}
        validationSchema={projectVisibiltyValidation}
      >
        <Form>
          {projectVisibilityInputs.map((input) => (
            <div className="border-2 border-gray-700 rounded my-4 p-4">
              <Input key={input.id} {...input} />
            </div>
          ))}

          <button type="submit">
            {loading ? (
              <span className="flex w-6 mx-auto">
                <Loading />
              </span>
            ) : (
              "Submit"
            )}
          </button>
        </Form>
      </Formik>
    </div>
  );
};

export default ProjectVisibility;
