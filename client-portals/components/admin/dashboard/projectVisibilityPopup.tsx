import { useState } from "react";
import { Formik, Form, FormikState } from "formik";
import {
  projectVisibilityInputs,
  projectVisibiltyValidation,
} from "../../../utils/constants";
import { ProjectVisibilityData } from "../../../utils/interfaces";
import Loading from "../../../utils/icons/loading";
import { Input } from "../../shared";
import Modal from "react-modal";
import Markdown from "react-markdown";

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

const ProjectVisibility = ({ approveProjectHandler }) => {
  let subtitle;
  const [loading, setLoading] = useState<boolean>(false);
  const [modalIsOpen, setIsOpen] = useState<boolean>(false);

  //@ts-ignore
  const initialValues: ProjectVisibilityData = {
    private: "",
    project_url: "",
  };

  function openModal() {
    setIsOpen(true);
  }

  function afterOpenModal() {
    console.log("works");
  }

  function closeModal() {
    setIsOpen(false);
  }

  // const acceptProjectHandler = async (project_id, isprivate, project_url) => {
  //   const res = await postAcceptProjectHandler(
  //     project_id,
  //     isprivate,
  //     project_url
  //   );
  //   if (res) {
  //     setAccepted(true);
  //     successToast("Project Approved successfully!");
  //   }
  // };

  const submitValues = () => {
    console.log("submit works");
  };

  return (
    <div>
      <Modal
        isOpen={modalIsOpen}
        onAfterOpen={afterOpenModal}
        onRequestClose={closeModal}
        style={customStyles}
        contentLabel="Example Modal"
      >
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
                  disabled={Object.keys(errors).length > 0}
                  type="submit"
                  className={`${
                    Object.keys(errors).length > 0
                      ? "cursor-not-allowed bg-opacity-70"
                      : "cursor-pointer"
                  } text-white bg-base-teal w-32 py-4 font-semibold rounded-lg`}
                  onClick={approveProjectHandler}
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
          )
        </Formik>
      </Modal>
    </div>
  );
};

export default ProjectVisibility;
