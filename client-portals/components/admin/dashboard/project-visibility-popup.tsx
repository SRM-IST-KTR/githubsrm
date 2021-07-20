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
  const [isPrivate, setIsPrivate] = useState<boolean>(false);

  //@ts-ignore
  const initialValues: ProjectVisibilityData = {
    private: false,
    project_url: "",
  };

  const submitValues = async (values) => {
    const _values = Object.assign({}, values, {
      private: isPrivate,
      project_id: projectId,
    });
    setLoading(true);
    const res = await postAcceptProjectHandler(_values);
    if (res) {
      successToast("Project Approved successfully!");
      setLoading(false);
      window.location.reload();
    } else {
      setLoading(false);
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
                    <div className="flex justify-center mt-2 mb-6">
                      <button
                        type="button"
                        onClick={() => setIsPrivate(true)}
                        className={`${
                          isPrivate ? "bg-base-blue" : "cursor-pointer"
                        } text-white bg-gray-400  w-20 py-1 font-semibold rounded-lg`}
                      >
                        Private
                      </button>
                      <button
                        type="button"
                        onClick={() => setIsPrivate(false)}
                        className={`${
                          !isPrivate ? "bg-base-blue" : "cursor-pointer"
                        } text-white bg-gray-400 ml-5 w-20 py-1 font-semibold rounded-lg`}
                      >
                        Public
                      </button>
                    </div>

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
                    {loading ? (
                      <span className="flex w-6 mx-auto">
                        <Loading />
                      </span>
                    ) : (
                      "Approve"
                    )}
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
