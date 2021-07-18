import { useState } from "react";
import { Formik, Form, FormikState } from "formik";
import {
  projectVisibilityInputs,
  projectVisibiltyValidation,
} from "../../../utils/constants";
import { ProjectVisibilityData } from "../../../utils/interfaces";
import Loading from "../../../utils/icons/loading";
import { Input } from "../../shared";
import Markdown from "react-markdown";
import Modal from "react-modal";
import { postAcceptProjectHandler } from "../../../services/api";
import { successToast } from "../../../utils/functions/toast";

const customStyles = {
  content: {
    top: "50%",
    left: "50%",
    right: "auto",
    bottom: "auto",
    marginRight: "-50%",
    transform: "translate(-50%, -50%)",
  },
};

const ProjectVisibility = ({ isOpen, close, projectId }) => {
  const [loading, setLoading] = useState<boolean>(false);

  //@ts-ignore
  const initialValues: ProjectVisibilityData = {
    private: false,
    project_url: "",
  };

  const submitValues = async (values) => {
    values.project_id = projectId;
    const res = await postAcceptProjectHandler(values);
    if (res) {
      successToast("Project Approved successfully!");
    }
  };

  return (
    <>
      <Modal
        isOpen={isOpen}
        onRequestClose={close}
        style={customStyles}
        ariaHideApp={false}
      >
        <div>
          <div>
            <h1>Select the project type</h1>
          </div>
          <Formik
            initialValues={initialValues}
            onSubmit={submitValues}
            validationSchema={projectVisibiltyValidation}
          >
            {({ errors, touched }) => (
              <Form>
                {projectVisibilityInputs.map((input) => (
                  <div
                    key={input.id}
                    className="border-2 border-gray-700 rounded my-4 p-4"
                  >
                    <Input {...input} />
                  </div>
                ))}
                <div className="flex justify-center">
                  <button
                    disabled={Object.keys(errors).length < 0}
                    type="submit"
                    className={`${
                      Object.keys(errors).length > 0
                        ? "cursor-not-allowed bg-opacity-70"
                        : "cursor-pointer"
                    } text-white bg-base-teal w-32 py-4 font-semibold rounded-lg`}
                  >
                    Submit
                  </button>
                </div>
                {Object.keys(errors).map((error) => {
                  if (touched[error]) {
                    return (
                      <Markdown
                        key={error.trim()}
                        className="text-red-500 my-2 lg:my-1"
                      >
                        {errors[error] as string}
                      </Markdown>
                    );
                  }
                })}
              </Form>
            )}
          </Formik>
        </div>
      </Modal>
    </>
  );
};

export default ProjectVisibility;
