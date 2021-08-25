import { useState } from "react";
import { Formik, Form } from "formik";
import { academicYearInputs, academicYearValidation } from "utils/constants";
import { AcademicYearData } from "utils/interfaces";
import { Loading } from "@/icons/index";
import { Input } from "@/shared/index";
import Markdown from "react-markdown";
import Modal from "react-modal";
import { postAcceptProjectHandler } from "services/api";
import { successToast } from "utils/functions/toast";
import { Button } from "@/shared/index";

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
interface AcademicYearProps {
  isOpen: boolean;
  close: (state: boolean) => void;
  year: string;
  projectId: string;
}

const AcademicYear = ({ isOpen, close, projectId }: AcademicYearProps) => {
  const [loading, setLoading] = useState<boolean>(false);

  //@ts-ignore
  const initialValues: AcademicYearData = {
    year: "",
  };

  const submitValues = async (values: AcademicYearProps) => {
    setLoading(true);
    const _values = Object.assign({}, values, {
      project_id: projectId,
    });

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
            <h1>Enter the Academic Year</h1>
          </div>
          <Formik
            initialValues={initialValues}
            onSubmit={submitValues}
            validationSchema={academicYearValidation}
          >
            {({ errors, touched }) => (
              <Form>
                {academicYearInputs.map((input) => (
                  <div
                    key={input.id}
                    className="border-2 border-gray-700 rounded my-4 p-4"
                  >
                    <Input {...input} />
                  </div>
                ))}
                <div className="flex justify-center">
                  <Button disabled={Object.keys(errors).length < 0}>
                    {loading ? (
                      <span className="flex w-6 mx-auto">
                        <Loading />
                      </span>
                    ) : (
                      "Submit"
                    )}
                  </Button>
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

export default AcademicYear;
