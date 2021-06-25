import React, { useState } from "react";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";

import SectionIcon from "./sectionIcon";
import FormTextField from "./formtextfield";

import { FormTextFieldProps } from "../../utils/interfaces";

const Register = () => {
  let [stage, setStage] = useState(0);

  const validationSchema = Yup.object().shape({
    name: Yup.string().trim().required("No Name provided."),
    email: Yup.string()
      .trim()
      .required("No Email provided.")
      .email("Should be a valid email."),
    githubid: Yup.string().trim().required("No githubid provided"),
    srmEmail: Yup.string().trim().required(),
    regNo: Yup.string().trim().required(),
    branch: Yup.string().trim().required(),
    project: Yup.string().trim().required(),
    feBug: Yup.string().trim().required("Proposal not provided"),
  });

  type FormData = Partial<Yup.InferType<typeof validationSchema>>;

  const initialValues: FormData = {};

  const submitValues = (values: FormData) => {
    //api call here
    console.log(values);
  };

  const handelVisibility = (i: number) => !(stage === i);

  const setActive = (i: number) => () => setStage(i);

  const goNext = () => {
    if (stage != Sections.length - 1) {
      setStage(stage + 1);
    }
  };

  const goBack = () => {
    if (stage !== 0) {
      setStage(stage - 1);
    }
  };

  const _disabled = (errors, touched) => {
    // TODO change to one line
    const a =
      Object.keys(errors).filter((i, k) => touched[i]).length !== 0 ||
      Object.keys(touched).length == 0;
    console.log(
      a,
      Object.keys(errors).filter((i, k) => touched[i]),
      Object.keys(touched)
    );
    return a;
  };

  const Sections = ["Personal", "SRM details", "Project"];
  const Projects = ["Project 1", "Project 2", "Project 3", "Project 4"];

  return (
    <div className="w-full">
      <div className="border-b-2 pb-4">
        <h1 className="font-montserrat font-medium text-2xl">Big text here</h1>
        <h3 className="font-montserrat font-medium text-base">
          small text here
        </h3>
      </div>

      <div className="flex flex-row w-full">
        <div className="w-1/4 mx-2">
          {Sections.map((section, i) => (
            <SectionIcon
              _key={section}
              name={section}
              sec={handelVisibility(i)}
              click={setActive(i)}
            />
          ))}
        </div>

        <div className="w-3/4 p-4 mx-2">
          <Formik
            initialValues={initialValues}
            onSubmit={submitValues}
            validationSchema={validationSchema}
          >
            {({ errors, touched }) => (
              <Form className="w-full p-4 m-2">
                <div className="flex flex-row">
                  <div className="relative h-72 w-1/2">
                    {/* TODO: del 'this' button */}
                    <button
                      type="button"
                      onClick={() => console.log(errors, touched)}
                    >
                      this
                    </button>

                    {/* Personal */}
                    <div
                      className={
                        (handelVisibility(0) ? "invisible" : " ") + " absolute"
                      }
                    >
                      <FormTextField
                        vals={{
                          id: "name",
                          label: "Name",
                          type: "name",
                          placeholder: "GithubSRM",
                        }}
                        touched={touched}
                        errors={errors}
                      />
                      <FormTextField
                        vals={{
                          id: "email",
                          label: "Email",
                          type: "email",
                          placeholder: "johndoe@mail.com",
                        }}
                        touched={touched}
                        errors={errors}
                      />
                      <FormTextField
                        vals={{
                          id: "githubid",
                          label: "Github Id",
                          type: "text",
                          placeholder: "john-doe",
                        }}
                        touched={touched}
                        errors={errors}
                      />
                    </div>

                    {/* SRM details */}
                    <div
                      className={
                        (handelVisibility(1) ? "invisible" : " ") + " absolute"
                      }
                    >
                      <label htmlFor="srmEmail">SRM Email</label>
                      <Field
                        type="text"
                        name="srmEmail"
                        placeholder="gs123@srmist.edu.in"
                        className={`
                      ${
                        touched.srmEmail && errors.srmEmail
                          ? "border-red-500"
                          : "border-gray-300"
                      } rounded-lg border-2 focus:border-gray-600 w-full py-2 px-4 bg-white text-gray-700 placeholder-gray-400 shadow-sm`}
                      />
                      <label htmlFor="regNo">Reg No.</label>
                      <Field
                        type="text"
                        name="regNo"
                        placeholder="RAXXXXXXXXXXXXX"
                        className={`
                      ${
                        touched.regNo && errors.regNo
                          ? "border-red-500"
                          : "border-gray-300"
                      } rounded-lg border-2 focus:border-gray-600 w-full py-2 px-4 bg-white text-gray-700 placeholder-gray-400 shadow-sm`}
                      />
                      <label htmlFor="branch">Branch</label>
                      <Field
                        type="text"
                        name="branch"
                        placeholder="CSE-BD"
                        className={`
                      ${
                        touched.branch && errors.branch
                          ? "border-red-500"
                          : "border-gray-300"
                      } rounded-lg border-2 focus:border-gray-600 w-full py-2 px-4 bg-white text-gray-700 placeholder-gray-400 shadow-sm`}
                      />
                    </div>

                    {/* Project */}
                    <div
                      className={
                        (handelVisibility(2) ? "invisible" : " ") + " absolute"
                      }
                    >
                      <label htmlFor="project">Project</label>
                      <Field
                        as="select"
                        name="project"
                        placeholder="Calculator"
                        className={`
                      ${
                        touched.githubid && errors.githubid
                          ? "border-red-500"
                          : "border-gray-300"
                      } rounded-lg border-2 focus:border-gray-600 w-full py-2 px-4 bg-white text-gray-700 placeholder-gray-400 shadow-sm`}
                      >
                        {Projects.map((project, i) => (
                          <option key={i} value={project}>
                            {project}
                          </option>
                        ))}
                      </Field>
                      <label htmlFor="feBug">Feature or Bugfix</label>
                      <Field
                        component="textarea"
                        name="feBug"
                        placeholder="Your project proposal"
                        rows="4"
                        cols="30"
                      />
                    </div>
                  </div>
                  <div>
                    {Object.keys(errors).map((error) => {
                      if (touched[error]) {
                        return (
                          <div className="text-red-500">{errors[error]}</div>
                        );
                      }
                    })}
                  </div>
                </div>

                <div className="flex flex-row">
                  {stage !== 0 && (
                    <button
                      type="button"
                      onClick={goBack}
                      className="py-2 px-4 text-base-black w-full transition ease-in duration-200 text-center text-base font-semibold ring-base-black focus:ring-purple-500 focus:ring-offset-purple-200 focus:outline-none ring-2 focus:ring-offset-2  rounded-lg mt-2"
                    >
                      Back
                    </button>
                  )}
                  <button
                    disabled={_disabled(errors, touched)}
                    type={stage === Sections.length - 1 ? "submit" : "button"}
                    onClick={goNext}
                    className={`py-2 px-4 bg-purple-600  hover:bg-purple-700 focus:ring-purple-500 focus:ring-offset-purple-200 text-white w-full transition ease-in duration-200 text-center text-base font-semibold  focus:outline-none focus:ring-2 focus:ring-offset-2  rounded-lg mt-2`}
                  >
                    {stage === Sections.length - 1 ? "Submit" : "Next"}
                  </button>
                </div>
              </Form>
            )}
          </Formik>
        </div>
      </div>
    </div>
  );
};

export default Register;
