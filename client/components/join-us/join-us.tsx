import React, { useState } from "react";
import { Formik, Form, Field } from "formik";
import * as Yup from "yup";

import { Section, Input } from "./";

import { InputProps } from "../../utils/interfaces";

const Register = () => {
  let [stage, setStage] = useState<number>(0);

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

  const goNext = () => {
    if (stage != sections.length - 1) {
      setStage(stage + 1);
    }
  };

  const goBack = () => {
    if (stage !== 0) {
      setStage(stage - 1);
    }
  };

  const disableButton = (errors, touched) => {
    // TODO change to one line
    const a =
      Object.keys(errors).filter((i, k) => touched[i]).length !== 0 ||
      Object.keys(touched).length === 0;
    console.log(
      a,
      Object.keys(errors).filter((i, k) => touched[i]),
      Object.keys(touched)
    );
    return a;
  };

  const projects: { value: string; name: string }[] = [
    { name: "Project 1", value: "project1" },
    { name: "Project 2", value: "project2" },
    { name: "Project 3", value: "project3" },
    { name: "Project 4", value: "project4" },
  ];

  const sections: { section: string; inputs: InputProps[] }[] = [
    {
      section: "Personal",
      inputs: [
        { id: "name", label: "Name", type: "text", placeholder: "GithubSRM" },
        {
          id: "githubid",
          label: "Github Id",
          type: "text",
          placeholder: "srm-ist-ktr",
        },
        {
          id: "email",
          label: "Email",
          type: "email",
          placeholder: "johndoe@mail.com",
        },
      ],
    },
    {
      section: "SRM Details",
      inputs: [
        {
          id: "srmEmail",
          label: "SRM Email",
          type: "text",
          placeholder: "gs123@srmist.edu.in",
        },
        {
          id: "regNo",
          label: "Reg No.",
          type: "text",
          placeholder: "RAXXXXXXXXXXXXX",
        },
        {
          id: "branch",
          label: "Branch",
          type: "text",
          placeholder: "CSE-BD",
        },
      ],
    },
    {
      section: "Projects",
      inputs: [
        {
          id: "project",
          label: "Project",
          type: "select",
          placeholder: "Calculator",
          selectOptions: { options: projects },
        },
        {
          id: "feBug",
          label: "Feature or Bugfix",
          type: "textarea",
          placeholder: "Your project proposal",
          textareaOptions: { rows: 4, cols: 30 },
        },
      ],
    },
  ];

  const errorInputId = (ids: string[], errors: string[]): boolean => {
    return ids.some((id) => errors.includes(id));
  };

  return (
    <div className="w-full">
      <div className="border-b-2 pb-4">
        <h1 className="font-montserrat font-medium text-2xl">Big text here</h1>
        <h3 className="font-montserrat font-medium text-base">
          small text here
        </h3>
      </div>

      <div className="w-3/4 p-4 mx-2">
        <Formik
          initialValues={initialValues}
          onSubmit={submitValues}
          validationSchema={validationSchema}
        >
          {({ errors, touched }) => (
            <Form className="w-full p-4 m-2">
              <div className="flex flex-col">
                {/* TODO: del 'this' button */}
                <button
                  type="button"
                  className="w-full bg-red-50"
                  onClick={() => {
                    console.log("errors", errors);
                    console.log("touched", touched);
                  }}
                >
                  print errors
                </button>

                <div className="w-1/4 mx-2 border-4">
                  {sections.map((item, index) => (
                    <Section
                      key={item.section}
                      name={item.section}
                      isActive={stage !== index}
                      setActive={() => setStage(index)}
                      onError={errorInputId(
                        item.inputs.map((i) => i.id),
                        Object.keys(errors).filter((i) => touched[i])
                      )}
                    />
                  ))}
                </div>

                <div className="h-72 relative">
                  {sections.map((section, index) => (
                    <div
                      key={`${section.inputs.length}_at_${index}`}
                      className={
                        (stage !== index ? "invisible" : " ") + " absolute"
                      }
                    >
                      {section.inputs.map((field) => (
                        <Input key={field.id} {...field} />
                      ))}
                    </div>
                  ))}
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

                {stage + 1 !== sections.length ? (
                  <button
                    type="button"
                    onClick={goNext}
                    className={`py-2 px-4 bg-purple-600 hover:bg-purple-700 focus:ring-purple-500 focus:ring-offset-purple-200 text-white w-full transition ease-in duration-200 text-center text-base font-semibold  focus:outline-none focus:ring-2 focus:ring-offset-2  rounded-lg mt-2`}
                  >
                    Next
                  </button>
                ) : (
                  <button
                    disabled={Object.keys(errors).length > 0}
                    type="submit"
                    onClick={goNext}
                    className={`py-2 px-4 bg-purple-600 hover:bg-purple-700 focus:ring-purple-500 focus:ring-offset-purple-200 text-white w-full transition ease-in duration-200 text-center text-base font-semibold  focus:outline-none focus:ring-2 focus:ring-offset-2  rounded-lg mt-2`}
                  >
                    Submit
                  </button>
                )}
              </div>
            </Form>
          )}
        </Formik>
      </div>
    </div>
  );
};

export default Register;
